#!/usr/bin/env python3
"""FEA: edição de criativo (anúncio) do Elite Experience no estilo "faixa de qualificação".

Estilo pedido pela Keila em 17/11/2026 (referência: anúncio com faixa "Para empresas que faturam
mais de R$ 100 MIL / mês"), aplicado na identidade visual oficial do Elite Experience
(manual em ELITE EXPERIENCE > 5. LOGO > Elite Experience - Identidade Visual):
  - faixa granada/rosé com "Para injetores que faturam mais de R$ 15 MIL / mês" do início até
    o momento em que ele fala "clica/clicar aqui em saiba mais";
  - dali até o fim, pílula "CLIQUE E SAIBA MAIS" (chamada do manual: Galano SemiBold sobre rosé
    #E48AA0, texto #0F0507) e um flash de luz rosé de 0,8 s na entrada;
  - legenda curta (até 3 palavras), Galano Grotesque SemiBold branca, números e palavras-chave
    em rosé #E48AA0;
  - zoom alternado (1,00 / 1,10) a cada frase, como os cortes secos da referência.

Uso:
  python3 fea_elite_criativo.py BRUTO.MOV TRANSCRICAO.json SAIDA.mp4 --ativos PASTA [--inicio s] [--fim s]
PASTA de ativos: faixa.png, cta.png, flash.png e fonts/ (Galano Grotesque).
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_editar_video import CORRECOES  # regra FEA ("pra" -> "para") e grafias

EXTRAS = [(r"\bSaba\b", "Saiba"), (r"\bsaiba mais\b", "Saiba Mais"), (r"\b[Ee]lite [Ee]xperience\b", "Elite Experience"),
          (r"\b15 mil reais\b", "R$ 15 mil"), (r"\btá\b", "está"), (r"\bTá\b", "Está")]
DESTAQUE = re.compile(r"^(R\$|\d+%?|mil|gratuito|gratuita|Elite|Experience|São|Paulo|200|dois|dias|presencial|"
                      r"marketing|vendas|equipe|crescer|selecionar|selecionado|selecionadas)$", re.I)
LIGACAO = re.compile(r"(?i)^(e|o|a|os|as|de|do|da|dos|das|em|no|na|um|uma|que|para|pra|com|se|eu|você|"
                     r"sua|seu|teu|tua|meu|minha|é|por|ao|à)$")
ROSE ="&H00A08AE4&"   # #E48AA0 em BGR do ASS
BRANCO = "&H00FFFFFF&"


def corrigir(t):
    for a, b in CORRECOES + EXTRAS:
        t = re.sub(a, b, t)
    return t


def palavras(tr, ini, fim):
    out = []
    for s in tr:
        for w in s["words"]:
            if w["s"] >= ini - 0.05 and w["e"] <= fim + 0.3:
                out.append({"s": max(w["s"], ini) - ini, "e": min(w["e"], fim) - ini, "w": w["w"].strip()})
    return out


UNIDADES = [r"(?i)^saiba mais", r"(?i)^são paulo", r"(?i)^\d+ mil( reais)?", r"(?i)^elite experience",
            r"(?i)^dois dias", r"(?i)^\d+ (pessoas|profissionais|inscritos)"]


def juntar_unidades(pal):
    """Expressões que nunca se separam na legenda viram um único token."""
    out, i = [], 0
    while i < len(pal):
        feito = False
        for n in (3, 2):
            grupo = pal[i:i + n]
            if len(grupo) < n:
                continue
            txt = " ".join(re.sub(r"[.,!?]$", "", g["w"]) for g in grupo[:-1]) + " " + grupo[-1]["w"]
            if any(re.match(u + r"[.,!?]?$", txt) for u in UNIDADES):
                out.append({"s": grupo[0]["s"], "e": grupo[-1]["e"], "w": txt})
                i += n
                feito = True
                break
        if not feito:
            out.append(pal[i])
            i += 1
    return out


def blocos(pal, max_pal=3, max_chars=20):
    """Agrupa em blocos curtos; quebra em pontuação e respeita limite de caracteres."""
    pal = juntar_unidades(pal)
    res, cur = [], []
    for p in pal:
        texto = " ".join(x["w"] for x in cur + [p])
        if cur and (sum(len(x["w"].split()) for x in cur) >= max_pal or len(texto) > max_chars):
            res.append(cur)
            cur = []
        cur.append(p)
        if re.search(r"[.,!?]$", p["w"]):
            res.append(cur)
            cur = []
    if cur:
        res.append(cur)
    # palavra de ligação, número ou "São" no fim do bloco vai para o próximo bloco
    # (evita "em São" / "Paulo", "de 15" / "mil")
    for i in range(len(res) - 1):
        while (len(res[i]) > 1 and not re.search(r"[.,!?]$", res[i][-1]["w"])
               and LIGACAO.match(res[i][-1]["w"])
               and sum(len(x["w"].split()) for x in res[i + 1]) < 4):
            res[i + 1].insert(0, res[i].pop())
    return [b for b in res if b]


def ts(t):
    t = max(t, 0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def gerar_ass(bls, caminho, y=1235):
    cab = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n"
           "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
           "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
           "MarginL, MarginR, MarginV, Encoding\n"
           "Style: L,Galano Grotesque SemiBold,72,&H00FFFFFF,&H00FFFFFF,&H00070510,&H96070510,0,0,0,0,100,100,0,0,1,0,3,5,60,60,0,1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    linhas = []
    for i, b in enumerate(bls):
        s = b[0]["s"]
        e = bls[i + 1][0]["s"] if i + 1 < len(bls) and bls[i + 1][0]["s"] - b[-1]["e"] < 0.6 else b[-1]["e"] + 0.15
        texto = corrigir(" ".join(p["w"] for p in b))
        texto = re.sub(r"[.,]$", "", texto)
        partes = []
        for w in texto.split(" "):
            nucleo = re.sub(r"[^\wÀ-ÿ$%]", "", w)
            cor = ROSE if DESTAQUE.match(nucleo or "-") else BRANCO
            partes.append("{\\c" + cor + "}" + w)
        linhas.append(f"Dialogue: 0,{ts(s)},{ts(e)},L,,0,0,0,,{{\\pos(540,{y})\\fad(60,0)}}" + " ".join(partes))
    open(caminho, "w", encoding="utf-8").write(cab + "\n".join(linhas) + "\n")


def momento_cta(pal):
    for i, p in enumerate(pal):
        if re.match(r"(?i)clic", p["w"]):
            return p["s"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("transcricao"); ap.add_argument("saida")
    ap.add_argument("--ativos", required=True)
    ap.add_argument("--inicio", type=float); ap.add_argument("--fim", type=float)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--previa", action="store_true")
    a = ap.parse_args()
    tr = json.load(open(a.transcricao, encoding="utf-8"))
    todas = [w for s in tr for w in s["words"]]
    ini = a.inicio if a.inicio is not None else max(0, todas[0]["s"] - 0.25)
    fim = a.fim if a.fim is not None else todas[-1]["e"] + 0.4
    dur = fim - ini
    pal = palavras(tr, ini, fim)
    cta = momento_cta(pal) or dur * 0.6
    bls = blocos(pal)
    base = os.path.splitext(a.saida)[0]
    ass = base + ".ass"
    gerar_ass(bls, ass)

    # zoom alternado por frase (fronteiras = início de cada segmento da transcrição)
    cortes = [max(0.0, s["start"] - ini) for s in tr if ini - 0.1 <= s["start"] < fim]
    cortes = sorted(set(round(c, 2) for c in cortes if c > 0.3))
    # expressão em cadeia: z(t) = z_k para t no intervalo k
    zs = []
    for i, c in enumerate(cortes):
        zs.append((c, 1.10 if i % 2 == 0 else 1.0))
    expr = "1"
    for c, z in zs:
        expr = f"if(gte(t\\,{c})\\,{z}\\,{expr})"
    at = a.ativos
    esc = ass.replace(":", "\\:").replace("'", "\\'")
    fx = (f"[0:v]setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          f"scale=w='trunc(1080*{expr}/2)*2':h='trunc(1920*{expr}/2)*2':eval=frame,crop=1080:1920,setsar=1,fps=30[v0];"
          f"[1:v]format=rgba[fa];[2:v]format=rgba[ct];"
          f"[3:v]format=rgba,fade=in:st={cta:.2f}:d=0.2:alpha=1,fade=out:st={cta + 0.25:.2f}:d=0.6:alpha=1[fl];"
          f"[v0][fa]overlay=0:1395:enable='lt(t,{cta:.2f})'[v1];"
          f"[v1][ct]overlay=(W-w)/2:1420:enable='gte(t,{cta:.2f})'[v2];"
          f"[v2][fl]overlay=0:0:enable='between(t,{cta:.2f},{cta + 0.9:.2f})'[v3];"
          f"[v3]ass='{esc}':fontsdir='{at}/fonts'[vo]")
    cmd = [a.ffmpeg, "-v", "error", "-y", "-ss", f"{ini:.3f}", "-t", f"{dur:.3f}", "-i", a.entrada,
           "-loop", "1", "-t", f"{dur:.3f}", "-i", f"{at}/faixa.png",
           "-loop", "1", "-t", f"{dur:.3f}", "-i", f"{at}/cta.png",
           "-loop", "1", "-t", f"{dur:.3f}", "-framerate", "30", "-i", f"{at}/flash.png",
           "-filter_complex", fx, "-map", "[vo]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "veryfast" if a.previa else "slow", "-crf", "23" if a.previa else "18",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-t", f"{dur:.3f}", a.saida]
    subprocess.run(cmd, check=True)
    print(f"OK {a.saida}: {dur:.1f} s, CTA aos {cta:.1f} s, {len(bls)} blocos de legenda")


if __name__ == "__main__":
    main()
