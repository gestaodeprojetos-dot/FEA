#!/usr/bin/env python3
"""Renderiza os vídeos do projeto e cola o CTA no final, em qualidade total.

1. fea_editar_video.py --entrega (H.264 CRF 18, áudio AAC 192k 48 kHz)
2. Junta o CTA com stream copy: sem recompressão, sem limite de tamanho

Limite de duração (Keila, 02/10/2026): vídeo final com CTA até 3 min.

Uso:
    python3 fea_render_com_cta.py projeto.json CTA.mp4 [trecho_do_nome ...]
"""
import json, os, subprocess, sys, tempfile

LIMITE_TOTAL_S = 180
AQUI = os.path.dirname(os.path.abspath(__file__))


def duracao(ff, caminho):
    r = subprocess.run([ff, "-i", caminho], capture_output=True, text=True)
    for linha in r.stderr.splitlines():
        if "Duration:" in linha:
            h, m, s = linha.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0


def main(projeto, cta, so):
    projeto, cta = os.path.abspath(projeto), os.path.abspath(cta)
    pasta = os.path.dirname(projeto)
    cfg = json.load(open(projeto, encoding="utf-8"))
    ff = cfg.get("ffmpeg", "ffmpeg")

    subprocess.run([sys.executable, os.path.join(AQUI, "fea_editar_video.py"), projeto, "--entrega", *so],
                   cwd=pasta, check=True)

    acima = []
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        base = os.path.join(pasta, v["saida"])
        if v.get("sem_cta"):   # versão sem o CTA de campanha (ex.: a do CTA da FEB falado pelo Dr.)
            d = duracao(ff, base)
            print(f"{'OK' if d <= LIMITE_TOTAL_S else 'ACIMA DE 3 MIN'} (sem CTA): {v['saida']} | {d:.1f}s", flush=True)
            if d > LIMITE_TOTAL_S:
                acima.append(v["saida"])
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=pasta) as lista:
            lista.write(f"file '{base}'\nfile '{cta}'\n")
        final = base + ".final.mp4"
        subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista.name,
                        "-c", "copy", "-movflags", "+faststart", final], check=True)
        os.unlink(lista.name)
        os.replace(final, base)
        d = duracao(ff, base)
        mb = os.path.getsize(base) / 1024 / 1024
        marca = "OK" if d <= LIMITE_TOTAL_S else "ACIMA DE 3 MIN"
        if d > LIMITE_TOTAL_S:
            acima.append(v["saida"])
        print(f"{marca}: {v['saida']} | {d:.1f}s | {mb:.1f} MB", flush=True)

    if acima:
        sys.exit("ERRO: passam de 3 min com CTA, cortar mais: " + ", ".join(acima))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
