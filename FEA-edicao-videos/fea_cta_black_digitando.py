#!/usr/bin/env python3
"""CTA de 5 s da Black Friday Vitalícia, modelo "digitando" (1080x1920, 30 fps).

Fundo todo preto, logo aparecendo aos poucos (fade com desfoque saindo) e, embaixo,
"Toque em Saiba Mais" sendo digitado letra a letra com cursor piscando e clique de teclado
em cada letra. Trilha suave por baixo (fade-in curto, fade-out no fim).

Uso:
    python3 fea_cta_black_digitando.py LOGO.png FONTE.ttf FFMPEG MUSICA.wav CLIQUES.wav saida.mp4

CLIQUES.wav = gravação curta de teclado com toques separados por silêncio; cada toque vira
uma amostra e as letras usam as amostras em rodízio.
"""
import random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR, SR = 1080, 1920, 30, 5.0, 48000
DOURADO = (227, 172, 102)
TEXTO = "Toque em Saiba Mais"
LOGO_INI, LOGO_FIM = 0.2, 1.7
DIG_INI, DIG_PASSO = 1.9, 0.085
GANHO_MUSICA_DB, GANHO_CLIQUE_DB = -6.0, -9.0


def suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ler_audio(ffmpeg, caminho, canais):
    bruto = subprocess.run([ffmpeg, "-v", "error", "-i", caminho, "-ac", str(canais), "-ar", str(SR),
                            "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(bruto, np.float32).reshape(-1, canais)


def amostras_de_clique(sinal):
    x = sinal[:, 0]
    jan = SR // 200
    ener = np.array([np.sqrt((x[i:i + jan] ** 2).mean()) for i in range(0, len(x) - jan, jan)])
    db = 20 * np.log10(ener + 1e-9)
    amostras, ult = [], -1
    for i in range(1, len(db)):
        if db[i] - db[i - 1] > 10 and db[i] > -35 and (i - ult) * jan > SR * 0.06:
            ini = max(0, i * jan - SR // 400)
            a = x[ini:ini + int(SR * 0.07)].copy()
            a[-int(SR * 0.03):] *= np.linspace(1, 0, int(SR * 0.03))
            amostras.append(a / (np.abs(a).max() + 1e-9))
            ult = i
    return amostras


def tempos_digitacao():
    rnd = random.Random(7)
    t, tempos = DIG_INI, []
    for ch in TEXTO:
        tempos.append(t)
        t += DIG_PASSO * (1.6 if ch == " " else rnd.uniform(0.8, 1.2))
    return tempos


def montar_audio(ffmpeg, musica_p, cliques_p, destino):
    musica = ler_audio(ffmpeg, musica_p, 2)[: int(DUR * SR)]
    n = int(DUR * SR)
    trilha = np.zeros((n, 2), np.float32)
    trilha[: len(musica)] = musica
    env = np.ones(n, np.float32)
    env[: int(0.4 * SR)] = np.linspace(0, 1, int(0.4 * SR))
    env[-int(0.8 * SR):] = np.linspace(1, 0, int(0.8 * SR))
    trilha *= (env * 10 ** (GANHO_MUSICA_DB / 20))[:, None]

    cliques = amostras_de_clique(ler_audio(ffmpeg, cliques_p, 1))
    g = 10 ** (GANHO_CLIQUE_DB / 20)
    for k, (ch, t) in enumerate(zip(TEXTO, tempos_digitacao())):
        a = cliques[k % len(cliques)] * g * (0.6 if ch == " " else 1.0)
        i = int(t * SR)
        trilha[i:i + len(a)] += a[: n - i, None]

    pico = np.abs(trilha).max()
    if pico > 0.95:
        trilha *= 0.95 / pico
    with wave.open(destino, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((trilha * 32767).astype(np.int16).tobytes())


def main():
    logo_p, fonte_p, ffmpeg, musica_p, cliques_p, saida = sys.argv[1:7]
    audio_tmp = saida + ".wav"
    montar_audio(ffmpeg, musica_p, cliques_p, audio_tmp)

    logo = Image.open(logo_p).convert("RGBA")
    logo = logo.resize((860, round(logo.height * 860 / logo.width)), Image.LANCZOS)
    fonte = ImageFont.truetype(fonte_p, 60)
    larg_total = fonte.getlength(TEXTO)
    x_txt, y_txt = (W - larg_total) / 2, 1110
    asc, desc = fonte.getmetrics()
    tempos = tempos_digitacao()

    proc = subprocess.Popen([
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", audio_tmp,
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida],
        stdin=subprocess.PIPE)

    for i in range(int(DUR * FPS)):
        t = i / FPS
        quadro = Image.new("RGBA", (W, H), (0, 0, 0, 255))

        # logo: surge aos poucos, saindo do desfoque com leve aproximação
        a = suave((t - LOGO_INI) / (LOGO_FIM - LOGO_INI))
        if a > 0:
            esc = 0.96 + 0.04 * a
            lg = logo.resize((round(logo.width * esc), round(logo.height * esc)), Image.LANCZOS)
            raio = 14 * (1 - a)
            if raio > 0.3:
                lg = lg.filter(ImageFilter.GaussianBlur(raio))
            lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
            quadro.alpha_composite(lg, (round((W - lg.width) / 2), round(800 - lg.height / 2)))

        # texto digitado + cursor
        if t >= DIG_INI - 0.4:
            n = sum(1 for tt in tempos if tt <= t)
            d = ImageDraw.Draw(quadro)
            d.text((x_txt, y_txt), TEXTO[:n], font=fonte, fill=DOURADO + (255,))
            digitando = n < len(TEXTO)
            if digitando or int((t - tempos[-1]) / 0.45) % 2 == 0:
                xc = x_txt + fonte.getlength(TEXTO[:n]) + 6
                d.rectangle([xc, y_txt + 6, xc + 4, y_txt + asc + desc - 8], fill=DOURADO + (255,))

        proc.stdin.write(quadro.convert("RGB").tobytes())

    proc.stdin.close()
    sys.exit(proc.wait())


if __name__ == "__main__":
    main()
