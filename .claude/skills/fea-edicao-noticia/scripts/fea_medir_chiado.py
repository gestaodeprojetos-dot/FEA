#!/usr/bin/env python3
"""FEA: mede o chiado de um bruto de duas formas, antes de decidir o filtro de voz.

Uso:
    python3 fea_medir_chiado.py audio.wav transcricao.json

1. Pausas: energia de 1 a 6 kHz nos intervalos entre palavras (limpo ~81, chiado forte ~96).
2. Durante a fala: chiado de 6 a 16 kHz relativo à voz (300 Hz a 3 kHz).
   Brutos limpos ficam em -24/-25 dB; acima de -23 dB tem chiado colado na voz.

As duas medidas são necessárias: na sessão dos "Melhores tratamentos" as pausas davam 81,6
(limpo), mas o chiado vinha junto com a voz e a Gabi ouviu (23/11/2026).
O áudio precisa ser WAV mono (ffmpeg -i bruto.MOV -ac 1 -ar 48000 audio.wav).
"""
import json
import sys
import wave

import numpy as np


def carregar(arq):
    w = wave.open(arq)
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    if w.getnchannels() > 1:
        a = a.reshape(-1, w.getnchannels()).mean(1)
    return a, sr


def pausas(a, sr, trans):
    ws = [x for s in trans for x in s["words"]]
    gaps = [(ws[i]["e"] + 0.05, ws[i + 1]["s"] - 0.05) for i in range(len(ws) - 1)
            if ws[i + 1]["s"] - ws[i]["e"] > 0.25]
    n = 2048
    pot = []
    for t0, t1 in gaps:
        x = a[int(t0 * sr):int(t1 * sr)]
        for i in range(0, len(x) - n, n):
            X = np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n))) ** 2
            f = np.fft.rfftfreq(n, 1 / sr)
            pot.append(X[(f >= 1000) & (f < 6000)].mean())
    return len(gaps), (10 * np.log10(np.mean(pot)) if pot else float("nan"))


def durante_fala(a, sr):
    n = 4096
    P = np.mean([np.abs(np.fft.rfft(a[i:i + n] * np.hanning(n))) ** 2 for i in range(0, len(a) - n, n)], 0)
    f = np.fft.rfftfreq(n, 1 / sr)
    b = lambda lo, hi: 10 * np.log10(P[(f >= lo) & (f < hi)].mean())
    return b(6000, 16000) - b(300, 3000), b(3000, 6000) - b(300, 3000)


if __name__ == "__main__":
    a, sr = carregar(sys.argv[1])
    trans = json.load(open(sys.argv[2], encoding="utf-8"))
    ng, p = pausas(a, sr, trans)
    hf, mf = durante_fala(a, sr)
    print(f"pausas ({ng}): 1-6 kHz = {p:.1f}  (limpo ~81, chiado ~96)")
    print(f"durante a fala: chiado 6-16 kHz = {hf:.1f} dB, 3-6 kHz = {mf:.1f} dB  (limpo -24/-25)")
    precisa = p > 86 or hf > -23.5
    print("=> ligar limpar_ruido + limpar_ruido_forte" if precisa else "=> sem filtro de voz")
