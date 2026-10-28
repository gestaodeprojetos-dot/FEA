import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import qrcode

ref, wm_path, fdir, out = sys.argv[1:5]
URL = 'https://sndflw.com/i/bf-2026-latam'
W, H = 2560, 968
BG = (7, 6, 5)

F = lambda n, s: ImageFont.truetype(f'{fdir}/{n}', s)
bebas = lambda s: F('BebasNeue-Regular.ttf', s)
def sora(s, w):
    f = F('Sora[wght].ttf', s); f.set_variation_by_axes([w]); return f
GOLD_HI, GOLD_LO = (244, 206, 150), (196, 140, 72)

# 1) referencia espelhada: fotos e faixa diagonal passam para a esquerda
base = ImageOps.mirror(Image.open(ref).convert('RGBA'))
assert base.size == (W, H)

# apaga o texto antigo (agora na direita) com gradiente escuro
x = np.arange(W, dtype=float)
fade = np.clip((x - 1340) / (1500 - 1340), 0, 1)
cover = np.zeros((H, W, 4), np.uint8)
cover[..., :3] = BG
cover[..., 3] = np.uint8(np.tile(fade, (H, 1)) * 255)
base.alpha_composite(Image.fromarray(cover, 'RGBA'))
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse((W - 520, -380, W + 420, 300), fill=(120, 85, 35, 70))
base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))

# faixa em espanhol cobrindo a original espelhada (canto inferior esquerdo)
ang = math.atan2(1, 1.7115)          # ~30.3 graus
cx, cy = W - 1926, 960
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
tcx = L / 2 + ((W - 2245) - cx) / math.cos(ang)
bd.text((tcx - (tb[2] - tb[0]) / 2 - tb[0], T / 2 - (tb[3] - tb[1]) / 2 - tb[1]), rt, font=rf, fill=(24, 18, 12))
rot = band.rotate(-math.degrees(ang), resample=Image.BICUBIC, expand=True)
base.alpha_composite(rot, (round(cx - rot.width / 2), round(cy - rot.height / 2)))

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

# 2) coluna direita: logo, headline e QR code
LX = 1540
d = ImageDraw.Draw(base)
wm = Image.open(wm_path).convert('RGBA')
a = np.array(wm); a[200:, 560:, 3] = 0; a[150:, 640:, 3] = 0
wm = Image.fromarray(a, 'RGBA')
wm = wm.resize((470, round(470 * wm.height / wm.width)), Image.LANCZOS)

f = bebas(150)
lines = [('ÚNETE AL GRUPO', True), ('DE WHATSAPP', False)]
lh = 132

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(URL); qr.make(fit=True)
q = qr.make_image(fill_color=(12, 10, 8), back_color='white').convert('RGBA')
QS, pad = 250, 16
q = q.resize((QS, QS), Image.NEAREST)
card = Image.new('RGBA', (QS + 2*pad + 8, QS + 2*pad + 8), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=GOLD_LO + (255,))
cd.rounded_rectangle((4, 4, card.width - 5, card.height - 5), 19, fill=(255, 255, 255, 255))
card.alpha_composite(q, (pad + 4, pad + 4))

block = wm.height + 50 + lh * len(lines) + 40 + card.height
y0 = (H - block) // 2
base.alpha_composite(wm, (LX, y0))
y = y0 + wm.height + 50
for t, gold in lines:
    pos = (LX, y - d.textbbox((0, 0), t, font=f, stroke_width=2)[1])
    if gold:
        gold_text(base, pos, t, f)
    else:
        d.text(pos, t, font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255))
    y += lh

qy = y + 40 - (lh - 120)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((LX - 6, qy - 6, LX + card.width + 6, qy + card.height + 6), 26, fill=(214, 160, 90, 110))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
base.alpha_composite(card, (LX, qy))

tx = LX + card.width + 40
fb, fr = sora(40, 700), sora(36, 400)
txt = [('Escanea el código QR', fb, GOLD_HI), ('con la cámara de tu celular', fr, (235, 235, 235)), ('y entra al grupo.', fr, (235, 235, 235))]
sl = 54
ty = qy + card.height // 2 - (sl * len(txt)) // 2 - 4
for i, (t, fo, col) in enumerate(txt):
    d.text((tx, ty + i * sl), t, font=fo, fill=col)

base.convert('RGB').save(out)
print('ok', out, 'texto termina em x =', max(d.textbbox((tx, 0), t, font=fo)[2] for t, fo, _ in txt))
