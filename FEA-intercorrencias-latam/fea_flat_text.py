"""Troca linhas de texto chapadas (arte achatada) PT -> ES, sem IA generativa.
Remove o texto original por inpainting simples (OpenCV Telea, a partir do entorno), mede a linha original
(altura, largura, peso) ajustando a fonte Advent Pro e reescreve o texto ES com os mesmos parâmetros.
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VF = None
SS = 4  # supersampling


def font(size, wght):
    f = ImageFont.truetype(VF, max(1, int(round(size * SS))))
    f.set_variation_by_axes([100, wght])
    return f


def render(text, size, wght, track, xscale):
    """Máscara float [0,1] na escala final; retorna (máscara, baseline_y_na_máscara)."""
    f = font(size, wght)
    asc, desc = f.getmetrics()
    pad = int(size * SS * 0.6)
    w = int(sum(f.getlength(c) + track * SS for c in text) + 2 * pad)
    h = asc + desc + 2 * pad
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    x = pad
    for c in text:
        d.text((x, pad), c, font=f, fill=255)
        x += f.getlength(c) + track * SS
    a = np.asarray(im).astype(np.float32) / 255
    if xscale != 1:
        a = cv2.resize(a, (max(1, int(a.shape[1] * xscale)), a.shape[0]), interpolation=cv2.INTER_AREA)
    a = cv2.resize(a, (max(1, a.shape[1] // SS), max(1, a.shape[0] // SS)), interpolation=cv2.INTER_AREA)
    return a, (pad + asc) / SS


def ink_box(a, thr=0.35):
    ys, xs = np.where(a > thr)
    return xs.min(), ys.min(), xs.max(), ys.max()


def classify(img, kind):
    b, g, r = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
    if kind == "orange":
        return (r > b + 60) & (r > 120)
    return (b > 150) & (g > 150) & (r > 150) & (np.abs(r - b) < 55)


def fit_line(orig_mask, text, xscale_mode=False, weights=(300, 400, 500, 600, 700)):
    x0, y0, x1, y1 = ink_box(orig_mask.astype(np.float32), 0.5)
    W, H = x1 - x0 + 1, y1 - y0 + 1
    best = None
    for wg in weights:
        lo, hi = 5.0, 400.0
        for _ in range(30):
            mid = (lo + hi) / 2
            a, _ = render(text, mid, wg, 0, 1)
            bx = ink_box(a)
            if bx[3] - bx[1] + 1 > H:
                hi = mid
            else:
                lo = mid
        size = lo
        a, _ = render(text, size, wg, 0, 1)
        bx = ink_box(a)
        w0 = bx[2] - bx[0] + 1
        if xscale_mode:
            track, xs = 0.0, W / w0
        else:
            track, xs = (W - w0) / max(1, len(text) - 1), 1.0
        a, base = render(text, size, wg, track, xs)
        bx = ink_box(a)
        crop = a[bx[1]:bx[3] + 1, bx[0]:bx[2] + 1]
        crop = cv2.resize(crop, (W, H), interpolation=cv2.INTER_LINEAR) > 0.5
        om = orig_mask[y0:y1 + 1, x0:x1 + 1]
        iou = (crop & om).sum() / max(1, (crop | om).sum())
        if best is None or iou > best["iou"]:
            best = dict(iou=iou, w=wg, size=size, track=track, xs=xs,
                        base_abs=y0 + (base - bx[1]), cx=(x0 + x1) / 2, box=(x0, y0, x1, y1))
    return best


def texture_field(img, known):
    """Campo de cor a partir dos pixels conhecidos (letras originais), espalhado por inpainting."""
    unk = (~known).astype(np.uint8) * 255
    return cv2.inpaint(img, unk, 7, cv2.INPAINT_TELEA)


def replace_line(img, region, kind, pt, es, xscale_mode=False, max_w=None, weights=(300, 400, 500, 600, 700),
                 erase_extra=None, log=None, size_scale=1.0, match_width=False):
    X0, Y0, X1, Y1 = region
    crop = img[Y0:Y1, X0:X1].copy()
    m = classify(crop, kind)
    fit = fit_line(m, pt, xscale_mode, weights)
    # 1) apaga o texto PT (inpainting a partir do entorno)
    er = cv2.dilate(m.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    if erase_extra is not None:
        ex0, ey0, ex1, ey1 = erase_extra
        er[ey0 - Y0:ey1 - Y0, ex0 - X0:ex1 - X0] = 255
    if kind == "orange":
        tex = texture_field(crop, cv2.erode(m.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(bool))
    else:
        col = np.median(crop[m], axis=0)
    clean = cv2.inpaint(crop, er, 6, cv2.INPAINT_TELEA)
    # 2) reescreve ES com os mesmos parâmetros
    size = fit["size"] * size_scale
    a, base = render(es, size, fit["w"], fit["track"], fit["xs"])
    bx = ink_box(a)
    wid = bx[2] - bx[0] + 1
    xs = fit["xs"]
    track = fit["track"]
    W_orig = fit["box"][2] - fit["box"][0] + 1
    if match_width and not xscale_mode:
        track = track + (W_orig - wid) / max(1, len(es) - 1)
        a, base = render(es, size, fit["w"], track, xs)
        bx = ink_box(a)
        wid = bx[2] - bx[0] + 1
    if max_w and wid > max_w:
        xs = xs * max_w / wid
        a, base = render(es, size, fit["w"], track, xs)
        bx = ink_box(a)
        wid = bx[2] - bx[0] + 1
    ox = int(round(fit["cx"] - (bx[0] + bx[2]) / 2))
    oy = int(round(fit["base_abs"] - base))
    A = np.zeros(crop.shape[:2], np.float32)
    ys, xs_ = slice(max(0, oy), min(A.shape[0], oy + a.shape[0])), slice(max(0, ox), min(A.shape[1], ox + a.shape[1]))
    A[ys, xs_] = a[ys.start - oy:ys.stop - oy, xs_.start - ox:xs_.stop - ox]
    if kind == "orange":
        fill = tex.astype(np.float32)
        # granulado dourado: mesmo desvio do grão das letras originais
        lum = crop.astype(np.float32).mean(axis=2)
        hp = lum - cv2.GaussianBlur(lum, (0, 0), 2.0)
        sd = float(hp[cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)].std())
        rng = np.random.default_rng(7)
        n = cv2.GaussianBlur(rng.normal(0, 1, A.shape).astype(np.float32), (0, 0), 0.7)
        n = n / (n.std() + 1e-6) * sd
        fill = fill + n[:, :, None]
    else:
        fill = np.zeros_like(crop, np.float32) + col
    out = clean.astype(np.float32) * (1 - A[:, :, None]) + fill * A[:, :, None]
    img[Y0:Y1, X0:X1] = np.clip(out, 0, 255).astype(np.uint8)
    if log is not None:
        log.append(f"{pt!r} -> {es!r}: Advent Pro peso {fit['w']}, corpo {size:.1f}px, tracking {fit['track']:.2f}px, "
                   f"tracking final {track:.2f}px, escala X {xs:.3f}, IoU ajuste {fit['iou']:.2f}, largura ES {wid}px")
    return img
