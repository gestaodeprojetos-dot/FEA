#!/usr/bin/env python3
"""[FEED] ADS 08.jpg e [STORIES] ADS 08.jpg (Ebook Olheiras) em espanhol LATAM.

Originais em trabalho/Fads08-feed.jpg e trabalho/Fads08-story.jpg
(Drive 18LE9PfKT5oLwlqV3OA4lYkYzxU6wxvRf e 16rACtcIVWMDw4tCrI9Dk3Dgi5gOD6VOK).

ATENÇÃO: no Drive, o [FEED] ADS 08.jpg NÃO é a versão feed do [STORIES] ADS 08.jpg. O feed é a
arte do Dr. João com 'DE R$ 200 POR R$ 97,00' (mesma copy do 'Ads 08 (Feed e Story, png)' do doc),
então o feed usa essa copy oficial e o story usa a copy '[FEED] ADS 08 e [STORIES] ADS 08 (jpg)'.

Story: prints de depoimento ficam em português (regra 4) com legenda ES abaixo do CTA; o tablet
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


def story():
    im = abrir('trabalho/Fads08-story.jpg')
    print('selo', selo_es(im, 1076, 304, 75, 82, (1032, 310, 1038, 313), ang_fixo=(-140, -22)))
    ouro = cor_texto(im, (50, 269, 434, 316), lambda r, g, b: (r > 150) & (b < 150) & (r - b > 50))
    branco = cor_texto(im, (50, 410, 536, 435), CLARO_TX)
    t_tit = tamanho_por_largura('referência em olheiras.', SR, 573 - 50 + 1)
    t_sub = tamanho_por_largura('Com a Técnica Tridimensional de', NR, 536 - 50 + 1)
    t_ebk = tamanho_por_largura('Tridimensional de Olheiras:', NR, 506 - 48 + 1)
    pt = [(269, 'De insegura para', SR, t_tit), (333, 'referência em olheiras.', SR, t_tit),
          (410, 'Com a Técnica Tridimensional de', NR, t_sub), (455, 'Preenchimento de Olheiras.', NR, t_sub),
          (530, 'Ebook Preenchimento', NR, t_ebk), (579, 'Tridimensional de Olheiras:', NR, t_ebk),
          (628, 'Um Guia Completo com a', NR, t_ebk), (677, 'Metodologia ARTI', NR, t_ebk)]
    es = ['De insegura a', 'referente en ojeras.',
          'Con la técnica tridimensional de', 'relleno de ojeras.',
          'Ebook Relleno', 'tridimensional de ojeras:', 'una guía completa con la', 'metodología ARTI']
    bases = [base_de(y, t, n, tam) for y, t, n, tam in pt]
    im.paste(apagar(im, (30, 255, 592, 725), CLARO_TX, 3))
    for (y, t, n, tam), e, b in zip(pt, es, bases):
        cor = ouro if n == SR else branco
        x = 50 - F(n, tam).getbbox(t[0], anchor='ls')[0] + F(n, tam).getbbox(e[0], anchor='ls')[0]
        desenhar(im, [(e, n, cor, False)], tam, b, x, alinh='esquerda')
        assert 50 + larg(e, n, tam) < 595, e
    print('titulo', t_tit, 'sub', t_sub, 'ebook', t_ebk)
    # CTA (caixa menta chapada; alarga para os lados sobre o fundo verde)
    pt_c = [('TOQUE EM SAIBA MAIS E GARANTA O SEU', NB, 0, False)]
    es_c = [('TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO', NB, 0, False)]
    print('cta', faixa(im, (241, 1366, 839, 1436), (pt_c, 1.5), es_c, 1395, 277, 802))
    # legendas dos depoimentos (regra 4), uma sob cada print, no verde livre abaixo do CTA
    y = 1466
    legenda_depoimento(im, 'Comparto este caso de ojeras + labios siguiendo las enseñanzas del profesor. Muy feliz con el resultado.',
                       336, 712, y, tamanho=20)
    legenda_depoimento(im, 'Solo quería mostrarle el relleno de ojeras que acabo de realizar en mi consultorio.',
                       742, 1068, y, tamanho=20)
    print(salvar(im, 'FEA-[STORIES] ADS 08 - LATAM.jpg'))


if __name__ == '__main__':
    story()
