"""Logo LATAM "RELLENO / TRIDIMENSIONAL / DE OJERAS" modelada na logo do Brasil.

Usa as próprias letras da logo original (mesma fonte, corpo, textura dourada e
linha de base). "TRIDIMENSIONAL" e o filete ficam intactos. Só o "J" não existe
no original: é desenhado em Arimo Bold (métrica da Helvetica Bold) e preenchido
com a textura dourada do próprio original, reconstruída por inpainting clássico.
Original: trabalho/logo-br.png (Drive 1ydfyTuMp4hmHVYBjHFayPz1j8SRycfqA).
"""
import os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import fonte, SAIDA

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
orig = Image.open(os.path.join(AQ, 'trabalho', 'logo-br.png')).convert('RGBA')
A = np.array(orig)
L1, L2, L3 = (22, 141), (175, 294), (326, 445)          # faixas das linhas (y0, y1 exclusivo)
G = {  # glifo: (linha, x0, x1)
    'R': (L1, 127, 225), 'E': (L1, 237, 324), 'N': (L1, 436, 533), 'O': (L1, 1255, 1367),
    'L': (L3, 561, 643), 'D': (L3, 188, 290), 'A': (L2, 1157, 1268), 'S': (L2, 786, 883),
}
CENTRO = 696


def glifo(ch):
    (y0, y1), x0, x1 = G[ch]
    return Image.fromarray(A[y0:y1, x0:x1].copy())


def textura():
    """Folha dourada contínua: preenche o vazio entre letras com inpainting clássico."""
    y0, y1 = L1
    tira = A[y0:y1, 26:1367]
    rgb = cv2.cvtColor(tira[..., :3], cv2.COLOR_RGB2BGR)
    vazio = (tira[..., 3] < 200).astype(np.uint8) * 255
    t = cv2.inpaint(rgb, vazio, 7, cv2.INPAINT_TELEA)
    return cv2.cvtColor(t, cv2.COLOR_BGR2RGB)


def glifo_j():
    h = L3[1] - L3[0]
    alt_cap = int((A[L1[0]:L1[1], 237:324, 3] > 40).any(1).sum())   # altura do E = altura de caixa alta
    caminho = fonte('Arimo_700Bold')
    tam = 10
    while True:
        f = ImageFont.truetype(caminho, tam)
        b = f.getbbox('E', anchor='ls')
        if -b[1] >= alt_cap:
            break
        tam += 1
    l, t, r, bo = f.getbbox('J', anchor='ls')
    w = r - l + 2
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((1 - l, h - 1), 'J', font=f, fill=255, anchor='ls')
    # textura: recortes 10x10 tirados só de áreas 100 % tingidas das letras originais, sorteados lado a lado
    rng = np.random.default_rng(7)
    fontes_rgb = []
    for (y0, y1) in (L1, L2, L3):
        al = A[y0:y1, :, 3]
        for yy in range(0, y1 - y0 - 10, 5):
            for xx in range(0, A.shape[1] - 10, 5):
                if al[yy:yy + 10, xx:xx + 10].min() == 255:
                    fontes_rgb.append(A[y0 + yy:y0 + yy + 10, xx:xx + 10, :3])
    tex = np.zeros((h, w, 3), np.uint8)
    for yy in range(0, h, 10):
        for xx in range(0, w, 10):
            pch = fontes_rgb[rng.integers(len(fontes_rgb))]
            tex[yy:yy + 10, xx:xx + 10] = pch[:min(10, h - yy), :min(10, w - xx)]
    rgb = Image.fromarray(tex)
    g = Image.merge('RGBA', (*rgb.split(), m))
    return g


def linha(chars, gaps, y0):
    pecas = [glifo_j() if c == 'J' else glifo(c) for c in chars]
    larg = sum(p.width for p in pecas) + sum(gaps)
    x = CENTRO - larg // 2
    for i, p in enumerate(pecas):
        out.alpha_composite(p, (x, y0))
        x += p.width + (gaps[i] if i < len(gaps) else 0)


out = Image.new('RGBA', orig.size, (0, 0, 0, 0))
# linha 2 (TRIDIMENSIONAL) e filete: pixels originais
out.alpha_composite(Image.fromarray(A[L2[0]:L2[1]]), (0, L2[0]))
out.alpha_composite(Image.fromarray(A[500:540]), (0, 500))
# vãos medidos no original: 13 entre letras retas, 8 depois de L, 48 de espaço entre palavras
linha('RELLENO', [13, 13, 8, 8, 13, 12], L1[0])
linha('DEOJERAS', [12, 48, 8, 10, 13, 0, 6], L3[0])
os.makedirs(SAIDA, exist_ok=True)
p = os.path.join(SAIDA, 'FEA-Logo - Nome - Fonte - Ojeras LATAM.png')
out.save(p, optimize=True)
print('ok', p, out.size)
