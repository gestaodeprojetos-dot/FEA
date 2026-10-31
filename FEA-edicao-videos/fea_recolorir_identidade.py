#!/usr/bin/env python3
"""FEA: troca a cor de identidade de um vídeo (ex.: roxo da FEP Experience -> azul-gelo do Elite).

Só os pixels cuja matiz cai na faixa de origem (e com saturação mínima) mudam de cor;
pele, terno, cabelo e fundo neutro ficam como estão. A transição nas bordas da faixa
é suave, para não aparecer serrilhado no brilho.

Uso:
    python3 fea_recolorir_identidade.py entrada.mp4 saida.mp4 [--quadro SEG saida.png]
Parâmetros (padrão = roxo FEP -> azul-gelo Elite, medido no KV "FEA-YT-KV-ELITE-TT-LOGO"):
    --de 245 330      faixa de matiz de origem, em graus
    --para 198        matiz de destino, em graus (Elite: RGB médio 67,104,120)
    --sat 0.70        fator de saturação aplicado aos pixels trocados (Elite é mais frio e menos saturado)
    --ffmpeg CAMINHO  binário do FFmpeg (padrão: ffmpeg do PATH)
Saída em H.264 CRF 18, yuv420p, áudio original copiado (nunca HEVC: abre preto no computador da Keila).
"""
import argparse
import subprocess
import sys

import numpy as np


def rgb_para_hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r)
    gm = m & (mx == g) & ~rm
    bm = m & ~rm & ~gm
    h[rm] = ((g[rm] - b[rm]) / d[rm]) % 6
    h[gm] = (b[gm] - r[gm]) / d[gm] + 2
    h[bm] = (r[bm] - g[bm]) / d[bm] + 4
    h = h * 60.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx


def hsv_para_rgb(h, s, v):
    c = v * s
    hp = (h / 60.0) % 6
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(h)
    i = np.floor(hp).astype(int)
    r = np.choose(i, [c, x, z, z, x, c])
    g = np.choose(i, [x, c, c, x, z, z])
    b = np.choose(i, [z, z, x, c, c, x])
    mm = v - c
    return np.stack([r + mm, g + mm, b + mm], -1)


def recolorir(quadro, de, para, fator_sat):
    rgb = quadro.astype(np.float32) / 255.0
    h, s, v = rgb_para_hsv(rgb)
    lo, hi = de
    borda = 15.0
    # peso 1 dentro da faixa, rampa de 15 graus nas bordas, 0 fora
    peso = np.clip(np.minimum(h - (lo - borda), (hi + borda) - h) / borda, 0, 1)
    peso *= np.clip((s - 0.12) / 0.13, 0, 1)  # cinza/neutro não muda
    novo = hsv_para_rgb(np.full_like(h, para), s * fator_sat, v)
    out = rgb * (1 - peso[..., None]) + novo * peso[..., None]
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


def medir(ff, entrada):
    p = subprocess.run([ff.replace("ffmpeg", "ffprobe") if "ffprobe" not in ff else ff, "-v", "error",
                        "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                        "-of", "csv=p=0", entrada], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip():
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,r_frame_rate", "-of", "csv=p=0", entrada],
                           capture_output=True, text=True, check=True)
    w, h, fps = p.stdout.strip().split(",")[:3]
    return int(w), int(h), fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--de", nargs=2, type=float, default=[245, 330])
    ap.add_argument("--para", type=float, default=198)
    ap.add_argument("--sat", type=float, default=0.70)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--quadro", type=float, help="só gera um PNG de teste neste segundo (saida = .png)")
    a = ap.parse_args()
    w, h, fps = medir(a.ffmpeg, a.entrada)

    ler = [a.ffmpeg, "-v", "error"]
    if a.quadro is not None:
        ler += ["-ss", str(a.quadro)]
    ler += ["-i", a.entrada, "-f", "rawvideo", "-pix_fmt", "rgb24"]
    if a.quadro is not None:
        ler += ["-frames:v", "1"]
    ler += ["-"]
    dec = subprocess.Popen(ler, stdout=subprocess.PIPE)

    if a.quadro is not None:
        from PIL import Image
        q = np.frombuffer(dec.stdout.read(w * h * 3), np.uint8).reshape(h, w, 3)
        Image.fromarray(recolorir(q, a.de, a.para, a.sat)).save(a.saida)
        return

    enc = subprocess.Popen([a.ffmpeg, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{w}x{h}", "-r", fps, "-i", "-", "-i", a.entrada,
                            "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "slow",
                            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy",
                            "-movflags", "+faststart", a.saida], stdin=subprocess.PIPE)
    n = 0
    tam = w * h * 3
    while True:
        buf = dec.stdout.read(tam)
        if len(buf) < tam:
            break
        q = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        enc.stdin.write(recolorir(q, a.de, a.para, a.sat).tobytes())
        n += 1
        if n % 90 == 0:
            print(f"  {n} quadros", file=sys.stderr)
    enc.stdin.close()
    enc.wait()
    dec.wait()
    print(f"OK: {n} quadros -> {a.saida}")


if __name__ == "__main__":
    main()
