#!/usr/bin/env python3
"""FEA: funções para os clipes de vídeo de artigo (painel de cima, 1080x1000).

Uso em um script do vídeo (ver references/exemplos-clipes-artigo):

    import fea_artigo_lib as A
    A.configurar(ffmpeg="ffmpeg", saida="trabalho/prod/artigo1")
    p1 = A.pagina("trabalho/dl/artigo1/hi/p-01.png")           # pdftoppm -r 220 -png artigo.pdf p
    A.scroll("s_titulo", p1.crop((100, 150, 1720, 1700)), 150, 330, 5)
    r = A.realce(p1, [(255, 1458, 1690, 1570)])                 # destaque roxo (coordenadas a 220 dpi)
    A.scroll("s_resumo", r.crop((240, 600, 1700, 2300)), 60, 250, 7)
    A.inteira("v_fig1", p2.crop((...)), 6)                       # figura inteira, fundo branco
    A.cheia("v_foto", "foto.jpg", 5, cx=0.5, cy=0.4)             # foto preenchendo o painel
    A.faixa("f_painel", p2.crop((...)), 5)                       # figura A|B|C deslizando

Coordenadas do destaque: pdftotext -bbox-layout artigo.pdf saida.html (pontos x 220/72).
Regras: o clipe de rolagem precisa durar MAIS que a cena (senão reinicia); a imagem recortada
precisa ter pelo menos 1000 px de altura depois de redimensionada para 1080 de largura.
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter

W, PH = 1080, 1000
ROXO = (91, 69, 153)
_cfg = {"ffmpeg": "ffmpeg", "saida": "."}


def configurar(ffmpeg="ffmpeg", saida="."):
    _cfg.update(ffmpeg=ffmpeg, saida=saida)
    os.makedirs(os.path.join(saida, "clips"), exist_ok=True)


def _ff(*a):
    subprocess.run([_cfg["ffmpeg"], "-y", "-v", "error", *a], check=True)


def _o(nome, ext):
    return os.path.join(_cfg["saida"], "clips" if ext == "mp4" else "", f"{nome}.{ext}")


def pagina(arq):
    return Image.open(arq).convert("RGB")


def realce(im, caixas):
    """Caixas roxas translúcidas sobre os trechos que o Dr. comenta."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for b in caixas:
        d.rounded_rectangle(b, 8, fill=ROXO + (60,), outline=ROXO + (230,), width=4)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")


def scroll(nome, im, y0, y1, dur):
    """Página rolando suave de y0 até y1 (px depois de redimensionar para 1080 de largura)."""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if im.height < PH:
        raise ValueError(f"{nome}: recorte baixo demais ({im.height}px < {PH}px), aumente a altura")
    im.save(_o(nome, "png"))
    ymax = im.height - PH
    y0, y1 = min(y0, ymax), min(y1, ymax)
    _ff("-loop", "1", "-i", _o(nome, "png"), "-t", str(dur), "-vf",
        f"fps=30,crop={W}:{PH}:0:'{y0}+({y1}-{y0})*(1-cos(PI*min(t/{dur},1)))/2',format=yuv420p",
        "-c:v", "libx264", "-crf", "16", _o(nome, "mp4"))


def _zoom(nome, im, dur):
    im.save(_o(nome, "png"))
    _ff("-loop", "1", "-i", _o(nome, "png"), "-t", str(dur), "-vf",
        f"fps=30,scale=2332:2160,zoompan=z='1.0+0.06*on/{dur * 30}':x='iw/2-iw/zoom/2':"
        f"y='ih/2-ih/zoom/2':d=1:s={W}x{PH}:fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", _o(nome, "mp4"))


def inteira(nome, im, dur=6, fundo="white"):
    """Figura inteira (sem cortar) centralizada em fundo branco, zoom lento."""
    s = min(W * 1.08 * 0.96 / im.width, PH * 1.08 * 0.96 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    tela = Image.new("RGB", (int(W * 1.08), int(PH * 1.08)), fundo)
    tela.paste(im, ((tela.width - im.width) // 2, (tela.height - im.height) // 2))
    _zoom(nome, tela, dur)


def cheia(nome, arq, dur=6, cx=0.5, cy=0.5):
    """Foto preenchendo o painel, recorte centrado em (cx, cy), zoom lento."""
    im = Image.open(arq).convert("RGB")
    w, h = int(W * 1.08), int(PH * 1.08)
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    x = int(max(0, min(im.width - w, cx * im.width - w / 2)))
    y = int(max(0, min(im.height - h, cy * im.height - h / 2)))
    _zoom(nome, im.crop((x, y, x + w, y + h)), dur)


def faixa(nome, im, dur=5):
    """Figura larga (painéis A, B, C lado a lado) na altura do painel, deslizando da esquerda para a direita."""
    s = PH / im.height
    im = im.resize((round(im.width * s), PH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im.save(_o(nome, "png"))
    x1 = im.width - W
    _ff("-loop", "1", "-i", _o(nome, "png"), "-t", str(dur), "-vf",
        f"fps=30,crop={W}:{PH}:'{x1}*(1-cos(PI*min(t/{dur},1)))/2':0,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", _o(nome, "mp4"))


def video_baixo(nome, arq, ini, dur, cx, cy, frac=0.86):
    """Vídeo de baixa resolução (ex.: 464x832) vira clipe 1080x1000 já recortado.
    frac = largura da janela em relação ao vídeo. Renomear antes arquivos com acento vindos do Drive."""
    _ff("-ss", str(ini), "-t", str(dur), "-i", arq, "-an", "-vf",
        f"crop='iw*{frac}':'iw*{frac}*{PH}/{W}':'(iw-iw*{frac})*{cx}':'ih*{cy}-iw*{frac}*{PH}/{W}/2',"
        f"scale={W}:{PH}:flags=lanczos,unsharp=5:5:0.6,fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", _o(nome, "mp4"))
