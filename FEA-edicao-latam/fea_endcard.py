"""Cartela final padrão LATAM: logo Black Friday Total surge com impacto + "Toca en Más información" digitado com som de teclado.
Áudio: o mesmo do finalzinho padrão dos criativos originais (endcard/sfx.wav). Uso: python3 fea_endcard.py out.mp4"""
import os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1080, 1920, 30, 5.0
TEXT = "Toca en Más información"
CLICKS = [1.54, 1.665, 1.71, 1.8, 1.845, 2.005, 2.05, 2.25, 2.335, 2.425, 2.58, 2.64, 2.745, 2.84, 2.935, 3.045, 3.135, 3.185, 3.28, 3.38]
GOLD = (222, 176, 98)
lg0 = Image.open(os.path.join(HERE, "logo", "FEA-black-friday-total-logo.png")).convert("RGBA")
LW = 740
lg = lg0.resize((LW, int(lg0.height * LW / lg0.width)), Image.LANCZOS)
glow = lg.filter(ImageFilter.GaussianBlur(26))
CY = 860
f = ImageFont.truetype(os.path.join(HERE, "fonts", "Montserrat-700.ttf"), 50)
d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
tw = d0.textlength(TEXT, font=f); tx = (W - tw) / 2; ty = CY + lg.height // 2 + 150


def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def nchars(t):
    if t < CLICKS[0]: return 0
    k = sum(1 for c in CLICKS if c <= t)
    return min(len(TEXT), round(k * len(TEXT) / len(CLICKS)))


def frame(t):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    # logo: varredura da esquerda para a direita (borda suave) + leve zoom, sincronizada com o impacto
    p = ease((t - 0.2) / 0.75)
    if p > 0:
        s = 1.05 - 0.05 * ease((t - 0.2) / 1.1)
        L = lg.resize((int(lg.width * s), int(lg.height * s)), Image.LANCZOS)
        G = glow.resize(L.size, Image.LANCZOS)
        x0 = np.arange(L.width)[None, :]
        edge = p * (L.width + 160) - 160
        m = np.clip((edge - x0) / 160 + 1, 0, 1)
        a = (np.array(L.split()[3], dtype=float) * m).astype(np.uint8)
        L.putalpha(Image.fromarray(a))
        gi = max(0.0, 1 - abs(t - 0.75) / 0.6) * 0.55  # brilho que acende e apaga junto com o impacto
        ga = (np.array(G.split()[3], dtype=float) * m * gi).astype(np.uint8); G.putalpha(Image.fromarray(ga))
        pos = ((W - L.width) // 2, CY - L.height // 2)
        im.alpha_composite(G, pos); im.alpha_composite(L, pos)
    n = nchars(t)
    d = ImageDraw.Draw(im)
    if n:
        d.text((tx, ty), TEXT[:n], font=f, fill=GOLD + (255,))
    if t >= CLICKS[0] - 0.3:
        typing = t <= CLICKS[-1] + 0.1
        if typing or int((t - CLICKS[-1]) / 0.45) % 2 == 1:
            cx = tx + d.textlength(TEXT[:n], font=f) + 6
            d.rectangle([cx, ty + 4, cx + 4, ty + 60], fill=(240, 232, 220, 255))
    return im.convert("RGB")


out = sys.argv[1]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", os.path.join(HERE, "endcard", "sfx.wav"), "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for k in range(int(DUR * FPS)):
    p.stdin.write(frame(k / FPS).tobytes())
p.stdin.close(); p.wait()
