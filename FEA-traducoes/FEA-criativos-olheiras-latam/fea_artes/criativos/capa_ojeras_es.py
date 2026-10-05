"""Capa ES "RELLENO TRIDIMENSIONAL DE OJERAS" feita a partir da capa verde do Brasil.

Sem IA generativa. O título da capa é idêntico (1:1) à logo do Brasil, deslocado
(258, 213); então as linhas 1 e 3 do PT são apagadas por inpainting clássico
(OpenCV xphoto FSR) e no lugar entram as linhas da logo LATAM (letras do próprio
original). "TRIDIMENSIONAL", filete, foto, faixas e assinatura ficam intactos.
O subtítulo vai em Playfair Display (itálico e "ARTI" reto, como no original),
pintado com a textura dourada do próprio original.
Saída: trabalho/capa-es.png (usada nos mockups) e FEA-artes-ES/FEA-Capa Ebook - Ojeras LATAM.png
"""
import os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQ)
from fea_arte_lib import fonte, calibrar, SAIDA

cap = Image.open(os.path.join(AQ, 'trabalho', 'capa-br.png')).convert('RGB')
logo_es = Image.open(os.path.join(SAIDA, 'FEA-Logo - Nome - Fonte - Ojeras LATAM.png')).convert('RGBA')
A = np.array(cap)
r, g, b = [A[..., i].astype(int) for i in range(3)]
OURO = (r > 120) & (r > b + 50) & (r > g + 10)
DX, DY = 258, 213


def apagar(y0, y1, x0, x1, dil=6):
    m = np.zeros(A.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = OURO[y0:y1, x0:x1]
    m = cv2.dilate(m * 255, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    py0, py1, px0, px1 = max(0, y0 - 60), y1 + 60, max(0, x0 - 60), x1 + 60
    reg = A[py0:py1, px0:px1].copy()
    mk = m[py0:py1, px0:px1]
    bgr = cv2.cvtColor(reg, cv2.COLOR_RGB2BGR)
    out = np.zeros_like(bgr)
    cv2.xphoto.inpaint(bgr, 255 - mk, out, cv2.xphoto.INPAINT_FSR_FAST)
    A[py0:py1, px0:px1] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


# texture patches from untouched gold (TRIDIMENSIONAL line), collected before erasing
pat = []
for yy in range(390, 495, 4):
    for xx in range(292, 1600, 4):
        if OURO[yy:yy + 8, xx:xx + 8].all():
            pat.append(A[yy:yy + 8, xx:xx + 8].copy())

apagar(228, 360, 270, 1640)   # PREENCHIMENTO
apagar(532, 664, 430, 1480)   # DE OLHEIRAS
apagar(788, 872, 255, 1650)   # subtítulo
im = Image.fromarray(A).convert('RGBA')
for (y0, y1) in ((22, 141), (326, 445)):
    im.alpha_composite(logo_es.crop((0, y0, logo_es.width, y1)), (DX, DY + y0))

# subtítulo
it, rt = fonte('PlayfairDisplay_700Bold_Italic'), fonte('PlayfairDisplay_700Bold')
f_it = calibrar(it, 'Um Guia Completo com a Metodologia ', 1637 - 267 - ImageFont.truetype(rt, 70).getlength('ARTI'))
f_rt = ImageFont.truetype(rt, f_it.size)
s1, s2 = 'Una Guía Completa con la Metodología ', 'ARTI'
larg = f_it.getlength(s1) + f_rt.getlength(s2)
while larg > 1637 - 267:
    f_it = ImageFont.truetype(it, f_it.size - 0.5); f_rt = ImageFont.truetype(rt, f_it.size)
    larg = f_it.getlength(s1) + f_rt.getlength(s2)
m = Image.new('L', cap.size, 0)
d = ImageDraw.Draw(m)
base = 846   # linha de base do subtítulo original
x = 954 - larg / 2
d.text((x, base), s1, font=f_it, fill=255, anchor='ls')
d.text((x + f_it.getlength(s1), base), s2, font=f_rt, fill=255, anchor='ls')
rng = np.random.default_rng(3)
tex = np.zeros((A.shape[0], A.shape[1], 3), np.uint8)
for yy in range(760, 900, 8):
    for xx in range(200, 1700, 8):
        tex[yy:yy + 8, xx:xx + 8] = pat[rng.integers(len(pat))]
im.paste(Image.fromarray(tex), (0, 0), m)
im = im.convert('RGB')
im.save(os.path.join(AQ, 'trabalho', 'capa-es.png'))
p = os.path.join(SAIDA, 'FEA-Capa Ebook - Ojeras LATAM.png')
im.save(p, optimize=True)
print('ok', p)
