#!/usr/bin/env python3
"""FEA: recupera os cortes de uma edição já entregue, alinhando os quadros com os brutos.

Uso:
    python3 fea_alinhar.py FFMPEG editado.mp4 bruto1.MOV [bruto2.MOV ...] [--cta 59.55]

Compara miniaturas em cinza (18x32, 30 fps, só a parte de cima do quadro: título e legenda
ficam de fora) por correlação normalizada. Imprime o bruto correspondente e os trechos
`manter` (segundos do bruto), prontos para o projeto.json. --cta descarta os segundos finais
do editado (CTA concatenado).
"""
import json, os, subprocess, sys
import numpy as np

LW, LH, FPS = 18, 32, 30
CACHE = os.environ.get("FEA_CACHE_ALINHAR", "/tmp")


def miniaturas(ff, arq):
    cache = os.path.join(CACHE, os.path.basename(arq) + f".{os.path.getsize(arq)}.npy")
    if os.path.exists(cache):
        return np.load(cache)
    raw = subprocess.run([ff, "-nostdin", "-v", "error", "-i", arq, "-vf",
                          f"fps={FPS},scale={LW}:{LH},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    m = np.frombuffer(raw, np.uint8).reshape(-1, LH, LW).astype(np.float32)
    np.save(cache, m)
    return m


def normalizar(m):
    m = m[:, :int(LH * 0.40), :].reshape(len(m), -1)   # faixa de cima: sem título (centro) e sem legenda
    m = m - m.mean(1, keepdims=True)
    return m / (np.linalg.norm(m, axis=1, keepdims=True) + 1e-6)


def alinhar(ff, editado, brutos, cta=0.0):
    e = miniaturas(ff, editado)
    if cta:
        e = e[:max(1, len(e) - int(round(cta * FPS)))]
    en = normalizar(e)
    melhor = None
    for b in brutos:
        bn = normalizar(miniaturas(ff, b))
        c = en @ bn.T
        j = c.argmax(1)
        score = float(np.median(c.max(1)[3 * FPS:])) if len(c) > 3 * FPS else float(c.max(1).mean())
        if melhor is None or score > melhor[0]:
            melhor = (score, b, j, c.max(1))
    score, b, j, cm = melhor
    # trechos: offset (j - i) constante; tolera 1 quadro de jitter
    off = j - np.arange(len(j))
    segs, ini = [], 0
    for i in range(1, len(j) + 1):
        if i == len(j) or abs(int(off[i]) - int(np.median(off[ini:i]))) > 2:
            if i - ini >= 6:   # trecho de 0,2 s ou mais
                o = int(np.median(off[ini:i]))
                segs.append([round((ini + o) / FPS, 3), round((i + o) / FPS, 3), round(float(cm[ini:i].mean()), 3)])
            ini = i
    # junta trechos contíguos no bruto
    juntos = []
    for s in segs:
        if juntos and abs(s[0] - juntos[-1][1]) < 0.1:
            juntos[-1][1] = s[1]
        else:
            juntos.append(s)
    return {"bruto": b, "score": round(score, 3), "dur_editado": round(len(e) / FPS, 2),
            "manter": [[a, z] for a, z, _ in juntos], "corr": [c for _, _, c in juntos]}


if __name__ == "__main__":
    a = sys.argv[1:]
    cta = 0.0
    if "--cta" in a:
        k = a.index("--cta"); cta = float(a[k + 1]); a = a[:k] + a[k + 2:]
    print(json.dumps(alinhar(a[0], a[1], a[2:], cta), ensure_ascii=False))
