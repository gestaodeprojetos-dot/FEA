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


def larg(f, s, tr=0.0, esp=0.0):
    l, _, r, _ = f.getbbox(s)
    return (r - l) + tr * (len(s) - 1) + esp * s.count(' ')


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


def desenhar(d, x, y, s, f, cor, tr=0.0, ss=4, esp=0.0):
    """Escreve s com origem (x, y) do Pillow e tracking tr; devolve o x final (avanço).
    Com tracking, cada letra é posicionada em supersample (ss x) para não acumular
    arredondamento de pixel entre letras."""
    if abs(tr) < 0.05 and not esp:
        d.text((x, y), s, font=f, fill=cor)
        return x + f.getlength(s)
    img = d._image
    F = ImageFont.truetype(f.path, f.size * ss)
    W = int(np.ceil(f.getlength(s) + abs(tr) * len(s) + f.size * 2 + 4)) * ss
    H = int(np.ceil(f.size * 3 + 4)) * ss
    cam = Image.new('L', (W, H), 0)
    dc = ImageDraw.Draw(cam)
    O = int(np.ceil(f.size))
    ox, oy = O * ss, O * ss
    for i, ch in enumerate(s):
        dc.text((ox + F.getlength(s[:i]) + tr * ss * i + esp * ss * s[:i].count(' '), oy), ch, font=F, fill=255)
    # desloca a camada para que a origem caia na posição fracionária exata
    fx, fy = x - int(np.floor(x)), y - int(np.floor(y))
    cam = cam.transform(cam.size, Image.AFFINE, (1, 0, -fx * ss, 0, 1, -fy * ss), resample=Image.BILINEAR)
    small = cam.resize((W // ss, H // ss), Image.LANCZOS)
    px, py = int(np.floor(x)) - O, int(np.floor(y)) - O
    if img.mode == 'L':
        alvo = Image.new('L', small.size, cor if isinstance(cor, int) else cor[0])
    else:
        alvo = Image.new(img.mode, small.size, cor)
    img.paste(alvo, (int(px), int(py)), small)
    return x + f.getlength(s) + tr * len(s) + esp * s.count(' ')


def linha(im, segs, f, tr, y_topo, ref, x0=None, x1=None, alinh='esquerda', mascara_out=None, esp=0.0):
    """segs = [(texto, cor)] numa linha. y_topo = topo medido da linha original cujo texto é ref
    (mantém a linha de base). Alinhamento à esquerda em x0, centro entre x0 e x1 ou direita em x1."""
    d = ImageDraw.Draw(im if mascara_out is None else mascara_out)
    s = ''.join(t for t, _ in segs)
    y = y_topo - f.getbbox(ref)[1]
    w = larg(f, s, tr, esp)
    l = f.getbbox(s)[0]
    if alinh == 'esquerda':
        x = x0 - l
    elif alinh == 'direita':
        x = x1 - w - l
    else:
        x = (x0 + x1) / 2 - w / 2 - l
    for t, cor in segs:
        x = desenhar(d, x, y, t, f, cor, tr, esp=esp)
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


def faixas(f, s, tr, h):
    """Colunas com tinta na faixa superior de altura h (palavra gigante cortada pela borda).
    Devolve (segmentos x relativos à origem, topo da tinta relativo à origem)."""
    c = Image.new('L', (int(f.getlength(s) + abs(tr) * len(s) + 400), int(f.size * 2) + 200), 0)
    desenhar(ImageDraw.Draw(c), 100, 100, s, f, 255, tr)
    a = np.array(c) > 128
    top = np.where(a.any(1))[0].min()
    a = a[top:top + h]
    out, ini = [], None
    for i, v in enumerate(list(a.any(0)) + [False]):
        if v and ini is None:
            ini = i
        if not v and ini is not None:
            out.append((ini - 100, i - 1 - 100))
            ini = None
    return out, top - 100


def ajustar_gigante(caminho, texto, segs_orig, h, tamanhos, trs):
    """Corpo e tracking que reproduzem as colunas da faixa visível do original."""
    melhor = None
    for t in tamanhos:
        f = ImageFont.truetype(caminho, float(t))
        for tr in trs:
            s, _ = faixas(f, texto, tr, h)
            n = min(len(s), len(segs_orig))
            x0 = segs_orig[0][0] - s[0][0]
            custo = sum(abs(s[i][0] + x0 - segs_orig[i][0]) + abs(s[i][1] + x0 - segs_orig[i][1]) for i in range(n))
            custo += 200 * max(0, len(segs_orig) - len(s))
            if melhor is None or custo < melhor[0]:
                melhor = (custo, float(t), float(tr), x0)
    return melhor


def altura_x(im, caixa, cond):
    """Altura-x medida: da linha onde a tinta das minúsculas começa (topo do x) até a base,
    pelas transições do histograma de linhas."""
    m = mascara(im, caixa, cond)
    cont = m.sum(1)
    lim = 0.45 * cont.max()
    ys = np.where(cont >= lim)[0]
    return ys.max() - ys.min() + 1, ys.min() + caixa[1], ys.max() + caixa[1]


def ajustar_x(caminho, texto, xh, largura, ref='xuvwz'):
    """Corpo pela altura-x medida e tracking pela largura total da linha."""
    lo, hi = 4.0, 600.0
    while hi - lo > 0.1:
        t = (lo + hi) / 2
        _, a, _, b = ImageFont.truetype(caminho, t).getbbox(ref)
        lo, hi = (t, hi) if (b - a) < xh else (lo, t)
    f = ImageFont.truetype(caminho, round((lo + hi) / 2 * 4) / 4)
    tr = (largura - larg(f, texto)) / max(1, len(texto) - 1)
    return f, tr
