#!/usr/bin/env python3
"""FEA: edição automática de vídeos verticais (Reels) no padrão da equipe.

Uso:
    python3 fea_editar_video.py projeto.json

O projeto.json descreve cada vídeo de saída:
{
  "ffmpeg": "/caminho/ffmpeg",
  "fontsdir": "fonts",
  "videos": [
    {
      "entrada": "raw/IMG_5481.MOV",
      "transcricao": "tr/raw_IMG_5481.json",   # saída do fea_transcrever.py (palavras com tempo)
      "saida": "out/1- Planejamento full face 4mL.mp4",
      "titulo": "Planejamento full face 4mL",
      "parte": null,                            # 1, 2 ou null
      "manter": [[0.0, 12.4], [15.1, 40.0]],    # trechos mantidos, em segundos do bruto
      "cartela_final": null                     # ex.: "Parte 2 no perfil"
    }
  ]
}

Padrão visual (derivado das referências da pasta "4- Full face 4ml", com os
ajustes pedidos pela Keila: Montserrat, título maior e centralizado, legenda
mais abaixo e menor):
  - Título: Montserrat ExtraBold, branco, sombra suave, centro exato do quadro,
    nos primeiros 3 segundos.
  - Legenda: Montserrat SemiBold, branca, contorno fino escuro, centralizada,
    no terço inferior, no máximo 2 linhas curtas por vez, em minúsculas.
  - Parte 1: "Parte 1" sob o título; cartela "Parte 2 no perfil" no mesmo
    estilo do título nos 3 segundos finais.
"""
import json
import re
import subprocess
import sys

W, H = 1080, 1920

TITULO_TAM = 140       # referência original: ~95 px (pedido: título maior)
TITULO_DUR = 3.0
LEGENDA_TAM = 36       # referência original: ~40 px
LEGENDA_Y = 1640       # referência original: ~1500 (centro da legenda)
CARTELA_DUR = 3.0
MAX_CHARS_LINHA = 26
MAX_PALAVRAS_BLOCO = 10
PAUSA_QUEBRA = 0.45    # pausa (s) que força novo bloco de legenda


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_header():
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat ExtraBold,{TITULO_TAM},&H00FFFFFF,&H00FFFFFF,&H64000000,&H78000000,0,0,0,0,100,100,0,0,1,2,4,5,80,80,0,1
Style: Legenda,Montserrat SemiBold,{LEGENDA_TAM},&H00FFFFFF,&H00FFFFFF,&H50000000,&H64000000,0,0,0,0,100,100,0,0,1,2.2,1.5,2,110,110,{H - LEGENDA_Y - 20},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def remapear_palavras(palavras, manter):
    """Converte tempos do bruto para a linha do tempo editada e descarta o que foi cortado."""
    saida = []
    offset = 0.0
    for a, b in manter:
        for p in palavras:
            meio = (p["s"] + p["e"]) / 2
            if a <= meio < b:
                saida.append({"w": p["w"].strip(),
                              "s": max(p["s"], a) - a + offset,
                              "e": min(p["e"], b) - a + offset})
        offset += b - a
    return [p for p in saida if p["w"]], offset


LIGACAO = {"de", "da", "do", "das", "dos", "a", "o", "as", "os", "e", "em", "no", "na",
           "com", "para", "pra", "que", "um", "uma", "por", "se", "ao", "à"}


def blocos_legenda(palavras):
    """Agrupa palavras em blocos curtos, quebrando em pausa, pontuação ou, se o bloco
    estourar o tamanho, na última vírgula dentro dele."""
    blocos, atual = [], []
    for p in palavras:
        if atual:
            texto = " ".join(x["w"] for x in atual + [p])
            if p["s"] - atual[-1]["e"] > PAUSA_QUEBRA or atual[-1]["w"][-1:] in ".?!":
                blocos.append(atual)
                atual = []
            elif len(atual) >= MAX_PALAVRAS_BLOCO or len(texto) > MAX_CHARS_LINHA * 2:
                virgulas = [i for i, x in enumerate(atual[:-1]) if x["w"].endswith(",")]
                corte = virgulas[-1] + 1 if virgulas and virgulas[-1] >= 1 else len(atual)
                # não termina bloco em preposição ou artigo ("do dia de / hoje")
                while corte > 2 and atual[corte - 1]["w"].strip().lower() in LIGACAO:
                    corte -= 1
                blocos.append(atual[:corte])
                atual = atual[corte:]
        atual.append(p)
    if atual:
        blocos.append(atual)
    return blocos


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


def quebrar_titulo(texto, limite=16):
    """Título em linhas equilibradas (até 3), cada uma com no máximo ~16 caracteres."""
    if r"\N" in texto:
        return texto
    palavras = texto.split()
    melhor = None
    for k in range(1, 4):
        def particoes(ps, k):
            if k == 1:
                yield [" ".join(ps)]
                return
            for i in range(1, len(ps) - k + 2):
                for resto in particoes(ps[i:], k - 1):
                    yield [" ".join(ps[:i])] + resto
        if k > len(palavras):
            break
        opcao = min(particoes(palavras, k), key=lambda ls: max(map(len, ls)))
        if melhor is None or max(map(len, opcao)) < max(map(len, melhor)):
            melhor = opcao
        if max(map(len, opcao)) <= limite:
            melhor = opcao
            break
    return r"\N".join(melhor)


