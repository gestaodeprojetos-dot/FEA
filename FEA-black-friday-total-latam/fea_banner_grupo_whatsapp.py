import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import qrcode

ref, wm_path, fdir, out = sys.argv[1:5]
URL = 'https://sndflw.com/i/bf-2026-latam'
W, H = 2560, 968
SHIFT = 380                     # fotos andam para a esquerda, abrindo a coluna do QR na direita
COL_X = W - SHIFT               # inicio da coluna do QR
BG = (7, 6, 5)

F = lambda n, s: ImageFont.truetype(f'{fdir}/{n}', s)
bebas = lambda s: F('BebasNeue-Regular.ttf', s)
def sora(s, w):
    f = F('Sora[wght].ttf', s); f.set_variation_by_axes([w]); return f
GOLD_HI, GOLD_LO = (244, 206, 150), (196, 140, 72)

# 1) camada de fotos: referencia + faixa diagonal em espanhol cobrindo a original
photo = Image.open(ref).convert('RGBA')
assert photo.size == (W, H)
ang = math.atan2(1, 1.7115)          # ~30.3 graus
cx, cy = 1926, 960
L, T = 2200, 96
g = np.zeros((T, L, 4), np.uint8)
u = np.abs(np.linspace(-1, 1, L))[None, :]
lo, hi = np.array([206, 148, 82]), np.array([236, 188, 128])
for i in range(3):
    g[..., i] = np.uint8(hi[i] + (lo[i] - hi[i]) * u)
g[..., 3] = 255
band = Image.fromarray(g, 'RGBA')
bd = ImageDraw.Draw(band)
rt = 'GRUPO EXCLUSIVO EN WHATSAPP'
rf = F('ArchivoBlack-Regular.ttf', 31)
tb = bd.textbbox((0, 0), rt, font=rf)
tcx = L / 2 + (2245 - cx) / math.cos(ang)
bd.text((tcx - (tb[2] - tb[0]) / 2 - tb[0], T / 2 - (tb[3] - tb[1]) / 2 - tb[1]), rt, font=rf, fill=(24, 18, 12))
rot = band.rotate(math.degrees(ang), resample=Image.BICUBIC, expand=True)
photo.alpha_composite(rot, (round(cx - rot.width / 2), round(cy - rot.height / 2)))

# desloca as fotos e funde as duas bordas no fundo escuro
base = Image.new('RGBA', (W, H), BG + (255,))
shifted = Image.new('RGBA', (W, H), (0, 0, 0, 0))
shifted.paste(photo.crop((SHIFT, 0, W, H)), (0, 0))
x = np.arange(W, dtype=float)
left = np.clip((x - 640) / (770 - 640), 0, 1)
right = np.clip((COL_X - x) / 170, 0, 1)
m = np.tile(left * right, (H, 1))
sa = np.array(shifted); sa[..., 3] = np.uint8(sa[..., 3] * m)
base.alpha_composite(Image.fromarray(sa, 'RGBA'))
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((-420, -380, 520, 300), fill=(120, 85, 35, 70))
gd.ellipse((COL_X - 120, 180, W + 200, 800), fill=(150, 105, 45, 55))
base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))

def gold_text(img, xy, text, font):
    mk = Image.new('L', img.size, 0)
    ImageDraw.Draw(mk).text(xy, text, font=font, fill=255, stroke_width=2, stroke_fill=255)
    bb = mk.getbbox()
    gg = np.zeros((H, W, 4), np.uint8)
    t = np.clip((np.arange(H)[:, None] - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)
    for i in range(3):
        gg[..., i] = np.uint8(GOLD_HI[i] + (GOLD_LO[i] - GOLD_HI[i]) * t)
    gg[..., 3] = 255
    grad = Image.fromarray(gg, 'RGBA'); grad.putalpha(mk)
    img.alpha_composite(grad)
    return bb

# 2) coluna esquerda: logo + headline, centralizados na vertical
wm = Image.open(wm_path).convert('RGBA')
a = np.array(wm); a[200:, 560:, 3] = 0; a[150:, 640:, 3] = 0
wm = Image.fromarray(a, 'RGBA')
LX = 110
wm = wm.resize((470, round(470 * wm.height / wm.width)), Image.LANCZOS)
f = bebas(150)
d = ImageDraw.Draw(base)
lines = [('ÚNETE AL', True), ('GRUPO DE', False), ('WHATSAPP', False)]
asc = d.textbbox((0, 0), 'Ú', font=f, stroke_width=2)
lh = 132
block = wm.height + 60 + lh * len(lines)
y0 = (H - block) // 2
base.alpha_composite(wm, (LX, y0))
y = y0 + wm.height + 60
for t, gold in lines:
    top = d.textbbox((0, 0), t, font=f, stroke_width=2)[1]
    pos = (LX, y - top + (0 if t != 'ÚNETE AL' else 0))
    if gold:
        gold_text(base, pos, t, f)
    else:
        d.text(pos, t, font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255))
    y += lh

# 3) coluna direita: QR code
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(URL); qr.make(fit=True)
q = qr.make_image(fill_color=(12, 10, 8), back_color='white').convert('RGBA')
QS, pad = 270, 16
q = q.resize((QS, QS), Image.NEAREST)
card = Image.new('RGBA', (QS + 2*pad + 8, QS + 2*pad + 8), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=GOLD_LO + (255,))
cd.rounded_rectangle((4, 4, card.width - 5, card.height - 5), 19, fill=(255, 255, 255, 255))
card.alpha_composite(q, (pad + 4, pad + 4))

ccx = COL_X + SHIFT // 2 - 4
lab_f = bebas(64)
sub_f = sora(30, 400)
lab_h = 64; sub_h = 40
stack = lab_h + 26 + card.height + 26 + sub_h * 2
sy = (H - stack) // 2
lb = d.textbbox((0, 0), 'ESCANEA EL QR', font=lab_f)
gold_text(base, (ccx - (lb[2] - lb[0]) / 2 - lb[0], sy - lb[1]), 'ESCANEA EL QR', lab_f)
qy = sy + lab_h + 26
qx = ccx - card.width // 2
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((qx - 6, qy - 6, qx + card.width + 6, qy + card.height + 6), 26, fill=(214, 160, 90, 110))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
base.alpha_composite(card, (qx, qy))
ty = qy + card.height + 26
for i, t in enumerate(['con la cámara', 'de tu celular.']):
    b = d.textbbox((0, 0), t, font=sub_f)
    d.text((ccx - (b[2] - b[0]) / 2 - b[0], ty + i * sub_h), t, font=sub_f, fill=(235, 235, 235))

base.convert('RGB').save(out)
print('ok', out)
