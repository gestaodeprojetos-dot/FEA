"""Imagem de apresentação com QR code para a live do MTB 11/26 (pesquisa da live).

Mesmo layout das imagens de QR do IFF10 (1806x886: QR grande num card branco à esquerda,
logo e copy à direita), com a identidade do MTB (fundo escuro, verde do logo).
Sem IA generativa: fundo, QR (segno) e texto desenhados em código.
Uso: python3 fea_qr_pesquisa_live.py LOGO_PNG FONTE_SORA SAIDA_PNG"""
import sys, segno, io
from PIL import Image, ImageDraw, ImageFont

URL = "https://docs.google.com/forms/d/e/1FAIpQLSd9tFWIDm7ILiYrXoLuSIgzWopPYOF-AXhBiD-z9p0Htmf_fw/viewform"
W, H = 1806, 886
KICKER = "APONTE A CÂMERA DO CELULAR"
TITULO = ["RESPONDA À", "PESQUISA DA", "MASTERCLASS"]
VERDE_CLARO, BRANCO = (93, 201, 160), (255, 255, 255)


def fonte(caminho, peso, px):
    f = ImageFont.truetype(caminho, px); f.set_variation_by_name(peso); return f


def main(logo, sora, saida):
    # fundo: degradê diagonal do verde escuro do MTB para quase preto
    fundo = Image.new("RGB", (W, H))
    px = fundo.load()
    a, b = (8, 58, 44), (12, 14, 14)
    for y in range(H):
        for x in range(W):
            t = min(1, max(0, (x / W) * 0.75 + (y / H) * 0.25))
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    d = ImageDraw.Draw(fundo)
    # card branco do QR
    d.rounded_rectangle((114, 99, 820, 805), radius=36, fill=BRANCO)
    qr = segno.make(URL, error="m")
    buf = io.BytesIO(); qr.save(buf, kind="png", scale=1, border=0); buf.seek(0)
    q = Image.open(buf).convert("RGB")
    lado = 608
    q = q.resize((lado, lado), Image.NEAREST)
    fundo.paste(q, (114 + (706 - lado) // 2, 99 + (706 - lado) // 2))
    # logo
    lg = Image.open(logo).convert("RGBA")
    lg = lg.resize((560, int(lg.height * 560 / lg.width)), Image.LANCZOS)
    fundo.paste(lg, (950, 120), lg)
    # copy
    fk = fonte(sora, "SemiBold", 34)
    d.text((950, 372), KICKER, font=fk, fill=VERDE_CLARO)
    ft = fonte(sora, "ExtraBold", 92)
    y = 440
    for linha in TITULO:
        d.text((946, y), linha, font=ft, fill=BRANCO); y += 112
    assert max(d.textlength(l, font=ft) for l in TITULO) + 946 < W - 60, "título passou da margem"
    fundo.save(saida)


if __name__ == "__main__":
    main(*sys.argv[1:4])
