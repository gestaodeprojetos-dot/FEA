#!/usr/bin/env python3
"""FEA: edição automática de vídeos verticais (Reels) no padrão da equipe.

Uso:
    python3 fea_editar_video.py projeto.json [--previa | --entrega]
    python3 fea_editar_video.py projeto.json --exportar-legendas PASTA   # legendas PT com tempo, para traduzir

Espanhol (skill fea-edicao-reels-es): "idioma": "es" no projeto ou no vídeo. Com
"legendas_es" (arquivo gerado por --exportar-legendas e traduzido), a legenda de cada
bloco sai em espanhol no mesmo tempo da fala em português; sem "legendas_es", o áudio
já é em espanhol e a legenda vem da própria transcrição (com CORRECCIONES_ES).

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
      "titulo_tam": null,                       # tamanho do título (padrão TITULO_TAM), também aceito no projeto
      "manter": [[0.0, 12.4], [15.1, 40.0, "exato"]],  # trechos mantidos (s do bruto); "exato" = não encaixar
      "cartela_final": null,                    # ex.: "Parte 2 no perfil"
      "cta": null,                              # ex.: "raw/CTA.MOV", vídeo colado no final (sem legenda)
      "espelhar": false,                        # true: desfaz o espelhamento da câmera frontal
      "limpar_audio": null,                     # modelo RNNoise (ex.: "rnn/sh.rnnn"), também aceito no projeto
      "idioma": "pt",                           # "es": legenda e título em espanhol (também aceito no projeto)
      "legendas_es": null                       # ex.: "es/1- Planificación.json" (tradução bloco a bloco)
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

TITULO_TAM_PADRAO = 116  # medido na referência da Keila (24/09): ExtraBold; lotes de anúncio usam 140 ("titulo_tam")
TITULO_TAM = TITULO_TAM_PADRAO   # tamanho em uso no vídeo atual (renderizar ajusta)
TITULO_DUR = 3.0
FONTSDIR = "fonts"
TITULO_REDUCAO_MAX = 140 / 125   # aceita reduzir a fonte até ~89% antes de quebrar em mais uma linha
TITULO_LARGURA_MAX = 1040  # px úteis na largura (1080 menos margens)
TITULO_ENTRELINHA = 0.78  # linhas bem próximas, igual à referência (medido em pixels)
LEGENDA_TAM = 56       # ajuste 24/09: legenda maior, igual à referência da Keila
LEGENDA_Y = 1540       # centro da legenda (~80% da altura)
CARTELA_DUR = 3.0
MAX_CHARS_LINHA = 22
MAX_PALAVRAS_BLOCO = 10
ENTRELINHA_LEGENDA = 0.80  # medido na referência de legenda
PAUSA_QUEBRA = 0.45    # pausa (s) que força novo bloco de legenda
MAX_CHARS_LINHA_ES = 24  # o espanhol corre 10% a 20% mais longo: 2 linhas de até 24 (26 no limite)
FIXO = "\u00a7"        # marca provisória de espaço que não quebra ("70 %", "0,2 mL", "Dr. João")


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
Style: Titulo,Montserrat ExtraBold,{TITULO_TAM},&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,4,1,5,80,80,0,1
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
    # palavra curta sozinha ("tá", "ali") pisca na tela: junta com a frase vizinha
    juntos = []
    for i, b in enumerate(blocos):
        if len(b) == 1 and len(b[0]["w"].strip(".,?!")) <= 5:
            # fim de frase ("face.") volta para a frase anterior, nunca abre a seguinte
            if b[0]["w"].strip()[-1:] in ".?!" and juntos and b[0]["s"] - juntos[-1][-1]["e"] < 1.0:
                juntos[-1].append(b[0])
                if len(" ".join(x["w"] for x in juntos[-1])) > MAX_CHARS_LINHA * 2 and len(juntos[-1]) > 3:
                    # ficou longo demais para 2 linhas: parte em duas legendas equilibradas
                    ws = juntos.pop()
                    tam = [len(" ".join(x["w"] for x in ws[:k])) for k in range(1, len(ws))]
                    k = min(range(1, len(ws)), key=lambda k: abs(2 * tam[k - 1] - tam[-1]))
                    juntos += [ws[:k], ws[k:]]
                continue
            prox = blocos[i + 1] if i + 1 < len(blocos) else None
            if prox and prox[0]["s"] - b[0]["e"] < 1.0:
                prox.insert(0, b[0])
                continue
            # conectivo sozinho ("E", "Que", "Vou") que ficaria pendurado no fim da frase anterior: sai
            if re.sub(r"[^\w]", "", b[0]["w"]).lower() in LIGACAO | {"vou", "é", "eu", "então"}:
                continue
            if juntos and b[0]["s"] - juntos[-1][-1]["e"] < 1.0:
                juntos[-1].append(b[0])
                continue
        juntos.append(b)
    return juntos


def quebrar_linhas(texto, limite=MAX_CHARS_LINHA, evitar=()):
    if len(texto) <= limite:
        return texto
    palavras = texto.split(" ")
    melhor, dif = texto, 10 ** 9
    for i in range(1, len(palavras)):
        l1, l2 = " ".join(palavras[:i]), " ".join(palavras[i:])
        d = abs(len(l1) - len(l2)) + (0 if len(l1) <= len(l2) + 4 else 3)
        d += 12 if palavras[i - 1].lower() in evitar else 0   # linha terminando em "del", "la"...
        d += 40 * (len(l1) > limite + 2) + 40 * (len(l2) > limite + 2)   # linha maior que o limite
        if d < dif:
            melhor, dif = l1 + r"\N" + l2, d
    return melhor


def quebrar_linhas_es(texto):
    """Legenda em espanhol: número e unidade, "Dr. João" e marca de duas palavras nunca
    ficam em linhas diferentes; a linha não termina em artigo ou preposição."""
    t = re.sub(r"(\d) (%|mL|U|G|mm|cm|ml)\b", rf"\1{FIXO}\2", texto)
    t = re.sub(r"(\d) (%)", rf"\1{FIXO}\2", t)
    t = re.sub(r"\b(Dr\.|Dra\.) (\w+)", rf"\1{FIXO}\2", t)
    for termo in MARCAS_DUAS_PALAVRAS:
        t = t.replace(termo, termo.replace(" ", FIXO))
    return quebrar_linhas(t, MAX_CHARS_LINHA_ES, LIGACAO_ES).replace(FIXO, "\u00a0")


def largura_titulo(linha, tam=None):
    tam = tam or TITULO_TAM
    try:
        from PIL import ImageFont
        return ImageFont.truetype(f"{FONTSDIR}/Montserrat-ExtraBold.ttf", tam).getlength(linha) + 10
    except (ImportError, OSError):
        return len(linha) * tam * 0.62


def quebrar_titulo(texto, max_linhas=3, dois_pontos=True):
    """Título em no máximo 3 linhas (regra da Keila, 26/09/2026), pela largura real da Montserrat ExtraBold:
    usa o menor número de linhas que cabe no tamanho padrão e, se não couber em 3, diminui a fonte;
    nunca separa "Black Friday"."""
    if r"\N" in texto:
        return texto
    if dois_pontos and ": " in texto and max_linhas > 1:   # tenta quebrar depois dos dois-pontos
        cabeca, resto = texto.split(": ", 1)
        com_pausa = cabeca + ":" + r"\N" + quebrar_titulo(resto, max_linhas - 1)
        sem_pausa = quebrar_titulo(texto, max_linhas, dois_pontos=False)
        # fica com a quebra que deixa a letra maior
        return max((sem_pausa, com_pausa), key=lambda t: tamanho_titulo(t.split(r"\N")))
    texto = re.sub(r"\b(\d{1,2}) de (\w+)", r"\1§de§\2", texto)   # datas inteiras
    texto = re.sub(r"\b(\d+) (mil|mL)\b", r"\1§\2", texto)          # "300 mil" nunca se separa
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
        # aceita reduzir a fonte até ~89% antes de criar mais uma linha
        if max(map(largura_titulo, melhor)) <= TITULO_LARGURA_MAX * TITULO_REDUCAO_MAX:
            break
    return r"\N".join(melhor).replace("§", " ")


# Correções fixas de transcrição (termos técnicos e regra de escrita FEA: nunca "pra")
CORRECOES = [
    (r"\bpra\b", "para"), (r"\bPra\b", "Para"),
    (r"\bpros\b", "para os"), (r"\bpro\b", "para o"),
    (r"\bcarpulha\b", "carpule"),
    (r"\b[Pp]r[ée]dio\b", "pré-jowl"),     # termo do Dr. (confirmado pela Keila, 25/09)
    (r"\b[Gg]elinh[oa]s?\b", "G'"),
    (r"\b[Tt]ier\b", "tear"), (r"\b[Tt]ir ?tr?of+\b", "tear trough"), (r"\b[Tt]ear ?trof+\b", "tear trough"),
    (r"\bN[uú]vi[ao]\b", "Neauvia"),
    # nomes de produto conferidos na fonte oficial (Keila, 26/09: "pesquise como é escrito")
    (r"\b[QqKk]uiri?al[iy]s\b", "Kirialys"), (r"\b[Kk]irialis\b", "Kirialys"),
    (r"\b[Vv]ol(i|ai|y)me\b", "Volyme"), (r"\b[Rr]es(ch|t)ilane\b", "Restylane"), (r"\b[Ss]ub ?[Ss]kin\b", "Subskin"),
    (r"\b[aá]cido (hi)?al[uo]r[oô]nico\b", "ácido hialurônico"), (r"\b[aá]cido lor[oô]nico\b", "ácido hialurônico"),
    (r"\bacel[eê]r[oô]nico\b", "ácido hialurônico"), (r"\b(?<!hi)al[uo]r[oô]nico\b", "hialurônico"),
    (r"\bb[oó]l[ou]s\b", "bolus"), (r"\bLúvia\b", "Neauvia"),     # grafia oficial (Keila, 26/09)       # "gelinho" = G' (Keila, 26/09)
    (r"\btempra\b", "têmpora"),
    (r"\binterfacial\b", "interfascial"),
    (r"\bplanosinho\b", "planozinho"), (r"\bPlanosinho\b", "Planozinho"),
    (r"\bRevanesse quisse\b", "Revanesse Kiss"),
    (r"\bNeuramis volume\b", "Neuramis Volume"),
    (r"(\d) ?ml\b", r"\1 mL"), (r"\bml\b", "mL"),
    # cânula: calibre x comprimento (ex.: "2270", "22 70", "24-70" -> 22x70)
    (r"\b(18|2[0-7])[- /]?(38|40|50|70)\b", r"\1x\2"),
    # G linha: "G linha" -> G' ; "G duas linhas" / "G linha linha" -> G''
    (r"\b[Gg](?:ê)?[- ]?(?:duas linhas|linha linha)\b", "G''"),
    (r"\b[Gg](?:ê)?[- ]?linha\b", "G'"),
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
    (r"\b(?:Sabamais|Sabamai|Sadamai|Saba Mais|Sabar Mais|Saber Mais|Salva Mais)\b", "Saiba Mais"),
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


# Espanhol (skill fea-edicao-reels-es): grafia e convenções do glossário FEA ES
LIGACAO_ES = {"de", "del", "la", "el", "las", "los", "a", "al", "y", "e", "en", "con", "para",
              "por", "que", "un", "una", "se", "lo", "su", "sus", "o", "u", "sin"}
MARCAS_DUAS_PALAVRAS = ["Neuramis Volume", "Revanesse Kiss", "Neauvia Stimulate", "Neauvia Intense",
                        "Yvoire Contour", "Restylane Volyme", "Restylane Lift", "Perfectha Subskin",
                        "Black Friday", "João Pithon", "full face", "tear trough"]
CORRECCIONES_ES = [
    (r"(\d)\.(\d{1,2})(?!\d)", r"\1,\2"),         # decimal con coma: 0,2 (1.000 fica: milhar com ponto)
    (r"(\d)\s*%", r"\1 %"),                        # RAE: 70 %
    (r"(\d) ?ml\b", r"\1 mL"), (r"\bml\b", "mL"),
    (r"\bG ?(''|’’)", "G’’"), (r"\bG ?'(?!')", "G’"),   # apóstrofo curvo (decisão do catálogo ES)
    (r"\b(18|2[0-7]) ?[xX] ?(38|40|50|70)\b", r"\1x\2"),              # cánula 22x70
    (r"\s*[—–]\s*", ", "),                         # FEA: nunca raya/travessão
    (r"\bhialur[oô]nico\b", "hialurónico"),
    (r"\bzigom[aá]tic", "cigomátic"), (r"\blacrimal\b", "lagrimal"), (r"\bnasojugal\b", "nasoyugal"),
    (r"\bNeuramis volume\b", "Neuramis Volume"), (r"\bRevanesse kiss\b", "Revanesse Kiss"),
    (r"\bN[uú]vi[ao]\b", "Neauvia"),
]


def corregir_es(texto, extras=()):
    for padrao, novo in list(CORRECCIONES_ES) + [tuple(x) for x in extras]:
        texto = re.sub(padrao, novo, texto)
    return texto.strip(" ,")


def limpiar_es(texto):
    """Mesmo padrão visual da legenda PT: começa minúscula (salvo nome próprio ou sigla),
    sem ponto final; "¿" e "¡" ficam, e a letra depois deles também desce."""
    texto = texto.replace("{", "(").replace("}", ")").strip().rstrip(".,;")
    abre = re.match(r"^[¿¡]*", texto).group(0)
    resto = texto[len(abre):]
    primeira = resto.split(" ", 1)[0].strip(",.?!")
    if primeira in NOMES_PROPRIOS | NOMBRES_ES or (len(primeira) > 1 and primeira.isupper()):
        return texto
    return abre + resto[:1].lower() + resto[1:]


NOMBRES_ES = {"Dr", "Dr.", "Dra.", "FEA", "Restylane", "Kirialys", "Perfectha", "Juvederm", "Botox", "Pithon"}


def dialogos_linhas(camada, s, e, estilo, texto, efeito=""):
    """Legenda: uma linha de texto por evento, posicionada à mão, para controlar a entrelinha."""
    partes = texto.split(r"\N")
    base = LEGENDA_Y + 20
    h = LEGENDA_TAM * ENTRELINHA_LEGENDA
    n = len(partes)
    return [f"Dialogue: {camada},{ts(s)},{ts(e)},Legenda,,0,0,0,,"
            f"{{\\an2\\pos({W // 2},{base - (n - 1 - i) * h:.0f})}}{p}\n" for i, p in enumerate(partes)]


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
    """Tamanho da fonte do título: TITULO_TAM, reduzido só se alguma linha passar da largura."""
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


def eventos_legenda(v, palavras, fim_legendas):
    """Blocos de legenda finais (s, e, texto) na linha do tempo editada, antes da quebra de linha."""
    es_audio = idioma(v) == "es" and not v.get("legendas_es")   # áudio já em espanhol
    eventos = []
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
        # palavra de ligação sozinha na tela ("e", "o", "para") não diz nada: fica fora
        if len(bloco) == 1 and re.sub(r"[^\w]", "", bloco[0]["w"]).lower() in LIGACAO | LIGACAO_ES | {"é", "eu"}:
            continue
        bruto = " ".join(p["w"] for p in bloco)
        if es_audio:
            texto = limpiar_es(corregir_es(bruto, v.get("correcoes", ())))
        else:
            texto = limpar(corrigir(bruto, v.get("correcoes", ())))
        if e - s < max(0.2, 0.02 * len(texto)):   # rápido demais para ler (ex.: cortado pelo título)
            continue
        eventos.append((round(s, 3), round(e, 3), texto))
    return eventos


def idioma(v):
    return v.get("idioma") or "pt"


def ler_legendas_es(v, eventos):
    """Troca o texto PT de cada bloco pela tradução revisada. O arquivo guarda o PT de
    origem: se os cortes mudaram depois da tradução, o bloco não confere e o render para
    (legenda em espanhol fora de sincronia é pior que nenhuma)."""
    dados = json.load(open(v["legendas_es"], encoding="utf-8"))
    blocos = dados["legendas"] if isinstance(dados, dict) else dados
    if len(blocos) != len(eventos):
        raise SystemExit(f"{v['legendas_es']}: {len(blocos)} blocos traduzidos para {len(eventos)} "
                         "legendas no vídeo. Os cortes mudaram: exportar de novo e traduzir os blocos novos.")
    saida = []
    for b, (s, e, pt) in zip(blocos, eventos):
        if b["pt"] != pt:
            raise SystemExit(f"{v['legendas_es']} bloco {b.get('id')}: PT mudou (\"{b['pt']}\" -> \"{pt}\"). Retraduzir.")
        es = (b.get("es") or "").strip()
        if not es:
            raise SystemExit(f"{v['legendas_es']} bloco {b.get('id')}: sem tradução.")
        if es == "-":        # bloco deliberadamente sem legenda (ex.: só "né?")
            continue
        saida.append((s, e, limpiar_es(corregir_es(es, v.get("correcciones_es", ())))))
    return saida


def gerar_ass(v, palavras, duracao, caminho):
    linhas = [ass_header()]
    linhas += linhas_titulo(quebrar_titulo(v["titulo"]), 0, TITULO_DUR, "\\fad(0,250)", v.get("parte"))
    fim_legendas = duracao
    if v.get("cartela_final"):
        ini = duracao - CARTELA_DUR
        fim_legendas = ini
        linhas += linhas_titulo(quebrar_titulo(v["cartela_final"]), ini, duracao, "\\fad(250,0)")
    eventos = eventos_legenda(v, palavras, fim_legendas)
    if idioma(v) == "es":
        if v.get("legendas_es"):
            eventos = ler_legendas_es(v, eventos)
        eventos = [(s, e, quebrar_linhas_es(t)) for s, e, t in eventos]
    else:
        eventos = [(s, e, quebrar_linhas(t)) for s, e, t in eventos]
    for s, e, texto in eventos:
        linhas += dialogos_linhas(0, s, e, "Legenda", texto)
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def perfil_voz(ff, entrada, passo=0.05):
    """Volume (dB) do áudio do bruto em janelas de 50 ms e o limiar de voz:
    12 dB acima do ruído de fundo (percentil 5: em vídeo com fala contínua o percentil 20 já é voz), nunca abaixo de 38 dB."""
    import numpy as np
    pcm = subprocess.run([ff, "-nostdin", "-v", "error", "-i", entrada, "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(float)
    h = int(16000 * passo)
    n = len(a) // h
    db = 20 * np.log10(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(axis=1)) + 1)
    return db, max(38.0, float(np.percentile(db, 5)) + 12), passo


def ancorar_na_voz(palavras, db, limiar, passo):
    """Tira da legenda só a palavra solta que a transcrição inventou no silêncio (sem voz e
    isolada, a mais de 0,4 s das vizinhas) e encurta a palavra "esticada" até onde a voz
    termina. Palavra no meio da fala nunca sai: tirar deixava a legenda com buracos e
    fora de sincronia com o áudio (Keila, 26/09)."""
    saida = []
    for k, p in enumerate(palavras):
        i0, i1 = max(0, int(p["s"] / passo)), min(len(db), int(p["e"] / passo) + 1)
        voz = [i for i in range(i0, i1) if db[i] >= limiar - 6]
        ant = palavras[k - 1]["e"] if k else -9
        prox = palavras[k + 1]["s"] if k + 1 < len(palavras) else 1e9
        isolada = p["s"] - ant > 0.4 and prox - p["e"] > 0.4
        if not voz and isolada:
            continue
        e = p["e"]
        if voz and p["e"] - p["s"] > 0.8:        # esticada: termina onde a voz termina
            e = min(p["e"], (voz[-1] + 1) * passo + 0.1)
        saida.append(dict(p, e=max(e, p["s"] + 0.15)))
    return saida


def encaixar_cortes(manter, db, passo, palavras=None):
    """Leva cada ponto de corte para o respiro entre palavras, medido no áudio (o instante
    mais silencioso logo antes ou logo depois do ponto): o vídeo não termina com o início
    de outra palavra nem começa com o fim de uma (pedido da Keila, 24/09: "básico bem feito").
    Não usa o tempo das palavras da transcrição, que erra em até 0,3 s."""
    import numpy as np
    fim_bruto = len(db) * passo
    limiar = max(38.0, float(np.percentile(db, 5)) + 12)

    def em_silencio(t):
        i = int(t / passo)
        return all(db[k] < limiar for k in range(max(0, i - 1), min(len(db), i + 2)))

    def vale(t):
        # fala contínua, sem silêncio perto: o ponto mais baixo a até 150 ms (entre duas palavras)
        i0, i1 = max(0, int((t - 0.15) / passo)), min(len(db), int((t + 0.15) / passo) + 1)
        i = min(range(i0, i1), key=lambda k: (round(db[k]), abs(k * passo - t)))
        return round(i * passo + passo / 2, 3)

    def fim_da_fala(b):
        # primeiro instante de silêncio de 150 ms antes a 350 ms depois do ponto; sem silêncio, fica
        for k in range(max(0, int((b - 0.15) / passo)), min(len(db), int((b + 0.35) / passo) + 1)):
            if db[k] < limiar:
                return round(k * passo + passo / 2, 3)
        return vale(b)

    def inicio_da_fala(a):
        # último instante de silêncio de 350 ms antes a 150 ms depois do ponto; sem silêncio, fica
        for k in range(min(len(db) - 1, int((a + 0.15) / passo)), max(-1, int((a - 0.35) / passo) - 1), -1):
            if db[k] < limiar:
                return round(k * passo + passo / 2, 3)
        return vale(a)

    novo = []
    for trecho in manter:
        a, b = trecho[0], trecho[1]
        if len(trecho) > 2 and trecho[2] == "exato":   # ponto conferido à mão: não mexer
            novo.append([a, b])
            continue
        a2 = a if a < 0.3 or em_silencio(a) else inicio_da_fala(a)
        b2 = b if b > fim_bruto - 0.3 or em_silencio(b) else fim_da_fala(b)
        novo.append([a2, b2] if b2 - a2 > 0.5 else [a, b])
    return novo


def tem_audio(ff, arquivo):
    r = subprocess.run([ff, "-hide_banner", "-i", arquivo], capture_output=True, text=True)
    return "Audio:" in r.stderr


def duracao_arquivo(ff, arquivo):
    r = subprocess.run([ff, "-hide_banner", "-i", arquivo], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def preparar(cfg, v):
    """Cortes encaixados no áudio e palavras da legenda na linha do tempo editada."""
    ff = cfg["ffmpeg"]
    v = dict(v, idioma=v.get("idioma") or cfg.get("idioma"),
             correcoes=list(cfg.get("correcoes", [])) + list(v.get("correcoes", [])))   # do lote + do vídeo
    db_voz = perfil_voz(ff, v["entrada"])
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    v = dict(v, manter=encaixar_cortes(v["manter"], db_voz[0], db_voz[2],
                                       [w for seg in trans for w in seg["words"]]))
    if "legendas" in v:          # palavras já revisadas manualmente
        palavras = v["legendas"]
    else:
        palavras = []
        for seg in trans:
            for i, w in enumerate(seg["words"]):
                # pedaço sem espaço na frente (",2", "%") é continuação da palavra anterior:
                # "0" + ",2" = "0,2" e "1" + "%" = "1%" (antes o número sumia da legenda)
                if i and palavras and not w["w"].startswith(" "):
                    palavras[-1]["w"] += w["w"]
                    palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                    continue
                # termo de duas palavras nunca se divide entre legendas ("tear trough")
                if palavras and w["w"].strip().lower().startswith("trough") and palavras[-1]["w"].strip().lower() in ("tier", "tear"):
                    palavras[-1]["w"] += w["w"]
                    palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                    continue
                # palavra "esticada" sobre silêncio não fica mais de 1,2 s na tela
                palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), ini=(i == 0)))
    # trechos sem fala real (ruído que a transcrição "inventou"), em segundos do bruto
    for a, b in v.get("remover_legenda", []) + v.get("silenciar", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    # interjeição "ó" (ex.: "aqui ó") não entra na legenda (pedido da Keila, 24/09)
    palavras = [p for p in palavras if re.sub(r"[^\w]", "", p["w"]).lower() != "ó"]
    # legenda só onde há voz no áudio (pedido da Keila, 24/09: nada de palavra solta no silêncio)
    if "legendas" not in v:
        palavras = ancorar_na_voz(palavras, *db_voz)
    palavras, duracao = remapear_palavras(juntar_termos(palavras), v["manter"])
    global FONTSDIR, TITULO_TAM
    FONTSDIR = cfg["fontsdir"]
    TITULO_TAM = v.get("titulo_tam") or cfg.get("titulo_tam") or TITULO_TAM_PADRAO
    return v, palavras, duracao


def exportar_legendas(cfg, v, pasta):
    """Legendas PT finais, bloco a bloco e com tempo, para a tradução ao espanhol.
    O tradutor preenche "es"; o render confere o "pt" para não aplicar tradução velha."""
    import os
    v, palavras, duracao = preparar(cfg, v)
    fim = duracao - (CARTELA_DUR if v.get("cartela_final") else 0)
    v_pt = dict(v, idioma="pt", legendas_es=None)
    eventos = eventos_legenda(v_pt, palavras, fim)
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.basename(v["saida"]).rsplit(".", 1)[0]
    destino = os.path.join(pasta, f"{nome}.json")
    antigos = {}
    if os.path.exists(destino):      # reaproveita a tradução dos blocos que não mudaram
        for b in json.load(open(destino, encoding="utf-8")).get("legendas", []):
            antigos.setdefault(b["pt"], b.get("es", ""))
    dados = {"video": v["saida"], "titulo_pt": v.get("titulo_pt", ""), "titulo_es": v["titulo"],
             "legendas": [{"id": i + 1, "s": s, "e": e, "seg": round(e - s, 2), "pt": t,
                           "es": antigos.get(t, "")} for i, (s, e, t) in enumerate(eventos)]}
    json.dump(dados, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return destino, len(eventos)


def renderizar(cfg, v, previa=False):
    ff = cfg["ffmpeg"]
    v, palavras, duracao = preparar(cfg, v)
    import os
    os.makedirs(os.path.dirname(v["saida"]) or ".", exist_ok=True)
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    gerar_ass(v, palavras, duracao, ass)

    # "silenciar": [[a, b], ...] em segundos do bruto (conversa de fundo, gemido ou som de dor
    # no meio do procedimento). "zoom": [[a, b, fator, cx, cy], ...] aproxima o quadro no ponto
    # (cx, cy), frações da largura/altura, para não mostrar a paciente com expressão de dor.
    mudo = "".join(f",volume=0:enable='between(t,{a},{b})'" for a, b in v.get("silenciar", []))
    zooms = v.get("zoom", [])
    partes, vrot, arot = [], [], []
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:a]atrim={a}:{b}{mudo},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        arot.append(f"[a{i}]")
        cortes = sorted({a, b} | {t for z in zooms for t in z[:2] if a < t < b})
        for j, (x0, x1) in enumerate(zip(cortes, cortes[1:])):
            f = f"[0:v]trim={x0}:{x1},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
            z = next((z for z in zooms if z[0] <= x0 and x1 <= z[1]), None)
            if z:
                zw, zh = int(W / z[2]) // 2 * 2, int(H / z[2]) // 2 * 2
                zx = min(max(0, int(z[3] * W - zw / 2)), W - zw)
                zy = min(max(0, int(z[4] * H - zh / 2)), H - zh)
                f += f",crop={zw}:{zh}:{zx}:{zy},scale={W}:{H}"
            partes.append(f + f",setsar=1[v{i}_{j}]")
            vrot.append(f"[v{i}_{j}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    # espelhar: selfie gravada com a câmera frontal (texto do fundo ao contrário)
    espelho = "hflip," if v.get("espelhar") else ""
    # limpar_audio: tira o ruído de fundo (ar-condicionado, clínica) e deixa só a voz
    rnn = v.get("limpar_audio", cfg.get("limpar_audio"))
    audio = (f"[ac0]aresample=48000,highpass=f=80,arnndn=m='{rnn}':mix=0.95,afftdn=nr=10:nf=-45[ac];"
             if rnn else "[ac0]anull[ac];")
    filtro = (";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0[vc];"
              + "".join(arot) + f"concat=n={len(arot)}:v=0:a=1[ac0];" + audio +
              f"[vc]{espelho}ass='{esc}':fontsdir='{cfg['fontsdir']}'")
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
    exportar = None
    if "--exportar-legendas" in args:
        i = args.index("--exportar-legendas")
        exportar = args[i + 1]
        args = args[:i] + args[i + 2:]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        if exportar:
            destino, n = exportar_legendas(cfg, v, exportar)
            print(f"{destino}: {n} blocos", flush=True)
            continue
        d = renderizar(cfg, v, previa)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
