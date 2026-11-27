#!/usr/bin/env python3
"""Cartão de foto para o painel (1080x1000): fundo = a própria foto desfocada; foto(s) com borda branca e sombra."""
import sys, json, subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
W, H = 1080, 1000
def cartao(fotos, centros, altura, saida):
    base = Image.open(fotos[0]).convert("RGB")
    s = max(W / base.width, H / base.height)
    bg = base.resize((int(base.width * s) + 2, int(base.height * s) + 2), Image.LANCZOS).crop((0, 0, W, H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.75)
    bg = Image.blend(bg, Image.new("RGB", (W, H), (208, 209, 233)), 0.25).convert("RGBA")
    for f, (cx, cy) in zip(fotos, centros):
        im = Image.open(f).convert("RGB")
        im = im.resize((int(im.width * altura / im.height), altura), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        b = 10
        card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (255, 255, 255, 255))
        card.paste(im, (b, b))
        m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], 14, fill=255)
        card.putalpha(m)
        sh = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0))
        sh.paste((0, 0, 0, 110), (40, 50, 40 + card.width, 50 + card.height), m)
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        x, y = int(cx - card.width / 2), int(cy - card.height / 2)
        bg.alpha_composite(sh, (x - 40, y - 40)); bg.alpha_composite(card, (x, y))
    bg.convert("RGB").save(saida)
if __name__ == "__main__":
    a = json.loads(sys.argv[1]); cartao(a["fotos"], a["centros"], a["altura"], a["saida"])
