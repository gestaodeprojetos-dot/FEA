#!/usr/bin/env python3
"""FEA · Ads 04 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Cinco caixas chapadas sobre foto (preta, cinza-clara, cinza-clara, preta, CTA vermelha),
serifada EB Garamond. Caixa sobre foto só cresce. A sinalização "#INJETORES ELITE"
desfocada no fundo da foto (nome de evento, parte da fotografia) não é texto da arte
e fica como está. Rodar a partir de fea_artes/: python3 criativos/ads04.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads01a04 import *  # noqa

SERIF = fonte('EBGaramond_400Regular')
CLARO_TXT = lambda r, g, b: (r > 130) & (g > 130) & (b > 130)
ESCURO_TXT = lambda r, g, b: (r < 140) & (g < 140) & (b < 140)
BRANCO_TXT = lambda r, g, b: (r > 200) & (g > 170) & (b > 170)

ES = dict(
    b1='Hoy, saber rellenar esta región es lo que distingue a los inyectores en todo el mundo.',
    b2='Es una oportunidad única para mejorar sus resultados de manera eficaz y segura.',
    b3='Ebook: Relleno tridimensional de ojeras: una guía completa con la metodología ARTI',
    b4=('Esta guía muestra cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e Intercurrencias) '
        'en el relleno de ojeras, la región más delicada del rostro, para obtener resultados superiores '
        'donde la mayoría falla.'),
    cta='Toque en “Más información” y obtenga su acceso.')

B4_PT = ['Este guia revela como aplicar a metodologia', 'ARTI — Anatomia, Reologia, Técnica e',
         'Intercorrências — no preenchimento de olheiras,', 'a região mais delicada da face, conquistando',
         'resultados superiores onde a maioria falha.']
CTA_PT = ['Toque em “Saiba mais” e libere o seu acesso!']

FEED = dict(
    b1=((201, 483, 868, 601), ['Hoje, saber fazer o preenchimento dessa região é',
                               'algo que diferencia a maior parte dos injetores de',
                               'todo o mundo, não somente do Brasil.'], CLARO_TXT),
    b2=((155, 611, 901, 694), ['Esta é uma oportunidade imperdível, onde você irá',
                               'melhorar os seus resultados de maneira efetiva e segura.'], ESCURO_TXT),
    b3=((190, 723, 881, 805), ['eBook: Preenchimento Tridimensional de Olheiras:',
                               'Um Guia Completo com a Metodologia ARTI'], ESCURO_TXT),
    b4=((266, 825, 797, 976), B4_PT, CLARO_TXT),
    cta=((291, 987, 782, 1028), CTA_PT, BRANCO_TXT))
STORY = dict(
    b1=((147, 774, 927, 1019), ['Hoje, saber fazer o preenchimento', 'dessa região é algo que diferencia a',
                                'maior parte dos injetores de todo o', 'mundo, não somente do Brasil.'], CLARO_TXT),
    b2=((114, 1040, 950, 1229), ['Esta é uma oportunidade imperdível,', 'onde você irá melhorar os seus',
                                 'resultados de maneira efetiva e segura.'], ESCURO_TXT),
    b3=((114, 1262, 951, 1451), ['eBook: Preenchimento Tridimensional', 'de Olheiras: Um Guia Completo',
                                 'com a Metodologia ARTI'], ESCURO_TXT),
    b4=((114, 1483, 950, 1720), B4_PT, CLARO_TXT),
    cta=((154, 1738, 926, 1803), CTA_PT, BRANCO_TXT))


def ads04(origem, saida, L, passo_b4):
    im = abrir(origem)
    print(saida)
    for k in ['b1', 'b2', 'b3', 'b4']:
        caixa, pt, cond = L[k]
        # b4: entrelinha um pouco maior, senão o 'g' de "guía" encosta no "A" de ARTI e parece acento
        paragrafo(im, caixa, pt, ES[k], SERIF, cond, fator_larg=1.06, verbose='  ' + k,
                  passo_fator=passo_b4 if k == 'b4' else 1.0)
    caixa, pt, cond = L['cta']
    paragrafo(im, caixa, pt, None, SERIF, cond, linhas_es=[ES['cta']], fator_larg=1.06, verbose='  cta')
    return salvar(im, saida)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ads04('trabalho/ads04-feed.png', 'FEA-Ads 04 - PTO-LATAM - Feed.png', FEED, 1.10)
    ads04('trabalho/ads04-story.png', 'FEA-Ads 04 - PTO-LATAM - Story.png', STORY, 1.06)
