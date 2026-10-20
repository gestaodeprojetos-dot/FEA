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
    # repõe o terno sob as pílulas antigas copiando um trecho do próprio terno; o deslocamento é escolhido
    # pelo menor desajuste na borda (anel de 6 px em volta da área), para a costura não aparecer
    im = apagar(im, (712, 1156, 762, 1186), lambda r, g, b: (r + g + b) > 330, 2, 4)   # seta antiga (traço fino)
    a = np.array(im)
    ai = a.astype(int)
    blocos = [np.array(mascara_pilula(im.size, (c[0] - 3, c[1] - 3, c[2] + 3, c[3] + 3))) > 0 for c in velhas]
    for m in blocos:
        anel = (cv2.dilate(m.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0) & ~m
        ys, xs = np.where(anel)
        ys_m, xs_m = np.where(m)
        lisa = cv2.GaussianBlur(a, (0, 0), 6).astype(float)
        anel_med = lisa[ys, xs].mean(0)
        melhor = None
        for dy in list(range(-150, -63, 6)) + list(range(66, 120, 6)):
            for dx in range(-90, 91, 15):
                yy, xx = ys + dy, xs + dx
                if yy.min() < 0 or yy.max() >= a.shape[0] or xx.min() < 0 or xx.max() >= a.shape[1]:
                    continue
                src = ai[yy, xx]
                if (src.sum(1) > 330).mean() > 0.02:      # evita fonte com pílula, texto ou fundo verde claro
                    continue
                yi, xi = ys_m + dy, xs_m + dx
                if yi.min() < 0 or yi.max() >= a.shape[0] or xi.min() < 0 or xi.max() >= a.shape[1]:
                    continue
                miolo = lisa[yi, xi]
                # desajuste na borda + diferença de tom do miolo + manchas grandes no miolo
                err = np.abs(src - ai[ys, xs]).mean() + 2 * np.abs(miolo.mean(0) - anel_med).sum() + miolo.std(0).sum()
                if melhor is None or err < melhor[0]:
                    melhor = (err, dy, dx)
        _, dy, dx = melhor
        # cópia do terno deslocado + correção de tom: a diferença de cor medida na borda é interpolada
        # para dentro (inpainting clássico do campo de diferença, suave); nenhum pixel inventado
        src = np.roll(np.roll(a, -dy, 0), -dx, 1).astype(float)
        dif = np.clip(cv2.GaussianBlur(a.astype(float) - src, (0, 0), 2) + 128, 0, 255).astype(np.uint8)
        mk = cv2.dilate((m * 255).astype(np.uint8), np.ones((3, 3), np.uint8))
        dif = cv2.inpaint(dif, mk, 9, cv2.INPAINT_TELEA).astype(float) - 128
        dif = cv2.GaussianBlur(dif, (0, 0), 4)
        a2 = np.clip(src + dif, 0, 255).astype(np.uint8)
        a[m] = a2[m]
        ai = a.astype(int)
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
