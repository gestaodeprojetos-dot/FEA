"""Utilitários do lote Ads 31 a 35 (Ebook Olheiras LATAM), complemento da fea_arte_lib.

- apagar_col: apaga texto interpolando cada coluna entre o pixel limpo de cima e o de baixo
  (preserva degradê horizontal de botão dourado e degradê vertical de fundo). Sem IA generativa.
- apagar_suave: convolução normalizada (fundo liso escuro), sem IA generativa.
- desenhar: linha com vários trechos (fonte, cor ou degradê), tracking e linha de base.
"""
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from fea_arte_lib import fonte, mascara

_cache = {}


def F(nome, tam):
    k = (nome, round(float(tam), 2))
    if k not in _cache:
        _cache[k] = ImageFont.truetype(fonte(nome), float(tam))
    return _cache[k]


def _mask(im, caixa, cond, dil):
    a = np.array(im)
    m = np.zeros(a.shape[:2], np.uint8)
    x0, y0, x1, y1 = caixa
    m[y0:y1, x0:x1] = mascara(im, caixa, cond).astype(np.uint8)
    if dil:
        m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    m[:y0, :] = 0; m[y1:, :] = 0; m[:, :x0] = 0; m[:, x1:] = 0
    return a, m.astype(bool)


def apagar_col(im, caixa, cond, dil=4):
    """Cada pixel de texto recebe a interpolação linear, na mesma coluna, entre o último pixel
    limpo acima e o primeiro limpo abaixo (dentro da caixa)."""
    a, m = _mask(im, caixa, cond, dil)
    a = a.astype(float)
    x0, y0, x1, y1 = caixa
    for x in range(x0, x1):
        col = m[y0:y1, x]
        if not col.any():
            continue
        ys = np.arange(y0, y1)
        ok = ~col
        if ok.sum() < 2:
            continue
        for c in range(3):
            a[y0:y1, x, c][col] = np.interp(ys[col], ys[ok], a[y0:y1, x, c][ok])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def apagar_lin(im, caixa, cond, dil=4):
    """Igual a apagar_col, mas interpolando na horizontal (fundo com degradê vertical forte)."""
    a, m = _mask(im, caixa, cond, dil)
    a = a.astype(float)
    x0, y0, x1, y1 = caixa
    for y in range(y0, y1):
        lin = m[y, x0:x1]
        if not lin.any():
            continue
        xs = np.arange(x0, x1)
        ok = ~lin
        if ok.sum() < 2:
            continue
        for c in range(3):
            a[y, x0:x1, c][lin] = np.interp(xs[lin], xs[ok], a[y, x0:x1, c][ok])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def apagar_misto(im, caixa, cond, dil=4):
    """Média de apagar_col e apagar_lin (some com riscos de interpolação em uma só direção)."""
    a1 = np.array(apagar_col(im, caixa, cond, dil)).astype(float)
    a2 = np.array(apagar_lin(im, caixa, cond, dil)).astype(float)
    return Image.fromarray(((a1 + a2) / 2).round().astype(np.uint8))


def apagar_suave(im, caixa, cond, dil=4, k=61):
    """Convolução normalizada: média dos pixels limpos vizinhos (fundo escuro liso)."""
    a, m = _mask(im, caixa, cond, dil)
    x0, y0, x1, y1 = caixa
    p = k
    X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - p), min(a.shape[1], x1 + p), min(a.shape[0], y1 + p)
    sub = a[Y0:Y1, X0:X1].astype(float)
    mm = m[Y0:Y1, X0:X1]
    w = (~mm).astype(float)
    num = np.stack([cv2.GaussianBlur(sub[..., c] * w, (k, k), 0) for c in range(3)], -1)
    den = cv2.GaussianBlur(w, (k, k), 0)[..., None]
    fill = num / np.maximum(den, 1e-6)
    sub[mm] = fill[mm]
    a = a.copy()
    a[Y0:Y1, X0:X1] = np.clip(sub, 0, 255).astype(np.uint8)
    return Image.fromarray(a)


def larg_run(t, f, tracking):
    if not t:
        return 0
    return sum(f.getlength(ch) for ch in t) + tracking * len(t) if tracking else f.getlength(t)


