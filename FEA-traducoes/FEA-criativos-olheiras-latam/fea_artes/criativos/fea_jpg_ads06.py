#!/usr/bin/env python3
"""[FEED] ADS 06.jpg e [STORIES] ADS 06.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Originais em trabalho/Fads06-feed.jpg e trabalho/Fads06-story.jpg
(Drive 14vwqVJEI7AvZZyL9bj58dNOlpSwPS4Ou e 1EhGjZw43yQghAYa4WVuMDCyXNrh3nX6A).
Fontes identificadas: Noto Serif (faixa amarela e chamada itálica), Noto Sans (corpo e CTA).
Selo dourado: arco superior trocado por 'MÉTODO EXCLUSIVO DEL' (o arco inferior 'DR. JOÃO PITHON'
completa a frase) e CÓPIAS -> COPIAS. Capa do livro e página do tablet (mockup PT): fase 2.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads06.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg06a09 import *  # noqa
from fea_arte_lib import abrir, salvar, preencher, apagar, cor_texto, cor_fundo, CLARO, ESCURO

SR, SI = 'NotoSerif_400Regular', 'NotoSerif_400Regular_Italic'
NR, NB = 'NotoSans_400Regular', 'NotoSans_700Bold'
LIM = 16  # margem lateral mínima


def recompor(orig, saida, P):
    im = abrir(orig)
    # 1. selo
    print(saida, 'selo', selo_es(im, *P['selo'], **P.get('selo_kw', {})))
    # 2. faixa amarela (texto escuro)
    am = P['amarela']
    pt = [('Evitar olheiras está te ', SR, 0, False), ('custando pacientes.', SI, 0, False)]
    es = [('Evitar tratar ojeras le está ', SR, 0, False), ('costando pacientes.', SI, 0, False)]
    t = faixa(im, am['caixa'], (pt, 0.0), es, am['ytop'], am['x0'], am['x1'])
    print('  faixa amarela', t)
    # 3. chamada itálica branca + corpo (sobre fundo verde liso): apaga os textos claros
    ch, co = P['chamada'], P['corpo']
    zona = (40, ch[0][0] - 10, im.width - 40, co[1][0] + 34)
    cor_ch = cor_texto(im, (ch[0][1], ch[0][0], ch[0][2], ch[0][0] + 40), CLARO)
    cor_co = cor_texto(im, (co[0][1], co[0][0], co[0][2], co[0][0] + 26), CLARO)
    tam_ch = tamanho_por_largura('valorizadas da harmonização.', SI, ch[1][2] - ch[1][1] + 1)
    b_ch = [base_de(y, txt, SI, tam_ch) for (y, _, _), txt in zip(ch, ['Domine uma das áreas mais', 'valorizadas da harmonização.'])]
    s1 = [('Com um ebook que mostra ', NR, 0, False), ('o ', NB, 0, False), ('raciocínio', NB, 0, True)]
    s2 = [('clínico', NB, 0, True), (' por trás de cada aplicação.', NB, 0, False)]
    tam_co = tamanho_segs(s1, co[0][2] - co[0][1] + 1)
    b_co = [base_de(co[0][0], 'Com um ebook que mostra o raciocínio', NB, tam_co),
            base_de(co[1][0], 'clínico por trás de cada aplicação.', NB, tam_co)]
    im2 = apagar(im, zona, CLARO, 2)
    im.paste(im2)
    for txt, b in zip(['Domine una de las áreas más', 'valoradas de la armonización.'], b_ch):
        desenhar(im, [(txt, SI, cor_ch, False)], tam_ch, b, ch[0][1], ch[0][2])
    e1 = [('Con un ebook que muestra ', NR, cor_co, False), ('el ', NB, cor_co, False), ('razonamiento', NB, cor_co, True)]
    e2 = [('clínico', NB, cor_co, True), (' detrás de cada aplicación.', NB, cor_co, False)]
    cxc = (co[0][1] + co[0][2]) / 2
    for segs, b in ((e1, b_co[0]), (e2, b_co[1])):
        desenhar(im, segs, tam_co, b, cxc, cxc, sub_desc=P['sub_desc'], sub_esp=P['sub_esp'])
    print('  chamada', tam_ch, 'corpo', tam_co)
    # 4. CTA verde
    ct = P['cta']
    pt = [('TOQUE EM SAIBA MAIS E GARANTA O SEU.', NB, 0, False)]
    es = [('TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO.', NB, 0, False)]
    t = faixa(im, ct['caixa'], (pt, 1.0), es, ct['ytop'], ct['x0'], ct['x1'])
    print('  cta', t)
    print(salvar(im, saida))


FEED = dict(
    selo=(735, 302, 73, 80, (692, 310, 699, 313)),
    amarela=dict(caixa=(177, 910, 906, 968), ytop=923, x0=187, x1=890),
    chamada=[(993, 299, 770), (1043, 282, 786)],
    corpo=[(1132, 316, 765), (1165, 340, 738)],
    sub_desc=4, sub_esp=1,
    cta=dict(caixa=(241, 1279, 839, 1350), ytop=1309, x0=273, x1=806),
)
STORY = dict(
    selo=(724, 338, 80, 89, (677, 349, 683, 352)), selo_kw=dict(escala=0.8),
    amarela=dict(caixa=(101, 1132, 983, 1202), ytop=1148, x0=112, x1=964),
    chamada=[(1233, 248, 819), (1292, 227, 839)],
    corpo=[(1400, 268, 813), (1440, 297, 781)],
    sub_desc=5, sub_esp=2,
    cta=dict(caixa=(241, 1552, 839, 1623), ytop=1582, x0=273, x1=806),
)

if __name__ == '__main__':
    recompor('trabalho/Fads06-feed.jpg', 'FEA-[FEED] ADS 06 - LATAM.jpg', FEED)
    recompor('trabalho/Fads06-story.jpg', 'FEA-[STORIES] ADS 06 - LATAM.jpg', STORY)
