#!/usr/bin/env python3
"""FEA · Ads 03 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Caixas chapadas sobre foto (preta, cinza-clara, vermelha de preço, CTA cinza-clara),
serifada EB Garamond. Caixa sobre foto só cresce (nunca encolhe, para não expor
área de foto que estava coberta). Rodar a partir de fea_artes/: python3 criativos/ads03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads01a04 import *  # noqa

SERIF = fonte('EBGaramond_400Regular')
NBSP = ' '
CLARO_TXT = lambda r, g, b: (r > 130) & (g > 130) & (b > 130)
ESCURO_TXT = lambda r, g, b: (r < 140) & (g < 140) & (b < 140)
BRANCO_TXT = lambda r, g, b: (r > 200) & (g > 170) & (b > 170)

TIT_ES = 'Aprenda el relleno tridimensional de ojeras'
PAR_ES = ('Esta guía muestra cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e Intercurrencias) '
          'en el relleno de ojeras, la región más delicada del rostro, para obtener resultados superiores '
          'donde la mayoría falla.')
PRECO_ES = ['De ' + PRECOS['de_200'], 'a solo ' + PRECOS['preco']]
CTA_PT = ['CLIQUE E GARANTA', 'O SEU DESCONTO']
CTA_ES = ['HAGA CLIC Y ASEGURE', 'SU DESCUENTO']

FEED = dict(
    tit=((240, 465, 843, 589), ['Aprenda o preenchimento', 'tridimensional de olheiras']),
    par=((106, 608, 960, 782), ['Este guia revela como aplicar a metodologia ARTI —',
                                'Anatomia, Reologia, Técnica e Intercorrências — no',
                                'preenchimento de olheiras, a região mais delicada da face,',
                                'conquistando resultados superiores onde a maioria falha.']),
    preco=((307, 801, 760, 925), ['De R$200,00', 'Por apenas R$ 97,00']),
    cta=((358, 943, 726, 1031), CTA_PT))
STORY = dict(
    tit=((143, 879, 942, 1043), ['Aprenda o preenchimento', 'tridimensional de olheiras']),
    par=((104, 1068, 987, 1398), ['Este guia revela como aplicar a metodologia',
                                  'ARTI — Anatomia, Reologia, Técnica e',
                                  'Intercorrências — no preenchimento de',
                                  'olheiras, a região mais delicada da face,',
                                  'conquistando resultados superiores onde a',
                                  'maioria falha.']),
    preco=((232, 1424, 833, 1588), ['De R$200,00', 'Por apenas R$ 97,00']),
    cta=((300, 1613, 787, 1729), CTA_PT))


def ads03(origem, saida, L, larg_lim):
    im = abrir(origem)
    print(saida)
    paragrafo(im, *L['tit'], TIT_ES, SERIF, CLARO_TXT, fator_larg=1.05, verbose='  titulo')
    paragrafo(im, *L['par'], PAR_ES, SERIF, ESCURO_TXT, larg_max=larg_lim, verbose='  paragrafo')
    paragrafo(im, *L['preco'], None, SERIF, BRANCO_TXT, linhas_es=PRECO_ES, larg_max=larg_lim, verbose='  preco')
    paragrafo(im, *L['cta'], None, SERIF, ESCURO_TXT, linhas_es=CTA_ES, larg_max=larg_lim, verbose='  cta')
    return salvar(im, saida)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ads03('trabalho/ads03-feed.png', 'FEA-Ads 03 - PTO-LATAM - Feed.png', FEED, 830)
    ads03('trabalho/ads03-story.png', 'FEA-Ads 03 - PTO-LATAM - Story.png', STORY, 840)
