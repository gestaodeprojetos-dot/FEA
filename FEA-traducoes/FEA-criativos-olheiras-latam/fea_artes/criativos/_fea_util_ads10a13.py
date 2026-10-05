"""Módulo de apoio (não gera arte sozinho) dos criativos jpg ADS 10 a 13.
Complemento da fea_arte_lib para linhas com vários estilos (cor, peso, itálico, risco, entreletra).

Usado pelos criativos jpg [FEED]/[STORIES] ADS 10 a 13 (fundo preto ou foto escura).
Tudo é desenhado na linha de base (anchor 'ls'), recalculada a partir do topo medido
da linha em português, para manter a mesma posição vertical do original.

span = (texto, fonte_PIL, cor[, cor_risco[, entreletra_px]])
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import ImageDraw, ImageFont
from fea_arte_lib import fonte


def F(nome, tam):
    return ImageFont.truetype(fonte(nome), float(tam))


def calib(nome, texto, largura):
    """Tamanho em que `texto` ocupa `largura` px de tinta (proporcional, 3 iterações)."""
    t = 40.0
    for _ in range(3):
        l, _, r, _ = F(nome, t).getbbox(texto)
        t = t * largura / (r - l)
    return F(nome, round(t * 4) / 4)


def por_altura_maiuscula(nome, altura_px):
    """Tamanho a partir da altura medida de uma maiúscula sem acento (ex.: o 'T')."""
    f = F(nome, 100)
    cap = -f.getbbox('H', anchor='ls')[1]
    return F(nome, round(100 * altura_px / cap * 4) / 4)


def entreletra(f, texto, largura):
    """Espaçamento extra por caractere para o texto ocupar `largura` px de tinta."""
    l, _, r, _ = f.getbbox(texto)
    return (largura - (r - l)) / max(1, len(texto) - 1)


def base_de(f, texto_pt, y_topo):
    """Linha de base que faz o texto PT ter o topo medido em y_topo."""
    return y_topo - f.getbbox(texto_pt, anchor='ls')[1]


def _avanco(t, f, tr):
    return f.getlength(t) + tr * len(t)


def caixa_spans(spans, x, base):
    """bbox de tinta (x0, y0, x1, y1) dos spans desenhados a partir de x na linha de base."""
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    cx = x
    for sp in spans:
        t, f = sp[0], sp[1]
        tr = sp[4] if len(sp) > 4 else 0
        if tr:
            for ch in t:
                if ch.strip():
                    l, tp, r, bt = f.getbbox(ch, anchor='ls')
                    x0, x1 = min(x0, cx + l), max(x1, cx + r)
                    y0, y1 = min(y0, base + tp), max(y1, base + bt)
                cx += f.getlength(ch) + tr
            continue
        if t.strip():
            l, tp, r, bt = f.getbbox(t, anchor='ls')
            ini = len(t) - len(t.lstrip())
            l = f.getbbox(t.lstrip(), anchor='ls')[0] + f.getlength(t[:ini])
            r = f.getlength(t.rstrip()) - f.getlength(t.rstrip()[-1]) + f.getbbox(t.rstrip()[-1], anchor='ls')[2]
            x0, x1 = min(x0, cx + l), max(x1, cx + r)
            y0, y1 = min(y0, base + tp), max(y1, base + bt)
        cx += f.getlength(t)
    return x0, y0, x1, y1


def largura_spans(spans):
    x0, _, x1, _ = caixa_spans(spans, 0, 0)
    return x1 - x0


def desenhar_spans(im, spans, base, centro=None, x_esq=None, cap_risco=0.5):
    """Centraliza pela tinta em `centro`, ou começa a tinta em `x_esq`. Retorna a bbox desenhada."""
    d = ImageDraw.Draw(im)
    x0, _, x1, _ = caixa_spans(spans, 0, base)
    x = (centro - (x0 + x1) / 2) if centro is not None else (x_esq - x0)
    cx = x
    for sp in spans:
        t, f, cor = sp[:3]
        risco = sp[3] if len(sp) > 3 else None
        tr = sp[4] if len(sp) > 4 else 0
        ini_x = cx
        if tr:
            for ch in t:
                d.text((cx, base), ch, font=f, fill=cor, anchor='ls')
                cx += f.getlength(ch) + tr
        else:
            d.text((cx, base), t, font=f, fill=cor, anchor='ls')
            cx += f.getlength(t)
        if risco:
            bx0, _, bx1, _ = caixa_spans([sp[:2] + (cor, None, tr)], ini_x, base)
            cap = -f.getbbox('H', anchor='ls')[1]
            ym = base - cap * cap_risco
            d.line([(bx0 - 1, ym), (bx1 + 1, ym)], fill=risco, width=max(2, round(f.size / 16)))
    return caixa_spans(spans, x, base)
