#!/usr/bin/env python3
"""FEA: edição no estilo "opinião / mito ou verdade" (Reels do Dr. João perguntando aos alunos).

Estilo copiado da pasta de referência da Keila (out/2026, "1- Olheiras" a "4- Lábios"):
  - Título em caixas brancas com texto preto (Montserrat Bold), alinhado à esquerda, com barra
    bege ao lado; entra deslizando da esquerda com o som de arrasto (whoosh) e some aos 4,1 s.
  - Legenda branca pequena (Montserrat Bold), centralizada a ~78% da altura, desde o início.
  - Produto citado: foto do produto num quadro branco no centro, entrando com um "pop".
  - CTA falado da Black Friday: "VITALÍCIO" grande na tela e, no fim, a cartela da campanha.

Usa o mesmo projeto.json do fea_editar_video.py (entrada, transcricao, saida, titulo, manter,
remover_legenda, silenciar, correcoes...), mais:
    "titulo_linhas": ["Linha 1", "Linha 2"]       # quebra manual do título (opcional)
    "produtos": [[t_bruto, "img.png", duracao]]   # insert da foto do produto (s do bruto)
    "destaques": [[ini_bruto, fim_bruto, "VITALÍCIO"]]
    "cartela": true                               # cola a cartela da Black Friday no final
e, no nível do projeto: "whoosh" (wav do som de arrasto) e "cartela" (mp4 da cartela final).

Uso:
    python3 fea_editar_opiniao.py projeto.json [--so-legenda] [trecho_do_nome ...]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as base  # noqa: E402

W, H = 1080, 1920

# medidas tiradas em pixels da referência "3- Toxina" (quadro de 2 s)
TIT_FS = 83            # tamanho ASS (PIL 53 px: "Todas as toxinas são iguais" = 753 px)
TIT_X = 104            # borda esquerda das caixas
TIT_PAD = 20           # respiro do texto dentro da caixa
TIT_CAIXA_H = 74
TIT_PASSO = 84         # distância entre as caixas
TIT_CENTRO_Y = 1202    # centro do bloco de 2 linhas
TIT_MAX_PX = 900       # largura máxima do texto de uma linha
BARRA = (70, 89)       # barra bege à esquerda, cor (219, 208, 147)
TIT_FIM = 4.1          # o título some de uma vez aos 4,1 s
SLIDE = (0.10, 0.60)   # entrada deslizando

LEG_FS = 62            # PIL 40 px: "como a Zelman que tem" = 510 px
LEG_Y = 1500
LEG_PASSO = 48
LEG_MAX = 22

DESTAQUE_FS = 125
DESTAQUE_Y = 1200
ROT_FS, ROT_PAD, ROT_H, ROT_Y = 50, 34, 86, 190  # rótulo das ilustrações (topo da tela)

PROD_LADO = 552
PROD_CENTRO = (540, 1125)
SPLIT_TOPO = 1020          # caso clínico ocupa o topo até aqui (com o esfumado no fim)
SPLIT_ESFUMADO = 240       # altura da faixa esfumaçada entre o caso e o Dr.
SPLIT_DR_H = 1140          # faixa do vídeo do Dr. que desce para a metade de baixo (começa sob o esfumado)
SPLIT_DR_Y = 200           # de onde ela sai no quadro original (rosto e mãos)
LEG_Y_SPLIT = 1010         # na tela dividida a legenda fica na emenda (igual ao Reel de referência)
PROD_CENTRO_ALTO = 700   # durante o título (caixas em y 1120 a 1290)
PROD_DUR = 2.5

PIL_POR_ASS = 0.641    # calibrado: fonte ASS 100 = Montserrat PIL 64,1


def fonte(cfg, peso="Bold", tam=100):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(cfg["fontsdir"], f"Montserrat-{peso}.ttf"), tam)


def largura(cfg, texto, fs, peso="Bold"):
    return fonte(cfg, peso, 100).getlength(texto) * fs * PIL_POR_ASS / 100


def quebrar_titulo(cfg, texto):
    """Linhas equilibradas que caibam na largura (a referência usa 2 a 3 linhas)."""
    ps = texto.split()
    for n in range(1, 6):
        melhor = None
        def particoes(ps, k):
            if k == 1:
                yield [" ".join(ps)]
                return
            for i in range(1, len(ps) - k + 2):
                for resto in particoes(ps[i:], k - 1):
                    yield [" ".join(ps[:i])] + resto
        if n > len(ps):
            break
        for ls in particoes(ps, n):
            m = max(largura(cfg, l, TIT_FS) for l in ls)
            if m > TIT_MAX_PX:
                continue
            # linha não termina em conectivo ("iguais ou / tem" -> "iguais / ou tem", como na referência)
            m += sum(150 for l in ls[:-1] if l.split()[-1].lower().strip(",") in base.LIGACAO | {"ou", "é"})
            if melhor is None or m < melhor[0]:
                melhor = (m, ls)
        if melhor and (n > 1 or len(texto) <= 26):
            return melhor[1]
    return [texto]


def ass_header():
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Tit,Montserrat Bold,{TIT_FS},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Caixa,Montserrat Bold,20,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Leg,Montserrat Bold,{LEG_FS},&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,2,1.5,5,60,60,0,1
Style: Rot,Montserrat Bold,{ROT_FS},&H0099455B,&H0099455B,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Dest,Montserrat ExtraBold,{DESTAQUE_FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,4,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def caixa_arredondada(w, h, r):
    """Desenho ASS de um retângulo com cantos arredondados (bezier), origem no canto superior esquerdo."""
    k = r * 0.45
    return (f"m {r} 0 l {w - r} 0 b {w - k} 0 {w} {k} {w} {r} l {w} {h - r} b {w} {h - k} {w - k} {h} {w - r} {h} "
            f"l {r} {h} b {k} {h} 0 {h - k} 0 {h - r} l 0 {r} b 0 {k} {k} 0 {r} 0")


def eventos_rotulo(cfg, texto, t0, t1):
    """Rótulo das ilustrações: caixa branca arredondada no topo, texto roxo FEA (#5B4599)."""
    ts = base.ts
    larg = largura(cfg, texto, ROT_FS) + 2 * ROT_PAD
    x0, y0 = (W - larg) / 2, ROT_Y - ROT_H / 2
    fad = r"\fad(180,150)"
    return [f"Dialogue: 4,{ts(t0)},{ts(t1)},Caixa,,0,0,0,,"
            rf"{{\pos({x0:.0f},{y0:.0f}){fad}\1a&H08&\p1}}{caixa_arredondada(round(larg), ROT_H, 18)}" "\n",
            f"Dialogue: 5,{ts(t0)},{ts(t1)},Rot,,0,0,0,,{{\\an5\\pos({W // 2},{ROT_Y}){fad}}}{texto}\n"]


def eventos_titulo(cfg, linhas):
    ts = base.ts
    out = []
    n = len(linhas)
    topo = TIT_CENTRO_Y - ((n - 1) * TIT_PASSO + TIT_CAIXA_H) / 2
    clip = rf"\clip({TIT_X},0,{W},{H})"
    for i, l in enumerate(linhas):
        y0 = topo + i * TIT_PASSO
        larg = largura(cfg, l, TIT_FS) + 2 * TIT_PAD
        t1, t2 = int(SLIDE[0] * 1000) + i * 80, int(SLIDE[1] * 1000) + i * 80
        dx = -larg - 10
        caixa = f"m 0 0 l {larg:.0f} 0 {larg:.0f} {TIT_CAIXA_H} 0 {TIT_CAIXA_H}"
        out.append(f"Dialogue: 1,{ts(0)},{ts(TIT_FIM)},Caixa,,0,0,0,,"
                   rf"{{\move({TIT_X + dx:.0f},{y0:.0f},{TIT_X},{y0:.0f},{t1},{t2}){clip}\p1}}{caixa}" "\n")
        out.append(f"Dialogue: 2,{ts(0)},{ts(TIT_FIM)},Tit,,0,0,0,,"
                   rf"{{\move({TIT_X + dx + TIT_PAD:.0f},{y0 + TIT_CAIXA_H / 2:.0f},{TIT_X + TIT_PAD},"
                   rf"{y0 + TIT_CAIXA_H / 2:.0f},{t1},{t2}){clip}}}{l}" "\n")
    bar = f"m 0 0 l {BARRA[1] - BARRA[0]} 0 {BARRA[1] - BARRA[0]} {n * TIT_PASSO - 6} 0 {n * TIT_PASSO - 6}"
    out.append(f"Dialogue: 1,{ts(0)},{ts(TIT_FIM)},Caixa,,0,0,0,,"
               rf"{{\pos({BARRA[0]},{topo - 2:.0f})\1c&H93D0DB&\fad(100,0)\p1}}{bar}" "\n")
    return out


def eventos_legenda(v, palavras, duracao, fim_fala, splits=()):
    ts = base.ts
    out = []
    blocos = base.blocos_legenda(palavras)
    carry, livre = [], 0.0
    for i, bloco in enumerate(blocos):
        if carry:
            bloco, carry = carry + bloco, []
        s, e = max(bloco[0]["s"], livre), bloco[-1]["e"] + 0.15
        prox = blocos[i + 1] if i + 1 < len(blocos) else None
        if prox:
            e = min(e, prox[0]["s"])
        e = min(e, fim_fala)
        if s >= fim_fala:
            continue
        if len(bloco) == 1 and re.sub(r"[^\w]", "", bloco[0]["w"]).lower() in base.LIGACAO | {"é", "eu"}:
            continue
        texto = base.juntar_texto(bloco)
        texto = base.limpar(base.pontuar(base.corrigir(texto, v.get("correcoes", ()))))
        texto = quebrar_linhas(texto)
        minimo = max(0.2, 0.02 * len(texto), 0.45 if len(bloco) == 1 else 0)
        if e - s < minimo:
            fala_inteira = len(bloco) == 1 and bloco[0].get("ini") and bloco[0]["w"].strip()[-1:] in ".?!"
            if prox and not fala_inteira and len(texto) + len(base.juntar_texto(prox)) + 1 <= LEG_MAX * 2:
                carry = list(bloco)
                continue
            e = min(s + minimo, fim_fala)
            livre = e
        partes = texto.split(r"\N")
        n = len(partes)
        for k, p in enumerate(partes):
            meio = (s + e) / 2
            y0 = LEG_Y_SPLIT if any(a <= meio <= b for a, b in splits) else LEG_Y
            y = y0 + (k - (n - 1) / 2) * LEG_PASSO
            out.append(f"Dialogue: 0,{ts(s)},{ts(e)},Leg,,0,0,0,,{{\\an5\\pos({W // 2},{y:.0f})}}{p}\n")
    return out


def quebrar_linhas(texto):
    if len(texto) <= LEG_MAX:
        return texto
    ps = texto.split()
    melhor, dif = texto, 10 ** 9
    for i in range(1, len(ps)):
        l1, l2 = " ".join(ps[:i]), " ".join(ps[i:])
        d = abs(len(l1) - len(l2)) + (8 if ps[i - 1].lower() in base.LIGACAO else 0)
        # marca ou nome composto não se divide entre as linhas ("Black / Friday")
        if (re.sub(r"[^\wé]", "", ps[i - 1]).lower(), re.sub(r"[^\wé]", "", ps[i]).lower()) in PARES:
            d += 30
        if d < dif:
            melhor, dif = l1 + r"\N" + l2, d
    return melhor


def para_editado(t, manter):
    """Tempo do bruto -> tempo do vídeo editado (None se caiu num corte)."""
    off = 0.0
    for a, b in manter:
        if a <= t < b:
            return t - a + off
        off += b - a
    return None


def cartao_produto(img, destino):
    """Quadro branco 552x552 com a foto do produto, levemente inclinado (igual à referência)."""
    from PIL import Image
    fundo = Image.new("RGBA", (PROD_LADO, PROD_LADO), (255, 255, 255, 255))
    p = Image.open(img).convert("RGBA")
    # fundo branco do arquivo vira branco do quadro; foto ocupa ~85% do quadro
    f = PROD_LADO * 0.86 / max(p.width, p.height)
    p = p.resize((round(p.width * f), round(p.height * f)), Image.LANCZOS)
    fundo.alpha_composite(p, ((PROD_LADO - p.width) // 2, (PROD_LADO - p.height) // 2))
    fundo = fundo.rotate(-1.2, resample=Image.BICUBIC, expand=True)
    fundo.save(destino)
    return destino


PAUSA_MAX = 0.9        # silêncio entre falas acima disso sai (pessoa demorando para responder)
MARGEM_PAUSA = 0.3     # respiro mantido antes e depois de cada fala


def tirar_pausas(cfg, v):
    """"faixas" (trechos do bruto a manter) menos os silêncios longos entre falas: o vídeo fica
    dinâmico e vai direto para a pessoa respondendo (Keila, 18/10/2026). Só corta onde o áudio
    está de fato em silêncio (medido em janelas de 50 ms) e entre duas palavras da transcrição,
    deixando um respiro de cada lado."""
    db, limiar, passo = base.perfil_voz(cfg["ffmpeg"], v["entrada"])
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    ws = sorted(((w["s"], w["e"]) for seg in trans for w in seg["words"]), key=lambda x: x[0])
    fora = [(a, b) for a, b in v.get("remover_legenda", [])]
    ws = [w for w in ws if not any(a <= (w[0] + w[1]) / 2 < b for a, b in fora)]
    pmax = v.get("pausa_max", PAUSA_MAX)
    manter = []
    for a, b in v["faixas"]:
        dentro = [w for w in ws if a <= (w[0] + w[1]) / 2 < b]
        if not dentro:
            continue
        # o trecho começa um respiro antes da primeira palavra (a transcrição adianta até 0,3 s)
        ini = min(a, max(0.0, dentro[0][0] - MARGEM_PAUSA))
        # ...mas nunca pega o fim da palavra anterior, que ficou fora do trecho
        antes = [w for w in ws if w[1] <= dentro[0][0] and (w[0] + w[1]) / 2 < a]
        if antes:
            ini = max(ini, min(a, antes[-1][1] + 0.05))
        for w0, w1 in zip(dentro, dentro[1:]):
            if w1[0] - w0[1] <= pmax:
                continue
            # maior trecho silencioso dentro da pausa
            i0, i1 = int(w0[1] / passo), int(w1[0] / passo)
            melhor, k = (0, 0), i0
            while k < i1:
                if db[k] < limiar:
                    m = k
                    while m < i1 and db[m] < limiar:
                        m += 1
                    if m - k > melhor[1] - melhor[0]:
                        melhor = (k, m)
                    k = m
                else:
                    k += 1
            c0, c1 = melhor[0] * passo + 0.15, melhor[1] * passo - 0.15
            if c1 - c0 >= pmax - MARGEM_PAUSA:
                if c0 - ini > 0.3:
                    manter.append([round(ini, 2), round(c0, 2)])
                ini = c1
        if b - ini > 0.3:
            manter.append([round(ini, 2), round(b, 2)])
    return manter


# marcas e nomes compostos: nunca se dividem entre duas legendas e mantêm a maiúscula
PARES = {("belotero", "intense"), ("revanesse", "kiss"), ("neuramis", "deep"), ("rennova", "deep"),
         ("deep", "line"), ("rennova", "lift"), ("lift", "plus"), ("yvoire", "contour"),
         ("juvéderm", "voluma"), ("juvederm", "voluma"), ("neauvia", "stimulate"), ("perfectha", "subskin"),
         ("black", "friday"), ("elite", "injectors"), ("injectors", "congress"), ("md", "codes"),
         ("restylane", "kiss"), ("restylane", "kysse"), ("restylane", "refyne"), ("restylane", "refine"), ("restylane", "lyft"),
         ("restylane", "lift"), ("restylane", "defyne"), ("restylane", "define"), ("saiba", "mais"),
         # como o Whisper escreve antes da correção
         ("neuromis", "deep"), ("neuromys", "deep"), ("renova", "deep"), ("renova", "lift"),
         ("nuve", "estimulate"), ("ivoar", "contour"), ("resilane", "refine"), ("neuronis", "jeep"),
         # lote Melhores produtos (22/10): termos que a legenda quebrava ao meio e a correção não pegava
         ("solo", "infector"), ("swelling", "factor"), ("e", "voar"), ("voar", "contour"), ("evoire", "contour"),
         ("yvoire", "contour"), ("dr", "joão"), ("biogelis", "global"), ("biogelis", "volume"),
         ("biogelis", "volumax"), ("neuramis", "volume"), ("belotero", "volume"), ("belotero", "intenso"),
         ("restylane", "volyme"), ("restylane", "volime"), ("rechilane", "volime"), ("rechilane", "refine"),
         ("restylane", "shape"), ("restylane", "shaype"), ("restylane", "gel"), ("hestlani", "kiss"),
         ("neauvia", "intense"), ("nuvia", "intense"), ("núvia", "intense"), ("nuvia", "stimulate"),
         ("neauvia", "stimulate"), ("eptik", "s100"), ("epetique", "s100"), ("perfecta", "subskin"),
         ("perfectha", "subskin"), ("tear", "trough"), ("tan", "delta"), ("doutor", "pithon"), ("doutor", "piton"),
         ("ácido", "hialurônico"), ("juvederm", "voluma")}
NOMES = {"Black", "Friday", "Elite", "Injectors", "Congress", "Radiesse", "Rennova", "Deep", "Line",
         "Belotero", "Intense", "Refyne", "Restylane", "Profhilo", "Yvoire", "Contour", "Juvéderm",
         "Voluma", "Singderm", "Sofiderm", "Biogelis", "Neauvia", "Stimulate", "Lyft", "Defyne", "Kiss",
         "Subskin", "Perfectha", "Kysse", "Vitalícia", "Vitalício", "MEC", "BD", "MD", "Codes", "Mari", "Botox",
         "Lift", "Plus", "Revanesse", "Neuramis", "YouTube", "Saiba", "Combo", "Mônaco",
         "Global", "Volume", "Volumax", "Shaype", "Volyme", "Dr.", "Yvoire", "Thiamidol", "Eucerin", "Intense", "Dr"}
base.NOMES_PROPRIOS |= NOMES


def juntar_pares(palavras):
    out = []
    for p in palavras:
        # marca dita devagar ("Restylane... Refyne") também fica junta: até 2 s entre as palavras
        if out and out[-1]["w"].strip() and p["s"] - out[-1]["e"] < 2.0:
            a = re.sub(r"[^\wé]", "", out[-1]["w"].split()[-1]).lower()
            b = re.sub(r"[^\wé]", "", p["w"]).lower()
            fim_frase = out[-1]["w"].strip()[-1:] in ".?!" and a != "dr"
            if (a, b) in PARES and not fim_frase:
                out[-1] = dict(out[-1], w=out[-1]["w"].rstrip().rstrip(",") + " " + p["w"].strip(), e=p["e"])
                continue
        out.append(p)
    return out


def gerar(cfg, v, so_legenda=False):
    ff = cfg["ffmpeg"]
    if "faixas" in v:
        v = dict(v, manter=tirar_pausas(cfg, v))
    v, palavras, duracao = base.preparar(cfg, v)
    palavras = juntar_pares(palavras)
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    linhas = v.get("titulo_linhas") or quebrar_titulo(cfg, v["titulo"])
    ev = [ass_header()] + eventos_titulo(cfg, linhas)
    casos = []
    for c in v.get("casos", []):
        t0, t1 = para_editado(c[0], v["manter"]), para_editado(min(c[1], v["manter"][-1][1] - 0.01), v["manter"])
        if t0 is None or t1 is None or t1 <= t0:
            print(f"  AVISO: caso clínico em {c[0]} s caiu num corte")
            continue
        casos.append((max(t0, TIT_FIM), t1, c[2], c[3] if len(c) > 3 else 0.0, c[4] if len(c) > 4 else "split"))
        if len(c) > 5 and c[5]:
            ev += eventos_rotulo(cfg, c[5], max(t0, TIT_FIM) + 0.15, t1)
    ev += eventos_legenda(v, palavras, duracao, duracao, [(a, b) for a, b, _, _, modo in casos if modo == "split"])
    for a, b, texto in v.get("destaques", []):
        ta, tb = para_editado(a, v["manter"]), para_editado(min(b, v["manter"][-1][1] - 0.01), v["manter"])
        if ta is not None:
            ev.append(f"Dialogue: 3,{base.ts(ta)},{base.ts(tb if tb else duracao)},Dest,,0,0,0,,"
                      f"{{\\an5\\pos({W // 2},{DESTAQUE_Y})\\fscx80\\fscy80\\t(0,120,\\fscx100\\fscy100)}}{texto}\n")
    open(ass, "w", encoding="utf-8").write("".join(ev))
    if so_legenda:
        return duracao

    entradas = ["-i", v["entrada"], "-i", cfg["whoosh"]]
    partes, vrot, arot = [], [], []
    mudo = "".join(f",volume=0:enable='between(t,{a},{b})'" for a, b in v.get("silenciar", []))
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1,fps=30[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b}{mudo},asetpts=PTS-STARTPTS,aresample=48000,"
                      f"aformat=channel_layouts=stereo,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        vrot.append(f"[v{i}]")
        arot.append(f"[a{i}]")
    partes.append("".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0[vc]")
    partes.append("".join(arot) + f"concat=n={len(arot)}:v=0:a=1[ac0]")
    def n_entradas():
        return len([e for e in entradas if e == "-i"])

    # efeitos sonoros: arrasto do título no início, "pop" em cada produto, whoosh em cada caso clínico
    sons = [("[1:a]", 0.0, 0.9)]
    prods = []
    for prod in v.get("produtos", []):
        t0 = para_editado(prod[0], v["manter"])
        if t0 is None:
            print(f"  AVISO: produto {prod[1]} em {prod[0]} s caiu num corte")
            continue
        prods.append((t0, prod[1], prod[2] if len(prod) > 2 else PROD_DUR))
    if cfg.get("sfx_pop"):
        for t0, _, _ in prods:
            entradas += ["-i", cfg["sfx_pop"]]
            sons.append((f"[{n_entradas() - 1}:a]", t0, 0.5))
    if cfg.get("sfx_split"):
        for t0, _, _, _, _ in casos:
            entradas += ["-i", cfg["sfx_split"]]
            sons.append((f"[{n_entradas() - 1}:a]", max(0.0, t0 - 0.15), 0.55))
    rot = ["[ac0]"]
    for k, (r, t, vol) in enumerate(sons):
        ms = int(t * 1000)
        partes.append(f"{r}aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]")
        rot.append(f"[s{k}]")
    if v.get("musica", cfg.get("musica")):
        # trilha de fundo baixa, em loop, com fade no fim (a voz do Dr. sempre na frente)
        entradas += ["-stream_loop", "-1", "-i", v.get("musica", cfg.get("musica"))]
        vol = v.get("musica_vol", cfg.get("musica_vol", 0.07))
        partes.append(f"[{n_entradas() - 1}:a]aresample=48000,aformat=channel_layouts=stereo,"
                      f"atrim=0:{duracao:.3f},volume={vol},afade=t=in:d=1.0,"
                      f"afade=t=out:st={max(0, duracao - 1.5):.3f}:d=1.5[mus]")
        rot.append("[mus]")
    partes.append("".join(rot) + f"amix=inputs={len(rot)}:duration=first:normalize=0[ac]")
    atual = "[vc]"
    # tela dividida: caso clínico em cima, Dr. embaixo, faixa esfumaçada no meio (modelo da Keila, 22/10)
    for k, (t0, t1, clip, ini, modo) in enumerate(casos):
        entradas += ["-ss", f"{ini:.2f}", "-t", f"{t1 - t0 + 0.5:.2f}", "-i", clip]
        idx = n_entradas() - 1
        en = f"enable='between(t,{t0:.3f},{t1:.3f})'"
        if modo == "cheia":
            # B-roll em tela cheia, com leve zoom para dar movimento
            partes.append(f"[{idx}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30,"
                          f"scale=w='trunc({W}*(1+0.04*t/{t1 - t0:.2f})/2)*2':h=-2:eval=frame,crop={W}:{H},"
                          f"setpts=PTS-STARTPTS+{t0:.3f}/TB[cs{k}]")
            partes.append(f"{atual}[cs{k}]overlay=0:0:eof_action=pass:{en}[sp{k}]")
            atual = f"[sp{k}]"
            continue
        partes.append(f"{atual}split[base{k}][dr{k}]")
        partes.append(f"[dr{k}]crop={W}:{SPLIT_DR_H}:0:{SPLIT_DR_Y}[drc{k}]")
        partes.append(f"[base{k}][drc{k}]overlay=0:{H - SPLIT_DR_H}:{en}[bm{k}]")
        partes.append(f"[{idx}:v]scale={W}:{SPLIT_TOPO}:force_original_aspect_ratio=increase,crop={W}:{SPLIT_TOPO},"
                      f"setsar=1,fps=30,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                      f"a='255*clip(({SPLIT_TOPO}-Y)/{SPLIT_ESFUMADO},0,1)',"
                      f"setpts=PTS-STARTPTS+{t0:.3f}/TB[cs{k}]")
        partes.append(f"[bm{k}][cs{k}]overlay=0:0:eof_action=pass:{en}[sp{k}]")
        atual = f"[sp{k}]"
    pasta_tmp = os.path.dirname(v["saida"]) or "."
    for k, (t0, img, dur) in enumerate(prods):
        card = cartao_produto(img, os.path.join(pasta_tmp, f".card_{k}.png"))
        entradas += ["-loop", "1", "-t", f"{dur:.2f}", "-framerate", "30", "-i", card]
        idx = n_entradas() - 1
        partes.append(f"[{idx}:v]format=rgba,scale=w='trunc(iw*min(1,0.82+t*1.2)/2)*2':h=-2:eval=frame,"
                      f"fade=t=in:d=0.1:alpha=1,setpts=PTS-STARTPTS+{t0:.3f}/TB[p{k}]")
        # citado enquanto o título está na tela: o quadro sobe para acima do título
        cy = PROD_CENTRO_ALTO if t0 < TIT_FIM else PROD_CENTRO[1]
        # na tela dividida o produto fica no centro do caso clínico (metade de cima)
        if any(a <= t0 <= b and m == "split" for a, b, _, _, m in casos):
            cy = SPLIT_TOPO // 2
        partes.append(f"{atual}[p{k}]overlay=x='{PROD_CENTRO[0]}-w/2':y='{cy}-h/2':eval=frame:"
                      f"enable='between(t,{t0:.3f},{t0 + dur:.3f})'[o{k}]")
        atual = f"[o{k}]"
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    partes.append(f"{atual}ass='{esc}':fontsdir='{cfg['fontsdir']}'[vt]")
    vfim, afim = "[vt]", "[ac]"
    if v.get("cartela"):
        idx = len([e for e in entradas if e == "-i"])
        entradas += ["-i", cfg["cartela"]]
        partes.append(f"[{idx}:v]scale={W}:{H},setsar=1,fps=30[cv]")
        partes.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo[ca]")
        partes.append(f"[vt][ac][cv][ca]concat=n=2:v=1:a=1[vf][af]")
        vfim, afim = "[vf]", "[af]"
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", ";".join(partes),
           "-map", vfim, "-map", afim, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    for k in range(len(v.get("produtos", []))):
        c = os.path.join(pasta_tmp, f".card_{k}.png")
        if os.path.exists(c):
            os.unlink(c)
    return duracao


def main():
    args = sys.argv[1:]
    so_leg = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = gerar(cfg, v, so_leg)
        extra = " + cartela" if v.get("cartela") else ""
        print(f"{v['saida']}: {d:.1f}s{extra}", flush=True)


if __name__ == "__main__":
    main()
