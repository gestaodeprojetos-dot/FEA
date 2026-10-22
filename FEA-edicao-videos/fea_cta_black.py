#!/usr/bin/env python3
"""CTA de 5 s da Black Friday Vitalícia (1080x1920, 30 fps): logo sem data + "Toque em Saiba Mais".

Fundo = banner.pdf da pasta "03 - 2026" da identidade visual, com logo, data e texto removidos
(sobram só o palco e os raios dourados). Logo = BFV_Asset 15@4x.png (BLACK FRIDAY branco,
VITALÍCIA dourado). Botão no estilo da pílula de data do banner (borda dourada, texto branco).

Trilha opcional: MUSICA a partir de INICIO segundos (impacto da batida cai quando a logo entra),
com fade-out no último 0,6 s. Sem MUSICA, sai com áudio mudo para concatenar.

Uso:
    python3 fea_cta_black.py FUNDO.png LOGO.png FONTE_BOLD.ttf FFMPEG saida.mp4 [MUSICA INICIO]
"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 5.0
DOURADO = (227, 172, 102)
TEXTO = "Toque em Saiba Mais"


def suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def faixa(t, ini, fim):
    return suave((t - ini) / (fim - ini))


def montar_fundo(caminho):
    img = Image.open(caminho).convert("RGB")
    # o banner tem 700x1000 pt; acima de y=160 pt era preto sólido (vetorial, removido junto com o logo)
    topo = int(img.height * 0.16) + 2
    ImageDraw.Draw(img).rectangle([0, 0, img.width, topo], fill=(0, 0, 0))
    # degradê para não marcar a emenda entre o preto e a foto do palco
    rampa = int(img.height * 0.14)
    mascara = Image.new("L", (1, rampa))
    mascara.putdata([round(255 * (1 - suave(y / rampa))) for y in range(rampa)])
    img.paste((0, 0, 0), (0, topo, img.width, topo + rampa), mascara.resize((img.width, rampa)))
    esc = H / img.height * 1.06  # margem para o zoom lento
    img = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    return img


def botao(fonte):
    f = ImageFont.truetype(fonte, 64)
    x0, y0, x1, y1 = f.getbbox(TEXTO)
    tw, th = x1 - x0, y1 - y0
    bw, bh = tw + 140, th + 76
    img = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    caixa = [20, 20, 20 + bw, 20 + bh]
    d.rounded_rectangle(caixa, radius=bh // 2, fill=(0, 0, 0, 150), outline=DOURADO, width=5)
    d.text((20 + (bw - tw) / 2 - x0, 20 + (bh - th) / 2 - y0), TEXTO, font=f, fill=(255, 255, 255))
    brilho = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(brilho).rounded_rectangle(caixa, radius=bh // 2, outline=DOURADO + (255,), width=12)
    brilho = brilho.filter(ImageFilter.GaussianBlur(14))
    return img, brilho


def seta(tam=46, esp=9):
    img = Image.new("RGBA", (tam * 2 + esp * 2, tam + esp * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).line([(esp, esp), (esp + tam, esp + tam), (esp + 2 * tam, esp)],
                             fill=DOURADO + (255,), width=esp, joint="curve")
    return img


def com_alfa(img, a):
    if a >= 1:
        return img
    r = img.copy()
    r.putalpha(r.getchannel("A").point(lambda v: int(v * a)))
    return r


def colar_centro(base, img, cx, cy, escala=1.0, alfa=1.0):
    if alfa <= 0:
        return
    if escala != 1.0:
        img = img.resize((max(1, round(img.width * escala)), max(1, round(img.height * escala))), Image.LANCZOS)
    img = com_alfa(img, alfa)
    base.alpha_composite(img, (round(cx - img.width / 2), round(cy - img.height / 2)))


def main():
    fundo_p, logo_p, fonte_p, ffmpeg, saida = sys.argv[1:6]
    if len(sys.argv) > 6:
        audio = ["-ss", sys.argv[7] if len(sys.argv) > 7 else "0", "-t", str(DUR), "-i", sys.argv[6]]
        filtro_a = ["-af", f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st={DUR - 0.6}:d=0.6"]
    else:
        audio = ["-f", "lavfi", "-t", str(DUR), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        filtro_a = []
    fundo = montar_fundo(fundo_p)
    logo = Image.open(logo_p).convert("RGBA")
    logo = logo.resize((900, round(logo.height * 900 / logo.width)), Image.LANCZOS)
    btn, btn_brilho = botao(fonte_p)
    sv = seta()

    proc = subprocess.Popen([
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        *audio, *filtro_a,
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", saida],
        stdin=subprocess.PIPE)

    for i in range(int(DUR * FPS)):
        t = i / FPS
        # fundo: zoom lento de 1,06 para 1,0 e entrada a partir do preto
        z = 1.0 - 0.055 * (t / DUR)
        fz = fundo.resize((round(fundo.width * z), round(fundo.height * z)), Image.BILINEAR)
        x0, y0 = (fz.width - W) // 2, (fz.height - H) // 2
        quadro = fz.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        luz = faixa(t, 0.0, 0.7)
        if luz < 1:
            quadro = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), quadro, luz)

        # logo: aparece com leve aproximação
        a = faixa(t, 0.25, 1.0)
        colar_centro(quadro, logo, W / 2, 600 - 30 * (1 - a), 0.94 + 0.06 * a, a)

        # botão: sobe e aparece; depois pulsa a cada 1 s com brilho dourado
        b = faixa(t, 0.9, 1.5)
        pulso = 0.0
        if t > 1.8:
            fase = (t - 1.8) % 1.0
            pulso = suave(fase / 0.35) if fase < 0.35 else 1 - suave((fase - 0.35) / 0.45) if fase < 0.8 else 0.0
        cy_btn = 925 + 40 * (1 - b)
        colar_centro(quadro, btn_brilho, W / 2, cy_btn, 1.0 + 0.04 * pulso, b * (0.25 + 0.75 * pulso))
        colar_centro(quadro, btn, W / 2, cy_btn, 1.0 + 0.04 * pulso, b)

        # setas para baixo indicando o botão "Saiba mais" do anúncio
        s = faixa(t, 1.4, 1.9)
        for k in range(2):
            onda = (t * 1.6 - k * 0.18) % 1.0
            colar_centro(quadro, sv, W / 2, 1075 + k * 42 + 14 * suave(onda), 1.0, s * (0.95 - 0.35 * k))

        proc.stdin.write(quadro.convert("RGB").tobytes())

    proc.stdin.close()
    sys.exit(proc.wait())


if __name__ == "__main__":
    main()
