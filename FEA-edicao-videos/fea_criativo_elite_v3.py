#!/usr/bin/env python3
"""FEA: criativos do Elite Experience, modelo Luca completo (Keila, 18/11/2026).

Em cima do v2 (tarja de público, legenda curta, CTA final), acrescenta o que o vídeo de
referência do Luca tem e o v2 não tinha:
  - CARDS: fotos da página do evento entrando na tela (sobe e aparece, com "whoosh") no
    momento em que o Dr. fala do assunto, com rótulo em pílula;
  - TELA DIVIDIDA: metade de cima com painel da marca (título + lista que vai aparecendo item
    a item, com miniatura), metade de baixo com o Dr.; legenda some nesse trecho;
  - TRILHA de impacto (trailer) + efeitos sonoros (boom na tela dividida, whoosh nos cards);
  - Galano Grotesque oficial (pasta de identidade do evento) em legenda, tarja, cards e CTA.

Elementos por vídeo no projeto.json ("elementos"), em segundos do vídeo final:
  {"tipo": "card", "img": "...", "ini": 5.0, "fim": 8.0, "rotulo": "TEXTO", "y": 640, "larg": 780}
  {"tipo": "split", "ini": 6.0, "fim": 12.5, "titulo": "...", "crop_y": 300,
   "itens": [{"txt": "...", "img": "..."}, ...]}

Uso:  python3 fea_criativo_elite_v3.py projeto.json [filtro ...]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_criativo_elite_v2 as v2   # noqa: E402
ce, fea = v2.ce, v2.fea
W, H, rgb, ass_cor = ce.W, ce.H, ce.rgb, ce.ass_cor
FUNDO, GRANADA, BORDO, ROSE, CLARO = ce.FUNDO, ce.GRANADA, ce.BORDO, ce.ROSE, ce.CLARO
GAL = {"m": "GalanoGrotesque-Medium.otf", "sb": "GalanoGrotesque-SemiBold.otf", "b": "GalanoGrotesque-Bold.otf",
       "xb": "GalanoGrotesque-ExtraBold.otf", "h": "GalanoGrotesque-Heavy.otf", "r": "GalanoGrotesque-Regular.otf"}
PASTA_FONTES = None
_fonte_orig = ce.fonte
_MAPA = {"Urbanist-300.ttf": "GalanoGrotesque-Light.otf", "Urbanist-400.ttf": "GalanoGrotesque-Regular.otf",
         "Urbanist-500.ttf": "GalanoGrotesque-Medium.otf", "Urbanist-600.ttf": "GalanoGrotesque-SemiBold.otf",
         "Urbanist-700.ttf": "GalanoGrotesque-Bold.otf", "Urbanist-800.ttf": "GalanoGrotesque-ExtraBold.otf"}


def _fonte_galano(pasta, nome, tam):
    """Galano Grotesque oficial no lugar da Urbanist (substituta web) em tarja, CTA e itens."""
    alt = _MAPA.get(nome)
    if alt and os.path.exists(os.path.join(pasta, alt)):
        nome = alt
    return _fonte_orig(pasta, nome, tam)


ce.fonte = _fonte_galano
v2.fonte = _fonte_galano


def gal(peso, tam):
    return ce.fonte(PASTA_FONTES, GAL[peso], tam)


# ---------- legenda em Galano ----------
def ass_header():
    c = ass_cor("#FFFFFF")
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,Galano Grotesque SemiBold,64,{c},{c},{ass_cor(FUNDO, 0x40)},{ass_cor(FUNDO, 0x50)},0,0,0,0,100,100,0,0,1,2.4,3,2,60,60,0,1
Style: Destaque,Galano Grotesque Heavy,150,{c},{c},{ass_cor(FUNDO, 0x30)},{ass_cor(FUNDO, 0x40)},0,0,0,0,96,100,-2,0,1,2.6,6,2,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


fea.ass_header = ass_header
JANELAS = []   # (ini, fim, tipo) dos elementos do vídeo em render: legenda/destaque respeitam


def _t(s):
    h, m, x = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


_gerar_v2 = v2.gerar_ass


def gerar_ass(v, palavras, duracao, caminho):
    _gerar_v2(v, palavras, duracao, caminho)
    saida = []
    for ln in open(caminho, encoding="utf-8").read().splitlines(True):
        if ln.startswith("Dialogue:"):
            p = ln.split(",")
            a, b = _t(p[1]), _t(p[2])
            meio = (a + b) / 2
            em_split = any(i <= meio < f for i, f, t in JANELAS if t == "split")
            em_card = any(i - 0.2 <= meio < f + 0.2 for i, f, t in JANELAS if t == "card")
            if em_split:
                continue                      # tela dividida: sem legenda, como no modelo
            if ",Destaque," in ln and em_card:
                continue                      # não disputa a tela com o card
        saida.append(ln)
    open(caminho, "w", encoding="utf-8").write("".join(saida))


fea.gerar_ass = gerar_ass


# ---------- desenho ----------
def cobrir(im, w, h, foco_y=0.4):
    from PIL import Image
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * foco_y)
    return im.crop((x, y, x + w, y + h))


def arredondar(im, raio):
    from PIL import Image, ImageDraw
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=raio, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m)
    return im


def sombra(img, caixa, raio, alfa=150, blur=30, dy=16):
    from PIL import Image, ImageDraw, ImageFilter
    s = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([caixa[0], caixa[1] + dy, caixa[2], caixa[3] + dy], radius=raio,
                                        fill=(15, 5, 7, alfa))
    return Image.alpha_composite(img, s.filter(ImageFilter.GaussianBlur(blur)))


def pilula(d, cx, cy, txt, f, fundo, cor, esp=0.12, pad=34, alt=None):
    tam = f.size
    lt = sum(d.textlength(ch, font=f) for ch in txt) + tam * esp * (len(txt) - 1)
    alt = alt or int(tam * 1.9)
    x0 = cx - (lt + 2 * pad) / 2
    d.rounded_rectangle([x0, cy - alt / 2, x0 + lt + 2 * pad, cy + alt / 2], radius=alt // 2, fill=fundo)
    ce.texto_espacado(d, (cx, cy), txt, f, cor, tam * esp)


def card_png(caminho, el):
    """Foto em cartão (cantos 28 px, fio rosé), sombra, e rótulo em pílula rosé claro."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    larg = el.get("larg", 780)
    foto = Image.open(el["img"]).convert("RGB")
    alt = el.get("alt") or min(int(larg * foto.height / foto.width), 900)
    foto = arredondar(cobrir(foto, larg, alt, el.get("foco_y", 0.35)), 28)
    cy = el.get("y", 700)
    x0, y0 = (W - larg) // 2, int(cy - alt / 2)
    img = sombra(img, (x0, y0, x0 + larg, y0 + alt), 28)
    img.alpha_composite(foto, (x0, y0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + larg - 1, y0 + alt - 1], radius=28, outline=rgb(ROSE) + (230,), width=3)
    if el.get("rotulo"):
        pilula(d, W / 2, y0 + alt, el["rotulo"], gal("b", 34), rgb(CLARO), rgb(GRANADA))
    img.save(caminho)
    return y0


