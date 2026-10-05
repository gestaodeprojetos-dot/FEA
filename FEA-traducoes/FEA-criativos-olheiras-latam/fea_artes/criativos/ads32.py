#!/usr/bin/env python3
"""FEA · Ads 32 (Feed e Story, png) · Ebook Olheiras LATAM.

Troca só a copy. Fontes do original: Noto Serif SemiBold (título), Open Sans Regular/Italic
(linha da previsibilidade), Noto Sans ExtraBold com tracking 0,04 em (CTA).
Selo '+30 MIL CÓPIAS VENDIDAS': só o acento do Ó é removido (COPIAS), o resto do selo é intacto.
Mockup do ebook (capa PT no tablet) fica para a fase 2.
Rodar a partir de fea_artes/:  python3 criativos/ads32.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar
from fea_util_ads31a35 import *

SERIF = 'NotoSerif_600SemiBold'
SANS = 'OpenSans_400Regular'
SANS_IT = 'OpenSans_400Regular_Italic'
CTA = 'NotoSans_800ExtraBold'
CTA_TR = 0.04
VERDE = lambda r, g, b: (r + g + b < 300) & (g >= r)
OURO = lambda r, g, b: (r - b > 70) & (r > 150)
TIT = lambda r, g, b: ((r + g + b < 420) & (g >= r - 5)) | ((r - b > 50) & (r > 140))
CINZA = lambda r, g, b: (r + g + b < 560)

M = {
    'feed': dict(arq='trabalho/loteI-ads32-feed.png', saida='FEA-Ads 32 Feed - PTO-LATAM.png',
                 acento=(1335, 1296, 1348, 1304),
                 tit=[(1537, 629, 1530), (1648, 590, 1567), (1758, 213, 1944)], larg_max=1860,
                 dif=(1952, 554, 1161, 1584, 1599),
                 pilula=(394, 2084, 1766, 2249), cta=(466, 1601, 2150), seta=(1625, 1712)),
    'story': dict(arq='trabalho/loteI-ads32-story.png', saida='FEA-Ads 32 Story - PTO-LATAM.png',
                  acento=(1312, 1759, 1324, 1767),
                  tit=[(2364, 587, 1570), (2485, 545, 1610), (2604, 135, 2021)], larg_max=1900,
                  dif=(2815, 506, 1168, 1628, 1644),
                  pilula=(332, 2960, 1826, 3140), cta=(410, 1646, 3031), seta=(1675, 1765)),
}

PT = ['Tem profissional', 'cobrando menos...', 'e ainda pegando mais pacientes.']
ES = ['Hay profesionales que', 'cobran menos…', 'y aun así atienden a más pacientes.']


def gerar(fmt):
    p = M[fmt]
    im = abrir(p['arq'])
    W, H = im.size

    # selo: tira só o acento agudo do Ó (CÓPIAS -> COPIAS)
    im = apagar_col(im, p['acento'], lambda r, g, b: (r + g + b) < 420, 1)

    # ---- título 3 linhas
    (t1, a0, a1), (t2, g0, g1), (t3, c0, c1) = p['tit']
    verde = cor_run(im, (c0, t3, c1, t3 + 110), VERDE, claro=False)
    ouro = cor_run(im, (g0, t2 + 5, g1, t2 + 85), OURO)
    tam = calibrar_runs([(PT[2], SERIF, verde)], c1 - c0 + 1)
    bases = [base_de([(PT[i], SERIF, verde)], tam, t) for i, t in enumerate((t1, t2, t3))]
    cx = (c0 + c1) / 2
    runs = [[(ES[0], SERIF, verde)], [(ES[1], SERIF, ouro)], [(ES[2], SERIF, verde)]]
    tam_es = min(caber(r, tam, p['larg_max'])[0] for r in runs)
    red = 1 - tam_es / tam
    im = apagar_misto(im, (80, t1 - 20, W - 80, t3 + 125), TIT, 4)
    # mantém o centro vertical do bloco ao reduzir
    meio = (bases[0] + bases[2]) / 2
    for i, r in enumerate(runs):
        b = meio + (bases[i] - meio) * (tam_es / tam)
        bb = desenhar(im, r, tam_es, b, cx=cx)
        assert bb[0] > 100 and bb[2] < W - 100, bb

    # ---- 'A diferença está na previsibilidade.'
    top, x0, xi, xi1, x1 = p['dif']
    cinza = cor_run(im, (x0, top, xi - 25, top + 70), CINZA, claro=False)
    c_it = cor_run(im, (xi, top, xi1, top + 70), OURO, claro=False)
    pt_runs = [('A diferença está na ', SANS, cinza), ('previsibilidade', SANS_IT, c_it), ('.', SANS, cinza)]
    ts = calibrar_runs(pt_runs, x1 - x0 + 1)
    base = base_de(pt_runs, ts, top)
    im = apagar_misto(im, (x0 - 30, top - 15, x1 + 30, top + 85), lambda r, g, b: CINZA(r, g, b) | OURO(r, g, b), 4)
    es_runs = [('La diferencia está en la ', SANS, cinza), ('previsibilidad', SANS_IT, c_it), ('.', SANS, cinza)]
    bb = desenhar(im, es_runs, ts, base, cx=(x0 + x1) / 2)
    assert bb[0] > 100 and bb[2] < W - 100, bb

    # ---- CTA (pílula verde escura): apaga texto, recentra o grupo texto + seta
    px0, py0, px1, py1 = p['pilula']
    tx0, tx1, ttop = p['cta']
    s0, s1 = p['seta']
    cor_c = cor_run(im, (tx0, ttop, tx1, ttop + 45), OURO)
    pt_c = [('QUERO AUMENTAR MINHA PREVISIBILIDADE', CTA, cor_c)]
    tc = calibrar_runs(pt_c, tx1 - tx0 + 1, CTA_TR)
    base = base_de(pt_c, tc, ttop, CTA_TR * tc)
    es_c = [('QUIERO AUMENTAR MI PREVISIBILIDAD', CTA, cor_c)]
    lw = (lambda b: b[2] - b[0])(desenhar(im, es_c, tc, 0, x_esq=0, tracking=CTA_TR * tc, so_medir=True))
    folga = (tx1 - tx0) - lw          # quanto o texto ES é mais curto
    desl = int(round(folga / 2))       # o grupo inteiro recentra: texto anda +desl, seta anda -desl
    yy0, yy1 = ttop - 30, ttop + 75
    seta = im.crop((s0, yy0, s1, yy1))
    claro = lambda r, g, b: (r + g + b) > 160
    im = apagar_col(im, (tx0 - 20, yy0, s1 + 5, yy1), claro, 4)
    # a seta (círculo translúcido + chevron) é recolocada inteira, deslocada
    im = apagar_seta(im, (s0, yy0, s1, yy1))
    im.paste(seta, (s0 - desl, yy0))
    desenhar(im, es_c, tc, base, x_esq=tx0 + desl, tracking=CTA_TR * tc)
    print(fmt, 'título', tam, '->', tam_es, 'redução %.1f%%' % (red * 100), 'CTA desl', desl)
    return im, p['saida']


def apagar_seta(im, caixa):
    """Repinta a área da seta com a interpolação de cada coluna entre as bordas de cima e de baixo
    (pílula lisa)."""
    x0, y0, x1, y1 = caixa
    a = np.array(im).astype(float)
    top, bot = a[y0, x0:x1], a[y1 - 1, x0:x1]
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = top[None] * (1 - t) + bot[None] * t
    return Image.fromarray(a.round().astype(np.uint8))


if __name__ == '__main__':
    for fmt in ('feed', 'story'):
        im, nome = gerar(fmt)
        print(salvar(im, nome))
