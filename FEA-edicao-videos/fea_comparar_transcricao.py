#!/usr/bin/env python3
"""FEA: compara duas transcrições do mesmo áudio (ex.: Whisper x ElevenLabs Scribe).

Uso:
    python3 fea_comparar_transcricao.py AUDIO.wav WHISPER.json SCRIBE.json [mais.json ...]

AUDIO.wav: mono 16 kHz (o mesmo que vai para o fea_transcrever.py).
Mede, contra a voz real no áudio, o que a revisora cobra nos Reels:
  - palavras: total de palavras transcritas;
  - sem voz: palavras cujo tempo cai em silêncio (palavra inventada ou fora de sincronia);
  - voz sem palavra: segundos de fala no áudio sem nenhuma palavra transcrita (fala que sumiu,
    como o fim da enumeração "4, 5, 6" ou a resposta baixa da paciente);
  - atraso mediano: quanto o início da palavra fica depois do início da voz, nas palavras que
    abrem uma frase (legenda atrasada ou adiantada).
Quanto menor "sem voz", "voz sem palavra" e |atraso|, melhor.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_transcrever import PASSO, carregar_audio, perfil  # noqa: E402


def palavras(caminho):
    return [w for s in json.load(open(caminho, encoding="utf-8")) for w in s["words"]]


def medir(ws, db, limiar):
    voz = db >= limiar
    n = len(voz)
    coberto = np.zeros(n, bool)
    sem_voz = 0
    for w in ws:
        i0, i1 = int(w["s"] / PASSO), max(int(w["s"] / PASSO) + 1, int(w["e"] / PASSO))
        coberto[max(0, i0 - 4):min(n, i1 + 4)] = True     # tolera 0,2 s de cada lado
        if not voz[max(0, i0 - 2):min(n, i1 + 2)].any():
            sem_voz += 1
    # voz sem palavra: só blocos de voz de pelo menos 0,3 s (respiração e ruído curto não contam)
    faltando, k = 0.0, 0
    while k < n:
        if voz[k] and not coberto[k]:
            j = k
            while j < n and voz[j] and not coberto[j]:
                j += 1
            if (j - k) * PASSO >= 0.3:
                faltando += (j - k) * PASSO
            k = j
        k += 1
    # atraso: palavra após pausa >= 0,5 s comparada ao início da voz mais próximo (janela de ±0,6 s)
    atrasos, ant = [], -1.0
    for w in ws:
        if w["s"] - ant >= 0.5:
            i = int(w["s"] / PASSO)
            j0, j1 = max(0, i - 12), min(n, i + 12)
            on = [x for x in range(max(1, j0), j1) if voz[x] and not voz[x - 1]]
            if on:
                x = min(on, key=lambda x: abs(x - i))
                atrasos.append(w["s"] - x * PASSO)
        ant = w["e"]
    med = float(np.median(atrasos)) if atrasos else float("nan")
    return len(ws), sem_voz, faltando, med


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    audio = carregar_audio(sys.argv[1])
    db, limiar = perfil(audio)
    print(f"{'transcrição':40} {'palavras':>8} {'sem voz':>8} {'voz sem palavra':>16} {'atraso med.':>12}")
    for c in sys.argv[2:]:
        n, sv, falt, med = medir(palavras(c), db, limiar)
        print(f"{os.path.basename(c)[:40]:40} {n:8d} {sv:5d} ({100 * sv / max(n, 1):3.0f}%)"
              f" {falt:13.1f} s {med:+10.2f} s")


if __name__ == "__main__":
    main()
