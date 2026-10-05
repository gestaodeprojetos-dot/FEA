#!/usr/bin/env python3
"""FEA · Ads 34 (Feed, png) · Ebook Olheiras LATAM.

Troca só a copy. Fontes do original: Noto Sans SemiBold tracking 0,2 em (selo 'ACESSO VITALÍCIO'),
Noto Serif Medium (título), Noto Serif Regular/Italic (subtítulo), Noto Sans Regular (corpo),
Noto Sans ExtraBold tracking 0,04 em (CTA). Preço do CTA lido de precos.json (PRECOS['preco']).
Selo +30 MIL: só sai o acento de CÓPIAS. Pílula de contorno e botão dourado alargados no miolo
(reamostragem horizontal, pontas intactas) quando o ES é mais longo.
Fase 2: mockups (tablet com capa '04. I - Intercorrências' e páginas PT) e a palavra-fantasma
'OLHEIRAS' gigante e quase transparente no fundo, atrás dos tablets (camada decorativa do arquivo
de design, trocar por 'OJERAS' na fonte do projeto).
O Story (7,0 MB) não baixou pelo conector do Drive: quando estiver em trabalho/loteI-ads34-story.png,
medir e acrescentar em M.
Rodar a partir de fea_artes/:  python3 criativos/ads34.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar, PRECOS
from fea_util_ads31a35 import *

SELO = 'NotoSans_600SemiBold'
SELO_TR = 0.2
SERIF_T = 'NotoSerif_500Medium'
SERIF = 'NotoSerif_400Regular'
SERIF_IT = 'NotoSerif_400Regular_Italic'
SANS = 'NotoSans_400Regular'
CTA = 'NotoSans_800ExtraBold'
CTA_TR = 0.04
TXT = lambda r, g, b: (r > 140) & (g > 110)
OURO = lambda r, g, b: (r > 120) & (r - b > 40)
ESC = lambda r, g, b: (r + g + b) < 330

M = {
    'feed': dict(arq='trabalho/loteI-ads34-feed.png', saida='FEA-Ads 34 Feed - PTO-LATAM.png',
                 acento=(1461, 1555, 1472, 1562),
                 pilula=(560, 160, 1600, 425), ponto=(763, 780), selo_txt=(809, 1393, 302),
                 t1=(432, 454, 1285, 1331, 1705), t2=(618, 401, 1753),
                 s1=(785, 468, 1002, 1074, 1693), s2=(905, 572, 848, 1586),
                 corpo=[(1036, 514, 1644), (1110, 555, 1605)],
                 btn=(300, 2095, 1860, 2420), btn_txt=(503, 1559, 2195), btn_seta=1595),
}


def gerar(fmt):
    p = M[fmt]
    orig = abrir(p['arq'])
    im = orig.copy()
    W, H = im.size
    im = apagar_col(im, p['acento'], lambda r, g, b: (r + g + b) < 530, 1)

    # ---- pílula de contorno '• ACESSO VITALÍCIO'
    qx0, qy0, qx1, qy1 = p['pilula']
    sx0, sx1, stop = p['selo_txt']
    d0, d1 = p['ponto']
    cor_s = perfil_cor(im, (sx0, stop, sx1, stop + 36), OURO)
    pt_s = [('ACESSO VITALÍCIO', SELO, cor_s)]
    ts = calibrar_runs(pt_s, sx1 - sx0 + 1, SELO_TR)
    base_s = base_de(pt_s, ts, stop - 11, SELO_TR * ts)     # topo medido inclui o acento do Í
    es_s = [('ACCESO DE POR VIDA', SELO, cor_s)]
    lw = (lambda b: b[2] - b[0])(desenhar(im, es_s, ts, 0, x_esq=0, tracking=SELO_TR * ts, so_medir=True))
    extra_s = extra = max(0, int(np.ceil(lw - (sx1 - sx0))))
    im = apagar_col(im, (d0 - 12, stop - 22, sx1 + 14, stop + 50), OURO, 3)
    if extra:
        im = esticar_horizontal(im, (qx0, qy0, qx1, qy1), qx0 - extra // 2, qx1 + (extra - extra // 2), d0 - 25, sx1 + 20)
    dx = -(extra // 2)
    im = mover_icone(orig, im, (d0 - 8, stop - 4, d1 + 8, stop + 40), dx, OURO, 2, 2)
    desenhar(im, es_s, ts, base_s, x_esq=sx0 + dx, tracking=SELO_TR * ts)

    # ---- título
    t1, a0, a1, g0, g1 = p['t1']
    t2, b0, b1 = p['t2']
    creme = cor_run(im, (b0, t2, b1, t2 + 150), TXT)
    ouro = yperfil_cor(im, (g0, t1, g1, t1 + 115), TXT, 12)  # degradê vertical dourado -> creme
    pt1 = [('O problema ', SERIF_T, creme), ('não é', SERIF_T, ouro)]
    tt = calibrar_runs([('preencher olheiras', SERIF_T, creme)], b1 - b0 + 1)
    bt1 = base_de(pt1, tt, t1)
    bt2 = base_de([('preencher olheiras', SERIF_T, creme)], tt, t2)

    # ---- subtítulo (2 linhas, Noto Serif com itálico dourado)
    s1, o0, e0, u0, u1 = p['s1']
    s2, r0, r1, n1 = p['s2']
    c_cre = cor_run(im, (o0, s1, e0 - 20, s1 + 70), TXT)
    c_our = cor_run(im, (u0, s1, u1, s1 + 70), TXT)
    pts1 = [('O problema ', SERIF, c_cre), ('é ', SERIF, c_our), ('usar o produto', SERIF_IT, c_our)]
    pts2 = [('errado', SERIF_IT, c_our), (' no plano errado.', SERIF, c_cre)]
    tsub = calibrar_runs(pts1, u1 - o0 + 1)
    bs1 = base_de(pts1, tsub, s1)
    bs2 = base_de(pts2, tsub, s2)

    # ---- corpo
    corpo = p['corpo']
    c_corpo = cor_run(im, (corpo[0][1], corpo[0][0], corpo[0][2], corpo[0][0] + 50), TXT)
    ptc = ['Copie o protocolo tridimensional que aumenta a', 'previsibilidade e a naturalidade dessa região.']
    tcp = calibrar_runs([(ptc[0], SANS, c_corpo)], corpo[0][2] - corpo[0][1] + 1)
    bcs = [base_de([(ptc[i], SANS, c_corpo)], tcp, corpo[i][0]) for i in range(2)]

    # apaga título, subtítulo e corpo de uma vez (fundo verde liso + palavra-fantasma)
    im = apagar_misto(im, (300, t1 - 25, W - 300, corpo[1][0] + 72), TXT, 4)

    cx = W / 2   # bloco centrado na arte (original centrado em ~1079)
    for runs, b, t in [([('El problema ', SERIF_T, creme), ('no es', SERIF_T, ouro)], bt1, tt),
                       ([('rellenar ojeras', SERIF_T, creme)], bt2, tt),
                       ([('El problema ', SERIF, c_cre), ('es ', SERIF, c_our), ('usar el producto', SERIF_IT, c_our)], bs1, tsub),
                       ([('equivocado', SERIF_IT, c_our), (' en el plano equivocado.', SERIF, c_cre)], bs2, tsub),
                       ([('Copie el protocolo tridimensional que aumenta la', SANS, c_corpo)], bcs[0], tcp),
                       ([('previsibilidad y la naturalidad de esta región.', SANS, c_corpo)], bcs[1], tcp)]:
        bb = desenhar(im, runs, t, b, cx=cx)
        assert bb[0] > 150 and bb[2] < W - 150, bb

    # ---- CTA dourado com preço
    bx0, by0, bx1, by1 = p['btn']
    tx0, tx1, ttop = p['btn_txt']
    cor_cta = cor_run(im, (tx0, ttop + 12, tx1, ttop + 52), ESC, claro=False)
    pt_c = [('RECEBER ACESSO VITALÍCIO POR R$97', CTA, cor_cta)]
    tc = calibrar_runs(pt_c, tx1 - tx0 + 1, CTA_TR)
    base = base_de(pt_c, tc, ttop, CTA_TR * tc)
    es_c = [('OBTENER ACCESO DE POR VIDA POR ' + PRECOS['preco'], CTA, cor_cta)]
    # cabe no máximo com 1780 px de botão; se passar, reduz a fonte (até 15 %)
    lw = (lambda b: b[2] - b[0])(desenhar(im, es_c, tc, 0, x_esq=0, tracking=CTA_TR * tc, so_medir=True))
    margem = (tx0 - bx0) + (bx1 - tx1)
    tc_es = tc
    while lw + margem > W - 260 and tc_es > tc * 0.85:
        tc_es -= 0.25
        lw = (lambda b: b[2] - b[0])(desenhar(im, es_c, tc_es, 0, x_esq=0, tracking=CTA_TR * tc_es, so_medir=True))
    im = apagar_col(im, (tx0 - 15, ttop - 15, tx1 + 15, ttop + 70), ESC, 3)
    extra = int(np.ceil(lw - (tx1 - tx0)))
    if extra > 0:
        im = esticar_horizontal(im, (bx0, by0, bx1, by1), bx0 - extra // 2, bx1 + (extra - extra // 2),
                                tx0 - 20, p['btn_seta'] - 15, suave=45)
        tx0n = tx0 - extra // 2
    else:
        tx0n = tx0 + (tx1 - tx0 - lw) / 2
    base_es = base - (tc - tc_es) * 0.36   # fonte menor: recentra na altura do botão
    desenhar(im, es_c, tc_es, base_es, x_esq=tx0n, tracking=CTA_TR * tc_es)
    print(fmt, 'selo alargado', extra_s, 'CTA', tc, '->', tc_es, 'alargado', extra)
    return im, p['saida']


if __name__ == '__main__':
    for fmt in M:
        im, nome = gerar(fmt)
        print(salvar(im, nome))
