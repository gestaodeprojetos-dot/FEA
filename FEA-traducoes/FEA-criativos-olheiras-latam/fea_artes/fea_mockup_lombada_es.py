#!/usr/bin/env python3
"""Lombada dos livros 3D verdes: troca o texto da lombada (português, e em várias artes do
Brasil um texto embaralhado de IA, tipo "PRENNMITO COLIEINAS") pelo título ES limpo
"RELLENO TRIDIMENSIONAL / DE OJERAS". Sem IA generativa.

Como funciona: a capa ES já aplicada (fea_mockup_capa_es.py) é localizada por SIFT; a lombada
é a faixa à esquerda da borda esquerda da capa. A faixa é retificada (homografia), o texto
dourado do título é apagado por inpainting clássico e o título ES é escrito em Arimo Bold
(métrica da Helvetica Bold, mesma família do original) com a textura dourada do próprio
original, na mesma direção de leitura (de cima para baixo), mesmas linhas e mesmo corpo.
"DR. JOÃO PITHON" na lombada fica intacto. Depois a faixa volta para a perspectiva da arte.
Rodar depois de fea_mockup_capa_es.py (rodar_todos.py chama no final).
"""
import glob, os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

AQ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQ)
from fea_arte_lib import fonte

SAIDA = os.path.join(os.path.dirname(AQ), 'FEA-artes-ES')
ES = cv2.imread(os.path.join(AQ, 'trabalho', 'capa-es.png'))
ESC = 0.5
sift = cv2.SIFT_create(nfeatures=6000)
es_s = cv2.resize(ES, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_AREA)
kb, db = sift.detectAndCompute(cv2.cvtColor(es_s, cv2.COLOR_BGR2GRAY), None)
ARIMO = fonte('Arimo_700Bold')
TITULO = ['RELLENO TRIDIMENSIONAL', 'DE OJERAS']


def capas(arte):
    g = cv2.cvtColor(arte, cv2.COLOR_BGR2GRAY)
    ka, da = sift.detectAndCompute(g, None)
    if da is None or len(ka) < 10:
        return []
    m = cv2.BFMatcher().knnMatch(db, da, k=2)
    bons = [a for a, b in (p for p in m if len(p) == 2) if a.distance < 0.75 * b.distance]
    out = []
    while len(bons) >= 60:
        src = np.float32([kb[x.queryIdx].pt for x in bons])
        dst = np.float32([ka[x.trainIdx].pt for x in bons])
        H, inl = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
        if H is None or inl.sum() < 60:
            break
        Hf = H @ np.diag([ESC, ESC, 1.0])
        c = cv2.perspectiveTransform(np.float32([[[0, 0]], [[ES.shape[1], 0]], [[ES.shape[1], ES.shape[0]]], [[0, ES.shape[0]]]]), Hf).reshape(-1, 2)
        lg = (np.linalg.norm(c[1] - c[0]) + np.linalg.norm(c[2] - c[3])) / 2
        al = (np.linalg.norm(c[3] - c[0]) + np.linalg.norm(c[2] - c[1])) / 2
        if lg > 150 and cv2.isContourConvex(np.int32(c)) and 1.1 < al / lg < 1.8:
            out.append(c)
        bons = [x for x, i in zip(bons, inl.ravel()) if not i]
    return out


def ouro(bgr):
    r, g, b = [bgr[..., i].astype(int) for i in (2, 1, 0)]
    return (r > b + 50) & (r > 110) & (r > g)


