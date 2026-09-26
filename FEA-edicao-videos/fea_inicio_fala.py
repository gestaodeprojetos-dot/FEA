#!/usr/bin/env python3
"""FEA: onde a fala começa de verdade em cada WAV (para cortar o silêncio inicial).

Uso:
    python3 fea_inicio_fala.py wav/*.wav

A transcrição com VAD costuma marcar a primeira palavra em 0,0 s mesmo com
silêncio antes; aqui o início vem da energia do áudio (janelas de 20 ms, limiar
18 dB abaixo do nível de voz). O vídeo deve começar ~0,08 s antes desse ponto:
pedido da Keila em 26/09/2026, "o Dr. começa a falar direto".
"""
import os
import sys

import numpy as np
import scipy.io.wavfile as wavfile


def inicio_fala(caminho, janela=0.02, abaixo_voz=18):
    r, a = wavfile.read(caminho)
    a = a.astype(float)
    h = int(r * janela)
    e = 20 * np.log10(np.sqrt((a[:len(a) // h * h].reshape(-1, h) ** 2).mean(1)) + 1)
    limiar = np.percentile(e, 90) - abaixo_voz
    for i in range(len(e) - 5):
        if (e[i:i + 5] > limiar).sum() >= 4:
            return i * janela
    return 0.0


if __name__ == "__main__":
    for wav in sys.argv[1:]:
        print(f"{os.path.basename(wav)}\t{inicio_fala(wav):.2f}")
