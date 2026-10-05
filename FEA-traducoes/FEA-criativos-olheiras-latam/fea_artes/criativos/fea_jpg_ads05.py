#!/usr/bin/env python3
"""[FEED] ADS 05.jpg e [STORIES] ADS 05.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Originais em trabalho/Jads05-feed.jpg e trabalho/Jads05-story.jpg
(Drive 1ir6NT5joQzE4VJwvflRr7urmguT34HI7 e 1xTYe9qtkvS6ujw4Rbgb4MPr_6dP8c9mH).
Prints de depoimento (WhatsApp) ficam ORIGINAIS em português (regra 4); legenda ES logo abaixo.
Preço lido de precos.json (PRECOS['preco']); a pílula se alarga para caber o valor.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads05.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_jpg_util import *  # noqa

DEP1 = 'Comparto este caso de ojeras + labios siguiendo las enseñanzas del profesor. Muy feliz con el resultado.'
DEP2 = 'Solo quería mostrarle el relleno de ojeras que acabo de realizar en mi consultorio.'
CLARO2 = lambda r, g, b: (r + g + b) > 330


def pilula(im, dy):
    """Pílula translúcida (branco ~16 %) com borda dourada/branca sobre o verde."""
    X0, Y0, X1, Y1 = 268, 1067 + dy, 813, 1130 + dy
    a = np.array(im).astype(float)
    bg = np.array(cor_fundo(im, (60, Y0, 200, Y1)), float)
    # 1) apaga o texto dentro da pílula (inpainting clássico)
    m = mascara_texto(im, (285, Y0 + 5, 800, Y1 - 5), lambda r, g, b: ((r + g + b) > 330) | ((g > 150) & (r < 150)), 3)
    im = apagar_mascara(im, m)
    a = np.array(im).astype(float)
    # 2) desfaz a translucidez dentro do contorno antigo (S = (P - a*255)/(1-a)), linha a linha
    alfas = {}
    for y in range(Y0 + 3, Y1 - 2):
        ref = a[y, 276:284].mean(0)
        al = float(np.clip(((ref - bg) / (255 - bg)).mean(), 0, 0.5))
        alfas[y - Y0] = al
    inn = np.array(mascara_pilula(im.size, (X0 + 2, Y0 + 2, X1 - 2, Y1 - 2))) / 255.0
    for y in range(Y0, Y1 + 1):
        al = alfas.get(y - Y0, alfas[min(alfas, key=lambda k: abs(k - (y - Y0)))])
        w = inn[y][:, None] * al
        a[y] = np.clip((a[y] - w * 255) / (1 - w), 0, 255)
    im = Image.fromarray(a.astype(np.uint8))
    # 3) apaga a borda antiga (anel de 2-3 px) por inpainting
    ext = np.array(mascara_pilula(im.size, (X0 - 1, Y0 - 1, X1 + 1, Y1 + 1)))
    inn2 = np.array(mascara_pilula(im.size, (X0 + 3, Y0 + 3, X1 - 3, Y1 - 3)))
    anel = ((ext > 20) & (inn2 < 235)).astype(np.uint8) * 255
    im = apagar_mascara(im, cv2.dilate(anel, np.ones((3, 3), np.uint8)), 4)
    # 4) texto ES e nova largura
    fr, fb = F('OpenSans_400Regular', 30.0), F('OpenSans_700Bold', 37.5)
    segs = [('Acceso completo por solo ', fr, (255, 255, 255)), (PRECOS['preco'], fb, (36, 255, 75))]
    w = largura(segs)
    larg = max(X1 - X0, w + 2 * 20)
    cx = (X0 + X1) / 2
    nx0, nx1 = cx - larg / 2, cx + larg / 2
    # 5) desenha a nova pílula: preenchimento branco translúcido (gradiente vertical do original) + borda
    camada = np.array(im).astype(float)
    mi = np.array(mascara_pilula(im.size, (nx0 + 2, Y0 + 2, nx1 - 2, Y1 - 2))) / 255.0
    for y in range(Y0, Y1 + 1):
        al = alfas.get(y - Y0, alfas[min(alfas, key=lambda k: abs(k - (y - Y0)))])
        wgt = mi[y][:, None] * al
        camada[y] = camada[y] * (1 - wgt) + 255 * wgt
    im = Image.fromarray(camada.astype(np.uint8))
    me = np.array(mascara_pilula(im.size, (nx0, Y0, nx1, Y1))).astype(float)
    anel = np.clip(me - mi * 255, 0, 255) / 255.0
    xs = np.arange(im.width)
    t = np.clip(np.abs(xs - cx) / (larg / 2), 0, 1) ** 6          # dourado no meio, branco nas pontas
    ouro, branco = np.array([241, 195, 110.]), np.array([255, 255, 255.])
    cor_b = ouro[None, :] * (1 - t[:, None]) + branco[None, :] * t[:, None]
    arr = np.array(im).astype(float)
    arr = arr * (1 - anel[..., None]) + cor_b[None, :, :] * anel[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    linha(im, cx, 1108 + dy, segs, 'centro')
    return im


def recompor(orig, dy, saida, story=False):
    im = abrir(orig)
    # ---------- título central (Noto Serif 47.75, branco + dourado) ----------
    im = apagar(im, (160, 765 + dy, 900, 1020 + dy), CLARO2, 3)
    f = F('NotoSerif_400Regular', 47.75)
    b = base_de(f, 'O preenchimento de olheiras', 777 + dy)
    passo = (971 - 777) / 3
    BR, OU = (255, 255, 255), (240, 194, 108)
    linhas = [[('El ', f, BR), ('relleno de ojeras', f, OU), (' no es', f, BR)],
              [('una técnica difícil para quien', f, BR)],
              [('tiene un razonamiento', f, BR)],
              [('clínico estructurado.', f, BR)]]
    for i, s in enumerate(linhas):
        linha(im, 529.5, b + passo * i, s, 'centro')
    # ---------- pílula de preço ----------
    im = pilula(im, dy)
    # ---------- CTA dourado ----------
    cta = (241, 1364, 839, 1435) if story else (241, 1279, 840, 1350)
    cta_dourado(im, cta, 1394 if story else 1309)
    # ---------- legendas dos depoimentos (regra 4) ----------
    cor_leg = (196, 210, 200)
    if story:
        fl = F('OpenSans_400Regular_Italic', 16)
        legenda_depoimento(im, DEP1, 272, 862, 460, fl, cor_leg, 21)
        legenda_depoimento(im, DEP2, 790, 870, 440, fl, cor_leg, 21)
    else:
        fl = F('OpenSans_400Regular_Italic', 14)
        legenda_depoimento(im, DEP1, 272, 725, 470, fl, cor_leg, 18)
        legenda_depoimento(im, DEP2, 785, 731, 440, fl, cor_leg, 18)
    # ---------- marca no rodapé (só story) ----------
    if story:
        cx = (380, 1530, 700, 1632)
        ouro = cor_texto(im, cx, lambda r, g, b: (r - b > 60) & (r > 120))
        im = apagar(im, cx, lambda r, g, b: (r - b > 40) & (r > 90), 3)
        fa = calibrar(fonte('Arimo_700Bold'), 'TRIDIMENSIONAL', 673 - 400)
        bb = base_de(fa, 'PREENCHIMENTO', 1539)
        cxm = (400 + 673) / 2
        for i, t in enumerate(['RELLENO', 'TRIDIMENSIONAL', 'DE OJERAS']):
            linha(im, cxm, bb + 31.5 * i, [(t, fa, ouro)], 'centro')
    print(salvar(im, saida))
    return im


if __name__ == '__main__':
    recompor('trabalho/Jads05-feed.jpg', 0, 'FEA-[FEED] ADS 05 - LATAM.jpg')
    recompor('trabalho/Jads05-story.jpg', 175, 'FEA-[STORIES] ADS 05 - LATAM.jpg', story=True)
