"""apaga a legenda pequena gravada (texto branco) na faixa do peito, quadro a quadro, com inpaint."""
import cv2, numpy as np, sys
ent, sai = sys.argv[1], sys.argv[2]; Y0, Y1, X0, X1 = 1330, 1680, 120, 960
cap = cv2.VideoCapture(ent); fps = cap.get(5)
out = cv2.VideoWriter(sai, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1080, 1920))
while True:
    ok, f = cap.read()
    if not ok: break
    roi = f[Y0:Y1, X0:X1]; g = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = ((g > 215) & (hsv[..., 1] < 40)).astype(np.uint8) * 255
    # só traços finos de letra: tira manchas grandes (reflexo, luz)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if h <= 45 and w <= 60 and a <= 900: keep[lab == k] = 255
    if keep.sum() > 255 * 40:
        keep = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        f[Y0:Y1, X0:X1] = cv2.inpaint(roi, keep, 9, cv2.INPAINT_NS)
    out.write(f)
out.release()
