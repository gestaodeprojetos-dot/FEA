#!/usr/bin/env python3
"""Ads 36 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Rodar a partir de fea_artes/:  python3 criativos/ads36.py
Originais em trabalho/Jads36-feed.png e trabalho/Jads36-story.png (Drive BR).
A página do ebook no tablet (transcrição em PT + QR Code) NÃO é tocada: fase 2.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads36a40 import *  # noqa

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLARO_HL = lambda r, g, b: (r + g + b) > 330      # título dourado/branco sobre verde escuro
CLARO_TX = lambda r, g, b: (r + g + b) > 330
ESC_CTA = lambda r, g, b: (r + g + b) < 300       # texto escuro no botão dourado
ESC_CTA_APAGAR = lambda r, g, b: (r + g + b) < 430
ESC_SELO = lambda r, g, b: (r + g + b) < 330

CHK_PT = ['Plano anatômico', 'correto', 'Regiões de risco', 'Bolus, microbolus', 'e retroinjeção',
          'Escolha do', 'preenchedor ideal']
# grupos de linhas por item (índices das linhas PT medidas) e as linhas ES de cada item
CHK_GRUPOS = [([0, 1], ['Plano anatómico', 'correcto']),
              ([2], ['Zonas de riesgo']),
              ([3, 4], ['Bolo, microbolo', 'y retroinyección']),
              ([5, 6], ['Elección del producto', 'de relleno ideal'])]
CTA_PT = 'QUERO DOMINAR O PROTOCOLO'
CTA_ES = 'QUIERO DOMINAR EL PROTOCOLO'


def gaps(im, caixa, cond, minimo=20):
    m = mascara(im, caixa, cond)
    xs = np.where(m.any(0))[0] + caixa[0]
    d = np.diff(xs)
    return [(int(xs[i]), int(xs[i + 1])) for i in np.where(d > minimo)[0]], int(xs.min()), int(xs.max())


def ads36(arq, P):
    im = abrir(os.path.join(AQ, 'trabalho', arq))
    W = im.width

    # ---------- título: 'Preenchimento' / 'tridimensional de olheiras.' ----------
    c1, c2 = P['hl1'], P['hl2']
    (l1,) = medir(im, c1, CLARO_HL)
    (l2,) = medir(im, c2, CLARO_HL)
    g, x0b, x1b = gaps(im, (c2[0], l2[0], c2[2], l2[1] + 1), CLARO_HL)
    x_fim_tri, x_ini_de = g[0]
    f = calibrar_larg(SERIF_BOLD, 'tridimensional', x_fim_tri - x0b + 1)
    cx = (x0b + x1b) / 2
    campo_ouro1 = campo_cor(im, (l1[2], l1[0], l1[3] + 1, l1[1] + 1), CLARO_HL)
    campo_ouro2 = campo_cor(im, (x0b, l2[0], x_fim_tri + 1, l2[1] + 1), CLARO_HL)
    campo_bco = campo_cor(im, (x_ini_de, l2[0], x1b + 1, l2[1] + 1), CLARO_HL)
    y1 = l1[0] - f.getbbox('Preenchimento')[1]
    y2 = l2[0] - f.getbbox('tridimensional de olheiras.')[1]
    im = apagar(im, (c1[0], l1[0] - 6, c1[2], l1[1] + 8), CLARO_HL, 4)
    im = apagar(im, (c2[0], l2[0] - 6, c2[2], l2[1] + 8), CLARO_HL, 4)
    t = 'Relleno'
    im = escrever_campo(im, t, f, cx - largura(f, t) / 2 - f.getbbox(t)[0], y1, campo_ouro1)
    t = 'tridimensional de ojeras.'
    xa = cx - largura(f, t) / 2 - f.getbbox(t)[0]
    assert xa + f.getbbox(t)[0] > 60 and xa + f.getbbox(t)[2] < W - 60
    im = escrever_campo(im, 'tridimensional', f, xa, y2, campo_ouro2)
    im = escrever_campo(im, 'de ojeras.', f, xa + f.getlength('tridimensional '), y2, campo_bco)

    # ---------- subtítulo ----------
    cs = P['sub']
    ls = medir(im, cs, CLARO_TX)
    assert len(ls) == 2, ls
    pt = ['A metodologia ARTI para aumentar previsibilidade,', 'naturalidade e segurança.']
    es = ['La metodología ARTI para aumentar la previsibilidad,', 'la naturalidad y la seguridad.']
    fs = calibrar_larg(SANS_REG, pt[0], ls[0][3] - ls[0][2] + 1)
    cor = cor_texto(im, cs, CLARO_TX)
    cxs = (ls[0][2] + ls[0][3]) / 2
    im = apagar(im, (cs[0], ls[0][0] - 6, cs[2], ls[1][1] + 6), CLARO_TX, 3)
    d = ImageDraw.Draw(im)
    for (top, bot, _, _), p, e in zip(ls, pt, es):
        y = top - fs.getbbox(p)[1]
        x = cxs - largura(fs, e) / 2 - fs.getbbox(e)[0]
        assert x > 60 and x + largura(fs, e) < W - 60
        d.text((x, y), e, font=fs, fill=cor)

    # ---------- checklist ----------
    cc = P['chk']
    lc = medir(im, cc, CLARO_TX)
    assert len(lc) == 7, lc
    fc = calibrar_larg(SANS_MED, CHK_PT[0], lc[0][3] - lc[0][2] + 1)
    corc = cor_texto(im, cc, CLARO_TX)
    xe = min(l[2] for l in lc)
    im = apagar(im, (cc[0], lc[0][0] - 8, cc[2], lc[-1][1] + 8), CLARO_TX, 3)
    d = ImageDraw.Draw(im)
    for idx, linhas_es in CHK_GRUPOS:
        for i, e in zip(idx, linhas_es):
            y = lc[i][0] - fc.getbbox(CHK_PT[i])[1]
            assert xe + largura(fc, e) < W - 50, e
            d.text((xe - fc.getbbox(e)[0], y), e, font=fc, fill=corc)

    # ---------- CTA dourado ----------
    ct = P['cta']
    cs_ = componentes(im, ct, ESC_CTA)
    letras = [c for c in cs_ if c[4] > 150]
    xs0 = min(c[0] for c in letras)
    seta_x0 = max(c[0] for c in letras)                     # o '>' é o componente mais à direita
    letras = [c for c in letras if c[0] < seta_x0]
    xs1 = max(c[2] for c in letras)
    topo = int(np.median([c[1] for c in letras]))
    alt = int(np.median([c[3] - c[1] for c in letras]))
    fct = calibrar_altura(SANS_XBOLD, 'H', alt)
    tr = track_medido(fct, CTA_PT, xs1 - xs0)
    cor_cta = cor_texto(im, (xs0, topo, xs1, topo + alt), ESC_CTA)
    im = apagar(im, (xs0 - 12, topo - 12, xs1 + 12, topo + alt + 22), ESC_CTA_APAGAR, 4)
    limite = seta_x0 - 40                                    # não encostar no círculo da seta
    cxc = (xs0 + xs1) / 2
    while True:
        wl = largura_track(fct, CTA_ES, tr)
        xi = cxc - wl / 2
        if xi + wl <= limite:
            break
        xi = max(xs0 - (xs0 - ct[0]) * 0.35, limite - wl)    # desloca à esquerda dentro da folga
        if xi + wl <= limite and xi >= ct[0] + 60:
            break
        fct = ImageFont.truetype(SANS_XBOLD, fct.size - 0.25)
        tr = tr * 0.995
    print(arq, 'CTA', round(fct.size, 2), 'x', round(xi), round(xi + wl), 'limite', limite)
    _, tp, _, _ = fct.getbbox('H')
    escrever_track(im, CTA_ES, fct, xi, topo + (alt - (fct.getbbox('H')[3] - tp)) / 2, cor_cta, tr)

    # ---------- selo: CÓPIAS -> COPIAS ----------
    im, _ = tirar_acento_selo(im, P['selo'], ESC_SELO)
    return im


FEED = dict(hl1=(250, 380, 1600, 530), hl2=(200, 528, 1950, 660), sub=(250, 660, 1950, 830),
            chk=(1320, 930, 2150, 1740), cta=(430, 2140, 1740, 2300), selo=(1690, 370, 1810, 405))
STORY = dict(hl1=(150, 520, 1600, 680), hl2=(150, 680, 1950, 810), sub=(150, 840, 2000, 1030),
             chk=(1380, 1080, 2150, 2020), cta=(430, 2680, 1740, 2840), selo=(1690, 508, 1810, 543))

if __name__ == '__main__':
    for arq, P, nome in [('Jads36-feed.png', FEED, 'FEA-Ads 36 Feed - PTO-LATAM.png'),
                         ('Jads36-story.png', STORY, 'FEA-Ads 36 Story - PTO-LATAM.png')]:
        print('ok', salvar(ads36(arq, P), nome))
