#!/usr/bin/env python3
"""Ads 15 (Feed e Story) em espanhol. Rodar a partir de fea_artes/: python3 criativos/fea_png_ads15_pto.py
Originais em trabalho/pto15-feed.png e trabalho/pto15-story.png (Drive Brasil).
Capa do ebook no mockup fica em português (fase 2)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_layout_livro_preto import *

TIT_ES = [('Una oportunidad única para inyectores que quieren dominar el procedimiento más desafiante de la armonización facial', 'Y'),
          (' (el relleno de ojeras) y convertirse en referentes del mercado.', 'W')]
SUB_ES = [('Ebook: Relleno tridimensional de ojeras: una guía completa con la metodología ARTI + 3 casos clínicos exclusivos', 'W')]
CTA_PT = [[('Toque em ', REG, 0, 0), ('SAIBA MAIS', BOLD, 0, 0)], [('e garanta o seu!', REG, 0, 0)]]
CTA_ES = [[('Toque en ', REG, 'W'), ('MÁS INFORMACIÓN', BOLD, 'Y')], [('y asegure el suyo.', REG, 'W')]]

FEED = dict(
    origem='trabalho/pto15-feed.png', saida='FEA-Ads 15 - PTO-LATAM - Feed.png',
    x_col=74, x_dir=640, x_lim=652,
    cor_branco_tit=(70, 451, 500, 522), cor_amarelo=(70, 229, 510, 265), cor_corpo=(70, 568, 515, 586),
    logo=dict(tops=[104, 131, 157], xs=[(78, 308), (79, 305), (106, 281)], sublinhado=189),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['Oportunidade única para', 'injetores que desejam dominar', 'o procedimento mais', 'desafiador da harmonização',
                 'facial — o preenchimento de', 'olheiras — e se tornarem', 'referência no mercado.'],
             tops=[229, 275, 320, 363, 408, 451, 492], xs=[(75, 502), (74, 607), (74, 441), (74, 559), (74, 557), (74, 487), (76, 468)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=SUB_ES,
             pt=['eBook: Preenchimento Tridimensional', 'de Olheiras: Um Guia Completo com a', 'Metodologia ARTI + 03 Casos Clínicos', 'Exclusivos'],
             tops=[568, 598, 629, 663], xs=[(74, 510), (74, 511), (76, 510), (76, 191)]),
    ],
    preco=dict(caixa=(0, 710, 463, 872), estilo='cinza', so_hoje=True,
               tops=[732, 778, 820], xs=[(77, 311), (77, 421), (74, 230)], x_max_esticar=640, folga_dir=42, x_corte=300),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[917, 950], xs=[(74, 336), (74, 250)]),
)

STORY = dict(
    origem='trabalho/pto15-story.png', saida='FEA-Ads 15 - PTO-LATAM - Story.png',
    x_col=86, x_dir=590, x_lim=600,
    cor_branco_tit=(80, 911, 560, 1011), cor_amarelo=(80, 434, 560, 483), cor_corpo=(80, 1059, 450, 1084),
    logo=dict(tops=[245, 281, 317], xs=[(90, 404), (92, 401), (129, 367)], sublinhado=361),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['Oportunidade única', 'para injetores que', 'desejam dominar o', 'procedimento mais', 'desafiador da',
                 'harmonização facial', '— o preenchimento', 'de olheiras — e se', 'tornarem referência', 'no mercado.'],
             tops=[434, 495, 555, 616, 675, 733, 795, 854, 911, 975],
             xs=[(86, 556), (88, 505), (86, 533), (88, 544), (86, 404), (88, 548), (85, 539), (86, 491), (84, 547), (88, 375)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=SUB_ES,
             pt=['eBook: Preenchimento', 'Tridimensional de Olheiras: Um', 'Guia Completo com a', 'Metodologia ARTI + 03 Casos', 'Clínicos Exclusivos'],
             tops=[1059, 1102, 1145, 1189, 1230], xs=[(86, 441), (85, 570), (86, 425), (88, 544), (86, 380)]),
    ],
    preco=dict(caixa=(0, 1309, 615, 1530), estilo='cinza', so_hoje=True,
               tops=[1339, 1403, 1459], xs=[(90, 409), (90, 543), (85, 299)], x_max_esticar=615, folga_dir=30, x_corte=330),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[1578, 1622], xs=[(85, 443), (86, 325)]),
)

if __name__ == '__main__':
    for sp in (FEED, STORY):
        _, rel = compor(sp)
        print(sp['saida'], rel)
