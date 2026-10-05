#!/usr/bin/env python3
"""[FEED] ADS 08.jpg e [STORIES] ADS 08.jpg (Ebook Olheiras) em espanhol LATAM.

Originais em trabalho/Fads08-feed.jpg e trabalho/Fads08-story.jpg
(Drive 18LE9PfKT5oLwlqV3OA4lYkYzxU6wxvRf e 16rACtcIVWMDw4tCrI9Dk3Dgi5gOD6VOK).

Feed e story têm o mesmo conteúdo (o feed é mais compacto).

Prints de depoimento ficam em português (regra 4) com legenda ES abaixo do CTA, uma sob cada print; o tablet
laranja 'Metodologia ARTI no Preenchimento de Olheiras' (página do ebook), a capa do livro e a
página do tablet são mockup PT (regra 5, fase 2). Selo: 'MÉTODO EXCLUSIVO DEL' + COPIAS.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads08.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg06a09 import *  # noqa
from fea_arte_lib import abrir, salvar, apagar, cor_texto, cor_fundo, preencher, PRECOS

SR = 'NotoSerif_400Regular'
NR, NI, NB = 'NotoSans_400Regular', 'NotoSans_400Regular_Italic', 'NotoSans_700Bold'
CLARO_TX = lambda r, g, b: (r + g + b) > 420


def recompor(orig, saida, P):
    im = abrir(orig)
    print(saida, 'selo', selo_es(im, *P['selo'], ang_fixo=(-140, -22), ajuste_ang=-3))
    L = P['linhas']
    ouro = cor_texto(im, (50, L[0], 434, L[0] + 47), lambda r, g, b: (r > 150) & (b < 150) & (r - b > 50))
    branco = cor_texto(im, (50, L[2], 536, L[2] + 25), CLARO_TX)
    t_tit = tamanho_por_largura('referência em olheiras.', SR, 573 - 50 + 1)
    t_sub = tamanho_por_largura('Com a Técnica Tridimensional de', NR, 536 - 50 + 1)
    t_ebk = tamanho_por_largura('Tridimensional de Olheiras:', NR, 506 - 48 + 1)
    pt = [('De insegura para', SR, t_tit), ('referência em olheiras.', SR, t_tit),
          ('Com a Técnica Tridimensional de', NR, t_sub), ('Preenchimento de Olheiras.', NR, t_sub),
          ('Ebook Preenchimento', NR, t_ebk), ('Tridimensional de Olheiras:', NR, t_ebk),
          ('Um Guia Completo com a', NR, t_ebk), ('Metodologia ARTI', NR, t_ebk)]
    es = ['De insegura a', 'referente en ojeras.',
          'Con la técnica tridimensional de', 'relleno de ojeras.',
          'Ebook Relleno', 'tridimensional de ojeras:', 'una guía completa con la', 'metodología ARTI']
    bases = [base_de(y, t, n, tam) for y, (t, n, tam) in zip(L, pt)]
    im.paste(apagar(im, (30, L[0] - 14, 592, L[-1] + 48), CLARO_TX, 3))
    for (t, n, tam), e, b in zip(pt, es, bases):
        cor = ouro if n == SR else branco
        x = 50 - F(n, tam).getbbox(t[0], anchor='ls')[0] + F(n, tam).getbbox(e[0], anchor='ls')[0]
        desenhar(im, [(e, n, cor, False)], tam, b, x, alinh='esquerda')
        assert 50 + larg(e, n, tam) < 595, e
    print('  titulo', t_tit, 'sub', t_sub, 'ebook', t_ebk)
    # CTA (caixa menta chapada; alarga para os lados sobre o fundo verde)
    pt_c = [('TOQUE EM SAIBA MAIS E GARANTA O SEU', NB, 0, False)]
    es_c = [('TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO', NB, 0, False)]
    y0 = P['cta_y']
    print('  cta', faixa(im, (241, y0, 839, y0 + P['cta_alt']), (pt_c, 1.5), es_c, y0 + 29, 277, 802, reduzir_antes=P['cta_reduzir']))
    # legendas dos depoimentos (regra 4), uma sob cada print, no verde livre abaixo do CTA
    kw = P['legenda']
    y = y0 + P['cta_alt'] + kw.pop('folga')
    legenda_depoimento(im, 'Comparto este caso de ojeras + labios siguiendo las enseñanzas del profesor. Muy feliz con el resultado.',
                       *P['col1'], y, **kw)
    legenda_depoimento(im, 'Solo quería mostrarle el relleno de ojeras que acabo de realizar en mi consultorio.',
                       *P['col2'], y, **kw)
    print(salvar(im, saida))


FEED = dict(selo=(1022, 261, 60, 65, (986, 272, 993, 276)),
            linhas=[216, 280, 357, 402, 493, 542, 591, 640], cta_y=1196, cta_alt=71, cta_reduzir=True,
            col1=(324, 724), col2=(744, 1070), legenda=dict(folga=8, tamanho=15.5, continuo=True, entrelinha=1.3))
STORY = dict(selo=(1076, 304, 75, 82, (1032, 310, 1038, 313)),
             linhas=[269, 333, 410, 455, 530, 579, 628, 677], cta_y=1366, cta_alt=70, cta_reduzir=False,
             col1=(336, 712), col2=(742, 1068), legenda=dict(folga=30, tamanho=20))


if __name__ == '__main__':
    recompor('trabalho/Fads08-feed.jpg', 'FEA-[FEED] ADS 08 - LATAM.jpg', FEED)
    recompor('trabalho/Fads08-story.jpg', 'FEA-[STORIES] ADS 08 - LATAM.jpg', STORY)
