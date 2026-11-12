#!/usr/bin/env python3
"""FEA: recorta o fundo branco da foto de um produto (caixa de ácido hialurônico, toxina etc.).

Uso:
    python3 fea_recortar_produto.py foto.jpg saida.png [--limiar 240] [--crop x0,y0,x1,y1] [--convexo]

Sem IA: o fundo é o branco ligado à borda da foto (limiar de brilho e pouca saturação), o que
sobra é o produto. Abertura morfológica tira resto de linha da borda; o alfa é erodido 2 px para
não ficar halo branco em volta da caixa.
--convexo: para caixa branca em fundo branco (ex.: e.p.t.q.), usar limiar alto (251) e o casco
convexo da caixa, que é um polígono convexo.
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage


def recortar(src, dst, limiar=240, crop=None, convexo=False):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    a = np.asarray(im).astype(int)
    obj = ~((a.min(2) >= limiar) & ((a.max(2) - a.min(2)) < 18))
    if not convexo:
        lab, _ = ndimage.label(~obj)
        borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        obj = ~np.isin(lab, list(borda))
    obj = ndimage.binary_opening(obj, iterations=4 if convexo else 1)
    lab, n = ndimage.label(obj)
    if n > 1:
        tam = ndimage.sum(obj, lab, range(1, n + 1))
        obj = np.isin(lab, [i + 1 for i, t in enumerate(tam) if t > (0.5 if convexo else 0.02) * tam.max()])
    obj = ndimage.binary_fill_holes(obj)
    if convexo:
        from scipy.spatial import ConvexHull
        ys, xs = np.where(obj)
        pts = np.c_[xs, ys]
        poly = [tuple(map(float, pts[i])) for i in ConvexHull(pts).vertices]
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
    else:
        m = Image.fromarray((obj * 255).astype("uint8"))
    m = m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.0))
    out = im.copy()
    out.putalpha(m)
    out = out.crop(out.getbbox())
    out.save(dst)
    return out.size


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--limiar", type=int, default=240)
    ap.add_argument("--crop")
    ap.add_argument("--convexo", action="store_true")
    a = ap.parse_args()
    crop = tuple(map(int, a.crop.split(","))) if a.crop else None
    print(a.dst, recortar(a.src, a.dst, a.limiar, crop, a.convexo))
