#!/usr/bin/env python3
"""[FEED] ADS 03.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Original em trabalho/Jads03-feed.jpg (Drive 1XutwAdMMUIb6r1BHGpiWb-JeCPUErZjk).
Capa do ebook (mockup em português) intacta: fase 2.
Preços de precos.json (de_297 riscado, preco). As pílulas de vidro sobre o terno são redesenhadas
com a largura do texto: o terno sob as pílulas antigas é reposto com a textura do próprio terno
logo acima (cópia de pixels), e a pílula nova é fosco (desfoque do fundo + branco 15 %) como no original.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_jpg_util import *  # noqa

BR, OU = (255, 255, 255), (240, 194, 108)
CLARO2 = lambda r, g, b: (r + g + b) > 240


def pilula_vidro(im, caixa, alpha=0.15, borda=0.32):
    x0, y0, x1, y1 = caixa
    a = np.array(im).astype(float)
    blur = cv2.GaussianBlur(a, (0, 0), 5)
    mi = np.array(mascara_pilula(im.size, (x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5))).astype(float)[..., None] / 255
    me = np.array(mascara_pilula(im.size, (x0, y0, x1, y1))).astype(float)[..., None] / 255
    fosco = blur * (1 - alpha) + 255 * alpha
    a = a * (1 - mi) + fosco * mi
    anel = np.clip(me - mi, 0, 1)
    a = a * (1 - anel * borda) + 255 * anel * borda
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def seta(im, x0, x1, y, cor=(255, 255, 255), esp=2):
    d = ImageDraw.Draw(im)
    d.line([(x0, y), (x1, y)], fill=cor, width=esp)
    d.line([(x1 - 8, y - 6), (x1, y)], fill=cor, width=esp)
    d.line([(x1 - 8, y + 6), (x1, y)], fill=cor, width=esp)


def recompor(orig, saida):
    im = abrir(orig)
    # ---------- título (Noto Serif, branco + dourado, sublinhado) ----------
    im = apagar_textura(im, (135, 175, 790, 512), CLARO2, 6)
    linhas = [[('La región más temida del', None, OU)],
              [('rostro', None, OU), (' puede convertirse en', None, BR)],
              [('la ', None, BR), ('más rentable', None, BR, 'sub'), (' cuando', None, BR)],
              [('usted sabe exactamente', None, BR)],
              [('dónde, cuánto y cómo aplicar.', None, BR)]]
    tam = 47.75
    fmax = lambda t: max(sum(F('NotoSerif_400Regular', t).getlength(s[0]) for s in l) for l in linhas)
    while fmax(tam) > 620:
        tam -= 0.25
    f = F('NotoSerif_400Regular', tam)
    f0 = F('NotoSerif_400Regular', 47.75)
    # mantém a linha de base de cada linha original (topos 188, 252, 317, 382, 447)
    b0 = base_de(f0, 'A região mais temida da', 188)
    for i, l in enumerate(linhas):
        segs = [(s[0], f, s[2]) + ((s[3],) if len(s) > 3 else ()) for s in l]
        linha(im, 146, b0 + 64.75 * i, segs)
    # ---------- caixa com borda dourada (Open Sans Bold branco) ----------
    im = apagar_textura(im, (150, 628, 462, 762), CLARO2, 5)
    ls = ['EBOOK CON PUNTOS DE', 'APLICACIÓN, VOLÚMENES', 'Y VARIACIONES SEGÚN', 'EL TIPO DE OJERA.']
    t = 24.5
    while max(F('OpenSans_700Bold', t).getlength(s) for s in ls) > 441 - 160:
        t -= 0.25
    fb = F('OpenSans_700Bold', t)
    b = base_de(F('OpenSans_700Bold', 24.5), 'EBOOK COM PONTOS', 638)
    for i, s in enumerate(ls):
        linha(im, 162, b + 33 * i, [(s, fb, BR)])
    # ---------- pílulas de preço sobre o terno ----------
    Y0, Y1 = 1139, 1201
    velhas = [(536, Y0, 706, Y1), (762, Y0, 1052, Y1)]
    a = np.array(im)
    m = np.zeros(a.shape[:2], bool)
    for c in velhas:
        m |= np.array(mascara_pilula(im.size, (c[0] - 3, c[1] - 3, c[2] + 3, c[3] + 3))) > 0
    m[Y0 - 4:Y1 + 5, 700:770] = True                       # seta antiga
    desl = (Y1 - Y0) + 14
    ys, xs = np.where(m)
    a[ys, xs] = a[ys - desl, xs]
    im = Image.fromarray(a)
    t = 1.0
    while True:
        fr, fb2, fv = F('OpenSans_400Regular', 29.2 * t), F('OpenSans_700Bold', 29.2 * t), F('OpenSans_700Bold', 32.25 * t)
        s1 = [('De ', fr, BR), (PRECOS['de_297'], fb2, (243, 23, 23), 'risco')]
        s2 = [('a solo ', fr, BR), (PRECOS['preco'], fv, (36, 255, 75))]
        w1 = largura(s1) + 39 * t
        w2 = largura(s2) + 47 * t
        total = w1 + 56 * t + w2
        if 536 + total <= 1062 or t < 0.4:
            break
        t -= 0.01
    p1 = (536, Y0, 536 + w1, Y1)
    p2 = (p1[2] + 56 * t, Y0, p1[2] + 56 * t + w2, Y1)
    im = pilula_vidro(im, p1)
    im = pilula_vidro(im, p2)
    base = 1181
    linha(im, p1[0] + 19 * t, base, s1, sub_esp=(243, 23, 23))
    seta(im, p1[2] + 12 * t, p2[0] - 7 * t, 1171)
    linha(im, p2[0] + 19 * t, base, s2)
    print(salvar(im, saida), 'escala do preço: %.2f' % t)
    return im


if __name__ == '__main__':
    recompor('trabalho/Jads03-feed.jpg', 'FEA-[FEED] ADS 03 - LATAM.jpg')
