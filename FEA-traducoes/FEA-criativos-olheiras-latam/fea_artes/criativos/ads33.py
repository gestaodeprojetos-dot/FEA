#!/usr/bin/env python3
"""FEA · Ads 33 (Feed, png) · Ebook Olheiras LATAM.

Troca só a copy. Fontes do original: Noto Serif Medium (título, 2a linha em degradê dourado),
Open Sans Regular (subtítulo), Open Sans Medium (checklist), Noto Sans ExtraBold com tracking (CTA).
O título ES é mais longo: a quebra fica 'Usted estudió… pero,' / 'a la hora de aplicar, ¿se bloquea?'
(o dourado começa no 'pero', como o 'mas' do original). Selo: só sai o acento de CÓPIAS.
Mockups do ebook (página e capa PT nos tablets) ficam para a fase 2.
O Story (Ads 33 Story - PTO.png, 6,5 MB) não baixou pelo conector do Drive (limite de tamanho):
quando o original estiver em trabalho/loteI-ads33-story.png, medir e acrescentar em M.
Rodar a partir de fea_artes/:  python3 criativos/ads33.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar
from fea_util_ads31a35 import *

SERIF = 'NotoSerif_500Medium'
SANS = 'OpenSans_400Regular'
BUL = 'OpenSans_500Medium'
CTA = 'NotoSans_800ExtraBold'
CTA_TR = 0.04
TXT = lambda r, g, b: (r > 150) & (g > 120)
ICONE = lambda r, g, b: (r > g + 5) & (r > 60)
ESC = lambda r, g, b: (r + g + b) < 330

M = {
    'feed': dict(arq='trabalho/loteI-ads33-feed.png', saida='FEA-Ads 33 Feed - PTO-LATAM.png',
                 acento=(1814, 1099, 1824, 1104),
                 tit=[(1380, 662, 1528), (1530, 237, 1919)], larg_max=1880,
                 sub=(1705, 424, 1730),
                 # linhas do checklist: (topo, [(ícone x0, x1)], [(texto x0, x1, pt, es)])
                 chk=[(1836, [(417, 502), (1133, 1218)],
                       [(545, 1098, 'Edema e efeito Tyndall', 'Edema y efecto Tyndall'),
                        (1261, 1656, 'Regiões de risco', 'Zonas de riesgo')]),
                      (1966, [(417, 502), (960, 1044)],
                       [(542, 923, 'Irregularidades', 'Irregularidades'),
                        (1088, 1737, 'Bolsas pós preenchimento', 'Bolsas tras el relleno')])],
                 btn=(560, 2105, 1600, 2290), btn_txt=(689, 1382, 2177), btn_seta=1405),
}


def checklist(im, orig, linha, W):
    top, icones, textos = linha
    y0, y1 = top - 32, top + 70
    cor = cor_run(orig, (textos[0][0], top, textos[0][1], top + 55), TXT)
    # tamanho calibrado no item mais largo
    x0, x1, pt, _ = max(textos, key=lambda t: t[1] - t[0])
    tb = calibrar_runs([(pt, BUL, cor)], x1 - x0 + 1)
    base = base_de([(textos[0][2], BUL, cor)], tb, top)
    # geometria nova: ícone -> texto com os mesmos respiros do original, linha recentrada
    gap_it = textos[0][0] - icones[0][1]                       # ícone -> texto
    gap_ti = icones[1][0] - textos[0][1]                       # texto -> próximo ícone
    larg = [(lambda b: b[2] - b[0])(desenhar(im, [(es, BUL, cor)], tb, 0, x_esq=0, so_medir=True)) for *_, es in textos]
    w_ic = [i1 - i0 for i0, i1 in icones]
    total = w_ic[0] + gap_it + larg[0] + gap_ti + w_ic[1] + gap_it + larg[1]
    cx = (icones[0][0] + textos[1][1]) / 2
    nx = cx - total / 2
    pos_ic = [nx, nx + w_ic[0] + gap_it + larg[0] + gap_ti]
    pos_tx = [pos_ic[0] + w_ic[0] + gap_it, pos_ic[1] + w_ic[1] + gap_it]
    im = apagar_col(im, (icones[0][0] - 25, y0, max(t[1] for t in textos) + 25, y1),
                    lambda r, g, b: TXT(r, g, b) | ICONE(r, g, b), 3)
    for (i0, i1), nx0 in zip(icones, pos_ic):
        im = mover_icone(orig, im, (i0 - 8, y0 + 4, i1 + 8, y1 - 4), int(round(nx0 - i0)), ICONE)
    for (x0, x1, pt, es), px in zip(textos, pos_tx):
        bb = desenhar(im, [(es, BUL, cor)], tb, base, x_esq=px)
        assert bb[2] < W - 80
    return im


def gerar(fmt):
    p = M[fmt]
    orig = abrir(p['arq'])
    im = orig.copy()
    W, H = im.size
    im = apagar_col(im, p['acento'], lambda r, g, b: (r + g + b) < 530, 1)

    # ---- título
    (t1, a0, a1), (t2, c0, c1) = p['tit']
    creme = cor_run(im, (a0, t1 + 10, a1, t1 + 95), TXT)
    ouro = perfil_cor(im, (c0, t2, c1, t2 + 115), TXT)
    tam = calibrar_runs([('mas na hora de aplicar, trava?', SERIF, creme)], c1 - c0 + 1)
    b1 = base_de([('Você estudou...', SERIF, creme)], tam, t1)
    b2 = base_de([('mas na hora de aplicar, trava?', SERIF, creme)], tam, t2)
    l1 = [('Usted estudió… ', SERIF, creme), ('pero,', SERIF, ('perfil', [(0, ouro[1][1][1]), (1, ouro[1][3][1])]))]
    l2 = [('a la hora de aplicar, ¿se bloquea?', SERIF, ouro)]
    tam_es = min(caber(l, tam, p['larg_max'])[0] for l in (l1, l2))
    im = apagar_misto(im, (120, t1 - 15, W - 120, t2 + 125), TXT, 4)
    cx = (c0 + c1) / 2
    meio = (b1 + b2) / 2
    k = tam_es / tam
    for l, b in ((l1, b1), (l2, b2)):
        bb = desenhar(im, l, tam_es, meio + (b - meio) * k, cx=cx)
        assert bb[0] > 100 and bb[2] < W - 100, bb

    # ---- subtítulo
    top, x0, x1 = p['sub']
    cor = cor_run(im, (x0, top, x1, top + 60), TXT)
    pt = 'Aqui você aprende o que realmente importa:'
    ts = calibrar_runs([(pt, SANS, cor)], x1 - x0 + 1)
    base = base_de([(pt, SANS, cor)], ts, top)
    im = apagar_misto(im, (x0 - 30, top - 15, x1 + 30, top + 80), TXT, 4)
    desenhar(im, [('Aquí aprende lo que realmente importa:', SANS, cor)], ts, base, cx=(x0 + x1) / 2)

    # ---- checklist
    for linha in p['chk']:
        im = checklist(im, orig, linha, W)

    # ---- CTA dourado (alarga o miolo se precisar)
    bx0, by0, bx1, by1 = p['btn']
    tx0, tx1, ttop = p['btn_txt']
    cor_cta = cor_run(im, (tx0, ttop, tx1, ttop + 45), ESC, claro=False)
    pt_c = [('QUERO DOMINAR OLHEIRAS', CTA, cor_cta)]
    tc = calibrar_runs(pt_c, tx1 - tx0 + 1, CTA_TR)
    base = base_de(pt_c, tc, ttop, CTA_TR * tc)
    im = apagar_col(im, (tx0 - 15, ttop - 22, tx1 + 15, ttop + 70), ESC, 3)
    es_c = [('QUIERO DOMINAR LAS OJERAS', CTA, cor_cta)]
    lw = (lambda b: b[2] - b[0])(desenhar(im, es_c, tc, 0, x_esq=0, tracking=CTA_TR * tc, so_medir=True))
    extra = int(np.ceil(lw - (tx1 - tx0)))
    if extra > 0:
        im = esticar_horizontal(im, (bx0, by0, bx1, by1), bx0 - extra // 2, bx1 + (extra - extra // 2),
                                tx0 - 20, p['btn_seta'] - 15)
        tx0n = tx0 - extra // 2
    else:
        tx0n = tx0 + (tx1 - tx0 - lw) / 2
    desenhar(im, es_c, tc, base, x_esq=tx0n, tracking=CTA_TR * tc)
    print(fmt, 'título', tam, '->', tam_es, 'redução %.1f%%' % ((1 - k) * 100), 'CTA alargado', extra)
    return im, p['saida']


if __name__ == '__main__':
    for fmt in M:
        im, nome = gerar(fmt)
        print(salvar(im, nome))