def split_pngs(base, el):
    """Painel da metade de cima: fundo da marca, título metálico e itens (um PNG por item)."""
    from PIL import Image, ImageDraw
    hp = H // 2
    pnl = Image.new("RGBA", (W, hp), rgb(FUNDO) + (255,))
    pnl = ce.luz_lateral(pnl, "esq", 0.75, cy=0.25)
    vd = ce.monograma_vidro(900, 0.05)
    pnl.alpha_composite(vd, (W - int(vd.width * 0.55), 40))
    pnl = ce.veludo(pnl)
    d = ImageDraw.Draw(pnl)
    simb = ce.logo("EE_Horizontal_Principal.png", 240)
    pnl.alpha_composite(simb, ((W - simb.width) // 2, 46))
    t = ce.bloco_titulo([el.get("titulo", "O que você vai viver")], ce.fonte(PASTA_FONTES, "Gloock-Regular.ttf", 64))
    pnl.alpha_composite(t, ((W - t.width) // 2, 46 + simb.height + 14))
    d.line([(0, hp - 3), (W, hp - 3)], fill=rgb(ROSE), width=6)
    full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    full.alpha_composite(pnl, (0, 0))
    full.save(f"{base}_painel.png")
    itens = el["itens"]
    y_ini = 46 + simb.height + 14 + t.height + 16
    alt_item = min(118, int((hp - 30 - y_ini) / len(itens)) - 12)
    caminhos = []
    for k, it in enumerate(itens):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        y = y_ini + k * (alt_item + 12)
        x0, x1 = 70, W - 70
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([x0, y, x1, y + alt_item], radius=18, fill=(58, 18, 30, 235),
                            outline=rgb(ROSE) + (110,), width=2)
        tx = x0 + 28
        if it.get("img"):
            th = arredondar(cobrir(Image.open(it["img"]).convert("RGB"), alt_item - 16, alt_item - 16, 0.3), 12)
            img.alpha_composite(th, (x0 + 8, y + 8))
            tx = x0 + alt_item + 18
        f = gal("sb", 42 if alt_item >= 100 else 38)
        d.text((tx, y + alt_item / 2), it["txt"], font=f, fill=rgb(CLARO), anchor="lm")
        if it.get("tag"):
            ft = gal("b", 26)
            lt = d.textlength(it["tag"], font=ft)
            d.rounded_rectangle([x1 - lt - 46, y + alt_item / 2 - 22, x1 - 16, y + alt_item / 2 + 22], radius=22,
                                fill=rgb(ROSE))
            d.text((x1 - 31 - lt / 2, y + alt_item / 2), it["tag"], font=ft, fill=rgb(FUNDO), anchor="mm")
        p = f"{base}_item{k}.png"
        img.save(p)
        caminhos.append(p)
    return f"{base}_painel.png", caminhos


# ---------- render ----------
def renderizar(cfg, v):
    global PASTA_FONTES
    PASTA_FONTES = cfg["fontsdir"]
    els = v.get("elementos", [])
    JANELAS[:] = [(e["ini"], e["fim"], e["tipo"]) for e in els]
    duracao = fea.renderizar(cfg, v, "legenda")
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    manter = ce.CAPTURA["manter"]
    base = os.path.dirname(v["saida"]) or "."
    nome = os.path.basename(v["saida"]).split(" - ")[0].replace(" ", "")
    tj, ct = f"{base}/_tarja.png", f"{base}/_cta.png"
    v2.tarja(tj, v.get("tarja", {}), PASTA_FONTES)
    v2.cta(ct, v.get("cta", {}), PASTA_FONTES)
    t_fim = v.get("tarja_fim", 6.5)
    c_ini = max(duracao - v.get("cta_dur", 6.5), t_fim + 1)

    entradas = [["-i", v["entrada"]],
                ["-loop", "1", "-framerate", "30", "-t", f"{t_fim}", "-i", tj],
                ["-loop", "1", "-framerate", "30", "-t", f"{duracao:.3f}", "-i", ct],
                ["-i", v["musica"]], ["-i", v["sfx_whoosh"]], ["-i", v["sfx_boom"]]]

    def nova(png, dur):
        entradas.append(["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", png])
        return len(entradas) - 1

    partes, vrot, arot = [], [], []
    for i, (a, b) in enumerate((t[0], t[1]) for t in manter):
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1[v{i}]")
        vrot.append(f"[v{i}]")
        arot.append(f"[a{i}]")
    f = ";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0,fps=30,eq=contrast=1.05:saturation=1.03[vb];"
    f += "".join(arot) + f"concat=n={len(arot)}:v=0:a=1[voz];"
    atual, n = "vb", 0
    sfx = []   # (rótulo de entrada, tempo)

    def ov(entrada, ini, fim, slide=True, xy="0:0"):
        nonlocal atual, n
        n += 1
        fl = f"[{entrada}:v]format=rgba,fade=t=in:st={ini:.2f}:d=0.22:alpha=1,fade=t=out:st={fim - 0.2:.2f}:d=0.2:alpha=1[o{n}];"
        y = f"if(lt(t,{ini + 0.28:.2f}),70*(1-(t-{ini:.2f})/0.28),0)" if slide else "0"
        fl += (f"[{atual}][o{n}]overlay=x=0:y='{y}':enable='between(t,{ini:.2f},{fim:.2f})':"
               f"eof_action=pass[s{n}];")
        atual = f"s{n}"
        return fl

    for k, el in enumerate(els):
        if el["tipo"] == "card":
            p = f"{base}/_{nome}_card{k}.png"
            card_png(p, el)
            f += ov(nova(p, el["fim"]), el["ini"], el["fim"])
            sfx.append((4, el["ini"]))
        elif el["tipo"] == "split":
            pnl, itens = split_pngs(f"{base}/_{nome}_split{k}", el)
            ini, fim = el["ini"], el["fim"]
            n += 1
            cy = el.get("crop_y", 300)
            # metade de baixo: o próprio Dr., enquadrado no rosto
            f += (f"[{atual}]split[sa{n}][sb{n}];[sb{n}]crop={W}:{H // 2}:0:{cy}[sc{n}];"
                  f"[sa{n}][sc{n}]overlay=0:{H // 2}:enable='between(t,{ini:.2f},{fim:.2f})'[s{n}];")
            atual = f"s{n}"
            f += ov(nova(pnl, fim), ini, fim, slide=False)
            sfx.append((5, ini))
            passo = min(0.55, (fim - ini - 1.0) / max(len(itens), 1))
            for j, p in enumerate(itens):
                t0 = ini + 0.35 + j * passo
                f += ov(nova(p, fim), t0, fim)
                sfx.append((4, t0))
    pr = v.get("print")
    if pr:
        ce.cartao_print(f"{base}/_{nome}_print.png", pr)
        f += ov(nova(f"{base}/_{nome}_print.png", pr["fim"]), pr["ini"], pr["fim"])
        sfx.append((4, pr["ini"]))
    # tarja e CTA
    f += (f"[1:v]format=rgba,fade=t=in:st=0.1:d=0.25:alpha=1,fade=t=out:st={t_fim - 0.25}:d=0.25:alpha=1[tj];"
          f"[{atual}][tj]overlay=0:0:eof_action=pass[tt];")
    f += (f"[2:v]format=rgba,fade=t=in:st={c_ini:.2f}:d=0.3:alpha=1[ct];"
          f"[tt][ct]overlay=0:0:enable='gte(t,{c_ini:.2f})'[tc];")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    fd = PASTA_FONTES.replace(":", "\\:")
    f += f"[tc]ass='{esc}':fontsdir='{fd}',format=yuv420p[vfin];"
    sfx.insert(0, (5, 0.1))   # boom na entrada da tarja
    # áudio: voz + trilha com ducking + efeitos
    mus_db = v.get("musica_db", -13)
    f += ("[voz]asplit=2[voz1][vozk];"
          f"[3:a]atrim=0:{duracao:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={mus_db}dB,"
          f"afade=t=in:d=0.3,afade=t=out:st={duracao - 1.0:.3f}:d=1.0[mus];"
          "[mus][vozk]sidechaincompress=threshold=0.035:ratio=3:attack=25:release=300[musd];")
    cont = {4: 0, 5: 0}
    usos = {4: sum(1 for e, _ in sfx if e == 4), 5: sum(1 for e, _ in sfx if e == 5)}
    for e, u in usos.items():
        if u:
            f += f"[{e}:a]aresample=48000,volume={'-9dB' if e == 4 else '-6dB'},asplit={u}" + "".join(
                f"[x{e}_{i}]" for i in range(u)) + ";"
    fx = []
    for e, t0 in sfx:
        i = cont[e]
        cont[e] += 1
        f += f"[x{e}_{i}]adelay={int(max(0, t0 - (0.4 if e == 4 else 0.05)) * 1000)}:all=1[y{e}_{i}];"
        fx.append(f"[y{e}_{i}]")
    f += (f"[voz1][musd]{''.join(fx)}amix=inputs={2 + len(fx)}:duration=first:normalize=0,"
          "alimiter=limit=0.95[afin]")
    cmd = [cfg["ffmpeg"], "-y", "-v", "error"]
    for e in entradas:
        cmd += e
    cmd += ["-filter_complex", f, "-map", "[vfin]", "-map", "[afin]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", f"{duracao:.3f}", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return duracao


def main():
    args = sys.argv[1:]
    cfg = json.load(open(args[0], encoding="utf-8"))
    for v in cfg["videos"]:
        if args[1:] and not any(x in v["saida"] for x in args[1:]):
            continue
        print(f"{v['saida']}: {renderizar(cfg, v):.1f}s", flush=True)


if __name__ == "__main__":
    main()
