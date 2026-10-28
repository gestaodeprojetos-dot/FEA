import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import qrcode

ref, wm_path, fdir, out = sys.argv[1:5]
URL = 'https://sndflw.com/i/bf-2026-latam'
W, H = 2560, 968
SHIFT = 1010                    # fotos do Dr. Joao vao para a esquerda, sem espelhar
EDGE = W - SHIFT                # borda direita das fotos (1550)
BG = (7, 6, 5)

F = lambda n, s: ImageFont.truetype(f'{fdir}/{n}', s)
bebas = lambda s: F('BebasNeue-Regular.ttf', s)
def sora(s, w):
    f = F('Sora[wght].ttf', s); f.set_variation_by_axes([w]); return f
GOLD_HI, GOLD_LO = (244, 206, 150), (196, 140, 72)

# 1) fotos deslocadas para a esquerda, borda direita fundindo no fundo escuro
photo = Image.open(ref).convert('RGBA')
base = Image.new('RGBA', (W, H), BG + (255,))
sh_ = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh_.paste(photo.crop((SHIFT, 0, W, H)), (0, 0))
x = np.arange(W, dtype=float)
m = np.clip((EDGE - 10 - x) / 150, 0, 1)
sa = np.array(sh_); sa[..., 3] = np.uint8(sa[..., 3] * np.tile(m, (H, 1)))
base.alpha_composite(Image.fromarray(sa, 'RGBA'))
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse((W - 700, -380, W + 300, 320), fill=(120, 85, 35, 60))
base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))

# 2) faixa em espanhol sobre a original, terminando em ponta de fita na borda das fotos
ang = math.atan2(1, 1.7115)
cx, cy = 1926 - SHIFT, 960
L, T = 2200, 96
end = int(L / 2 + (EDGE + 5 - cx) / math.cos(ang))
g = np.zeros((T, L, 4), np.uint8)
u = np.abs(np.linspace(-1, 1, L))[None, :]
lo, hi = np.array([206, 148, 82]), np.array([236, 188, 128])
for i in range(3):
    g[..., i] = np.uint8(hi[i] + (lo[i] - hi[i]) * u)
g[..., 3] = 255
g[:, end:, 3] = 0
band = Image.fromarray(g, 'RGBA')
bd = ImageDraw.Draw(band)
bd.polygon([(end - 34, T / 2), (end + 1, -1), (end + 1, T + 1)], fill=(0, 0, 0, 0))
rt = 'GRUPO EXCLUSIVO EN WHATSAPP'
rf = F('ArchivoBlack-Regular.ttf', 31)
tb = bd.textbbox((0, 0), rt, font=rf)
tcx = L / 2 + ((2245 - SHIFT) - cx) / math.cos(ang) - 20
bd.text((tcx - (tb[2] - tb[0]) / 2 - tb[0], T / 2 - (tb[3] - tb[1]) / 2 - tb[1]), rt, font=rf, fill=(24, 18, 12))
rot = band.rotate(math.degrees(ang), resample=Image.BICUBIC, expand=True)
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

# 3) bloco da direita: logo, headline, texto de apoio e QR (mesmo desenho da versao B)
LX = 1640
d = ImageDraw.Draw(base)
wm = Image.open(wm_path).convert('RGBA')
a = np.array(wm); a[200:, 560:, 3] = 0; a[150:, 640:, 3] = 0
wm = Image.fromarray(a, 'RGBA')
wm = wm.resize((470, round(470 * wm.height / wm.width)), Image.LANCZOS)
base.alpha_composite(wm, (LX, 70))
y = 70 + wm.height + 55
f = bebas(150)
bb = gold_text(base, (LX, y), 'ÚNETE AL GRUPO', f)
y2 = bb[3] + 16
top = d.textbbox((0, 0), 'DE WHATSAPP', font=f)[1]
d.text((LX, y2 - top), 'DE WHATSAPP', font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255))
y_after = d.textbbox((LX, y2 - top), 'DE WHATSAPP', font=f)[3]

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
qr.add_data(URL); qr.make(fit=True)
q = qr.make_image(fill_color=(12, 10, 8), back_color='white').convert('RGBA').resize((250, 250), Image.NEAREST)
pad = 16
card = Image.new('RGBA', (250 + 2*pad + 8,) * 2, (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=GOLD_LO + (255,))
cd.rounded_rectangle((4, 4, card.width - 5, card.height - 5), 19, fill=(255, 255, 255, 255))
card.alpha_composite(q, (pad + 4, pad + 4))
qy = y_after + 48
QX = LX + 560
glowq = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glowq).rounded_rectangle((QX - 6, qy - 6, QX + card.width + 6, qy + card.height + 6), 26, fill=(214, 160, 90, 110))
base.alpha_composite(glowq.filter(ImageFilter.GaussianBlur(22)))
base.alpha_composite(card, (QX, qy))
txt = [('Escanea el código QR', sora(40, 700), GOLD_HI), ('con la cámara de tu celular', sora(38, 400), (235, 235, 235)), ('y entra al grupo.', sora(38, 400), (235, 235, 235))]
ty = qy + card.height // 2 - (54 * 3) // 2 - 4
for i, (t, fo, col) in enumerate(txt):
    d.text((LX, ty + i * 54), t, font=fo, fill=col)

base.convert('RGB').save(out)
print('ok; QR termina em x =', QX + card.width)
