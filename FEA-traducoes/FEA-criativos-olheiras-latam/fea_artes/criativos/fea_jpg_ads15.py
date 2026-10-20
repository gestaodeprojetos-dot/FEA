#!/usr/bin/env python3
"""[FEED] ADS 15 (jpg) em espanhol LATAM. Troca só a copy; livro (mockup, fase 2), fundo e layout intactos.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads15.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

ORIG = 'trabalho/ads15-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 15 - LATAM.jpg'

VERDE = lambda r, g, b: (g > r + 12) & (r < 150) & (g < 175)
VERDE_APAGAR = lambda r, g, b: ((r + g + b) < 640) & (g >= r)  # inclui a borda clara das letras e acentos
OURO = lambda r, g, b: (r > 150) & (r - b > 45) & (g < 215) & (g > 110)
SERIF_TXT = 'Tinos_400Regular'
SERIF_CAPS = 'NotoSerif_600SemiBold'
SERIF_CTA = 'NotoSerif_700Bold'
SERIF_PRECO = 'PlayfairDisplay_600SemiBold'


def titulo(im0):
    limpo = apagar(im0, (60, 146, 880, 228), VERDE, 3, 6)
    limpo = apagar(limpo, (278, 330, 660, 412), VERDE, 3, 6)  # 'LHEIRAS' (DE O fica)
    im = limpo.copy()
    L1, L3 = (146, 228), (330, 412)
    g = {'R': (130, 182, L1), 'E': (188, 235, L1), 'E2': (244, 290, L1), 'N': (299, 354, L1), 'O': (762, 818, L1),
         'L': (282, 327, L3), 'E3': (400, 446, L3), 'R3': (483, 534, L3), 'A': (537, 593, L3), 'S': (599, 637, L3)}
    colocar(im, im0, limpo, g, ['R', 'E', 'L', 'L', 'E2', 'N', 'O'], 78, L1[0], [6, 8, 7, 8, 9, 8, 0])
    grad = grad_rel(im0, (395, 339, 640, 404), VERDE)
    nome_j = 'Gelasio_500Medium'
    tam = tam_por_cap(nome_j, 403 - 339)
    _, x_fim = linha(im, [('J', nome_j, tam, ('grad', grad, 339, 403))], 403, 275 + 9, 'esquerda')
    colocar(im, im0, limpo, g, ['E3', 'R3', 'A', 'S'], int(round(x_fim)) + 8, L3[0], [8, 3, 6, 0])
    return im


def gerar():
    im0 = abrir(ORIG)
    im = titulo(im0)
    verde_txt = cor_texto(im0, (78, 475, 480, 514), VERDE)
    ouro_txt = cor_nucleo(im0, (334, 521, 422, 550), OURO, 40)

    # subtítulo: 'Um Guia Completo com' / 'a Metodologia ARTI' (ARTI dourado)
    im = apagar(im, (65, 466, 568, 516), VERDE_APAGAR, 3, 6)
    im = apagar(im, (65, 516, 440, 562), lambda r, g, b: VERDE_APAGAR(r, g, b) | OURO(r, g, b), 3, 6)
    tam = tam_por_largura(lambda t: [('Um Guia Completo com', SERIF_TXT, t, verde_txt)], 492 - 78)
    tam = tam_por_largura(lambda t: [('a Metodologia ', SERIF_TXT, t, verde_txt), ('ARTI', SERIF_TXT, t, ouro_txt)], 422 - 78)
    b1 = base_de(SERIF_TXT, tam, 'Um Guia Completo com', 475)
    b2 = base_de(SERIF_TXT, tam, 'a Metodologia', 520)
    linha(im, [('Una guía completa con', SERIF_TXT, tam, verde_txt)], b1, 78, peso=0.2)
    linha(im, [('la metodología ', SERIF_TXT, tam, verde_txt), ('ARTI', SERIF_TXT, tam, ouro_txt)], b2, 78, peso=0.2)

    # 'ESSE EBOOK É' / 'PRA VOCÊ QUE:' -> 'ESTE EBOOK ES' / 'PARA USTED SI:'
    cor_caps = cor_texto(im0, (100, 609, 350, 633), VERDE)
    im = apagar(im, (90, 598, 560, 680), VERDE_APAGAR, 3, 6)
    tam = tam_por_cap(SERIF_CAPS, 632 - 609)
    tr = track_para('PRA VOCÊ QUE:', SERIF_CAPS, tam, 374 - 101)
    linha(im, [('ESTE EBOOK ES', SERIF_CAPS, tam, cor_caps)], 632, 100, tr=tr)
    linha(im, [('PARA USTED SI:', SERIF_CAPS, tam, cor_caps)], 674, 101, tr=tr)

    # lista
    cor_l = cor_texto(im0, (200, 706, 432, 726), VERDE)
    tam = tam_por_largura(lambda t: [('Evita tratar olheiras', SERIF_TXT, t, cor_l)], 432 - 201)
    itens = [
        ((195, 698, 568, 770), [('Evita tratar olheiras', 706, 'Evita tratar ojeras'), ('por insegurança', 743, 'por inseguridad')]),
        ((195, 790, 568, 860), [('Já faz, mas sem', 797, 'Ya lo hace, pero sin'), ('previsibilidade', 828, 'previsibilidad')]),
        ((195, 879, 568, 944), [('Quer reduzir risco', 886, 'Quiere reducir riesgos'), ('e ter mais controle técnico', 917, 'y tener más control técnico')]),
        ((195, 970, 568, 1038), [('Tudo isso com método', 977, 'Todo esto con un método'), ('estruturado por apenas', 1007, 'estructurado por solo')]),
    ]
    for caixa, linhas_ in itens:
        im = apagar(im, caixa, VERDE_APAGAR, 3, 6)
        for pt, yt, es in linhas_:
            t = caber(lambda s: [(es, SERIF_TXT, s, cor_l)], tam, 566 - 200, 0.15)
            linha(im, [(es, SERIF_TXT, t, cor_l)], base_de(SERIF_TXT, tam, pt, yt), 200, peso=0.2)

    # preço dentro da caixa com borda dourada (164..428)
    cor_p = cor_texto(im0, (278, 1065, 382, 1138), VERDE)
    im = apagar(im, (190, 1058, 405, 1145), VERDE_APAGAR, 3, 6)
    moeda, valor = dividir_preco(PRECOS['preco'])
    t_m = tam_por_cap(SERIF_PRECO, 1134 - 1085, 'R')
    t_v = tam_por_cap(SERIF_PRECO, 1138 - 1065, '9')
    k = 1.0
    while True:
        segs = [(moeda + ' ', SERIF_PRECO, t_m * k, cor_p), (valor, SERIF_PRECO, t_v * k, cor_p)]
        if largura_segs(segs) <= (428 - 164) - 40 or k < 0.4:
            break
        k -= 0.01
    linha(im, segs, 1134 - (1 - k) * (1134 - 1101) * 0.5, (164 + 428) / 2, 'centro')

    # CTA
    cor_c = cor_texto(im0, (251, 1209, 502, 1248), VERDE)
    grad_c = grad_rel(im0, (525, 1209, 797, 1240), OURO)
    im = apagar(im, (240, 1200, 830, 1290), lambda r, g, b: VERDE_APAGAR(r, g, b) | OURO(r, g, b), 3, 6)
    t1 = tam_por_cap(SERIF_CTA, 1239 - 1209, 'T')
    tr1 = track_para('TOQUE EM SAIBA MAIS', SERIF_CTA, t1, 797 - 251)
    seg1 = lambda t: [('TOQUE EN ', SERIF_CTA, t, cor_c), ('MÁS INFORMACIÓN', SERIF_CTA, t, ('grad', grad_c, 1209, 1239))]
    LIM = 815 - 240  # entre o círculo da mão e o círculo da seta, com respiro
    t1b = caber(seg1, t1, LIM, 0.15, tr1)
    tr1b = tr1
    while largura_segs(seg1(t1b), tr1b) > LIM and tr1b > 0:
        tr1b -= 0.05
    k = t1b / t1
    cx = (240 + 815) / 2
    linha(im, seg1(t1b), 1239, cx, 'centro', tr=tr1b)
    t2 = tam_por_cap(SERIF_CTA, 1281 - 1259, 'E') * k
    tr2 = track_para('E GARANTA O SEU.', SERIF_CTA, t2 / k, 704 - 365) * k * (tr1b / tr1)
    linha(im, [('Y ASEGURE EL SUYO.', SERIF_CTA, t2, cor_c)], 1281, (365 + 704) / 2, 'centro', tr=tr2)

    p = salvar(im, SAIDA_NOME)
    print('ok', p, im.size, 'CTA reducao %.0f%% tracking %.2f->%.2f' % ((1 - k) * 100, tr1, tr1b), 'preco k %.2f' % k)


if __name__ == '__main__':
    gerar()
