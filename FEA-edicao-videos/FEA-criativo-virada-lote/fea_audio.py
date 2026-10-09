"""FEA: efeitos sonoros e trilha do criativo de virada de lote, sincronizados com as cenas do JSON.
Trilha sintetizada aqui mesmo (sem banco de música, sem problema de direito autoral):
pulso de grave tipo batida de coração, relógio, pad em lá menor e ostinato, impacto na virada do lote.
Uso: python3 fea_audio.py cfg.json sfx.wav trilha.wav"""
import json, sys, wave
import numpy as np
from scipy.signal import lfilter

SR = 48000
cfg = json.load(open(sys.argv[1])); DUR = cfg['dur']; N = int(DUR * SR)
rng = np.random.default_rng(7)
T = np.arange(N) / SR

def salvar(sig, caminho):
    sig = sig / max(1e-9, np.max(np.abs(sig))) * .89
    pcm = (np.stack([sig, sig], 1) * 32767).astype('<i2')
    w = wave.open(caminho, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()

def add(out, sig, t, g):
    i = int(t * SR)
    if i >= N: return
    j = min(N, i + len(sig)); out[max(i, 0):j] += sig[max(0, -i):j - i] * g

def lp(x, fc):
    c = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - c], [1, -c], x)

def whoosh(d=.45, f0=300, f1=3000):
    n = int(d * SR); x = rng.standard_normal(n); f = np.geomspace(f0, f1, n); y = np.zeros(n); lpv = 0
    c = np.exp(-2 * np.pi * f / SR)
    for k in range(n): lpv = (1 - c[k]) * x[k] + c[k] * lpv; y[k] = lpv
    env = np.sin(np.linspace(0, np.pi, n)) ** 2; y *= env; return y / np.max(np.abs(y))

def tick(f=2200, d=.035):
    n = int(d * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 140) + .4 * rng.standard_normal(n) * np.exp(-t * 300)

def boom(d=1.4, f0=90, f1=32, dec=3.2):
    n = int(d * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec)
    s += lp(rng.standard_normal(n), 900) * np.exp(-t * 18) * .6; return s

def pop(d=.09):
    n = int(d * SR); t = np.arange(n) / SR; f = 900 + 1400 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)

def riser(d=1.2):
    n = int(d * SR); x = rng.standard_normal(n); env = np.linspace(0, 1, n) ** 2.5
    y = lp(x, 2500) * env; t = np.arange(n) / SR
    y += .5 * np.sin(2 * np.pi * np.cumsum(np.linspace(200, 900, n)) / SR) * env; return y / np.max(np.abs(y))

# ---------- efeitos ----------
fx = np.zeros(N); W, Ws = whoosh(), whoosh(.32, 500, 4000)
for c in cfg['cenas']:
    tp = c['tipo']
    if tp in ('logo', 'celular', 'palestrantes', 'virada', 'final'): add(fx, W, c['s'] - .07, .22)
    if tp == 'lote': add(fx, Ws, c['s'] - .02, .12)
    if tp == 'gancho' and c['tFlip'] < c['e']: add(fx, tick(), c['tFlip'] + .08, .35); add(fx, tick(1600, .05), c['tFlip'] + .18, .2)
    if tp == 'virada':
        for k in range(max(0, c['ate'] - c['de'])): add(fx, tick(2000 + k * 150), c['tCal'] + k * .175 + .05, .32)
        add(fx, Ws, c['tFlip'] - .03, .16); add(fx, boom(.35, 110, 45, 9), c['tCarimbo'], .55); add(fx, tick(3000, .03), c['tCarimbo'], .25)
    if tp == 'celular':
        for ch in c.get('chips', []): add(fx, pop(), ch['t'], .3)
    if tp == 'palestrantes':
        for it in c['itens']: add(fx, pop(), it['t'], .26)
    if tp == 'saiba': add(fx, pop(), c['tToque'], .28)
    if tp == 'final': add(fx, pop(), c['s'] + .82, .22)
salvar(fx, sys.argv[2])

# ---------- trilha ----------
BPM = 120; beat = 60 / BPM; bar = 4 * beat
fim = cfg['fim_fala'] + .3
raizes = [55.0, 55.0, 43.65, 41.2]           # Am Am F E (lá menor harmônico)
acordes = [[220, 261.63, 329.63], [220, 261.63, 329.63], [174.61, 220, 261.63], [164.81, 207.65, 246.94]]
mus = np.zeros(N)
idx = np.minimum((T / bar).astype(int) % 4, 3)
# pad de saw desafinado, filtrado
pad = np.zeros(N)
for v in range(3):
    f = np.array([acordes[i][v] for i in range(4)])[idx]
    for det in (-.0025, .0025):
        ph = np.cumsum(f * (1 + det)) / SR; pad += 2 * (ph % 1) - 1
pad = lp(lp(pad, 900), 900) * .22
sub = np.sin(2 * np.pi * np.cumsum(np.array(raizes)[idx]) / SR) * .35
# ostinato em colcheias
ost = np.zeros(N); t8 = beat / 2; padrao = [1, 1, 1.189, 1, 1.498, 1, 1.335, 1.189]
for k in range(int(DUR / t8)):
    t0 = k * t8; b = int(t0 / bar) % 4; f = raizes[b] * 4 * padrao[k % 8]
    n = int(.2 * SR); tt = np.arange(n) / SR
    ph = np.cumsum(np.full(n, f)) / SR; s = (2 * (ph % 1) - 1) * np.exp(-tt * 16)
    add(ost, s, t0, .16 + .1 * min(1, t0 / max(1, fim)))
ost = lp(ost, 1800)
# pulso de coração (grave duplo) e relógio
pul = np.zeros(N); rel = np.zeros(N)
for k in range(int(DUR / beat)):
    t0 = k * beat
    if k % 2 == 0: add(pul, boom(.35, 70, 40, 12), t0, .7); add(pul, boom(.3, 65, 40, 14), t0 + .17, .45)
    add(rel, tick(2600 if k % 2 else 1900, .03), t0, .25)
mus = pad + sub + ost + pul + rel
# impactos nas telas cheias e na virada; subida antes da virada e do final
for c in cfg['cenas']:
    if c['tipo'] in ('logo', 'celular', 'palestrantes'): add(mus, boom(), c['s'], .5)
    if c['tipo'] == 'virada': add(mus, riser(1.0), c['tFlip'] - 1.0, .35); add(mus, boom(1.8), c['tFlip'] + .02, 1.0)
    if c['tipo'] == 'final': add(mus, riser(.9), c['s'] - .9, .3); add(mus, boom(2.2), c['s'], 1.0)
# entra em 0,4 s e sai no fim
env = np.clip(T / .4, 0, 1) * np.clip((DUR - T) / 1.2, 0, 1)
salvar(mus * env, sys.argv[3])
