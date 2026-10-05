"""Funções auxiliares dos criativos jpg [FEED]/[STORIES] ADS 14 a ADS 20 (Ebook Olheiras LATAM).

Módulo de apoio (não gera arte sozinho; rodar_todos.py o executa sem efeito).
Complementa fea_arte_lib com:
- linha rica: trechos com fonte, cor ou degradê diferentes na mesma linha, com tracking;
- degradê vertical amostrado do próprio texto original (dourado metálico) e reaplicado;
- transplante de glifo: letra do próprio original (mesma fonte, mesma textura) copiada
  para outra posição por diferença (original menos fundo limpo), sem redesenhar;
- texto em arco para o selo dourado (troca do arco superior) e remoção do acento de CÓPIAS.
Nada aqui usa IA generativa: só desenho vetorial (Pillow) e inpainting clássico (OpenCV Telea).
"""
import math, os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *  # noqa

_cache = {}


def F(nome, tam):
    k = (nome, round(float(tam) * 4) / 4)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(fonte(nome), k[1])
    return _cache[k]


# ---------- medição ----------
def colunas(im, caixa, cond, gap=1):
    """Faixas horizontais (x0, x1) com tinta na caixa (letras separadas)."""
    m = mascara(im, caixa, cond)
    c = m.any(0)
    runs, s, vazio = [], None, 0
    for i, v in enumerate(list(c) + [False] * (gap + 1)):
        if v:
            if s is None:
                s = i
            vazio, ult = 0, i
        elif s is not None:
            vazio += 1
            if vazio >= gap:
                runs.append((s + caixa[0], ult + caixa[0]))
                s = None
    return runs


