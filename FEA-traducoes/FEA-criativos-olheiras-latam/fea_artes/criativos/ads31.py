#!/usr/bin/env python3
"""FEA · Ads 31 (Feed, png) · Ebook Olheiras LATAM.

Troca só a copy. Fontes do original: Noto Serif Medium (título, alinhado à esquerda),
Noto Sans Regular (subtítulo), Noto Sans Medium/Bold (checklist, 'NO' em negrito),
Noto Sans ExtraBold com tracking 0,05 em (CTA de 2 linhas).
Título ES em 3 linhas como o original: 'Usted no evita' / 'tratar ojeras por' / 'falta de cursos.'
(dourado a partir de 'por', como no original). CTA: 'COPIE EL PROTOCOLO' é mais largo que a
linha PT; as 2 linhas do CTA descem 6 a 7 % de corpo para caber sem mexer no botão (o tablet
encosta no lado direito do botão).
Ficam como estão: página do ebook no tablet (PT, fase 2), capa Allergan em inglês e QR Code.
Selo: só sai o acento de CÓPIAS.
O Story (7,7 MB) não baixou pelo conector do Drive: quando estiver em trabalho/loteI-ads31-story.png,
medir e acrescentar em M.
Rodar a partir de fea_artes/:  python3 criativos/ads31.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar
from fea_util_ads31a35 import *

SERIF = 'NotoSerif_500Medium'
SANS = 'NotoSans_400Regular'
CHK = 'NotoSans_500Medium'
CHK_B = 'NotoSans_700Bold'
CTA = 'NotoSans_800ExtraBold'
CTA_TR = 0.05
TXT = lambda r, g, b: (r > 130) & (g > 110)
OURO = lambda r, g, b: (r > 130) & (r - b > 60)
ESC = lambda r, g, b: (r + g + b) < 330

M = {
    'feed': dict(arq='trabalho/loteI-ads31-feed.png', saida='FEA-Ads 31 Feed - PTO-LATAM.png',
                 acento=(1053, 2080, 1068, 2089),
                 tit=[(395, 180, 'Você não evita'), (533, 187, 'olheiras por falta'), (672, 187, 'de curso.')],
                 tit_ouro=(747, 1304, 533), tit_larg=(187, 1304),
                 sub=[(861, 180, 'Você evita porque ainda'), (953, 187, 'não sabe:')], sub_larg=(180, 1077),
                 chk=[(1128, 'Qual plano usar'), (1272, 'Qual produto escolher'), (1406, 'Quando NÃO preencher')],
                 chk_x=333, chk_larg=(333, 1057),
                 cta=[(1620, 320, 'COPIE O PROTOCOLO'), (1678, 318, 'TRIDIMENSIONAL')], cta_larg=(320, 869),
                 cta_lim=875),
}


def pen(nome, tam, texto, x_tinta):
    """Origem da caneta que põe a tinta do 1o caractere em x_tinta."""
    return x_tinta - F(nome, tam).getbbox(texto[0], anchor='ls')[0]


def tinta_esq(nome, tam, texto, x_pen):
    return x_pen + F(nome, tam).getbbox(texto[0], anchor='ls')[0]


def gerar(fmt):
    p = M[fmt]
    orig = abrir(p['arq'])
    im = orig.copy()
    W, H = im.size
    im = apagar_col(im, p['acento'], lambda r, g, b: (r + g + b) < 530, 1)

    # ---- título (alinhado à esquerda)
    tit = p['tit']
    creme = cor_run(im, (180, 395, 1115, 498), TXT)
    g0, g1, gt = p['tit_ouro']
    ouro = cor_run(im, (g0, gt, g1, gt + 105), OURO)
    tt = calibrar_runs([('olheiras por falta', SERIF, creme)], p['tit_larg'][1] - p['tit_larg'][0] + 1)
    bases = [base_de([(t, SERIF, creme)], tt, top) for top, _, t in tit]
    pens = [pen(SERIF, tt, t, x) for _, x, t in tit]
    # caixas por linha: a faixa dourada diagonal começa em x ~1316 (linha 1) e ~1358 (linha 2)
    for (top, _, _), x1 in zip(tit, (1250, 1336, 1250)):
        im = apagar_misto(im, (150, top - 20, x1, top + 125), TXT, 4)
    es = [[('Usted no evita', SERIF, creme)],
          [('tratar ojeras ', SERIF, creme), ('por', SERIF, ouro)],
          [('falta de cursos.', SERIF, ouro)]]
    for runs, b, pn in zip(es, bases, pens):
        bb = desenhar(im, runs, tt, b, x_esq=tinta_esq(SERIF, tt, runs[0][0], pn))
        assert bb[2] < 1320, bb

    # ---- subtítulo
    sub = p['sub']
    cinza = cor_run(im, (180, 861, 1077, 925), TXT)
    ts = calibrar_runs([(sub[0][2], SANS, cinza)], p['sub_larg'][1] - p['sub_larg'][0] + 1)
    bs = [base_de([(t, SANS, cinza)], ts, top) for top, _, t in sub]
    ps = [pen(SANS, ts, t, x) for _, x, t in sub]
    im = apagar_misto(im, (150, sub[0][0] - 15, 1132, sub[1][0] + 80), TXT, 4)
    for t, b, pn in zip(['Lo evita porque aún', 'no sabe:'], bs, ps):
        desenhar(im, [(t, SANS, cinza)], ts, b, x_esq=tinta_esq(SANS, ts, t, pn))

    # ---- checklist (ícones intactos; texto alinhado em x = chk_x)
    chk = p['chk']
    cc = cor_run(im, (333, 1272, 1057, 1340), TXT)
    tc = calibrar_runs([(chk[1][1], CHK, cc)], p['chk_larg'][1] - p['chk_larg'][0] + 1)
    pt_runs = [[(chk[0][1], CHK, cc)], [(chk[1][1], CHK, cc)],
               [('Quando ', CHK, cc), ('NÃO', CHK_B, cc), (' preencher', CHK, cc)]]
    es_runs = [[('Qué plano usar', CHK, cc)], [('Qué producto elegir', CHK, cc)],
               [('Cuándo ', CHK, cc), ('NO', CHK_B, cc), (' rellenar', CHK, cc)]]
    for (top, _), pr, er in zip(chk, pt_runs, es_runs):
        b = base_de(pr, tc, top)
        pn = pen(CHK, tc, pr[0][0], p['chk_x'])
        im = apagar_misto(im, (310, top - 18, 1132, top + 82), TXT, 4)
        desenhar(im, er, tc, b, x_esq=tinta_esq(CHK, tc, er[0][0], pn))

    # ---- CTA (2 linhas, botão dourado intacto)
    cta = p['cta']
    cor_c = cor_run(im, (320, 1620, 869, 1656), ESC, claro=False)
    tk = calibrar_runs([(cta[0][2], CTA, cor_c)], p['cta_larg'][1] - p['cta_larg'][0] + 1, CTA_TR)
    bk = [base_de([(t, CTA, cor_c)], tk, top, CTA_TR * tk) for top, _, t in cta]
    pk = [pen(CTA, tk, t, x) for _, x, t in cta]
    es_c = ['COPIE EL PROTOCOLO', 'TRIDIMENSIONAL']
    tk_es = tk
    lim = p['cta_lim'] - p['cta_larg'][0]
    while (lambda b: b[2] - b[0])(desenhar(im, [(es_c[0], CTA, cor_c)], tk_es, 0, x_esq=0,
                                           tracking=CTA_TR * tk_es, so_medir=True)) > lim:
        tk_es -= 0.25
    assert tk_es >= tk * 0.85
    k = tk_es / tk
    meio = (bk[0] + bk[1]) / 2 - tk * 0.36            # centro vertical do bloco de 2 linhas
    im = apagar_col(im, (300, cta[0][0] - 14, 900, cta[1][0] + 52), ESC, 3)
    for t, b, pn in zip(es_c, bk, pk):
        bn = meio + (b - tk * 0.36 - meio) * k + tk_es * 0.36
        desenhar(im, [(t, CTA, cor_c)], tk_es, bn, x_esq=tinta_esq(CTA, tk_es, t, pn), tracking=CTA_TR * tk_es)
    print(fmt, 'título', tt, 'CTA', tk, '->', tk_es, 'redução %.1f%%' % ((1 - k) * 100))
    return im, p['saida']


if __name__ == '__main__':
    for fmt in M:
        im, nome = gerar(fmt)
        print(salvar(im, nome))
