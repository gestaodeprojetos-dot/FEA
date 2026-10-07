#!/usr/bin/env python3
"""FEA: edição automática de vídeos verticais (Reels) no padrão da equipe.

Uso:
    python3 fea_editar_video.py projeto.json [--previa | --entrega | --so-legenda] [trecho_do_nome ...]

--so-legenda gera só o .ass (rápido), para ler e conferir o texto antes do render.

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
      "manter": [[0.0, 12.4], [15.1, 40.0, "exato"]],  # trechos mantidos (s do bruto); "exato" = não encaixar
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

TITULO_TAM = 116       # medido na referência da Keila (24/09): ExtraBold, ~2/3 da largura
TITULO_DUR = 3.0
LEGENDA_TAM = 56       # ajuste 24/09: legenda maior, igual à referência da Keila
LEGENDA_Y = 1540       # centro da legenda (~80% da altura)
CARTELA_DUR = 3.0
MAX_CHARS_LINHA = 22
MAX_PALAVRAS_BLOCO = 10
ENTRELINHA_TITULO = 0.78   # linhas bem próximas, igual à referência (medido em pixels)
ENTRELINHA_LEGENDA = 0.80  # idem, medido na referência de legenda
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
            prox = blocos[i + 1] if i + 1 < len(blocos) else None
            # fim de frase ("pura.", "fez?") volta para a frase dele, não vai para a próxima
            # (antes saía "fez? Bem diferente", juntando a pergunta do Dr. com a resposta da paciente)
            if b[0]["w"].strip()[-1:] in ".?!" and juntos and b[0]["s"] - juntos[-1][-1]["e"] < 1.0 \
                    and not b[0].get("ini"):
                juntos[-1].append(b[0])
                continue
            # fala inteira de uma palavra ("Doeu?", a resposta "Não." da paciente) fica sozinha na
            # tela: juntar misturava a fala do Dr. com a do paciente (Keila, 02/10/2026)
            if b[0].get("ini") and b[0]["w"].strip()[-1:] in ".?!":
                juntos.append(b)
                continue
            if prox and prox[0]["s"] - b[0]["e"] < 1.0:
                prox.insert(0, b[0])
                continue
            # conectivo sozinho ("E", "Que", "Uma"): vai para a frase seguinte se ela vem logo
            # ("vou usar o que? uma unidade" saía só "unidade"); senão, sai
            if re.sub(r"[^\w]", "", b[0]["w"]).lower() in LIGACAO | {"vou", "é", "eu", "então"}:
                if prox and prox[0]["s"] - b[0]["e"] < 3.0:
                    prox.insert(0, b[0])
                continue
            if juntos and b[0]["s"] - juntos[-1][-1]["e"] < 1.0:
                juntos[-1].append(b[0])
                continue
        juntos.append(b)
    return juntos


def quebrar_linhas(texto):
    if len(texto) <= MAX_CHARS_LINHA:
        return texto
    palavras = texto.split()
    melhor, dif = texto, 10 ** 9
    for i in range(1, len(palavras)):
        # quantidade nunca quebra de linha no meio ("2" numa linha e "mL" na outra)
        if eh_unidade(palavras[i]) and eh_numero(palavras[i - 1]) or \
                palavras[i].strip(",").lower() in ("e", "vírgula", "meio", "meia") and eh_numero(palavras[i - 1]) or \
                eh_numero(palavras[i]) and palavras[i - 1].lower() in ("e", "vírgula") and i > 1 and eh_numero(palavras[i - 2]):
            continue
        l1, l2 = " ".join(palavras[:i]), " ".join(palavras[i:])
        d = abs(len(l1) - len(l2)) + (0 if len(l1) <= len(l2) + 4 else 3)
        # linha não termina em preposição ou artigo ("1,2 mL de / lidocaína")
        d += 8 if re.sub(r"[^\w]", "", palavras[i - 1]).lower() in LIGACAO else 0
        if d < dif:
            melhor, dif = l1 + r"\N" + l2, d
    return melhor


ABREVIACOES_TITULO = [
    (r"\bPreenchimento\b", "Preench."),
    (r"\bAplicação\b", "Aplic."),
    (r"\bReavaliação\b", "Reaval."),
    (r"\bComplicação\b", "Complic."),
    (r"\bPlanejamento\b", "Planej."),
    (r"\bBioestimulador\b", "Bioestim."),
    (r"\bRinomodelação\b", "Rinomod."),
    (r"\bHarmonização\b", "Harmon."),
    (r"\bResultado\b", "Result."),
    (r"\bTécnica\b", "Técn."),
    (r" e resultado\b", " e result."),
    (r" avançad[ao]\b", " avanç."),
    (r" de toxina botulínica\b", " de toxina"),
    (r" botulínica\b", " botulín."),
    (r" do efeito ", " efeito "),
    (r" em região de ", " em "),
    (r" para não deixar ", " sem "),
    (r" sem perder ", " mantendo "),
    (r"Como fica o resultado da? ", "Result. "),
]


def condensar_titulo(texto, limite_chars=22):
    """Encurta títulos longos por abreviação progressiva, sem perder o sentido clínico.
    Retorna o título condensado e True se houve mudança."""
    if r"\N" in texto:
        linhas = texto.split(r"\N")
        if all(len(l) <= limite_chars for l in linhas):
            return texto, False
    elif len(texto) <= limite_chars * 2:
        return texto, False
    # título da imagem tem que sair exato: só abrevia se nem em 3 linhas couber
    # ("Técnica anestésica para o mento e comissura labial" saía "Técn. anestésica...")
    if all(len(l) <= limite_chars + 3 for l in quebrar_titulo(texto, limite_chars).split(r"\N")) \
            and quebrar_titulo(texto, limite_chars).count(r"\N") <= 2:
        return texto, False

    original = texto
    for rx, sub in ABREVIACOES_TITULO:
        texto = re.sub(rx, sub, texto)
        palavras = texto.split()
        quebrado = quebrar_titulo(texto, limite_chars)
        linhas = quebrado.split(r"\N")
        if all(len(l.strip()) <= limite_chars for l in linhas) and len(linhas) <= 2:
            break
    return texto, texto != original


def quebrar_titulo(texto, limite=22):
    """Título em linhas equilibradas: 2 linhas (como na referência) sempre que passar de 14
    caracteres, até ~22 por linha; 3 linhas só se não couber."""
    if r"\N" in texto:
        return texto
    palavras = texto.split()
    melhor = None
    for k in range(1 if len(texto) <= 14 else 2, 4):
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
    (r"(\d) ?ml\b", r"\1 mL"), (r"\bml\b", "mL"), (r"(\d) ?mg\b", r"\1 mg"),
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
    (r"\bVietre\b", "Vietri"), (r"\b[Ee]voar Contour\b", "Yvoire Contour"),
    (r"\bSerintox\b", "Seryntox"),
    (r"\b(?:[Nn]uvia|Lúvia|[Nn]euvia) (?:Stimulate|Estimulate)\b", "Neauvia Stimulate"),
    (r"\b[Ss]w[ea]l+ing ?f[aá]ct?or\b", "swelling factor"),
    (r"\bsubi?mento\b", "submento"),
    (r"\b[Nn]euramiz\b", "Neuramis"),
    (r"\b[Ee] ?voar\b", "Yvoire"), (r"\bcom ?o? ?tour\b", "Contour"),
    (r"\bmeomodular\b", "miomodular"),
    # Whisper confunde "lábio" com "lado" em contexto labial (sons parecidos em fala rápida)
    (r"\blado inferior\b", "lábio inferior"), (r"\blado superior\b", "lábio superior"),
    (r"\bpoli[- ]?[lL][- ]?l[aá]tico\b", "poli-L-lático"),
    (r"\bpoli ?l[aá]tico\b", "poli-L-lático"),
    (r"\bpolil[aá]tico\b", "poli-L-lático"),
    # Keila 02/10: pertuito (nunca "hipertuito"), picadinha (nunca "picadinho"),
    # parestesia→anestesia (Whisper confunde), descimento→desse mento
    # lote de outubro (02/10/2026): variantes que o Whisper inventou nos casos de toxina e preenchimento
    (r"\b[Ll]etibona\b", "Letybo na"), (r"\b[Ll]et[ií]?b(?:ol|ô|on|o)\b", "Letybo"), (r"\b[Ll]et[ií]bo\b", "Letybo"),
    (r"\b[Pp]r[óo]s?cero\b", "prócero"), (r"\b[Ll]etipo\b", "Letybo"),
    (r"\b[Cc]orrogador(es)?\b", r"corrugador\1"),
    (r"\b[Pp]r[eé][- ]?jo(?:w|y|u)l?\b", "pré-jowl"), (r"\b(?<!pré-)jaw\b", "jowl"),
    (r"\b[Bb]odoguinho\b", "buldoguinho"),
    (r"\b[Aa]fecta\b", "Perfectha"), (r"\b[Pp]erfecta\b", "Perfectha"),
    (r"\b[Ii]vo[aá]r\b", "Yvoire"),
    (r"\bauto ?gelinh[ao]\b", "alto G'"),
    (r"\b[aá]cido (?:hi)?(?:acil|acel|al|l)[uoeé]r[oô]nico\b", "ácido hialurônico"),
    (r"\b(?:acil|acel)[uoeé]r[oô]nico\b", "ácido hialurônico"),
    (r"\b[Ww]i-?[Ff]i(zinho)?\b", r"Wi-Fi\1"), (r"\b[Nn]efertit[ei]\b", "Nefertiti"),
    (r"\b[Ll]etbo\b", "Letybo"),
    # lote 07/10/2026 ("4 unidades de letboa", "dilete boa")
    (r"\b[Ll]etboa\b", "Letybo"), (r"\bdilete ?boa\b", "de Letybo"),
    (r"\b[Ff]ace do (músculo )?frontal\b", r"fáscia do \1frontal"),
    (r"\b(?:[Hh]ip|[Pp]i)tose\b", "ptose"), (r"\b[Hh]iptose\b", "ptose"),
    # Biofils: marca de fios (Keila, 03/10/2026); o Whisper ouve "biofios"
    (r"\b[Bb]io ?f[ií](?:l|o)s\b", "Biofils"), (r"\b[Bb]io ?fil\b", "Biofils"),
    (r"\bintroral\b", "intraoral"), (r"\bintroorais\b", "intraorais"),
    (r"\bFicadinha\b", "Picadinha"), (r"\bficadinha\b", "picadinha"),
    # (antes "hipertuitos?" virava sempre "pertuitos": o singular saía no plural)
    (r"\b[Hh]iper ?tu[ií]to(s?)\b", r"pertuito\1"), (r"\bpertu[ií]to(s?)\b", r"pertuito\1"),
    (r"\bpicadinho(s?)\b", r"picadinha\1"), (r"\bPicadinho(s?)\b", r"Picadinha\1"),
    # "parestesia" NÃO vira anestesia sempre: "sem nenhum paciente com parestesia" é o termo certo
    # (complicação neural). Só quando o contexto é a anestesia em si ("como foi a parestesia?"),
    # caso a caso, em "correcoes" do vídeo (Keila pediu em 02/10; conferir o contexto).
    (r"\b([Cc]omo (?:foi|ficou|está|tá) a) parestesia\b", r"\1 anestesia"),
    (r"\bdescimento\b", "desse mento"),
]


NUMEROS = {"um": "1", "dois": "2", "três": "3", "tres": "3", "quatro": "4", "cinco": "5", "seis": "6",
           "sete": "7", "oito": "8", "nove": "9", "dez": "10", "onze": "11", "doze": "12"}


def numerar_enumeracao(palavras):
    """Enumeração com número por extenso misturado a algarismo ("1, 2, 3, quatro, cinco, seis":
    a 2ª passada da transcrição devolve por extenso) vira toda em algarismo, para a legenda
    mostrar todos os números iguais (Keila, 02/10/2026: pertuito 1 a 6)."""
    def chave(w):
        return re.sub(r"[^\w]", "", w).lower()

    def eh_num(w):
        return chave(w).isdigit()
    mudou = True
    while mudou:
        mudou = False
        for i, p in enumerate(palavras):
            k = chave(p["w"])
            if k not in NUMEROS:
                continue
            ant = palavras[i - 1] if i and p["s"] - palavras[i - 1]["e"] < 4.0 else None
            prox = palavras[i + 1] if i + 1 < len(palavras) and palavras[i + 1]["s"] - p["e"] < 4.0 else None
            # só dentro da lista: "3, quatro" ou "quatro, 5" (nunca "seis. Um paciente...")
            def em_lista(x):   # vizinho que é número (algarismo ou por extenso) separado por vírgula
                return x and (eh_num(x["w"]) or chave(x["w"]) in NUMEROS)
            if (ant and eh_num(ant["w"]) and ant["w"].strip().endswith(",")) or \
                    (prox and eh_num(prox["w"]) and p["w"].strip().endswith(",")) or \
                    (em_lista(ant) and ant["w"].strip().endswith(",") and em_lista(prox)
                     and p["w"].strip().endswith(",")):
                m = re.match(r"^(\s*)(\w+)(.*)$", p["w"])
                p["w"] = m.group(1) + NUMEROS[k] + m.group(3)
                mudou = True
    return palavras


# Quantidade = número + unidade ("2 mL", "meio mL", "1,5 mL", "1 e meio mL", "duas unidades", "20 mg",
# "1%"). Nunca se separa na legenda (Keila, 05/10/2026, pasta 2 vídeo 2: o "2" entrava antes de o Dr.
# falar, no fim do bloco anterior, e quando ele falava aparecia só "mL"). O Whisper dá ao número um
# tempo adiantado; a unidade e a voz medida no áudio é que dizem quando a quantidade é falada.
NUM_EXTENSO = set(NUMEROS) | {"uma", "duas", "meio", "meia", "zero", "treze", "quatorze", "catorze", "quinze",
                              "dezesseis", "dezessete", "dezoito", "dezenove", "vinte", "trinta", "quarenta",
                              "cinquenta", "cem", "cento", "duzentos", "duzentas"}
UNIDADE_RX = re.compile(r"^(?:m[lL]|mL|ML|mg|mgs|U|UI|ui|%|cm|mm|mililitros?|miligramas?|unidades?|"
                        r"centímetros?|milímetros?|seringas?|ampolas?)$")


def _chave_qtd(w):
    return re.sub(r"[^\w,%]", "", w).strip(",").lower() if w.strip() != "%" else "%"


def eh_numero(w):
    k = _chave_qtd(w)
    return bool(re.fullmatch(r"\d+(?:[.,]\d+)?%?", k)) or k in NUM_EXTENSO


def eh_unidade(w):
    k = re.sub(r"[^\w%]", "", w)
    return bool(UNIDADE_RX.match(k)) or bool(UNIDADE_RX.match(k.lower()))


def juntar_quantidades(palavras, db=None, limiar=None, passo=0.05):
    """Junta número e unidade num item só ("2" + "mL" = "2 mL", "1" + "e" + "meio" + "mL"), com o
    início ancorado no tempo real da fala: quando o número vem colado na unidade na transcrição, vale
    o tempo do número; quando vem descolado (tempo adiantado do Whisper), o início é a voz medida no
    áudio logo antes da unidade, no máximo o tempo de falar o número."""
    saida, i = [], 0
    while i < len(palavras):
        p = palavras[i]
        if not eh_numero(p["w"]):
            saida.append(p)
            i += 1
            continue
        j = i
        # "1 e meio", "um vírgula cinco", "0 ,2"
        while j + 2 < len(palavras) and _chave_qtd(palavras[j + 1]["w"]) in ("e", "vírgula", "virgula") \
                and eh_numero(palavras[j + 2]["w"]) and palavras[j + 2]["s"] - palavras[j]["e"] < 1.0:
            j += 2
        u = j + 1
        # número sem voz no próprio tempo (Whisper adiantou ou esticou: "3" em 45,3 s e "unidades" em
        # 49,4 s, fala real "3 unidades" em 49,2 s; lote de 07/10/2026) aceita a unidade até 6 s depois
        folga = 2.5
        if db is not None and u < len(palavras):
            k0, k1 = int(p["s"] / passo), max(int(p["s"] / passo) + 1, int(palavras[j]["e"] / passo))
            if k1 <= len(db) and sum(db[x] >= limiar for x in range(k0, k1)) < 0.3 * (k1 - k0):
                folga = 6.0
        if u >= len(palavras) or not eh_unidade(palavras[u]["w"]) or palavras[u]["s"] - palavras[j]["e"] > folga:
            saida.append(p)
            i += 1
            continue
        fim = u
        # "2 mL e meio"
        if fim + 2 < len(palavras) and _chave_qtd(palavras[fim + 1]["w"]) == "e" \
                and _chave_qtd(palavras[fim + 2]["w"]) in ("meio", "meia") and palavras[fim + 2]["s"] - palavras[fim]["e"] < 0.8:
            fim += 2
        grupo = palavras[i:fim + 1]
        un = palavras[u]
        texto = " ".join(re.sub(r"[.?!]+$", "", g["w"].strip()) if k < len(grupo) - 1 else g["w"].strip()
                         for k, g in enumerate(grupo))
        # tempo de falar o número: "dois" ~0,4 s; "zero vírgula três" ~0,85 s
        dur_num = 0.0
        for g in palavras[i:u]:
            k = _chave_qtd(g["w"])
            dur_num += 0.15 if k in ("e", "vírgula", "virgula") else \
                0.4 + 0.45 * len(re.findall(r"[.,]\d", k)) + 0.1 * max(0, len(re.sub(r"\D", "", k)) - 2)
        dur_num = min(1.4, dur_num)
        ant_e = saida[-1]["e"] if saida else -9.0
        s = p["s"]
        if un["s"] - palavras[j]["e"] > 0.25 or un["s"] - p["s"] > dur_num + 0.6:
            # número descolado da unidade (tempo adiantado ou esticado pelo Whisper): o início é
            # a voz que volta depois do último silêncio antes da unidade
            s = un["s"] - dur_num
            if db is not None:
                k1 = int(un["s"] / passo)
                k0 = max(0, int((un["s"] - dur_num - 0.3) / passo))
                mudo = [x for x in range(k0, k1) if db[x] < limiar - 6]
                ult = None
                for x in mudo:
                    if x + 1 < k1 and x - 2 >= 0 and all(db[y] < limiar - 6 for y in range(x - 2, x + 1)):
                        ult = x
                if ult is not None:
                    s = (ult + 1) * passo - 0.05
            s = max(s, ant_e)
        novo = dict(p, w=(" " if p["w"].startswith(" ") else "") + texto, s=min(s, un["s"]),
                    e=grupo[-1]["e"], e0=grupo[-1].get("e0", grupo[-1]["e"]), ini=p.get("ini", False),
                    qtd=True)
        saida.append(novo)
        i = fim + 1
    return saida


def corrigir(texto, extras=()):
    for padrao, novo in list(CORRECOES) + [tuple(x) for x in extras]:
        texto = re.sub(padrao, novo, texto)
    return texto


def pontuar(texto):
    """Insere vírgulas em posições comuns do português falado onde o Whisper omite."""
    # antes de conjunções adversativas e explicativas (só se não há pontuação antes)
    texto = re.sub(r"(\w) (mas|porém|portanto|entretanto) ", r"\1, \2 ", texto)
    # antes de "porque", "pois", "então", "aí" quando precedidos de palavra (não no início)
    # (nunca depois de palavra de ligação: "acho que aí eu vou", "e então", "é porque")
    texto = re.sub(r"\b(?!(?i:que|e|é|de|do|da|o|a|os|as|por|para|se|mas|só|até|ou|nem|tipo)\b)(\w+) "
                   r"(porque|pois|então) ", r"\1, \2 ", texto)   # "aí" saiu: "vem aí com bônus" ganhava vírgula
    # antes de "né" (marcador) e de "tá"/"viu" só no fim da frase ("..., tá?"): no meio, "tá" é o
    # verbo ("a minha agulha tá de cima para baixo" ficava "agulha, tá de cima")
    texto = re.sub(r"(\w) (né)([.,?!\s]|$)", r"\1, \2\3", texto)
    texto = re.sub(r"(\w) (tá|viu)([.,?!])", r"\1, \2\3", texto)   # sem "$": "a gente ainda tá / começando"
    # evitar vírgula duplicada
    texto = re.sub(r",\s*,", ",", texto)
    return texto


NOMES_PROPRIOS = {"Neuramis", "Revanesse", "Neauvia", "Letybo", "Vietri", "Yvoire", "Seryntox", "Rai", "Raina", "Rainá", "João", "Pithon",
                  "Nefertiti", "Botox", "Volumax", "Biogelis", "Subskin", "Perfectha", "Dysport", "Kiss", "Wi", "Dani",
                  "Kirialys", "Restylane", "Biofils", "Volyme", "Contour", "Nike", "FEB", "FEA", "FEP", "FEF", "DAO", "PLA"}


def limpar(texto):
    texto = texto.replace("{", "(").replace("}", ")")
    texto = re.sub(r" -(\w)", r"-\1", texto)          # "ponto -chave" -> "ponto-chave"
    texto = re.sub(r"(\d) ,(\d)", r"\1,\2", texto)     # "1 ,2 mL" -> "1,2 mL"
    texto = texto.rstrip(".,;")
    primeira = texto.split(" ", 1)[0].strip(",.?!")
    if primeira in NOMES_PROPRIOS or primeira.split("-")[0] in NOMES_PROPRIOS or (len(primeira) > 1 and primeira.isupper()):
        return texto
    return texto[:1].lower() + texto[1:]


def dialogos_linhas(camada, s, e, estilo, texto, efeito=""):
    """Uma linha de texto por evento, posicionada à mão, para controlar a entrelinha."""
    partes = texto.split(r"\N")
    if estilo == "Titulo":
        tams = []
        for p in partes:
            m = re.match(r"\{\\fs(\d+)\}", p)
            tams.append(int(m.group(1)) if m else TITULO_TAM)
        alturas = [t * ENTRELINHA_TITULO for t in tams]
        y = H / 2 - sum(alturas) / 2
        saida = []
        for p, h in zip(partes, alturas):
            saida.append(f"Dialogue: {camada},{ts(s)},{ts(e)},Titulo,,0,0,0,,"
                         f"{{\\an5\\pos({W // 2},{y + h / 2:.0f}){efeito}}}{p}\n")
            y += h
        return saida
    base = LEGENDA_Y + 20
    h = LEGENDA_TAM * ENTRELINHA_LEGENDA
    n = len(partes)
    return [f"Dialogue: {camada},{ts(s)},{ts(e)},Legenda,,0,0,0,,"
            f"{{\\an2\\pos({W // 2},{base - (n - 1 - i) * h:.0f})}}{p}\n" for i, p in enumerate(partes)]


def juntar_texto(bloco):
    """Texto do bloco. Começo de frase no meio do bloco ganha vírgula antes e minúscula
    ("mesma coisa do outro lado Vocês veem" -> "mesma coisa do outro lado, vocês veem")."""
    partes = []
    for k, p in enumerate(bloco):
        w = p["w"].strip()
        if k and p.get("ini") and partes and partes[-1][-1:] not in ".?!" \
                and re.sub(r"[^\w]", "", partes[-1]).lower() not in LIGACAO:
            if partes[-1][-1:] not in ",;:":
                partes[-1] += ","
            chave = re.sub(r"[^\w]", "", w)
            if w[:1].isupper() and chave not in NOMES_PROPRIOS and not (len(chave) > 1 and chave.isupper()):
                w = w[:1].lower() + w[1:]
        partes.append(w)
    return " ".join(partes)


TITULO_TAM_LONGO = 100   # título da imagem que não cabe em 3 linhas: 4 linhas um pouco menores


def formatar_titulo(v):
    """Texto ASS do título. Título que veio da imagem sai EXATO (nunca abrevia): se não couber em
    3 linhas de ~22 caracteres, vai em 4 linhas com fonte 100 (Keila: título exato da imagem)."""
    texto = v["titulo"]
    if v.get("titulo_origem", "imagem") != "imagem":
        texto, mudou = condensar_titulo(texto)
        if mudou:
            print(f"  Headline condensada: \"{v['titulo']}\" → \"{texto}\"")
    titulo = quebrar_titulo(texto)
    linhas = titulo.split(r"\N")
    if len(linhas) > 3 or max(map(len, linhas)) > MAX_CHARS_LINHA + 3:
        ps = texto.split()
        def particoes(ps, k):
            if k == 1:
                yield [" ".join(ps)]
                return
            for i in range(1, len(ps) - k + 2):
                for resto in particoes(ps[i:], k - 1):
                    yield [" ".join(ps[:i])] + resto
        linhas = min(particoes(ps, 4), key=lambda ls: max(map(len, ls)))
        titulo = r"\N".join(rf"{{\fs{TITULO_TAM_LONGO}}}{l}" for l in linhas)
    if v.get("parte"):
        titulo += rf"\N{{\fs{int(TITULO_TAM * 0.62)}}}Parte {v['parte']}"
    return titulo


ANTECIPA = 0.15   # legenda entra um pouco antes da voz: entrar no instante exato já parece atrasado


def gerar_ass(v, palavras, duracao, caminho, voz=None):
    """voz = (db, limiar, passo) do áudio na linha do tempo editada: o início de cada bloco vai
    para o começo real da voz (a transcrição às vezes marca a 1ª palavra até 0,5 s depois) e a
    legenda entra ANTECIPA s antes (Keila, 05/10/2026: "legendas um pouco atrasadas")."""
    anterior = {}
    for k, p in enumerate(palavras):
        anterior[id(p)] = palavras[k - 1]["e"] if k else 0.0

    def inicio(bloco):
        s0 = bloco[0]["s"]
        if voz is not None:
            db, lim, ps = voz
            i = k = min(len(db) - 1, int(s0 / ps))
            while k > 0 and (i - k) * ps < 0.6 and any(db[j] >= lim - 3 for j in range(max(0, k - 3), k)):
                k -= 1
            if k * ps < s0 - 0.1 and k * ps >= anterior.get(id(bloco[0]), 0.0):
                s0 = k * ps
        # antecipa, mas sem tirar da tela a fala anterior antes de ela terminar
        return max(s0 - ANTECIPA, min(s0, anterior.get(id(bloco[0]), 0.0)))

    linhas = [ass_header()]
    titulo = formatar_titulo(v)
    linhas += dialogos_linhas(1, 0, TITULO_DUR, "Titulo", titulo, r"\fad(0,250)")
    fim_legendas = duracao
    if v.get("cartela_final"):
        ini = duracao - CARTELA_DUR
        # a legenda continua por baixo da cartela (posições diferentes na tela): a fala dos
        # 3 s finais da Parte 1 ficava sem legenda (Keila, 02/10/2026: toda fala legendada)
        linhas += dialogos_linhas(1, ini, duracao, "Titulo", quebrar_titulo(v["cartela_final"]), r"\fad(250,0)")
    blocos = blocos_legenda(palavras)
    carry = []
    livre = 0.0     # a legenda anterior pegou tempo emprestado: esta só entra depois
    for i, bloco in enumerate(blocos):
        if carry:
            bloco = carry + bloco
            carry = []
        if bloco[-1]["e"] <= TITULO_DUR:       # fala debaixo do título (padrão: sem legenda)
            continue
        s, e = max(inicio(bloco), TITULO_DUR, livre), bloco[-1]["e"] + 0.15
        prox = blocos[i + 1] if i + 1 < len(blocos) else None
        if prox:
            e = min(e, inicio(prox))
        if s >= fim_legendas:
            continue
        e = min(e, fim_legendas)
        # conectivo solto não aparece, mas "Uma." falado sozinho é contagem (uma unidade), fica
        if len(bloco) == 1 and re.sub(r"[^\w]", "", bloco[0]["w"]).lower() in LIGACAO | {"é", "eu"} \
                and not (bloco[0]["w"].strip()[-1:] in ".?!" and eh_numero(bloco[0]["w"])):
            continue
        texto = quebrar_linhas(limpar(pontuar(corrigir(juntar_texto(bloco), v.get("correcoes", ())))))
        minimo = max(0.2, 0.02 * len(texto), 0.45 if len(bloco) == 1 else 0)
        if e - s < minimo:
            # curta demais: vai junto com a próxima, se couber em 2 linhas; senão fica na tela o
            # mínimo para ler e a próxima entra um pouco depois (antes a palavra sumia ou o bloco
            # juntado estourava as 2 linhas: "por isso que a gente está escolhendo aqui um produto...")
            fala_inteira = len(bloco) == 1 and bloco[0].get("ini") and bloco[0]["w"].strip()[-1:] in ".?!"
            if prox and not fala_inteira and len(texto) + len(juntar_texto(prox)) + 1 <= MAX_CHARS_LINHA * 2:
                carry = [p for p in bloco if p["s"] >= TITULO_DUR - 0.3]
                continue
            e = min(s + minimo, fim_legendas)
            livre = e
        linhas += dialogos_linhas(0, s, e, "Legenda", texto)
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def perfil_voz(ff, entrada, passo=0.05, ganho_db=0):
    """Volume (dB) do áudio do bruto em janelas de 50 ms e o limiar de voz:
    12 dB acima do ruído de fundo (percentil 5: em vídeo com fala contínua o percentil 20 já é voz), nunca abaixo de 38 dB.
    ganho_db aplica boost antes da análise (para vídeos com volume_db no projeto)."""
    import numpy as np
    af = ["-vn", "-ac", "1", "-ar", "16000"]
    if ganho_db:
        af = ["-af", f"volume={ganho_db}dB"] + af
    pcm = subprocess.run([ff, "-nostdin", "-v", "error", "-i", entrada] + af +
                          ["-f", "s16le", "-"], capture_output=True, check=True).stdout
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
        # palavra esticada: procura a voz no intervalo inteiro da transcrição (e0), não só no
        # pedaço de 1,2 s: o 2º "duas" de "duas unidades, duas unidades" sumia da legenda
        i0, i1 = max(0, int(p["s"] / passo)), min(len(db), int(max(p["e"], p.get("e0", p["e"])) / passo) + 1)
        voz = [i for i in range(i0, i1) if db[i] >= limiar - 6]
        ant = palavras[k - 1]["e"] if k else -9
        prox = palavras[k + 1]["s"] if k + 1 < len(palavras) else 1e9
        isolada = p["s"] - ant > 0.25 or prox - p["e"] > 0.25
        if not voz and isolada:
            continue
        s, e = p["s"], p["e"]
        e0 = p.get("e0", e)
        if not voz and prox - p["e"] > 2.0:
            # palavra que a transcrição deixou segundos antes da frase dela, no silêncio ("Pra ...
            # gente ver melhor"): se há voz logo antes da palavra seguinte, vai para lá
            j0, j1 = int((prox - 0.7) / passo), int(prox / passo)
            if any(db[i] >= limiar for i in range(max(0, j0), min(len(db), j1))):
                d = min(0.5, p["e"] - p["s"])
                saida.append(dict(p, s=prox - 0.02 - d, e=prox - 0.02))
                continue
        if e0 - s > 1.5:
            # palavra "esticada" pela transcrição (ex.: "Pra" de 55 s a 69 s): a fala de verdade
            # fica no fim do intervalo, logo antes da palavra seguinte
            j1 = min(len(db), int(e0 / passo) + 1)
            fala = [i for i in range(max(0, int(s / passo)), j1) if db[i] >= limiar]
            if fala:
                i_s = int(s / passo)
                if fala[0] - i_s <= 3 and sum(1 for i in fala if i < i_s + 6) >= 4 and k and \
                        p["s"] - palavras[k - 1]["e"] < 0.15:
                    # fala corrida: a palavra está no começo do intervalo, colada na anterior
                    # ("de solução anestésica": "solução" entrava 2 s atrasada)
                    j = 0
                    while j + 1 < len(fala) and fala[j + 1] - fala[j] <= 2:
                        j += 1
                    e = min(e0, (fala[j] + 1) * passo + 0.05, s + 1.5)
                    saida.append(dict(p, s=s, e=max(e, s + 0.15)))
                    continue
                k2 = len(fala) - 1
                while k2 > 0 and fala[k2] - fala[k2 - 1] <= 3:
                    k2 -= 1
                s = max(fala[k2] * passo - 0.05, e0 - 1.0)
                e = min(e0, s + 1.0)
                saida.append(dict(p, s=s, e=max(e, s + 0.15)))
                continue
        if not voz:
            # palavra inteira marcada no silêncio, logo antes da fala: empurra até a voz começar
            j = next((i for i in range(i1, min(len(db), i1 + int(1.0 / passo))) if db[i] >= limiar - 6), None)
            if j is not None:
                d = j * passo - 0.05 - s
                s, e = s + d, e + d
        if voz:
            inicio = voz[0]
            for vi in range(len(voz) - 1):
                if voz[vi + 1] - voz[vi] <= 1:
                    inicio = voz[vi]
                    break
            s = max(s, inicio * passo - 0.05)
            if e - s > 0.8:
                e = min(e, (voz[-1] + 1) * passo + 0.1)
        gap = p["s"] - ant
        if gap > 0.6:
            look = max(0, int((p["s"] - min(gap, 1.0)) / passo))
            vb = [i for i in range(look, i0) if db[i] >= limiar]
            if len(vb) >= 3:
                for vi in range(len(vb) - 1):
                    if vb[vi + 1] - vb[vi] <= 1:
                        s = min(s, vb[vi] * passo - 0.05)
                        break
        saida.append(dict(p, s=s, e=max(e, s + 0.15)))
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


def renderizar(cfg, v, previa=False):
    ff = cfg["ffmpeg"]
    ganho = v.get("volume_db", 0)
    db_voz = perfil_voz(ff, v["entrada"], ganho_db=ganho)
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    v = dict(v, manter=encaixar_cortes(v["manter"], db_voz[0], db_voz[2],
                                       [w for seg in trans for w in seg["words"]]))
    if "legendas" in v:          # palavras já revisadas manualmente
        palavras = v["legendas"]
    else:
        palavras = []
        for seg in trans:
            ws = [dict(w) for w in seg["words"]]
            for i, w in enumerate(ws):
                # pedaço sem espaço na frente (",2", "%") é continuação da palavra anterior:
                # "0" + ",2" = "0,2" e "1" + "%" = "1%" (antes o número sumia da legenda)
                if i and palavras and not w["w"].startswith(" "):
                    palavras[-1]["w"] += w["w"]
                    palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                    continue
                # termo de duas palavras nunca se divide entre legendas ("tear trough", "swelling factor")
                if palavras and w["w"].strip().lower().startswith("trough") and palavras[-1]["w"].strip().lower() in ("tier", "tear"):
                    palavras[-1]["w"] += w["w"]
                    palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                    continue
                if palavras and w["w"].strip().lower().startswith("factor") and palavras[-1]["w"].strip().lower().endswith("swelling"):
                    palavras[-1]["w"] += w["w"]
                    palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                    continue
                # palavra "esticada" sobre silêncio não fica mais de 1,2 s na tela
                palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), e0=w["e"], ini=(i == 0)))
    # "mover_palavra": [[inicio_na_transcricao, inicio_certo], ...] para a palavra que a
    # transcrição pôs no lugar errado (conferido ouvindo o áudio)
    for s0, s1 in v.get("mover_palavra", []):
        for p in palavras:
            if abs(p["s"] - s0) < 0.06:
                d = min(0.5, p["e"] - p["s"])
                p.update(s=s1, e=s1 + d, e0=s1 + d)
    palavras.sort(key=lambda p: p["s"])
    palavras = numerar_enumeracao(palavras)
    # número e unidade viram um item só, antes de ancorar na voz: sozinho, o número com tempo
    # adiantado saía no fim do bloco anterior (ou sumia no silêncio) e a unidade ficava só
    if "legendas" not in v:
        palavras = juntar_quantidades(palavras, *db_voz)
    # trechos sem fala real (ruído que a transcrição "inventou"), em segundos do bruto
    for a, b in v.get("remover_legenda", []) + v.get("silenciar", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    # interjeição "ó" (ex.: "aqui ó") não entra na legenda (pedido da Keila, 24/09)
    palavras = [p for p in palavras if re.sub(r"[^\w]", "", p["w"]).lower() != "ó"]
    # legenda só onde há voz no áudio (pedido da Keila, 24/09: nada de palavra solta no silêncio)
    if "legendas" not in v:
        palavras = ancorar_na_voz(palavras, *db_voz)
    palavras, duracao = remapear_palavras(palavras, v["manter"])
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    import numpy as np
    db_ed = np.concatenate([db_voz[0][int(a / db_voz[2]):int(b / db_voz[2])] for a, b in v["manter"]])
    gerar_ass(v, palavras, duracao, ass, voz=(db_ed, db_voz[1], db_voz[2]))
    if previa == "legenda":   # só o .ass, para revisar o texto antes de renderizar
        return duracao

    # "silenciar": [[a, b], ...] em segundos do bruto (conversa de fundo, gemido ou som de dor
    # no meio do procedimento). "zoom": [[a, b, fator, cx, cy], ...] aproxima o quadro no ponto
    # (cx, cy), frações da largura/altura, para não mostrar a paciente com expressão de dor.
    mudo = "".join(f",volume=0:enable='between(t,{a},{b})'" for a, b in v.get("silenciar", []))
    ganho = f",volume={v['volume_db']}dB" if v.get("volume_db") else ""
    zooms = v.get("zoom", [])
    partes, vrot, arot = [], [], []
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:a]atrim={a}:{b}{mudo}{ganho},asetpts=PTS-STARTPTS,"
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
    filtro = (";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0[vc];"
              + "".join(arot) + f"concat=n={len(arot)}:v=0:a=1[ac];"
              f"[vc]ass='{esc}':fontsdir='{cfg['fontsdir']}'[vo]")
    saida = v["saida"]
    if previa == "entrega":   # qualidade total, sem limite de tamanho (nunca HEVC: abre com tela preta)
        codec = ["-map", "[vo]", "-map", "[ac]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    elif previa:   # cabe no limite de 30 MB para envio na conversa
        vb = int(min(4000, 26 * 8 * 1000 / duracao - 96))
        filtro += ";[vo]scale=720:1280[vp]"
        codec = ["-map", "[vp]", "-map", "[ac]", "-c:v", "libx264", "-preset", "fast",
                 "-b:v", f"{vb}k", "-maxrate", f"{vb * 3 // 2}k", "-bufsize", f"{vb * 2}k",
                 "-c:a", "aac", "-b:a", "96k"]
        pasta, nome = saida.rsplit("/", 1)
        saida = f"{pasta}/PREVIA {nome}"
    else:
        codec = ["-map", "[vo]", "-map", "[ac]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd = [ff, "-y", "-v", "error", "-i", v["entrada"], "-filter_complex", filtro, *codec,
           "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    return duracao


def main():
    args = sys.argv[1:]
    previa = ("entrega" if "--entrega" in args else "legenda" if "--so-legenda" in args
              else ("--previa" in args))
    args = [a for a in args if a not in ("--previa", "--entrega", "--so-legenda")]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = renderizar(cfg, v, previa)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
