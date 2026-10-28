"""Trilha original do teaser Reology Map: 120 BPM, Ré menor, 40 s.
Sintetizada do zero (nenhuma amostra de áudio externa).
Uso: python3 fea_trilha.py saida.wav
"""
import sys
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
DUR = 40.0
BPM = 120
BEAT = 60 / BPM          # 0,5 s
BAR = 4 * BEAT           # 2 s
N = int(SR * DUR)
rng = np.random.default_rng(42)

# momentos-chave (segundos) alinhados ao vídeo
CORTES = [8, 14, 18, 22, 26, 30]
DROP = 4.0
FINAL = 34.0
CLIQUES = [12.27, 16.68]

L = np.zeros(N); R = np.zeros(N)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    gl = gain * np.cos((pan + 1) * np.pi / 4)
    gr = gain * np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gl
    R[i:i + len(sig)] += sig * gr


def filt(x, kind, f, order=4):
    wn = [x / (SR / 2) for x in f] if isinstance(f, (list, tuple)) else f / (SR / 2)
    sos = butter(order, wn, btype=kind, output='sos')
    return sosfilt(sos, x)


def midi(n):
    return 440 * 2 ** ((n - 69) / 12)


def saw(freq, d, detune=0.0):
    t = t_axis(d)
    ph = (t * freq * (1 + detune)) % 1
    return 2 * ph - 1


def adsr(d, a, dec, s, r):
    n = int(d * SR)
    env = np.ones(n) * s
    na, nd, nr = int(a * SR), int(dec * SR), int(r * SR)
    na = min(na, n); env[:na] = np.linspace(0, 1, na)
    nd = min(nd, n - na); env[na:na + nd] = np.linspace(1, s, nd)
    if nr and n > nr:
        env[-nr:] *= np.linspace(1, 0, nr)
    return env


# ---------- instrumentos ----------
def kick(gain=1.0):
    t = t_axis(0.5)
    f = 55 + 92 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7)
    click = filt(rng.standard_normal(len(t)), 'highpass', 2500) * np.exp(-t * 300) * 0.25
    return np.tanh((body + click) * 1.6) * gain


def hat(open_=False):
    d = 0.18 if open_ else 0.05
    t = t_axis(d)
    n = filt(rng.standard_normal(len(t)), 'highpass', 7000)
    return n * np.exp(-t * (18 if open_ else 90))


def snare():
    t = t_axis(0.3)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)
    n = filt(rng.standard_normal(len(t)), 'bandpass', [1200, 7000], 2) * np.exp(-t * 16)
    return tone * 0.5 + n


def bass_note(note, d):
    f = midi(note)
    s = saw(f, d) * 0.6 + saw(f, d, 0.004) * 0.6
    s = filt(s, 'lowpass', 380)
    sub = np.sin(2 * np.pi * f / 2 * t_axis(d))
    env = adsr(d, 0.004, 0.12, 0.55, 0.03)
    return (s * 0.75 + sub * 0.5) * env


def pad(notes, d):
    out = np.zeros(int(d * SR))
    for n in notes:
        for dt in (-0.006, 0.0, 0.007):
            out += saw(midi(n), d, dt)
    out = filt(out, 'lowpass', 1300, 2)
    return out * adsr(d, 0.6, 0.2, 0.9, 0.6) / (len(notes) * 3)


def pluck(note, d=0.22):
    t = t_axis(d)
    f = midi(note)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    return s * np.exp(-t * 16)


def impact(size=1.0):
    d = 3.2 * size
    t = t_axis(d)
    f = 36.7 + 36 * np.exp(-t * 4)
    boom = filt(np.sin(2 * np.pi * np.cumsum(f) / SR), 'highpass', 28, 2) * np.exp(-t * 2.2 / size)
    n = filt(rng.standard_normal(len(t)), 'lowpass', 1800) * np.exp(-t * 6)
    metal = filt(rng.standard_normal(len(t)), 'bandpass', [2500, 6000], 2) * np.exp(-t * 9) * 0.25
    return np.tanh((boom * 0.9 + n * 0.6 + metal) * 1.3)


def whoosh(d=0.9, up=True):
    t = t_axis(d)
    n = rng.standard_normal(len(t))
    # varredura de banda em blocos
    out = np.zeros_like(n)
    blocks = 24
    seg = len(n) // blocks
    for b in range(blocks):
        x = b / (blocks - 1)
        fc = 300 * (40 ** (x if up else 1 - x))
        lo, hi = fc * 0.6, min(fc * 1.6, SR / 2 - 100)
        sl = slice(b * seg, (b + 1) * seg + 2048)
        out[sl] += filt(n[sl], 'bandpass', [lo, hi], 2) * np.hanning(len(n[sl]))
    env = (t / d) ** 2 if up else (1 - t / d) ** 2
    return out * env


def riser(d):
    t = t_axis(d)
    w = whoosh(d, True)
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * (t / d) ** 2) / SR) * (t / d) ** 3 * 0.25
    return w + tone


