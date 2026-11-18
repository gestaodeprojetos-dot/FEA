#!/usr/bin/env python3
"""FEA: criativos do Elite Experience no "modelo Luca" (pedido da Keila, 18/11/2026).

Espelha o vídeo de referência enviado pelo Luca (anúncio de empresa com tarja de público):
  - sem abertura com véu e título: o vídeo começa direto no Dr., já falando;
  - tarja fixa nos primeiros segundos com a chamada de público
    ("Para injetores que faturam mais de R$ 15 MIL /mês"), em pílula, com o monograma;
  - legenda curta (2 a 4 palavras, uma linha), branca, com sombra, um pouco acima da tarja;
  - palavras-chave em destaque grande no lugar da legenda (2 DIAS, GRATUITO, 200..., R$ 15 MIL);
  - "CLIQUE E SAIBA MAIS" fixo nos segundos finais, com data e cidade do evento;
  - trilha mais presente e ritmada que a versão anterior, com ducking leve;
  - sem cartela final (o vídeo de referência termina no apresentador).
Mantém a identidade do manual: rosé claro #FFE3EA, granada #8E1F3A, rosé #E48AA0, Urbanist
(substituta da Galano), monograma oficial.

Uso:
    python3 fea_criativo_elite_v2.py projeto.json [filtro ...]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_criativo_elite as ce   # noqa: E402  (aplica os patches de identidade e reaproveita os desenhos)
fea = ce.fea
W, H, rgb, ass_cor, fonte = ce.W, ce.H, ce.rgb, ce.ass_cor, ce.fonte
FUNDO, GRANADA, ROSE, CLARO = ce.FUNDO, ce.GRANADA, ce.ROSE, ce.CLARO

# ---------- legenda curta, uma linha, sem título ----------
fea.TITULO_DUR = 0.0
fea.LEGENDA_TAM = 62
fea.LEGENDA_Y = 1280          # base da linha em 1300 (acima da tarja)
fea.MAX_CHARS_LINHA = 14      # bloco de até ~28 caracteres
fea.MAX_PALAVRAS_BLOCO = 4
fea.quebrar_linhas = lambda texto: texto   # sempre uma linha, como no modelo

DESTAQUES = [   # (regex no bloco, texto grande) — cada um no máximo uma vez por vídeo
    (r"\b(dois|2) dias\b", "2 DIAS"),
    (r"\bgratuit[oa]\b", "GRATUITO"),
    (r"\b15 mil\b", "R$ 15 MIL"),
    (r"\b30 milhões\b", "30 MILHÕES"),
    (r"\b200 (pessoas|profissionais|inscritos)\b", None),   # None = o próprio trecho em caixa alta
    (r"\bSão Paulo\b", "SÃO PAULO"),
]
MAX_DESTAQUES = 4


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
Style: Legenda,Urbanist,{fea.LEGENDA_TAM},{c},{c},{ass_cor(FUNDO, 0x50)},{ass_cor(FUNDO, 0x60)},-1,0,0,0,100,100,0,0,1,2.2,3,2,60,60,0,1
Style: Destaque,Urbanist ExtraBold,150,{c},{c},{ass_cor(FUNDO, 0x40)},{ass_cor(FUNDO, 0x50)},0,0,0,0,94,100,-2,0,1,2.5,5,2,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


fea.ass_header = ass_header
_gerar_base = ce._gerar_ass


def gerar_ass(v, palavras, duracao, caminho):
    ce.CAPTURA["manter"] = v["manter"]
    _gerar_base(v, palavras, duracao, caminho)
    usados, n = set(), 0
    saida = []
    for ln in open(caminho, encoding="utf-8").read().splitlines(True):
        if ln.startswith("Dialogue:") and ",Titulo," in ln:
            continue
        if ln.startswith("Dialogue:") and ",Legenda," in ln:
            cab, txt = ln.rsplit("}", 1)
            txt = txt.rstrip("\n")
            limpo = re.sub(r"\{[^}]*\}", "", txt)
            for i, (rx, grande) in enumerate(DESTAQUES):
                m = re.search(rx, limpo, re.I)
                if m and i not in usados and n < MAX_DESTAQUES:
                    usados.add(i)
                    n += 1
                    grande = grande or m.group(0).upper()
                    tam = min(150, int(1700 / max(len(grande), 1)))
                    partes = cab.split(",")
                    ini, fim = partes[1], partes[2]
                    ln = (f"Dialogue: 1,{ini},{fim},Destaque,,0,0,0,,{{\\an2\\pos({W // 2},{fea.LEGENDA_Y + 30})\\fs{tam}"
                          f"\\fscx80\\fscy80\\t(0,120,\\fscx100\\fscy100)}}{grande}\n")
                    break
            else:
                ln = cab + "}" + ce.colorir(txt, v.get("destaques", [])) + "\n"
        saida.append(ln)
    open(caminho, "w", encoding="utf-8").write("".join(saida))


fea.gerar_ass = gerar_ass


# ---------- grafismos ----------
def simbolo_granada(alt):
    """Monograma oficial na versão Granada (mesmo desenho, cor sólida do manual)."""
    from PIL import Image
    s = Image.open(os.path.join(ce.MARCA, "EE_Simbolo_Principal.png"))
    s = s.resize((int(s.width * alt / s.height), alt), Image.LANCZOS)
    g = Image.new("RGBA", s.size, rgb(GRANADA) + (0,))
    g.putalpha(s.getchannel("A"))
    return g


def tarja(caminho, c, pasta):
    """Tarja de público: barra rosé claro, texto granada, pílula granada com o valor e o monograma."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y0, alt = c.get("y", 1385), 128
    d.rectangle([0, y0, W, y0 + alt], fill=rgb(CLARO) + (250,))
    f1 = fonte(pasta, "Urbanist-600.ttf", 34)
    fv = fonte(pasta, "Urbanist-800.ttf", 58)
    fm = fonte(pasta, "Urbanist-600.ttf", 26)
    l1, l2 = c.get("linha1", "Para injetores que"), c.get("linha2", "faturam mais de")
    valor, sufixo = c.get("valor", "R$ 15 MIL"), c.get("sufixo", "/mês")
    w_txt = max(d.textlength(l1, font=f1), d.textlength(l2, font=f1))
    w_val, w_suf = d.textlength(valor, font=fv), d.textlength(sufixo, font=fm)
    w_pil = w_val + w_suf + 64
    simb = simbolo_granada(78)
    gap = 26
    total = w_txt + gap + w_pil + gap + 2 + gap + simb.width
    x = (W - total) / 2
    cy = y0 + alt / 2
    d.text((x + w_txt, cy - 4), l1, font=f1, fill=rgb(GRANADA), anchor="rs")
    d.text((x + w_txt, cy + 4), l2, font=f1, fill=rgb(GRANADA), anchor="rt")
    x += w_txt + gap
    d.rounded_rectangle([x, cy - 44, x + w_pil, cy + 44], radius=14, fill=rgb(GRANADA))
    d.text((x + 28, cy + 2), valor, font=fv, fill=rgb(CLARO), anchor="lm")
    d.text((x + 28 + w_val + 8, cy + 14), sufixo, font=fm, fill=rgb(CLARO), anchor="ls")
    x += w_pil + gap
    d.line([(x, cy - 40), (x, cy + 40)], fill=rgb(GRANADA) + (120,), width=2)
    x += 2 + gap
    img.alpha_composite(simb, (int(x), int(cy - simb.height / 2)))
    img.save(caminho)


