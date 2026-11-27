#!/usr/bin/env python3
"""FEA: cartela final "Comente BLACK" do CTA Black Vitalícia Ads 022 (Keila, 21/10/2026).

Só arquivos oficiais da pasta Black Vitalícia do Drive (1s1hs4Pmy4BZCUj5q82IeUQFcDyzfipoU),
sem imagem de IA. TRAB precisa ter:
    bfv/        a pasta baixada inteira (logo em 02 - LOGOTIPO/PNG, KV em 03 - 2026/banner.pdf)
    kvimg/banner1080.png   pdftoppm -png -scale-to-x 1080 -scale-to-y -1 -singlefile banner.pdf kvimg/banner1080
    fonts/Montserrat-ExtraBold.ttf   (fea_preparar_ambiente.sh)

Uso:
    python3 fea_cartela_comente_black.py TRAB     # gera TRAB/cartela/FEA-cartela-comente-black.png

Montagem do CTA (Ads 022 até 20,400 s + cartela 3 s, fade-in 0,3 s, áudio com fade e silêncio):
    ffmpeg -i "Ads 022 ..." -loop 1 -framerate 30 -t 3 -i cartela.png -f lavfi -t 3 -i anullsrc=r=48000:cl=stereo
      -filter_complex "[0:v]trim=end_frame=612,setpts=PTS-STARTPTS,fps=30,format=yuv420p,setsar=1[v0];
        [0:a]atrim=0:20.4,asetpts=PTS-STARTPTS,afade=t=out:st=20.10:d=0.30[a0];
        [1:v]fps=30,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.3[v1];[v0][a0][v1][2:a]concat=n=2:v=1:a=1[v][a]"
      -map [v] -map [a] -c:v libx264 -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 FEA-CTA-Ads022-comente-black.mp4
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
W, H = 1080, 1920
logo = Image.open(f"{S}/bfv/02 - LOGOTIPO/PNG/Black Vitalícia/BFV_Asset 15@4x.png").convert("RGBA")
a = np.asarray(logo); m = a[..., 3] > 200
px = a[m][:, :3]; gold = px[(px[:, 0] - px[:, 2]) > 60]
GOLD = tuple(int(v) for v in np.median(gold, axis=0)); print("dourado do logo", GOLD, "#%02X%02X%02X" % GOLD)
kv = Image.open(f"{S}/kvimg/banner1080.png").convert("RGB")
tela = Image.new("RGB", (W, H), (0, 0, 0))
# palco e raios do KV 2026 (parte de baixo do banner, sem texto), topo esmaecido para o preto
palco = kv.crop((0, 1040, 1080, kv.height))
esc = 1.12
palco = palco.resize((int(palco.width * esc), int(palco.height * esc)), Image.LANCZOS)
palco = palco.crop(((palco.width - W) // 2, 0, (palco.width - W) // 2 + W, palco.height))
alfa = np.ones((palco.height, W), np.float32)
f = 320; alfa[:f] = (np.linspace(0, 1, f) ** 1.6)[:, None]
pm = Image.fromarray((alfa * 255).astype(np.uint8))
tela.paste(palco, (0, H - palco.height), pm)
# brilho central do KV (linha de luz entre o logo e o texto)
luz = np.asarray(kv.crop((140, 690, 940, 800))).astype(np.float32)
luz = np.clip((luz - 34) * (255 / (255 - 34)), 0, 255)   # tira o fundo do banner, fica só o brilho
xs = np.linspace(-1, 1, luz.shape[1]); luz *= np.clip(1.4 - np.abs(xs) * 1.4, 0, 1)[None, :, None]
tela_np = np.asarray(tela).astype(np.float32)
y0, x0 = 890, 140
reg = tela_np[y0:y0 + luz.shape[0], x0:x0 + luz.shape[1]]
tela_np[y0:y0 + luz.shape[0], x0:x0 + luz.shape[1]] = np.maximum(reg, luz)
tela = Image.fromarray(tela_np.clip(0, 255).astype(np.uint8))
# logo oficial
lw = 880; lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
tela.paste(lg, ((W - lw) // 2, 560), lg)
d = ImageDraw.Draw(tela)
fnt1 = ImageFont.truetype(f"{S}/fonts/Montserrat-ExtraBold.ttf", 118)
fnt2 = ImageFont.truetype(f"{S}/fonts/Montserrat-ExtraBold.ttf", 230)
def centro(txt, fnt, y, cor):
    b = d.textbbox((0, 0), txt, font=fnt); w = b[2] - b[0]
    d.text(((W - w) // 2 - b[0], y - b[1]), txt, font=fnt, fill=cor)
    return b[3] - b[1]
centro("Comente", fnt1, 1030, (255, 255, 255))
centro("BLACK", fnt2, 1185, GOLD)
tela.save(f"{S}/cartela/FEA-cartela-comente-black.png")
