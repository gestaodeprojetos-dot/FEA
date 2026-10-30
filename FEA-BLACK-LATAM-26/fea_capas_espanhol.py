"""Versões em espanhol das capas de curso da LP Black Friday LATAM (lp.joaopithon.com.br/black-friday-latam).
Apaga o texto em português com inpaint (OpenCV, sem IA generativa) e reescreve em espanhol com a fonte
mais próxima; no Botox usa o logo oficial em espanhol do Drive. Também tira o selo "Combo Vitalício",
que não vale para a oferta LATAM (12 meses).

Uso: python3 fea_capas_espanhol.py PASTA   (PASTA tem site/*.png 720x1040 e orig/logo-feb-latam.png)"""
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTES = "/tmp/claude-0/-home-user-FEA/ce2ef478-67a4-5284-b1d6-9d4c8f98649b/scratchpad/fontes"


def fonte(nome, peso, px):
    f = ImageFont.truetype(f"{FONTES}/{nome}.ttf", px)
    f.set_variation_by_name(peso)
    return f


def apagar(img, caixas, limiar, dilata=4, raio=7):
    """Inpaint dos pixels claros (texto) dentro de cada caixa."""
    a = np.asarray(img.convert("RGB")).copy()
    mask = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in caixas:
        sub = a[y0:y1, x0:x1].max(axis=2)
        mask[y0:y1, x0:x1][sub > limiar] = 255
    mask = cv2.dilate(mask, np.ones((dilata * 2 + 1, dilata * 2 + 1), np.uint8))
    out = cv2.inpaint(a, mask, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(out)


def escrever(img, texto, f, cor, centro_x=None, x=None, topo=0, largura=None):
    """Escreve em caixa alta com espaçamento ajustado para ocupar `largura` (se dada)."""
    d = ImageDraw.Draw(img)
    larg = [d.textlength(c, font=f) for c in texto]
    base = sum(larg)
    track = (largura - base) / (len(texto) - 1) if largura else 0
    total = base + track * (len(texto) - 1)
    cx = x if x is not None else centro_x - total / 2
    asc = f.getbbox("H")[1]                    # topo das maiúsculas
    for c, w in zip(texto, larg):
        d.text((cx, topo - asc), c, font=f, fill=tuple(cor))
        cx += w + track
    return img


def _largura_texto(texto, f, track=0):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    return sum(d.textlength(c, font=f) for c in texto) + track * (len(texto) - 1)


def febio(p):
    im = Image.open(f"{p}/site/capa-bioestimuladores.png").convert("RGB")
    im = apagar(im, [(140, 788, 580, 860), (285, 910, 435, 992)], 95)
    f = fonte("Sora", "SemiBold", 27)
    cor = (226, 222, 219)
    escrever(im, "FORMACIÓN ESPECIALISTA", f, cor, centro_x=360, topo=800)
    escrever(im, "EN BIOESTIMULADORES", f, cor, centro_x=360, topo=834)
    return im


def ctx(p):
    im = Image.open(f"{p}/site/capa-toxina-express.png").convert("RGB")
    return apagar(im, [(285, 910, 435, 992)], 95)


def colar_logo(im, logo_path, x, y, largura):
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo = logo.resize((largura, round(logo.height * largura / logo.width)), Image.LANCZOS)
    base = im.convert("RGBA")
    base.alpha_composite(logo, (x, y))
    return base.convert("RGB")


def full_face(p):
    """Logo oficial LATAM ("Inmersión Avanzada en Relleno Full Face") no lugar do logo em português."""
    im = Image.open(f"{p}/site/capa-full-face-5ml.png").convert("RGB")
    im = apagar(im, [(60, 745, 670, 905)], 85, dilata=4, raio=9)
    return colar_logo(im, f"{p}/orig/logo-ff-latam.png", 70, 748, 590)


def botox(p):
    im = Image.open(f"{p}/site/capa-botox.png").convert("RGB")
    im = apagar(im, [(100, 705, 668, 880)], 70, dilata=5, raio=9)
    return colar_logo(im, f"{p}/orig/logo-feb-latam.png", 112, 715, 498)


def logos(p):
    """Logos pequenos da seção de cursos (exibidos em 143x45 e 142x39): versões 3x a partir dos oficiais LATAM."""
    for nome, origem, (w, h) in [("logo-botox", "logo-feb-latam.png", (143, 45)),
                                 ("logo-full-face-5ml", "logo-ff-latam.png", (142, 39))]:
        lg = Image.open(f"{p}/orig/{origem}").convert("RGBA")
        lg = lg.crop(lg.getbbox())
        W, H = w * 3, h * 3
        esc = min(W / lg.width, H / lg.height)
        lg = lg.resize((round(lg.width * esc), round(lg.height * esc)), Image.LANCZOS)
        tela = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tela.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2))
        tela.save(f"{p}/{nome}-ES.png")
        print("ok", nome)


if __name__ == "__main__":
    p = sys.argv[1]
    for nome, fn in [("capa-bioestimuladores", febio), ("capa-toxina-express", ctx),
                     ("capa-full-face-5ml", full_face), ("capa-botox", botox)]:
        fn(p).save(f"{p}/{nome}-ES.png")
        print("ok", nome)
    logos(p)