def ui_click():
    t = t_axis(0.09)
    tick = np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 160)
    snap = filt(rng.standard_normal(len(t)), 'highpass', 3500) * np.exp(-t * 650) * 0.8
    thock = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 70) * 0.6
    return (tick * 0.7 + snap + thock)


# ---------- arranjo ----------
# progressão Dm - Bb - F - C (2 compassos cada acorde a partir do drop)
PROG = [(50, [62, 65, 69]), (46, [58, 62, 65]), (41, [57, 60, 65]), (48, [55, 60, 64])]  # raiz do baixo, acorde
ARP = {50: [74, 77, 81, 77], 46: [70, 74, 77, 74], 41: [69, 72, 77, 72], 48: [67, 72, 76, 72]}


def chord_at(time):
    k = int((time - DROP) // (2 * BAR)) % 4 if time >= DROP else 0
    return PROG[k]


# intro: drone + pad abafado + pulso filtrado
drone = (np.sin(2 * np.pi * midi(38) * t_axis(4.5)) * 0.5 + filt(saw(midi(38), 4.5), 'lowpass', 220) * 0.4) * adsr(4.5, 1.5, 0.5, 1, 0.8)
add(drone, 0, 0.55)
add(pad([62, 65, 69], 4.2), 0, 0.35, -0.2)
add(pad([57, 62, 65], 4.2), 0, 0.25, 0.2)
add(impact(0.7), 0.15, 0.55)                       # entrada do logo
for i in range(8):                                 # pulso de colcheias abafado
    tt = 2.0 + i * BEAT / 2
    add(filt(bass_note(38, 0.22), 'lowpass', 160), tt, 0.35 + 0.05 * i)
add(riser(1.6), DROP - 1.6, 0.45)

# drop e corpo
time = DROP
while time < FINAL - 1e-6:
    root, ch = chord_at(time)
    beat_i = int(round((time - DROP) / (BEAT / 2)))
    build = time >= 30
    # baixo em colcheias (com variação de oitava a cada 4)
    note = root - 12 + (12 if beat_i % 8 == 7 else 0)
    add(bass_note(note, BEAT / 2 * 0.95), time, 0.62)
    # kick nos tempos
    if beat_i % 2 == 0:
        add(kick(), time, 0.95)
    # chimbal em semicolcheias
    for s in range(2):
        tt = time + s * BEAT / 4
        add(hat(open_=(beat_i % 4 == 3 and s == 1)), tt, (0.10 if s else 0.16), 0.3)
    # snare/clap no 2 e no 4
    if beat_i % 4 == 2:
        add(snare(), time, 0.38, -0.1)
    # arpejo a partir dos 8 s
    if time >= 8:
        for s in range(2):
            tt = time + s * BEAT / 4
            idx = (beat_i * 2 + s) % 4
            add(pluck(ARP[root][idx]), tt, 0.13, -0.35 if idx % 2 else 0.35)
    # pad a cada troca de acorde
    if abs(((time - DROP) % (2 * BAR))) < 1e-6:
        add(pad(ch, 2 * BAR + 0.6), time, 0.42)
    time += BEAT / 2

# impactos e whooshes nos cortes
add(impact(1.2), DROP, 0.85)
for c in CORTES:
    add(whoosh(0.8, True), c - 0.8, 0.45, 0.2)
    add(impact(0.6), c, 0.42)

# construção final (mobile): caixa acelerando + riser
for i, tt in enumerate(np.concatenate([np.arange(32, 33, BEAT / 2), np.arange(33, 33.75, BEAT / 4), np.arange(33.75, 34, BEAT / 8)])):
    add(snare(), tt, 0.18 + 0.03 * i)
add(riser(2.6), FINAL - 2.6, 0.55)

# final: impacto grande + pad longo + sub
add(impact(1.8), FINAL, 1.0)
add(pad([50, 57, 62, 65, 69], 6.0), FINAL, 0.5)
add(np.sin(2 * np.pi * midi(38) * t_axis(5)) * np.exp(-t_axis(5) * 0.9), FINAL, 0.35)
add(pluck(86, 1.5) + pluck(81, 1.5) * 0.7, FINAL + 0.02, 0.18)

mix = np.stack([L, R])

# sidechain: abaixa o mix (exceto cliques) quando o kick bate
duck = np.ones(N)
time = DROP
while time < FINAL:
    i = int(time * SR); n = int(0.22 * SR)
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.35 * np.exp(-np.arange(n) / SR * 14))
    time += BEAT
mix *= duck

# reverb sintético
ir_t = t_axis(2.2)
ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 3.2)
ir = filt(ir, 'lowpass', 5000)
wet = np.stack([fftconvolve(mix[0], ir[0])[:N], fftconvolve(mix[1], ir[1])[:N]])
mix = mix + wet * 0.018

# cliques de interface (secos, por cima)
for c in CLIQUES:
    i = int(c * SR); s = ui_click()
    mix[:, i:i + len(s)] += s * 0.55

# fade de saída e master
fo = int(1.2 * SR)
mix[:, -fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix * 1.1)
mix /= np.abs(mix).max() / 0.89

import soundfile as sf
sf.write(sys.argv[1], mix.T, SR, subtype='PCM_24')
print('ok', sys.argv[1])
