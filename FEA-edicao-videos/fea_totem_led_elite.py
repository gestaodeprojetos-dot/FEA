#!/usr/bin/env python3
"""FEA: arte do elevador Elite (Modelo 2, 1024x1024) adaptada ao totem LED 344x1032.

Mantém o fundo da arte do elevador (arena azul + brilho e estrelas no alto, sem a porta),
os mesmos elementos (Bem-vindos, logo Elite, FEA, Elite Mentoring horizontal) e o mesmo
movimento de fundo do vídeo do elevador (diferença quadro a quadro do 2B aplicada ao fundo limpo).

Uso: python3 fea_totem_led_elite.py PASTA_ELEVADOR PASTA_ELEMENTOS SAIDA_PREFIXO [--efeito]
  PASTA_ELEVADOR: com '2A ...mp4' e '2B ...mp4' do elevador
  PASTA_ELEMENTOS: bemvindos.png, elite_logo.png, fea.png, ment_h.png (RGBA)
Gera SAIDA_PREFIXO.png (quadro estático) e SAIDA_PREFIXO.mp4 (12 s, 30 fps, sem áudio).
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H = 344, 1024           # monta em 1024 de altura (escala do elevador) e estica para 1032 no fim
HF = 1032
TOPO_FIM, EMENDA = 250, 330  # topo vem do centro da arte; abaixo disso, das laterais da arena
COL_E, COL_D = (36, 208), (816, 988)


def quadros(video):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(1024 * 1024 * 3)
        if len(b) < 1024 * 1024 * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(1024, 1024, 3).astype(np.float32)


def remontar(f):
    """1024x1024 do elevador -> 344x1024 sem porta."""
    topo = f[:, 340:684]
    lat = np.concatenate([f[:, COL_E[0]:COL_E[1]], f[:, COL_D[0]:COL_D[1]]], 1)
    a = np.clip((np.arange(1024) - TOPO_FIM) / (EMENDA - TOPO_FIM), 0, 1)[:, None, None]
    return topo * (1 - a) + lat * a


def camada(pasta, nome, largura):
    im = Image.open(os.path.join(pasta, nome)).convert("RGBA")
    h = round(im.height * largura / im.width)
    return im.resize((largura, h), Image.LANCZOS)


def main():
    elev, elem, saida = sys.argv[1:4]
    efeito = "--efeito" in sys.argv
    a2 = glob.glob(os.path.join(elev, "2A*.mp4"))[0]
    b2 = glob.glob(os.path.join(elev, "2B*.mp4"))[0]
    limpo = next(quadros(a2))  # quadro 0 do 2A: fundo sem nenhum texto

    # posições no padrão do elevador (Bem-vindos y=67, logo logo abaixo; FEA e mentoria sobre a arena)
    # tempos medidos quadro a quadro no 2A do elevador: (entra_ini, entra_fim, sai_ini, sai_fim) em quadros
    itens = [
        (camada(elem, "bemvindos.png", 230), 67, (9, 22, 337, 345)),
        (Image.new("RGBA", (48, 2), (190, 205, 212, 140)), 117, (15, 24, 332, 341)),
        (camada(elem, "elite_logo.png", 300), 136, (14, 28, 340, 350)),
        (camada(elem, "fea.png", 172), 548, (19, 30, 333, 343)),
        (camada(elem, "ment_h.png", 196), 672, (22, 30, 331, 340)),
    ]

    def compor(fundo, n):
        img = Image.fromarray(np.clip(fundo, 0, 255).astype(np.uint8)).convert("RGBA")
        for im, y, (e0, e1, s0, s1) in itens:
            dy = 0
            if efeito:
                if n < s0:
                    u = float(np.clip((n - e0) / (e1 - e0), 0, 1))
                    k = 1 - (1 - u) ** 3            # entra desacelerando (curva medida)
                    dy = round(8 * (1 - k))          # sobe ~8 px enquanto entra
                else:
                    u = float(np.clip((n - s0) / (s1 - s0), 0, 1))
                    k = 1 - u ** 2                   # sai acelerando
                if k <= 0.002:
                    continue
                c = im.filter(ImageFilter.GaussianBlur(5 * (1 - k))) if k < 1 else im.copy()
                al = np.array(c)[..., 3].astype(np.float32) * k
                c.putalpha(Image.fromarray(al.astype(np.uint8)))
            else:
                c = im
            img.alpha_composite(c, ((W - im.width) // 2, y + dy))
        return img.convert("RGB").resize((W, HF), Image.LANCZOS)

    b0 = None
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HF}",
                            "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", saida + ".mp4"], stdin=subprocess.PIPE)
    for n, fb in enumerate(quadros(b2)):
        if b0 is None:
            b0 = fb
        fundo = remontar(limpo + (fb - b0))
        q = compor(fundo, n)
        if n == 60:
            q.save(saida + ".png")
        enc.stdin.write(q.tobytes())
    enc.stdin.close()
    enc.wait()
    print("OK", saida, n + 1, "quadros")


if __name__ == "__main__":
    main()
