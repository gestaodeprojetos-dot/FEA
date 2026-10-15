#!/usr/bin/env python3
"""FEA: leitura dos textos queimados num criativo (OCR) e montagem do cfg de tradução.

Par do fea_traduzir_criativo.py (tradução PT -> ES de anúncios com legenda gravada na imagem).

Uso:
    python3 fea_ocr_criativo.py ocr FFMPEG video.mp4 saida_ocr.json      # OCR a 3 quadros/s, em 1080x1920
    python3 fea_ocr_criativo.py blocos ocr.json blocos.json                # agrupa e lista (id, tempo, posição, texto)
    python3 fea_ocr_criativo.py montar blocos.json es.json cfg.json        # junta a tradução -> cfg do render

es.json: {"id": "texto em espanhol" | null | ""}
    null  = texto da cena (story do paciente, rótulo de produto, ruído do OCR): fica como está
    ""    = apaga o PT e não escreve nada (linha duplicada do OCR)
    "_ajustes": {"id": {"tipo": "contorno|branco|caixa", "escala": 1.1, "largura": 1.2, "fonte": "..."}}

Precisa de: pip install rapidocr_onnxruntime opencv-python-headless
"""
import difflib
import json
import os
import re
import subprocess
import sys
from collections import Counter

FPS_OCR = 3
DT = 1 / FPS_OCR
W, H = 1080, 1920


