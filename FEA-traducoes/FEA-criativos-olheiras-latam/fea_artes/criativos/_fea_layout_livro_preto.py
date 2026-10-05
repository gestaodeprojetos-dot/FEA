"""Base comum dos criativos Ads 13, 14 e 15 (layout preto, faixa amarela à direita,
mockup do livro branco). Só define funções: não gera arquivo quando executado.

Texto em Manrope (corpo e título, com tracking negativo calibrado pela arte) e
Arimo Bold (logo do topo). Apagamento por inpainting clássico OpenCV, sem IA.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import abrir, salvar, fonte, PRECOS, cor_texto, previa  # noqa: E402,F401

REG = fonte('Manrope_400Regular')
MED = fonte('Manrope_500Medium')
SEMI = fonte('Manrope_600SemiBold')
BOLD = fonte('Manrope_700Bold')
XBOLD = fonte('Manrope_800ExtraBold')
LOGO = fonte('Arimo_700Bold')

_cache = {}


def F(caminho, tam):
    k = (caminho, round(tam * 4) / 4)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(caminho, k[1])
    return _cache[k]


def largura_runs(runs, tam, track):
    """runs: [(texto, caminho_fonte, cor, riscado)]; track em em (fração do tamanho)."""
    w = 0.0
    n = 0
    for t, p, *_ in runs:
        f = F(p, tam)
        w += f.getlength(t)
        n += len(t)
    return w + track * tam * max(n - 1, 0)


def desenhar_runs(im, x, base, runs, tam, track, alinhar='esquerda', largura_ref=None):
    d = ImageDraw.Draw(im)
    W = largura_runs(runs, tam, track)
    if alinhar == 'centro':
        x = x - W / 2
    cx = x
    for t, p, cor, riscado in runs:
        f = F(p, tam)
        x_ini = cx
        for i, ch in enumerate(t):
            d.text((cx, base), ch, font=f, fill=cor, anchor='ls')
            cx += (f.getlength(t[:i + 1]) - f.getlength(t[:i])) + track * tam
        if riscado:
            alto = f.getbbox('0', anchor='ls')[1]  # topo dos algarismos (negativo)
            ym = base + alto * 0.42
            esp = max(2, round(tam / 14))
            d.line([(x_ini - tam * 0.04, ym), (cx - track * tam + tam * 0.04, ym)], fill=cor, width=esp)
    return W


def ajustar(linhas_pt, larguras, track):
    """Tamanho que reproduz a largura medida de cada linha PT (mediana entre linhas)."""
    est = []
    for runs, w in zip(linhas_pt, larguras):
        lo, hi = 5.0, 200.0
        for _ in range(40):
            m = (lo + hi) / 2
            if largura_runs(runs, m, track) > w:
                hi = m
            else:
                lo = m
        est.append(lo)
    return float(np.median(est))


def estimar_track(linhas_pt, larguras):
    """Ajuste por mínimos quadrados de tamanho e tracking: w = s*a + s*t*(n-1)."""
    A, b = [], []
    for runs, w in zip(linhas_pt, larguras):
        a = sum(F(p, 100).getlength(t) for t, p, *_ in runs) / 100
        n = sum(len(t) for t, *_ in runs)
        A.append([a, n - 1]); b.append(w)
    (s, st), *_ = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
    return s, st / s


def quebrar(runs, tam, track, largura_max):
    """Quebra por palavras preservando o estilo de cada trecho."""
    palavras = []  # lista de listas de (texto, p, cor, riscado) formando 1 palavra
    atual = []
    for t, p, cor, ris in runs:
        partes = t.split(' ')
        for j, pt in enumerate(partes):
            if j > 0:
                if atual:
                    palavras.append(atual)
                atual = []
            if pt:
                atual.append((pt, p, cor, ris))
    if atual:
        palavras.append(atual)
    linhas, linha = [], []
    for w in palavras:
        teste = linha + ([(' ', w[0][1], w[0][2], False)] if linha else []) + w
        if linha and largura_runs(teste, tam, track) > largura_max:
            linhas.append(linha); linha = list(w)
        else:
            linha = teste
    if linha:
        linhas.append(linha)
    return linhas


def bloco(im, x, base1, passo, runs, tam, track, largura_max, base_max, alinhar='esquerda', reducao_max=0.15, max_linhas=None):
    """Escreve um parágrafo. Reduz a fonte (até reducao_max) se precisar caber até base_max."""
    for k in range(0, int(reducao_max * 100) + 1):
        s = 1 - k / 100
        ls = quebrar(runs, tam * s, track, largura_max)
        ultima = base1 + passo * s * (len(ls) - 1)
        if ultima <= base_max and (max_linhas is None or len(ls) <= max_linhas):
            break
    else:
        raise SystemExit(f'texto não coube: {runs[0][0][:40]}... ({len(ls)} linhas, base {ultima:.0f} > {base_max})')
    for i, l in enumerate(ls):
        desenhar_runs(im, x, base1 + passo * s * i, l, tam * s, track, alinhar)
    return {'escala': s, 'linhas': len(ls), 'ultima_base': base1 + passo * s * (len(ls) - 1)}


def base_de(topo_medido, runs, tam, track):
    """Linha de base a partir do topo medido da linha PT (texto e fonte conhecidos)."""
    t = min(F(p, tam).getbbox(tx, anchor='ls')[1] for tx, p, *_ in runs if tx.strip())
    return topo_medido - t


def apagar_mascara(im, m, dil=3, raio=7):
    a = np.array(im)
    m = cv2.dilate(m.astype(np.uint8) * 255, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def mascara_caixa(im, caixa, cond):
    a = np.array(im).astype(int)
    m = np.zeros(a.shape[:2], bool)
    x0, y0, x1, y1 = caixa
    s = a[y0:y1, x0:x1]
    m[y0:y1, x0:x1] = cond(s[..., 0], s[..., 1], s[..., 2])
    return m


TEXTO_CLARO = lambda r, g, b: (r + g + b) > 260  # branco e amarelo sobre o fundo preto
TEXTO_ESCURO = lambda r, g, b: (r + g + b) < 420  # texto escuro sobre a caixa amarela


def cor_mediana(im, caixa, cond):
    a = np.array(im).astype(int)[caixa[1]:caixa[3], caixa[0]:caixa[2]]
    m = cond(a[..., 0], a[..., 1], a[..., 2])
    px = a[m]
    lum = px.sum(1)
    sel = px[lum >= np.percentile(lum, 50)] if np.median(lum) > 382 else px[lum <= np.percentile(lum, 50)]
    return tuple(int(v) for v in np.median(sel, 0))


AMARELO = lambda r, g, b: (r > 200) & (g > 130) & (b < 140) & (r - b > 90)
BRANCO = lambda r, g, b: (r > 190) & (g > 190) & (b > 190)


# ---------------------------------------------------------------- composição
TRACK_TIT = -0.006
TRACK_CORPO = -0.01


def _bases(linhas_pt, tops, tam, track, p):
    return [base_de(t, [(l, p, 0, False)], tam, track) for l, t in zip(linhas_pt, tops)]


def _calib(linhas_pt, xs, p, track):
    return ajustar([[(l, p, 0, False)] for l in linhas_pt], [b - a for a, b in xs], track)


def _caixa_preco(im, caixa, estilo):
    """Repinta o miolo da caixa de preço (cinza chapada ou amarela em degradê horizontal)."""
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    ref = a[y0 + 2, :].copy()  # linha sem texto: cor por coluna (degradê só na horizontal)
    alvo = ref[x0 + 5].astype(int)
    for y in range(y0 + 1, y1):
        linha = a[y, x0:x1 + 3].astype(int)
        perto = np.abs(linha - alvo).max(1) <= (6 if estilo == 'cinza' else 40)
        if estilo == 'amarelo':
            perto = (linha[:, 0] > 225) & (linha[:, 1] > 185) & (linha[:, 2] > 100)
        idx = np.where(perto)[0]
        if not len(idx):
            continue
        dir_ = x0 + idx.max() - 3
        a[y, x0:dir_] = ref[x0:dir_]
    return Image.fromarray(a)


def _esticar(im, caixa, dx, x_corte, x_lim):
    """Alarga a caixa de preço para a direita deslocando a ponta arredondada (copia colunas)."""
    if dx <= 0:
        return im
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    ys = slice(max(0, y0 - 3), y1 + 4)
    orig = a[ys].copy()
    a[ys, x_corte + dx:x_lim] = orig[:, x_corte:x_lim - dx]
    a[ys, x_corte:x_corte + dx] = orig[:, x_corte:x_corte + 1]
    return Image.fromarray(a)


def compor(sp):
    im = abrir(sp['origem'])
    rel = {}
    # ---------- apagar texto sobre o fundo preto (fora da caixa de preço)
    cx0, cy0, cx1, cy1 = sp['preco']['caixa']
    m = mascara_caixa(im, (40, sp['logo']['tops'][0] - 8, sp['x_lim'], cy0 - 1), TEXTO_CLARO)
    uy = sp['logo']['sublinhado']
    m[uy - 3:uy + 4, :] = False
    m |= mascara_caixa(im, (40, cy1 + 2, sp['x_lim'], sp['cta']['tops'][-1] + 60), TEXTO_CLARO)
    cor_tit_b = cor_mediana(im, sp['cor_branco_tit'], BRANCO)
    cor_y = cor_mediana(im, sp['cor_amarelo'], AMARELO)
    cor_logo = cor_mediana(im, (sp['logo']['xs'][1][0], sp['logo']['tops'][1], sp['logo']['xs'][1][1], sp['logo']['tops'][1] + 20), AMARELO)
    cor_corpo = cor_mediana(im, sp['cor_corpo'], BRANCO)
    im = apagar_mascara(im, m, dil=3, raio=7)

    # ---------- logo (Arimo Bold, centrado)
    lg = sp['logo']
    pt = ['PREENCHIMENTO', 'TRIDIMENSIONAL', 'DE OLHEIRAS']
    es = ['RELLENO', 'TRIDIMENSIONAL', 'DE OJERAS']
    tam = _calib(pt, lg['xs'], LOGO, 0)
    centro = (lg['xs'][1][0] + lg['xs'][1][1]) / 2
    for l_pt, l_es, t in zip(pt, es, lg['tops']):
        b = base_de(t, [(l_pt, LOGO, 0, 0)], tam, 0)
        desenhar_runs(im, centro, b, [(l_es, LOGO, cor_logo, False)], tam, 0, 'centro')

    # ---------- fluxo título + corpo (+ subtítulo)
    blocos = sp['fluxo']
    medidas = []
    for bl in blocos:
        p = bl['fonte']
        tr = bl['track']
        t = _calib(bl['pt'], bl['xs'], p, tr)
        bs = _bases(bl['pt'], bl['tops'], t, tr, p)
        passo = (bs[-1] - bs[0]) / (len(bs) - 1)
        medidas.append((t, bs, passo))
    limite = sp['limite_fluxo']
    larg = sp['x_dir'] - sp['x_col']
    for k in range(0, 16):
        s = 1 - k / 100
        y = medidas[0][1][0]
        planos = []
        ok = True
        for i, (bl, (t, bs, passo)) in enumerate(zip(blocos, medidas)):
            if i > 0:
                ant_bs = medidas[i - 1][1]
                y = y + (bs[0] - ant_bs[-1]) * s  # mesmo respiro entre blocos, escalado
            runs = [(tx, bl['fonte'] if st != 'B' else bl.get('fonte_b', bl['fonte']),
                     cor_y if st == 'Y' else (cor_tit_b if bl['tipo'] == 'titulo' else cor_corpo), False)
                    for tx, st in bl['es']]
            ls = quebrar(runs, t * s, bl['track'], larg)
            planos.append((y, passo * s, ls, t * s, bl['track']))
            y = y + passo * s * (len(ls) - 1)
        if y <= limite:
            break
    else:
        raise SystemExit('fluxo não coube em ' + sp['saida'])
    rel['escala_fluxo'] = s
    rel['linhas'] = [len(p_[2]) for p_ in planos]
    for y0, ps, ls, t, tr in planos:
        for i, l in enumerate(ls):
            desenhar_runs(im, sp['x_col'], y0 + ps * i, l, t, tr)

    # ---------- caixa de preço
    pr = sp['preco']
    im = _caixa_preco(im, pr['caixa'], pr['estilo'])
    cor_txt = pr['cor_txt'] if pr['estilo'] == 'amarelo' else cor_corpo
    cor_val = pr['cor_txt'] if pr['estilo'] == 'amarelo' else cor_y
    pt_runs = [[('Por apenas ', REG, 0, 0), ('R$ 97,00', SEMI, 0, 0)]]
    tam = ajustar(pt_runs, [pr['xs'][1][1] - pr['xs'][1][0]], TRACK_CORPO)
    bases = [base_de(pr['tops'][0], [('De ', REG, 0, 0), ('R$200,00', SEMI, 0, 0)], tam, TRACK_CORPO),
             base_de(pr['tops'][1], pt_runs[0], tam, TRACK_CORPO)]
    es = [[('De ', REG, cor_txt, False), (PRECOS['de_200'], SEMI, cor_txt, True)],
          [('A solo ', REG, cor_txt, False), (PRECOS['preco'], SEMI, cor_val, False)]]
    if pr.get('so_hoje'):
        bases.append(base_de(pr['tops'][2], [('SÓ HOJE', XBOLD, 0, 0)], tam, TRACK_CORPO))
        es.append([('SOLO HOY', XBOLD, cor_txt, False)])
    x = pr['xs'][0][0]
    lim_txt = pr['x_max_esticar'] - pr['folga_dir']
    s = 1.0
    while max(largura_runs(r, tam * s, TRACK_CORPO) for r in es) > lim_txt - x and s > 0.85:
        s -= 0.01
    precisa = x + max(largura_runs(r, tam * s, TRACK_CORPO) for r in es) + pr['folga_dir']
    dx = int(np.ceil(precisa - pr['caixa'][2]))
    if dx > 0:
        im = _esticar(im, pr['caixa'], dx, pr['x_corte'], sp['x_lim'])
    rel['preco'] = {'escala': s, 'caixa_alargada_px': max(dx, 0)}
    for b, r in zip(bases, es):
        desenhar_runs(im, x, b, r, tam * s, TRACK_CORPO)

    # ---------- CTA
    ct = sp['cta']
    tam = ajustar([ct['pt'][0]], [ct['xs'][0][1] - ct['xs'][0][0]], TRACK_CORPO)
    for l_pt, l_es, t in zip(ct['pt'], ct['es'], ct['tops']):
        b = base_de(t, l_pt, tam, TRACK_CORPO)
        runs = [(tx, p, cor_y if st == 'Y' else cor_corpo, False) for tx, p, st in l_es]
        desenhar_runs(im, ct['xs'][0][0], b, runs, tam, TRACK_CORPO)

    salvar(im, sp['saida'])
    previa(im, os.path.join(os.path.dirname(sp['origem']), 'pto-saida-' + os.path.basename(sp['origem']).replace('.png', '.jpg')), 1080)
    return im, rel