def cta(caminho, c, pasta):
    """'CLIQUE E SAIBA MAIS' com ícone, e o evento (data e cidade) logo abaixo."""
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = c.get("y", 1430)
    f = fonte(pasta, "Urbanist-800.ttf", 52)
    txt = c.get("texto", "CLIQUE E SAIBA MAIS")
    tmp = ImageDraw.Draw(img)
    lt = tmp.textlength(txt, font=f)
    r = 26
    total = 2 * r + 20 + lt
    x = (W - total) / 2
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    ds.text((x + 2 * r + 20, y + 4), txt, font=f, fill=(15, 5, 7, 170), anchor="lm")
    ds.ellipse([x, y - r + 4, x + 2 * r, y + r + 4], outline=(15, 5, 7, 170), width=5)
    img = Image.alpha_composite(img, sombra.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(img)
    d.ellipse([x, y - r, x + 2 * r, y + r], outline=rgb(ROSE), width=5)
    # seta diagonal (clique) dentro do círculo
    d.line([(x + r - 9, y + 9), (x + r + 9, y - 9)], fill=rgb(ROSE), width=5)
    d.line([(x + r - 2, y - 9), (x + r + 9, y - 9), (x + r + 9, y + 2)], fill=rgb(ROSE), width=5)
    d.text((x + 2 * r + 20, y), txt, font=f, fill=(255, 255, 255), anchor="lm")
    sub = c.get("evento", "ELITE EXPERIENCE  ·  4 E 5 DE DEZEMBRO  ·  SÃO PAULO")
    fs = fonte(pasta, "Urbanist-700.ttf", 27)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ce.texto_espacado(ImageDraw.Draw(sh), (W / 2, y + 66), sub, fs, (15, 5, 7, 190), 27 * 0.22)
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(4)))
    ce.texto_espacado(ImageDraw.Draw(img), (W / 2, y + 62), sub, fs, rgb(CLARO), 27 * 0.22)
    img.save(caminho)


