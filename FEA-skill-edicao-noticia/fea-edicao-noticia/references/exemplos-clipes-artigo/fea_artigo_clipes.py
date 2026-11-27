#!/usr/bin/env python3
"""FEA: clipes do artigo (página rolando com destaque roxo e fotos com zoom lento) para o painel do modelo notícia. Uso: python3 fea_artigo_clipes.py SCRATCHPAD FFMPEG"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFilter
S, F = sys.argv[1], sys.argv[2]
H = f"{S}/dl/bio/hi"; O = f"{S}/prod/nod"
W, PH = 1080, 1000
def page(n): return Image.open(f"{H}/p-{n}.png").convert("RGB")
def realce(im, boxes):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for b in boxes: d.rounded_rectangle(b, 8, fill=(91, 69, 153, 60), outline=(91, 69, 153, 230), width=4)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
def scroll(nome, im, y0, y1, dur):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f"{O}/{nome}.png")
    ymax = im.height - PH; y0, y1 = min(y0, ymax), min(y1, ymax)
    subprocess.run([F, "-y", "-v", "error", "-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
        f"fps=30,crop={W}:{PH}:0:'{y0}+({y1}-{y0})*(1-cos(PI*min(t/{dur},1)))/2',format=yuv420p",
        "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4"], check=True)
def foto(nome, arq, cy=0.5, dur=6):
    im = Image.open(f"{O}/{arq}").convert("RGB")
    s = max(W / im.width, PH / im.height) * 1.08
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 70, 2))
    y = int(max(0, min(im.height - PH * 1.08, cy * im.height - PH * 0.54)))
    im = im.crop((0, y, im.width, y + int(PH * 1.08))); x = (im.width - int(W * 1.08)) // 2
    im = im.crop((x, 0, x + int(W * 1.08), im.height)); im.save(f"{O}/{nome}.png")
    subprocess.run([F, "-y", "-v", "error", "-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
        f"fps=30,scale=2332:2160,zoompan=z='1.0+0.06*on/{dur*30}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{PH}:fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4"], check=True)
# fotos (sem o "(A)" do canto)
for k in ["f1a", "f2a", "f3a", "f4a"]:
    im = Image.open(f"{O}/{k}.png"); im.crop((0, 45, im.width, im.height)).save(f"{O}/{k}c.png")
foto("v_f1a", "f1ac.png", 0.45); foto("v_f2a", "f2ac.png", 0.35); foto("v_f3a", "f3ac.png", 0.5); foto("v_f4a", "f4ac.png", 0.4)
im = Image.open(f"{O}/f1b.png").convert("RGB"); foto("v_f1b", "f1b.png", 0.5)
# página 1: título e resumo
p1 = page(1).crop((60, 0, 1760, 2391))
scroll("s_titulo", p1, 0, 330, 4); scroll("s_resumo", p1, 320, 700, 4)
# tabela 1 (coluna esquerda da p. 3), com nódulos em destaque
p3 = page(3)
tab = realce(p3, [(140, 640, 890, 690), (140, 300, 890, 390)]).crop((110, 120, 900, 1470))
scroll("s_tabela", tab, 0, 700, 11)
# discussão: "excess product, lack of massage ... trapping"
dis = realce(p3, [(925, 2008, 1705, 2082), (925, 2163, 1705, 2245)]).crop((910, 1480, 1720, 2330))
scroll("s_discussao", dis, 0, 380, 9)
