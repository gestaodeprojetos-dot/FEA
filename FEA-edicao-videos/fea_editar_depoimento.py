#!/usr/bin/env python3
"""FEA: edição de depoimentos de alunos no padrão "Ads FEP" (Reels de anúncio da FEP).

Padrão (pastas de referência "Ads N FEP" e "Ads N FEP ES", out/2026):
- bruto horizontal 4K da entrevista vira vertical 1080x1920, 30 fps, recortado acima da
  legenda queimada que já vem no bruto (o recorte nunca pode pegar essa legenda);
- jump cut entre os melhores trechos, com zoom alternado (1,0 / 1,1) para disfarçar o corte;
- legenda Montserrat Bold branca com contorno fino, centralizada a ~76% da altura (no peito),
  frase com maiúscula e pontuação (como a referência), 1 a 2 linhas;
- destaque em caixa alta condensada (Oswald Bold) acima da legenda nas palavras-chave;
- termina com a cartela FEP de 4 s ("Toque em SAIBA MAIS" / "Toca en MÁS INFORMACIÓN"),
  extraída das próprias referências.

Uso:
    python3 fea_editar_depoimento.py projeto.json pt|es [id ...] [--previa]

projeto.json: {"fontes": dir, "cta": {"pt": mp4, "es": mp4}, "saida": dir, "videos": [
  {"id", "entrada", "nome": {"pt", "es"}, "crop": {"cx", "h"},
   "trechos": [[ini, fim], ...]                 (segundos do bruto),
   "legendas": [[ini, fim, "pt", "es"], ...]     (segundos do bruto),
   "destaques": [[ini, fim, "PT", "ES"], ...]}]}
"""
import json
import os
import subprocess
import sys

W, H = 1080, 1920
LEG_Y = 1470          # centro da legenda: no peito, abaixo do queixo (enquadramento mais fechado que a referência)
DEST_Y = 1380         # base do destaque, logo acima da legenda
LEG_MAX = 28          # caracteres por linha


def quebrar(txt, maxc=LEG_MAX):
    if len(txt) <= maxc:
        return txt
    pal = txt.split()
    melhor, dif = txt, 1e9
    for i in range(1, len(pal)):
        a, b = " ".join(pal[:i]), " ".join(pal[i:])
        d = max(len(a), len(b)) + (0 if len(a) <= len(b) + 6 else 3)
        if d < dif:
            melhor, dif = a + r"\N" + b, d
    return melhor


def ts(t):
    t = max(t, 0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def mapa(trechos):
    """Converte tempo do bruto em tempo do vídeo editado (None se caiu num corte)."""
    def f(t, borda=False):
        acc = 0.0
        for a, b in trechos:
            if a - (0.05 if borda else 0) <= t <= b + (0.05 if borda else 0):
                return acc + min(max(t, a), b) - a
            acc += b - a
        return None
    return f


def recortar(intervalo, trechos):
    """Partes de [ini, fim] do bruto que sobrevivem aos cortes, já no tempo editado."""
    ini, fim = intervalo
    out, acc = [], 0.0
    for a, b in trechos:
        x, y = max(ini, a), min(fim, b)
        if y - x > 0.05:
            out.append((acc + x - a, acc + y - a))
        acc += b - a
    return out


def gerar_ass(v, lang, caminho):
    tr = v["trechos"]
    linhas = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Leg,Montserrat,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,"
        "3.2,1.5,5,60,60,0,1",
        "Style: Dest,Oswald,92,&H00F2EEEC,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,1,0,1,"
        "0,3,2,60,60,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    idx = 2 if lang == "pt" else 3
    for item in v["legendas"]:
        for a, b in recortar(item[:2], tr):
            txt = quebrar(item[idx])
            linhas.append(f"Dialogue: 0,{ts(a)},{ts(b)},Leg,,0,0,0,,{{\\pos({W // 2},{LEG_Y})}}{txt}")
    for item in v.get("destaques", []):
        for a, b in recortar(item[:2], tr):
            txt = quebrar(item[idx].upper(), 16)
            linhas.append(f"Dialogue: 1,{ts(a)},{ts(b)},Dest,,0,0,0,,{{\\pos({W // 2},{DEST_Y})"
                          f"\\fad(120,80)}}{txt}")
    open(caminho, "w", encoding="utf-8").write("\n".join(linhas) + "\n")


def render(proj, v, lang, previa=False):
    os.makedirs(proj["saida"], exist_ok=True)
    ass = os.path.join(proj["saida"], f"{v['id']}_{lang}.ass")
    gerar_ass(v, lang, ass)
    cx, ch = v["crop"]["cx"], v["crop"]["h"]
    tmp = os.path.join(proj["saida"], "tmp")
    os.makedirs(tmp, exist_ok=True)
    partes = []
    # cada trecho é decodificado sozinho (o 4K HEVC inteiro num filtro só estoura a memória)
    for i, (a, b) in enumerate(v["trechos"]):
        z = 1.0 if i % 2 == 0 else 1.1
        h = int(ch / z) // 2 * 2
        w = int(h * 9 / 16) // 2 * 2
        y = int(v["crop"].get("topo", 0) + (ch - h) * 0.25) // 2 * 2
        x = int(cx - w / 2) // 2 * 2
        d = b - a
        parte = os.path.join(tmp, f"{v['id']}_{i}.mkv")
        chave = json.dumps([a, b, w, h, x, y, v["entrada"]])
        if not (os.path.exists(parte) and open(parte + ".k").read() == chave):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", v["entrada"], "-t", f"{d}",
                            "-vf", f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p",
                            "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,"
                                   f"afade=t=out:st={d - 0.03:.3f}:d=0.03",
                            "-c:v", "libx264", "-crf", "10", "-preset", "veryfast", "-c:a", "pcm_s16le",
                            parte], check=True)
            open(parte + ".k", "w").write(chave)
        partes.append(parte)
    lista = os.path.join(tmp, f"{v['id']}.txt")
    open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
    fontes = proj["fontes"]
    filtros = [f"[0:v]subtitles='{ass}':fontsdir='{fontes}',setsar=1[vl]",
               "[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[vk]",
               "[1:a]aresample=48000,aformat=channel_layouts=stereo[ak]",
               "[0:a]aformat=channel_layouts=stereo[ac]",
               "[vl][ac][vk][ak]concat=n=2:v=1:a=1[vo][ao]"]
    saida = os.path.join(proj["saida"], v["nome"][lang])
    q = ["-crf", "26", "-preset", "veryfast"] if previa else ["-crf", "18", "-preset", "slow"]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-i", proj["cta"][lang],
           "-filter_complex", ";".join(filtros), "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", *q, "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    return saida


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    previa = "--previa" in sys.argv
    proj = json.load(open(args[0], encoding="utf-8"))
    lang = args[1]
    ids = set(args[2:])
    for v in proj["videos"]:
        if ids and v["id"] not in ids:
            continue
        dur = sum(b - a for a, b in v["trechos"])
        print(f"{v['id']} {lang}: {dur:.1f} s + CTA -> {v['nome'][lang]}", flush=True)
        render(proj, v, lang, previa)


if __name__ == "__main__":
    main()
