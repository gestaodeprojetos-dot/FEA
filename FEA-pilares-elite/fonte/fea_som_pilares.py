"""Efeitos sonoros da animação dos pilares (Atrair, Converter, Entregar, Elite).
Tudo sintetizado aqui, sem amostras externas. Uso: python3 fea_som_pilares.py saida.wav"""
import sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR, DUR = 48000, 11.6
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(3)
L = np.zeros(N); Rch = np.zeros(N)


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); sig = sig[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.41; Rch[i:i + len(sig)] += sig * gain * r * 1.41


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), x)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-np.maximum(0, t - a) / d)


def bell(f, dur=2.2, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    parts = [(1, 1, 1.6), (2.0, .45, .9), (2.76, .3 * bright, .6), (5.4, .12 * bright, .3), (8.9, .06 * bright, .18)]
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in parts)
    return s * np.minimum(1, t / .004)


def whoosh(dur, lo=400, hi=5000):
    n = int(dur * SR); x = rng.standard_normal(n)
    t = np.arange(n) / n
    # varredura do filtro de baixo para cima e envelope em arco
    out = np.zeros(n); k = 8
    for j in range(k):
        a, b = j * n // k, (j + 1) * n // k
        c = lo * (hi / lo) ** (j / (k - 1))
        out[a:b] = bp(x, c * .6, min(c * 1.6, 20000))[a:b]
    return out * np.sin(np.pi * t) ** 1.5


# pad ambiente bem baixo (Ré maior com sétima), entra devagar
pad = np.zeros(N)
for f in (146.83, 220.0, 277.18, 329.63, 440.0):
    pad += np.sin(2 * np.pi * f * t_all + rng.uniform(0, 6)) * (1 + .3 * np.sin(2 * np.pi * .13 * t_all + f))
pad = bp(pad, 120, 2500) * np.clip(t_all / 2.5, 0, 1) * np.clip((DUR - t_all) / 1.5, 0, 1) * .035
add(pad, 0)

RING_AT, DRAW = [0.6, 2.4, 4.2], 1.25
NOTES = [880.0, 1108.73, 1318.51]          # Lá, Dó#, Mi: sobe a cada pilar
PANS = [0.0, -0.45, 0.45]
for t0, f, pan in zip(RING_AT, NOTES, PANS):
    add(whoosh(DRAW + .2, 500, 7000), t0 - .05, pan, .22)       # traço do círculo
    add(bell(f, 2.4), t0 + .6, pan, .30)                       # palavra aparece
    add(bell(f * 2, 1.2, .6), t0 + .62, pan, .08)

REVEAL = 6.1
# subida antes do Elite: ruído que cresce + tom subindo
n = int(.9 * SR); tt = np.arange(n) / SR
riser = bp(rng.standard_normal(n), 1500, 12000) * (tt / tt[-1]) ** 2.2 * .5
riser += np.sin(2 * np.pi * (300 * tt + 500 * tt ** 2)) * (tt / tt[-1]) ** 3 * .25
add(riser, REVEAL - .9, 0, .55)
# impacto grave
n = int(2.4 * SR); tt = np.arange(n) / SR
f_sweep = 70 * np.exp(-tt * 3) + 42
boom = np.sin(2 * np.pi * np.cumsum(f_sweep) / SR) * env(n, .005, .7)
boom += bp(rng.standard_normal(n), 60, 400) * env(n, .002, .12) * .6
add(boom, REVEAL, 0, .9)
# brilho do Elite: acorde de sinos + cascata aguda
for f, d in ((587.33, 0), (880.0, .0), (1108.73, .0), (1479.98, .02)):
    add(bell(f, 3.2, .8), REVEAL + d, 0, .17)
for k, f in enumerate([2349.3, 2793.8, 3520.0, 4434.9, 5274.0, 5919.9]):
    add(bell(f, .9, .4), REVEAL + .25 + k * .07, (-1) ** k * .5, .05)
add(whoosh(1.4, 3000, 14000), REVEAL + .05, 0, .12)

# reverberação curta para colar tudo
ir_n = int(1.6 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / .45)
ir = bp(ir, 200, 9000); ir /= np.abs(ir).sum() / 6
L2 = L + .35 * fftconvolve(L, ir)[:N]; R2 = Rch + .35 * fftconvolve(Rch, ir[::-1][::-1])[:N]
st = np.stack([L2, R2], 1)
st *= np.clip((DUR - t_all) / .4, 0, 1)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
