#!/usr/bin/env python3
"""Troca a capa verde PT ("PREENCHIMENTO TRIDIMENSIONAL DE OLHEIRAS") pela capa ES
em todos os mockups das artes de FEA-artes-ES. Sem IA generativa.

Como funciona: localiza a capa PT em cada arte por correspondência de pontos (SIFT +
homografia RANSAC) contra trabalho/capa-br.png, projeta a capa BR e a ES na mesma
perspectiva e soma à arte só a diferença (ES menos BR). Assim luz, reflexo, sombra e
textura do mockup ficam intactos e muda apenas o texto que difere. Onde algo cobre a
capa (selo, tablet, mão), a capa BR projetada não confere com a arte e nada é alterado.
Rodar depois dos scripts de criativo (rodar_todos.py chama no final).
"""
import glob, os, sys
import cv2, numpy as np

AQ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQ), 'FEA-artes-ES')
BR = cv2.imread(os.path.join(AQ, 'trabalho', 'capa-br.png'))
ES = cv2.imread(os.path.join(AQ, 'trabalho', 'capa-es.png'))
# só o bloco do título e subtítulo muda entre BR e ES (dentro da moldura dourada)
ZONA = (215, 205, 1675, 890)   # x0, y0, x1, y1 na capa em resolução cheia
sift = cv2.SIFT_create(nfeatures=6000)
ESC = 0.5
br_s = cv2.resize(BR, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_AREA)
kb, db = sift.detectAndCompute(cv2.cvtColor(br_s, cv2.COLOR_BGR2GRAY), None)


def achar(arte):
    """Lista de homografias (capa BR em escala ESC -> arte) para cada ocorrência da capa."""
    g = cv2.cvtColor(arte, cv2.COLOR_BGR2GRAY)
    ka, da = sift.detectAndCompute(g, None)
    if da is None or len(ka) < 10:
        return []
    m = cv2.BFMatcher().knnMatch(db, da, k=2)
    bons = [a for a, b in (p for p in m if len(p) == 2) if a.distance < 0.75 * b.distance]
    achados = []
    while len(bons) >= 25:
        src = np.float32([kb[x.queryIdx].pt for x in bons])
        dst = np.float32([ka[x.trainIdx].pt for x in bons])
        H, inl = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
        if H is None or inl.sum() < 25:
            break
        achados.append((H, int(inl.sum())))
        bons = [x for x, i in zip(bons, inl.ravel()) if not i]
    return achados


def aplicar(arte, H):
    h, w = arte.shape[:2]
    S = np.diag([ESC, ESC, 1.0])
    Hf = H @ S                      # capa em resolução cheia -> arte
    # área projetada da capa na arte; capa muito pequena ou degenerada: ignora
    cant = cv2.perspectiveTransform(np.float32([[[0, 0]], [[BR.shape[1], 0]], [[BR.shape[1], BR.shape[0]]], [[0, BR.shape[0]]]]), Hf)
    area = cv2.contourArea(cant)
    if area < 60 * 80 or not cv2.isContourConvex(cant.astype(np.int32)):
        return arte, 0
    # reduzir a capa antes do warp evita serrilhado (amostragem em escala parecida)
    lado = np.sqrt(area / (BR.shape[0] * BR.shape[1]))
    k = max(lado, 0.05)
    Hk = Hf @ np.diag([1 / k, 1 / k, 1.0])
    br = cv2.resize(BR, None, fx=k, fy=k, interpolation=cv2.INTER_AREA).astype(np.float32)
    es = cv2.resize(ES, None, fx=k, fy=k, interpolation=cv2.INTER_AREA).astype(np.float32)
    wb = cv2.warpPerspective(br, Hk, (w, h), flags=cv2.INTER_LINEAR)
    we = cv2.warpPerspective(es, Hk, (w, h), flags=cv2.INTER_LINEAR)
    zona = np.zeros(BR.shape[:2], np.float32)
    zona[ZONA[1] + 20:ZONA[3] - 20, ZONA[0] + 20:ZONA[2] - 20] = 255
    zona = cv2.GaussianBlur(zona, (0, 0), 8)
    zona = cv2.resize(zona, (br.shape[1], br.shape[0]), interpolation=cv2.INTER_AREA)
    wz = cv2.warpPerspective(zona, Hk, (w, h)).astype(np.float32) / 255
    a = arte.astype(np.float32)
    # oclusão: compara em escala grossa (tolera serrilhado e leve desalinho do texto);
    # selo, tablet ou mão sobre a capa ficam de fora
    dif = np.abs(cv2.GaussianBlur(a, (0, 0), 4) - cv2.GaussianBlur(wb, (0, 0), 4)).mean(2)
    conf = np.clip((70 - dif) / 30, 0, 1)
    conf = cv2.morphologyEx(conf, cv2.MORPH_CLOSE, np.ones((9, 9)))
    conf = cv2.GaussianBlur(cv2.erode(conf, np.ones((3, 3))), (0, 0), 1.5)
    # luz do mockup (brilho, reflexo, sombra): comparação local arte x capa plana em escala
    # grossa, separada para o fundo e para as letras douradas (cada uma com seu tom)
    sig = max(8, 0.03 * np.sqrt(area))

    def ouro(x):
        r_, g_, b_ = x[..., 2], x[..., 1], x[..., 0]
        return ((r_ > 110) & (r_ > b_ + 45)).astype(np.float32)

    def media(x, m):
        return cv2.GaussianBlur(x * m[..., None], (0, 0), sig) / (cv2.GaussianBlur(m, (0, 0), sig)[..., None] + 1e-3)

    def tom(m):
        ba, bb = media(a, m), media(wb, m)
        g = np.clip((ba + 20) / (bb + 20), 0.5, 1.8)
        return g, np.clip(ba - bb * g, -40, 40)

    ob = ouro(wb)
    gF, lF = tom(cv2.erode(1 - ob, np.ones((3, 3))))
    gL, lL = tom(cv2.erode(ob, np.ones((2, 2))))
    oe = cv2.GaussianBlur(ouro(we), (0, 0), 0.7)[..., None]
    novo = oe * (we * gL + lL) + (1 - oe) * (we * gF + lF)
    peso = (wz * conf)[..., None]
    out = a * (1 - peso) + peso * np.clip(novo, 0, 255)
    return np.clip(out, 0, 255).astype(np.uint8), float((wz * conf).sum() / max(wz.sum(), 1))


def processar(caminho, relatar=True):
    arte = cv2.imread(caminho)
    achados = achar(arte)
    feitos = []
    for H, n in achados:
        arte2, cob = aplicar(arte, H)
        if cob > 0.2:
            arte = arte2
            feitos.append((n, round(cob, 2)))
    if feitos:
        if caminho.lower().endswith(('.jpg', '.jpeg')):
            cv2.imwrite(caminho, arte, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            cv2.imwrite(caminho, arte)
    if relatar:
        print(('capa ES ' if feitos else 'sem capa') + f'  {os.path.basename(caminho)} {feitos}')
    return feitos


if __name__ == '__main__':
    alvos = sys.argv[1:] or sorted(glob.glob(os.path.join(SAIDA, '*')))
    for c in alvos:
        if 'Logo' in c or 'Capa Ebook' in c:
            continue
        processar(c)
