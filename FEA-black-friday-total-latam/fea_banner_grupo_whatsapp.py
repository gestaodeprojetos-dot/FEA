import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import qrcode

ref, wm_path, fdir, out = sys.argv[1:5]
URL = 'https://sndflw.com/i/bf-2026-latam'
W, H = 2560, 968
base = Image.open(ref).convert('RGBA')
assert base.size == (W, H)

# 1) apaga o bloco de texto da esquerda com gradiente escuro
x = np.arange(W, dtype=float)
fade = np.clip((1110 - x) / (1110 - 930), 0, 1)
alpha = np.tile(fade, (H, 1))
cover = np.zeros((H, W, 4), np.uint8)
cover[..., 0], cover[..., 1], cover[..., 2] = 7, 6, 5
cover[..., 3] = np.uint8(alpha * 255)
base.alpha_composite(Image.fromarray(cover, 'RGBA'))
# brilho dourado sutil no canto superior esquerdo, como na referencia
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((-420, -380, 520, 300), fill=(120, 85, 35, 70))
base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))

F = lambda n, s: ImageFont.truetype(f'{fdir}/{n}', s)
bebas = lambda s: F('BebasNeue-Regular.ttf', s)
def sora(s, w):
    f = F('Sora[wght].ttf', s); f.set_variation_by_axes([w]); return f
GOLD_HI, GOLD_LO = (244, 206, 150), (196, 140, 72)

def gold_text(img, xy, text, font, spread=0):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).text(xy, text, font=font, fill=255, stroke_width=2, stroke_fill=255)
    bb = m.getbbox()
    grad = Image.new('RGBA', img.size)
    g = np.zeros((H, W, 4), np.uint8)
    t = np.clip((np.arange(H)[:, None] - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)
    for i in range(3):
        g[..., i] = np.uint8(GOLD_HI[i] + (GOLD_LO[i] - GOLD_HI[i]) * t)
    g[..., 3] = 255
    grad = Image.fromarray(g, 'RGBA'); grad.putalpha(m)
    img.alpha_composite(grad)
    return bb

# 2) logo Black Friday Total
wm = Image.open(wm_path).convert('RGBA')
a = np.array(wm)
a[200:, 560:, 3] = 0
a[150:, 640:, 3] = 0
wm = Image.fromarray(a, 'RGBA')
LX = 118
wm = wm.resize((470, round(470 * wm.height / wm.width)), Image.LANCZOS)
base.alpha_composite(wm, (LX, 70))

# 3) headline em espanhol
d = ImageDraw.Draw(base)
y = 70 + wm.height + 55
f = bebas(150)
bb = gold_text(base, (LX, y), 'ÚNETE AL GRUPO', f)
y2 = bb[3] + 16
d.text((LX, y2 - (d.textbbox((0, 0), 'DE WHATSAPP', font=f)[1])), 'DE WHATSAPP', font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255))
y_after = d.textbbox((LX, y2 - d.textbbox((0, 0), 'DE WHATSAPP', font=f)[1]), 'DE WHATSAPP', font=f)[3]

# 4) QR code em cartao branco com borda dourada
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(URL); qr.make(fit=True)
q = qr.make_image(fill_color=(12, 10, 8), back_color='white').convert('RGBA')
QS = 250
q = q.resize((QS, QS), Image.NEAREST)
pad = 16
qy = y_after + 48
card = Image.new('RGBA', (QS + 2*pad + 8, QS + 2*pad + 8), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=GOLD_LO + (255,))
cd.rounded_rectangle((4, 4, card.width - 5, card.height - 5), 19, fill=(255, 255, 255, 255))
card.alpha_composite(q, (pad + 4, pad + 4))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((LX - 6, qy - 6, LX + card.width + 6, qy + card.height + 6), 26, fill=(214, 160, 90, 110))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
base.alpha_composite(card, (LX, qy))

# texto de apoio ao lado do QR
tx = LX + card.width + 40
fb, fr = sora(40, 700), sora(38, 400)
lines = [('Escanea el código QR', fb, GOLD_HI), ('con la cámara de tu celular', fr, (235, 235, 235)), ('y entra al grupo.', fr, (235, 235, 235))]
lh = 54
ty = qy + card.height // 2 - (lh * len(lines)) // 2 - 4
for i, (t, fo, col) in enumerate(lines):
    d.text((tx, ty + i * lh), t, font=fo, fill=col)

# 5) faixa diagonal em espanhol cobrindo a original
ang = math.atan2(1, 1.7115)          # ~30.3 graus
cx, cy = 1926, 960
L, T = 2200, 96
band = Image.new('RGBA', (L, T), (0, 0, 0, 0))
bg = np.zeros((T, L, 4), np.uint8)
u = np.abs(np.linspace(-1, 1, L))[None, :]
lo, hi = np.array([206, 148, 82]), np.array([236, 188, 128])
for i in range(3):
    bg[..., i] = np.uint8(hi[i] + (lo[i] - hi[i]) * u)
bg[..., 3] = 255
band = Image.fromarray(bg, 'RGBA')
bd = ImageDraw.Draw(band)
rt = 'GRUPO EXCLUSIVO EN WHATSAPP'
rf = F('ArchivoBlack-Regular.ttf', 31)
tb = bd.textbbox((0, 0), rt, font=rf)
# centro do texto na posicao original (~ x 2160 ao longo da faixa)
along = (2245 - cx) / math.cos(ang)
tcx = L / 2 + along
bd.text((tcx - (tb[2] - tb[0]) / 2 - tb[0], T / 2 - (tb[3] - tb[1]) / 2 - tb[1]), rt, font=rf, fill=(24, 18, 12))
rot = band.rotate(math.degrees(ang), resample=Image.BICUBIC, expand=True)
base.alpha_composite(rot, (round(cx - rot.width / 2), round(cy - rot.height / 2)))

base.convert('RGB').save(out, quality=95)
print('ok', out)