def desenhar(im, runs, tam, base, cx=None, x_esq=None, tracking=0.0, so_medir=False):
    """runs: [(texto, nome_fonte, cor)] com cor = (r,g,b) ou ('grad', (r,g,b), (r,g,b)) horizontal.
    Linha de base 'base'. Centraliza a tinta em cx ou começa a tinta em x_esq.
    tracking em px por caractere. Retorna bbox (x0, y0, x1, y1) da tinta."""
    W, H = im.size
    camada = Image.new('L', (W, H), 0)
    # 1a passada: medir tinta a partir de x=0
    pos = []
    x = 0.0
    tx0 = ty0 = 1e9
    tx1 = ty1 = -1e9
    for t, nome, cor in runs:
        f = F(nome, tam)
        chars = []
        if tracking:
            for ch in t:
                chars.append((x, ch))
                if ch.strip():
                    l, tp, r, bt = f.getbbox(ch, anchor='ls')
                    tx0, tx1 = min(tx0, x + l), max(tx1, x + r)
                    ty0, ty1 = min(ty0, base + tp), max(ty1, base + bt)
                x += f.getlength(ch) + tracking
        else:
            chars.append((x, t))
            if t.strip():
                l, tp, r, bt = f.getbbox(t, anchor='ls')
                tx0, tx1 = min(tx0, x + l), max(tx1, x + r)
                ty0, ty1 = min(ty0, base + tp), max(ty1, base + bt)
            x += f.getlength(t)
        pos.append((t, f, cor, chars))
    dx = (cx - (tx0 + tx1) / 2) if cx is not None else (x_esq - tx0)
    bbox = (tx0 + dx, ty0, tx1 + dx, ty1)
    if so_medir:
        return bbox
    a = np.array(im).astype(float)
    for t, f, cor, chars in pos:
        lay = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(lay)
        for x, ch in chars:
            d.text((x + dx, base), ch, font=f, fill=255, anchor='ls')
        al = np.array(lay).astype(float)[..., None] / 255.0
        if cor[0] == 'grad':
            ys, xs = np.where(al[..., 0] > 0)
            c0, c1 = np.array(cor[1], float), np.array(cor[2], float)
            xa, xb = xs.min(), xs.max()
            tt = (np.arange(W) - xa) / max(1, xb - xa)
            tt = np.clip(tt, 0, 1)[None, :, None]
            col = c0 + (c1 - c0) * tt
            col = np.broadcast_to(col, (H, W, 3))
        elif cor[0] == 'perfil':
            ys, xs = np.where(al[..., 0] > 0)
            xa, xb = xs.min(), xs.max()
            tt = np.clip((np.arange(W) - xa) / max(1, xb - xa), 0, 1)
            pts = np.array([q[0] for q in cor[1]], float)
            cs = np.array([q[1] for q in cor[1]], float)
            col = np.stack([np.interp(tt, pts, cs[:, c]) for c in range(3)], -1)[None]
            col = np.broadcast_to(col, (H, W, 3))
        else:
            col = np.array(cor, float)[None, None, :]
        a = a * (1 - al) + col * al
    im.paste(Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8)))
    return bbox


def calibrar_runs(runs, largura, tracking=0.0, ini=8, fim=300):
    """Tamanho (passo 0,25) em que os runs PT ocupam a largura de tinta medida.
    tracking em fração do tamanho (em)."""
    dummy = Image.new('RGB', (10, 10))
    w = lambda t: (lambda b: b[2] - b[0])(desenhar(dummy, runs, t, 0, x_esq=0, tracking=tracking * t, so_medir=True))
    lo, hi = ini, fim
    while hi - lo > 0.25:
        mid = (lo + hi) / 2
        if w(mid) < largura:
            lo = mid
        else:
            hi = mid
    return min((round(lo * 4) / 4, round(hi * 4) / 4), key=lambda t: abs(w(t) - largura))


def base_de(runs, tam, y_topo, tracking=0.0):
    """Linha de base que põe o topo da tinta dos runs PT em y_topo."""
    dummy = Image.new('RGB', (10, 10))
    b = desenhar(dummy, runs, tam, 0, x_esq=0, tracking=tracking, so_medir=True)
    return y_topo - b[1]


def cor_mediana(im, caixa, cond, pct=None):
    a = np.array(im)[caixa[1]:caixa[3], caixa[0]:caixa[2]].astype(int)
    px = a[cond(a[..., 0], a[..., 1], a[..., 2])]
    return tuple(int(v) for v in np.median(px, 0))


