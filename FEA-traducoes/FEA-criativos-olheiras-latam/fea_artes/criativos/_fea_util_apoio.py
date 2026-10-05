"""Utilidades do lote de artes de apoio do Ebook Olheiras (checkout, pop-up, banner,
capa de módulo, avatar). Complementa fea_arte_lib com: espaçamento entre letras
(tracking), texto em vários segmentos de cor na mesma linha e preenchimento com
textura (dourado) reaproveitada do próprio original. Sem IA generativa."""
import os, sys
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
os.chdir(AQUI)
from fea_arte_lib import *  # noqa
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

T = 'trabalho/apoio-'


def larg(f, s, tr=0.0):
    l, _, r, _ = f.getbbox(s)
    return (r - l) + tr * (len(s) - 1)


def ajustar(caminho, texto, alt, largura):
    """Tamanho pela altura medida da linha (topo a base da tinta) e tracking pela largura."""
    lo, hi = 4.0, 600.0
    while hi - lo > 0.1:  # altura cresce com o corpo: bisseção
        t = (lo + hi) / 2
        _, a, _, b = ImageFont.truetype(caminho, t).getbbox(texto)
        lo, hi = (t, hi) if (b - a) < alt else (lo, t)
    f = ImageFont.truetype(caminho, round((lo + hi) / 2 * 4) / 4)
    tr = (largura - larg(f, texto)) / max(1, len(texto) - 1)
    return f, tr


def desenhar(d, x, y, s, f, cor, tr=0.0):
    """Escreve s com origem (x, y) do Pillow e tracking tr; devolve o x final (avanço)."""
    if abs(tr) < 0.05:
        d.text((x, y), s, font=f, fill=cor)
        return x + f.getlength(s)
    for i, ch in enumerate(s):
        d.text((x + f.getlength(s[:i]) + tr * i, y), ch, font=f, fill=cor)
    return x + f.getlength(s) + tr * len(s)


def linha(im, segs, f, tr, y_topo, ref, x0=None, x1=None, alinh='esquerda', mascara_out=None):
    """segs = [(texto, cor)] numa linha. y_topo = topo medido da linha original cujo texto é ref
    (mantém a linha de base). Alinhamento à esquerda em x0, centro entre x0 e x1 ou direita em x1."""
    d = ImageDraw.Draw(im if mascara_out is None else mascara_out)
    s = ''.join(t for t, _ in segs)
    y = y_topo - f.getbbox(ref)[1]
    w = larg(f, s, tr)
    l = f.getbbox(s)[0]
    if alinh == 'esquerda':
        x = x0 - l
    elif alinh == 'direita':
        x = x1 - w - l
    else:
        x = (x0 + x1) / 2 - w / 2 - l
    for t, cor in segs:
        x = desenhar(d, x, y, t, f, cor, tr)
    return w


def campo_textura(im, caixa, cond, raio=15):
    """Campo contínuo de cor a partir dos pixels de texto (ex.: dourado com textura):
    os pixels que não são texto são preenchidos por inpainting clássico."""
    x0, y0, x1, y1 = caixa
    sub = np.array(im)[y0:y1, x0:x1].copy()
    m = mascara(im, caixa, cond)
    m = cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8))
    buraco = (m == 0).astype(np.uint8) * 255
    out = cv2.inpaint(cv2.cvtColor(sub, cv2.COLOR_RGB2BGR), buraco, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def colar_textura(im, mascara_L, textura, caixa):
    """Aplica a textura (do tamanho da caixa) onde a máscara L (tamanho da imagem) tem texto."""
    x0, y0, x1, y1 = caixa
    camada = Image.new('RGB', im.size)
    camada.paste(textura, (x0, y0))
    im.paste(camada, (0, 0), mascara_L)
    return im
