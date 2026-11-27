#!/usr/bin/env python3
"""FEA: clipes do artigo de padrões de contração (Lima et al., Surg Cosmet Dermatol 2022, CC BY).
Uso: python3 fea_artigo_forca_clipes.py SCRATCHPAD FFMPEG"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
S, F = sys.argv[1], sys.argv[2]
H = f"{S}/dl/forca/hi"; O = f"{S}/prod/forca"; os.makedirs(f"{O}/clips", exist_ok=True)
W, PH = 1080, 1000
def page(n): return Image.open(f"{H}/p-{n:02d}.png").convert("RGB")
def ff(*a): subprocess.run([F, "-y", "-v", "error", *a], check=True)
def realce(im, boxes):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for b in boxes: d.rounded_rectangle(b, 8, fill=(91, 69, 153, 60), outline=(91, 69, 153, 230), width=4)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
def scroll(nome, im, y0, y1, dur):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); im.save(f"{O}/{nome}.png")
    ymax = max(0, im.height - PH); y0, y1 = min(y0, ymax), min(y1, ymax)
    ff("-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
       f"fps=30,crop={W}:{PH}:0:'{y0}+({y1}-{y0})*(1-cos(PI*min(t/{dur},1)))/2',format=yuv420p",
       "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4")
def foto(nome, im, dur=6):
    """Figura inteira centralizada em fundo branco, zoom lento."""
    s = min(W * 1.08 * 0.96 / im.width, PH * 1.08 * 0.96 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    tela = Image.new("RGB", (int(W * 1.08), int(PH * 1.08)), "white")
    tela.paste(im, ((tela.width - im.width) // 2, (tela.height - im.height) // 2)); tela.save(f"{O}/{nome}.png")
    ff("-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
       f"fps=30,scale=2332:2160,zoompan=z='1.0+0.06*on/{dur*30}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{PH}:fps=30,format=yuv420p",
       "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4")
def faixa(nome, im, dur=5):
    """Faixa larga de painéis (A, B, C) na altura do painel, deslizando da esquerda para a direita."""
    s = PH / im.height
    im = im.resize((round(im.width * s), PH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2)); im.save(f"{O}/{nome}.png")
    x1 = im.width - W
    ff("-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
       f"fps=30,crop={W}:{PH}:'{x1}*(1-cos(PI*min(t/{dur},1)))/2':0,format=yuv420p",
       "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4")
p2, p3, p4 = page(2), page(3), page(4)
foto("v_glabela_clin", p4.crop((99, 1170, 1430, 2314)), 4)          # Fig. 7: 6 padrões glabelares (clínico)
faixa("f_periocular_clin", p4.crop((99, 619, 1703, 1045)), 5)      # Fig. 6
faixa("f_frontal_clin", p4.crop((99, 255, 1703, 515)), 4)           # Fig. 5
faixa("f_frontal", p2.crop((99, 1027, 1716, 1573)), 5)             # Fig. 1 (ilustração)
faixa("f_glabela", p3.crop((99, 884, 1716, 1495)), 5)              # Fig. 4
faixa("f_periorbital", p2.crop((99, 1617, 1716, 2158)), 4)         # Fig. 2
p1 = page(1)
scroll("s_titulo", p1.crop((100, 250, 1280, 1500)), 0, 120, 5)
r = realce(p1, [(120, 1210, 1262, 1282), (120, 1395, 1262, 1466)]).crop((100, 250, 1280, 1500))
scroll("s_resumo", r, 250, 400, 7)
