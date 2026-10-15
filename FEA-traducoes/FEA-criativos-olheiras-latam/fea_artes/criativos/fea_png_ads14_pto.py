#!/usr/bin/env python3
"""Ads 14 (Feed e Story) em espanhol. Rodar a partir de fea_artes/: python3 criativos/fea_png_ads14_pto.py
Originais em trabalho/pto14-feed.png e trabalho/pto14-story.png (Drive Brasil).
Capa do ebook no mockup fica em português (fase 2)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_layout_livro_preto import *

TIT_ES = [('¿Le da miedo realizar el procedimiento más desafiante de la armonización facial:', 'Y'), (' el relleno de ojeras?', 'W')]
CORPO_ES = [('Esta guía se creó precisamente para evitarlo: domine el procedimiento más desafiante de la armonización facial '
             'con la metodología ARTI y logre resultados naturales, seguros y duraderos.', 'W')]
CTA_PT = [[('Toque em ', REG, 0, 0), ('SAIBA MAIS', BOLD, 0, 0)], [('e garanta o seu!', REG, 0, 0)]]
CTA_ES = [[('Toque en ', REG, 'W'), ('MÁS INFORMACIÓN', BOLD, 'Y')], [('y asegure el suyo.', REG, 'W')]]

FEED = dict(
    origem='trabalho/pto14-feed.png', saida='FEA-Ads 14 - PTO-LATAM - Feed.png',
    x_col=63, x_dir=645, x_lim=692, livro_esq=((696, 220), (668, 886)),
    cor_branco_tit=(60, 414, 610, 452), cor_amarelo=(60, 265, 510, 296), cor_corpo=(60, 508, 610, 534),
    logo=dict(tops=[116, 145, 175], xs=[(66, 327), (68, 325), (98, 297)], sublinhado=212),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['Tem medo de realizar o', 'procedimento mais desafiador', 'da harmonização facial: o', 'preenchimento de olheiras?'],
             tops=[265, 315, 363, 414], xs=[(62, 505), (64, 664), (63, 548), (64, 605)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=CORPO_ES,
             pt=['Este guia foi criado justamente para evitar', 'isso: Domine o procedimento mais',
                 'desafiador da harmonização facial — com a', 'metodologia ARTI — e alcance resultados', 'naturais, seguros e duradouros.'],
             tops=[508, 544, 580, 616, 652], xs=[(64, 605), (62, 517), (62, 620), (64, 599), (64, 468)]),
    ],
    preco=dict(caixa=(0, 720, 503, 872), estilo='cinza', so_hoje=False,
               tops=[745, 799], xs=[(66, 332), (66, 444)], x_max_esticar=645, folga_dir=45, x_corte=300),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[905, 941], xs=[(62, 360), (62, 262)]),
)

STORY = dict(
    origem='trabalho/pto14-story.png', saida='FEA-Ads 14 - PTO-LATAM - Story.png',
    x_col=86, x_dir=590, x_lim=660, livro_esq=((657, 572), (625, 1341)),
    cor_branco_tit=(80, 784, 570, 880), cor_amarelo=(80, 545, 590, 582), cor_corpo=(80, 940, 570, 971),
    logo=dict(tops=[365, 401, 437], xs=[(90, 404), (92, 401), (129, 367)], sublinhado=481),
    fluxo=[
        dict(tipo='titulo', fonte=BOLD, track=TRACK_TIT, es=TIT_ES,
             pt=['Tem medo de realizar', 'o procedimento mais', 'desafiador da', 'harmonização facial:', 'o preenchimento de', 'olheiras?'],
             tops=[545, 605, 664, 722, 784, 843], xs=[(85, 578), (86, 584), (86, 404), (88, 561), (86, 558), (86, 295)]),
        dict(tipo='corpo', fonte=REG, track=TRACK_CORPO, es=CORPO_ES,
             pt=['Este guia foi criado justamente', 'para evitar isso: Domine o', 'procedimento mais desafiador',
                 'da harmonização facial — com a', 'metodologia ARTI — e alcance', 'resultados naturais, seguros e', 'duradouros.'],
             tops=[940, 984, 1027, 1069, 1114, 1157, 1200],
             xs=[(88, 565), (87, 485), (87, 570), (86, 578), (87, 557), (87, 548), (86, 273)]),
    ],
    preco=dict(caixa=(0, 1268, 615, 1450), estilo='cinza', so_hoje=False,
               tops=[1298, 1364], xs=[(90, 409), (90, 538)], x_max_esticar=615, folga_dir=30, x_corte=330),
    cta=dict(pt=CTA_PT, es=CTA_ES, tops=[1503, 1547], xs=[(85, 443), (86, 325)]),
)

if __name__ == '__main__':
    for sp in (FEED, STORY):
        _, rel = compor(sp)
        print(sp['saida'], rel)
