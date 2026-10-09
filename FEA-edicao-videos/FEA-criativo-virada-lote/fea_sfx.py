"""FEA: efeitos sonoros discretos do criativo de virada de lote (whoosh, tique, pop, impacto).
Uso: python3 fea_sfx.py saida.wav DURACAO   (tempos dos efeitos fixos abaixo, ajustar por vídeo)"""
import sys, wave
import numpy as np
sr = 48000
saida, dur = sys.argv[1], float(sys.argv[2])
N = int(dur * sr); out = np.zeros(N); rng = np.random.default_rng(7)

def add(sig, t, g):
    i = int(t * sr); j = min(N, i + len(sig)); out[i:j] += sig[:j - i] * g

def whoosh(d=.45, f0=300, f1=3000):
    n = int(d * sr); x = rng.standard_normal(n); y = np.zeros(n); f = np.geomspace(f0, f1, n); lp = 0
    for k in range(n):
        c = np.exp(-2 * np.pi * f[k] / sr); lp = (1 - c) * x[k] + c * lp; y[k] = lp
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return y * env / np.max(np.abs(y * env))

def tick(f=2200, d=.035):
    n = int(d * sr); t = np.arange(n) / sr
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 140) + .4 * rng.standard_normal(n) * np.exp(-t * 300)

def thump(d=.35):
    n = int(d * sr); t = np.arange(n) / sr; f = 110 * np.exp(-t * 6) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 9)

def pop(d=.09):
    n = int(d * sr); t = np.arange(n) / sr; f = 900 + 1400 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 45)

W, Ws = whoosh(), whoosh(.32, 500, 4000)
for t in (2.38, 7.12, 16.5, 22.58): add(W, t, .22)        # entradas de tela cheia
for t in (10.78, 19.68): add(Ws, t, .12)                  # cartão do lote
add(tick(), .70, .35); add(tick(1600, .05), .80, .2)      # flip 5 -> 4
for k in range(4): add(tick(2000 + k * 150), 17.33 + k * .175, .32)  # calendário 10 -> 14
add(Ws, 17.92, .16); add(thump(), 18.5, .55); add(tick(3000, .03), 18.5, .25)  # vira o lote + carimbo
for t in (8.0, 9.72, 15.84, 23.5): add(pop(), t, .28)     # chips, toque no Saiba Mais, botão final
pcm = (np.stack([np.clip(out, -1, 1)] * 2, 1) * 32767).astype('<i2')
w = wave.open(saida, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes()); w.close()
