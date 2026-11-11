#!/usr/bin/env python3
"""FEA: revisão automática dos criativos (fea_editar_criativo.py) antes da entrega.

Uso: python3 fea_revisar_criativo.py projeto.json [trecho_do_nome ...]

Confere em cada vídeo final:
  - abertura: a voz do Dr. começa em até 0,2 s (Keila, 07/11: nada de respiro no começo);
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
    # perfil de voz montado dos brutos, trecho a trecho, na linha do tempo final: com a trilha de
    # fundo, medir o vídeo final acusava "respiro" falso (a música mexe no limiar de voz)
    import numpy as np
    cache, partes, lim, passo = {}, [], None, 0.05
    for nome, arq, a, b in trechos:
        if arq not in cache:
            cache[arq] = fe.perfil_voz(ff, arq)
        rdb, rlim, passo = cache[arq]
        lim = rlim if lim is None else lim
        partes.append(rdb[int(a / passo):int(b / passo)])
    db = np.concatenate(partes)
    # abertura
    # sílaba forte seguida de fala (a voz oscila entre sílabas: 4 janelas seguidas acima do limiar
    # dava falso "respiro" quando a 1ª palavra tinha uma consoante fraca no meio)
    ini = next((i * passo for i in range(len(db) - 6)
                if db[i] >= lim + 6 and sum(db[j] >= lim - 3 for j in range(i + 1, i + 6)) >= 3), 0)
    i = int(ini / passo)
    while i > 0 and db[i - 1] >= lim - 10:   # a 1ª sílaba costuma ser mais baixa
        i -= 1
    j = i - 1                                  # palavra baixa antes de micropausa ("Eu... sempre")
    while j > max(0, i - int(0.5 / passo)):
        if db[j] >= lim and db[j - 1] >= lim - 4:
            while j > 0 and db[j - 1] >= lim - 10:
                j -= 1
            i = j
            break
        j -= 1
    ini = i * passo
    if ini > 0.2:
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
