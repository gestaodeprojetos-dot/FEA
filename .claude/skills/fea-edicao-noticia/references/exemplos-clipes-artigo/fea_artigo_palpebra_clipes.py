#!/usr/bin/env python3
"""FEA: clipes do artigo de toxina na pálpebra inferior (Zhou et al., J Cosmet Dermatol 2025, CC BY).
Uso: python3 fea_artigo_palpebra_clipes.py SCRATCHPAD FFMPEG"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
S, F = sys.argv[1], sys.argv[2]
H = f"{S}/dl/palp/hi"; O = f"{S}/prod/palp"; os.makedirs(f"{O}/clips", exist_ok=True)
W, PH = 1080, 1000
def page(n): return Image.open(f"{H}/p-{n:02d}.png").convert("RGB")
def realce(im, boxes):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for b in boxes: d.rounded_rectangle(b, 8, fill=(91, 69, 153, 60), outline=(91, 69, 153, 230), width=4)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
def scroll(nome, im, y0, y1, dur):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f"{O}/{nome}.png")
    ymax = max(0, im.height - PH); y0, y1 = min(y0, ymax), min(y1, ymax)
    subprocess.run([F, "-y", "-v", "error", "-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
        f"fps=30,pad={W}:max(ih\\,{PH}):0:0:white,crop={W}:{PH}:0:'{y0}+({y1}-{y0})*(1-cos(PI*min(t/{dur},1)))/2',format=yuv420p",
        "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4"], check=True)
def foto(nome, arq, dur=6, fundo=(255, 255, 255)):
    """Figura inteira (sem cortar) centralizada no painel, fundo branco, zoom lento."""
    im = Image.open(f"{O}/{arq}").convert("RGB")
    s = min(W * 1.08 * 0.96 / im.width, PH * 1.08 * 0.96 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    tela = Image.new("RGB", (int(W * 1.08), int(PH * 1.08)), fundo)
    tela.paste(im, ((tela.width - im.width) // 2, (tela.height - im.height) // 2)); tela.save(f"{O}/{nome}.png")
    subprocess.run([F, "-y", "-v", "error", "-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
        f"fps=30,scale=2332:2160,zoompan=z='1.0+0.06*on/{dur*30}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{PH}:fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4"], check=True)
# fotos: olhos com rugas marcadas (fig. 5), antes/depois (fig. 4 e 6), pontos de aplicação (fig. 1)
foto("v_olhos", "fig5.png", 7); foto("v_ad1", "fig4.png", 7); foto("v_ad2", "fig6.png", 7); foto("v_pontos", "fig1.png", 11)
# página 1: título; resumo com "intradermal" e o único evento adverso (pseudo-bolsa) em destaque
p1 = page(1).crop((60, 0, 1760, 2391)); scroll("s_titulo", p1, 0, 330, 5)
r = realce(page(1), [(150, 1132, 1672, 1185), (150, 1408, 1668, 1500)]).crop((60, 0, 1760, 2391))
scroll("s_resumo", r, 400, 820, 12)
# p. 2: métodos (0,01 mL por ponto, 3 a 4 pontos intradérmicos, pápula)
m = realce(page(2), [(925, 405, 1690, 492), (925, 510, 1690, 562)]).crop((910, 60, 1720, 1100))
scroll("s_metodos", m, 0, 300, 12)
