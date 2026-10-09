#!/usr/bin/env python3
"""[FEED] ADS 20 e [STORIES] ADS 20 (jpg) em espanhol LATAM. Troca só a copy.
Foto do Dr. João, livro e tablet (mockup, página do tablet gerada por IA no original) intactos: fase 2.
Feed e Story têm o mesmo layout em escalas/posições diferentes: medidas próprias de cada um em V.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads20.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

TIT = 'NotoSerif_500Medium'
SANS, SANS_B = 'NotoSans_400Regular', 'NotoSans_700Bold'
BIG = 'NotoSerif_700Bold'
ESCURO = lambda r, g, b: ((r + g + b) < 420) & (g >= r - 5)
OURO = lambda r, g, b: (r > 140) & (r - b > 55) & (g < 210)
BRANCO = lambda r, g, b: (r > 190) & (g > 190) & (b > 180)
LETRA_SELO = lambda r, g, b: ((r + g + b) < 380) & (r > b + 15)

V = {
    'feed': dict(
        orig='trabalho/ads20-feed.jpg', saida='FEA-[FEED] ADS 20 - LATAM.jpg',
        x_txt=66, x_lim=560,               # margem esquerda do texto e limite antes da foto
        tit=[(203, 'Você não evita'), (271, 'olheiras por falta'), (339, 'de técnica,')], tit_larg=(65, 450),
        tit_caixa=(52, 195, 560, 400), tecnica=(144, 339, 331, 384),
        sans=[(420, 'você evita porque sabe'), (462, 'o risco que está correndo.')], sans_larg=(66, 439),
        sans_caixa=(52, 412, 560, 505), risco=(97, 462, 172, 487),
        apr=[(560, 'Aprenda a decidir com'), (594, 'segurança: profundidade, plano e'), (629, 'quantidade (sem improviso).')],
        apr_larg=(66, 512), apr_caixa=(52, 552, 560, 664),
        pl=[(737, 'De R$297'), (781, 'por apenas')], pl_larg=(100, 256), big=(291, 727, 516, 811),
        preco_caixa=(84, 712, 545, 828), preco_box=(64, 540),
        selo=(462.5, 961.9, 58.5, 65.5, (-144, -22)), acento=(427, 970, 431, 973),
        cta=(534, 1251, 1033, 'Toque em Saiba Mais e garanta o seu.'), pilula=(508, 1065), cta_caixa=(520, 1240, 1052, 1290),
    ),
    'story': dict(
        orig='trabalho/ads20-story.jpg', saida='FEA-[STORIES] ADS 20 - LATAM.jpg',
        x_txt=70, x_lim=590,
        tit=[(374, 'Você não evita'), (445, 'olheiras por falta'), (517, 'de técnica,')], tit_larg=(69, 476),
        tit_caixa=(55, 365, 595, 585), tecnica=(153, 517, 350, 565),
        sans=[(603, 'você evita porque sabe'), (648, 'o risco que está correndo.')], sans_larg=(70, 465),
        sans_caixa=(55, 595, 595, 692), risco=(102, 647, 182, 674),
        apr=[(751, 'Aprenda a decidir com'), (787, 'segurança: profundidade, plano e'), (824, 'quantidade (sem improviso).')],
        apr_larg=(70, 542), apr_caixa=(55, 742, 595, 862),
        pl=[(938, 'De R$297'), (985, 'por apenas')], pl_larg=(106, 271), big=(308, 935, 546, 1016),
        preco_caixa=(90, 922, 575, 1040), preco_box=(70, 570),
        selo=(488.8, 1177.1, 62.5, 70, (-143, -22)), acento=(452, 1185, 456, 1188),
        cta=(242, 1635, 835, 'Toque em Saiba Mais e garanta o seu.'), pilula=(219, 862), cta_caixa=(228, 1625, 853, 1676),
    ),
}


def criativo(v):
    im0 = abrir(v['orig'])
    im = im0.copy()
    X = v['x_txt']

    # manchete serifada (3 linhas, 'técnica' dourado)
    verde = cor_nucleo(im0, (v['tit_larg'][0], v['tit'][1][0], v['tit_larg'][1], v['tit'][1][0] + 45), ESCURO, 30)
    tc = v['tecnica']
    grad_t = grad_rel(im0, tc, OURO)
    im = apagar(im, v['tit_caixa'], lambda r, g, b: ESCURO(r, g, b) | OURO(r, g, b), 3, 6)
    tt = tam_por_largura(lambda s: [(v['tit'][0][1], TIT, s, verde)], v['tit_larg'][1] - v['tit_larg'][0])
    bases = [base_de(TIT, tt, pt, y) for y, pt in v['tit']]
    ytec = (tc[1], tc[3])
    L = [[('Usted no evita', verde)], [('tratar ojeras por', verde)],
         [('falta de ', verde), ('técnica', ('grad', grad_t, ytec[0], ytec[1])), (':', verde)]]
    t1 = min(caber(lambda s, sg=sg: [(x, TIT, s, c) for x, c in sg], tt, v['x_lim'] - X, 0.15) for sg in L)
    for base, sg in zip(bases, L):
        linha(im, [(x, TIT, t1, c) for x, c in sg], base, X)

    # duas linhas sans ('riesgo' dourado em negrito)
    cor_s = cor_nucleo(im0, (v['sans_larg'][0], v['sans'][0][0], v['sans_larg'][1], v['sans'][0][0] + 30), ESCURO, 30)
    ouro_s = cor_nucleo(im0, (v['risco'][0], v['risco'][1], v['risco'][2], v['risco'][3]), OURO, 40)
    im = apagar(im, v['sans_caixa'], lambda r, g, b: ESCURO(r, g, b) | OURO(r, g, b), 3, 6)
    ts = tam_por_largura(lambda s: [(v['sans'][0][1], SANS, s, cor_s)], v['sans_larg'][1] - v['sans_larg'][0])
    L = [[('lo evita porque conoce', SANS, cor_s)], [('el ', SANS, cor_s), ('riesgo', SANS_B, ouro_s), (' que corre.', SANS, cor_s)]]
    for (y, pt), sg in zip(v['sans'], L):
        linha(im, [(x, n, ts, c) for x, n, c in sg], base_de(SANS, ts, pt, y), X)

    # 'Aprenda a decidir com segurança: ...'
    cor_a = cor_nucleo(im0, (v['apr_larg'][0], v['apr'][0][0], v['apr_larg'][1], v['apr'][0][0] + 28), ESCURO, 30)
    im = apagar(im, v['apr_caixa'], ESCURO, 3, 6)
    ta = tam_por_largura(lambda s: [('segurança:', SANS_B, s, cor_a), (' profundidade, plano e', SANS, s, cor_a)],
                         v['apr_larg'][1] - v['apr_larg'][0])
    L = [[('Aprenda a decidir con', SANS_B)], [('seguridad:', SANS_B), (' profundidad, plano y', SANS)], [('cantidad (sin improvisar).', SANS)]]
    for (y, pt), sg in zip(v['apr'], L):
        ref = SANS_B if pt.startswith(('Aprenda', 'segurança')) else SANS
        linha(im, [(x, n, ta, cor_a) for x, n in sg], base_de(ref, ta, pt, y), X)

    # caixa de preço: 'De R$297 / por apenas' + 'R$97' -> 'De US$ [ANT] / a solo' + 'US$ [PRECIO]'
    cor_p = cor_nucleo(im0, (v['pl_larg'][0], v['pl'][0][0], v['pl_larg'][1], v['pl'][1][0] + 25), ESCURO, 30)
    bg = v['big']
    cor_big = cor_nucleo(im0, (bg[0], bg[1], bg[2], bg[3]), ESCURO, 30)
    im = apagar(im, v['preco_caixa'], ESCURO, 3, 6)
    tp = tam_por_largura(lambda s: [('por apenas', SANS, s, cor_p)], v['pl_larg'][1] - v['pl_larg'][0])
    tb = tam_por_cap(BIG, bg[3] - bg[1], 'R')
    ant, atual = PRECOS['de_297'], PRECOS['preco']
    x0b, x1b = v['preco_box']
    pad = v['pl_larg'][0] - x0b
    gap = bg[0] - v['pl_larg'][1]
    disp = (x1b - x0b) - 2 * pad + 6
    k = 1.0  # escala do preço grande; o texto pequeno da esquerda não desce de 60 % (legibilidade)
    while True:
        kl = max(k, 0.6)
        wl = max(largura_segs([('De ' + ant, SANS, tp * kl, cor_p)]), largura_segs([('a solo', SANS, tp * kl, cor_p)]))
        wb = largura_segs([(atual, BIG, tb * k, cor_big)])
        if wl + gap * k + wb <= disp or k < 0.25:
            break
        k -= 0.01
    xl = (x0b + x1b) / 2 - (wl + gap * k + wb) / 2
    yc = (bg[1] + bg[3]) / 2  # centro vertical do bloco original
    b_big = yc + (bg[3] - bg[1]) * k / 2
    b1o = base_de(SANS, tp, v['pl'][0][1], v['pl'][0][0])
    b2o = base_de(SANS, tp, v['pl'][1][1], v['pl'][1][0])
    meio = (b1o + b2o) / 2
    linha(im, [('De ' + ant, SANS, tp * kl, cor_p)], yc + (b1o - meio) * kl + (meio - yc) * kl, xl)
    linha(im, [('a solo', SANS, tp * kl, cor_p)], yc + (b2o - meio) * kl + (meio - yc) * kl, xl)
    linha(im, [(atual, BIG, tb * k, cor_big)], b_big, xl + wl + gap * k)
    k_preco = k

    # selo: arco superior + acento de CÓPIAS
    cx, cy, r0, r1, angs = v['selo']
    info = trocar_arco_selo(im, cx, cy, r0, r1, 'O PRIMEIRO & MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL', 'Montserrat_700Bold',
                            ang_lim=(angs[0] - 6, angs[1] + 6), cond=LETRA_SELO, pct_cor=15, escala=0.75, ang_fixo=angs)
    im = apagar(im, v['acento'], lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 185, 0, 2)

    # CTA na pílula verde
    x0c, ytc, x1c, ptc = v['cta']
    branco = cor_nucleo(im0, (x0c, ytc, x1c, ytc + 26), BRANCO, 50, escuro=False)
    im = apagar(im, v['cta_caixa'], BRANCO, 3, 6)
    tcta = tam_por_largura(lambda s: [(ptc, SANS_B, s, branco)], x1c - x0c)
    tr = 0.0
    if largura_segs([(ptc, SANS_B, tcta, branco)]) < (x1c - x0c) - 10:  # original com tracking
        tr = track_para(ptc, SANS_B, tcta, x1c - x0c)
    es = 'Toque en Más información y asegure el suyo.'
    p0, p1 = v['pilula']
    LIM = (p1 - p0) - 2 * 18
    trb = tr
    while largura_segs([(es, SANS_B, tcta, branco)], trb) > LIM and trb > 0:
        trb = max(0.0, trb - 0.1)
    t2 = caber(lambda s: [(es, SANS_B, s, branco)], tcta, LIM, 0.15, trb)
    bc = base_de(SANS_B, tcta, ptc, ytc)
    bc -= (tcta - t2) * 0.36  # recentra verticalmente a linha menor
    linha(im, [(es, SANS_B, t2, branco)], bc, (p0 + p1) / 2, 'centro', tr=trb)

    p = salvar(im, v['saida'])
    print('ok', p, im.size, 'tit %.1f->%.1f' % (tt, t1), 'preco k %.2f' % k_preco, 'cta %.1f->%.1f tr %.2f->%.2f' % (tcta, t2, tr, trb),
          'selo', info)


if __name__ == '__main__':
    for nome in ('feed', 'story'):
        criativo(V[nome])
