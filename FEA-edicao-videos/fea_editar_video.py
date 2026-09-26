#!/usr/bin/env python3
"""FEA: edição automática de vídeos verticais (Reels) no padrão da equipe.

Uso:
    python3 fea_editar_video.py projeto.json [--previa | --entrega]

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
      "cartela_final": null,                    # ex.: "Parte 2 no perfil"
      "cta": null,                              # ex.: "raw/CTA.MOV", vídeo colado no final (sem legenda)
      "espelhar": false,                        # true: desfaz o espelhamento da câmera frontal
      "limpar_audio": null                      # modelo RNNoise (ex.: "rnn/sh.rnnn"), também aceito no projeto
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
FONTSDIR = "fonts"
TITULO_TAM_MIN = 125     # menor tamanho aceito antes de quebrar em mais uma linha
TITULO_LARGURA_MAX = 1040  # px úteis na largura (1080 menos margens)
TITULO_ENTRELINHA = 0.8   # distância entre linhas do título, em múltiplos do tamanho da fonte
LEGENDA_TAM = 56       # ajuste 24/09: legenda maior, igual à referência da Keila
LEGENDA_Y = 1540       # centro da legenda (~80% da altura)
CARTELA_DUR = 3.0
MAX_CHARS_LINHA = 22
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
Style: Titulo,Montserrat ExtraBold,{TITULO_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H78000000,0,0,0,0,100,100,0,0,1,5,4,5,80,80,0,1
Style: Legenda,Montserrat Bold,{LEGENDA_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H80000000,0,0,0,0,100,100,0,0,1,3.5,2,2,90,90,{H - LEGENDA_Y - 20},1

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
                saida.append({"w": p["w"].strip(), "ini": p.get("ini", False),
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
            if (p["s"] - atual[-1]["e"] > PAUSA_QUEBRA or atual[-1]["w"][-1:] in ".?!"
                    or p.get("ini")):
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


def largura_titulo(linha, tam=None):
    tam = tam or TITULO_TAM
    try:
        from PIL import ImageFont
        return ImageFont.truetype(f"{FONTSDIR}/Montserrat-ExtraBold.ttf", tam).getlength(linha) + 10
    except (ImportError, OSError):
        return len(linha) * tam * 0.62


def quebrar_titulo(texto, max_linhas=4):
    """Título em linhas equilibradas (até 4), pela largura real da Montserrat ExtraBold:
    usa o menor número de linhas que cabe em 140 px; nunca separa "Black Friday"."""
    if r"\N" in texto:
        return texto
    if ": " in texto:   # "Anota essa data: 20 de outubro" quebra depois dos dois-pontos
        cabeca, resto = texto.split(": ", 1)
        return cabeca + ":" + r"\N" + quebrar_titulo(resto, max_linhas - 1)
    texto = re.sub(r"\b(\d{1,2}) de (\w+)", r"\1§de§\2", texto)   # datas inteiras
    palavras = texto.replace("Black Friday", "Black§Friday").split()

    def particoes(ps, k):
        if k == 1:
            yield [" ".join(ps)]
            return
        for i in range(1, len(ps) - k + 2):
            for resto in particoes(ps[i:], k - 1):
                yield [" ".join(ps[:i])] + resto

    def custo(ls):   # linha mais larga, penalizando linhas desiguais ("Em / 2026 eu fiz a")
        ws = list(map(largura_titulo, ls))
        return max(ws) + 0.5 * (max(ws) - min(ws))

    melhor = None
    for k in range(1, min(max_linhas, len(palavras)) + 1):
        melhor = min(particoes(palavras, k), key=custo)
        # aceita reduzir a fonte até ~125 px antes de criar mais uma linha
        if max(map(largura_titulo, melhor)) <= TITULO_LARGURA_MAX * TITULO_TAM / TITULO_TAM_MIN:
            break
    return r"\N".join(melhor).replace("§", " ")


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
    (r"\b[Cc]arpulli\b", "carpule"),
    (r"\bSanep\b", "SANEP"),
    (r"\bhidroxapatita\b", "hidroxiapatita"),
    (r"\btessidual\b", "tecidual"),
    (r"\bbio ?remodelador\b", "biorremodelador"),
    (r"\bsuco naso ?labial\b", "sulco nasolabial"),
    (r"\bsuco lábio mentual\b", "sulco labiomentual"),
    (r"\bácido alurônico\b", "ácido hialurônico"),
    (r"\b[Ss]?[Tt]andeltas?\b", "tan delta"),
    (r"\b[Cc]alda\b", "cauda"),
    (r"\bHumanidade\b", "Uma unidade"), (r"\bhumanidade\b", "uma unidade"),
    (r"\bletibo ?molhada\b", "Letybo molhada"),
    (r"\bletbo\b", "Letybo"),
    (r"\bsuco\b", "sulco"), (r"\blábio mentual\b", "labiomentual"),
    (r"\balurônico\b", "hialurônico"), (r"\bmanejamento\b", "planejamento"),
    (r"\bintercorrente\b", "intercorrência"), (r"(\d) %", r"\1%"), (r"\bmeio ml\b", "meio mL"),
    (r"\bVietre\b", "Vietri"), (r"\bEvoar Contour\b", "Yvoire Contour"),
    (r"\bSerintox\b", "Seryntox"),
    (r"\b(?:[Nn]uvia|Lúvia|[Nn]euvia) (?:Stimulate|Estimulate)\b", "Neauvia Stimulate"),
]


def corrigir(texto, extras=()):
    for padrao, novo in list(CORRECOES) + [tuple(x) for x in extras]:
        texto = re.sub(padrao, novo, texto)
    return texto


NOMES_PROPRIOS = {"Black", "Neuramis", "Revanesse", "Neauvia", "Letybo", "Vietri", "Yvoire", "Seryntox", "Rai", "Raina", "Rainá", "João", "Pithon"}


def limpar(texto):
    texto = texto.replace("{", "(").replace("}", ")")
    texto = re.sub(r" -(\w)", r"-\1", texto)          # "ponto -chave" -> "ponto-chave"
    texto = re.sub(r"(\d) ,(\d)", r"\1,\2", texto)     # "1 ,2 mL" -> "1,2 mL"
    texto = texto.rstrip(".,;")
    primeira = texto.split(" ", 1)[0].strip(",.?!")
    if primeira in NOMES_PROPRIOS or (len(primeira) > 1 and primeira.isupper()):
        return texto
    return texto[:1].lower() + texto[1:]


# termos de mais de uma palavra que nunca podem ser quebrados entre duas legendas
TERMOS_JUNTOS = [(r"(?i)^(saiba|saba|salva|saber|sabar)$", r"(?i)^mais\b", "Saiba Mais"),
                 (r"^Black$", r"^Friday\b", "Black Friday"),
                 (r"^Black Friday$", r"(?i)^vitalícia\b", "Black Friday Vitalícia")]


def juntar_termos(palavras):
    for re1, re2, novo in TERMOS_JUNTOS:
        saida = []
        for p in palavras:
            ant = saida[-1] if saida else None
            if ant and re.match(re1, ant["w"].strip()) and re.match(re2, p["w"].strip()):
                resto = re.sub(re2, "", p["w"].strip())
                saida[-1] = dict(ant, w=novo + resto, e=p["e"])
            else:
                saida.append(p)
        palavras = saida
    return palavras


def tamanho_titulo(linhas):
    """Tamanho da fonte do título: 140 px, reduzido só se alguma linha passar da largura."""
    maior = max(map(largura_titulo, linhas))
    return TITULO_TAM if maior <= TITULO_LARGURA_MAX else int(TITULO_TAM * TITULO_LARGURA_MAX / maior)


def linhas_titulo(texto, ini, fim, efeito, parte=None):
    """Cada linha do título em um evento próprio com \\pos: a entrelinha da Montserrat
    é muito aberta (pedido da Keila em 26/09: headline com linhas mais próximas)."""
    tam = tamanho_titulo(texto.split(r"\N"))
    linhas = [(l, tam) for l in texto.split(r"\N")]
    if parte:
        linhas.append((f"Parte {parte}", int(TITULO_TAM * 0.62)))
    alturas = [tam * TITULO_ENTRELINHA for _, tam in linhas]
    y = H / 2 - sum(alturas) / 2
    eventos = []
    for (l, tam), alt in zip(linhas, alturas):
        eventos.append(f"Dialogue: 1,{ts(ini)},{ts(fim)},Titulo,,0,0,0,,"
                       f"{{\\an5\\pos({W // 2},{y + alt / 2:.0f})\\fs{tam}{efeito}}}{l}\n")
        y += alt
    return eventos


def gerar_ass(v, palavras, duracao, caminho):
    linhas = [ass_header()]
    linhas += linhas_titulo(quebrar_titulo(v["titulo"]), 0, TITULO_DUR, "\\fad(0,250)", v.get("parte"))
    fim_legendas = duracao
    if v.get("cartela_final"):
        ini = duracao - CARTELA_DUR
        fim_legendas = ini
        linhas += linhas_titulo(quebrar_titulo(v["cartela_final"]), ini, duracao, "\\fad(250,0)")
    blocos = blocos_legenda(palavras)
    for i, bloco in enumerate(blocos):
        s, e = bloco[0]["s"], bloco[-1]["e"] + 0.15
        if i + 1 < len(blocos):          # nunca duas legendas ao mesmo tempo
            e = min(e, blocos[i + 1][0]["s"])
        # como na referência, a legenda só entra depois que o título sai; o pedaço de
        # frase falado ainda sob o título sai da legenda (evita começar em "vitalícia, para...")
        if s < TITULO_DUR:
            # corta até a última pontuação falada sob o título; sem pontuação, mostra o bloco inteiro
            sob = [j for j, p in enumerate(bloco) if p["s"] < TITULO_DUR - 0.1 and p["w"].strip()[-1:] in ",.!?"]
            if sob:
                bloco = bloco[sob[-1] + 1:]
                if len(bloco) <= 1:
                    continue
                s = bloco[0]["s"]
            s = max(s, TITULO_DUR)
        if s >= e or s >= fim_legendas:
            continue
        e = min(e, fim_legendas)
        texto = quebrar_linhas(limpar(corrigir(" ".join(p["w"] for p in bloco), v.get("correcoes", ()))))
        if e - s < max(0.2, 0.02 * len(texto)):   # rápido demais para ler (ex.: cortado pelo título)
            continue
        linhas.append(f"Dialogue: 0,{ts(s)},{ts(e)},Legenda,,0,0,0,,{texto}\n")
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def tem_audio(ff, arquivo):
    r = subprocess.run([ff, "-hide_banner", "-i", arquivo], capture_output=True, text=True)
    return "Audio:" in r.stderr


def duracao_arquivo(ff, arquivo):
    r = subprocess.run([ff, "-hide_banner", "-i", arquivo], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def renderizar(cfg, v, previa=False):
    ff = cfg["ffmpeg"]
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    if "legendas" in v:          # palavras já revisadas manualmente
        palavras = v["legendas"]
    else:
        palavras = []
        for seg in trans:
            for i, w in enumerate(seg["words"]):
                # palavra "esticada" sobre silêncio não fica mais de 1,2 s na tela
                palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), ini=(i == 0)))
    # trechos sem fala real (ruído que a transcrição "inventou"), em segundos do bruto
    for a, b in v.get("remover_legenda", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    palavras, duracao = remapear_palavras(juntar_termos(palavras), v["manter"])
    global FONTSDIR
    FONTSDIR = cfg["fontsdir"]
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
    # espelhar: selfie gravada com a câmera frontal (texto do fundo ao contrário)
    espelho = "hflip," if v.get("espelhar") else ""
    # limpar_audio: tira o ruído de fundo (ar-condicionado, clínica) e deixa só a voz
    rnn = v.get("limpar_audio", cfg.get("limpar_audio"))
    audio = (f"[ac0]aresample=48000,highpass=f=80,arnndn=m='{rnn}':mix=0.95,afftdn=nr=10:nf=-45[ac];"
             if rnn else "[ac0]anull[ac];")
    filtro = (";".join(partes) + ";" + "".join(rotulos) + f"concat=n={n}:v=1:a=1[vc][ac0];" + audio +
              f"[vc]{espelho}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
              f"ass='{esc}':fontsdir='{cfg['fontsdir']}'")
    entradas = ["-i", v["entrada"]]
    cta = v.get("cta") or cfg.get("cta")
    if cta:   # vídeo de CTA colado no final, sem título nem legenda
        entradas += ["-i", cta]
        dcta = duracao_arquivo(ff, cta)
        audio_cta = ("[1:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[ca]"
                     if tem_audio(ff, cta) else f"anullsrc=r=48000:cl=stereo,atrim=0:{dcta}[ca]")
        filtro += (f",fps=30,format=yuv420p[vm];[ac]aresample=48000,aformat=channel_layouts=stereo[am];"
                   f"[1:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                   f"fps=30,format=yuv420p,setpts=PTS-STARTPTS[cv];{audio_cta};"
                   f"[vm][am][cv][ca]concat=n=2:v=1:a=1[vo][ac2]")
        duracao += dcta
        amap = "[ac2]"
    else:
        filtro += "[vo]"
        amap = "[ac]"
    saida = v["saida"]
    if previa == "entrega":   # 1080p H.264 abaixo de 30 MB (nunca HEVC: abre com tela preta)
        vb = int(min(8000, 26.5 * 8 * 1024 * 1024 / 1000 / duracao - 96))
        codec = ["-map", "[vo]", "-map", amap, "-c:v", "libx264", "-preset", "medium",
                 "-b:v", f"{vb}k", "-maxrate", f"{vb * 3 // 2}k", "-bufsize", f"{vb * 2}k",
                 "-profile:v", "high", "-c:a", "aac", "-b:a", "96k"]
    elif previa:   # cabe no limite de 30 MB para envio na conversa
        vb = int(min(4000, 26 * 8 * 1000 / duracao - 96))
        filtro += ";[vo]scale=720:1280[vp]"
        codec = ["-map", "[vp]", "-map", amap, "-c:v", "libx264", "-preset", "fast",
                 "-b:v", f"{vb}k", "-maxrate", f"{vb * 3 // 2}k", "-bufsize", f"{vb * 2}k",
                 "-c:a", "aac", "-b:a", "96k"]
        pasta, nome = saida.rsplit("/", 1)
        saida = f"{pasta}/PREVIA {nome}"
    else:
        codec = ["-map", "[vo]", "-map", amap, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", filtro, *codec,
           "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    return duracao


def main():
    args = sys.argv[1:]
    previa = "entrega" if "--entrega" in args else ("--previa" in args)
    args = [a for a in args if a not in ("--previa", "--entrega")]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = renderizar(cfg, v, previa)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
