#!/usr/bin/env python3
"""FEA: criativos de anúncio do Elite Experience (vídeo do Dr. falando para a câmera).

Reaproveita os cortes e a legenda do fea_editar_video.py (mesma transcrição, mesmo encaixe
nos respiros, mesmas correções de texto) e troca a camada visual pela identidade do evento:

  - fundo vinho #0F0507, granada #8E1F3A, rosé #E48EA0 (só números e palavras-chave),
    texto claro #FFE3EA; títulos em Gloock (substituta web da Canela Deck), texto em Urbanist
    (substituta web da Galano), como no briefing v4 de 11/11;
  - selo fixo no topo com data e cidade (briefing: "data e cidade visíveis acima da dobra");
  - degradê vinho embaixo para a legenda respirar e feixe de luz diagonal discreto;
  - cartela final com fundo vinho, feixes diagonais, data, local e botão de CTA;
  - trilha de fundo baixa, com "ducking" (abaixa sozinha quando o Dr. fala) e sobe na cartela.

Uso:
    python3 fea_criativo_elite.py projeto.json [--so-legenda]

projeto.json: mesmo formato do fea_editar_video.py, com os campos extras
    "musica": "musica.wav", "musica_db": -19, "cartela": {...}, "destaques": ["regex", ...]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fea  # noqa: E402

W, H = fea.W, fea.H
FUNDO, GRANADA, VINHO, ROSE, CLARO = "#0F0507", "#8E1F3A", "#9B2F4B", "#E48EA0", "#FFE3EA"


def ass_cor(hexa, alfa=0):
    r, g, b = hexa[1:3], hexa[3:5], hexa[5:7]
    return f"&H{alfa:02X}{b}{g}{r}".upper()


# ---------- estilos ASS da identidade Elite ----------
fea.TITULO_TAM = 104
fea.LEGENDA_TAM = 60
fea.LEGENDA_Y = 1470
fea.ENTRELINHA_TITULO = 0.92
fea.ENTRELINHA_LEGENDA = 0.86
fea.MAX_CHARS_LINHA = 22

TOPO_Y = 300   # selo de data/cidade: abaixo da faixa de interface do Reels (~220 px)


def ass_header():
    c, r, f = ass_cor(CLARO), ass_cor(ROSE), ass_cor(FUNDO, 0x30)
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Gloock,{fea.TITULO_TAM},{c},{c},{f},{ass_cor(FUNDO, 0x40)},0,0,0,0,100,100,0,0,1,3,0,5,80,80,0,1
Style: Legenda,Urbanist ExtraBold,{fea.LEGENDA_TAM},{c},{c},{ass_cor(FUNDO, 0x10)},{ass_cor(FUNDO, 0x80)},0,0,0,0,100,100,0,0,1,4,2,2,90,90,0,1
Style: Selo,Urbanist Bold,36,{r},{r},{f},{f},0,0,0,0,100,100,14,0,1,1.5,0,8,60,60,0,1
Style: SeloData,Urbanist SemiBold,42,{c},{c},{f},{f},0,0,0,0,100,100,2,0,1,1.5,0,8,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


fea.ass_header = ass_header
_gerar_ass = fea.gerar_ass
CAPTURA = {}


def colorir(texto, destaques):
    """Palavras-chave e números em rosé (briefing: rosé só em números, botões e palavras-chave)."""
    rose, claro = ass_cor(ROSE), ass_cor(CLARO)
    for d in destaques:
        texto = re.sub(d, lambda m: rf"{{\c{rose}}}{m.group(0)}{{\c{claro}}}", texto, flags=re.I)
    return texto


def gerar_ass(v, palavras, duracao, caminho):
    CAPTURA["manter"] = v["manter"]
    _gerar_ass(v, palavras, duracao, caminho)
    linhas = open(caminho, encoding="utf-8").read().splitlines(True)
    destaques = v.get("destaques", [])
    saida = []
    for ln in linhas:
        if ln.startswith("Dialogue:") and ",Legenda," in ln:
            cab, txt = ln.rsplit("}", 1)
            ln = cab + "}" + colorir(txt.rstrip("\n"), destaques) + "\n"
        if ln.startswith("Dialogue:") and ",Titulo," in ln:
            # entrada suave (fade + leve subida), sem o corte seco do padrão de procedimento
            cab, txt = ln.rsplit("}", 1)
            ln = cab.replace(r"\fad(0,250)", r"\fad(300,300)\blur0.6") + "}" + colorir(txt.rstrip("\n"), v.get("destaques_titulo", [])) + "\n"
        saida.append(ln)
    # abertura "jantar de gala": véu vinho sob o título, que se desfaz quando ele sai
    saida.append(f"Dialogue: 0,0:00:00.00,{fea.ts(fea.TITULO_DUR + 0.3)},Selo,,0,0,0,,{{\\an7\\pos(0,0)\\bord0\\shad0"
                 f"\\1c{ass_cor(FUNDO)}\\1a&H48&\\fad(0,500)\\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}\n")
    sel = v.get("selo", {})
    fim = fea.ts(duracao)
    saida.append(f"Dialogue: 2,0:00:00.00,{fim},Selo,,0,0,0,,{{\\an8\\pos({W // 2},{TOPO_Y})\\fad(400,0)}}"
                 f"{sel.get('marca', 'ELITE EXPERIENCE')}\n")
    saida.append(f"Dialogue: 2,0:00:00.00,{fim},SeloData,,0,0,0,,{{\\an8\\pos({W // 2},{TOPO_Y + 52})\\fad(400,0)}}"
                 f"{sel.get('data', '4 e 5 de dezembro  ·  São Paulo')}\n")
    # fio rosé entre a marca e a data
    saida.append(f"Dialogue: 2,0:00:00.00,{fim},Selo,,0,0,0,,{{\\an7\\pos({W // 2 - 60},{TOPO_Y + 44})\\bord0\\shad0"
                 f"\\1c{ass_cor(ROSE)}\\1a&H40&\\fad(400,0)\\p1}}m 0 0 l 120 0 120 2 0 2{{\\p0}}\n")
    open(caminho, "w", encoding="utf-8").write("".join(saida))


fea.gerar_ass = gerar_ass


# ---------- camadas gráficas (PIL) ----------
def fonte(pasta, nome, tam):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(pasta, nome), tam)


def feixes(img, alfa=1.0):
    """Feixes de luz diagonais (linguagem visual do briefing), desfocados."""
    from PIL import Image, ImageDraw, ImageFilter
    luz = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(luz)
    for x0, larg, a, cor in [(-200, 260, 70, VINHO), (180, 120, 45, ROSE), (520, 340, 55, GRANADA), (980, 160, 30, ROSE)]:
        rgb = tuple(int(cor[i:i + 2], 16) for i in (1, 3, 5))
        d.polygon([(x0, 0), (x0 + larg, 0), (x0 + larg + 900, H), (x0 + 900, H)], fill=rgb + (int(a * alfa),))
    luz = luz.filter(ImageFilter.GaussianBlur(70))
    return Image.alpha_composite(img, luz)


def camada_video(caminho):
    """Degradê vinho embaixo (leitura da legenda) e em cima (selo), mais um feixe diagonal sutil."""
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    base = tuple(int(FUNDO[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(H):
        a = 0
        if y > 1080:
            a = int(235 * ((y - 1080) / (H - 1080)) ** 0.85)
        elif y < 640:
            a = int(225 * ((640 - y) / 640) ** 0.9)
        if a:
            for x in range(W):
                px[x, y] = base + (a,)
    luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rgb = tuple(int(ROSE[i:i + 2], 16) for i in (1, 3, 5))
    ImageDraw.Draw(luz).polygon([(-300, 0), (-120, 0), (520, H), (340, H)], fill=rgb + (26,))
    luz = luz.filter(ImageFilter.GaussianBlur(60))
    Image.alpha_composite(img, luz).save(caminho)


def cartela(c, pasta_fontes, caminho):
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (W, H), FUNDO)
    img = feixes(img)
    d = ImageDraw.Draw(img)
    claro, rose, fundo = CLARO, ROSE, FUNDO

    def centro(y, txt, f, cor, esp=0):
        if esp:
            larg = sum(d.textlength(ch, font=f) for ch in txt) + esp * (len(txt) - 1)
            x = (W - larg) / 2
            for ch in txt:
                d.text((x, y), ch, font=f, fill=cor)
                x += d.textlength(ch, font=f) + esp
        else:
            d.text((W / 2, y), txt, font=f, fill=cor, anchor="ma")

    centro(560, "ELITE", fonte(pasta_fontes, "Gloock-Regular.ttf", 190), claro, esp=18)
    centro(790, "EXPERIENCE", fonte(pasta_fontes, "Urbanist-400.ttf", 52), rose, esp=22)
    centro(880, c.get("assinatura", "by Dr. João Pithon"), fonte(pasta_fontes, "Urbanist-400.ttf", 36), claro)
    d.line([(W / 2 - 70, 990), (W / 2 + 70, 990)], fill=rose, width=2)
    centro(1040, c.get("data", "4 e 5 de dezembro"), fonte(pasta_fontes, "Gloock-Regular.ttf", 84), rose)
    centro(1150, c.get("local", "São Paulo  ·  MC Hall"), fonte(pasta_fontes, "Urbanist-500.ttf", 46), claro)
    centro(1225, c.get("apoio", "Presencial e gratuito  ·  vagas por aplicação"),
           fonte(pasta_fontes, "Urbanist-400.ttf", 36), claro)
    fb = fonte(pasta_fontes, "Urbanist-700.ttf", 42)
    txt = c.get("cta", "Quero aplicar para a minha vaga")
    lb = d.textlength(txt, font=fb) + 120
    x0, y0 = (W - lb) / 2, 1380
    d.rounded_rectangle([x0, y0, x0 + lb, y0 + 112], radius=56, fill=rose)
    d.text((W / 2, y0 + 56), txt, font=fb, fill=fundo, anchor="mm")
    img.convert("RGB").save(caminho)


# ---------- render ----------
def renderizar(cfg, v, so_legenda=False):
    duracao = fea.renderizar(cfg, v, "legenda")
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    if so_legenda:
        return duracao
    manter = CAPTURA["manter"]
    base = os.path.dirname(v["saida"]) or "."
    over, card = f"{base}/_camada.png", f"{base}/_cartela.png"
    camada_video(over)
    cartela(v.get("cartela", {}), cfg["fontsdir"], card)
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
        f"[vc]eq=contrast=1.04:saturation=0.96,colorbalance=rs=0.03:bs=-0.02[vg];" \
        f"[vg][1:v]overlay=0:0[vo0];[vo0]ass='{esc}':fontsdir='{fd}',format=yuv420p[vt];" \
        f"[2:v]scale={W}:{H},zoompan=z='min(1.0+0.0009*on,1.05)':d={int(dc * 30)}:s={W}x{H}:fps=30," \
        f"format=yuv420p,setsar=1[vk];" \
        f"[vt][vk]xfade=transition=fade:duration={xf}:offset={duracao - xf:.3f}[vfin];" \
        f"[voz]asplit=2[voz1][vozk];" \
        f"[3:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={mus_db}dB," \
        f"volume='if(gte(t,{duracao - xf:.3f}),2.8,1)':eval=frame," \
        f"afade=t=in:d=1.2,afade=t=out:st={total - 1.6:.3f}:d=1.6[mus];" \
        f"[mus][vozk]sidechaincompress=threshold=0.03:ratio=4:attack=40:release=450[musd];" \
        f"[voz1][musd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[afin]"
    cmd = [cfg["ffmpeg"], "-y", "-v", "error", "-i", v["entrada"], "-i", over,
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
