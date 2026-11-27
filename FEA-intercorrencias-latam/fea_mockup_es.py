"""Troca o texto da capa em mockup (perspectiva) pela capa ES, transferindo a iluminação do mockup.
Uso: python3 -I fea_mockup_es.py DIR_IMG mockup.png H.npy saida.png [x0 y0 x1 y1 da área do mockup]
Sem IA generativa: homografia + razão de iluminação + máscara das faixas de texto.
"""
import sys

import cv2
import numpy as np

D, MOCK, HF, OUT = sys.argv[1:5]
cov_pt = cv2.imread(f"{D}/cover_v6.jpeg").astype(np.float32)
cov_es = cv2.imread(f"{D}/cover_es.jpeg").astype(np.float32)
mock = cv2.imread(f"{D}/{MOCK}", cv2.IMREAD_UNCHANGED)
alpha = mock[:, :, 3:] if mock.shape[2] == 4 else None
mk = mock[:, :, :3].astype(np.float32)
H = np.load(HF)
h, w = mk.shape[:2]

# reduz a capa antes do warp (evita serrilhado)
corners = cv2.perspectiveTransform(np.float32([[0, 0], [1519, 0], [1519, 2181], [0, 2181]]).reshape(-1, 1, 2), H)
span = np.linalg.norm(corners[1] - corners[0])
s = min(1.0, 1.6 * span / 1519)
S = np.array([[1 / s, 0, 0], [0, 1 / s, 0], [0, 0, 1]], np.float64)
Hs = H @ S
small = lambda im: cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
wp = cv2.warpPerspective(small(cov_pt), Hs, (w, h), flags=cv2.INTER_CUBIC)
we = cv2.warpPerspective(small(cov_es), Hs, (w, h), flags=cv2.INTER_CUBIC)

# faixas de texto na capa (coordenadas da capa 1519x2181): título+subtítulo e box
band = np.zeros((2181, 1519), np.float32)
band[38:332, 40:1480] = 1
band[1828:1964, 60:1460] = 1
mask = cv2.warpPerspective(small(band), Hs, (w, h), flags=cv2.INTER_LINEAR)
mask = cv2.GaussianBlur(mask, (0, 0), 1.2)[:, :, None]

# iluminação do mockup: razão suave mockup / capa PT achatada, medida só no fundo azul
# (convolução normalizada: ignora letras, bordas da capa e fotos)
inside = cv2.warpPerspective(small(np.ones((2181, 1519), np.float32)), Hs, (w, h), flags=cv2.INTER_NEAREST)
inside = cv2.erode(inside, np.ones((7, 7), np.uint8))
def bluebg(im):
    b, g, r = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return ((b > r + 25) & (b > g + 5)).astype(np.float32)
Wt = inside * bluebg(mk) * bluebg(wp)
sig = max(6, span / 40)
nb = lambda im: cv2.GaussianBlur(im * Wt[:, :, None], (0, 0), sig) / (cv2.GaussianBlur(Wt, (0, 0), sig)[:, :, None] + 1e-4)
L = (nb(mk) + 1) / (nb(wp) + 1)
if len(sys.argv) > 6 and sys.argv[6] == 'gray':
    L = np.repeat(L.mean(axis=2, keepdims=True), 3, axis=2)
L = np.clip(L, 0.3, 3.0)
mask = (cv2.GaussianBlur(mask[:, :, 0], (0, 0), 2.5) * inside)[:, :, None]
MODE = sys.argv[5] if len(sys.argv) > 5 else "delta"
if MODE == "delta":
    # só a diferença ES - PT entra (fundo idêntico fica intocado); texto PT sai pela mesma conta
    new = np.clip(mk + (we - wp) * L, 0, 255)
else:
    # letras: cor média do mockup (sem o brilho local), fundo: iluminação local
    def cls(im):
        b, g, r = im[:, :, 0], im[:, :, 1], im[:, :, 2]
        orange = (r > b + 60) & (r > 120)
        white = (b > 150) & (g > 150) & (r > 150) & (np.abs(r - b) < 45)
        return orange, white
    band_px = mask[:, :, 0] > 0.5
    om, wm = cls(mk); oe, wpw = cls(wp)
    Lo = np.median(mk[om & band_px], axis=0) / np.median(wp[oe & band_px], axis=0)
    Lw = np.median(mk[wm & band_px], axis=0) / np.median(wp[wpw & band_px], axis=0)
    o2, w2 = cls(we)
    to = cv2.GaussianBlur(o2.astype(np.float32), (0, 0), 0.8)[:, :, None]
    tw = cv2.GaussianBlur(w2.astype(np.float32), (0, 0), 0.8)[:, :, None]
    tb = np.clip(1 - to - tw, 0, 1)
    new = np.clip(we * (L * tb + Lo * to + Lw * tw), 0, 255)
    print("Lo", Lo.round(3), "Lw", Lw.round(3))
out = mk * (1 - mask) + new * mask
out = out.round().astype(np.uint8)
if alpha is not None:
    out = np.dstack([out, alpha])
cv2.imwrite(OUT, out)
# relatório: resíduo fora da máscara (deve ser ~0) e diferença dentro
print("pixels alterados:", int((mask[:, :, 0] > 0.01).sum()), "escala", round(s, 3), "sigma", round(sig, 1))
