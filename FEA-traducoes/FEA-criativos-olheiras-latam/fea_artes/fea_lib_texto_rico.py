"""Complemento da fea_arte_lib para linhas com vários estilos (cor, peso, itálico, risco).

Usado pelos criativos jpg [FEED]/[STORIES] ADS 10 a 13 (fundo preto ou foto escura).
Tudo é desenhado na linha de base (anchor 'ls'), recalculada a partir do topo medido
da linha em português, para manter a mesma posição vertical do original.
"""
from PIL import ImageDraw, ImageFont
from fea_arte_lib import fonte, calibrar


def F(nome, tam):
    return ImageFont.truetype(fonte(nome), float(tam))


def base_de(f, texto_pt, y_topo):
    """Linha de base que faz o texto PT ter o topo medido em y_topo."""
    return y_topo - f.getbbox(texto_pt, anchor='ls')[1]


def largura_spans(spans):
    return sum(f.getlength(t) for t, f, *_ in spans)


def caixa_spans(spans, x, base):
    """bbox real (x0, y0, x1, y1) dos spans desenhados a partir de x na linha de base."""
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    cx = x
    for t, f, *_ in spans:
        l, tp, r, bt = f.getbbox(t, anchor='ls')
        if t.strip():
            x0, x1 = min(x0, cx + l), max(x1, cx + r)
            y0, y1 = min(y0, base + tp), max(y1, base + bt)
        cx += f.getlength(t)
    return x0, y0, x1, y1


def desenhar_spans(im, spans, base, centro=None, x_esq=None):
    """spans: [(texto, fonte, cor, cor_risco_ou_None)]. Centraliza pela tinta (bbox real)
    em `centro`, ou começa a tinta em `x_esq`. Retorna a bbox desenhada."""
    d = ImageDraw.Draw(im)
    x0, _, x1, _ = caixa_spans(spans, 0, base)
    x = (centro - (x0 + x1) / 2) if centro is not None else (x_esq - x0)
    cx = x
    for sp in spans:
        t, f, cor = sp[:3]
        risco = sp[3] if len(sp) > 3 else None
        d.text((cx, base), t, font=f, fill=cor, anchor='ls')
        if risco:
            l, tp, r, _ = f.getbbox(t.rstrip(), anchor='ls')
            # mesmo risco do original: altura ~ meio da altura-x, espessura ~ size/14
            hx = -f.getbbox('x', anchor='ls')[1]
            ym = base - hx * 0.5
            d.line([(cx + l - 1, ym), (cx + r + 1, ym)], fill=risco, width=max(2, round(f.size / 14)))
        cx += f.getlength(t)
    return caixa_spans(spans, x, base)
