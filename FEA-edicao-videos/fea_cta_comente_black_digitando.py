#!/usr/bin/env python3
"""FEA: CTA padrão "digitando" dos Reels de conteúdo (Black Friday Vitalícia, "Comente BLACK").

Mesmo modelo da cartela final dos criativos LATAM ("ADS 001 - BLACK LATAM.mp4", Drive
1fwY-U4c3ZWwoZodAmsOxVYouls7IiPdS, cartela de 31,68 s até o fim, 5,0 s), reaproveitando
FEA-edicao-latam/fea_endcard.py: fundo preto, logo oficial surgindo com impacto (varredura da
esquerda para a direita, brilho e leve zoom, junto com o whoosh) e, embaixo, o texto digitado
letra a letra com cursor e clique de teclado.

Áudio: FEA-edicao-latam/assets/sfx.wav é o áudio exato da cartela da referência (impacto de
0,06 a 0,95 s, 20 cliques de 1,54 a 3,48 s, silêncio até 5,0 s). O impacto entra como está e os
cliques reais são recortados um a um e recolocados, 1 por letra, no quadro em que a letra
aparece (o espaço não tem clique: sai junto com a letra seguinte).

Medidas da referência (25 fps, tempos a partir do início da cartela):
    logo surge 0,24 a 0,56 s (740 px de largura, centro em y 860), cursor aparece em 1,28 s,
    1ª letra 1,56 s, última 3,48 s, cursor pisca (0,4 s apagado / 0,4 s aceso) até o fim.

Uso:
    python3 fea_cta_comente_black_digitando.py SAIDA.mp4
        [--texto "Comente BLACK"] [--destaque BLACK] [--logo PNG] [--duracao 5.0]
        [--sfx WAV] [--fonte TTF] [--tamanho 78] [--png-final PREVIA.png]

--destaque = palavra do texto que sai no dourado do logo (o resto sai branco).
Logo padrão: FEA-cta-digitando/FEA-BFV-logo-Asset15.png = "02 - LOGOTIPO/PNG/Black Vitalícia/
BFV_Asset 15@4x.png" da pasta oficial Black Vitalícia (1s1hs4Pmy4BZCUj5q82IeUQFcDyzfipoU), sem
redesenho e sem IA.
"""
import argparse, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
LATAM = os.path.join(AQUI, "..", "FEA-edicao-latam", "assets")
W, H, FPS, SR = 1080, 1920, 30, 48000
DOURADO = (229, 173, 106)          # #E5AD6A, dourado do logo (mesmo da cartela Ads 022)
BRANCO = (255, 255, 255)
CURSOR = (240, 232, 220)           # cursor claro da referência
LOGO_L, LOGO_CY = 740, 860         # medidos na referência
TXT_TOPO = 1150
CURSOR_INI = 1.28
PRIMEIRA = 47                      # quadro da 1ª letra (1,567 s; referência 1,56 s)
# intervalo em quadros entre as teclas, ritmo de digitação humana (pausa maior no espaço)
PASSOS = [4, 4, 5, 4, 4, 5, 9, 5, 4, 5, 4]
# cliques da referência (s), usados para achar o início exato de cada clique no sfx.wav
CLIQUES_REF = [1.54, 1.665, 1.71, 1.8, 1.845, 2.005, 2.05, 2.25, 2.335, 2.425, 2.58, 2.64,
               2.745, 2.84, 2.935, 3.045, 3.135, 3.185, 3.28, 3.38]


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def ler_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()), w.getframerate()


def recortar_cliques(sfx):
    """Início exato (1 ms) de cada clique da referência e a amostra até o clique seguinte."""
    mono = np.abs(sfx).mean(1)
    j = SR // 1000
    env = np.array([mono[i:i + j].max() for i in range(0, len(mono) - j, j)])
    inicios = []
    for t in CLIQUES_REF:
        a, b = int((t - 0.03) * 1000), int((t + 0.04) * 1000)
        pico = a + int(np.argmax(env[a:b]))
        k = pico
        while k > a and env[k - 1] > env[pico] * 0.1:
            k -= 1
        inicios.append(max(0, k - 2) * j)
    amostras = []
    for n, i in enumerate(inicios):
        fim = inicios[n + 1] - 2 * j if n + 1 < len(inicios) else i + int(0.12 * SR)
        fim = min(fim, i + int(0.12 * SR))
        a = sfx[i:fim].copy()
        f = min(len(a), int(0.012 * SR))
        a[-f:] *= np.linspace(1, 0, f)[:, None]
        amostras.append(a)
    return amostras


