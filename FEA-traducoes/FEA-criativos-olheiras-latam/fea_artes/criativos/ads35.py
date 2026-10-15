#!/usr/bin/env python3
"""FEA · Ads 35 (Feed e Story, png) · Ebook Olheiras LATAM.

Troca só a copy. Fontes do original: Noto Serif Medium (título), Noto Serif SemiBold (rótulos
dos cards), Open Sans Medium (bullets), Open Sans Regular/Italic (linha do protocolo), Noto Sans ExtraBold com
tracking (CTA). Texto apagado por interpolação de fundo (sem IA generativa).

O título ES ("3 errores que hacen que su relleno de ojeras se vea artificial") não cabe em
2 linhas nem reduzindo 15 %: vai em 3 linhas no tamanho original e a faixa de baixo
(bullets, protocolo, CTA) desce uma entrelinha sobre o degradê liso do fundo.
Rodar a partir de fea_artes/:  python3 criativos/ads35.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar, mascara
from fea_util_ads31a35 import *

SERIF = 'NotoSerif_500Medium'
SERIF_CARD = 'NotoSerif_600SemiBold'
SANS = 'OpenSans_400Regular'
SANS_IT = 'OpenSans_400Regular_Italic'
BUL = 'OpenSans_500Medium'
CTA = 'NotoSans_800ExtraBold'
CTA_TR = 0.03
TXT = lambda r, g, b: (r > 120) & (g > 100)
ESC = lambda r, g, b: (r + g + b) < 330

# medidas do original (px, arte 2160 de largura)
M = {
    'feed': dict(arq='trabalho/loteI-ads35-feed.png', saida='FEA-Ads 35 Feed - PTO-LATAM.png', dy_card=0,
                 tit=[(1411, 501, 946, 1660), (1571, 252, 1911)], faixa=1700,
                 bul_top=1781, bul1=(347, 862), bul3=(1503, 1912),
                 prot=(1899, 444, 1344, 1701),
                 btn=(520, 2060, 1640, 2290), btn_txt=(642, 1418, 2144), btn_seta=1455),
    'story': dict(arq='trabalho/loteI-ads35-story.png', saida='FEA-Ads 35 Story - PTO-LATAM.png', dy_card=440,
                  tit=[(1854, 448, 933, 1713), (2029, 176, 1987)], faixa=2200,
                  bul_top=2259, bul1=(279, 842), bul3=(1542, 1988),
                  prot=(2387, 386, 1369, 1758),
                  btn=(470, 2560, 1690, 2810), btn_txt=(601, 1449, 2654), btn_seta=1490),
}


def cards(im, dy):
    # card 1: 'Produto muito' -> 'Producto muy' (2a linha 'hidrofílico' igual em ES)
    # card 2: 'Plano superficial' igual em ES
    # card 3: 'Excesso de' / 'projeção' -> 'Exceso de' / 'proyección'
    # cor por linha tirada do card do meio (intacto): 1a linha creme, 2a linha dourada
    cor_l = {1009: cor_run(im, (990, 1009 + dy, 1170, 1056 + dy), TXT),
             1079: cor_run(im, (920, 1079 + dy, 1240, 1140 + dy), TXT)}
    out = []
    for pt, es, top, x0, x1 in [('Produto muito', 'Producto muy', 1009, 260, 672),
                                ('Excesso de', 'Exceso de', 1009, 1539, 1842),
                                ('projeção', 'proyección', 1079, 1567, 1812)]:
        cor = cor_l[top]
        top += dy
        caixa = (x0 - 20, top - 6, x1 + 20, top + 66)
        tam = calibrar_runs([(pt, SERIF_CARD, cor)], x1 - x0 + 1)
        base = base_de([(pt, SERIF_CARD, cor)], tam, top)
        out.append((caixa, es, cor, tam, base, (x0 + x1) / 2))
    for caixa, *_ in out:
        im = apagar_col(im, caixa, TXT, 3)
    for caixa, es, cor, tam, base, cx in out:
        desenhar(im, [(es, SERIF_CARD, cor)], tam, base, cx=cx)
    return im


def gerar(fmt):
    p = M[fmt]
    im = abrir(p['arq'])
    W, H = im.size
    im = cards(im, p['dy_card'])

    # ---- título: medir, apagar, abrir espaço, escrever em 3 linhas
    (t1, gx0, gx1, x1a), (t2, x0b, x1b) = p['tit']
    ouro = cor_run(im, (gx0 - 5, t1, gx1 + 5, t1 + 110), TXT)
    creme = cor_run(im, (x0b, t2, x1b, t2 + 105), TXT)
    tam = calibrar_runs([('sua olheira ficar artificial', SERIF, creme)], x1b - x0b + 1)
    b1 = base_de([('3 erros que fazem', SERIF, creme)], tam, t1)
    b2 = base_de([('sua olheira ficar artificial', SERIF, creme)], tam, t2)
    passo = b2 - b1
    cx = (x0b + x1b) / 2
    im = apagar_col(im, (120, t1 - 25, W - 120, p['faixa'] - 5), TXT, 4)
    # desce a faixa inferior uma entrelinha (fundo liso: repete a linha de cima no vão)
    a = np.array(im)
    d = int(round(passo))
    f0 = p['faixa']
    a[f0 + d:] = a[f0:H - d].copy()
    a[f0:f0 + d] = a[f0 - 1]
    im = Image.fromarray(a)
    linhas = [[('3 errores', SERIF, ouro), (' que hacen que', SERIF, creme)],
              [('su relleno de ojeras', SERIF, creme)],
              [('se vea artificial', SERIF, creme)]]
    for i, runs in enumerate(linhas):
        bb = desenhar(im, runs, tam, b1 + i * passo, cx=cx)
        assert bb[0] > 100 and bb[2] < W - 100, bb

    # ---- bullets (só 1 e 3 mudam; 'Plano superficial' é igual em ES)
    bt = p['bul_top'] + d
    for (x0, x1), pt, es in [(p['bul1'], 'Produto muito hidrofílico', 'Producto muy hidrofílico'),
                             (p['bul3'], 'Excesso de projeção', 'Exceso de proyección')]:
        caixa = (x0 - 8, bt - 8, x1 + 10, bt + 60)
        cor = cor_run(im, caixa, TXT)
        tb = calibrar_runs([(pt, BUL, cor)], x1 - x0 + 1)
        base = base_de([(pt, BUL, cor)], tb, bt)
        im = apagar_col(im, caixa, TXT, 3)
        bb = desenhar(im, [(es, BUL, cor)], tb, base, x_esq=x0)
        assert bb[2] < W - 60, bb

    # ---- 'O protocolo tridimensional resolve os 3'
    pt_top, px0, pit0, px1 = p['prot']
    pt_top += d
    c_cre = cor_run(im, (px0, pt_top, pit0 - 30, pt_top + 75), TXT)
    c_our = cor_run(im, (pit0 - 5, pt_top, px1 + 5, pt_top + 75), TXT)
    pt_runs = [('O protocolo tridimensional ', SANS, c_cre), ('resolve os 3', SANS_IT, c_our)]
    tp = calibrar_runs(pt_runs, px1 - px0 + 1)
    base = base_de(pt_runs, tp, pt_top)
    im = apagar_col(im, (px0 - 30, pt_top - 15, px1 + 30, pt_top + 90), TXT, 4)
    desenhar(im, [('El protocolo tridimensional ', SANS, c_cre), ('resuelve los 3', SANS_IT, c_our)], tp, base,
             cx=(px0 + px1) / 2)

    # ---- CTA dourado: apaga o texto, alarga o miolo do botão, escreve
    bx0, by0, bx1, by1 = p['btn']
    by0 += d; by1 += d
    tx0, tx1, ttop = p['btn_txt']
    ttop += d
    cor_cta = cor_run(im, (tx0, ttop, tx1, ttop + 50), ESC, claro=False)
    pt_c = [('QUERO EVITAR ESSES ERROS', CTA, cor_cta)]
    tc = calibrar_runs(pt_c, tx1 - tx0 + 1, CTA_TR)
    base = base_de(pt_c, tc, ttop, CTA_TR * tc)
    im = apagar_col(im, (tx0 - 15, ttop - 22, tx1 + 15, ttop + 75), ESC, 3)
    es_c = [('QUIERO EVITAR ESTOS ERRORES', CTA, cor_cta)]
    larg_es = (lambda b: b[2] - b[0])(desenhar(im, es_c, tc, 0, x_esq=0, tracking=CTA_TR * tc, so_medir=True))
    extra = int(np.ceil(larg_es - (tx1 - tx0)))
    if extra > 0:
        cort_e, cort_d = tx0 - 20, p['btn_seta'] - 20
        im = esticar_horizontal(im, (bx0, by0, bx1, by1), bx0 - extra // 2, bx1 + (extra - extra // 2), cort_e, cort_d)
        tx0n = tx0 - extra // 2
    else:
        tx0n = tx0 + (tx1 - tx0 - larg_es) / 2
    desenhar(im, es_c, tc, base, x_esq=tx0n, tracking=CTA_TR * tc)
    print(fmt, 'título', tam, 'passo', passo, 'CTA alargado', extra)
    return im, p['saida']


if __name__ == '__main__':
    for fmt in ('feed', 'story'):
        im, nome = gerar(fmt)
        print(salvar(im, nome))
