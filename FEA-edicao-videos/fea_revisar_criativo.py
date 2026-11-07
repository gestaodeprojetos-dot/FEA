#!/usr/bin/env python3
"""FEA: revisão automática dos criativos (fea_editar_criativo.py) antes da entrega.

Uso: python3 fea_revisar_criativo.py projeto.json [trecho_do_nome ...]

Confere em cada vídeo final:
  - abertura: a voz do Dr. começa em até 0,15 s (Keila, 07/11: nada de respiro no começo);
  - cortes: cada emenda cai em silêncio, não no meio de palavra;
  - legenda: cada bloco tem voz durante pelo menos 35% do tempo na tela;
  - duração: entre 30 s e 70 s (roteiro: 45 a 60 s).
Imprime ERRO / ATENÇÃO por vídeo e um resumo final.
"""
import json
import re
import sys

import fea_editar_criativo as cr
import fea_editar_video as fe


def tempo_ass(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def revisar(cfg, v):
    ff = cfg["ffmpeg"]
    probs = []
    trechos, ass, duracao, cartelas, palavras, broll = cr.montar(cfg, v)
    db, lim, passo = fe.perfil_voz(ff, v["saida"])
    # abertura
    ini = next((i * passo for i in range(len(db) - 4) if all(db[j] >= lim for j in range(i, i + 4))), 0)
    if ini > 0.15:
        probs.append(("ERRO", f"respiro no começo: voz só aos {ini:.2f} s"))
    # emendas
    t = 0.0
    for nome, arq, a, b in trechos[:-1]:
        t += b - a
        i = int(t / passo)
        antes = db[max(0, i - 1)]
        depois = db[min(len(db) - 1, i + 1)]
        if antes >= lim + 4 and depois >= lim + 4:
            probs.append(("ATENÇÃO", f"emenda aos {t:.2f} s com voz dos dois lados ({antes:.0f}/{depois:.0f} dB)"))
    # legendas
    for ln in open(ass, encoding="utf-8"):
        if not ln.startswith("Dialogue") or ",Legenda," not in ln:
            continue
        p = ln.split(",", 9)
        s, e = tempo_ass(p[1]), tempo_ass(p[2])
        txt = re.sub(r"\{[^}]*\}", "", p[9]).strip()
        ja = [x for x in probs if x[1].endswith(f"[{p[1]}]")]
        if ja:
            continue
        i0, i1 = int(s / passo), max(int(s / passo) + 1, int(e / passo))
        voz = sum(1 for i in range(i0, min(i1, len(db))) if db[i] >= lim - 6) / max(1, i1 - i0)
        if voz < 0.35 and e - s > 0.3:
            probs.append(("ATENÇÃO", f"legenda sem voz ({voz:.0%}) aos {s:.1f} s: \"{txt}\" [{p[1]}]"))
    if not 30 <= duracao <= 70:
        probs.append(("ATENÇÃO", f"duração {duracao:.1f} s fora de 30 a 70 s"))
    return duracao, ini, probs


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    so = sys.argv[2:] or None
    total = {"ERRO": 0, "ATENÇÃO": 0}
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d, ini, probs = revisar(cfg, v)
        nome = v["saida"].rsplit("/", 1)[-1]
        print(f"{nome}: {d:.1f} s, voz aos {ini:.2f} s, {len(probs)} ponto(s)")
        for nivel, msg in probs:
            total[nivel] += 1
            print(f"   {nivel}: {msg}")
    print(f"RESUMO: {total['ERRO']} ERRO, {total['ATENÇÃO']} ATENÇÃO")


if __name__ == "__main__":
    main()