def degrade(im, caixa, cond):
    """Cor mediana do núcleo do texto por linha da caixa: [(y, (r, g, b))]."""
    x0, y0, x1, y1 = caixa
    a = np.array(im)[y0:y1, x0:x1].astype(int)
    m = cond(a[..., 0], a[..., 1], a[..., 2])
    m = cv2.erode(m.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(bool)
    out = []
    for i in range(a.shape[0]):
        px = a[i][m[i]]
        if len(px) >= 3:
            out.append((y0 + i, tuple(np.median(px, 0))))
    return out


def grad_rel(im, caixa, cond):
    """Degradê normalizado: [(t, cor)] com t=0 no topo e t=1 na base da tinta medida."""
    g = degrade(im, caixa, cond)
    ys = [y for y, _ in g]
    a, b = min(ys), max(ys)
    return [((y - a) / max(1, b - a), c) for y, c in g]


def _cor_em(grad, t):
    ts = [x for x, _ in grad]
    cs = np.array([c for _, c in grad], float)
    return tuple(np.interp(t, ts, cs[:, k]) for k in range(3))


# ---------- escrita ----------
def larg_seg(t, f, tr):
    if not t:
        return 0.0
    return sum(f.getlength(c) for c in t) + tr * (len(t) - 1) if tr else f.getlength(t)


def tinta_segs(segs, tr=0.0):
    """(esq, dir) da tinta em relação à origem. segs: [(texto, nome_fonte, tam, cor)]."""
    f0 = F(segs[0][1], segs[0][2])
    l = f0.getbbox(segs[0][0][0], anchor='ls')[0]
    x = 0.0
    for i, s in enumerate(segs):
        f = F(s[1], s[2])
        x += larg_seg(s[0], f, tr) + (tr if i < len(segs) - 1 else 0)
    fl = F(segs[-1][1], segs[-1][2])
    ch = segs[-1][0][-1]
    r = x - fl.getlength(ch) + fl.getbbox(ch, anchor='ls')[2]
    return l, r


def largura_segs(segs, tr=0.0):
    l, r = tinta_segs(segs, tr)
    return r - l


def _mascara_seg(W, H, t, f, nome, tam, cx, base, tr, peso):
    """Máscara L do trecho. peso > 0 engrossa o traço (px) via superamostragem 4x + dilatação."""
    if not peso:
        L = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(L)
        if tr:
            xx = cx
            for c in t:
                d.text((xx, base), c, font=f, fill=255, anchor='ls')
                xx += f.getlength(c) + tr
        else:
            d.text((cx, base), t, font=f, fill=255, anchor='ls')
        return L
    from PIL import ImageFilter
    S = 4
    x0 = int(cx - tam); y0 = int(base - tam * 1.6)
    w = int(larg_seg(t, f, tr) + tam * 2); h = int(tam * 2.4)
    f4 = F(nome, tam * S)
    L4 = Image.new('L', (w * S, h * S), 0)
    d = ImageDraw.Draw(L4)
    if tr:
        xx = (cx - x0) * S
        for c in t:
            d.text((xx, (base - y0) * S), c, font=f4, fill=255, anchor='ls')
            xx += f4.getlength(c) + tr * S
    else:
        d.text(((cx - x0) * S, (base - y0) * S), t, font=f4, fill=255, anchor='ls')
    k = int(round(peso * S)) * 2 + 1
    if k > 1:
        L4 = L4.filter(ImageFilter.MaxFilter(k))
    sm = L4.resize((w, h), Image.BOX)
    L = Image.new('L', (W, H), 0)
    L.paste(sm, (x0, y0))
    return L


def linha(im, segs, base, x, alinh='esquerda', tr=0.0, peso=0.0, sombra=None):
    """Escreve segmentos na linha de base 'base'. x = borda da tinta (esquerda/direita) ou centro.
    cor do segmento: tupla RGB ou ('grad', [(t, cor)], y_topo, y_base) para degradê vertical
    (t=0 em y_topo, t=1 em y_base). Retorna (x_ini_tinta, x_fim_tinta)."""
    l, r = tinta_segs(segs, tr)
    if alinh == 'esquerda':
        ox = x - l
    elif alinh == 'direita':
        ox = x - r
    else:
        ox = x - (l + r) / 2
    W, H = im.size
    a = np.array(im).astype(np.float32)
    cx = ox
    for i, (t, nome, tam, cor) in enumerate(segs):
        f = F(nome, tam)
        L = _mascara_seg(W, H, t, f, nome, tam, cx, base, tr, peso)
        if sombra:  # (dx, dy, desfoque, opacidade, cor)
            from PIL import ImageFilter
            dx, dy, bl, op = sombra[:4]
            cs = np.array(sombra[4] if len(sombra) > 4 else (0, 0, 0), np.float32)
            Ls = Image.new('L', (W, H), 0)
            Ls.paste(L, (int(dx), int(dy)))
            Ls = Ls.filter(ImageFilter.GaussianBlur(bl)) if bl else Ls
            als = np.array(Ls).astype(np.float32)[..., None] / 255 * op
            a = a * (1 - als) + cs * als
        al = np.array(L).astype(np.float32)[..., None] / 255
        if isinstance(cor, tuple) and len(cor) == 4 and cor[0] == 'grad':
            _, grad, yt, yb = cor
            rows = np.arange(H)
            tt = np.clip((rows - yt) / max(1, yb - yt), 0, 1)
            ci = np.array([_cor_em(grad, v) for v in tt], np.float32)
            cimg = np.broadcast_to(ci[:, None, :], a.shape)
        else:
            cimg = np.array(cor, np.float32)
        a = a * (1 - al) + cimg * al
        cx += larg_seg(t, f, tr) + (tr if i < len(segs) - 1 else 0)
    im.paste(Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)))
    return ox + l, ox + r


def base_de(nome, tam, texto_pt, y_topo):
    return y_topo - F(nome, tam).getbbox(texto_pt, anchor='ls')[1]


def tam_por_largura(segs_fn, largura, tr=0.0, lo=6, hi=220):
    """segs_fn(tam) -> segs. Tamanho em que a tinta tem a largura dada."""
    for _ in range(40):
        mid = (lo + hi) / 2
        if largura_segs(segs_fn(mid), tr) > largura:
            hi = mid
        else:
            lo = mid
    return round(lo * 4) / 4


def tam_por_cap(nome, altura, ref='H'):
    f = F(nome, 100)
    _, t, _, b = f.getbbox(ref, anchor='ls')
    return 100 * altura / (b - t)


