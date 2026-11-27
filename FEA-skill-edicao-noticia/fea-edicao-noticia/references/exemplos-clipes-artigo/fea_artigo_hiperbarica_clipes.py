#!/usr/bin/env python3
"""FEA: clipes do vídeo da câmara hiperbárica (artigo Lopes et al., Case Rep Ophthalmol Med 2019, CC BY).
Fotos de câmara: Wikimedia Commons (CC BY / CC BY-SA, crédito no SKILL.md). Necrose: banco de inserts da equipe.
Uso: python3 fea_artigo_hiperbarica_clipes.py SCRATCHPAD FFMPEG"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
S, F = sys.argv[1], sys.argv[2]
H = f"{S}/dl/hiper/hi"; O = f"{S}/prod/hiper"; os.makedirs(f"{O}/clips", exist_ok=True)
W, PH = 1080, 1000
def page(n): return Image.open(f"{H}/p-{n}.png").convert("RGB")
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
def zoom(nome, im, dur):
    im.save(f"{O}/{nome}.png")
    ff("-loop", "1", "-i", f"{O}/{nome}.png", "-t", str(dur), "-vf",
       f"fps=30,scale=2332:2160,zoompan=z='1.0+0.06*on/{dur*30}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{PH}:fps=30,format=yuv420p",
       "-c:v", "libx264", "-crf", "16", f"{O}/clips/{nome}.mp4")
def cheia(nome, arq, dur=6, cx=0.5, cy=0.5):
    """Foto preenchendo o painel (recorte centrado em cx, cy)."""
    im = Image.open(arq).convert("RGB"); w, h = int(W * 1.08), int(PH * 1.08)
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    x = int(max(0, min(im.width - w, cx * im.width - w / 2))); y = int(max(0, min(im.height - h, cy * im.height - h / 2)))
    zoom(nome, im.crop((x, y, x + w, y + h)), dur)
def inteira(nome, im, dur=6):
    s = min(W * 1.08 * 0.96 / im.width, PH * 1.08 * 0.96 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    tela = Image.new("RGB", (int(W * 1.08), int(PH * 1.08)), "white")
    tela.paste(im, ((tela.width - im.width) // 2, (tela.height - im.height) // 2)); zoom(nome, tela, dur)
CM, IC = f"{S}/dl/hiper/cm", f"{S}/dl/interc"
cheia("v_paciente_camara", f"{CM}/c2.jpg", 5, 0.62, 0.5)       # paciente deitada na câmara monoplace
cheia("v_camaras", f"{CM}/c4.jpg", 5, 0.55, 0.5)              # câmaras monoplace fechadas
cheia("v_multiplace", f"{CM}/c3.jpg", 5)                      # câmara multiplace por dentro
cheia("v_multiplace2", f"{CM}/c5.jpg", 5, 0.45)
cheia("v_controle", f"{CM}/c8.jpg", 5, 0.62)
cheia("v_nec1", f"{IC}/384582cc-36fa-4bd8-8bd9-16620c56cc57.jpg", 5, 0.5, 0.55)
inteira("v_nec2", Image.open(f"{IC}/09979e81-191c-44cc-91f0-434ea7d52125.jpg").convert("RGB"), 5)
cheia("v_nec3", f"{IC}/bbeafc0e-70c4-49a3-a24d-867eee5520fe.jpg", 5, 0.5, 0.42)
cheia("v_nec4", f"{IC}/8b463efb-f6aa-4e7b-b8eb-c1d50456f2c1.jpg", 5, 0.5, 0.33)
cheia("v_nec5", f"{IC}/cafef188-b1f6-47a9-8006-550e53202c67.jpg", 5, 0.5, 0.42)
p1, p2, p3 = page(1), page(2), page(3)
scroll("s_titulo", p1.crop((100, 150, 1720, 1700)), 150, 330, 5)
r = realce(p2, [(935, 598, 1690, 720)]).crop((925, 300, 1700, 1300))
scroll("s_protocolo", r, 0, 160, 7)
inteira("v_graficos", p3.crop((120, 330, 1700, 1180)), 5)
r = realce(p3, [(940, 1165, 1690, 1251)]).crop((925, 900, 1700, 1900))
scroll("s_melhora", r, 0, 200, 7)
# resumo com a conclusão (oclusão da artéria da retina, perda de visão) em destaque
r = realce(p1, [(255, 1458, 1690, 1570)]).crop((240, 600, 1700, 2300))
scroll("s_resumo", r, 60, 250, 7)
