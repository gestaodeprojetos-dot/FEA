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
    pts = []
    for y in range(y0 + 20, y0 + h - 40, 6):
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
    a, b = np.polyfit(pts[:, 1], pts[:, 0], 1)
    res = np.abs(pts[:, 0] - (a * pts[:, 1] + b))
    ok = res < 4
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
    return out.astype(np.uint8)


if __name__ == '__main__':
    for o, s in ALVOS:
        po, ps = os.path.join(AQ, o), os.path.join(SAIDA, s)
        orig, arte = cv2.imread(po), cv2.imread(ps)
        if orig is None or arte is None:
            print('ausente', o, s); continue
        Q = quina(orig)
        cv2.imwrite(ps, aplicar(orig, arte, Q))
        print('livro ES', s, np.round(Q).astype(int).tolist())
