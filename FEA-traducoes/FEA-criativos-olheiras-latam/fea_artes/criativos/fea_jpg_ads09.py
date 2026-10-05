#!/usr/bin/env python3
"""[FEED] ADS 09.jpg e [STORIES] ADS 09.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Originais em trabalho/Fads09-feed.jpg e trabalho/Fads09-story.jpg
(Drive 1mq0kkwI4zhri5MpiHP9j47lFiaLgGYGy e 1seLOpLEPvt8h6xMT0m_4vRhG5xjdk_r-).
Fontes: Noto Serif Regular/Italic (título), Noto Sans Regular (corpo), Noto Sans Bold (CTA).
Story = feed deslocado 93 px para baixo no texto; CTA em pílula dourada.
Mockup (capa PT e página do tablet com texto gerado por IA) intacto: fase 2.
Selo: 'MÉTODO EXCLUSIVO DEL' + COPIAS.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads09.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg06a09 import *  # noqa
from fea_arte_lib import abrir, salvar, apagar, cor_texto, cor_fundo

SR, SI = 'NotoSerif_400Regular', 'NotoSerif_400Regular_Italic'
NR, NB = 'NotoSans_400Regular', 'NotoSans_700Bold'
TXT = lambda r, g, b: ((r + g + b) < 560) | ((r - b > 45) & (r < 236))   # verde-escuro e dourado sobre o creme
ESC = lambda r, g, b: (r + g + b) < 330


def recompor(orig, saida, dy, selo, cta):
    im = abrir(orig)
    print(saida, 'selo', selo_es(im, *selo))
    verde = cor_texto(im, (231, 188 + dy, 793, 244 + dy), lambda r, g, b: (r + g + b) < 450)
    ouro = cor_texto(im, (369, 255 + dy, 874, 300 + dy), lambda r, g, b: (r - b > 60) & (r > 120) & (r < 235))
    t_t = tamanho_por_largura('Não é sobre preencher. É', SR, 793 - 231 + 1)
    t_i = tamanho_por_largura('comprometem o resultado.', SI, 822 - 231 + 1)
    t_c = tamanho_por_largura('Ebook com erros mais frequentes e', NR, 758 - 232 + 1)
    b = [base_de(188 + dy, 'Não é sobre preencher. É', SR, t_t), base_de(255 + dy, 'sobre saber onde NÃO tocar.', SR, t_t),
         base_de(346 + dy, 'Evite erros comuns que', SI, t_i), base_de(411 + dy, 'comprometem o resultado.', SI, t_i),
         base_de(503 + dy, 'Ebook com erros mais frequentes e', NR, t_c), base_de(547 + dy, 'como corrigir na prática.', NR, t_c)]
    im.paste(apagar(im, (215, 175 + dy, 905, 592 + dy), TXT, 3))
    x0 = 231
    L = [
        ([('No se trata de rellenar. Se', SR, verde, False)], t_t),
        ([('trata de ', SR, verde, False), ('saber dónde NO tocar.', SR, ouro, True)], t_t),
        ([('Evite los errores comunes', SI, verde, True), (' que', SI, verde, False)], t_i),
        ([('comprometen el resultado.', SI, verde, False)], t_i),
        ([('Ebook con los errores más frecuentes y', NR, verde, False)], t_c),
        ([('cómo corregirlos en la práctica.', NR, verde, False)], t_c),
    ]
    for (segs, tam), base in zip(L, b):
        l, r = tinta(segs, tam)
        assert x0 + (r - l) < im.width - 16, segs
        desenhar(im, segs, tam, base, x0 - 1 if segs[0][1] == SI else x0, alinh='esquerda', sub_desc=7, sub_esp=2)
    print('  titulo', t_t, 'italico', t_i, 'corpo', t_c)

    # CTA: pílula dourada com borda; o ES cabe na pílula original reduzindo a fonte (12 %)
    cx0, cy0, cx1, cy1, ytop = cta
    cor_p = cor_fundo(im, (cx0 + 30, cy0 + 6, cx1 - 30, cy0 + 12))
    tam0 = tamanho_por_largura('TOQUE EM SAIBA MAIS E GARANTA O SEU.', NB, 806 - 273 + 1, 1.0)
    es = 'TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO.'
    tam = tam0
    while larg(es, NB, tam, 1.0) > 806 - 273 + 1 and tam > tam0 * 0.85:
        tam -= 0.25
    cap = lambda t: -F(NB, t).getbbox('H', anchor='ls')[1]
    base = base_de(ytop, 'TOQUE EM SAIBA MAIS E GARANTA O SEU', NB, tam0) - (cap(tam0) - cap(tam)) / 2
    im.paste(apagar(im, (cx0 + 20, ytop - 6, cx1 - 20, ytop + 28), ESC, 2))
    desenhar(im, [(es, NB, (0, 0, 0), False)], tam, base, cx0, cx1, tracking=1.0)
    print('  cta', tam0, '->', tam, 'cor', cor_p)
    print(salvar(im, saida))


if __name__ == '__main__':
    recompor('trabalho/Fads09-feed.jpg', 'FEA-[FEED] ADS 09 - LATAM.jpg', 0,
             (736, 744, 89, 98, (685, 755, 692, 760)), (241, 1279, 839, 1350, 1309))
    recompor('trabalho/Fads09-story.jpg', 'FEA-[STORIES] ADS 09 - LATAM.jpg', 93,
             (736, 874, 90, 99, (684, 885, 691, 889)), (244, 1526, 836, 1596, 1556))
