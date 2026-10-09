# -*- coding: utf-8 -*-
"""Confere o PDF entregue: relê cada QR e cruza com a sua anotação de link.

Usa os dois detectores do OpenCV. O Aruco lê QR que o detector clássico perde
quando a arte tem moldura ou fundo texturizado, e foi o caso das páginas 20 e
36 deste material: sem ele a conferência acusa falha que não existe.

Falha se um QR não decodificar, se QR e link divergirem na mesma página, se um
QR do YouTube cair fora do mapa, ou se faltar algum destino do mapa no arquivo.

Uso, a partir de traducciones/relleno-ojeras/:
    python3 produccion/conferir_qr_youtube.py Relleno_Tridimensional_de_Ojeras_ES.pdf
"""
import json
import sys

import cv2
import numpy as np
import pymupdf

MAPA = json.load(open('produccion/mapa_youtube_es.json', encoding='utf-8'))
ESPERADO = set(MAPA.values())


def le_qrs(page):
    """Todo QR legível da página, subindo a resolução até algum decodificar."""
    for dpi in (300, 450, 600):
        pix = page.get_pixmap(dpi=dpi)
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
        img = cv2.cvtColor(img, {1: cv2.COLOR_GRAY2BGR, 3: cv2.COLOR_RGB2BGR,
                                 4: cv2.COLOR_RGBA2BGR}[pix.n])
        achados = []
        for detector in (cv2.QRCodeDetectorAruco(), cv2.QRCodeDetector()):
            ok, textos, _, _ = detector.detectAndDecodeMulti(img)
            if not ok:
                continue
            for texto in textos:
                if texto.strip() and texto not in achados:
                    achados.append(texto)
        if achados:
            return achados
    return []


doc = pymupdf.open(sys.argv[1])
falhas, lidos, no_youtube, vistos = [], 0, 0, set()

for page in doc:
    qrs = le_qrs(page)
    links = {l['uri'] for l in page.get_links() if l.get('uri')}
    p = page.number + 1

    if links and not qrs:
        falhas.append('p%d: tem link mas nenhum QR legível' % p)

    for texto in qrs:
        lidos += 1
        if 'youtu' in texto:
            no_youtube += 1
            vistos.add(texto)
            if texto not in ESPERADO:
                falhas.append('p%d: QR do YouTube fora do mapa -> %s' % (p, texto))
        if texto not in links:
            falhas.append('p%d: QR %s sem link correspondente' % (p, texto))

    for url in links:
        if url not in qrs:
            falhas.append('p%d: link %s sem QR correspondente' % (p, url))

ausentes = ESPERADO - vistos
if ausentes:
    falhas.append('destinos do mapa ausentes do PDF: %s' % sorted(ausentes))

print('QR lidos:', lidos, '· apontando para YouTube:', no_youtube)
print('destinos do mapa presentes:', len(vistos), 'de', len(ESPERADO))
print('FALHAS:', len(falhas))
for f in falhas:
    print(' ', f)
sys.exit(1 if falhas else 0)
