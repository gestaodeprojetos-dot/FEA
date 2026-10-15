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


# ---- logo dourado "PREENCHIMENTO / TRIDIMENSIONAL / DE OLHEIRAS" (ADS 11, 12 e 13) ----
# Medidas no [FEED] ADS 11 (dy=0): linha 1 'PREENCHIMENTO' tinta x 398-676, topo 1156, base 1180;
# linha 2 'TRIDIMENSIONAL' 1187-1211 (fica intacta); linha 3 'DE OLHEIRAS' x 432-643, topo 1219, base 1243.
# Outras artes: mesmo logo deslocado (dx, dy).

def campo_dourado(im, caixa):
    """Campo de cor do logo: pixels dourados conhecidos e o resto preenchido por inpainting
    clássico (Telea), mantendo o degradê e a granulação do original. Sem IA generativa."""
    import cv2
    import numpy as np
    from PIL import Image
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    sub = a[y0:y1, x0:x1]
    s = sub.astype(int)
    conhecido = (s.sum(2) > 330) & (s[..., 0] > s[..., 2] + 60)
    campo = cv2.inpaint(cv2.cvtColor(sub, cv2.COLOR_RGB2BGR), (~conhecido).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
    out = Image.new('RGB', im.size, (0, 0, 0))
    out.paste(Image.fromarray(cv2.cvtColor(campo, cv2.COLOR_BGR2RGB)), (x0, y0))
    return out


def logo_es(im, dx=0, dy=0, apagar_linha=None):
    """Troca as linhas 1 e 3 do logo por 'RELLENO' e 'DE OJERAS' (linha 2 é igual em ES).
    apagar_linha(im, caixa) apaga o texto PT; padrão: repinta de preto (fundo chapado)."""
    from PIL import Image, ImageDraw
    campo = campo_dourado(im, (380 + dx, 1145 + dy, 700 + dx, 1252 + dy))
    fg = por_altura_maiuscula('Arimo_700Bold', 24)
    tg = entreletra(fg, 'PREENCHIMENTO', 676 - 398 + 1)
    for caixa in [(385 + dx, 1150 + dy, 690 + dx, 1184 + dy), (420 + dx, 1214 + dy, 655 + dx, 1249 + dy)]:
        if apagar_linha:
            im = apagar_linha(im, caixa)
        else:
            ImageDraw.Draw(im).rectangle([caixa[0], caixa[1], caixa[2] - 1, caixa[3] - 1], fill=(0, 0, 0))
    for texto, base, centro in [('RELLENO', 1180, (398 + 676) / 2), ('DE OJERAS', 1243, (432 + 643) / 2)]:
        camada = Image.new('L', im.size, 0)
        desenhar_spans(camada, [(texto, fg, 255, None, tg)], base + dy, centro=centro + dx)
        im.paste(campo, (0, 0), camada)
    return im
