"""Trilha original da contagem regressiva (10 s, 48 kHz, estéreo), sincronizada com o template.

Marcos: 0-2 s tique-taque + riser | 2,0 s impacto (número) | 4,6 s impacto (logo) | 8,2 s brilho final.
Síntese 100% própria (sem sample de terceiros), então não há risco de direito autoral.
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
import os

SR = 48000
DUR = 10.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)


def env_exp(start, decay, attack=0.004):
    e = np.zeros(N)
    m = t >= start
    tt = t[m] - start
    e[m] = (1 - np.exp(-tt / attack)) * np.exp(-tt / decay)
    return e


def lp(x, f, o=4):
    return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, o=4):
    return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, o=4):
    return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)


def saw(freq_t):
    ph = np.cumsum(freq_t) / SR
    return 2 * (ph - np.floor(ph + 0.5))


def fade(a, b):
    return np.clip((t - a) / (b - a), 0, 1) if b > a else np.ones(N)


dry_L = np.zeros(N); dry_R = np.zeros(N)
send = np.zeros(N)  # mono para reverb


def add(x, pan=0.0, rev=0.0):
    global dry_L, dry_R, send
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    dry_L += x * l * 1.414 / 2 * 2 ** .5
    dry_R += x * r * 1.414 / 2 * 2 ** .5
    send += x * rev


# 1) drone grave (E1/A1) com respiração lenta
drone = (np.sin(2 * np.pi * 41.2 * t) * .5 + np.sin(2 * np.pi * 55 * t + .3) * .35
         + lp(saw(np.full(N, 110.0)) + saw(np.full(N, 110.6)), 300) * .25)
drone *= (.55 + .45 * np.sin(2 * np.pi * .18 * t)) * fade(0, 1.8) * (1 - fade(8.8, 10))
add(drone * .22, 0, .1)

# ar: ruído filtrado
air = bp(rng.standard_normal(N), 2500, 9000) * fade(0, 2) * (1 - fade(8.5, 10))
add(air * .012, .3, .3)

# 2) tique-taque de relógio
def tick(at, hi=True, amp=1.0):
    e = env_exp(at, .018, .0005)
    f = 2900 if hi else 2200
    s = np.sin(2 * np.pi * f * t) * e + bp(rng.standard_normal(N), 1500, 7000) * env_exp(at, .004, .0002) * .8
    return s * amp

for i, at in enumerate([0.25, 0.75, 1.25, 1.55, 1.75, 1.88]):
    add(tick(at, i % 2 == 0, .5 + i * .08), -.35 if i % 2 else .35, .25)
for i, at in enumerate(np.arange(3.0, 9.6, 0.5)):
    add(tick(at, i % 2 == 0, .16), -.4 if i % 2 else .4, .35)

# 3) riser antes do impacto (1,0 -> 2,0 s)
rmask = (t >= 1.0) & (t < 2.0)
rp = np.clip((t - 1.0) / 1.0, 0, 1)
noise = rng.standard_normal(N)
riser = np.zeros(N)
# varredura em blocos de banda crescente
for k in range(20):
    a, b = 1.0 + k * .05, 1.0 + (k + 1) * .05
    m = (t >= a) & (t < b + .02)
    fc = 300 * (12 ** (k / 19))
    seg = bp(noise, fc * .7, min(fc * 1.6, 20000))
    riser[m] += seg[m]
tone = np.sin(2 * np.pi * np.cumsum(180 * (6 ** rp)) / SR)
riser = (riser * .6 + tone * .25) * rp ** 2.2 * rmask
add(riser * .55, 0, .5)

# 4) impacto principal em 2,0 s
def impact(at, amp=1.0, braam=True):
    tt = np.clip(t - at, 0, None)
    on = t >= at
    f = 32 + 95 * np.exp(-tt / .09)
    sub = np.sin(2 * np.pi * np.cumsum(f * on) / SR) * env_exp(at, 1.3, .002)
    click = hp(rng.standard_normal(N), 2000) * env_exp(at, .012, .0003)
    body = lp(rng.standard_normal(N), 900) * env_exp(at, .35, .001)
    out = sub * 1.0 + click * .35 + body * .5
    if braam:
        fr = [55, 82.4, 110, 164.8]
        b = sum(saw(np.full(N, x)) + saw(np.full(N, x * 1.006)) for x in fr)
        cut = 300 + 2400 * np.exp(-tt / .5)
        # filtro com corte variável aproximado em 4 faixas
        bl = np.zeros(N)
        for lo_c, a0, a1 in [(2600, 0, .25), (1500, .25, .7), (800, .7, 1.5), (420, 1.5, 9)]:
            m = (tt >= a0) & (tt < a1) & on
            bl[m] = lp(b, lo_c)[m]
        bl = np.tanh(bl * .6) * env_exp(at, 2.4, .012)
        out += bl * .55
    return out * amp

add(impact(2.0, 1.0), 0, .55)

# 5) whoosh + impacto da logo em 4,6 s
wm = (t >= 3.9) & (t < 4.6)
wp = np.clip((t - 3.9) / .7, 0, 1)
whoosh = bp(noise, 400, 5000) * wp ** 3 * wm
add(whoosh * .35, -.2, .5)
add(impact(4.6, .55, braam=True), 0, .6)

# 6) pad de cordas (A menor -> F maior) a partir de 2,4 s
def pad(freqs, a, b):
    x = sum(saw(np.full(N, f)) + saw(np.full(N, f * 1.004)) + saw(np.full(N, f * .996)) for f in freqs)
    x = lp(x, 1400, 2)
    return x * fade(a, a + 1.4) * (1 - fade(b - .6, b + .8))

strings = pad([110, 130.8, 164.8, 220], 2.4, 6.4) + pad([87.3, 130.8, 174.6, 220], 6.0, 10.4)
strings *= (1 - fade(9.2, 10))
add(strings * .045, 0, .7)

# pulsos graves (batimento) entre os impactos
for at in [3.0, 4.0, 5.6, 6.6, 7.6]:
    add(impact(at, .18, braam=False), 0, .2)

# 7) brilho final 8,2 s (sino)
bell = sum(np.sin(2 * np.pi * f * t) * env_exp(8.2, d, .002) * g
           for f, d, g in [(880, 1.6, 1), (1318.5, 1.2, .5), (1760, .9, .35), (2637, .6, .2)])
add(bell * .06, .2, .8)

# reverb sintético (IR de ruído com decaimento exponencial, estéreo)
irn = int(SR * 2.8)
ti = np.arange(irn) / SR
irL = lp(rng.standard_normal(irn), 7000) * np.exp(-ti / .75)
irR = lp(rng.standard_normal(irn), 7000) * np.exp(-ti / .75)
irL[:int(.012 * SR)] = 0; irR[:int(.017 * SR)] = 0
wetL = fftconvolve(send, irL)[:N]; wetR = fftconvolve(send, irR)[:N]
norm = np.max(np.abs(np.concatenate([wetL, wetR]))) + 1e-9
dn = np.max(np.abs(np.concatenate([dry_L, dry_R]))) + 1e-9
L = dry_L / dn + wetL / norm * .38
R = dry_R / dn + wetR / norm * .38

mix = np.stack([L, R], 1)
mix = hp(mix.T, 25, 2).T
mix = np.tanh(mix * 1.6) / np.tanh(1.6)
mix *= (1 - fade(9.7, 10.0))[:, None]
mix /= np.max(np.abs(mix)) / 0.89  # pico -1 dBFS

out = os.path.join(os.path.dirname(__file__), '..', 'output', 'FEA-elite-trilha.wav')
os.makedirs(os.path.dirname(out), exist_ok=True)
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print('ok', out)
