#!/usr/bin/env python3
"""[FEED] ADS 14 (jpg) em espanhol LATAM. Troca só a copy; foto, livro (mockup, fase 2) e layout intactos.
Rodar de fea_artes/:  python3 criativos/ads14.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads14a20 import *  # noqa

ORIG = 'trabalho/ads14-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 14 - LATAM.jpg'

OURO = lambda r, g, b: (r > 60) & (r - b > 18) & (r >= g)
BRANCO = lambda r, g, b: (r > 120) & (g > 120) & (b > 110) & (abs(r - b) < 45)
SERIF_TXT = 'Tinos_400Regular'
SERIF_CAPS = 'NotoSerif_500Medium'
SERIF_PRECO = 'PlayfairDisplay_500Medium'


def titulo(im0):
    """RELLENO / TRIDIMENSIONAL (intacta) / DE OJERAS, com as letras do próprio título original."""
    limpo = apagar(im0, (80, 118, 790, 196), OURO, 3, 6)
    limpo = apagar(limpo, (262, 281, 600, 359), OURO, 3, 6)  # 'LHEIRAS' (DE O fica)
    im = limpo.copy()
    # glifos do original: (x0, x1) e linha (y0, y1) da caixa de recorte
    L1, L3 = (119, 196), (282, 359)
    g = {'R': (136, 184, L1), 'E': (191, 232, L1), 'E2': (240, 281, L1), 'N': (289, 339, L1),
         'O': (717, 768, L1), 'L': (269, 308, L3), 'E3': (374, 415, L3), 'R3': (449, 496, L3),
         'A': (501, 550, L3), 'S': (557, 592, L3)}
    m = 3

    def por(seq, x, y_lin, gaps):
        for k, gap in zip(seq, gaps):
            x0, x1, (y0, y1) = g[k]
            transplantar(im, im0, limpo, (x0 - m, y0, x1 + m + 1, y1), x - m, y_lin)
            x = x + (x1 - x0) + 1 + gap
        return x

    # linha 1: RELLENO alinhada à esquerda em x=88 (borda do P original)
    por(['R', 'E', 'L', 'L', 'E2', 'N', 'O'], 88, L1[0], [7, 7, 6, 7, 8, 7, 0])
    # linha 3: 'DE O' original, J desenhado, E R A S do próprio 'OLHEIRAS'
    grad = grad_rel(im0, (370, 290, 600, 349), OURO)
    xj = 262 + 8
    nome_j = 'Gelasio_500Medium'  # J que pousa na linha de base, peso igual ao título
    tam = tam_por_cap(nome_j, 349 - 290)
    f = F(nome_j, tam)
    lj = f.getbbox('J', anchor='ls')
    x_ini, x_fim = linha(im, [('J', nome_j, tam, ('grad', grad, 290, 348))], 348, xj, 'esquerda')
    por(['E3', 'R3', 'A', 'S'], int(round(x_fim)) + 8, L3[0], [7, 5, 7, 0])
    return im


def selo(im):
    info = trocar_arco_selo(im, 931.5, 327.5, 91, 103, 'O PRIMEIRO E MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL',
                            'Montserrat_600SemiBold', ang_lim=(-175, -5))
    # CÓPIAS -> COPIAS: apaga só o acento (componente pequeno acima do O)
    acento = (874, 337, 881, 342)  # pixels escuros do acento agudo, acima do O
    im = apagar(im, acento, lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 180, 1, 3)
    return im, info, acento


def gerar():
    im0 = abrir(ORIG)
    im = titulo(im0)

    # subtítulo branco
    sub = (80, 405, 560, 482)
    cor = cor_texto(im, sub, BRANCO)
    im = apagar(im, sub, BRANCO, 3, 6)
    tam = tam_por_largura(lambda t: [('com a Metodologia ARTI', SERIF_TXT, t, cor)], 438 - 87)
    b1 = base_de(SERIF_TXT, tam, 'Um Guia Completo', 415)
    b2 = base_de(SERIF_TXT, tam, 'com a Metodologia ARTI', 453)
    linha(im, [('Una guía completa', SERIF_TXT, tam, cor)], b1, 88)
    linha(im, [('con la metodología ARTI', SERIF_TXT, tam, cor)], b2, 87)

    # 'O QUE VOCÊ VAI RECEBER' -> 'LO QUE RECIBIRÁ' (caixa alta espaçada, dourado)
    cx = (80, 522, 520, 560)
    grad = grad_rel(im0, (80, 532, 500, 557), OURO)
    im = apagar(im, cx, OURO, 3, 6)
    tam = tam_por_cap(SERIF_CAPS, 552 - 532)
    pt = 'O QUE VOCÊ VAI RECEBER'
    f = F(SERIF_CAPS, tam)
    tr = ((497 - 88) - (f.getlength(pt) - f.getbbox(pt[0], anchor='ls')[0] - (f.getlength(pt[-1]) - f.getbbox(pt[-1], anchor='ls')[2]))) / (len(pt) - 1)
    linha(im, [('LO QUE RECIBIRÁ', SERIF_CAPS, tam, ('grad', grad, 532, 552))], 552, 88, tr=tr)

    # preço: 'POR' fica; 'R$97' -> PRECOS['preco'] (moeda pequena + valor grande), cabe antes do livro
    grad_p = grad_rel(im0, (230, 566, 320, 632), OURO)
    im = apagar(im, (160, 562, 330, 640), OURO, 3, 6)
    moeda, valor = dividir_preco(PRECOS['preco'])
    t_moeda = tam_por_cap(SERIF_PRECO, 629 - 590, 'R')   # 'R$' original: cap ~39 px
    t_valor = tam_por_cap(SERIF_PRECO, 629 - 568, '9')
    x_max = 552  # o livro começa em ~571
    k = 1.0
    while True:
        segs = [(moeda + ' ', SERIF_PRECO, t_moeda * k, ('grad', grad_p, 568, 629)),
                (valor, SERIF_PRECO, t_valor * k, ('grad', grad_p, 568, 629))]
        if largura_segs(segs) <= x_max - 171 or k < 0.4:
            break
        k -= 0.01
    linha(im, segs, 629, 171)

    # lista (Tinos, branco, alinhada em x=187)
    cor = cor_texto(im, (180, 660, 440, 690), BRANCO)
    tam = tam_por_largura(lambda t: [('Técnica tridimensional', SERIF_TXT, t, cor)], 420 - 185)
    SOMBRA = (1, 2, 1.5, 0.55)
    itens = [  # (caixa para apagar, [(texto_pt, y_topo_pt, texto_es)])
        ((180, 662, 565, 726), [('Técnica tridimensional', 669, 'Técnica tridimensional'), ('passo a passo', 702, 'paso a paso')]),
        ((180, 752, 565, 812), [('Raciocínio clínico', 760, 'Razonamiento clínico'), ('estruturado', 788, 'estructurado')]),
        ((180, 843, 565, 908), [('Revisão científica', 851, 'Revisión científica'), ('com artigos', 883, 'con artículos')]),
        ((180, 933, 565, 993), [('Casos reais', 941, 'Casos reales'), ('comentados', 969, 'comentados')]),
        ((180, 1023, 565, 1118), [('Conteúdo clínico direto', 1031, 'Contenido clínico directo'),
                                  ('para aplicar já no', 1059, 'para aplicar desde el'),
                                  ('próximo paciente.', 1090, 'próximo paciente.')]),
    ]
    for caixa, linhas_ in itens:
        im = apagar(im, caixa, BRANCO, 3, 6)
        for pt, yt, es in linhas_:
            linha(im, [(es, SERIF_TXT, tam, cor)], base_de(SERIF_TXT, tam, pt, yt), 187, peso=0.25, sombra=SOMBRA)

    im, info, ac = selo(im)

    # CTA: 'TOQUE EM SAIBA MAIS' / 'E GARANTA O SEU EBOOK.'
    branco = cor_texto(im, (220, 1185, 460, 1222), BRANCO)
    grad_c = grad_rel(im0, (520, 1185, 745, 1216), OURO)
    im = apagar(im, (215, 1178, 785, 1226), lambda r, g, b: BRANCO(r, g, b) | ((r > 120) & (r - b > 40)), 3, 6)
    branco2 = cor_texto(im0, (220, 1234, 735, 1260), BRANCO)
    im = apagar(im, (215, 1229, 785, 1265), BRANCO, 3, 6)
    t1 = tam_por_cap(SERIF_CAPS, 1215 - 1185, 'T')
    pt1 = 'TOQUE EM SAIBA MAIS'
    tr1 = ((742 - 224) - largura_segs([(pt1, SERIF_CAPS, t1, branco)])) / (len(pt1) - 1)
    seg1 = lambda t: [('TOQUE EN ', SERIF_CAPS, t, branco), ('MÁS INFORMACIÓN', SERIF_CAPS, t, ('grad', grad_c, 1185, 1215))]
    x_lim0, x_lim1 = 140, 775
    t1b = caber(seg1, t1, x_lim1 - x_lim0, 0.15, tr1)
    w1 = largura_segs(seg1(t1b), tr1)
    centro = (224 + 742) / 2
    x0 = max(x_lim0, min(centro - w1 / 2, x_lim1 - w1))
    k = t1b / t1
    base1 = 1215
    linha(im, seg1(t1b), base1, x0, tr=tr1)
    t2 = tam_por_cap(SERIF_CAPS, 1257 - 1236, 'E') * k
    pt2 = 'E GARANTA O SEU EBOOK.'
    tr2 = ((730 - 227) - largura_segs([(pt2, SERIF_CAPS, t2 / k, branco2)])) / (len(pt2) - 1) * k
    linha(im, [('Y ASEGURE SU EBOOK.', SERIF_CAPS, t2, branco2)], 1257, x0 + 2, tr=tr2)

    p = salvar(im, SAIDA_NOME)
    previa(im, 'trabalho/ads14-es-prev.jpg', 1080)
    print('ok', p, im.size, 'selo', info, 'acento', ac, 'reducao CTA %.0f%%' % ((1 - k) * 100))


if __name__ == '__main__':
    gerar()
