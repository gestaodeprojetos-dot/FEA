"""Utilitários dos criativos jpg do lote [FEED]/[STORIES] ADS 01 a 05 (Ebook Olheiras LATAM).

Módulo de apoio (não gera arte sozinho). Complementa fea_arte_lib com:
- texto em linha rica (trechos com fonte/cor diferentes na mesma linha, sublinhado, riscado);
- linha de base calculada a partir do topo medido do texto PT original;
- pílula de preço desenhada (fundo arredondado, borda, sombra) com largura dinâmica,
  para caber o preço de precos.json sem cortar texto.
Nada aqui usa IA generativa: só desenho vetorial (Pillow) e inpainting clássico (OpenCV).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *  # noqa
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = lambda nome, tam: ImageFont.truetype(fonte(nome), tam)


def base_de(f, texto_pt, y_topo):
    """Linha de base que reproduz o topo medido (y_topo) do texto PT na fonte f."""
    return y_topo - f.getbbox(texto_pt, anchor='ls')[1]


def largura(segs):
    return sum(s[1].getlength(s[0]) for s in segs)


def linha(im, x, base, segs, alinhamento='esquerda', sub_esp=None):
    """segs: [(texto, fonte, cor, efeito)] efeito None | 'sub' (sublinhado) | 'risco' (riscado, cor do risco em sub_esp).
    x: borda esquerda (alinhamento esquerda), centro ('centro') ou borda direita ('direita')."""
    d = ImageDraw.Draw(im)
    w = largura(segs)
    x0 = x if alinhamento == 'esquerda' else (x - w / 2 if alinhamento == 'centro' else x - w)
    cx = x0
    for s in segs:
        txt, f, cor = s[0], s[1], s[2]
        ef = s[3] if len(s) > 3 else None
        d.text((cx, base), txt, font=f, fill=cor, anchor='ls')
        lw = f.getlength(txt)
        if ef == 'sub':
            ini = cx + (f.getlength(txt) - f.getlength(txt.lstrip()))
            fim = cx + f.getlength(txt.rstrip())
            esp = max(2, round(f.size / 22))
            y = base + round(f.size * 0.13)
            d.rectangle([ini, y, fim, y + esp - 1], fill=cor)
        elif ef == 'risco':
            ini = cx + (f.getlength(txt) - f.getlength(txt.lstrip()))
            fim = cx + f.getlength(txt.rstrip())
            t = f.getbbox('R', anchor='ls')[1]
            y = base + t * 0.42
            esp = max(2, round(f.size / 14))
            d.rectangle([ini - 1, y - esp / 2, fim + 1, y + esp / 2], fill=sub_esp or cor)
        cx += lw
    return x0, x0 + w


def mascara_texto(im, caixa, cond, dil=3):
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    m = np.zeros(a.shape[:2], np.uint8)
    sub = a[y0:y1, x0:x1].astype(int)
    m[y0:y1, x0:x1] = cond(sub[..., 0], sub[..., 1], sub[..., 2]).astype(np.uint8) * 255
    return cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))


def apagar_mascara(im, m, raio=6):
    a = np.array(im)
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def mascara_pilula(tam, caixa, raio=None, ss=4):
    """Máscara L (0 a 255) de retângulo arredondado com antisserrilhado."""
    x0, y0, x1, y1 = caixa
    raio = (y1 - y0) / 2 if raio is None else raio
    W, H = tam
    m = Image.new('L', (W * ss // ss, H), 0)
    big = Image.new('L', ((int(x1) - int(x0) + 4) * ss, (int(y1) - int(y0) + 4) * ss), 0)
    ImageDraw.Draw(big).rounded_rectangle([2 * ss, 2 * ss, (x1 - int(x0) + 2) * ss - 1, (y1 - int(y0) + 2) * ss - 1], radius=raio * ss, fill=255)
    big = big.resize((big.width // ss, big.height // ss), Image.LANCZOS)
    m.paste(big, (int(x0) - 2, int(y0) - 2))
    return m


def compor(im, mask_l, cor, alpha=1.0):
    """Pinta cor sobre im com máscara L (0 a 255) multiplicada por alpha."""
    camada = Image.new('RGB', im.size, cor)
    m = mask_l.point(lambda v: int(v * alpha))
    return Image.composite(camada, im, m)


def borda_pilula(im, caixa, cor, alpha, esp=2, raio=None):
    ext = mascara_pilula(im.size, caixa, raio)
    x0, y0, x1, y1 = caixa
    r = (y1 - y0) / 2 if raio is None else raio
    inn = mascara_pilula(im.size, (x0 + esp, y0 + esp, x1 - esp, y1 - esp), max(1, r - esp))
    anel = Image.fromarray(np.clip(np.array(ext).astype(int) - np.array(inn).astype(int), 0, 255).astype(np.uint8))
    return compor(im, anel, cor, alpha)


def sombra_pilula(im, caixa, cor=(0, 0, 0), alpha=0.18, dy=4, blur=6, raio=None):
    x0, y0, x1, y1 = caixa
    m = mascara_pilula(im.size, (x0, y0 + dy, x1, y1 + dy), raio).filter(ImageFilter.GaussianBlur(blur))
    return compor(im, m, cor, alpha)


CTA_ES = 'TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO.'


def cta_dourado(im, caixa, y_topo, texto=CTA_ES, pt='TOQUE EM SAIBA MAIS', tam=26.0, nome='OpenSans_700Bold', folga=23):
    """Faixa dourada chapada com texto escuro (Open Sans Bold 26). Repinta a faixa, reduz a fonte
    no máximo 15 % e, se ainda faltar espaço, alarga a faixa simetricamente."""
    x0, y0, x1, y1 = caixa
    ouro = cor_fundo(im, (x0 + 4, y0 + 4, x0 + 20, y1 - 4))
    cor = cor_texto(im, caixa, lambda r, g, b: (r + g + b) < 200)
    preencher(im, caixa, ouro)
    f0 = F(nome, tam)
    fc = f0
    while fc.getlength(texto) > (x1 - x0) - 2 * folga and fc.size > tam * 0.85:
        fc = F(nome, fc.size - 0.25)
    alargar_caixa(im, caixa, ouro, fc.getlength(texto), folga)
    base = base_de(f0, pt, y_topo)
    base += (f0.getbbox('T', anchor='ls')[1] - fc.getbbox('T', anchor='ls')[1]) / 2
    linha(im, (x0 + x1) / 2, base, [(texto, fc, cor)], 'centro')
    return fc


def quebrar(texto, f, largura_max):
    """Quebra gulosa de linha pela largura em pixels."""
    linhas, atual = [], ''
    for p in texto.split(' '):
        t = (atual + ' ' + p).strip()
        if f.getlength(t) <= largura_max or not atual:
            atual = t
        else:
            linhas.append(atual); atual = p
    linhas.append(atual)
    return linhas


def legenda_depoimento(im, traducao, cx, y_topo, largura_max, f, cor, entrelinha=None):
    """Regra 4: print do depoimento fica em PT; legenda pequena em ES logo abaixo."""
    txt = 'Testimonio original en portugués: «%s»' % traducao
    ls = quebrar(txt, f, largura_max)
    passo = entrelinha or round(f.size * 1.3)
    base = y_topo - f.getbbox('T', anchor='ls')[1]
    for i, l in enumerate(ls):
        linha(im, cx, base + passo * i, [(l, f, cor)], 'centro')
    return len(ls), base + passo * (len(ls) - 1)


def _mapa_polar(cx, cy, r0, r1, a0, a1, rm, S):
    nr = int(round((r1 - r0) * S))
    na = int(round(np.radians(a1 - a0) * rm * S))
    rr = np.linspace(r1, r0, nr)[:, None]
    aa = np.radians(np.linspace(a0, a1, na))[None, :]
    mx = (cx + rr * np.sin(aa)).astype(np.float32)
    my = (cy - rr * np.cos(aa)).astype(np.float32)
    return mx, my, nr, na


def trocar_texto_arco(im, cx, cy, R, texto, nome_fonte='Montserrat_700Bold', S=3, a0=-100, a1=100, r0=55, debug=None):
    """Troca o texto curvo do topo do selo dourado (anel). Desenrola o anel em coordenadas polares,
    apaga as letras por inpainting clássico, escreve o novo texto reto e enrola de volta só na faixa do texto.
    Centro e raio do selo vêm de HoughCircles (medidos no script)."""
    a = np.array(im)
    r1 = R + 3
    rm = R * 0.86
    mx, my, nr, na = _mapa_polar(cx, cy, r0, r1, a0, a1, rm, S)
    u = cv2.remap(a, mx, my, cv2.INTER_CUBIC)
    ui = u.astype(int)
    lum = ui.sum(2)
    marrom = ((lum < 470) & (ui[..., 0] - ui[..., 2] > 50) & (ui[..., 0] < 210)).astype(np.uint8)
    # letras: componentes altos (os pontilhados laterais são baixos)
    n, lab, st, _ = cv2.connectedComponentsWithStats(marrom, 8)
    ok = lambda i: 0.10 * nr < st[i][3] < 0.35 * nr and st[i][2] < 3 * st[i][3] and st[i][1] < nr * 0.6
    hs = [st[i][3] for i in range(1, n) if ok(i)]
    hmax = sorted(hs)[int(len(hs) * 0.8)]
    letras = [i for i in range(1, n) if ok(i) and st[i][3] > 0.6 * hmax]
    cols0 = min(st[i][0] for i in letras); cols1 = max(st[i][0] + st[i][2] for i in letras)
    rows0 = min(st[i][1] for i in letras); rows1 = max(st[i][1] + st[i][3] for i in letras)
    alturas = sorted(st[i][3] for i in letras)
    cap = alturas[len(alturas) // 2]
    base_row = int(np.median([st[i][1] + st[i][3] for i in letras]))
    escuro = ui[(marrom > 0) & (lum < np.percentile(lum[marrom > 0], 30))]
    cor = tuple(int(v) for v in np.median(escuro, 0))
    m = np.zeros(marrom.shape, np.uint8)
    m[rows0 - 3:rows1 + 3, cols0 - 6:cols1 + 6] = marrom[rows0 - 3:rows1 + 3, cols0 - 6:cols1 + 6] * 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    ue = cv2.inpaint(cv2.cvtColor(u, cv2.COLOR_RGB2BGR), m, 5, cv2.INPAINT_TELEA)
    ue = cv2.cvtColor(ue, cv2.COLOR_BGR2RGB)
    # fonte calibrada pela altura de caixa-alta
    melhor = None
    for t in np.arange(6, 120, 0.25):
        f = ImageFont.truetype(fonte(nome_fonte), float(t))
        bb = f.getbbox('MPRDEV', anchor='ls')
        if melhor is None or abs(-bb[1] - cap) < abs(melhor[1] - cap):
            melhor = (t, -bb[1])
    f = ImageFont.truetype(fonte(nome_fonte), float(melhor[0]))
    larg_ant = cols1 - cols0
    while f.getlength(texto) > larg_ant * 1.15 and f.size > melhor[0] * 0.85:
        f = ImageFont.truetype(fonte(nome_fonte), f.size - 0.25)
    camada = Image.new('RGBA', (na, nr), (0, 0, 0, 0))
    ImageDraw.Draw(camada).text(((cols0 + cols1) / 2, base_row), texto, font=f, fill=cor + (255,), anchor='ms')
    camada = camada.filter(ImageFilter.GaussianBlur(0.5 * S / 2))
    base_img = Image.fromarray(ue).convert('RGBA')
    base_img.alpha_composite(camada)
    ue = np.array(base_img.convert('RGB'))
    nw = f.getlength(texto)
    c_ini = int(min(cols0, (cols0 + cols1) / 2 - nw / 2) - 8)
    c_fim = int(max(cols1, (cols0 + cols1) / 2 + nw / 2) + 8)
    c_ini, c_fim = max(c_ini, 0), min(c_fim, na - 1)
    if debug:
        Image.fromarray(np.vstack([u, ue])).save(debug)
    # enrola de volta só na faixa alterada
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    ang = np.degrees(np.arctan2(xx - cx, -(yy - cy)))
    row = (r1 - d) * S * (nr - 1) / ((r1 - r0) * S)
    col = (ang - a0) / (a1 - a0) * (na - 1)
    sel = (row >= rows0 - 4) & (row <= rows1 + 4) & (col >= c_ini) & (col <= c_fim)
    out = cv2.remap(ue, col.astype(np.float32), row.astype(np.float32), cv2.INTER_CUBIC)
    a2 = a.copy()
    a2[sel] = out[sel]
    return Image.fromarray(a2), dict(cor=cor, tam=f.size, cap=cap)


def apagar_textura(im, caixa, cond, dil=3, raio=6, seed=7):
    """apagar() + granulação: devolve à área apagada o ruído medido do fundo vizinho (fundos com textura fina),
    para não sobrar 'mancha lisa' do inpainting."""
    m = mascara_texto(im, caixa, cond, dil)
    out = np.array(apagar_mascara(im, m, raio)).astype(float)
    x0, y0, x1, y1 = caixa
    a = np.array(im).astype(float)[y0:y1, x0:x1]
    fundo = (m[y0:y1, x0:x1] == 0)
    hp = a - cv2.GaussianBlur(a, (0, 0), 2)
    sd = hp[fundo].std(0)
    rng = np.random.default_rng(seed)
    ruido = rng.normal(0, 1, out.shape[:2])[..., None] * sd[None, None, :]
    mk = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1)[..., None]
    out = out + ruido * mk
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