def caber(segs_fn, tam, largura_max, reducao_max=0.15, tr=0.0):
    """Reduz o tamanho (no máximo reducao_max) até a linha caber. Retorna o tamanho."""
    t = tam
    while largura_segs(segs_fn(t), tr) > largura_max and t > tam * (1 - reducao_max):
        t -= 0.25
    return t


# ---------- transplante de glifo ----------
def transplantar(dst, src, limpo, caixa_src, x_dst, y_dst):
    """Copia a diferença (src - limpo) da caixa_src para dst na posição (x_dst, y_dst) do canto
    superior esquerdo. Reproduz a letra original com a mesma textura sobre o fundo de dst."""
    x0, y0, x1, y1 = caixa_src
    s = np.array(src).astype(np.float32)[y0:y1, x0:x1]
    c = np.array(limpo).astype(np.float32)[y0:y1, x0:x1]
    d = np.array(dst).astype(np.float32)
    h, w = s.shape[:2]
    d[y_dst:y_dst + h, x_dst:x_dst + w] += s - c
    dst.paste(Image.fromarray(np.clip(d + 0.5, 0, 255).astype(np.uint8)))
    return dst


# ---------- selo ----------
def texto_arco(im, texto, nome, tamanho, cor, centro, raio, ang_centro=-90.0, tracking=0.0, por_fora=True):
    """Texto ao longo de um arco (raio = linha de base). ang_centro em graus (-90 = topo)."""
    f = F(nome, tamanho)
    larguras = [f.getlength(ch) for ch in texto]
    total = sum(larguras) + tracking * (len(texto) - 1)
    cx, cy = centro
    s = -total / 2
    for ch, w in zip(texto, larguras):
        meio = s + w / 2
        ang = ang_centro + math.degrees(meio / raio) if por_fora else ang_centro - math.degrees(meio / raio)
        rad = math.radians(ang)
        px, py = cx + raio * math.cos(rad), cy + raio * math.sin(rad)
        if ch.strip():
            tam = int(tamanho * 3)
            cam = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
            ImageDraw.Draw(cam).text((tam / 2, tam / 2), ch, font=f, fill=tuple(int(v) for v in cor) + (255,), anchor='ms')
            rot = ang + 90 if por_fora else ang - 90
            r = cam.rotate(-rot, resample=Image.BICUBIC, center=(tam / 2, tam / 2))
            im.paste(r, (int(round(px - tam / 2)), int(round(py - tam / 2))), r)
        s += w + tracking
    return im


def marrom(r, g, b):
    return (r > g) & (g > b) & (r < 170) & (r - b > 25)


def trocar_arco_selo(im, cx, cy, r0, r1, texto_pt, texto_es, nome_fonte, ang_lim=(-178, -2),
                     dil=2, escala=0.88, cond=marrom, ajuste_ang=0.0, dr=0.0):
    """Troca o texto do arco superior do selo (letras de pé, lidas em sentido horário).
    (cx, cy) centro; r0..r1 faixa radial das letras (r0 = linha de base). Mede extensão angular,
    cor e tamanho do PT; escreve o ES no mesmo raio, mesmo tamanho e mesmo eixo central."""
    a = np.array(im)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.hypot(xx - cx, yy - cy)
    ang = np.degrees(np.arctan2(yy - cy, xx - cx))
    ai = a.astype(int)
    sel = cond(ai[..., 0], ai[..., 1], ai[..., 2]) & (dd >= r0 - 1) & (dd <= r1 + 1) & (ang > ang_lim[0]) & (ang < ang_lim[1])
    angs = ang[sel]
    a0, a1 = np.percentile(angs, 0.5), np.percentile(angs, 99.5)
    meio = (a0 + a1) / 2 + ajuste_ang
    px = a[sel].astype(int)
    lum = px.sum(1)
    cor = tuple(int(v) for v in np.median(px[lum <= np.percentile(lum, 35)], 0))
    m = sel.astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    m[(dd < r0 - 4) | (dd > r1 + 4)] = 0
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, 5, cv2.INPAINT_TELEA)
    im.paste(Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)))
    f1 = F(nome_fonte, 100)
    cap = -f1.getbbox('H', anchor='ls')[1] / 100
    tam = (r1 - r0 + 1) / cap * escala
    arco = np.radians(a1 - a0) * (r0 + (r1 - r0) * 0.35)
    tr = (arco - larg_seg(texto_pt, F(nome_fonte, tam), 0)) / (len(texto_pt) - 1)
    larg_es = larg_seg(texto_es, F(nome_fonte, tam), tr)
    if larg_es > arco * 1.02:  # não cabe no mesmo arco: reduz o tracking, depois a fonte
        tr = max(0.0, (arco - larg_seg(texto_es, F(nome_fonte, tam), 0)) / (len(texto_es) - 1))
        while larg_seg(texto_es, F(nome_fonte, tam), tr) > arco * 1.02 and tam > 5:
            tam -= 0.25
    texto_arco(im, texto_es, nome_fonte, tam, cor, (cx, cy), r0 + dr, ang_centro=meio, tracking=tr)
    return dict(ang=(round(float(a0), 1), round(float(a1), 1)), cor=cor, tam=round(tam, 2), tracking=round(float(tr), 2))