# Correções fixas de transcrição (termos técnicos e regra de escrita FEA: nunca "pra")
CORRECOES = [
    (r"\bpra\b", "para"), (r"\bPra\b", "Para"),
    (r"\bpros\b", "para os"), (r"\bpro\b", "para o"),
    (r"\bcarpulha\b", "carpule"),
    (r"\btempra\b", "têmpora"),
    (r"\binterfacial\b", "interfascial"),
    (r"\bplanosinho\b", "planozinho"), (r"\bPlanosinho\b", "Planozinho"),
    (r"\bRevanesse quisse\b", "Revanesse Kiss"),
    (r"\bNeuramis volume\b", "Neuramis Volume"),
    (r"(\d) ?ml\b", r"\1 mL"),
    (r"\b24-70\b", "24G 70 mm"),
    (r"\bboulos\b", "bolus"),
]


def corrigir(texto, extras=()):
    for padrao, novo in list(CORRECOES) + [tuple(x) for x in extras]:
        texto = re.sub(padrao, novo, texto)
    return texto


NOMES_PROPRIOS = {"Neuramis", "Revanesse", "Rai", "Raina", "Rainá", "João", "Pithon"}


def limpar(texto):
    texto = texto.replace("{", "(").replace("}", ")")
    texto = re.sub(r" -(\w)", r"-\1", texto)          # "ponto -chave" -> "ponto-chave"
    texto = re.sub(r"(\d) ,(\d)", r"\1,\2", texto)     # "1 ,2 mL" -> "1,2 mL"
    texto = texto.rstrip(".,;")
    primeira = texto.split(" ", 1)[0].strip(",.?!")
    if primeira in NOMES_PROPRIOS or (len(primeira) > 1 and primeira.isupper()):
        return texto
    return texto[:1].lower() + texto[1:]


def gerar_ass(v, palavras, duracao, caminho):
    linhas = [ass_header()]
    titulo = quebrar_titulo(v["titulo"])
    if v.get("parte"):
        titulo += rf"\N{{\fs{int(TITULO_TAM * 0.62)}}}Parte {v['parte']}"
    linhas.append(f"Dialogue: 1,{ts(0)},{ts(TITULO_DUR)},Titulo,,0,0,0,,{{\\fad(0,250)}}{titulo}\n")
    fim_legendas = duracao
    if v.get("cartela_final"):
        ini = duracao - CARTELA_DUR
        fim_legendas = ini
        linhas.append(f"Dialogue: 1,{ts(ini)},{ts(duracao)},Titulo,,0,0,0,,{{\\fad(250,0)}}{quebrar_titulo(v['cartela_final'])}\n")
    blocos = blocos_legenda(palavras)
    for i, bloco in enumerate(blocos):
        s, e = bloco[0]["s"], bloco[-1]["e"] + 0.15
        if i + 1 < len(blocos):          # nunca duas legendas ao mesmo tempo
            e = min(e, blocos[i + 1][0]["s"])
        # como na referência, a legenda só entra depois que o título sai
        s = max(s, TITULO_DUR)
        if s >= e or s >= fim_legendas:
            continue
        e = min(e, fim_legendas)
        texto = quebrar_linhas(limpar(corrigir(" ".join(p["w"] for p in bloco), v.get("correcoes", ()))))
        linhas.append(f"Dialogue: 0,{ts(s)},{ts(e)},Legenda,,0,0,0,,{texto}\n")
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def renderizar(cfg, v):
    ff = cfg["ffmpeg"]
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    if "legendas" in v:          # palavras já revisadas manualmente
        palavras = v["legendas"]
    else:
        palavras = [w for seg in trans for w in seg["words"]]
    # trechos sem fala real (ruído que a transcrição "inventou"), em segundos do bruto
    for a, b in v.get("remover_legenda", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    palavras, duracao = remapear_palavras(palavras, v["manter"])
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    gerar_ass(v, palavras, duracao, ass)

    partes, rotulos = [], []
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                      f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        rotulos.append(f"[v{i}][a{i}]")
    n = len(v["manter"])
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filtro = (";".join(partes) + ";" + "".join(rotulos) + f"concat=n={n}:v=1:a=1[vc][ac];"
              f"[vc]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
              f"ass='{esc}':fontsdir='{cfg['fontsdir']}'[vo]")
    cmd = [ff, "-y", "-v", "error", "-i", v["entrada"], "-filter_complex", filtro,
           "-map", "[vo]", "-map", "[ac]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return duracao


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    so = sys.argv[2:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = renderizar(cfg, v)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