def faixas(v, minimo):
    """Intervalos contíguos onde v > minimo."""
    on = np.concatenate([[False], v > minimo, [False]])
    d = np.diff(on.astype(int))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def lombada(arte, c):
    largura = np.linalg.norm(c[1] - c[0])
    alt = np.linalg.norm(c[3] - c[0])
    u = (c[0] - c[1]) / largura                  # para fora da capa (esquerda)
    # a borda da capa estimada pela homografia erra alguns px: a faixa cobre dos dois lados
    d, e = 0.15 * largura, 0.09 * largura
    Ws, Hs = int(round(d + e)), int(round(alt))
    # S: x = 0 borda externa, x = Ws já dentro da capa; y desce pela lombada
    dst = np.float32([c[0] + u * d, c[0] - u * e, c[3] - u * e, c[3] + u * d])
    src = np.float32([[0, 0], [Ws, 0], [Ws, Hs], [0, Hs]])
    Hm = cv2.getPerspectiveTransform(src, dst)
    S = cv2.warpPerspective(arte, np.linalg.inv(Hm), (Ws, Hs), flags=cv2.INTER_CUBIC)
    T = np.ascontiguousarray(np.rot90(S))       # leitura horizontal: topo de T = lado da capa
    mo = ouro(T)
    if mo.sum() < 120:
        return arte, None
    # colunas tomadas por um objeto na frente (selo dourado): dourado em quase toda a altura
    cheio = mo.mean(0) > 0.5
    # linhas de texto: densidade de transições ouro/fundo ao longo da lombada (letras alternam
    # cheio e vazio; filete da moldura, aresta e brilho são faixas lisas e quase não alternam)
    x_ = mo[:, ~cheio].astype(np.int8)
    if x_.shape[1] < 20:
        return arte, None
    tr = np.abs(np.diff(x_, axis=1)).sum(1) / x_.shape[1] * 100
    if tr.max() < 3:
        return arte, None
    on = tr >= 0.4 * tr.max()
    on = (np.convolve(on.astype(int), [1, 1, 1], 'same') >= 2) | on   # tapa vão de 1 linha
    linhas = [(a_, b_) for a_, b_ in faixas(on.astype(int), 0) if b_ - a_ >= 3][:2]
    if not linhas:
        return arte, None
    y0l, y1l = linhas[0][0], linhas[-1][1]
    # blocos ao longo da lombada: título (primeiro) e assinatura (depois de um vão grande)
    cols = mo[y0l:y1l].any(0) & ~cheio
    blocos = faixas(cols.astype(int), 0)
    juntos = []
    for a_, b_ in blocos:
        if juntos and a_ - juntos[-1][1] < 0.06 * Hs:
            juntos[-1] = (juntos[-1][0], b_)
        else:
            juntos.append((a_, b_))
    juntos = [j for j in juntos if j[1] - j[0] > 0.02 * Hs]
    if not juntos:
        return arte, None
    # a assinatura "DR. JOÃO PITHON" é o último bloco, curto e separado por vão grande: fica.
    # todo o resto (título PT ou texto embaralhado, inclusive sobras) é apagado.
    fim = len(juntos)
    if len(juntos) > 1:
        a_, b_ = juntos[-1]
        if b_ - a_ < 0.4 * Hs and a_ - juntos[-2][1] > 0.04 * Hs and a_ > 0.55 * Hs:
            fim -= 1
    x0t, x1t = juntos[0][0], juntos[fim - 1][1]
    if cheio[x0t:x1t].any():
        x1t = x0t + int(np.argmax(cheio[x0t:x1t]))
    if x1t - x0t < 0.25 * Hs:                   # pequeno demais para ser o título
        return arte, None
    # textura dourada (recortes 4x4 só de ouro pleno)
    pat = []
    for yy in range(y0l, y1l - 4, 2):
        for xx in range(x0t, x1t - 4, 2):
            if mo[yy:yy + 4, xx:xx + 4].all():
                pat.append(T[yy:yy + 4, xx:xx + 4].copy())
    if len(pat) < 5:
        pat = [np.full((4, 4, 3), np.median(T[mo], 0), np.uint8)]
    # apagar o título antigo
    r_, g_, b_ = [T[..., i].astype(int) for i in (2, 1, 0)]
    halo = (r_ > b_ + 22) & (r_ > 70)           # borda antisserrilhada do dourado
    apaga = np.zeros(mo.shape, np.uint8)
    ya, yb_ = max(0, y0l - 4), y1l + 4
    xa_, xb_ = max(0, x0t - 4), x1t + 4
    apaga[ya:yb_, xa_:xb_] = (halo[ya:yb_, xa_:xb_] & ~cheio[None, xa_:xb_])
    apaga = cv2.dilate(apaga, np.ones((5, 5), np.uint8))
    T2 = cv2.inpaint(T, apaga * 255, 5, cv2.INPAINT_TELEA)
    # escrever o título ES nas mesmas linhas, mesmo corpo (altura de caixa alta = altura da linha)
    textos = TITULO if len(linhas) == 2 else [' '.join(TITULO)]
    larg_max = (x1t - x0t)
    tam = []
    for (a, b), t in zip(linhas, textos):
        cap = b - a
        s = 6
        while ImageFont.truetype(ARIMO, s + 1).getbbox('E', anchor='ls')[1] * -1 <= cap and s < 200:
            s += 1
        tam.append(s)
    s = min(tam)
    f = ImageFont.truetype(ARIMO, s)
    while max(f.getlength(t) for t in textos) > larg_max and s > 6:
        s -= 1
        f = ImageFont.truetype(ARIMO, s)
    mk = Image.new('L', (T.shape[1], T.shape[0]), 0)
    dr = ImageDraw.Draw(mk)
    cx = (x0t + x1t) / 2
    for (a, b), t in zip(linhas, textos):
        dr.text((cx - f.getlength(t) / 2, b), t, font=f, fill=255, anchor='ls')
    rng = np.random.default_rng(11)
    tex = np.zeros_like(T)
    for yy in range(0, T.shape[0], 4):
        for xx in range(0, T.shape[1], 4):
            p = pat[rng.integers(len(pat))]
            tex[yy:yy + 4, xx:xx + 4] = p[:T.shape[0] - yy, :T.shape[1] - xx]
    al = np.array(mk, np.float32)[..., None] / 255
    T3 = (T2 * (1 - al) + tex * al).astype(np.uint8)
    # de volta para a arte, só na região do título
    S3 = np.ascontiguousarray(np.rot90(T3, -1))
    reg = np.zeros((Hs, Ws), np.float32)
    reg_t = np.zeros(T.shape[:2], np.float32)
    reg_t[max(0, y0l - 6):y1l + 6, max(0, x0t - 6):x1t + 6] = 1
    reg = np.ascontiguousarray(np.rot90(reg_t, -1))
    h, w = arte.shape[:2]
    volta = cv2.warpPerspective(S3, Hm, (w, h), flags=cv2.INTER_CUBIC).astype(np.float32)
    mreg = cv2.warpPerspective(reg, Hm, (w, h), flags=cv2.INTER_LINEAR)
    mreg = cv2.GaussianBlur(mreg, (0, 0), 0.8)[..., None]
    out = arte.astype(np.float32) * (1 - mreg) + volta * mreg
    return np.clip(out, 0, 255).astype(np.uint8), (len(linhas), s)


def processar(caminho):
    arte = cv2.imread(caminho)
    feitos = []
    for c in capas(arte):
        arte2, info = lombada(arte, c)
        if info:
            arte = arte2
            feitos.append(info)
    if feitos:
        if caminho.lower().endswith(('.jpg', '.jpeg')):
            cv2.imwrite(caminho, arte, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            cv2.imwrite(caminho, arte)
    print(('lombada ES ' if feitos else 'sem lombada') + f'  {os.path.basename(caminho)} {feitos}')


if __name__ == '__main__':
    alvos = sys.argv[1:] or sorted(glob.glob(os.path.join(SAIDA, '*')))
    for c in alvos:
        if 'Logo' in c or 'Capa Ebook' in c:
            continue
        processar(c)
