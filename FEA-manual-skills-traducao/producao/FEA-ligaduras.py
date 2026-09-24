# -*- coding: utf-8 -*-
"""Dá às fontes do manual os glifos de ligadura `fi` e `fl`.

Por que isto existe: o motor de HTML do pymupdf troca `fi` e `fl` pelas
ligaduras U+FB01 e U+FB02 por conta própria. Se a fonte não tiver esses
glifos, a palavra sai corrompida, e foi o que aconteceu: «verificação» saiu
«verizcação» no primeiro PDF gerado.

A solução não é uma ligadura desenhada, é um composto de `f` seguido de `i`
na largura natural, que reproduz exatamente o par de letras solto. O texto
fica com a aparência correta e a camada de texto continua legível.

É o mesmo problema que o `limpar_cmap.py` da skill de tradução resolve pelo
outro lado: lá as entradas existiam no cmap com contorno vazio e eram
apagadas; aqui elas não existem e precisam ser criadas.

Uso, a partir de FEA-manual-skills-traducao/:
    python3 producao/FEA-ligaduras.py
"""
import glob
import os

from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(BASE)

PARES = {0xFB01: ('f', 'i'), 0xFB02: ('f', 'l')}


def compor(caminho):
    fonte = TTFont(caminho)
    cmap = fonte.getBestCmap()
    glyf, hmtx = fonte['glyf'], fonte['hmtx']
    criados = []

    for codigo, (a, b) in PARES.items():
        if codigo in cmap:
            continue
        if ord(a) not in cmap or ord(b) not in cmap:
            continue
        ga, gb = cmap[ord(a)], cmap[ord(b)]
        avanco_a = hmtx[ga][0]

        nome = {0xFB01: 'fi', 0xFB02: 'fl'}[codigo]
        caneta = TTGlyphPen(fonte.getGlyphSet())
        caneta.addComponent(ga, (1, 0, 0, 1, 0, 0))
        caneta.addComponent(gb, (1, 0, 0, 1, avanco_a, 0))
        glyf[nome] = caneta.glyph()
        hmtx[nome] = (avanco_a + hmtx[gb][0], hmtx[ga][1])

        for tabela in fonte['cmap'].tables:
            if tabela.isUnicode():
                tabela.cmap[codigo] = nome
        criados.append(nome)

    if criados:
        fonte.save(caminho)
    return criados


for arquivo in sorted(glob.glob('producao/fontes/*.ttf')):
    feitos = compor(arquivo)
    print('%-34s %s' % (os.path.basename(arquivo),
                        ', '.join(feitos) if feitos else 'já tinha'))
