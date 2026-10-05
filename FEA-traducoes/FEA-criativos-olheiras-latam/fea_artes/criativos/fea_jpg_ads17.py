#!/usr/bin/env python3
"""[FEED] ADS 17 (jpg) em espanhol LATAM. Troca só a copy.
Livro e tablet com página do ebook (mockup, página gerada por IA no original) ficam intactos: fase 2.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads17.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

ORIG = 'trabalho/ads17-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 17 - LATAM.jpg'

BRANCO = lambda r, g, b: (r > 150) & (g > 150) & (b > 135)
OURO = lambda r, g, b: (r > 140) & (r - b > 55)
ESCURO = lambda r, g, b: (r + g + b) < 420
MARROM_TXT = lambda r, g, b: (r > g) & (g > b) & (r - b > 35) & (r < 190)
REG, BOLD = 'Gelasio_400Regular', 'Gelasio_700Bold'
LETRA_SELO = lambda r, g, b: ((r + g + b) < 360) & (r > b + 15)


def gerar():
    im0 = abrir(ORIG)
    im = im0.copy()

    # manchete: 'O guia clínico mais vendido / sobre olheiras'
    branco = cor_nucleo(im0, (167, 40, 352, 100), BRANCO, 50, escuro=False)
    grad_h = grad_rel(im0, (371, 40, 938, 87), OURO)
    im = apagar(im, (150, 28, 960, 165), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    th = tam_por_cap(BOLD, 87 - 40, 'O')
    ouro_h = ('grad', grad_h, 40, 87)
    b1, b2 = 87, base_de(BOLD, th, 'sobre olheiras', 107)
    cxh = 552
    L1 = lambda s: [('La guía ', BOLD, s, branco), ('clínica', BOLD, s, ('grad', grad_h, b1 - (87 - 40) * s / th, b1)),
                    (' sobre ojeras con', BOLD, s, branco)]
    L2 = lambda s: [('más de 30 mil copias vendidas', BOLD, s, ('grad', grad_h, b2 - (87 - 40) * s / th, b2))]
    t2 = min(caber(L1, th, 1000 - 80, 0.15), caber(L2, th, 1000 - 80, 0.15))
    linha(im, L1(t2), b1, cxh, 'centro')
    linha(im, L2(t2), b2, cxh, 'centro')

    # 'Aprenda a técnica tridimensional / por apenas R$97'
    branco2 = cor_nucleo(im0, (248, 216, 842, 257), BRANCO, 50, escuro=False)
    grad_p = grad_rel(im0, (603, 263, 706, 307), OURO)
    im = apagar(im, (230, 208, 860, 316), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    ta = tam_por_largura(lambda s: [('Aprenda a técnica tridimensional', REG, s, branco2)], 842 - 248)
    ba1 = base_de(REG, ta, 'Aprenda a técnica tridimensional', 216)
    ba2 = ba1 + 50
    linha(im, [('Aprenda la técnica tridimensional', REG, ta, branco2)], ba1, 545, 'centro')
    preco = PRECOS['preco']
    seg2 = lambda s: [('por solo ', REG, ta, branco2), (preco, BOLD, s, ('grad', grad_p, ba2 - 0.72 * s, ba2))]
    tp = caber(seg2, ta, 1000 - 90, 0.5)
    linha(im, seg2(tp), ba2, 548, 'centro')

    # faixa clara
    verde = cor_nucleo(im0, (222, 353, 862, 401), ESCURO, 30)
    marrom = cor_nucleo(im0, (201, 410, 373, 448), MARROM_TXT, 30)
    im = apagar(im, (180, 345, 905, 525), lambda r, g, b: ESCURO(r, g, b) | MARROM_TXT(r, g, b) | ((r + g + b) < 560), 3, 6)
    tb = tam_por_cap(REG, 391 - 355, 'T')
    linhas_b = [
        (391, [('Convierta', BOLD, verde), (' el relleno de', REG, verde)]),
        (391 + 57, [('ojeras', BOLD, marrom), (' en su ', REG, verde), ('mayor diferencial', BOLD, marrom)]),
        (391 + 57 * 2, [('dentro de la armonización facial.', REG, verde)]),
    ]
    tb2 = min(caber(lambda s, sg=sg: [(x, n, s, c) for x, n, c in sg], tb, 1000 - 90, 0.15) for _, sg in linhas_b)
    for base, sg in linhas_b:
        linha(im, [(x, n, tb2, c) for x, n, c in sg], base, 545, 'centro')

    # faixa escura
    branco3 = cor_nucleo(im0, (230, 559, 833, 597), BRANCO, 50, escuro=False)
    im = apagar(im, (190, 552, 890, 650), BRANCO, 3, 6)
    td = tam_por_largura(lambda s: [('precisão anatômica e previsibilidade real.', REG, s, branco3)], 875 - 207)
    bd1 = base_de(REG, td, 'Método comprovado para atuar com', 559)
    bd2 = base_de(REG, td, 'precisão anatômica e previsibilidade real.', 604)
    ld = [(bd1, 'Un método probado para trabajar con'), (bd2, 'precisión anatómica y previsibilidad real.')]
    td2 = min(caber(lambda s, t=t: [(t, REG, s, branco3)], td, 1000 - 90, 0.15) for _, t in ld)
    for base, t in ld:
        linha(im, [(t, REG, td2, branco3)], base, 540, 'centro')

    # selo (sobre o livro): arco superior e acento de CÓPIAS
    # círculo do texto ajustado pelos centros das letras (o selo está em perspectiva)
    info = trocar_arco_selo(im, 185.9, 1150.9, 91, 102, 'O PRIMEIRO & MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL',
                            'Montserrat_700Bold', ang_lim=(-150, -36), cond=LETRA_SELO, pct_cor=15, escala=0.7,
                            ang_fixo=(-145, -41))

    # CÓPIAS -> COPIAS: só os pixels escuros do acento, acima do O
    acento = (139, 1151, 145, 1155)
    im = apagar(im, acento, lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 168, 0, 3)

    # CTA
    branco_c = cor_nucleo(im0, (341, 1266, 566, 1297), BRANCO, 50, escuro=False)
    grad_c = grad_rel(im0, (581, 1266, 827, 1297), OURO)
    im = apagar(im, (330, 1255, 845, 1310), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    CTA = 'NotoSerif_600SemiBold'
    tc = tam_por_largura(lambda s: [('TOQUE EM SAIBA MAIS', CTA, s, branco_c)], 827 - 341)
    seg = lambda s: [('TOQUE EN ', CTA, s, branco_c), ('MÁS INFORMACIÓN', CTA, s, ('grad', grad_c, 1266, 1297))]
    LIM = 862 - 312  # entre o ícone da mão e a borda direita do botão
    tc2 = caber(seg, tc, LIM, 0.15)
    linha(im, seg(tc2), 1297, (312 + 862) / 2, 'centro')

    p = salvar(im, SAIDA_NOME)
    print('ok', p, im.size, 'selo', info, 'CTA reducao %.0f%%' % ((1 - tc2 / tc) * 100), 'manchete %.1f->%.1f' % (th, t2))


if __name__ == '__main__':
    gerar()
