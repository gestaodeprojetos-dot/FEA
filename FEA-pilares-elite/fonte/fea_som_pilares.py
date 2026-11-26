"""Som suave da animação dos pilares: só o movimento dos círculos e a entrada do Elite.
Cada círculo que desce tem um sopro leve e um toque macio quando encaixa; as palavras ficam
sem som. O Elite entra com um acorde suave que cresce devagar. Sintetizado aqui, sem amostras.
Uso: python3 fea_som_pilares.py saida.wav"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 12.0
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

# mesmos tempos da animação (FEA-pilares-elite.html)
RING_AT, FALL, REVEAL = [0.4, 2.5, 4.6], 1.3, 6.9
LAND = 0.78 * FALL          # quando o círculo encosta no lugar (curva back.out)
PANS = [0.0, -0.35, 0.35]


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); sig = sig[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.41; R[i:i + len(sig)] += sig * gain * r * 1.41


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype='low', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), x)


def descida(dur):
    """sopro de ar suave que acompanha o círculo descendo (filtro vai fechando)"""
    n = int(dur * SR); x = rng.standard_normal(n); t = np.arange(n) / n
    out = np.zeros(n); k = 10
    for j in range(k):
        a, b = j * n // k, (j + 1) * n // k
        c = 2600 * (500 / 2600) ** (j / (k - 1))
        out[a:b] = bp(x, c * .5, c * 1.5)[a:b]
    return out * (np.sin(np.pi * t) ** 2)


def encaixe():
    """toque macio de encaixe: grave curto + leve brilho de vidro, bem baixo"""
    n = int(1.6 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (140 * np.exp(-t * 18) + 90) * t) * np.exp(-t / .09)
    glass = (np.sin(2 * np.pi * 1760 * t) + .4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t / .5) * np.minimum(1, t / .01)
    return lp(thump, 400) * .9 + glass * .08


for t0, pan in zip(RING_AT, PANS):
    add(descida(LAND + .15), t0, pan, .11)
    add(encaixe(), t0 + LAND, pan, .30)

# Elite: acorde suave (Ré maior com nona) crescendo, com um sino delicado
n = int((DUR - REVEAL + .3) * SR); t = np.arange(n) / SR
pad = np.zeros(n)
for f, a in ((146.83, 1), (220.0, .8), (293.66, .7), (369.99, .55), (440.0, .45), (659.25, .25)):
    pad += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * (1 + .15 * np.sin(2 * np.pi * .3 * t + f))
pad = lp(pad, 2200) * np.clip(t / 1.6, 0, 1) ** 1.5
add(pad, REVEAL - .2, 0, .045)
n = int(3.5 * SR); t = np.arange(n) / SR
sino = sum(a * np.sin(2 * np.pi * 1174.66 * m * t) * np.exp(-t / d) for m, a, d in ((1, 1, 1.8), (2.0, .3, .9), (3.0, .12, .5)))
add(sino * np.minimum(1, t / .02), REVEAL + .2, 0, .07)
add(descida(1.4) * .6, REVEAL - .4, 0, .06)

# reverberação leve para tudo soar no mesmo ambiente
ir_n = int(1.8 * SR); ir = bp(rng.standard_normal(ir_n), 200, 7000) * np.exp(-np.arange(ir_n) / SR / .5)
ir /= np.abs(ir).sum() / 5
st = np.stack([L + .4 * fftconvolve(L, ir)[:N], R + .4 * fftconvolve(R, ir)[:N]], 1)
st *= np.clip((DUR - t_all) / .8, 0, 1)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
