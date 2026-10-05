"""Utilitários dos criativos Ads 01 a 04 (texto em caixas chapadas estilo Instagram).

Não gera arte quando rodado sozinho (rodar_todos.py executa todo *.py da pasta).
Nunca usa IA generativa: só repinta caixas chapadas com a cor medida e escreve texto.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
    for p in [w for w in texto.split(' ') if w]:
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


class Tipo:
    """Fonte com compressão horizontal opcional (kx) para casar com o original."""
    def __init__(self, caminho, tam, kx=1.0):
        self.caminho, self.size, self.kx = caminho, tam, kx
        self.f = ImageFont.truetype(caminho, tam)

    def getlength(self, s):
        return self.f.getlength(s) * self.kx

    def getbbox(self, s, anchor='ls'):
        l, t, r, b = self.f.getbbox(s, anchor=anchor)
        return l * self.kx, t, r * self.kx, b

    def escala(self, fator):
        return Tipo(self.caminho, self.size * fator, self.kx)


def ajustar(texto, tipo, largura, n_max, reducao_max=0.15, equilibrar=True):
    """Maior tamanho (até -15 %) em que o texto cabe em n_max linhas na largura."""
    fator = 1.0
    while fator >= 1 - reducao_max - 1e-6:
        f = tipo.escala(fator)
        ls = quebrar(texto, f, largura)
        if len(ls) <= n_max:
            if equilibrar:
                ls = quebrar_equilibrado(texto, f, largura, len(ls))
            return f, ls
        fator -= 0.005
    f = tipo.escala(1 - reducao_max)
    ls = quebrar(texto, f, largura)
    if equilibrar:
        ls = quebrar_equilibrado(texto, f, largura, len(ls))
    return f, ls


def larg(f, s):
    return f.getlength(s)


def escrever_bloco(im, linhas, f, cor, cx, base1, passo, alinhamento='centro', x_esq=None, traco=0):
    """Escreve linhas com linha de base base1 + i*passo. cx = centro horizontal."""
    for i, s in enumerate(linhas):
        y = base1 + i * passo
        w = f.getlength(s)
        x = x_esq if alinhamento == 'esquerda' else cx - w / 2
        escrever_linha(im, s, f, cor, x, y, traco)


def escrever_linha(im, s, f, cor, x, y_base, traco=0):
    """Escreve uma linha (origem à esquerda na linha de base), com compressão kx via camada."""
    if getattr(f, 'kx', 1.0) == 1.0:
        ft = f.f if isinstance(f, Tipo) else f
        ImageDraw.Draw(im).text((x, y_base), s, font=ft, fill=cor, anchor='ls', stroke_width=traco, stroke_fill=cor)
        return
    esc = 4  # supersample para a compressão não borrar
    ft = ImageFont.truetype(f.caminho, f.size * esc)
    l, t, r, b = ft.getbbox(s, anchor='ls')
    pad = 4 * esc
    W, H = int(r - min(l, 0) + 2 * pad), int(b - t + 2 * pad)
    alfa = Image.new('L', (W, H), 0)
    ImageDraw.Draw(alfa).text((pad - min(l, 0), pad - t), s, font=ft, fill=255, anchor='ls', stroke_width=traco * esc, stroke_fill=255)
    nw, nh = max(1, round(W * f.kx / esc)), max(1, round(H / esc))
    alfa = alfa.resize((nw, nh), Image.LANCZOS)
    cam = Image.new('RGB', (nw, nh), tuple(cor))
    ox = x - (pad - min(l, 0)) * f.kx / esc
    oy = y_base - (pad - t) / esc
    im.paste(cam, (int(round(ox)), int(round(oy))), alfa)


def bbox_linhas(linhas, f, cx, base1, passo):
    """Caixa real ocupada pelo texto (para conferir margens)."""
    xs0, ys0, xs1, ys1 = [], [], [], []
    for i, s in enumerate(linhas):
        l, t, r, b = f.getbbox(s, anchor='ls')
        w = f.getlength(s)
        xs0.append(cx - w / 2 + l); xs1.append(cx - w / 2 + r)
        ys0.append(base1 + i * passo + t); ys1.append(base1 + i * passo + b)
    return min(xs0), min(ys0), max(xs1), max(ys1)


def linhas_texto(im, caixa, cond, frac_min=0.45):
    """medir() sem imprimir, descartando faixas pequenas (acentos soltos)."""
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        ls = medir(im, caixa, cond)
    if not ls:
        return ls
    hmax = max(l[1] - l[0] for l in ls)
    bons = [list(l) for l in ls if l[1] - l[0] >= frac_min * hmax]
    # faixa pequena logo acima de uma linha (til, circunflexo) é anexada a ela
    for l in ls:
        if l[1] - l[0] < frac_min * hmax:
            prox = [b for b in bons if b[0] > l[1]]
            if prox:
                alvo = min(prox, key=lambda b: b[0])
                alvo[2] = min(alvo[2], l[2]); alvo[3] = max(alvo[3], l[3])
    return [tuple(b) for b in bons]


def paragrafo(im, caixa, linhas_pt, texto_es, caminho, cond_txt, fundo_ext=None, larg_max=None, n_max=None,
              linhas_es=None, reducao_max=0.15, cor_caixa=None, cor_txt=None, inset=3, verbose=''):
    """Troca o texto de uma caixa chapada (estilo destaque do Instagram).

    caixa: (x0, y0, x1, y1) exclusivos da caixa chapada original.
    fundo_ext: cor do fundo atrás da caixa, se for chapado (aí a caixa pode encolher);
               None = fundo foto: a nova caixa é a união com a original (só cresce).
    """
    x0, y0, x1, y1 = caixa
    med = linhas_texto(im, (x0 + inset, y0 + inset, x1 - inset, y1 - inset), cond_txt)
    if len(med) != len(linhas_pt):
        raise SystemExit(f'{verbose}: {len(med)} linhas medidas, {len(linhas_pt)} esperadas: {med}')
    if cor_caixa is None:
        cor_caixa = cor_fundo(im, (x0 + 1, y0 + 1, x1 - 1, y0 + inset + 1))
    if cor_txt is None:
        cor_txt = cor_texto(im, caixa, cond_txt)
    i = max(range(len(med)), key=lambda k: med[k][3] - med[k][2])
    f = calibrar(caminho, linhas_pt[i], med[i][3] - med[i][2] + 1)
    bases = [m[0] - f.getbbox(pt, anchor='ls')[1] for m, pt in zip(med, linhas_pt)]
    passo = (bases[-1] - bases[0]) / (len(bases) - 1) if len(bases) > 1 else 0
    cx = (min(m[2] for m in med) + max(m[3] for m in med) + 1) / 2
    pad_x = min(m[2] for m in med) - x0
    larg_pt = max(m[3] - m[2] + 1 for m in med)
    if larg_max is None:
        larg_max = larg_pt
    t = Tipo(caminho, f.size)
    if linhas_es is None:
        f2, ls = ajustar(texto_es, t, larg_max, n_max or len(linhas_pt), reducao_max)
    else:
        ls = linhas_es
        fator = 1.0
        while max(t.escala(fator).getlength(s) for s in ls) > larg_max and fator > 1 - reducao_max:
            fator -= 0.005
        f2 = t.escala(fator)
    s = f2.size / t.size
    passo2 = passo * s if passo else f2.size * 1.2
    meio = (bases[0] + bases[-1]) / 2
    b1 = meio - passo2 * (len(ls) - 1) / 2
    bn = b1 + passo2 * (len(ls) - 1)
    larg_es = max(f2.getlength(z) for z in ls)
    nova = (int(round(cx - larg_es / 2 - pad_x)), int(round(b1 - (bases[0] - y0))),
            int(round(cx + larg_es / 2 + pad_x)), int(round(bn + (y1 - bases[-1]))))
    if fundo_ext is not None:
        preencher(im, (x0 - 2, y0 - 2, x1 + 2, y1 + 2), fundo_ext)
        # só alarga/encolhe na horizontal; altura acompanha o número de linhas
    else:
        nova = (min(nova[0], x0), min(nova[1], y0), max(nova[2], x1), max(nova[3], y1))
    preencher(im, nova, cor_caixa)
    escrever_bloco(im, ls, f2, cor_txt, cx, b1, passo2)
    if verbose:
        print(verbose, 'escala %.3f' % s, 'caixa', caixa, '->', nova, ls)
    return nova, f2, ls


if __name__ == '__main__':
    pass
