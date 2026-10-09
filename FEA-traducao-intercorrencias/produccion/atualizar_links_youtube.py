# -*- coding: utf-8 -*-
"""Aponta as anotações de link do PDF para o YouTube, junto com os QR.

O QR e a área clicável são coisas distintas no PDF: `atualizar_qr.py` redesenha
a imagem, este script reescreve a anotação que fica por cima dela. Sem os dois,
o leitor que toca no QR na tela vai para um destino e quem escaneia com o
celular vai para outro.

O casamento é pelo ID do arquivo, não pela URL inteira, porque a mesma origem
aparece com `?usp=`, `?t=` ou sem sufixo nenhum.
"""
import json, re, sys

import pymupdf

MAPA = json.load(open('produccion/mapa_youtube_es.json', encoding='utf-8'))


def ident(url):
    m = re.search(r'/d/([\w-]+)', url)
    return m.group(1) if m else None


doc = pymupdf.open(sys.argv[1])
trocados, mantidos = [], []

for page in doc:
    for link in page.get_links():
        url = link.get('uri', '')
        destino = MAPA.get(ident(url) or '')
        if not destino:
            if url:
                mantidos.append((page.number + 1, url))
            continue
        link['uri'] = destino
        page.update_link(link)
        trocados.append((page.number + 1, destino))

doc.save(sys.argv[2], garbage=3, deflate=True)
print('links trocados', len(trocados), '· mantidos', len(mantidos))
for p, u in trocados:
    print('  p%-3d %s' % (p, u))
