#!/usr/bin/env python3
"""Acha sons da paciente (gemido, "ai", "ui", "hum" de dor) que o Whisper não transcreve.

Keila, 28/10/2026 (pasta 27 "Fios de tração"): som de dor da paciente durante o procedimento
sai com "silenciar" no projeto.json, sem cortar. O Whisper não escreve gemido (nem sem VAD), então
a busca é pelo áudio: voz (pitch) fora das palavras transcritas, em janelas de 20 ms.

Uso:
    python3 fea_sons_paciente.py FFMPEG bruto.MOV transcricao.json [--agudo 175]

Lista cada trecho com voz e sem palavra transcrita perto: início-fim (s do bruto), pitch mediano
e volume. A voz do Dr. fica em ~100 a 150 Hz; o "ai"/"hum" da paciente ficou em 200 a 450 Hz e
mais fraco. Gemido de boca fechada pode ser grave: conferir o rosto nos quadros de todo candidato
e ouvir antes de silenciar. "AGUDO" marca o trecho com pitch acima de --agudo.
"""
import json, subprocess, sys

import numpy as np


def pitch(ff, entrada, sr=16000, passo=0.02, janela=0.04):
    pcm = subprocess.run([ff, "-nostdin", "-v", "error", "-i", entrada, "-vn", "-ac", "1", "-ar", str(sr),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    h, n = int(passo * sr), int(janela * sr)
    lmin, lmax = sr // 450, sr // 70
    saida = []
    for i in range(0, len(a) - n, h):
        x = a[i:i + n] - a[i:i + n].mean()
        db = 10 * np.log10((x ** 2).mean() + 1e-12) + 94
        f0 = 0.0
        if db >= 42:   # YIN simplificado
            d = np.array([((x[:-l] - x[l:]) ** 2).sum() for l in range(1, lmax + 1)])
            cm = d * np.arange(1, lmax + 1) / np.cumsum(d)
            l = int(np.argmin(cm[lmin - 1:])) + lmin
            f0 = sr / l if cm[l - 1] < 0.25 else 0.0
        saida.append((i / sr, db, f0))
    return np.array(saida), passo


def main(ff, entrada, transcricao, agudo=175.0):
    r, ps = pitch(ff, entrada)
    trans = json.load(open(transcricao, encoding="utf-8"))
    segs = trans["segments"] if isinstance(trans, dict) else trans
    coberto = np.zeros(len(r), bool)
    for w in (w for s in segs for w in s.get("words", [])):
        # palavra esticada pela transcrição cobre no máximo 0,6 s
        coberto[int(w["s"] / ps):int(min(w["e"], w["s"] + 0.6) / ps) + 1] = True
    cand = (r[:, 2] > 0) & ~coberto
    i = 0
    while i < len(r):
        if not cand[i]:
            i += 1
            continue
        j = i
        while j < len(r) and cand[j:j + 4].any():
            j += 1
        if j - i >= 4:
            f0 = float(np.median(r[i:j][r[i:j, 2] > 0, 2]))
            print(f"{r[i, 0]:7.2f}-{r[j - 1, 0] + 0.04:7.2f}  pitch {f0:4.0f} Hz  {r[i:j, 1].max():3.0f} dB"
                  + ("  AGUDO" if f0 > agudo else ""))
        i = j


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit(__doc__)
    ag = float(args[args.index("--agudo") + 1]) if "--agudo" in args else 175.0
    main(args[0], args[1], args[2], ag)
