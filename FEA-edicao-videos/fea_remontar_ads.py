#!/usr/bin/env python3
"""FEA: remonta anúncios já aprovados a partir do bruto original, em qualidade total.

Uso quando o anúncio aprovado existe só em baixa qualidade (ex.: lote Black Amazonia,
26/09/2026, editado quando ainda não havia acesso ao Drive). Refaz o mesmo corte, a mesma
headline e as mesmas linhas de legenda aprovadas, direto do .MOV, com o CTA no final.

Uso:
    python3 fea_remontar_ads.py projeto.json [trecho_do_nome ...]

projeto.json:
{
  "fontsdir": "/caminho/fonts",
  "cta": "/caminho/CTA.mov",
  "videos": [
    {
      "entrada": "brutos/IMG_0665.MOV",
      "transcricao": "tr/IMG_0665.json",          # saída do fea_transcrever.py
      "saida": "out/Ads 004 - Faltam 3 dias - BFV.mp4",
      "manter": [[0.27, 22.60], [24.67, 25.63]],  # segundos do bruto, cortes exatos (sem encaixe)
      "titulo": ["Faltam 3 dias"],                # uma linha por item, nos 3 primeiros segundos
      "legendas": ["das inscrições para Black Friday Vitalícia", ...]   # linhas aprovadas, em ordem
    }
  ]
}

Padrão visual medido nos anúncios aprovados do lote: headline Montserrat ExtraBold 140 px
branca com contorno preto, centro do quadro, 0 a 3 s; legenda Montserrat Bold 56 px branca
com contorno escuro, terço inferior, só depois dos 3 s; CTA sem nada por cima.
Saída H.264 CRF 18, AAC 192k 48 kHz (nunca HEVC: abre com tela preta no computador da Keila).
"""
import difflib
import json
import os
import re
import subprocess
import sys

W, H = 1080, 1920
TITULO_TAM = 140
TITULO_DUR = 3.0
LEGENDA_TAM = 56
LEGENDA_MARGEM_V = 365
MAX_CHARS_LINHA = 22
FF = os.environ.get("FEA_FFMPEG", "ffmpeg")


def ts(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def norm(w):
    w = re.sub(r"[^\wà-ú]", "", w.lower())
    return {"pra": "para", "pro": "para", "tá": "está", "tamo": "estamos", "tua": "sua"}.get(w, w)


def quebrar_linhas(texto):
    if len(texto) <= MAX_CHARS_LINHA:
        return texto
    palavras = texto.split()
    melhor, dif = texto, 10 ** 9
    for i in range(1, len(palavras)):
        l1, l2 = " ".join(palavras[:i]), " ".join(palavras[i:])
        d = abs(len(l1) - len(l2)) + (0 if len(l1) <= len(l2) + 4 else 3)
        if d < dif:
            melhor, dif = l1 + r"\N" + l2, d
    return melhor


def palavras_no_corte(trans, manter):
    """Palavras da transcrição levadas para o tempo do vídeo editado (só as que ficam no corte)."""
    out, base = [], 0.0
    for a, b in manter:
        for seg in trans:
            for w in seg["words"]:
                meio = (w["s"] + w["e"]) / 2
                if a <= meio < b:
                    out.append({"w": w["w"].strip(), "s": w["s"] - a + base, "e": min(w["e"], b) - a + base})
        base += b - a
    return out, base


def tempos_das_linhas(linhas, palavras, duracao):
    """Casa cada linha aprovada com as palavras faladas e devolve (inicio, fim) de cada uma."""
    toks = [(i, norm(t)) for i, l in enumerate(linhas) for t in l.split()]
    falas = [norm(p["w"]) for p in palavras]
    sm = difflib.SequenceMatcher(None, [t for _, t in toks], falas, autojunk=False)
    casado = {}
    for bl in sm.get_matching_blocks():
        for k in range(bl.size):
            casado[bl.a + k] = bl.b + k
    ini, fim = [None] * len(linhas), [None] * len(linhas)
    for k, (i, _) in enumerate(toks):
        if k in casado:
            p = palavras[casado[k]]
            ini[i] = p["s"] if ini[i] is None else ini[i]
            fim[i] = p["e"]
    sem = [linhas[i] for i in range(len(linhas)) if ini[i] is None]
    if sem:
        sys.exit("ERRO: linha sem fala correspondente: " + " | ".join(sem))
    tempos = []
    for i in range(len(linhas)):
        s = max(TITULO_DUR, ini[i])
        prox = ini[i + 1] if i + 1 < len(linhas) else duracao
        e = prox if prox - fim[i] < 0.8 else fim[i] + 0.35
        tempos.append((s, min(e, duracao)))
    return tempos


def gerar_ass(v, tempos, caminho):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat ExtraBold,{TITULO_TAM},&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,6,2,5,60,60,0,1
Style: Legenda,Montserrat Bold,{LEGENDA_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H80000000,0,0,0,0,100,100,0,0,1,3.5,2,2,90,90,{LEGENDA_MARGEM_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 1,{ts(0)},{ts(TITULO_DUR)},Titulo,,0,0,0,,{{\\fad(0,250)}}" + r"\N".join(v["titulo"])]
    for linha, (s, e) in zip(v["legendas"], tempos):
        if e - s > 0.05:
            ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Legenda,,0,0,0,,{quebrar_linhas(linha)}")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(cab + "\n".join(ev) + "\n")


def renderizar(cfg, v):
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    palavras, duracao = palavras_no_corte(trans, v["manter"])
    tempos = tempos_das_linhas(v["legendas"], palavras, duracao)
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    gerar_ass(v, tempos, ass)
    for linha, (s, e) in zip(v["legendas"], tempos):
        print(f"  [{s:5.2f}-{e:5.2f}] {linha}")

    partes, rot = [], []
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},fps=30,setsar=1[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,"
                      f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        rot.append(f"[v{i}][a{i}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filtro = (";".join(partes) + ";" + "".join(rot) + f"concat=n={len(rot)}:v=1:a=1[vc][ac];"
              f"[vc]ass='{esc}':fontsdir='{cfg['fontsdir']}'[vt];"
              f"[1:v]scale={W}:{H},fps=30,setsar=1[cv];[1:a]aresample=48000[ca];"
              f"[vt][ac][cv][ca]concat=n=2:v=1:a=1[vo][ao]")
    cmd = [FF, "-nostdin", "-y", "-v", "error", "-i", v["entrada"], "-i", cfg["cta"], "-filter_complex", filtro,
           "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-ac", "2", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)


def main():
    args = sys.argv[1:]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:]
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        print(v["saida"], flush=True)
        renderizar(cfg, v)


if __name__ == "__main__":
    main()
