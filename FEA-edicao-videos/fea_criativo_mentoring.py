#!/usr/bin/env python3
"""FEA: criativos do Elite Mentoring no mesmo estilo de edição aprovado para o Elite Experience
(modelo Luca: tarja de público, legenda curta, destaques, tela dividida com lista, cards, trilha de
impacto, CTA final), trocando só a identidade para a da Mentoring (pasta IDENTIDADE VISUAL do produto):
petróleo #011A24, verde-água #2EB9B3, água clara #86F9F8, logotipos oficiais EM_Asset (FEA-mentoring-marca/).

Uso:  python3 fea_criativo_mentoring.py projeto.json [filtro ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_criativo_elite_v3 as v3   # noqa: E402
v2, ce = v3.v2, v3.ce

CORES = {"FUNDO": "#011A24", "GRANADA": "#1E8F8A", "BORDO": "#0B3A3E", "ROSE": "#2EB9B3", "CLARO": "#E6FFFE"}
for mod in (ce, v2, v3):
    for k, val in CORES.items():
        if hasattr(mod, k):
            setattr(mod, k, val)
ce.MARCA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FEA-mentoring-marca")


def metalico(larg, alt):
    """Degradê verde-água da marca Mentoring (no lugar do rosé metálico do Experience)."""
    import numpy as np
    from PIL import Image
    paradas = [(0.0, ce.rgb("#2EB9B3")), (0.45, ce.rgb("#86F9F8")), (0.55, ce.rgb("#C9FFFE")),
               (0.8, ce.rgb("#5CD6D1")), (1.0, ce.rgb("#1E8F8A"))]
    x = np.linspace(0, 1, larg)
    cols = np.zeros((larg, 3))
    for (a, ca), (b, cb) in zip(paradas, paradas[1:]):
        m = (x >= a) & (x <= b)
        t = ((x[m] - a) / (b - a))[:, None]
        cols[m] = np.array(ca) * (1 - t) + np.array(cb) * t
    y = np.linspace(-1, 1, alt)[:, None, None]
    return Image.fromarray(np.clip(cols[None, :, :] * (1 - 0.08 * y), 0, 255).astype("uint8"), "RGB")


ce.metalico = metalico


def main():
    args = sys.argv[1:]
    cfg = json.load(open(args[0], encoding="utf-8"))
    for v in cfg["videos"]:
        if args[1:] and not any(x in v["saida"] for x in args[1:]):
            continue
        if v.get("destaques_grandes"):
            v2.DESTAQUES[:] = [tuple(x) for x in v["destaques_grandes"]]
        print(f"{v['saida']}: {v3.renderizar(cfg, v):.1f}s", flush=True)


if __name__ == "__main__":
    main()
