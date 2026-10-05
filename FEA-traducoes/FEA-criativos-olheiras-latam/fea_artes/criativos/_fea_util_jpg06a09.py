"""Módulo de apoio (não gera arte sozinho). Complemento da fea_arte_lib para o lote [FEED]/[STORIES] ADS 06 a 09 (jpg).

Texto rico numa linha (trechos com fonte, cor e sublinhado diferentes, como
'Com um ebook que mostra **o raciocínio clínico**'), espaçamento entre letras
(tracking) e texto em arco (selo dourado). Tudo desenhado com Pillow, sem IA.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fea_arte_lib import fonte, mascara

_cache = {}


def F(nome, tamanho):
    k = (nome, round(tamanho * 4) / 4)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(fonte(nome), k[1])
    return _cache[k]


def larg(texto, nome, tamanho, tracking=0.0):
    f = F(nome, tamanho)
    if not texto:
        return 0.0
    return f.getlength(texto) + tracking * (len(texto) - 1)


def largura_segs(segs, tamanho, tracking=0.0):
    """segs: [(texto, nome_fonte, cor, sublinhado)]. Largura total da linha."""
    tot = 0.0
    for i, (t, n, _, _) in enumerate(segs):
        tot += larg(t, n, tamanho, tracking)
        if i < len(segs) - 1:
            tot += tracking
    return tot


def tinta(segs, tamanho, tracking=0.0):
    """(esquerda, direita) da tinta real em relação à origem da linha."""
    l = F(segs[0][1], tamanho).getbbox(segs[0][0][0], anchor='ls')[0]
    ult = segs[-1]
    r_ult = F(ult[1], tamanho).getbbox(ult[0][-1], anchor='ls')[2] - F(ult[1], tamanho).getlength(ult[0][-1])
    return l, largura_segs(segs, tamanho, tracking) + r_ult


def desenhar(im, segs, tamanho, base, x0, x1=None, alinh='centro', tracking=0.0,
             sub_desc=None, sub_esp=None):
    """Desenha a linha com linha de base 'base'. alinh centro usa (x0+x1)/2, esquerda usa x0
    como borda da tinta, direita usa x1. Retorna (x_tinta_ini, x_tinta_fim)."""
    d = ImageDraw.Draw(im)
    l, r = tinta(segs, tamanho, tracking)
    if alinh == 'esquerda':
        x = x0 - l
    elif alinh == 'direita':
        x = x1 - r
    else:
        x = (x0 + x1) / 2 - (r + l) / 2
    ini = x + l
    sub_desc = tamanho * 0.11 if sub_desc is None else sub_desc
    sub_esp = max(1, round(tamanho * 0.06)) if sub_esp is None else sub_esp
    for i, (t, n, cor, sub) in enumerate(segs):
        f = F(n, tamanho)
        xs = x
        if tracking:
            for ch in t:
                d.text((x, base), ch, font=f, fill=cor, anchor='ls')
                x += f.getlength(ch) + tracking
            x -= tracking
        else:
            d.text((x, base), t, font=f, fill=cor, anchor='ls')
            x += f.getlength(t)
        if sub:
            tt = t.rstrip()
            xe = xs + larg(tt, n, tamanho, tracking)
            xb = xs + (f.getbbox(t[0], anchor='ls')[0] if t[0] != ' ' else f.getlength(' '))
            d.rectangle([xb, base + sub_desc, xe, base + sub_desc + sub_esp - 1], fill=cor)
        if i < len(segs) - 1:
            x += tracking
    return ini, x + r - largura_segs(segs, tamanho, tracking)


def base_de(ytop, texto_pt, nome, tamanho):
    """Linha de base a partir do topo medido da linha original (mesmo método de escrever())."""
    return ytop - F(nome, tamanho).getbbox(texto_pt, anchor='ls')[1]


def tamanho_por_largura(texto, nome, largura, tracking=0.0):
    melhor = None
    for t in np.arange(8, 200, 0.25):
        f = F(nome, float(t))
        l = f.getbbox(texto[0], anchor='ls')[0]
        r = f.getlength(texto[:-1]) + f.getbbox(texto[-1], anchor='ls')[2] + tracking * (len(texto) - 1)
        w = r - l
        if melhor is None or abs(w - largura) < abs(melhor[1] - largura):
            melhor = (float(t), w)
    return melhor[0]


def tamanho_segs(segs, largura, tracking=0.0):
    melhor = None
    for t in np.arange(8, 200, 0.25):
        l, r = tinta(segs, float(t), tracking)
        if melhor is None or abs((r - l) - largura) < abs(melhor[1] - largura):
            melhor = (float(t), r - l)
    return melhor[0]


def comparar(im, caixa, cond, texto, nomes, tracking=0.0):
    """Nota de semelhança (IoU) do recorte com cada fonte candidata, já no tamanho calibrado."""
    m = mascara(im, caixa, cond)
    ys, xs = np.where(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    out = []
    for n in nomes:
        t = tamanho_por_largura(texto, n, m.shape[1], tracking)
        c = Image.new('L', (m.shape[1] + 400, m.shape[0] + 200), 0)
        segs = [(texto, n, 255, False)]
        desenhar(c, segs, t, 150, 100, alinh='esquerda', tracking=tracking)
        a = np.array(c) > 110
        yy, xx = np.where(a)
        a = a[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
        a = np.array(Image.fromarray(a.astype(np.uint8) * 255).resize((m.shape[1], m.shape[0]))) > 127
        iou = (a & m).sum() / max(1, (a | m).sum())
        out.append((round(float(iou), 3), n, t, a.shape, m.shape))
    return sorted(out, reverse=True)


def texto_arco(im, texto, nome, tamanho, cor, centro, raio, ang_centro=-90.0, tracking=0.0,
               por_fora=True, sombra=None):
    """Texto ao longo de um arco. raio = raio da linha de base. ang_centro em graus (−90 = topo).
    por_fora=True: letras de pé, lidas no sentido horário (arco superior).
    por_fora=False: arco inferior, lido da esquerda para a direita, letras com o pé para fora."""
    f = F(nome, tamanho)
    larguras = [f.getlength(ch) for ch in texto]
    total = sum(larguras) + tracking * (len(texto) - 1)
    cx, cy = centro
    s = -total / 2
    for ch, w in zip(texto, larguras):
        meio = s + w / 2
        if por_fora:
            ang = ang_centro + math.degrees(meio / raio)
        else:
            ang = ang_centro - math.degrees(meio / raio)
        rad = math.radians(ang)
        px, py = cx + raio * math.cos(rad), cy + raio * math.sin(rad)
        if ch.strip():
            tam = int(tamanho * 3)
            ix, iy = math.floor(px - tam / 2), math.floor(py - tam / 2)
            ox, oy = px - ix, py - iy  # posição subpixel dentro da camada
            cam = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
            dc = ImageDraw.Draw(cam)
            if sombra:
                dc.text((ox + sombra[1][0], oy + sombra[1][1]), ch, font=f, fill=tuple(sombra[0]) + (255,), anchor='ms')
            dc.text((ox, oy), ch, font=f, fill=tuple(cor) + (255,), anchor='ms')
            rot = ang + 90 if por_fora else ang - 90
            r = cam.rotate(-rot, resample=Image.BICUBIC, center=(ox, oy))
            im.paste(r, (ix, iy), r)
        s += w + tracking
    return im


def _marrom(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g) & (g > b) & (r < 165) & (r - b > 25)


def trocar_selo(im, cx, cy, r0, r1, texto_pt, texto_es, nome_fonte='Montserrat_700Bold',
                ang_lim=(-178, -2), dil=2, ajuste_ang=0.0, inpaint=None, escala=0.88, dr=0.0, ang_fixo=None):
    """Troca o texto do arco superior do selo dourado (letras marrons de pé sobre o arco).
    (cx, cy) centro do selo; r0..r1 faixa radial das letras (r0 = linha de base).
    Mede extensão angular, cor e tamanho do texto PT e escreve o ES no mesmo raio,
    mesmo tamanho, mesmo espaçamento e mesmo eixo central. inpaint: função
    (im, mascara_uint8) -> im; padrão OpenCV Telea."""
    import cv2
    a = np.array(im)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.hypot(xx - cx, yy - cy)
    ang = np.degrees(np.arctan2(yy - cy, xx - cx))
    sel = _marrom(a.astype(int)) & (dd >= r0 - 1) & (dd <= r1 + 1) & (ang > ang_lim[0]) & (ang < ang_lim[1])
    h, e = np.histogram(ang[sel], bins=np.arange(-180, 181, 1))
    on = np.where(h >= 3)[0]
    # maior bloco contínuo de graus com tinta (lacunas < 9°)
    blocos, ini = [], 0
    for i in range(1, len(on) + 1):
        if i == len(on) or on[i] - on[i - 1] > 9:
            blocos.append((e[on[ini]], e[on[i - 1] + 1], h[on[ini]:on[i - 1] + 1].sum()))
            ini = i
    a0, a1, _ = max(blocos, key=lambda b: b[2])
    if ang_fixo:  # selo cortado pela borda da arte: extensão conhecida dos outros selos
        a0, a1 = ang_fixo
    meio = (a0 + a1) / 2 + ajuste_ang
    sel &= (ang >= a0 - 1) & (ang <= a1 + 1)
    px = a[sel].astype(int)
    lum = px.sum(1)
    cor = tuple(int(v) for v in np.median(px[lum <= np.percentile(lum, 35)], 0))
    # apagar
    m = sel.astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    m[(dd < r0 - 4) | (dd > r1 + 4)] = 0
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, 5, cv2.INPAINT_TELEA)
    novo = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    im.paste(novo)
    # tamanho pela altura de maiúscula, tracking pela extensão angular do PT
    f1 = F(nome_fonte, 100)
    cap = -f1.getbbox('H', anchor='ls')[1] / 100
    tam = (r1 - r0 + 1) / cap * escala
    arco = np.radians(a1 - a0) * (r0 + (r1 - r0) * 0.35)
    tr = (arco - larg(texto_pt, nome_fonte, tam)) / (len(texto_pt) - 1)
    texto_arco(im, texto_es, nome_fonte, tam, cor, (cx, cy), r0 + dr, ang_centro=meio, tracking=tr)
    return dict(ang=(round(float(a0), 1), round(float(a1), 1)), cor=cor, tam=round(tam, 2), tracking=round(float(tr), 2))


def apagar_mascara(im, m, raio=4):
    import cv2
    a = np.array(im)
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, raio, cv2.INPAINT_TELEA)
    im.paste(Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)))
    return im


def tirar_acento(im, caixa):
    """Apaga só os pixels escuros do acento dentro da caixa (ex.: CÓPIAS -> COPIAS no selo).
    A caixa deve parar logo acima da letra. Os pixels do acento recebem a cor do fundo
    dourado ao redor (mediana), com borda suavizada."""
    import cv2
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    sub = a[y0:y1, x0:x1].astype(int)
    lum = sub.sum(2)
    m = (lum < np.median(lum) - 40).astype(np.uint8)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8))
    fundo = np.median(sub[m == 0], 0) if (m == 0).any() else np.median(a[y0 - 3:y0, x0:x1].reshape(-1, 3), 0)
    peso = cv2.GaussianBlur(m.astype(float), (3, 3), 0.6)
    peso = np.maximum(peso, m)[..., None]
    sub = sub * (1 - peso) + fundo * peso
    a[y0:y1, x0:x1] = np.clip(sub, 0, 255).astype(np.uint8)
    im.paste(Image.fromarray(a))
    return im


def selo_es(im, cx, cy, r0, r1, acento, **kw):
    """Selo dourado: 'O PRIMEIRO & MAIS VENDIDO' -> 'MÉTODO EXCLUSIVO DEL' (arco superior;
    o arco inferior 'DR. JOÃO PITHON' já completa a frase) e CÓPIAS -> COPIAS."""
    info = trocar_selo(im, cx, cy, r0, r1, 'O PRIMEIRO & MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL', **kw)
    tirar_acento(im, acento)
    return info


def caixa_esticada(im, caixa, largura_nova, cond_texto, borda=24, dil=2, x0_novo=None):
    """Botão com borda/degradê (não chapado): apaga o texto por inpainting dentro da caixa
    e, se precisar de mais largura, estica só o miolo (bordas laterais preservadas),
    mantendo o centro. Retorna a nova caixa."""
    from fea_arte_lib import apagar
    x0, y0, x1, y1 = caixa
    im.paste(apagar(im, (x0 + 4, y0 + 4, x1 - 4, y1 - 4), cond_texto, dil))
    w = x1 - x0
    if largura_nova <= w:
        return caixa
    largura_nova = int(round(largura_nova))
    bx = im.crop(caixa)
    esq, dir_ = bx.crop((0, 0, borda, y1 - y0)), bx.crop((w - borda, 0, w, y1 - y0))
    meio = bx.crop((borda, 0, w - borda, y1 - y0)).resize((largura_nova - 2 * borda, y1 - y0), Image.BICUBIC)
    nx0 = int(round((x0 + x1) / 2 - largura_nova / 2)) if x0_novo is None else int(x0_novo)
    im.paste(esq, (nx0, y0))
    im.paste(meio, (nx0 + borda, y0))
    im.paste(dir_, (nx0 + largura_nova - borda, y0))
    return (nx0, y0, nx0 + largura_nova, y1)


def quebrar(texto, nome, tamanho, largura):
    """Quebra o texto em linhas que caibam na largura (por palavra)."""
    linhas, atual = [], ''
    for p in texto.split():
        t = (atual + ' ' + p).strip()
        if atual and larg(t, nome, tamanho) > largura:
            linhas.append(atual)
            atual = p
        else:
            atual = t
    if atual:
        linhas.append(atual)
    return linhas


def legenda_depoimento(im, traducao, x0, x1, y_topo, nome='NotoSans_400Regular', nome_it='NotoSans_400Regular_Italic',
                       tamanho=21, cor=(170, 192, 180), entrelinha=1.35, alinh='esquerda', continuo=False):
    """Regra 4: print original em PT + legenda pequena em ES abaixo.
    'Testimonio original en portugués:' (regular) e a tradução entre «» (itálico)."""
    f = F(nome, tamanho)
    asc = -f.getbbox('Tt', anchor='ls')[1]
    base = y_topo + asc
    passo = tamanho * entrelinha
    if continuo:  # pouco espaço (feed): rótulo e tradução no mesmo parágrafo
        rot = 'Testimonio original en portugués:'
        for i, l in enumerate(quebrar(rot + ' «' + traducao + '»', nome, tamanho, x1 - x0)):
            if i == 0 and l.startswith(rot):
                segs = [(rot, nome, cor, False)] + ([(l[len(rot):], nome_it, cor, False)] if len(l) > len(rot) else [])
            else:
                segs = [(l, nome_it, cor, False)]
            desenhar(im, segs, tamanho, base, x0, x1, alinh=alinh)
            base += passo
        return base - passo
    for l in quebrar('Testimonio original en portugués:', nome, tamanho, x1 - x0):
        desenhar(im, [(l, nome, cor, False)], tamanho, base, x0, x1, alinh=alinh)
        base += passo
    for l in quebrar('«' + traducao + '»', nome_it, tamanho, x1 - x0):
        desenhar(im, [(l, nome_it, cor, False)], tamanho, base, x0, x1, alinh=alinh)
        base += passo
    return base - passo


def faixa(im, caixa, segs_pt, segs_es, ytop, x0t, x1t, nome_cor=None):
    """Caixa chapada com uma linha de texto (faixa amarela, CTA). Alarga a caixa se precisar."""
    from fea_arte_lib import cor_fundo, cor_texto, preencher, ESCURO
    cor_cx = cor_fundo(im, (caixa[0] + 3, caixa[1] + 3, caixa[2] - 3, caixa[1] + 8))
    cor_tx = cor_texto(im, (x0t, ytop, x1t, caixa[3] - 3), ESCURO)
    tam = tamanho_segs(segs_pt[0], x1t - x0t + 1, segs_pt[1])
    tr = segs_pt[1]
    pad = x0t - caixa[0]
    segs = [(t, n, cor_tx, s) for t, n, _, s in segs_es]
    while True:
        l, r = tinta(segs, tam, tr)
        if (r - l) + 2 * pad <= im.width - 2 * 16 or tam < 10:
            break
        tam -= 0.25
    base = base_de(ytop, segs_pt[0][0][0] + segs_pt[0][-1][0], segs_pt[0][0][1], tam)
    preencher(im, caixa, cor_cx)
    cx = (caixa[0] + caixa[2]) / 2
    w = max(caixa[2] - caixa[0], (r - l) + 2 * pad)
    preencher(im, (int(round(cx - w / 2)), caixa[1], int(round(cx + w / 2)), caixa[3]), cor_cx)
    desenhar(im, segs, tam, base, caixa[0], caixa[2], 'centro', tr)
    return tam
