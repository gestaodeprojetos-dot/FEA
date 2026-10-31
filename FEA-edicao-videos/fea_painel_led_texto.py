#!/usr/bin/env python3
"""FEA: entrada do Dr. no painel LED 4032x1344 com o bloco de texto centralizado na altura.

O Dr. fica enquadrado com 80 px de folga em cima; o texto (JOÃO PITHON / @DRJOAOPITHON /
Médico, Professor e Pesquisador) sobe DESLOC px para ter o mesmo respiro em cima e embaixo
(pedido do Luca, 31/10/2026). Como texto e Dr. estão no mesmo vídeo, a área do texto vem de
um segundo enquadramento (DESLOC px mais baixo na fonte) e entra por uma máscara que
acompanha o Dr. quadro a quadro (fica sempre à esquerda dele) e não cobre os raios do canto.

O texto é digitado na posição original e sobe até o centro (quadros SOBE) já afastado do Dr.\n\nUso: python3 fea_painel_led_texto.py entrada_1920x1080.mp4 saida.mp4
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H = 4032, 1344
DESLOC = 218           # texto ia de 515 a 1264 (margens 515/79); centralizado = 297 a 1046
CROP_Y = 93            # enquadramento do Dr. (80 px acima do cabelo)
SOBE = (200, 222)      # o texto é digitado na posição original (nasce de trás do Dr.) e, já
                       # afastado dele, sobe suave até o centro entre estes quadros


def filtro(y):
    return ("crop=1904:1080:8:0,scale=3484:1976:flags=lanczos,"
            f"crop=3484:1344:0:'{y}',split=3[c][l][r];"
            "[l]crop=200:1344:0:0,hflip,scale=274:1344[L];"
            "[r]crop=200:1344:3284:0,hflip,scale=274:1344[R];"
            "[L][c][R]hstack=inputs=3[v]")


def leitor(ent, y):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-i", ent, "-filter_complex", filtro(y), "-map", "[v]",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)


def borda_dr(q):
    """x mais à esquerda do Dr. (pele da mão/rosto, com folga para o terno), em resolução reduzida."""
    p = q[::8, ::8].astype(np.int16)
    pele = (p[..., 0] > 110) & (p[..., 0] > p[..., 2] + 20) & (p[..., 1] > 60)
    cols = np.where(pele[30:].sum(0) > 2)[0]
    return None if len(cols) == 0 else int(cols.min()) * 8 - 110


def main():
    ent, sai = sys.argv[1:3]
    u = f"clip((n-{SOBE[0]})/{SOBE[1] - SOBE[0]},0,1)"
    a = leitor(ent, CROP_Y)
    b = leitor(ent, f"{CROP_Y}+{DESLOC}*({u}*{u}*(3-2*{u}))")   # deslocamento com aceleração suave
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", "30", "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                            "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy",
                            "-movflags", "+faststart", sai], stdin=subprocess.PIPE)
    yy = np.arange(H, dtype=np.float32)[:, None]
    xx = np.arange(W, dtype=np.float32)[None, :]
    vert = np.clip((yy - 200) / 80, 0, 1)          # não mexe nos raios do canto de cima
    tam = W * H * 3
    n, borda = 0, None
    while True:
        ba, bb = a.stdout.read(tam), b.stdout.read(tam)
        if len(ba) < tam or len(bb) < tam:
            break
        qa = np.frombuffer(ba, np.uint8).reshape(H, W, 3)
        qb = np.frombuffer(bb, np.uint8).reshape(H, W, 3)
        if n < SOBE[0]:
            out = qa
        else:
            e = borda_dr(qa)
            borda = e if e is not None else borda
            lim = min(borda if borda is not None else 1900, 1900)
            horiz = np.clip((lim - xx) / 250, 0, 1)   # emenda longa no escuro da arena (texto acaba em x=1631)
            m = (horiz * vert)[..., None]
            out = (qa * (1 - m) + qb * m + 0.5).astype(np.uint8)
        enc.stdin.write(out.tobytes())
        n += 1
        if n % 150 == 0:
            print(f"  {n} quadros", file=sys.stderr)
    enc.stdin.close()
    enc.wait()
    print("OK", n, "quadros")


if __name__ == "__main__":
    main()
