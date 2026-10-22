#!/usr/bin/env python3
"""Troca o CTA final de um criativo: mantém os trechos indicados do vídeo e cola o CTA novo no fim.

A trilha do CTA é ajustada para a mesma loudness (LUFS) do conteúdo mantido, para não dar salto de
volume na emenda. Cada corte interno ganha fade de 15 ms no áudio para não estalar.

Uso:
    python3 fea_trocar_cta.py FFMPEG entrada.mov CTA.mp4 saida.mp4 INICIO-FIM [INICIO-FIM ...]

Ex.: Ads 003, cortando "porque dia 20 de outubro" e o CTA antigo (a partir de 47,25 s):
    python3 fea_trocar_cta.py ffmpeg ads003.mp4 cta.mp4 out.mp4 0-19.30 21.27-47.25
"""
import re, subprocess, sys


def loudness(ffmpeg, arquivo, filtro=""):
    cadeia = (filtro + "," if filtro else "") + "ebur128"
    r = subprocess.run([ffmpeg, "-nostats", "-i", arquivo, "-map", "0:a", "-af", cadeia, "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def main():
    ffmpeg, entrada, cta, saida = sys.argv[1:5]
    trechos = [tuple(map(float, t.split("-"))) for t in sys.argv[5:]]
    sel = "+".join(f"between(t,{a},{b})" for a, b in trechos)
    ganho = loudness(ffmpeg, entrada, f"aselect='{sel}'") - loudness(ffmpeg, cta)

    partes, rot = [], []
    for i, (a, b) in enumerate(trechos):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,"
                      f"afade=t=in:d=0.015,afade=t=out:st={b - a - 0.015:.3f}:d=0.015[a{i}]")
        rot.append(f"[v{i}][a{i}]")
    n = len(trechos)
    partes.append(f"[1:v]fps=30,scale=1080:1920,setsar=1[vc]")
    partes.append(f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={ganho:.2f}dB,"
                  f"alimiter=limit=0.95[ac]")
    partes.append("".join(rot) + f"[vc][ac]concat=n={n + 1}:v=1:a=1[v][a]")

    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", entrada, "-i", cta,
                    "-filter_complex", ";".join(partes), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida], check=True)
    print(f"OK {saida} (CTA {ganho:+.1f} dB)")


if __name__ == "__main__":
    main()
