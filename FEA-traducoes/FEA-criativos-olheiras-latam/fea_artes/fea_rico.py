"""Complemento da fea_arte_lib para o lote [FEED]/[STORIES] ADS 06 a 09 (jpg).

Texto rico numa linha (trechos com fonte, cor e sublinhado diferentes, como
'Com um ebook que mostra **o raciocínio clínico**'), espaçamento entre letras
(tracking) e texto em arco (selo dourado). Tudo desenhado com Pillow, sem IA.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fea_arte_lib import fonte, mascara

_cache = {}


def F(nome, tamanho):
    k = (nome, round(tamanho * 4) / 4)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(fonte(nome), k[1])
    return _cache[k]


def larg(texto, nome, tamanho, tracking=0.0):
    f = F(nome, tamanho)
    if not texto:
        return 0.0
    return f.getlength(texto) + tracking * (len(texto) - 1)


def largura_segs(segs, tamanho, tracking=0.0):
    """segs: [(texto, nome_fonte, cor, sublinhado)]. Largura total da linha."""
    tot = 0.0
    for i, (t, n, _, _) in enumerate(segs):
        tot += larg(t, n, tamanho, tracking)
        if i < len(segs) - 1:
            tot += tracking
    return tot


def tinta(segs, tamanho, tracking=0.0):
    """(esquerda, direita) da tinta real em relação à origem da linha."""
    l = F(segs[0][1], tamanho).getbbox(segs[0][0][0], anchor='ls')[0]
    ult = segs[-1]
    r_ult = F(ult[1], tamanho).getbbox(ult[0][-1], anchor='ls')[2] - F(ult[1], tamanho).getlength(ult[0][-1])
    return l, largura_segs(segs, tamanho, tracking) + r_ult


def desenhar(im, segs, tamanho, base, x0, x1=None, alinh='centro', tracking=0.0,
             sub_desc=None, sub_esp=None):
    """Desenha a linha com linha de base 'base'. alinh centro usa (x0+x1)/2, esquerda usa x0
    como borda da tinta, direita usa x1. Retorna (x_tinta_ini, x_tinta_fim)."""
    d = ImageDraw.Draw(im)
    l, r = tinta(segs, tamanho, tracking)
    if alinh == 'esquerda':
        x = x0 - l
    elif alinh == 'direita':
        x = x1 - r
    else:
        x = (x0 + x1) / 2 - (r + l) / 2
    ini = x + l
    sub_desc = tamanho * 0.11 if sub_desc is None else sub_desc
    sub_esp = max(1, round(tamanho * 0.06)) if sub_esp is None else sub_esp
    for i, (t, n, cor, sub) in enumerate(segs):
        f = F(n, tamanho)
        xs = x
        if tracking:
            for ch in t:
                d.text((x, base), ch, font=f, fill=cor, anchor='ls')
                x += f.getlength(ch) + tracking
            x -= tracking
        else:
            d.text((x, base), t, font=f, fill=cor, anchor='ls')
            x += f.getlength(t)
        if sub:
            tt = t.rstrip()
            xe = xs + larg(tt, n, tamanho, tracking)
            xb = xs + (f.getbbox(t[0], anchor='ls')[0] if t[0] != ' ' else f.getlength(' '))
            d.rectangle([xb, base + sub_desc, xe, base + sub_desc + sub_esp - 1], fill=cor)
        if i < len(segs) - 1:
            x += tracking
    return ini, x + r - largura_segs(segs, tamanho, tracking)


def base_de(ytop, texto_pt, nome, tamanho):
    """Linha de base a partir do topo medido da linha original (mesmo método de escrever())."""
    return ytop - F(nome, tamanho).getbbox(texto_pt, anchor='ls')[1]


def tamanho_por_largura(texto, nome, largura, tracking=0.0):
    melhor = None
    for t in np.arange(8, 200, 0.25):
        f = F(nome, float(t))
        l = f.getbbox(texto[0], anchor='ls')[0]
        r = f.getlength(texto[:-1]) + f.getbbox(texto[-1], anchor='ls')[2] + tracking * (len(texto) - 1)
        w = r - l
        if melhor is None or abs(w - largura) < abs(melhor[1] - largura):
            melhor = (float(t), w)
    return melhor[0]


def tamanho_segs(segs, largura, tracking=0.0):
    melhor = None
    for t in np.arange(8, 200, 0.25):
        l, r = tinta(segs, float(t), tracking)
        if melhor is None or abs((r - l) - largura) < abs(melhor[1] - largura):
            melhor = (float(t), r - l)
    return melhor[0]


def comparar(im, caixa, cond, texto, nomes, tracking=0.0):
    """Nota de semelhança (IoU) do recorte com cada fonte candidata, já no tamanho calibrado."""
    m = mascara(im, caixa, cond)
    ys, xs = np.where(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    out = []
    for n in nomes:
        t = tamanho_por_largura(texto, n, m.shape[1], tracking)
        c = Image.new('L', (m.shape[1] + 400, m.shape[0] + 200), 0)
        segs = [(texto, n, 255, False)]
        desenhar(c, segs, t, 150, 100, alinh='esquerda', tracking=tracking)
        a = np.array(c) > 110
        yy, xx = np.where(a)
        a = a[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
        a = np.array(Image.fromarray(a.astype(np.uint8) * 255).resize((m.shape[1], m.shape[0]))) > 127
        iou = (a & m).sum() / max(1, (a | m).sum())
        out.append((round(float(iou), 3), n, t, a.shape, m.shape))
    return sorted(out, reverse=True)


def texto_arco(im, texto, nome, tamanho, cor, centro, raio, ang_centro=-90.0, tracking=0.0,
               por_fora=True, sombra=None):
    """Texto ao longo de um arco. raio = raio da linha de base. ang_centro em graus (−90 = topo).
    por_fora=True: letras de pé, lidas no sentido horário (arco superior).
    por_fora=False: arco inferior, lido da esquerda para a direita, letras com o pé para fora."""
    f = F(nome, tamanho)
    larguras = [f.getlength(ch) for ch in texto]
    total = sum(larguras) + tracking * (len(texto) - 1)
    cx, cy = centro
    s = -total / 2
    for ch, w in zip(texto, larguras):
        meio = s + w / 2
        if por_fora:
            ang = ang_centro + math.degrees(meio / raio)
        else:
            ang = ang_centro - math.degrees(meio / raio)
        rad = math.radians(ang)
        px, py = cx + raio * math.cos(rad), cy + raio * math.sin(rad)
        if ch.strip():
            tam = int(tamanho * 3)
            cam = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
            dc = ImageDraw.Draw(cam)
            if sombra:
                dc.text((tam / 2 + sombra[1][0], tam / 2 + sombra[1][1]), ch, font=f, fill=tuple(sombra[0]) + (255,), anchor='ms')
            dc.text((tam / 2, tam / 2), ch, font=f, fill=tuple(cor) + (255,), anchor='ms')
            rot = ang + 90 if por_fora else ang - 90
            r = cam.rotate(-rot, resample=Image.BICUBIC, center=(tam / 2, tam / 2))
            im.paste(r, (int(round(px - tam / 2)), int(round(py - tam / 2))), r)
        s += w + tracking
    return im