# ---------- render ----------
def renderizar(cfg, v):
    duracao = fea.renderizar(cfg, v, "legenda")
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    manter = ce.CAPTURA["manter"]
    base = os.path.dirname(v["saida"]) or "."
    tj, ct = f"{base}/_tarja.png", f"{base}/_cta.png"
    tarja(tj, v.get("tarja", {}), cfg["fontsdir"])
    cta(ct, v.get("cta", {}), cfg["fontsdir"])
    t_fim = v.get("tarja_fim", 6.5)
    c_ini = max(duracao - v.get("cta_dur", 7.0), t_fim + 1)
    pr = v.get("print")
    if pr:
        ce.cartao_print(f"{base}/_print.png", pr)
    mus_db = v.get("musica_db", -16)
    partes, vrot, arot = [], [], []
    for i, (a, b) in enumerate((t[0], t[1]) for t in manter):
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1[v{i}]")
        vrot.append(f"[v{i}]")
        arot.append(f"[a{i}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    fd = cfg["fontsdir"].replace(":", "\\:")
    f = ";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0,fps=30[vc];"
    f += "".join(arot) + f"concat=n={len(arot)}:v=0:a=1[voz];"
    f += "[vc]eq=contrast=1.05:saturation=1.03[vg];"
    f += (f"[1:v]format=rgba,fade=t=in:st=0.15:d=0.25:alpha=1,fade=t=out:st={t_fim - 0.25}:d=0.25:alpha=1[tj];"
          f"[vg][tj]overlay=0:0:eof_action=pass[v1];")
    f += (f"[2:v]format=rgba,fade=t=in:st={c_ini:.2f}:d=0.3:alpha=1[ct];"
          f"[v1][ct]overlay=0:0:enable='gte(t,{c_ini:.2f})'[v2];")
    if pr:
        f += (f"[4:v]format=rgba,fade=t=in:st={pr['ini']}:d=0.25:alpha=1,"
              f"fade=t=out:st={pr['fim'] - 0.25}:d=0.25:alpha=1[pr];[v2][pr]overlay=0:0:eof_action=pass[v3];")
    else:
        f += "[v2]null[v3];"
    f += f"[v3]ass='{esc}':fontsdir='{fd}',format=yuv420p[vfin];"
    f += ("[voz]asplit=2[voz1][vozk];"
          f"[3:a]atrim=0:{duracao:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={mus_db}dB,"
          f"afade=t=in:d=0.4,afade=t=out:st={duracao - 1.2:.3f}:d=1.2[mus];"
          "[mus][vozk]sidechaincompress=threshold=0.04:ratio=2.5:attack=30:release=350[musd];"
          "[voz1][musd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[afin]")
    cmd = [cfg["ffmpeg"], "-y", "-v", "error", "-i", v["entrada"],
           "-loop", "1", "-framerate", "30", "-t", f"{t_fim}", "-i", tj,
           "-loop", "1", "-framerate", "30", "-t", f"{duracao:.3f}", "-i", ct,
           "-stream_loop", "-1", "-i", v["musica"],
           *(["-loop", "1", "-framerate", "30", "-t", f"{pr['fim']}", "-i", f"{base}/_print.png"] if pr else []),
           "-filter_complex", f, "-map", "[vfin]", "-map", "[afin]",
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
