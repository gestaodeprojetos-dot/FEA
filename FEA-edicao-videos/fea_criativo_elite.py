#!/usr/bin/env python3
"""FEA: criativos de anúncio do Elite Experience (vídeo do Dr. falando para a câmera).

Reaproveita os cortes e a legenda do fea_editar_video.py (mesma transcrição, mesmo encaixe
nos respiros, mesmas correções de texto) e aplica o Manual de Identidade Visual do evento
(PDF de 18 páginas enviado pela Keila em 12/11/2026):

  - paleta: base escura #0F0507, granada #8E1F3A, bordô #9B2F4B, rosé #E48AA0, rosé claro #FFE3EA;
  - logotipo oficial em PNG (FEA-elite-marca/, extraído do manual), nunca redigitado nem
    recomposto, sem sombra, brilho ou contorno, com respiro de 2x e acima do tamanho mínimo
    (horizontal 140 px, vertical 90 px);
  - títulos em Canela Deck (aqui Gloock, a substituta web) com degradê rosé metálico,
    entrelinha 100 a 105% e espaçamento -1%;
  - textos em Galano Grotesque (aqui Urbanist): rótulo Medium em caixa alta espaçada,
    apoio Light, chamada SemiBold em caixa alta sobre pílula rosé #E48AA0 com texto #0F0507;
  - clima do key visual: fundo escuro aveludado, luz rosé vinda de um lado, monograma em vidro;
  - trilha de fundo baixa, com "ducking" (abaixa sozinha quando o Dr. fala), sobe na cartela.

Uso:
    python3 fea_criativo_elite.py projeto.json [--so-legenda]

projeto.json: mesmo formato do fea_editar_video.py, com os campos extras
    "musica", "musica_db", "cartela": {...}, "selo": {...}, "destaques": [regex, ...],
    "destaques_titulo": [palavras do título em rosé claro/brilho]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fea  # noqa: E402

W, H = fea.W, fea.H
FUNDO, GRANADA, BORDO, ROSE, CLARO = "#0F0507", "#8E1F3A", "#9B2F4B", "#E48AA0", "#FFE3EA"
MARCA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FEA-elite-marca")


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def ass_cor(hexa, alfa=0):
    r, g, b = hexa[1:3], hexa[3:5], hexa[5:7]
    return f"&H{alfa:02X}{b}{g}{r}".upper()


# ---------- legenda (ASS) ----------
fea.LEGENDA_TAM = 60
fea.LEGENDA_Y = 1470
fea.ENTRELINHA_LEGENDA = 0.86
fea.MAX_CHARS_LINHA = 22


def ass_header():
    c = ass_cor(CLARO)
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Gloock,100,{c},{c},{ass_cor(FUNDO)},{ass_cor(FUNDO)},0,0,0,0,100,100,0,0,1,0,0,5,80,80,0,1
Style: Legenda,Urbanist SemiBold,{fea.LEGENDA_TAM},{c},{c},{ass_cor(FUNDO, 0x18)},{ass_cor(FUNDO, 0x80)},0,0,0,0,100,100,0,0,1,3.5,1.5,2,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


fea.ass_header = ass_header
_gerar_ass = fea.gerar_ass
CAPTURA = {}


def colorir(texto, destaques):
    """Números e palavras-chave em rosé (manual: os rosés trazem luz e destaque)."""
    rose, claro = ass_cor(ROSE), ass_cor(CLARO)
    for d in destaques:
        texto = re.sub(d, lambda m: rf"{{\c{rose}}}{m.group(0)}{{\c{claro}}}", texto, flags=re.I)
    return texto


def gerar_ass(v, palavras, duracao, caminho):
    """Legenda do padrão FEA; o título sai do ASS (vira imagem com degradê metálico)."""
    CAPTURA["manter"] = v["manter"]
    _gerar_ass(v, palavras, duracao, caminho)
    saida = []
    for ln in open(caminho, encoding="utf-8").read().splitlines(True):
        if ln.startswith("Dialogue:") and ",Titulo," in ln:
            continue
        if ln.startswith("Dialogue:") and ",Legenda," in ln:
            cab, txt = ln.rsplit("}", 1)
            ln = cab + "}" + colorir(txt.rstrip("\n"), v.get("destaques", [])) + "\n"
        saida.append(ln)
    open(caminho, "w", encoding="utf-8").write("".join(saida))


fea.gerar_ass = gerar_ass


# ---------- desenho (PIL) ----------
def fonte(pasta, nome, tam):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(pasta, nome), tam)


def metalico(larg, alt):
    """Degradê rosé metálico (como o ELITE do logotipo): rosé, brilho rosé claro, rosé, bordô."""
    import numpy as np
    from PIL import Image
    paradas = [(0.0, rgb("#D9849A")), (0.38, rgb("#F7D3DC")), (0.5, rgb(CLARO)),
               (0.72, rgb(ROSE)), (1.0, rgb("#B8607A"))]
    x = np.linspace(0, 1, larg)
    cols = np.zeros((larg, 3))
    for (a, ca), (b, cb) in zip(paradas, paradas[1:]):
        m = (x >= a) & (x <= b)
        t = ((x[m] - a) / (b - a))[:, None]
        cols[m] = np.array(ca) * (1 - t) + np.array(cb) * t
    # leve variação vertical (reflexo de metal)
    y = np.linspace(-1, 1, alt)[:, None, None]
    img = cols[None, :, :] * (1 - 0.10 * y)
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB")


def texto_espacado(d, xy, txt, f, cor, esp, anchor="mm"):
    """Texto com espaçamento entre letras (rótulos em caixa alta do manual)."""
    larg = sum(d.textlength(ch, font=f) for ch in txt) + esp * (len(txt) - 1)
    x = xy[0] - larg / 2 if anchor[0] == "m" else xy[0]
    for ch in txt:
        d.text((x, xy[1]), ch, font=f, fill=cor, anchor="l" + anchor[1])
        x += d.textlength(ch, font=f) + esp
    return larg


def bloco_titulo(linhas, f, entrelinha=1.03, rastreio=-0.01):
    """Título em Gloock com degradê metálico, linhas centradas, espaçamento -1%."""
    from PIL import Image, ImageDraw
    tam = f.size
    esp = tam * rastreio
    med = ImageDraw.Draw(Image.new("L", (1, 1)))
    largs = [sum(med.textlength(ch, font=f) for ch in l) + esp * (len(l) - 1) for l in linhas]
    lw, lh = int(max(largs)) + 40, int(tam * entrelinha * len(linhas) + tam * 0.4)
    mask = Image.new("L", (lw, lh), 0)
    d = ImageDraw.Draw(mask)
    for i, (l, lg) in enumerate(zip(linhas, largs)):
        x = (lw - lg) / 2
        y = tam * 0.15 + i * tam * entrelinha
        for ch in l:
            d.text((x, y), ch, font=f, fill=255, anchor="la")
            x += d.textlength(ch, font=f) + esp
    tex = metalico(lw, lh).convert("RGBA")
    tex.putalpha(mask)
    return tex


def luz_lateral(img, lado="esq", forca=1.0, cy=0.42):
    """Luz rosé vinda de um lado, sobre fundo escuro aveludado (key visual)."""
    import numpy as np
    from PIL import Image
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cx = -0.15 * w if lado == "esq" else 1.15 * w
    dist = np.sqrt(((xx - cx) / (0.95 * w)) ** 2 + ((yy - cy * h) / (0.55 * h)) ** 2)
    a = np.clip(1 - dist, 0, 1) ** 1.6 * forca
    cor = np.zeros((h, w, 4))
    cor[..., :3] = np.array(rgb(BORDO)) * (1 - a[..., None] * 0.5) + np.array(rgb(ROSE)) * a[..., None] * 0.5
    cor[..., 3] = np.clip(a * 235, 0, 255)
    return Image.alpha_composite(img, Image.fromarray(cor.astype("uint8"), "RGBA"))


def veludo(img, seed=7):
    """Granulado fino (textura aveludada do manual)."""
    import numpy as np
    from PIL import Image
    a = np.array(img).astype(float)
    ruido = np.random.default_rng(seed).normal(0, 3.2, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + ruido, 0, 255)
    return Image.fromarray(a.astype("uint8"), img.mode)


def monograma_vidro(alt, alfa=0.16):
    """Monograma "em vidro": preenchimento translúcido e fio claro, usado como grafismo grande."""
    from PIL import Image, ImageFilter, ImageChops
    simb = Image.open(os.path.join(MARCA, "EE_Simbolo_Principal.png"))
    simb = simb.resize((int(simb.width * alt / simb.height), alt), Image.LANCZOS)
    m = simb.getchannel("A")
    borda = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
    vidro = Image.new("RGBA", simb.size, rgb(CLARO) + (0,))
    vidro.putalpha(m.point(lambda v: int(v * alfa)))
    fio = Image.new("RGBA", simb.size, rgb(CLARO) + (0,))
    fio.putalpha(borda.point(lambda v: int(v * 0.45)))
    return Image.alpha_composite(vidro, fio)


def logo(nome, larg):
    from PIL import Image
    im = Image.open(os.path.join(MARCA, nome))
    return im.resize((larg, int(im.height * larg / im.width)), Image.LANCZOS)


def camada_video(caminho, sel, pasta_fontes):
    """Camada fixa: degradês escuros (contraste), logotipo horizontal e data/cidade no topo."""
    import numpy as np
    from PIL import Image, ImageDraw
    a = np.zeros(H, float)
    y = np.arange(H)
    a[y > 1080] = 235 * ((y[y > 1080] - 1080) / (H - 1080)) ** 0.85
    a[y < 640] = 230 * ((640 - y[y < 640]) / 640) ** 0.9
    arr = np.zeros((H, W, 4), "uint8")
    arr[..., :3] = rgb(FUNDO)
    arr[..., 3] = a[:, None].astype("uint8")
    img = Image.fromarray(arr, "RGBA")
    lg = logo("EE_Horizontal_Principal.png", sel.get("logo_larg", 380))   # mínimo do manual: 140 px
    topo = sel.get("topo", 235)                                           # abaixo da interface do Reels
    img.alpha_composite(lg, ((W - lg.width) // 2, topo))
    d = ImageDraw.Draw(img)
    x_alt = lg.height * 0.16                     # altura de EXPERIENCE no logotipo (x do respiro)
    yy = topo + lg.height + int(2 * x_alt) + 6   # respiro de 2x
    texto_espacado(d, (W / 2, yy + 16), sel.get("data", "4 E 5 DE DEZEMBRO  ·  SÃO PAULO"),
                   fonte(pasta_fontes, "Urbanist-500.ttf", 30), rgb(CLARO) + (255,), 30 * 0.3)
    img.save(caminho)


def abertura(caminho, v, pasta_fontes):
    """Abertura (3 s): véu escuro, luz rosé lateral, monograma em vidro e título metálico."""
    from PIL import Image
    img = Image.new("RGBA", (W, H), rgb(FUNDO) + (175,))
    img = luz_lateral(img, "esq", 0.55, cy=0.5)
    vd = monograma_vidro(1100, 0.06)
    img.alpha_composite(vd, (W - int(vd.width * 0.45), int(H * 0.62 - vd.height / 2)))
    linhas = v.get("titulo_linhas") or fea.quebrar_titulo(v["titulo"]).split(r"\N")
    tam = v.get("titulo_tam", 124)
    while True:   # cabe em ~84% da largura, sem quebrar o título
        t = bloco_titulo(linhas, fonte(pasta_fontes, "Gloock-Regular.ttf", tam))
        if t.width <= W * 0.84 or tam <= 70:
            break
        tam -= 4
    img.alpha_composite(t, ((W - t.width) // 2, int(H * 0.5 - t.height / 2)))
    img.save(caminho)


def cartela(c, pasta_fontes, caminho):
    """Cartela final no clima do key visual, com hierarquia do manual."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (W, H), rgb(FUNDO) + (255,))
    img = luz_lateral(img, "esq", 0.85, cy=0.30)
    vd = monograma_vidro(1700, 0.05)
    img.alpha_composite(vd, (-int(vd.width * 0.62), 40))
    img = veludo(img)
    d = ImageDraw.Draw(img)
    lg = logo("EE_Vertical_Principal.png", c.get("logo_larg", 560))
    y = 330
    img.alpha_composite(lg, ((W - lg.width) // 2, y))
    y += lg.height + 120                                        # respiro bem acima de 2x
    texto_espacado(d, (W / 2, y), c.get("rotulo", "COM DR. JOÃO PITHON"),
                   fonte(pasta_fontes, "Urbanist-500.ttf", 30), rgb(ROSE), 30 * 0.35)
    y += 70
    t = bloco_titulo([c.get("data", "4 e 5 de dezembro")], fonte(pasta_fontes, "Gloock-Regular.ttf", 104))
    img.alpha_composite(t, ((W - t.width) // 2, y))
    y += t.height + 10
    d.text((W / 2, y), c.get("local", "São Paulo  ·  MC Hall"), font=fonte(pasta_fontes, "Urbanist-300.ttf", 50),
           fill=rgb(CLARO), anchor="mt")
    y += 80
    texto_espacado(d, (W / 2, y + 16), c.get("apoio", "PRESENCIAL E GRATUITO  ·  VAGAS POR APLICAÇÃO"),
                   fonte(pasta_fontes, "Urbanist-500.ttf", 27), rgb(CLARO), 27 * 0.28)
    y += 130
    fb = fonte(pasta_fontes, "Urbanist-600.ttf", 34)
    txt = c.get("cta", "QUERO APLICAR PARA A MINHA VAGA")
    esp = 34 * 0.16
    lt = sum(d.textlength(ch, font=fb) for ch in txt) + esp * (len(txt) - 1)
    lb = lt + 130
    x0 = (W - lb) / 2
    d.rounded_rectangle([x0, y, x0 + lb, y + 108], radius=54, fill=rgb(ROSE))
    texto_espacado(d, (W / 2, y + 54), txt, fb, rgb(FUNDO), esp)
    img.convert("RGB").save(caminho)


# ---------- render ----------
def renderizar(cfg, v, so_legenda=False):
    duracao = fea.renderizar(cfg, v, "legenda")
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    if so_legenda:
        return duracao
    manter = CAPTURA["manter"]
    base = os.path.dirname(v["saida"]) or "."
    over, ab, card = f"{base}/_camada.png", f"{base}/_abertura.png", f"{base}/_cartela.png"
    camada_video(over, v.get("selo", {}), cfg["fontsdir"])
    abertura(ab, v, cfg["fontsdir"])
    cartela(v.get("cartela", {}), cfg["fontsdir"], card)
    td = fea.TITULO_DUR
    dc = v.get("cartela_dur", 4.5)
    xf = 0.6
    total = duracao + dc - xf
    mus_db = v.get("musica_db", -19)
    partes, vrot, arot = [], [], []
    for i, (a, b) in enumerate(manter):
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1[v{i}]")
        vrot.append(f"[v{i}]")
        arot.append(f"[a{i}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    fd = cfg["fontsdir"].replace(":", "\\:")
    filtro = ";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0,fps=30[vc];" \
        + "".join(arot) + f"concat=n={len(arot)}:v=0:a=1,apad=whole_dur={total:.3f}[voz];" \
        f"[vc]eq=contrast=1.04:saturation=0.95,colorbalance=rs=0.03:bs=-0.02[vg];" \
        f"[2:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={td - 0.2:.2f}:d=0.5:alpha=1[ab];" \
        f"[vg][ab]overlay=0:0:eof_action=pass[vo0];" \
        f"[vo0][1:v]overlay=0:0[vo1];" \
        f"[vo1]ass='{esc}':fontsdir='{fd}',format=yuv420p[vt];" \
        f"[3:v]scale={W}:{H},zoompan=z='min(1.0+0.0007*on,1.04)':d={int(dc * 30)}:s={W}x{H}:fps=30," \
        f"format=yuv420p,setsar=1[vk];" \
        f"[vt][vk]xfade=transition=fade:duration={xf}:offset={duracao - xf:.3f}[vfin];" \
        f"[voz]asplit=2[voz1][vozk];" \
        f"[4:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={mus_db}dB," \
        f"volume='if(gte(t,{duracao - xf:.3f}),2.8,1)':eval=frame," \
        f"afade=t=in:d=1.2,afade=t=out:st={total - 1.6:.3f}:d=1.6[mus];" \
        f"[mus][vozk]sidechaincompress=threshold=0.03:ratio=4:attack=40:release=450[musd];" \
        f"[voz1][musd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[afin]"
    cmd = [cfg["ffmpeg"], "-y", "-v", "error", "-i", v["entrada"], "-i", over,
           "-loop", "1", "-framerate", "30", "-t", f"{td + 0.4}", "-i", ab,
           "-loop", "1", "-t", f"{dc}", "-i", card, "-i", v["musica"],
           "-filter_complex", filtro, "-map", "[vfin]", "-map", "[afin]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-t", f"{total:.3f}", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return total


def main():
    args = sys.argv[1:]
    so = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    filtro = args[1:]
    for v in cfg["videos"]:
        if filtro and not any(x in v["saida"] for x in filtro):
            continue
        d = renderizar(cfg, v, so)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
