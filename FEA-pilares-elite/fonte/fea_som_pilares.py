"""Som da animação dos pilares, versão sutil.
Só três toques bem leves (um por círculo que encaixa) e, no Elite, um ar suave que cresce devagar
com um único toque delicado. Sem música de fundo, sem som nas palavras.
Tudo sintetizado aqui, sem amostras externas. Uso: python3 fea_som_pilares.py saida.wav"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 12.0
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)

# mesmos tempos da animação (FEA-pilares-elite.html)
RING_AT, FALL, REVEAL = [0.4, 2.5, 4.6], 1.3, 6.9
LAND = 0.78 * FALL
HZ = lambda m: 440 * 2 ** ((m - 69) / 12)


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); sig = sig[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.41; R[i:i + len(sig)] += sig * gain * r * 1.41


def lp(x, f):
    return sosfilt(butter(2, f, btype='low', fs=SR, output='sos'), x)


def toque(f, dur=1.8):
    """toque macio, quase um sino de vidro distante: senoide pura com ataque arredondado"""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + .12 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .3)
    return s * (1 - np.exp(-t / .012)) * np.exp(-t / .55)


def ar(dur):
    """ar suave: ruído rosado bem filtrado, entra e sai devagar"""
    n = int(dur * SR); x = lp(lp(rng.standard_normal(n), 900), 900)
    t = np.arange(n) / n
    return x * np.sin(np.pi * t) ** 2


for t0, m, pan in zip(RING_AT, (74, 78, 81), (0.0, -0.25, 0.25)):   # Ré, Fá#, Lá agudos
    add(toque(HZ(m)), t0 + LAND, pan, .16)

add(ar(3.2), REVEAL - .6, 0, .05)
add(toque(HZ(86), 2.6), REVEAL + .35, 0, .07)                        # Ré bem agudo, único

# ambiência curta e macia
n = int(1.6 * SR); ir = lp(rng.standard_normal(n), 5000) * np.exp(-np.arange(n) / SR / .45)
ir[:int(.015 * SR)] = 0; ir /= np.abs(ir).sum() / 5
st = np.stack([L + .4 * fftconvolve(L, ir)[:N], R + .4 * fftconvolve(R, ir[::-1][::-1] * 1)[:N]], 1)
st *= np.clip((DUR - t_all) / .9, 0, 1)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
