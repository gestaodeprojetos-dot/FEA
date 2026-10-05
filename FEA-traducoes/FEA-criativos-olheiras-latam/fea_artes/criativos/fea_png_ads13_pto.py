#!/usr/bin/env python3
"""Ads 13 (Feed e Story) em espanhol. Rodar a partir de fea_artes/: python3 criativos/fea_png_ads13_pto.py
Originais em trabalho/pto13-feed.png e trabalho/pto13-story.png (Drive Brasil).
Capa do ebook no mockup fica em português (fase 2)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_layout_livro_preto import *

TIT_ES = [('EL PASO A PASO', 'Y'), (' para que los inyectores dominen el relleno tridimensional de ojeras, incluso si empiezan desde cero.', 'W')]
CORPO_ES = [('Esta guía muestra cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e Intercurrencias) en el relleno '
             'de ojeras, la región más delicada del rostro, para obtener resultados superiores donde la mayoría falla.', 'W')]
CTA_PT = [[('CLIQUE E GARANTA', REG, 0, 0)], [('O SEU DESCONTO', REG, 0, 0)]]
CTA_ES = [[('HAGA CLIC Y ASEGURE', REG, 'W')], [('SU DESCUENTO', REG, 'W')]]
COR_TXT_CAIXA = (24, 22, 20)

FEED = dict(
    origem='trabalho/pto13-feed.png', saida='FEA-Ads 13 - PTO-LATAM - Feed.png',
    x_col=76, x_dir=640, x_lim=655,
    cor_branco_tit=(70, 290, 470, 325), cor_amarelo=(70, 245, 400, 280), cor_corpo=(70, 489, 560, 545),
    logo=dict(tops=[116, 143, 169], xs=[(79, 313), (80, 311), (107, 286)], sublinhado=202),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['O PASSO A PASSO para', 'Injetores dominarem o', 'preenchimento tridimensional', 'de olheiras, mesmo', 'começando do zero!'],
             tops=[245, 290, 335, 380, 425], xs=[(76, 483), (77, 472), (77, 608), (75, 413), (75, 430)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=CORPO_ES,
             pt=['Este guia revela como aplicar a', 'metodologia ARTI — Anatomia, Reologia,', 'Técnica e Intercorrências — no',
                 'preenchimento de olheiras, a região mais', 'delicada da face, conquistando resultados', 'superiores onde a maioria falha.'],
             tops=[489, 522, 552, 587, 619, 652], xs=[(77, 430), (76, 553), (75, 430), (76, 555), (75, 570), (75, 443)]),
    ],
    preco=dict(caixa=(0, 708, 457, 872), estilo='amarelo', cor_txt=COR_TXT_CAIXA, so_hoje=True,
               tops=[724, 770, 814], xs=[(78, 317), (78, 438), (75, 234)], x_max_esticar=640, folga_dir=19, x_corte=300),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[911, 944], xs=[(75, 314), (75, 299)]),
)

STORY = dict(
    origem='trabalho/pto13-story.png', saida='FEA-Ads 13 - PTO-LATAM - Story.png',
    x_col=70, x_dir=585, x_lim=592,
    cor_branco_tit=(70, 589, 540, 630), cor_amarelo=(68, 537, 420, 577), cor_corpo=(70, 873, 490, 938),
    logo=dict(tops=[368, 399, 431], xs=[(73, 348), (74, 345), (106, 315)], sublinhado=469),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['O PASSO A PASSO para', 'Injetores dominarem o', 'preenchimento', 'tridimensional de', 'olheiras, mesmo', 'começando do zero!'],
             tops=[537, 589, 641, 693, 746, 799], xs=[(69, 546), (71, 533), (70, 387), (67, 428), (69, 404), (69, 484)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=CORPO_ES,
             pt=['Este guia revela como aplicar a', 'metodologia ARTI — Anatomia,', 'Reologia, Técnica e', 'Intercorrências — no',
                 'preenchimento de olheiras, a', 'região mais delicada da face,', 'conquistando resultados', 'superiores onde a maioria falha.'],
             tops=[873, 911, 947, 985, 1025, 1063, 1101, 1139],
             xs=[(70, 484), (70, 494), (70, 329), (70, 350), (70, 464), (70, 460), (69, 412), (69, 500)]),
    ],
    preco=dict(caixa=(0, 1202, 516, 1394), estilo='amarelo', cor_txt=COR_TXT_CAIXA, so_hoje=True,
               tops=[1221, 1277, 1326], xs=[(72, 352), (72, 496), (68, 256)], x_max_esticar=565, folga_dir=20, x_corte=330),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[1443, 1481], xs=[(69, 348), (69, 330)]),
)

if __name__ == '__main__':
    for sp in (FEED, STORY):
        _, rel = compor(sp)
        print(sp['saida'], rel)