def apagar_componentes(im, caixa, cond, filtro, folga=3, dil=2, raio=4):
    """Apaga componentes conectados da caixa que passam no filtro((x0, y0, x1, y1, area))."""
    m = mascara(im, caixa, cond).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    achados = []
    for i in range(1, n):
        c = (int(st[i][0] + caixa[0]), int(st[i][1] + caixa[1]), int(st[i][0] + st[i][2] + caixa[0]),
             int(st[i][1] + st[i][3] + caixa[1]), int(st[i][4]))
        if filtro(c):
            achados.append(c)
    for c in achados:
        im = apagar(im, (c[0] - folga, c[1] - folga, c[2] + folga, c[3] + folga), cond, dil, raio)
    return im, achados


def componentes(im, caixa, cond):
    m = mascara(im, caixa, cond).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    return [(int(st[i][0] + caixa[0]), int(st[i][1] + caixa[1]), int(st[i][0] + st[i][2] + caixa[0]),
             int(st[i][1] + st[i][3] + caixa[1]), int(st[i][4])) for i in range(1, n)]


def dividir_preco(p):
    """'US$ [PRECIO]' -> ('US$', '[PRECIO]'); 'US$19,00' -> ('US$', '19,00')."""
    p = p.strip()
    for moeda in ('US$', 'USD', '$'):
        if p.startswith(moeda):
            return moeda, p[len(moeda):].strip()
    return '', p


def zoom(im, caixa, caminho, fator=2):
    c = im.crop(caixa)
    c.resize((c.width * fator, c.height * fator), Image.LANCZOS).save(caminho)
    return caminho


def colocar(im, im0, limpo, glifos, seq, x, y_lin, gaps, m=3):
    """Transplanta a sequência de glifos (chaves de 'glifos': (x0, x1, (y0, y1))) a partir de x,
    com o topo da caixa de recorte em y_lin. gaps: espaço entre tintas, um por glifo. Retorna x final."""
    for k, gap in zip(seq, gaps):
        x0, x1, (y0, y1) = glifos[k]
        transplantar(im, im0, limpo, (x0 - m, y0, x1 + m + 1, y1), x - m, y_lin)
        x = x + (x1 - x0) + 1 + gap
    return x


def track_para(texto, nome, tam, largura):
    """Tracking que faz 'texto' ocupar 'largura' de tinta."""
    w0 = largura_segs([(texto, nome, tam, (0, 0, 0))], 1e-9)
    return (largura - w0) / (len(texto) - 1)


def cor_nucleo(im, caixa, cond, pct=30, escuro=True):
    """Cor do miolo das letras: mediana dos pixels mais escuros (ou mais claros) que passam em cond."""
    a = np.array(im)[caixa[1]:caixa[3], caixa[0]:caixa[2]].astype(int)
    px = a[cond(a[..., 0], a[..., 1], a[..., 2])]
    lum = px.sum(1)
    sel = px[lum <= np.percentile(lum, pct)] if escuro else px[lum >= np.percentile(lum, 100 - pct)]
    return tuple(int(v) for v in np.median(sel, 0))
