"""Som da animação dos pilares, versão "encaixe": sem notas musicais.
Cada círculo: sucção invertida durante a descida + clique de encaixe seco (peça travando).
Elite: prato invertido subindo + impacto grave abafado + faíscas finas. Palavras sem som.
Tudo sintetizado aqui, sem amostras externas. Uso: python3 som_encaixe.py saida.wav"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 12.0
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(21)
L = np.zeros(N); R = np.zeros(N)

RING_AT, FALL, REVEAL = [0.4, 2.5, 4.6], 1.3, 6.9
LAND = 0.78 * FALL


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR)
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.41; R[i:i + len(sig)] += sig * gain * r * 1.41


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output='sos'), x)


def succao(dur):
    """ruído com cauda invertida: cresce e corta seco no encaixe"""
    n = int(dur * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), 'band', [800, 6000]) * np.exp(-t / (dur * .35))
    return x[::-1]


def clique():
    """encaixe: dois transientes (clique-claque) + ressonância metálica curta + corpo grave"""
    n = int(.5 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for d, a in ((0, 1.0), (.016, .6)):
        i = int(d * SR); m = n - i; tt = t[:m]
        burst = filt(rng.standard_normal(m), 'high', 2500) * np.exp(-tt / .004)
        metal = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / dec) for f, dec in ((2150, .06), (3420, .045), (5230, .03))) * .25
        s[i:] += a * (burst + metal)
    body = np.sin(2 * np.pi * 115 * t) * np.exp(-t / .05) * .7
    return s + body


def prato_invertido(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), 'high', 4000) * np.exp(-t / (dur * .3))
    return x[::-1]


for t0, pan in zip(RING_AT, (0.0, -0.4, 0.4)):
    add(succao(.55), t0 + LAND - .55, pan, .16)
    add(clique(), t0 + LAND, pan, .42)

add(prato_invertido(1.3), REVEAL + .15 - 1.3, 0, .12)
n = int(1.6 * SR); t = np.arange(n) / SR
impacto = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 8)) * t) * np.exp(-t / .45) * np.minimum(1, t / .004)
impacto += filt(rng.standard_normal(n), 'low', 300) * np.exp(-t / .08) * .5
add(impacto, REVEAL + .15, 0, .55)
for k in range(26):                                                   # faíscas finas, bem baixas
    f = rng.uniform(5000, 9500); n = int(.25 * SR); t = np.arange(n) / SR
    add(np.sin(2 * np.pi * f * t) * np.exp(-t / .05), REVEAL + .25 + rng.exponential(.45), rng.uniform(-.8, .8), .02)

# sala pequena e seca, só para dar corpo
n = int(.9 * SR); ir = filt(rng.standard_normal(n), 'low', 7000) * np.exp(-np.arange(n) / SR / .18)
ir /= np.abs(ir).sum() / 4
st = np.stack([L + .3 * fftconvolve(L, ir)[:N], R + .3 * fftconvolve(R, ir)[:N]], 1)
st *= np.clip((DUR - t_all) / .9, 0, 1)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