def ocr(ff, video, saida):
    os.environ["OMP_NUM_THREADS"] = "1"
    import numpy as np
    from rapidocr_onnxruntime import RapidOCR
    o = RapidOCR(intra_op_num_threads=1, inter_op_num_threads=1)
    p = subprocess.Popen([ff, "-nostdin", "-v", "error", "-i", video, "-vf", f"fps={FPS_OCR},scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    res, i = [], 0
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        r, _ = o(np.frombuffer(b, np.uint8).reshape(H, W, 3))
        res.append({"t": round(i / FPS_OCR, 3),
                    "txt": [{"box": [[int(x), int(y)] for x, y in bx], "s": s, "c": round(float(c), 3)}
                            for bx, s, c in (r or [])]})
        i += 1
    json.dump(res, open(saida, "w"), ensure_ascii=False)
    print("ok", video, i, "quadros")


def _bb(box):
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    return [min(xs), min(ys), max(xs), max(ys)]


def _vert(a, b):
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return iy / max(1, min(a[3] - a[1], b[3] - b[1]))


def _sim(a, b):
    return difflib.SequenceMatcher(None, a.lower().replace(" ", ""), b.lower().replace(" ", "")).ratio()


def agrupar(amostras):
    """Liga a mesma linha de texto entre amostras seguidas (mesma faixa vertical, texto parecido
    ou crescendo, no caso de texto que aparece digitando)."""
    abertos, fechados = [], []
    for am in amostras:
        t = am["t"]
        usados, novos = set(), []
        for it in am["txt"]:
            b, s = _bb(it["box"]), it["s"]
            melhor, mv = None, 0
            for gi, g in enumerate(abertos):
                if gi in usados:
                    continue
                ls = g["textos"][-1]
                v, ss = _vert(b, g["boxes"][-1]), _sim(s, ls)
                a_, b_ = ls.replace(" ", "").lower(), s.replace(" ", "").lower()
                cresce = b_.startswith(a_) and len(a_) >= 2
                if v > 0.6 and (ss > 0.75 or cresce) and v + ss > mv:
                    mv, melhor = v + ss, gi
            if melhor is None:
                g = {"t0": t, "boxes": [], "textos": [], "ts": [], "conf": []}
                novos.append(g)
            else:
                g = abertos[melhor]
                usados.add(melhor)
            g["boxes"].append(b)
            g["textos"].append(s)
            g["ts"].append(t)
            g["conf"].append(it["c"])
        resto = []
        for gi, g in enumerate(abertos):
            (resto if gi in usados else fechados).append(g)
        abertos = resto + novos
    fechados += abertos
    out = []
    for g in fechados:
        bx = g["boxes"]
        out.append({"t0": g["t0"], "t1": round(g["ts"][-1] + DT, 3), "n": len(g["ts"]),
                    "bbox": [min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)],
                    "txt": max(g["textos"], key=lambda s: len(s.replace(" ", ""))),
                    "variantes": [s for s, _ in Counter(g["textos"]).most_common(3)]})
    return sorted(out, key=lambda g: (g["t0"], g["bbox"][1]))


def blocos(gs):
    """Junta linhas que aparecem e somem juntas, uma embaixo da outra (legenda de 2 linhas, caixa)."""
    gs = [g for g in gs if g["bbox"][3] - g["bbox"][1] < 150                     # logo grande
          and not re.fullmatch(r"[FE ]*P?", g["txt"].strip())                     # logo FEP
          and not (g["bbox"][2] - g["bbox"][0] < 65 and len(g["txt"].strip()) <= 5)]  # ruído miúdo
    gs = sorted(gs, key=lambda g: (g["t0"], g["bbox"][1]))
    usado, out = set(), []
    for i, g in enumerate(gs):
        if i in usado:
            continue
        bl = [g]
        usado.add(i)
        mudou = True
        while mudou:
            mudou = False
            for j, h in enumerate(gs):
                if j in usado:
                    continue
                for b in bl:
                    ov = min(b["t1"], h["t1"]) - max(b["t0"], h["t0"])
                    curto = min(b["t1"] - b["t0"], h["t1"] - h["t0"])
                    lh = max(b["bbox"][3] - b["bbox"][1], h["bbox"][3] - h["bbox"][1])
                    gap = max(h["bbox"][1] - b["bbox"][3], b["bbox"][1] - h["bbox"][3])
                    hx = min(b["bbox"][2], h["bbox"][2]) - max(b["bbox"][0], h["bbox"][0])
                    mesma_dur = abs(b["t0"] - h["t0"]) <= 0.7 and abs(b["t1"] - h["t1"]) <= 0.7
                    if (mesma_dur and ov >= 0.6 * curto and gap < 0.6 * lh
                            and hx > 0.25 * min(b["bbox"][2] - b["bbox"][0], h["bbox"][2] - h["bbox"][0])):
                        bl.append(h)
                        usado.add(j)
                        mudou = True
                        break
        bl.sort(key=lambda x: x["bbox"][1])
        out.append({"linhas": [{"bbox": x["bbox"], "txt": x["txt"]} for x in bl],
                    "t0": min(x["t0"] for x in bl), "t1": max(x["t1"] for x in bl),
                    "bbox": [min(x["bbox"][0] for x in bl), min(x["bbox"][1] for x in bl),
                             max(x["bbox"][2] for x in bl), max(x["bbox"][3] for x in bl)],
                    "pt": " / ".join(x["txt"] for x in bl), "n": max(x["n"] for x in bl)})
    out.sort(key=lambda b: (b["t0"], b["bbox"][1]))
    for k, b in enumerate(out):
        b["id"] = k
    return out


def montar(blocos_json, es_json, cfg_json):
    bl = json.load(open(blocos_json))
    es = json.load(open(es_json))
    ajustes = es.pop("_ajustes", {})
    faltam = [b["id"] for b in bl if str(b["id"]) not in es]
    if faltam:
        sys.exit(f"faltam traduções para os blocos {faltam}")
    for b in bl:
        v = es[str(b["id"])]
        if v is None:
            b["acao"] = "manter"
        else:
            b["es"] = v
        b.update(ajustes.get(str(b["id"]), {}))
    json.dump({"blocos": bl}, open(cfg_json, "w"), ensure_ascii=False, indent=0)
    print("ok", sum(1 for b in bl if "es" in b), "blocos traduzidos")


def main():
    cmd = sys.argv[1]
    if cmd == "ocr":
        ocr(*sys.argv[2:5])
    elif cmd == "blocos":
        bs = blocos(agrupar(json.load(open(sys.argv[2]))))
        json.dump(bs, open(sys.argv[3], "w"), ensure_ascii=False, indent=0)
        for b in bs:
            print(f'{b["id"]:3d} {b["t0"]:6.2f}-{b["t1"]:6.2f} y{b["bbox"][1]:4d} x{b["bbox"][0]:4d}-{b["bbox"][2]:4d} | {b["pt"]}')
    elif cmd == "montar":
        montar(*sys.argv[2:5])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
