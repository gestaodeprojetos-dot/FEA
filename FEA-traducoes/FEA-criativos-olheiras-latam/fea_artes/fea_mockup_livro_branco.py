#!/usr/bin/env python3
"""Ads 13, 14 e 15 (png PTO): o mockup do livro branco tem capa em português com letras
gigantes giradas que vazam da capa. Aqui a face do livro inteira recebe a capa ES real
(trabalho/capa-es.png) em perspectiva, sem IA generativa: a quina é medida no original
(máscara do papel branco + vão escuro entre face e lombada) e a luz da face original
(sombra e brilho do papel) é reaplicada sobre a capa nova.
Rodar depois dos scripts de criativo (rodar_todos.py chama no final).
"""
import os
import cv2, numpy as np

AQ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQ), 'FEA-artes-ES')
ES = cv2.imread(os.path.join(AQ, 'trabalho', 'capa-es.png'))
ALVOS = [(f'trabalho/pto{n}-{t}.png', f'FEA-Ads {n} - PTO-LATAM - {T}.png')
         for n in (13, 14, 15) for t, T in (('feed', 'Feed'), ('story', 'Story'))]


def quina(orig):
    g = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY).astype(int)
    hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    papel = ((hsv[..., 1] < 40) & (g > 170)).astype(np.uint8)
    papel = cv2.morphologyEx(papel, cv2.MORPH_CLOSE, np.ones((25, 25)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(papel)
    i = 1 + int(np.argmax(st[1:, 4]))
    m = lab == i
    x0, y0, w, h = st[i][:4]
    # borda direita da face: vão escuro entre face e lombada, linha a linha
    # só a metade de cima: embaixo as letras douradas gigantes confundem o vão
    pts = []
    for y in range(y0 + 20, y0 + int(0.55 * h), 4):
        cols = np.where(m[y])[0]
        if len(cols) < 50:
            continue
        xr = cols.max()
        seg = g[y, xr - 90:xr + 1]
        esc = np.where(seg < 165)[0]
        if len(esc):
            pts.append((xr - 90 + esc[0], y))
    pts = np.array(pts, np.float32)
    # ajuste robusto x = a*y + b
    melhor = None
    for i in range(len(pts)):
        for j in range(i + 5, len(pts), 3):
            (xa, ya), (xb, yb) = pts[i], pts[j]
            aa = (xb - xa) / (yb - ya); bb_ = xa - aa * ya
            n_ok = int((np.abs(pts[:, 0] - (aa * pts[:, 1] + bb_)) < 3).sum())
            if melhor is None or n_ok > melhor[0]:
                melhor = (n_ok, aa, bb_)
    _, a, b = melhor
    ok = np.abs(pts[:, 0] - (a * pts[:, 1] + b)) < 3
    a, b = np.polyfit(pts[ok, 1], pts[ok, 0], 1)
    # borda esquerda, topo e base a partir do contorno da máscara
    ys = np.arange(y0, y0 + h)
    esq = np.array([(np.where(m[y])[0].min() if m[y].any() else -1, y) for y in ys])
    esq = esq[esq[:, 0] >= 0]
    mid = esq[(esq[:, 1] > y0 + 0.15 * h) & (esq[:, 1] < y0 + 0.85 * h)]
    al, bl = np.polyfit(mid[:, 1], mid[:, 0], 1)
    def borda(lado):
        xs = np.arange(x0 + int(0.1 * w), x0 + int(0.6 * w))
        yy = [(np.where(m[:, x])[0].min() if lado == 'topo' else np.where(m[:, x])[0].max()) for x in xs]
        return np.polyfit(xs, yy, 1)
    at, bt = borda('topo')
    ab, bb = borda('base')
    def cruza(ax, bx, ay, by):          # x = ax*y + bx ; y = ay*x + by
        y = (ay * bx + by) / (1 - ay * ax)
        return (ax * y + bx, y)
    return np.float32([cruza(al, bl, at, bt), cruza(a, b, at, bt), cruza(a, b, ab, bb), cruza(al, bl, ab, bb)])


def aplicar(orig, arte, Q):
    h, w = arte.shape[:2]
    lado = np.linalg.norm(Q[1] - Q[0])
    k = lado / ES.shape[1]
    es = cv2.resize(ES, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
    src = np.float32([[0, 0], [es.shape[1], 0], [es.shape[1], es.shape[0]], [0, es.shape[0]]])
    H = cv2.getPerspectiveTransform(src, Q)
    we = cv2.warpPerspective(es, H, (w, h), flags=cv2.INTER_LINEAR).astype(np.float32)
    mask = np.zeros((h * 4, w * 4), np.uint8)
    cv2.fillConvexPoly(mask, np.int32(np.round(Q * 4)), 255)
    mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    # oclusão: caixa cinza chapada (preço) que passa na frente do livro. Só conta o que é
    # cinza-escuro liso e também existe fora da face; a etiqueta escura da capa fica toda dentro.
    gg = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dv = np.sqrt(np.clip(cv2.blur(gg * gg, (5, 5)) - cv2.blur(gg, (5, 5)) ** 2, 0, None))
    sat = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)[..., 1]
    liso = ((gg > 20) & (gg < 70) & (dv < 2.5) & (sat < 25)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(liso, 4)
    dentro = mask > 0.5
    frente = np.zeros_like(dentro)
    for i in range(1, n):
        comp = lab == i
        fora = (comp & ~dentro).sum()
        if st[i][4] > 400 and fora > 200 and (comp & dentro).sum() > 0:
            frente |= comp
    mask[frente] = 0
    # luz do papel original (só pixels brancos), suavizada
    g = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY).astype(np.float32)
    hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    papel = ((hsv[..., 1] < 40) & (g > 170)).astype(np.float32) * mask
    sig = max(8, lado * 0.06)
    luz = cv2.GaussianBlur(g * papel, (0, 0), sig) / (cv2.GaussianBlur(papel, (0, 0), sig) + 1e-3)
    ref = np.median(g[papel > 0])
    fator = np.clip(luz / ref, 0.6, 1.25)[..., None]
    novo = np.clip(we * fator, 0, 255)
    out = arte.astype(np.float32) * (1 - mask[..., None]) + novo * mask[..., None]
    # lombada: papel à direita da face vira verde da capa ES, com a curvatura de luz do original
    cheio = cv2.morphologyEx(((hsv[..., 1] < 40) & (g > 170)).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25)))
    yy, xx = np.mgrid[0:h, 0:w]
    xa = Q[1][0] + (yy - Q[1][1]) * (Q[2][0] - Q[1][0]) / (Q[2][1] - Q[1][1])
    R, G_, B = [orig[..., i].astype(int) for i in (2, 1, 0)]
    neutro = hsv[..., 1] < 40
    # faixa amarela lisa do fundo: cor parecida com o dourado, mas sem a textura da folha de ouro
    gf = g.astype(np.float32)
    desvio = np.sqrt(np.clip(cv2.blur(gf * gf, (5, 5)) - cv2.blur(gf, (5, 5)) ** 2, 0, None))
    faixa = (R > 235) & (G_ > 195) & (B < 170) & (desvio < 5)
    ouro = (R > B + 50) & ~faixa          # letra dourada, não a faixa amarela
    lomb = (xx > xa - 2) & (xx < xa + 70) & (neutro | ouro) & (yy > Q[1][1] - 4) & (yy < Q[2][1] + 6)
    lomb = cv2.morphologyEx(lomb.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3)))
    lomb = cv2.morphologyEx(lomb, cv2.MORPH_CLOSE, np.ones((9, 9)))
    lomb = (cv2.dilate(lomb, np.ones((3, 3))) > 0) & ~faixa & (xx > xa - 2) & (xx < xa + 70)
    # borda de baixo do livro (espessura das folhas sob a face): mesmo tratamento
    yb = Q[3][1] + (xx - Q[3][0]) * (Q[2][1] - Q[3][1]) / (Q[2][0] - Q[3][0])
    base = (yy > yb - 2) & (yy < yb + 10) & (xx > Q[3][0] - 3) & (xx < xa + 70) & ((g > 60) | ouro) & ~faixa & ~frente
    lomb = lomb | base
    if lomb.any():
        verde = np.median(ES[:, 40:90].reshape(-1, 3), 0).astype(np.float32)
        # perfil de luz por coluna relativa à aresta (só papel branco, sem letras)
        dx = np.clip((xx - xa).astype(int), 0, 70)
        pb = neutro & lomb
        perfil = np.array([np.median(g[pb & (dx == d)]) if (pb & (dx == d)).sum() > 20 else np.nan for d in range(71)])
        ok = ~np.isnan(perfil)
        perfil = np.interp(np.arange(71), np.where(ok)[0], perfil[ok]) if ok.any() else np.full(71, ref)
        f = np.clip(perfil[dx] / ref, 0.5, 1.3)[..., None]
        cor = np.clip(verde * 1.6 * f, 0, 255)
        sm = cv2.GaussianBlur(lomb.astype(np.float32), (0, 0), 0.8)[..., None]
        out = out * (1 - sm) + cor * sm
    # fiapos dourados/brancos que sobram na aresta face-lombada e na borda de baixo: inpainting clássico
    o8 = np.clip(out, 0, 255).astype(np.uint8)
    r2, g2, b2 = [o8[..., i].astype(int) for i in (2, 1, 0)]
    claro = ((r2 > b2 + 30) & (r2 > 80)) | ((r2 > 130) & (g2 > 130) & (b2 > 130))
    banda = ((xx > xa - 9) & (xx < xa + 70) & (yy > Q[1][1] - 4) & (yy < Q[2][1] + 10)) | \
            ((yy > yb - 3) & (yy < yb + 12) & (xx > Q[3][0] + 4) & (xx < xa + 70))
    xl = Q[0][0] + (yy - Q[0][1]) * (Q[3][0] - Q[0][0]) / (Q[3][1] - Q[0][1])
    banda |= (xx > xl - 10) & (xx < xl + 2) & (yy > Q[0][1] - 4) & (yy < Q[3][1] + 4)
    fiapo = (claro & banda & ~faixa).astype(np.uint8)
    if fiapo.any():
        fiapo = cv2.dilate(fiapo, np.ones((3, 3)))
        o8 = cv2.inpaint(o8, fiapo, 3, cv2.INPAINT_TELEA)
    return o8


if __name__ == '__main__':
    for o, s in ALVOS:
        po, ps = os.path.join(AQ, o), os.path.join(SAIDA, s)
        orig, arte = cv2.imread(po), cv2.imread(ps)
        if orig is None or arte is None:
            print('ausente', o, s); continue
        Q = quina(orig)
        cv2.imwrite(ps, aplicar(orig, arte, Q))
        print('livro ES', s, np.round(Q).astype(int).tolist())