def montar_audio(sfx_p, tempos, dur, destino):
    sfx, sr = ler_wav(sfx_p)
    assert sr == SR and sfx.shape[1] == 2, "sfx.wav precisa ser 48 kHz estéreo"
    n = int(round(dur * SR))
    trilha = np.zeros((n, 2), np.float32)
    corte = int(1.2 * SR)                              # impacto/whoosh (acaba em ~0,95 s)
    trilha[:min(corte, n)] = sfx[:min(corte, n)]
    cliques = recortar_cliques(sfx)
    for k, t in enumerate(tempos):
        a = cliques[k % len(cliques)]
        i = int(round(t * SR))
        m = min(len(a), n - i)
        trilha[i:i + m] += a[:m]
    pico = np.abs(trilha).max()
    if pico > 0.98:
        trilha *= 0.98 / pico
    with wave.open(destino, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((trilha * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("saida")
    ap.add_argument("--texto", default="Comente BLACK")
    ap.add_argument("--destaque", default="BLACK")
    ap.add_argument("--logo", default=os.path.join(AQUI, "FEA-cta-digitando", "FEA-BFV-logo-Asset15.png"))
    ap.add_argument("--duracao", type=float, default=5.0)
    ap.add_argument("--sfx", default=os.path.join(LATAM, "sfx.wav"))
    ap.add_argument("--fonte", default=os.path.join(LATAM, "Montserrat-800.ttf"))
    ap.add_argument("--tamanho", type=int, default=78)
    ap.add_argument("--png-final", help="salva o último quadro (prévia)")
    a = ap.parse_args()

    texto = a.texto
    # teclas = caracteres visíveis; o espaço sai junto com a letra seguinte
    teclas = [i for i, c in enumerate(texto) if c != " "]
    passos = PASSOS if len(teclas) == len(PASSOS) + 1 else \
        [9 if texto[teclas[k] - 1] == " " else 4 for k in range(1, len(teclas))]
    quadros = [PRIMEIRA]
    for p in passos:
        quadros.append(quadros[-1] + p)
    tempos = [q / FPS for q in quadros]
    nq = int(round(a.duracao * FPS))
    if quadros[-1] + FPS > nq:
        raise SystemExit(f"duração curta: a última letra cai em {tempos[-1]:.2f} s")
    # quantos caracteres do texto estão na tela no quadro q
    visiveis = lambda q: 0 if q < quadros[0] else teclas[sum(1 for x in quadros if x <= q) - 1] + 1

    lg0 = Image.open(a.logo).convert("RGBA")
    lg = lg0.resize((LOGO_L, round(lg0.height * LOGO_L / lg0.width)), Image.LANCZOS)
    brilho = lg.filter(ImageFilter.GaussianBlur(26))
    fnt = ImageFont.truetype(a.fonte, a.tamanho)
    d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    larg = d0.textlength(texto, font=fnt)
    x0 = (W - larg) / 2
    asc, desc = fnt.getmetrics()
    ini_dest = texto.find(a.destaque) if a.destaque else -1

    def quadro(q):
        t = q / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        # logo: varredura com borda suave + brilho e leve zoom, junto com o impacto do sfx
        p = ease((t - 0.2) / 0.75)
        if p > 0:
            s = 1.05 - 0.05 * ease((t - 0.2) / 1.1)
            L = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS)
            G = brilho.resize(L.size, Image.LANCZOS)
            borda = p * (L.width + 160) - 160
            m = np.clip((borda - np.arange(L.width)[None, :]) / 160 + 1, 0, 1)
            L.putalpha(Image.fromarray((np.asarray(L.getchannel("A"), float) * m).astype(np.uint8)))
            gi = max(0.0, 1 - abs(t - 0.75) / 0.6) * 0.55
            G.putalpha(Image.fromarray((np.asarray(G.getchannel("A"), float) * m * gi).astype(np.uint8)))
            pos = ((W - L.width) // 2, LOGO_CY - L.height // 2)
            im.alpha_composite(G, pos)
            im.alpha_composite(L, pos)
        d = ImageDraw.Draw(im)
        n = visiveis(q)
        x = x0
        for i, c in enumerate(texto[:n]):
            cor = DOURADO if 0 <= ini_dest <= i < ini_dest + len(a.destaque) else BRANCO
            d.text((x, TXT_TOPO), c, font=fnt, fill=cor + (255,))
            x = x0 + d.textlength(texto[:i + 1], font=fnt)
        if t >= CURSOR_INI:
            fim = quadros[-1]
            if q <= fim or ((q - fim - 1) // 12) % 2 == 1:   # pisca 0,4 s apagado / 0,4 s aceso
                xc = x0 + d.textlength(texto[:n], font=fnt) + 8
                d.rectangle([xc, TXT_TOPO + 8, xc + 5, TXT_TOPO + asc + desc - 12], fill=CURSOR + (255,))
        return im.convert("RGB")

    wav = a.saida + ".wav"
    montar_audio(a.sfx, tempos, nq / FPS, wav)
    proc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-i", wav,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", f"{nq / FPS:.3f}", "-movflags", "+faststart", a.saida], stdin=subprocess.PIPE)
    for q in range(nq):
        im = quadro(q)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg falhou")
    os.remove(wav)
    if a.png_final:
        im.save(a.png_final)
    for k, (q, t) in enumerate(zip(quadros, tempos)):
        print(f"tecla {k + 1:2d} '{texto[teclas[k]]}' quadro {q:3d} = {t:.3f} s")


if __name__ == "__main__":
    main()
