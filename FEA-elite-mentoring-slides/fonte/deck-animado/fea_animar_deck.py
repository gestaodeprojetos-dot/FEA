"""Anima a passagem entre slides seguidos do pitch Elite Mentoring (slides em imagem).

Para cada par (A -> B) gera um MP4 que começa em A e termina exatamente em B:
- entradas: só o que é novo em B se move (pilar sobe, item desliza, linha escreve...)
- viradas: a tela inteira de B entra (flash, zoom suave, scanner)
Uso: python3 fea_animar_deck.py PASTA_IMAGENS PASTA_SAIDA [slide ...]
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

IMG, OUT = sys.argv[1], sys.argv[2]
FPS = 30
W, H = 1920, 1080

# estilo de cada slide (número do slide B; A é o anterior)
PLAN = {}
for b in (4, 5, 6, 30, 31, 51, 52, 53, 54): PLAN[b] = 'up'
for b in (8, 9, 11, 12, 15, 16, 18, 19, 65, 80, 81, 82, 84, 85): PLAN[b] = 'left'
for b in (22, 23, 24, 27, 28, 38, 39, 42, 44, 45, 46, 47, 72, 73, 74, 75, 76, 88): PLAN[b] = 'rise'
for b in (57, 58, 59, 60, 61, 91, 97): PLAN[b] = 'pop'
for b in (93, 94, 95, 96): PLAN[b] = 'wipe'
for b in (48, 49, 99, 100, 103, 106, 108, 110, 111, 112, 114): PLAN[b] = 'flash'
for b in (33, 55, 67, 69, 105, 113, 118): PLAN[b] = 'push'
PLAN[2] = 'scan'
DUR = {'up': 1.0, 'left': .8, 'rise': .8, 'pop': .7, 'wipe': .8, 'flash': 1.1, 'push': 1.6, 'scan': 1.8}

ease = lambda x: 1 - (1 - np.clip(x, 0, 1)) ** 3            # power3.out
ease_io = lambda x: np.where(x < .5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)


def load(i):
    return np.asarray(Image.open(f'{IMG}/s{i:03d}.jpg').convert('RGB').resize((W, H)), dtype=np.float32)


def shift(img, dx, dy):
    """desloca a imagem (sub-pixel por interpolação linear) preenchendo com a borda"""
    return ndimage.shift(img, (dy, dx, 0) if img.ndim == 3 else (dy, dx), order=1, mode='nearest')


def new_mask(a, b):
    d = np.abs(a - b).max(axis=2) > 20
    d = ndimage.binary_opening(d, iterations=1)
    d = ndimage.binary_closing(d, iterations=6)
    d = ndimage.binary_dilation(d, iterations=8)
    lab, n = ndimage.label(d)
    boxes = ndimage.find_objects(lab)
    m = ndimage.gaussian_filter(d.astype(np.float32), 3)
    return np.clip(m * 1.4, 0, 1), lab, boxes


def frames_build(a, b, style, n):
    m, lab, boxes = new_mask(a, b)
    yy, xx = np.mgrid[0:H, 0:W]
    for f in range(n):
        t = f / (n - 1)
        if style == 'rise':
            p = ease(t); dy = 34 * (1 - p)
            layer, mm = shift(b, 0, dy), shift(m, 0, dy) * p
        elif style == 'left':
            p = ease(t); dx = -44 * (1 - p)
            layer, mm = shift(b, dx, 0), shift(m, dx, 0) * p
        elif style == 'pop':
            p = ease(t); s = .86 + .14 * p
            layer, mm = b.copy(), np.zeros_like(m)
            for k, bx in enumerate(boxes, 1):
                cy, cx = (bx[0].start + bx[0].stop) / 2, (bx[1].start + bx[1].stop) / 2
                z = ndimage.affine_transform(b, np.diag([1 / s, 1 / s, 1]), offset=(cy - cy / s, cx - cx / s, 0), order=1, mode='nearest')
                zm = ndimage.affine_transform(m * (lab == k), np.diag([1 / s, 1 / s]), offset=(cy - cy / s, cx - cx / s), order=1)
                layer = np.where(zm[..., None] > 0, z, layer); mm = np.maximum(mm, zm * p)
        elif style in ('up', 'wipe'):
            p = ease_io(t) if style == 'up' else ease(t)
            reveal = np.zeros_like(m)
            for k, bx in enumerate(boxes, 1):
                y0, y1, x0, x1 = bx[0].start, bx[0].stop, bx[1].start, bx[1].stop
                if style == 'up':
                    edge = y1 - (y1 - y0) * p; soft = np.clip((yy - edge) / 24 + 1, 0, 1)
                else:
                    edge = x0 + (x1 - x0) * p; soft = np.clip((edge - xx) / 40 + 1, 0, 1)
                reveal = np.maximum(reveal, soft * (lab == k))
            layer, mm = b, m * ndimage.gaussian_filter(reveal, 2)
            # linha de luz na frente que avança
            if style == 'up' and t < 1:
                glow = np.zeros_like(m)
                for k, bx in enumerate(boxes, 1):
                    y0, y1 = bx[0].start, bx[0].stop
                    edge = y1 - (y1 - y0) * p
                    glow = np.maximum(glow, np.exp(-((yy - edge) / 10) ** 2) * (lab == k))
                layer = layer + glow[..., None] * np.array([90, 200, 200]) * (1 - p)
        # brilho do elemento novo no meio da entrada
        bloom = np.sin(np.pi * t) * .12
        layer = layer * (1 + bloom)
        yield np.clip(a * (1 - mm[..., None]) + layer * mm[..., None], 0, 255)


def frames_full(a, b, style, n):
    yy = np.mgrid[0:H, 0:W][0]
    for f in range(n):
        t = f / (n - 1)
        if style == 'flash':
            p = ease(t); s = 1.07 - .07 * p
            z = ndimage.affine_transform(b, np.diag([1 / s, 1 / s, 1]), offset=(H / 2 - H / 2 / s, W / 2 - W / 2 / s, 0), order=1, mode='nearest') if t < 1 else b
            mix = np.clip(t / .18, 0, 1)
            fl = (t / .18 if t < .18 else np.clip(1 - (t - .18) / .35, 0, 1)) * .55
            img = a * (1 - mix) + z * mix
            img = img + (255 - img) * fl * np.array([.75, 1, 1])
        elif style == 'push':
            p = ease(t); s = 1.08 - .08 * p
            z = ndimage.affine_transform(b, np.diag([1 / s, 1 / s, 1]), offset=(H / 2 - H / 2 / s, W / 2 - W / 2 / s, 0), order=1, mode='nearest') if t < 1 else b
            mix = ease_io(np.clip(t / .55, 0, 1))
            img = a * (1 - mix) + z * mix
        elif style == 'scan':
            p = ease_io(t); edge = p * (H + 80) - 40
            rev = np.clip((edge - yy) / 30 + .5, 0, 1)[..., None]
            img = a * (1 - rev) + b * rev
            line = np.exp(-((yy - edge) / 4) ** 2)[..., None] * np.array([134, 249, 248]) * (1 - t) * 1.2
            beam = (np.clip((edge - yy) / 220, 0, 1) * (yy < edge) * np.exp(-(edge - yy) / 120))[..., None] * np.array([40, 110, 110]) * (1 - t)
            img = img + line + beam
        yield np.clip(img, 0, 255)


def render(bnum):
    style = PLAN[bnum]
    a, b = load(bnum - 1), load(bnum)
    n = int(DUR[style] * FPS) + 1
    gen = frames_full if style in ('flash', 'push', 'scan') else frames_build
    out = f'{OUT}/FEA-elite-anim-slide-{bnum:03d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    last = None
    for fr in gen(a, b, style, n):
        last = fr.astype(np.uint8); p.stdin.write(last.tobytes())
    # segura o quadro final idêntico a B por 0,2 s
    for _ in range(6): p.stdin.write(b.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    print(bnum, style, flush=True)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    todo = [int(x) for x in sys.argv[3:]] or sorted(PLAN)
    for bnum in todo:
        render(bnum)
