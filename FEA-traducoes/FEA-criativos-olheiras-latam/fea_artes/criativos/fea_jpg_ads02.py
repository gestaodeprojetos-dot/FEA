#!/usr/bin/env python3
"""[FEED] ADS 02.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Original em trabalho/Jads02-feed.jpg (Drive 15mabKbWCO3eKSvluV6Qm8uBlw6rHjYC0).
Mockup (capa do ebook + tablet com página gerada por IA) intacto: fase 2.
Selo dourado: arco 'O PRIMEIRO & MAIS VENDIDO' vira 'MÉTODO EXCLUSIVO DEL' (com o 'DR. JOÃO PITHON'
que já está no arco de baixo, o selo lê 'MÉTODO EXCLUSIVO DEL DR. JOÃO PITHON · +30 MIL COPIAS VENDIDAS');
'CÓPIAS' perde o acento (COPIAS).
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads02.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_jpg_util import *  # noqa

VERDE_ESC = (17, 55, 34)
OURO = (217, 178, 105)


def pilula_clara(im, cx, X0, Y0, X1, Y1, segs, pad=19, ext=13):
    """Pílula clara do original esticada: tampa esquerda + coluna central repetida + tampa direita.
    Texto antigo apagado antes por inpainting. Usa só pixels do próprio original."""
    a = np.array(im)
    w_txt = largura(segs)
    W = max(X1 - X0, w_txt + 2 * pad)
    nx0 = int(round(cx - W / 2)); nx1 = nx0 + int(round(W))
    ya, yb = Y0 - 10, Y1 + 12
    tampa_e = a[ya:yb, X0 - ext:X0 + 32].copy()
    tampa_d = a[ya:yb, X1 - 32:X1 + ext + 6].copy()
    meio = np.median(a[ya:yb, int(cx) - 40:int(cx) + 40], 1).astype(np.uint8)
    out = a.copy()
    for x in range(nx0 + 32, nx1 - 32):
        out[ya:yb, x] = meio
    out[ya:yb, nx0 - ext:nx0 + 32] = tampa_e
    out[ya:yb, nx1 - 32:nx1 + ext + 6] = tampa_d
    # costura suave nas bordas externas das tampas e nas faixas de cima/baixo (fundo em degradê)
    for k in range(10):
        t = k / 10
        for xo in (nx0 - ext + k, nx1 + ext + 5 - k):
            out[ya:yb, xo] = (out[ya:yb, xo] * t + a[ya:yb, xo] * (1 - t)).astype(np.uint8)
    for k in range(6):
        t = k / 6
        for yo in (ya + k, yb - 1 - k):
            out[yo, nx0 - ext:nx1 + ext + 6] = (out[yo, nx0 - ext:nx1 + ext + 6] * t + a[yo, nx0 - ext:nx1 + ext + 6] * (1 - t)).astype(np.uint8)
    return Image.fromarray(out), (nx0, nx1)


def recompor(orig, saida):
    im = abrir(orig)
    # ---------- título (Noto Serif caixa-alta 54.75, verde-escuro + dourado) ----------
    im = apagar(im, (150, 222, 935, 442), lambda r, g, b: (r + g + b) < 660, 3)
    f = F('NotoSerif_400Regular', 54.75)
    b = base_de(f, 'APRENDA O PASSO A PASSO', 236)
    cx = 537.5
    linha(im, cx, b, [('APRENDA EL PASO A PASO', f, VERDE_ESC)], 'centro')
    linha(im, cx, b + 75, [('PARA ', f, VERDE_ESC), ('TRATAR OJERAS', f, OURO)], 'centro')
    linha(im, cx, b + 150, [('SIN IMPROVISAR.', f, OURO)], 'centro')
    # ---------- subtítulo (Open Sans Bold + Regular) ----------
    im = apagar(im, (295, 470, 790, 540), lambda r, g, b: (r + g + b) < 600, 2)
    tam = 23.0
    while F('OpenSans_700Bold', tam).getlength('EBOOK COM PROTOCOLO COMPLETO') + F('OpenSans_400Regular', tam).getlength(':') < 452:
        tam += 0.25
    fb, fr = F('OpenSans_700Bold', tam), F('OpenSans_400Regular', 25.0)
    b1 = base_de(fb, 'EBOOK COM', 479)
    preto = (20, 20, 20)
    linha(im, 540, b1, [('EBOOK CON PROTOCOLO COMPLETO', fb, preto), (':', F('OpenSans_400Regular', tam), preto)], 'centro')
    linha(im, 539, b1 + 32, [('ANÁLISIS, PLANIFICACIÓN Y EJECUCIÓN.', fr, preto)], 'centro')
    # ---------- pílula de preço ----------
    im = apagar(im, (282, 584, 800, 630), lambda r, g, b: ((r + g + b) < 560) | (g > r + 40), 3)
    fo, fv = F('OpenSans_400Regular', 30.0), F('OpenSans_700Bold', 37.5)
    segs = [('Acceso completo por solo ', fo, (28, 27, 27)), (PRECOS['preco'], fv, (51, 148, 69))]
    im, _ = pilula_clara(im, 540, 268, 575, 812, 636, segs)
    linha(im, 540, 616, segs, 'centro')
    # ---------- selo dourado ----------
    im, info = trocar_texto_arco(im, 736.5, 782.5, 96.4, 'MÉTODO EXCLUSIVO DEL')
    im = apagar(im, (688, 786, 701, 795), lambda r, g, b: ((r + g + b) < 520) & (r - b > 50), 1, 3)  # acento de CÓPIAS
    print(salvar(im, saida))
    return im


if __name__ == '__main__':
    recompor('trabalho/Jads02-feed.jpg', 'FEA-[FEED] ADS 02 - LATAM.jpg')
