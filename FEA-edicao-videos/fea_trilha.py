#!/usr/bin/env python3
"""FEA: compõe uma trilha instrumental original (sem direito autoral de terceiros) para fundo de vídeo.

Uso: python3 fea_trilha.py saida.wav [duracao_s] [variacao A a F]

Clima calmo e premium (Elite Mentoring): pad quente de acordes, piano suave em arpejo e um grave
discreto. Progressão em lá menor (Am - F - C - G), 84 bpm. Gerada por síntese, então pode ir para
anúncio no Meta sem risco de bloqueio por música protegida (Keila, 10/11: "uma musiquinha baixa").
"""
import sys
import wave

import numpy as np

SR = 48000


def nota(n):
    """Frequência da nota MIDI n."""
    return 440.0 * 2 ** ((n - 69) / 12)


def envelope(n, a, r):
    e = np.ones(n)
    ia, ir = int(a * SR), int(r * SR)
    e[:ia] = np.linspace(0, 1, ia)
    if ir:
        e[-ir:] *= np.linspace(1, 0, ir)
    return e


def pad(freqs, dur):
    """Pad quente: senos levemente desafinados com harmônicos fracos e vibrato lento."""
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            ff = f * 2 ** (det / 12)
            vib = 1 + 0.0015 * np.sin(2 * np.pi * 0.25 * t)
            s += np.sin(2 * np.pi * ff * vib * t) + 0.18 * np.sin(4 * np.pi * ff * t) + 0.06 * np.sin(6 * np.pi * ff * t)
    return s / (len(freqs) * 3) * envelope(len(t), 0.8, 0.8)


def piano(f, dur):
    """Piano suave: ataque curto e decaimento exponencial, com harmônicos que caem mais rápido."""
    t = np.arange(int(dur * SR)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2)
         + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4.0)
         + 0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6.0))
    return s * envelope(len(t), 0.004, 0.05)


def reverb(x, segs=(0.031, 0.047, 0.061, 0.079), fb=0.55, mix=0.35):
    """Reverb simples por linhas de atraso com realimentação (dá espaço e suaviza a síntese)."""
    out = np.zeros(len(x) + SR * 2)
    out[:len(x)] += x
    wet = np.zeros_like(out)
    for d in segs:
        k = int(d * SR)
        # ecos sucessivos com ganho decrescente
        buf = np.zeros_like(out)
        buf[:len(x)] = x
        acc = np.zeros_like(out)
        g = 1.0
        for rep in range(1, 30):
            g *= fb
            if g < 0.01:
                break
            ini = rep * k
            if ini >= len(out):
                break
            acc[ini:] += g * buf[:len(out) - ini]
        wet += acc
    wet /= len(segs)
    return (out * (1 - mix) + wet * mix)[:len(x)]


# Variações para alternar entre os vídeos (Keila 10/11: "não é para colocar a mesma em todos").
# acordes: tríades em MIDI; graves: fundamental; arpejo: índices do acorde em colcheias (None = pausa)
VARIACOES = {
    "A": dict(bpm=84, acordes=[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],
              graves=[45, 41, 48, 43], arpejo=[0, 1, 2, 1, 2, 0, 1, 2]),                # Am F C G
    "B": dict(bpm=92, acordes=[[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]],
              graves=[48, 43, 45, 41], arpejo=[0, 2, 1, 2, 0, 2, 1, 2]),                # C G Am F
    "C": dict(bpm=74, acordes=[[62, 65, 69], [58, 62, 65], [53, 57, 60], [60, 64, 67]],
              graves=[50, 46, 41, 48], arpejo=[0, None, 2, None, 1, None, 2, None]),    # Dm Bb F C (lenta)
    "D": dict(bpm=96, acordes=[[64, 67, 71], [60, 64, 67], [55, 59, 62], [62, 66, 69]],
              graves=[52, 48, 43, 50], arpejo=[0, 1, 2, 0, 1, 2, 0, 1]),                # Em C G D
    "E": dict(bpm=80, acordes=[[53, 57, 60], [60, 64, 67], [62, 65, 69], [58, 62, 65]],
              graves=[41, 48, 50, 46], arpejo=[2, 1, 0, 1, 2, 1, 0, 1]),                # F C Dm Bb
    "F": dict(bpm=88, acordes=[[55, 58, 62], [51, 55, 58], [58, 62, 65], [53, 57, 60]],
              graves=[43, 39, 46, 41], arpejo=[0, 2, None, 1, 0, 2, None, 2]),          # Gm Eb Bb F
}


def compor(dur=75.0, bpm=84, variacao="A"):
    v = VARIACOES[variacao]
    bpm = v["bpm"]
    beat = 60.0 / bpm
    compasso = 4 * beat
    acordes, graves, arpejo = v["acordes"], v["graves"], v["arpejo"]
    n = int(dur * SR)
    L = np.zeros(n + SR * 4)
    R = np.zeros(n + SR * 4)
    c, t0 = 0, 0.0
    while t0 < dur:
        ac = acordes[c % 4]
        i0 = int(t0 * SR)
        p = pad([nota(x) for x in ac], compasso + 0.8) * 0.30
        L[i0:i0 + len(p)] += p
        R[i0:i0 + len(p)] += p
        g = pad([nota(graves[c % 4])], compasso + 0.5) * 0.22
        L[i0:i0 + len(g)] += g
        R[i0:i0 + len(g)] += g
        if c >= 1:   # o piano entra no 2º compasso
            for k, idx in enumerate(arpejo):
                if idx is None:
                    continue
                ti = t0 + k * beat / 2
                if ti >= dur:
                    break
                oit = 12 if k % 4 == 3 else 0
                pn = piano(nota(ac[idx] + 12 + oit), 1.6) * (0.16 if k % 2 == 0 else 0.11)
                j = int(ti * SR)
                pan = 0.35 if k % 2 else -0.35
                L[j:j + len(pn)] += pn * (1 - pan)
                R[j:j + len(pn)] += pn * (1 + pan)
        c += 1
        t0 += compasso
    L, R = L[:n], R[:n]
    L, R = reverb(L), reverb(R, segs=(0.029, 0.043, 0.067, 0.083))
    st = np.stack([L, R], axis=1)
    fade = int(2.0 * SR)
    st[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st /= np.max(np.abs(st)) + 1e-9
    return st * 0.8


def main():
    saida = sys.argv[1]
    dur = float(sys.argv[2]) if len(sys.argv) > 2 else 75.0
    variacao = sys.argv[3] if len(sys.argv) > 3 else "A"
    bpm = VARIACOES[variacao]["bpm"]
    st = compor(dur, bpm, variacao)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(saida, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{saida}: {dur:.0f} s, variação {variacao}, {bpm:.0f} bpm")


if __name__ == "__main__":
    main()