def esticar_horizontal(im, caixa, novo_x0, novo_x1, x_corte_esq, x_corte_dir):
    """Alarga uma pílula/botão (caixa = x0,y0,x1,y1) para [novo_x0, novo_x1]: as pontas
    [x0, x_corte_esq) e [x_corte_dir, x1) são copiadas intactas e o miolo é reamostrado
    horizontalmente (mantém o degradê e o brilho central). Só pixels do botão."""
    x0, y0, x1, y1 = caixa
    a = np.array(im)
    esq = a[y0:y1, x0:x_corte_esq]
    dir_ = a[y0:y1, x_corte_dir:x1]
    meio = a[y0:y1, x_corte_esq:x_corte_dir]
    w_meio = (novo_x1 - novo_x0) - esq.shape[1] - dir_.shape[1]
    meio2 = cv2.resize(meio, (w_meio, meio.shape[0]), interpolation=cv2.INTER_CUBIC)
    nova = np.concatenate([esq, meio2, dir_], 1)
    a = a.copy()
    a[y0:y1, novo_x0:novo_x1] = nova
    return Image.fromarray(a)


def cor_run(im, caixa, cond, claro=True, lim=22):
    """Cor do texto num trecho: sólida, ou ('grad', esq, dir) se a tinta muda ao longo do x.
    Usa só o miolo dos traços (metade mais clara se claro=True, mais escura se False)."""
    x0, y0, x1, y1 = caixa
    a = np.array(im)[y0:y1, x0:x1].astype(int)
    m = cond(a[..., 0], a[..., 1], a[..., 2])
    lum = a.sum(2)
    ys, xs = np.where(m)
    L = lum[ys, xs]
    core = (L >= np.percentile(L, 70)) if claro else (L <= np.percentile(L, 30))
    ys, xs = ys[core], xs[core]
    px = a[ys, xs]
    xa, xb = xs.min(), xs.max()
    w = xb - xa
    esq = np.median(px[xs <= xa + w * 0.15], 0)
    dir_ = np.median(px[xs >= xb - w * 0.15], 0)
    if np.abs(esq - dir_).max() > lim:
        return ('grad', tuple(int(v) for v in esq), tuple(int(v) for v in dir_))
    return tuple(int(v) for v in np.median(px, 0))


def caber(runs_es, tam, largura_max, tracking=0.0, red_max=0.15):
    """Reduz o tamanho (até red_max) para a linha caber em largura_max. Retorna (tam, reducao)."""
    dummy = Image.new('RGB', (10, 10))
    t = tam
    while t > tam * (1 - red_max):
        b = desenhar(dummy, runs_es, t, 0, x_esq=0, tracking=tracking * t, so_medir=True)
        if b[2] - b[0] <= largura_max:
            return t, 1 - t / tam
        t -= 0.25
    return t, 1 - t / tam


def perfil_cor(im, caixa, cond, n=12, claro=True):
    """Degradê horizontal da tinta: ('perfil', [(t, cor)]) com t de 0 a 1 ao longo da tinta."""
    x0, y0, x1, y1 = caixa
    a = np.array(im)[y0:y1, x0:x1].astype(int)
    m = cond(a[..., 0], a[..., 1], a[..., 2])
    ys, xs = np.where(m)
    L = a[ys, xs].sum(1)
    xa, xb = xs.min(), xs.max()
    pts = []
    for i in range(n):
        lo, hi = xa + (xb - xa) * i / n, xa + (xb - xa) * (i + 1) / n
        sel = (xs >= lo) & (xs <= hi)
        if sel.sum() < 10:
            continue
        Ls = L[sel]
        core = (Ls >= np.percentile(Ls, 70)) if claro else (Ls <= np.percentile(Ls, 30))
        c = np.median(a[ys[sel][core], xs[sel][core]], 0)
        pts.append(((i + 0.5) / n, tuple(int(v) for v in c)))
    pts = [(0.0, pts[0][1])] + pts + [(1.0, pts[-1][1])]
    return ('perfil', pts)


def mover_icone(orig, im, caixa, dx, cond, dil=4, suav=5):
    """Cola o ícone (pixels de 'cond' na caixa do ORIGINAL) deslocado dx, com borda suave,
    sobre a imagem atual (fundo já limpo)."""
    x0, y0, x1, y1 = caixa
    o = np.array(orig)[y0:y1, x0:x1].astype(float)
    m = cond(o[..., 0], o[..., 1], o[..., 2]).astype(np.uint8)
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8)).astype(float)
    m = cv2.GaussianBlur(m, (2 * suav + 1, 2 * suav + 1), 0)[..., None]
    a = np.array(im).astype(float)
    dst = a[y0:y1, x0 + dx:x1 + dx]
    a[y0:y1, x0 + dx:x1 + dx] = dst * (1 - m) + o * m
    return Image.fromarray(a.round().astype(np.uint8))
