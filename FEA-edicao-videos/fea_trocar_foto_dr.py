#!/usr/bin/env python3
"""FEA: troca a imagem do Dr. no vídeo de entrada pela foto ORIGINAL (sem cara de IA).

O motion da entrada foi feito a partir da foto de estúdio "IMG_1341" (pasta "IMAGENS DR JOÃO" no
Drive), mas com um tratamento que deixou o rosto com aspecto artificial (Keila, 01/11/2026).
O script recorta a foto original (recorte RGBA já pronto), acha em cada quadro onde o Dr. está
(pontos SIFT foto x quadro, transformação de semelhança), ajusta a cor da foto à luz da cena,
mantém os raios de luz que passam NA FRENTE do terno e preserva a fase da silhueta preta e a
entrada da luz (ganho de brilho medido no próprio vídeo).

Uso: python3 fea_trocar_foto_dr.py video_1920x1080.mp4 recorte.png saida.mp4
"""
import subprocess
import sys

import cv2
import numpy as np

W, H = 1920, 1080
RED = 0.5                  # SIFT em meia resolução (mais rápido; M é corrigido para a resolução cheia)
MIN_INLIERS = 40


def quadros(video):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


def main():
    ent, rec_png, sai = sys.argv[1:4]
    rec = cv2.imread(rec_png, cv2.IMREAD_UNCHANGED)
    foto, alfa = rec[..., :3], rec[..., 3]
    sift = cv2.SIFT_create(3000)
    fs = cv2.resize(foto, None, fx=0.45, fy=0.45)  # foto já perto da escala do vídeo
    fa = cv2.resize(alfa, (fs.shape[1], fs.shape[0]))
    k1, d1 = sift.detectAndCompute(cv2.cvtColor(fs, cv2.COLOR_BGR2GRAY), (fa > 128).astype(np.uint8) * 255)
    p1_all = np.float32([k.pt for k in k1]) / 0.45          # em coordenadas da foto original
    bf = cv2.BFMatcher()

    # 1ª passada: transformação foto -> quadro em cada quadro
    Ms, inl = [], []
    for q in quadros(ent):
        g = cv2.cvtColor(cv2.resize(q, None, fx=RED, fy=RED), cv2.COLOR_BGR2GRAY)
        k2, d2 = sift.detectAndCompute(g, None)
        M, ni = None, 0
        if d2 is not None and len(k2) > 10:
            mm = bf.knnMatch(d1, d2, k=2)
            good = [x for x, y in (m for m in mm if len(m) == 2) if x.distance < 0.75 * y.distance]
            if len(good) >= MIN_INLIERS:
                a = p1_all[[x.queryIdx for x in good]]
                b = np.float32([k2[x.trainIdx].pt for x in good]) / RED
                M, msk = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=3)
                ni = int(msk.sum()) if msk is not None else 0
        Ms.append(M if ni >= MIN_INLIERS else None)
        inl.append(ni)
    n = len(Ms)
    print(f"quadros {n}, com Dr. encontrado: {sum(m is not None for m in Ms)}", file=sys.stderr)

    # suaviza os parâmetros (escala, rotação, translação) com mediana móvel, para não tremer
    par = np.full((n, 4), np.nan)
    for i, M in enumerate(Ms):
        if M is not None:
            par[i] = [M[0, 0], M[1, 0], M[0, 2], M[1, 2]]
    sm = par.copy()
    for i in range(n):
        j = par[max(0, i - 3):i + 4]
        j = j[~np.isnan(j[:, 0])]
        if len(j) and not np.isnan(par[i, 0]):
            sm[i] = np.median(j, 0)

    # cor: transfere média/desvio (Lab) do Dr. do vídeo para a foto, num quadro de referência estável
    ref = 360                                 # 12 s: Dr. parado, luz cheia
    while ref < n and np.isnan(sm[ref, 0]):
        ref += 1
    for i, q in enumerate(quadros(ent)):
        if i == ref:
            qref = q.copy()
            break
    def matriz(i):
        a, b, tx, ty = sm[i]
        return np.float32([[a, -b, tx], [b, a, ty]])
    Mr = matriz(ref)
    wf = cv2.warpAffine(foto, Mr, (W, H), flags=cv2.INTER_AREA)
    wa = cv2.warpAffine(alfa, Mr, (W, H)) > 200
    lab_v = cv2.cvtColor(qref, cv2.COLOR_BGR2LAB).astype(np.float32)[wa]
    lab_f = cv2.cvtColor(wf, cv2.COLOR_BGR2LAB).astype(np.float32)[wa]
    mv, sv = lab_v.mean(0), lab_v.std(0)
    mf, sf = lab_f.mean(0), lab_f.std(0)
    FORCA = 0.75                              # 75% da cor da cena, 25% da cor natural da foto
    ganho = 1 + FORCA * (sv / sf - 1)
    alvo_m = mf + FORCA * (mv - mf)
    lum_ref = None

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", "30", "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                            "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy",
                            "-movflags", "+faststart", sai], stdin=subprocess.PIPE)
    for i, q in enumerate(quadros(ent)):
        if np.isnan(sm[i, 0]):
            enc.stdin.write(q.tobytes())
            continue
        M = matriz(i)
        wf = cv2.warpAffine(foto, M, (W, H), flags=cv2.INTER_AREA)
        wa = cv2.warpAffine(alfa, M, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
        wa = cv2.GaussianBlur(wa, (0, 0), 0.8)
        lab = cv2.cvtColor(wf, cv2.COLOR_BGR2LAB).astype(np.float32)
        lab = (lab - mf) * ganho + alvo_m
        cf = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
        qf = q.astype(np.float32)
        # entrada da luz: brilho do Dr. no vídeo em relação ao quadro de referência
        m_dr = wa > 0.8
        lv = qf[m_dr].mean() if m_dr.any() else 0
        if lum_ref is None:
            lum_ref = qref.astype(np.float32)[cv2.warpAffine(alfa, Mr, (W, H)) > 200].mean()
        k = float(np.clip(lv / lum_ref, 0, 1))
        cf = cf * k
        # raios de luz na frente do terno: pixels claros e saturados de ciano no vídeo continuam
        hsv = cv2.cvtColor(q, cv2.COLOR_BGR2HSV)
        raio = ((hsv[..., 0] > 85) & (hsv[..., 0] < 102) & (hsv[..., 1] > 70) & (hsv[..., 2] > 120)).astype(np.float32)
        raio = cv2.GaussianBlur(raio, (0, 0), 2.0)
        a3 = (wa * (1 - raio))[..., None]
        out = cf * a3 + qf * (1 - a3)
        # o brilho do raio soma por cima (como luz), para não ficar recortado
        out = np.maximum(out, qf * raio[..., None])
        enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    print("OK", n, "quadros")


if __name__ == "__main__":
    main()
