#!/usr/bin/env python3
"""FEA: gera o CTA final de 5 s dos anúncios de Masterclass (padrão dos Ads 54 e 55 - MPL).

Quadro off-white (#FBFBFB), logo da masterclass entrando com fade e "Toque em Saiba Mais"
(Montserrat Bold, #0A343C) digitado letra a letra, com som de digitação.
Tempos medidos quadro a quadro no Ads 54 (11/11/2026):
  - logo: fade de 0,07 s a 0,47 s, caixa final x 149-926, y 664-1053
  - texto: alinhado à esquerda em x 210, topo do texto em y 1214, digitado de 0,77 s a 1,23 s
  - som: 1,5 s de digitação no início do CTA, depois silêncio

Sai em H.264 CRF 18, 1080x1920, 30 fps, AAC 192k 48 kHz estéreo: o mesmo formato do
fea_editar_video.py --entrega, para o fea_render_com_cta.py juntar sem recompressão.

Uso:
    python3 fea_cta_masterclass.py LOGO.png SOM_DIGITACAO.wav FONTE_BOLD.ttf FFMPEG saida.mp4 [--texto "Toque em Saiba Mais"]
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 5.0
FUNDO = (251, 251, 251)
COR_TEXTO = (10, 52, 60)
LOGO_X0, LOGO_X1, LOGO_Y0 = 149, 926, 664
TEXTO_X, TEXTO_Y, TEXTO_TAM = 210, 1214, 60
FADE_INI, FADE_FIM = 2, 14          # quadros
DIGITA_INI, DIGITA_FIM = 23, 37     # quadros


def logo_recortado(caminho):
    im = Image.open(caminho).convert("RGBA")
    a = np.array(im)
    # fundo branco ou transparente fora do desenho
    tinta = (a[..., 3] > 20) & (a[..., :3].min(2) < 235)
    ys, xs = np.where(tinta)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    larg = LOGO_X1 - LOGO_X0
    im = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    # branco do PNG vira transparente para assentar no off-white
    a = np.array(im).astype(np.float32)
    branco = a[..., :3].min(2)
    alfa = np.clip((255 - branco) / 255 * 6, 0, 1) * (a[..., 3] / 255)
    # desfaz a mistura com branco para manter a cor cheia nas bordas
    with np.errstate(divide="ignore", invalid="ignore"):
        cor = np.where(alfa[..., None] > 0, (a[..., :3] - 255 * (1 - alfa[..., None])) / alfa[..., None], 0)
    a[..., :3] = np.clip(cor, 0, 255)
    a[..., 3] = alfa * 255
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def main(logo, som, fonte, ff, saida, texto="Toque em Saiba Mais"):
    lg = logo_recortado(logo)
    font = ImageFont.truetype(fonte, TEXTO_TAM)
    topo = font.getbbox(texto)[1]
    n = int(DUR * FPS)
    enc = subprocess.Popen(
        [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", som, "-filter_complex",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{DUR}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-ac", "2", "-t", str(DUR), "-movflags", "+faststart", saida], stdin=subprocess.PIPE)
    for i in range(n):
        q = Image.new("RGB", (W, H), FUNDO)
        alfa = min(1.0, max(0.0, (i - FADE_INI) / (FADE_FIM - FADE_INI)))
        if alfa > 0:
            l = lg.copy()
            l.putalpha(l.getchannel("A").point(lambda v: int(v * alfa)))
            q.paste(l, (LOGO_X0, LOGO_Y0), l)
        letras = round(len(texto) * min(1.0, max(0.0, (i - DIGITA_INI + 1) / (DIGITA_FIM - DIGITA_INI + 1))))
        if letras:
            ImageDraw.Draw(q).text((TEXTO_X, TEXTO_Y - topo), texto[:letras], font=font, fill=COR_TEXTO)
        enc.stdin.write(q.tobytes())
    enc.stdin.close()
    if enc.wait():
        sys.exit("ERRO no FFmpeg ao gerar o CTA")
    print(f"CTA pronto: {saida}")


if __name__ == "__main__":
    args = sys.argv[1:]
    txt = "Toque em Saiba Mais"
    if "--texto" in args:
        k = args.index("--texto")
        txt = args[k + 1]
        del args[k:k + 2]
    if len(args) != 5:
        sys.exit(__doc__)
    main(*args, texto=txt)
