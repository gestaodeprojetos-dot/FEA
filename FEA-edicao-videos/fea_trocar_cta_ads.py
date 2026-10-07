#!/usr/bin/env python3
"""FEA: corta trechos de fala de um Ads já editado e troca o CTA do final.

Os Ads de Black Friday Vitalícia chegam prontos (legenda queimada e CTA antigo no fim).
Este script mantém só os trechos listados no projeto, remove o CTA antigo e cola o CTA novo.
Os cortes caem no silêncio entre palavras (transcrição com tempo por palavra, fea_transcrever.py
ou equivalente), com 20 ms de fade no áudio para não estalar.

Uso:
    python3 fea_trocar_cta_ads.py projeto.json PASTA_BRUTOS PASTA_TRANSCRICOES CTA.mp4 PASTA_SAIDA [098 099 ...]

PASTA_BRUTOS tem os arquivos "Ads NNN - BFV" e PASTA_TRANSCRICOES tem NNN.json (segmentos com
"words": [{s, e, w}]). Saída: H.264 CRF 18, 1080x1920, 30 fps, AAC 192k 48 kHz.
"""
import glob, json, os, subprocess, sys

FPS = 30
FADE = 0.02


def palavras(caminho):
    return [w for s in json.load(open(caminho, encoding="utf-8")) for w in s["words"]]


def limites(ws, ini, ult, fim_max):
    """Converte [início da 1a palavra, início da última] em tempos de corte no silêncio."""
    i = min(range(len(ws)), key=lambda k: abs(ws[k]["s"] - ini)) if ini > 0 else None
    j = min(range(len(ws)), key=lambda k: abs(ws[k]["s"] - ult))
    if i is None:
        a = 0.0
    else:
        ant = ws[i - 1]["e"] if i > 0 else 0.0
        a = max(ws[i]["s"] - 0.12, (ant + ws[i]["s"]) / 2)
    prox = ws[j + 1]["s"] if j + 1 < len(ws) else fim_max
    b = min(ws[j]["e"] + 0.25, (ws[j]["e"] + prox) / 2, fim_max)
    return round(a, 3), round(b, 3)


def main(projeto, brutos, transcr, cta, saida, so):
    cfg = json.load(open(projeto, encoding="utf-8"))
    os.makedirs(saida, exist_ok=True)
    for n, v in cfg["videos"].items():
        if so and n not in so:
            continue
        bruto = glob.glob(os.path.join(brutos, f"Ads {n} - BFV*"))[0]
        ws = palavras(os.path.join(transcr, f"{n}.json"))
        trechos = [limites(ws, a, b, v["fim_cta_antigo"]) for a, b in v["manter"]]
        f, k = [], len(trechos)
        for i, (a, b) in enumerate(trechos):
            d = b - a
            f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},scale=1080:1920,setsar=1,format=yuv420p[v{i}]")
            f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,"
                     f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{i}]")
        f.append(f"[1:v]fps={FPS},scale=1080:1920,setsar=1,format=yuv420p[vc]")
        f.append("[1:a]aresample=48000[ac]")
        pares = "".join(f"[v{i}][a{i}]" for i in range(k)) + "[vc][ac]"
        f.append(f"{pares}concat=n={k + 1}:v=1:a=1[v][a]")
        destino = os.path.join(saida, f"FEA-Ads {n} - BFV - CTA comente.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-i", cta, "-filter_complex", ";".join(f),
                        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", destino],
                       check=True)
        print(f"{n}: trechos {trechos} -> {os.path.basename(destino)}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    main(*sys.argv[1:6], sys.argv[6:])
