#!/usr/bin/env python3
"""FEA · Ads 06 (Ebook Olheiras) em espanhol LATAM, Feed e Story.

Origem: parte Ads 06 de ../fea_recompor_ads06_ads09.py (copy ES já validada),
agora com o preço da caixa vermelha lido de precos.json (PRECOS['preco']).
Rodar a partir de fea_artes/:  python3 criativos/ads06.py
Originais em trabalho/pto06-feed.png e trabalho/pto06-story.png (Drive Brasil:
Ads 06 - PTO - Feed.png 18t2vaC7XPvtPpRrIBKmPbAHVLTWoY0i-,
Ads 06 - PTO - Story.png 1b2auyFzJLDKqNtY0jCJ1EV7NP8LbUHkX).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

ROBOTO_LIGHT = fonte('Roboto_300Light')
ROBOTO_REG = fonte('Roboto_400Regular')
ROBOTO_COND_BOLD = fonte('RobotoCondensed_700Bold')

CORPO_PT = ['É isso que te separa de', 'dominar o preenchimento', 'tridimensional de olheiras.']
CORPO_ES = ['Es lo que lo separa de', 'dominar el relleno', 'tridimensional de ojeras.']
CTA_PT = ['CLIQUE E GARANTA', 'O SEU DESCONTO']
CTA_ES = ['HAGA CLIC Y ASEGURE', 'SU DESCUENTO']
VERMELHO = lambda r, g, b: (r > 200) & (g < 60) & (b < 60)


def linhas(im, pt, es, medidas, caminho, cor):
    """Uma fonte só (calibrada na linha PT mais larga), linha de base de cada linha preservada."""
    i = max(range(len(medidas)), key=lambda k: medidas[k][2] - medidas[k][1])
    f = calibrar(caminho, pt[i], medidas[i][2] - medidas[i][1])
    for p, e, m in zip(pt, es, medidas):
        escrever(im, [p], [e], [m], caminho, cor, f=f)
    return f


def preco(im, caixa, med):
    """Caixa vermelha chapada: repinta, escreve PRECOS['preco'] em Roboto Regular branco,
    mesma linha de base do 'R$ 97,00' original, centralizado; alarga a caixa se precisar."""
    x0, y0, x1, y1 = caixa
    ytop, tx0, tx1 = med
    verm = cor_fundo(im, (x0 + 4, y0 + 4, x1 - 4, y0 + 12))
    preencher(im, caixa, verm)
    f = calibrar(ROBOTO_REG, 'R$ 97,00', tx1 - tx0)
    texto = PRECOS['preco']
    folga = min(tx0 - x0, x1 - tx1)
    largura_max = im.width - 2 * 40 - 2 * folga
    while f.getbbox(texto)[2] - f.getbbox(texto)[0] > largura_max and f.size > 0.85 * calibrar(ROBOTO_REG, 'R$ 97,00', tx1 - tx0).size:
        f = ImageFont.truetype(ROBOTO_REG, f.size - 0.5)
    l, _, r, _ = f.getbbox(texto)
    nova = alargar_caixa(im, caixa, verm, r - l, folga)
    # linha de base do original: topo medido do 'R$ 97,00' menos o topo do glifo na fonte
    y = ytop - f.getbbox('R$ 97,00')[1]
    # colchetes/descendentes do placeholder não podem vazar da caixa: se vazar, cresce a caixa na vertical
    t, b = y + f.getbbox(texto)[1], y + f.getbbox(texto)[3]
    margem = 8
    if t < nova[1] + margem or b > nova[3] - margem:
        cresce = int(max(nova[1] + margem - t, b - (nova[3] - margem), 0)) + 1
        nova = (nova[0], nova[1] - cresce, nova[2], nova[3] + cresce)
        preencher(im, nova, verm)
    cx = (nova[0] + nova[2]) / 2
    ImageDraw.Draw(im).text((cx - (r - l) / 2 - l, y), texto, font=f, fill=(255, 255, 255))
    return nova


def ads06(nome, caixa_preco, med_preco, corpo, cta_caixa, cta_med):
    im = abrir(nome)
    preco(im, caixa_preco, med_preco)
    # corpo sobre a foto (Roboto Light claro): inpainting só nos pixels de texto
    caixa = (min(m[1] for m in corpo) - 12, corpo[0][0] - 8, max(m[2] for m in corpo) + 12, corpo[-1][0] + 70)
    caixa = (caixa[0], caixa[1], caixa[2], min(caixa[3], cta_caixa[1] - 4))
    cor = cor_texto(im, caixa, CLARO)
    im = apagar(im, caixa, CLARO, 3)
    linhas(im, CORPO_PT, CORPO_ES, corpo, ROBOTO_LIGHT, cor)
    # CTA verde chapado
    verde = cor_fundo(im, (cta_caixa[0] + 3, cta_caixa[1] + 3, cta_caixa[2] - 3, cta_caixa[1] + 8))
    preencher(im, cta_caixa, verde)
    f = calibrar(ROBOTO_COND_BOLD, CTA_PT[0], cta_med[0][2] - cta_med[0][1])
    l, _, r, _ = f.getbbox(CTA_ES[0])
    alargar_caixa(im, cta_caixa, verde, r - l, cta_med[0][1] - cta_caixa[0])
    linhas(im, CTA_PT, CTA_ES, cta_med, ROBOTO_COND_BOLD, (255, 255, 255))
    return im


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    feed = ads06('trabalho/pto06-feed.png', (314, 537, 759, 667), (556, 337, 734),
                 [(716, 329, 744), (771, 302, 769), (819, 298, 770)],
                 (346, 903, 727, 1006), [(920, 361, 712), (965, 378, 694)])
    story = ads06('trabalho/pto06-story.png', (254, 1071, 819, 1236), (1093, 300, 788),
                  [(1300, 273, 800), (1369, 240, 832), (1430, 233, 834)],
                  (295, 1537, 778, 1668), [(1558, 314, 760), (1615, 335, 737)])
    for im, n in [(feed, 'FEA-Ads 06 - PTO-LATAM - Feed.png'), (story, 'FEA-Ads 06 - PTO-LATAM - Story.png')]:
        print('ok', salvar(im, n), im.size)
        previa(im, 'trabalho/pto06-es-' + ('feed' if 'Feed' in n else 'story') + '-prev.jpg')
