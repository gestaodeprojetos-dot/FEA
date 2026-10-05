"""Utilitários dos criativos Ads 01 a 04 (texto em caixas chapadas estilo Instagram).

Não gera arte quando rodado sozinho (rodar_todos.py executa todo *.py da pasta).
Nunca usa IA generativa: só repinta caixas chapadas com a cor medida e escreve texto.
"""
import os, sys
import numpy as np
from PIL import ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from fea_arte_lib import *  # noqa


def caixa_solida(im, cor, regiao, tol=3, min_lin=60, min_col=10):
    """Limites (x0, y0, x1, y1) exclusivos da caixa chapada de cor 'cor' dentro da região."""
    a = np.array(im).astype(int)
    x0, y0, x1, y1 = regiao
    s = a[y0:y1, x0:x1]
    m = np.abs(s - np.array(cor)).max(2) <= tol
    r = np.where(m.sum(1) > min_lin)[0]
    c = np.where(m.sum(0) > min_col)[0]
    return (int(c.min() + x0), int(r.min() + y0), int(c.max() + x0 + 1), int(r.max() + y0 + 1))


def quebrar(texto, f, largura):
    """Quebra gulosa por palavras."""
    linhas, atual = [], ''
    for p in texto.split():
        t = (atual + ' ' + p).strip()
        if atual and f.getlength(t) > largura:
            linhas.append(atual)
            atual = p
        else:
            atual = t
    if atual:
        linhas.append(atual)
    return linhas


def quebrar_equilibrado(texto, f, largura, n):
    """Quebra em exatamente n linhas minimizando a linha mais larga (busca pela largura)."""
    lo, hi = 10, largura
    melhor = None
    while lo <= hi:
        mid = (lo + hi) // 2
        ls = quebrar(texto, f, mid)
        if len(ls) <= n:
            melhor = ls
            hi = mid - 1
        else:
            lo = mid + 1
    return melhor


def ajustar(texto, caminho, tam, largura, n_max, reducao_max=0.15, equilibrar=True):
    """Maior tamanho (até -15 %) em que o texto cabe em n_max linhas na largura."""
    t = tam
    while t >= tam * (1 - reducao_max) - 1e-6:
        f = ImageFont.truetype(caminho, t)
        ls = quebrar(texto, f, largura)
        if len(ls) <= n_max:
            if equilibrar:
                ls = quebrar_equilibrado(texto, f, largura, len(ls))
            return f, ls
        t -= 0.25
    f = ImageFont.truetype(caminho, tam * (1 - reducao_max))
    ls = quebrar(texto, f, largura)
    if equilibrar:
        ls = quebrar_equilibrado(texto, f, largura, len(ls))
    return f, ls


def larg(f, s):
    return f.getlength(s)


def escrever_bloco(im, linhas, f, cor, cx, base1, passo, alinhamento='centro', x_esq=None, traco=0):
    """Escreve linhas com linha de base base1 + i*passo. cx = centro horizontal."""
    d = ImageDraw.Draw(im)
    for i, s in enumerate(linhas):
        y = base1 + i * passo
        if alinhamento == 'esquerda':
            d.text((x_esq, y), s, font=f, fill=cor, anchor='ls', stroke_width=traco, stroke_fill=cor)
        else:
            d.text((cx, y), s, font=f, fill=cor, anchor='ms', stroke_width=traco, stroke_fill=cor)


def bbox_linhas(linhas, f, cx, base1, passo):
    """Caixa real ocupada pelo texto (para conferir margens)."""
    xs0, ys0, xs1, ys1 = [], [], [], []
    for i, s in enumerate(linhas):
        l, t, r, b = f.getbbox(s, anchor='ms')
        xs0.append(cx + l); xs1.append(cx + r)
        ys0.append(base1 + i * passo + t); ys1.append(base1 + i * passo + b)
    return min(xs0), min(ys0), max(xs1), max(ys1)


if __name__ == '__main__':
    pass
