#!/usr/bin/env python3
"""FEA: quadro com 2 fotos de antes e depois (etiquetas Antes/Depois, sem aviso: público técnico) para o painel do modelo notícia. Uso: python3 fea_antes_depois.py SCRATCHPAD"""
import sys
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageFont
W, H = 1080, 1000
S = sys.argv[1]; P = S + "/prod/k4"; fontes = S + "/fonts"
fotos = [(S + "/dl/k4/images.jfif", None), (S + "/dl/k4/eucerin-small-teaser-image-1-marionette-450x288.webp", (0, 18, 450, 270))]
ims = []
for f, c in fotos:
    im = Image.open(f).convert("RGB")
    if c: im = im.crop(c)
    ims.append(im)
bg = ims[0].resize((W, H)).filter(ImageFilter.GaussianBlur(40))
bg = Image.blend(ImageEnhance.Brightness(bg).enhance(0.75), Image.new("RGB", (W, H), (208, 209, 233)), 0.3).convert("RGBA")
ft = ImageFont.truetype(fontes + "/Sora-700.ttf", 30)
fp = ImageFont.truetype(fontes + "/Sora-700.ttf", 24) if False else ImageFont.truetype(fontes + "/Sora-700.ttf", 24)
def pill(txt, cor):
    l, t, r, b = ft.getbbox(txt); w, h = r - l + 36, 48
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=cor); d.text((18 - l, (h - (b - t)) / 2 - t), txt, font=ft, fill=(255, 255, 255, 255))
    return im
alt = 350; ys = [30, 410]
for im, y in zip(ims, ys):
    im = im.resize((int(im.width * alt / im.height), alt), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    b = 10
    card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (255, 255, 255, 255)); card.paste(im, (b, b))
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], 14, fill=255); card.putalpha(m)
    x = (W - card.width) // 2
    sh = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), (40, 50, 40 + card.width, 50 + card.height), m)
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40)); bg.alpha_composite(card, (x, y))
    a, d = pill("Antes", (60, 60, 60, 230)), pill("Depois", (91, 69, 153, 240))
    bg.alpha_composite(a, (x + 22, y + card.height - a.height - 18)); bg.alpha_composite(d, (x + card.width // 2 + 22, y + card.height - d.height - 18))
# sem aviso de "imagem ilustrativa": público técnico (Keila, 06/11/2026)
bg.convert("RGB").save(P + "/c_antesdepois.png")
