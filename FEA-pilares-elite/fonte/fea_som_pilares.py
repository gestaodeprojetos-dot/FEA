"""Som da animação dos pilares, versão musical: piano suave + cordas leves.
Cada círculo que encaixa toca uma nota de piano (as três notas formam um acorde de Ré maior);
o Elite entra com o acorde completo, arpejado devagar, sobre uma cama de cordas bem baixa.
As palavras ficam sem som. Tudo sintetizado aqui, sem amostras externas.
Uso: python3 fea_som_pilares.py saida.wav"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 12.0
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

# mesmos tempos da animação (FEA-pilares-elite.html)
RING_AT, FALL, REVEAL = [0.4, 2.5, 4.6], 1.3, 6.9
LAND = 0.78 * FALL
NOTE = lambda name: 440 * 2 ** ((name - 69) / 12)            # número MIDI -> Hz


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); sig = sig[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.41; R[i:i + len(sig)] += sig * gain * r * 1.41


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype='low', fs=SR, output='sos'), x)


def piano(f, dur=4.0, vel=.7):
    """piano de feltro: parciais levemente inarmônicos, duas cordas com batimento, martelo macio"""
    n = int(dur * SR); t = np.arange(n) / SR
    B = 0.00025; s = np.zeros(n)
    for k in range(1, 13):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 9000: break
        amp = (1 / k ** 1.25) * np.exp(-(k - 1) * (1.15 - vel * .6) * .35)
        tau = 2.6 / k ** .75
        for det in (-.6, .6):                                  # duas cordas, leve batimento
            s += amp * .5 * np.sin(2 * np.pi * (fk + det * (1 + k * .1)) * t + rng.uniform(0, 6)) * np.exp(-t / tau)
    hammer = lp(rng.standard_normal(n), 2500) * np.exp(-t / .006) * .15
    s = (s + hammer) * np.minimum(1, t / .003) * np.exp(-np.maximum(0, t - dur + .6) / .25)
    return lp(s, 3500 + 3000 * vel)


def cordas(freqs, dur):
    """cama de cordas suave: dente de serra filtrado com coro lento"""
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-.18, 0, .21):
            ph = 2 * np.pi * f * (1 + det / 100) * t + 0.002 * np.sin(2 * np.pi * .4 * t + f)
            s += ((ph / (2 * np.pi)) % 1 * 2 - 1)
    return lp(lp(s, 1400), 1400)


# notas dos três encaixes: Ré, Fá#, Lá (sobe e forma o acorde)
for t0, m, pan in zip(RING_AT, (62, 66, 69), (0.0, -0.3, 0.3)):
    add(piano(NOTE(m), 4.0, .55), t0 + LAND, pan, .32)
    add(piano(NOTE(m + 12), 3.0, .4), t0 + LAND + .012, pan, .10)   # oitava bem discreta

# Elite: acorde de Ré maior com nona, arpejado devagar
for k, m in enumerate((38, 50, 57, 62, 66, 69, 76)):
    add(piano(NOTE(m), 5.2, .5 if m > 45 else .4), REVEAL + .05 + k * .085, (k - 3) * .12, .2 if m > 45 else .26)
n = int((DUR - REVEAL + .4) * SR); env = np.clip(np.arange(n) / SR / 1.8, 0, 1) ** 2
add(cordas([NOTE(m) for m in (50, 57, 62, 66)], n / SR) * env, REVEAL - .3, 0, .018)

# reverberação de sala (decaimento longo, estéreo)
def ir(seed):
    r = np.random.default_rng(seed); n = int(2.6 * SR); t = np.arange(n) / SR
    x = r.standard_normal(n) * np.exp(-t / .7); x = lp(x, 6000)
    x[:int(.02 * SR)] = 0                                         # pré-atraso
    return x / np.abs(x).sum() * 6
L2 = L + .45 * fftconvolve(L, ir(1))[:N]; R2 = R + .45 * fftconvolve(R, ir(2))[:N]
st = np.stack([L2, R2], 1)
st *= np.clip((DUR - t_all) / .9, 0, 1)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
