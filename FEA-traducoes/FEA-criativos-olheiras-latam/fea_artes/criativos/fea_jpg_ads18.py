#!/usr/bin/env python3
"""[FEED] ADS 18 e [STORIES] ADS 18 (jpg) em espanhol LATAM. Troca só a copy.
Livro e tablet (mockup, página do tablet gerada por IA no original) ficam intactos: fase 2.
O Story repete as 1350 linhas de cima do Feed pixel a pixel; só acrescenta o botão de CTA.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads18.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

SANS, SANS_B = 'NotoSans_400Regular', 'NotoSans_700Bold'
SERIF, SERIF_B = 'NotoSerif_400Regular', 'NotoSerif_700Bold'
ESCURO = lambda r, g, b: (r + g + b) < 420
OURO_TXT = lambda r, g, b: (r > 120) & (r - b > 55) & (g < 190)
BRANCO = lambda r, g, b: (r > 170) & (g > 170) & (b > 150)
AMARELO = lambda r, g, b: (r > 190) & (g > 140) & (b < 160) & (r - b > 60)
LETRA_SELO = lambda r, g, b: ((r + g + b) < 360) & (r > b + 15)
CX = 590.5


def comum(im0):
    im = im0.copy()
    preto = cor_nucleo(im0, (211, 181, 970, 213), ESCURO, 30)

    # 'Nenhum outro lugar no Brasil ensina esse método.'
    im = apagar(im, (195, 172, 990, 222), ESCURO, 3, 6)
    t = tam_por_largura(lambda s: [('Nenhum outro lugar no Brasil ensina esse método.', SANS, s, preto)], 970 - 211)
    linha(im, [('Un método exclusivo del Dr. João Pithon.', SANS, t, preto)],
          base_de(SANS, t, 'Nenhum outro lugar no Brasil ensina esse método.', 181), CX, 'centro')

    # parágrafo grande
    verde = cor_nucleo(im0, (261, 268, 917, 313), ESCURO, 30)
    ouro = cor_nucleo(im0, (174, 404, 500, 454), OURO_TXT, 30)
    im = apagar(im, (150, 250, 1030, 534), lambda r, g, b: ESCURO(r, g, b) | OURO_TXT(r, g, b) | ((r + g + b) < 560), 3, 6)
    tb = tam_por_largura(lambda s: [('isso, poucos dominam essa técnica.', SERIF, s, verde)], 1004 - 174)
    passo = 68
    b0 = base_de(SERIF_B, tb, 'quando ninguém te dá um', 336) - passo
    linhas_ = [
        [('Es difícil dominar las ojeras', SERIF_B, verde)],
        [('cuando nadie le da un', SERIF_B, verde)],
        [('protocolo clínico', SERIF_B, ouro), (' para seguir.', SERIF_B, verde), (' Por', SERIF, verde)],
        [('eso, pocos dominan esta técnica.', SERIF, verde)],
    ]
    tt = min(caber(lambda s, sg=sg: [(x, n, s, c) for x, n, c in sg], tb, 1040 - 140, 0.15) for sg in linhas_)
    for i, sg in enumerate(linhas_):
        linha(im, [(x, n, tt, c) for x, n, c in sg], b0 + passo * i, CX, 'centro')

    # 'Você tem duas opções:'
    im = apagar(im, (400, 600, 780, 650), ESCURO, 3, 6)
    t = tam_por_largura(lambda s: [('Você tem duas opções:', SANS, s, preto)], 759 - 419)
    linha(im, [('Tiene dos opciones:', SANS, t, preto)], base_de(SANS, t, 'Você tem duas opções:', 609), CX, 'centro')

    # opção 1 (caixa vermelha)
    im = apagar(im, (390, 705, 1035, 757), ESCURO, 3, 6)
    t = tam_por_largura(lambda s: [('Continuar evitando olheiras por medo;', SANS, s, preto)], 976 - 401)
    es = 'Seguir evitando tratar ojeras por miedo;'
    t1 = caber(lambda s: [(es, SANS, s, preto)], t, 1030 - 401, 0.15)
    linha(im, [(es, SANS, t1, preto)], base_de(SANS, t, 'Continuar evitando olheiras por medo;', 717), 401)

    # opção 2 (caixa verde)
    branco = cor_nucleo(im0, (401, 829, 540, 860), BRANCO, 50, escuro=False)
    amarelo = cor_nucleo(im0, (553, 829, 745, 860), AMARELO, 50, escuro=False)
    im = apagar(im, (390, 818, 1035, 912), lambda r, g, b: BRANCO(r, g, b) | AMARELO(r, g, b), 3, 6)
    b1 = base_de(SANS, t, 'Ou pagar apenas', 829)
    b2 = base_de(SANS, t, 'mapear e tratar com segurança.', 876)
    preco = PRECOS['preco']
    L1 = lambda s: [('O pagar ', SANS, s, branco), ('solo ' + preco, SANS_B, s, amarelo), (' para aprender', SANS, s, branco)]
    L2 = lambda s: [('a mapearlas y tratarlas con seguridad.', SANS, s, branco)]
    t2 = min(caber(L1, t, 1030 - 401, 0.15), caber(L2, t, 1030 - 401, 0.15))
    linha(im, L1(t2), b1, 401)
    linha(im, L2(t2), b2, 401)

    # caixa do ebook
    im = apagar(im, (630, 1088, 1030, 1205), BRANCO, 3, 6)
    te = tam_por_largura(lambda s: [('Ebook prático com passos', SANS, s, branco)], 966 - 642)
    for pt, yt, es in [('Ebook prático com passos', 1097, 'Ebook práctico con pasos'),
                       ('em 3D, casos reais e', 1134, 'en 3D, casos reales y'),
                       ('aplicações comentadas.', 1171, 'aplicaciones comentadas.')]:
        linha(im, [(es, SANS, te, branco)], base_de(SANS, te, pt, yt), 641)

    # selo: arco superior ('O PRIMEIRO & MAIS VENDIDO') e acento de CÓPIAS
    info = trocar_arco_selo(im, 490.5, 990.7, 54.5, 60.5, 'O PRIMEIRO & MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL',
                            'Montserrat_700Bold', ang_lim=(-150, -15), cond=LETRA_SELO, pct_cor=15, escala=0.75,
                            ang_fixo=(-141, -23))
    # CÓPIAS -> COPIAS: só os pixels escuros do acento, acima do O
    im = apagar(im, (458, 996, 463, 999), lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 185, 0, 2)
    return im, info, (t, t1, t2)


def gerar():
    im0 = abrir('trabalho/ads18-feed.jpg')
    im, info, tams = comum(im0)
    p1 = salvar(im, 'FEA-[FEED] ADS 18 - LATAM.jpg')

    s0 = abrir('trabalho/ads18-story.jpg')
    st, _, _ = comum(s0)
    # CTA do Story (botão em degradê verde): 'TOQUE EM SAIBA MAIS' -> 'TOQUE EN MÁS INFORMACIÓN'
    branco = cor_nucleo(s0, (415, 1532, 765, 1555), BRANCO, 50, escuro=False)
    st = apagar(st, (400, 1522, 790, 1565), BRANCO, 3, 6)
    tc = tam_por_cap(SANS_B, 1554 - 1532, 'T')
    tr = track_para('TOQUE EM SAIBA MAIS', SANS_B, tc, 765 - 415)
    es = 'TOQUE EN MÁS INFORMACIÓN'
    LIM = 805 - 380  # botão vai de ~348 a ~835
    trb = tr
    while largura_segs([(es, SANS_B, tc, branco)], trb) > LIM and trb > tr * 0.4:
        trb -= 0.1
    tc2 = caber(lambda s: [(es, SANS_B, s, branco)], tc, LIM, 0.15, trb)
    linha(st, [(es, SANS_B, tc2, branco)], 1554, CX, 'centro', tr=trb)
    p2 = salvar(st, 'FEA-[STORIES] ADS 18 - LATAM.jpg')
    print('ok', p1, im.size, p2, st.size, 'selo', info, 'tamanhos', tams, 'cta', tc, tc2, tr, trb)


if __name__ == '__main__':
    gerar()
