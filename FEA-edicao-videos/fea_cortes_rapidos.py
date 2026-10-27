#!/usr/bin/env python3
"""FEA: corte rápido (jump cut) para o modelo notícia: tira toda pausa de respiração entre frases.

Uso:
    python3 fea_cortes_rapidos.py bruto.mp4 [trechos.json]  > manter.json

trechos.json (opcional): [[ini, fim], ...] em segundos do bruto, os trechos que ficam no vídeo
(conteúdo já escolhido); sem ele, o bruto inteiro. Dentro de cada trecho, todo silêncio de 0,2 s
ou mais (áudio abaixo de 45 dB) vira corte, deixando 0,06 s depois da última palavra e 0,04 s
antes da próxima (Keila, 26/10/2026: "precisa de um corte mais rápido"). A saída vem com
"exato" em cada trecho, para o encaixe automático do fea_editar_video.py não devolver o respiro.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as base  # noqa: E402

LIMIAR_DB, PAUSA_MIN, FOLGA_FIM, FOLGA_INI = 45.0, 0.20, 0.06, 0.04


def silencios(db, passo):
    runs, i = [], 0
    while i < len(db):
        if db[i] < LIMIAR_DB:
            j = i
            while j < len(db) and db[j] < LIMIAR_DB:
                j += 1
            if (j - i) * passo >= PAUSA_MIN:
                runs.append((i * passo, j * passo))
            i = j
        else:
            i += 1
    return runs


def cortar(trechos, runs):
    saida = []
    for a, b in trechos:
        ini = a
        for s, e in runs:
            if e <= a or s >= b:
                continue
            if s <= a:                      # trecho começa no silêncio: entra junto com a voz
                ini = max(ini, e - FOLGA_INI)
                continue
            if e >= b:                      # termina no silêncio: sai logo depois da voz
                b = min(b, s + FOLGA_FIM)
                break
            saida.append([round(ini, 2), round(s + FOLGA_FIM, 2)])
            ini = e - FOLGA_INI
        saida.append([round(ini, 2), round(b, 2)])
    return [t + ["exato"] for t in saida if t[1] - t[0] > 0.25]


def main():
    bruto = sys.argv[1]
    ff = subprocess.run(["python3", "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                        capture_output=True, text=True).stdout.strip()
    db, _, passo = base.perfil_voz(ff, bruto)
    trechos = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else [[0.0, len(db) * passo]]
    manter = cortar(trechos, silencios(db, passo))
    print(json.dumps(manter))
    print(f"{len(manter)} trechos, {sum(b - a for a, b, _ in manter):.1f} s", file=sys.stderr)


if __name__ == "__main__":
    main()
