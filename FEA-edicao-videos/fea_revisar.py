#!/usr/bin/env python3
"""FEA: revisão rigorosa dos Reels editados, regra por regra (skill fea-revisao-reels).

Uso:
    python3 fea_revisar.py projeto.json [projeto2.json ...] [--folhas PASTA]

Para cada vídeo do projeto confere o arquivo final (.mp4 + .ass) contra todas as regras
pedidas pela Keila e imprime um relatório com ERRO (reprovado, refazer) e ATENÇÃO (conferir
com os olhos). Com --folhas, gera uma folha de contato por vídeo (1 quadro a cada 2 s)
para a revisão visual de sangue, dor, luva tapando e erro de procedimento.
"""
import json
import os
import numpy as np
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402

LIMITE_S = 180

# nomes de produto e termos técnicos com todas as variantes que o Whisper inventa;
# cada tupla: (regex de erro, nome correto, motivo curto para o relatório)
PRODUTOS_CONHECIDOS = [
    (r"\b[Ee] ?voar\b|\b[Ee]voá\b|\b[Ii]voar\b|\b[Ii]vo[aá]r?\b", "Yvoire", "é Yvoire"),
    (r"\bcom ?o? ?tour\b|\b[Cc]ontur\b|\b[Cc]onto[uw]r\b(?! )", "Contour", "é Contour"),
    (r"\bN[uú]vi[ao]\b|\bLúvia\b|\b[Nn]euvia\b(?! )", "Neauvia", "é Neauvia"),
    (r"\b[Nn]euramiz\b|\b[Nn]euramise?\b|\b[Nn]uramis\b", "Neuramis", "é Neuramis"),
    (r"\b[Qq]uiri?al[iy]s\b|\b[Kk]irialis\b|\b[Kk]iriális\b|\b[Cc]urial[iy]s\b", "Kirialys", "é Kirialys"),
    (r"\b[Vv]ol(i|ai|y)me\b(?!.*Volyme)", "Volyme", "é Restylane Volyme"),
    (r"\b[Rr]es(ch|t)ilane\b|\b[Rr]echiline\b", "Restylane", "é Restylane"),
    (r"\b[Ss]ub [Ss]kin\b|\b[Ss]abskin\b|\bsubskin\b|\bSubSkin\b", "Subskin", "é Subskin (Perfectha Subskin)"),
    (r"\b[Rr]evan[ea]ss?e? [Qq]uiss?e?\b", "Revanesse Kiss", "é Revanesse Kiss"),
    (r"\b(?!Revanesse\b)[Rr]evan[ea]ss?e?\b", "Revanesse", "é Revanesse"),
    (r"\b[Ll]et[iy]?bo\b|\bletbo\b|\b[Ll]etibol\b", "Letybo", "é Letybo"),
    (r"\b[Ss]erint?ox\b|\b[Ss]erin?tox\b", "Seryntox", "é Seryntox"),
    (r"\b[Vv]ietr[ei]\b|\b[Vv]ietry\b", "Vietri", "é Vietri"),
    (r"\b[Pp]erfecta\b|\b[Pp]erfect?h?a\b(?! Subskin)", "Perfectha", "é Perfectha"),
    (r"(?<!hi)al[uo]r[oô]nic|lor[oô]nic|acel[eê]r[oô]nic", "hialurônico", "é ácido hialurônico"),
]

# texto que nunca pode aparecer na legenda (regra -> motivo)
PROIBIDO_LEGENDA = [
    (r"\b[Pp]ra\b|\b[Pp]ros?\b", "\"pra/pro\": sempre \"para\""),
    (r"(^|\s)ó(\s|$|[,.!?])", "interjeição \"ó\""),
    (r"\bpr[ée]dio\b", "\"prédio\": é pré-jowl"),
    (r"\b[Gg]elinh", "\"gelinho\": é G'"),
    (r"\bbolos\b|\bbólos\b", "é bolus"),
    (r"\b[Tt]ier\b|\b[Tt]irtrof", "tear trough"),
    (r"(^|\s)%|\b0 0\b", "número incompleto (ex.: \"%\" sem o 1, \"0\" sem o ,2)"),
    (r"\bG linha\b|\bG duas linhas\b", "G linha: escrever G' ou G''"),
    (r"\b(18|2[0-7])[ -]?(38|40|50|70)\b", "cânula sem o x (ex.: 22x70)"),
    (r"\bml\b", "unidade: mL"),
    (r"\bid[ée]ia\b".replace("[ée]", "é"), "grafia antiga \"idéia\""),
    (r"\bsubimento\b", "\"subimento\": é submento"),
    (r"\bmeomodular\b", "\"meomodular\": é miomodular"),
    (r"\blado inferior\b", "\"lado inferior\": é lábio inferior"),
    (r"\blado superior\b", "\"lado superior\": é lábio superior"),
    (r"\bhidroxapatita\b", "é hidroxiapatita"),
    (r"\btessidual\b", "é tecidual"),
    (r"\binterfacial\b", "é interfascial"),
    (r"\bcarpulha\b|\b[Cc]arpulli\b", "é carpule"),
    (r"\btempra\b", "é têmpora"),
    (r"\bsubi?mento\b", "é submento"),
    (r"\bmanejamento\b", "é planejamento"),
    (r"\bintercorrente\b", "é intercorrência"),
    (r"\b[Hh]iper ?tu[ií]tos?\b|\bpertuíto", "\"hipertuito\": é pertuito"),
    (r"\b[Pp]icadinhos?\b", "\"picadinho\": é picadinha"),
    (r"\b(?:[Cc]omo (?:foi|ficou|está|tá)|[Ff]azer|[Dd]a|[Nn]a|[Ee]ssa|[Aa] cada) (?:a )?parestesia\b", "\"parestesia\" no lugar de anestesia (Whisper confunde)"),
    (r"\bdescimento\b", "\"descimento\": é desse mento (duas palavras)"),
]

# falas que as regras mandam cortar: se aparecem no trecho mantido, conferir
FALA_SUSPEITA = [
    (r"parestesia", "\"parestesia\": conferir no áudio se é parestesia (complicação, termo certo) ou anestesia (Whisper confunde)"),
    (r"nenhum\w* (tipo de )?(intercorr|necrose|trauma)|zero (intercorr|necrose)", "afirmação absoluta de segurança: compliance CFM, levar para a Keila"),
    (r"espelh", "espelho para a paciente se ver"),
    (r"fech\w* (o |os )?olh", "pedido de \"fecha o olho\""),
    (r"cirurgi", "histórico da paciente (cirurgia)"),
    (r"\bdói\b|\bdor\b|\bdoeu\b|\bdolorid", "dor fora de contexto técnico"),
    (r"\bmedo\b|ruim de agulha", "medo / conversa pessoal da paciente"),
    (r"marketing|todo mundo fing", "fala que ataca colegas"),
    (r"procurand\w* (o |os )?pertuit|cadê o pertuit", "procurando o pertuito"),
    (r"sangr|sangue|escorr", "menção a sangue (conferir se escorre na imagem)"),
    (r"estour|quebr\w* a agulha", "agulha estourando"),
]


# marcas que nunca entram em título inventado ("Mento feminino com Volumax" -> "Mento feminino")
MARCAS_TITULO = ["Volumax", "Voluma", "Volux", "Volbella", "Juvederm", "Restylane", "Volyme", "Kirialys",
                 "Neauvia", "Neuramis", "Revanesse", "Yvoire", "Perfectha", "Subskin", "Letybo", "Seryntox",
                 "Botox", "Dysport", "Xeomin", "Botulift", "Nabota", "Radiesse", "Sculptra", "Ellansé",
                 "Rennova", "Elleva", "Saypha", "Belotero", "Stylage", "Teosyal", "Princess", "Biofils", "Vietri"]

PALAVRA_NUMERO = re.compile(r"^\d+$")


def _tok(texto):
    return [re.sub(r"[^\w]", "", w).lower() for w in texto.split() if re.sub(r"[^\w]", "", w)]


MARGEM_TITULO_PX = 80   # margem mínima de cada lado (80 px = ~7,4% de 1080)
LARGURA_SEGURA = fe.W - 2 * MARGEM_TITULO_PX   # área útil para o título (920 px)
MAX_CHARS_TITULO_LINHA = 22   # acima disso, enxugar

_font_titulo = None
FATOR_ASS_PIL = 0.543   # libass renderiza menor que PIL no mesmo size; calibrado na referência


def _carregar_fonte():
    global _font_titulo
    if _font_titulo is not None:
        return _font_titulo
    try:
        from PIL import ImageFont
        tam_pil = int(fe.TITULO_TAM * FATOR_ASS_PIL)
        for base in [os.path.dirname(os.path.abspath(__file__)),
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"),
                     "/tmp/claude-0"]:
            for root, _, files in os.walk(base):
                for f in files:
                    if "Montserrat" in f and "ExtraBold" in f and f.endswith(".ttf"):
                        _font_titulo = ImageFont.truetype(os.path.join(root, f), tam_pil)
                        return _font_titulo
    except ImportError:
        pass
    return None


def medir_titulo_px(texto):
    """Largura em pixels da linha mais larga do título (Montserrat ExtraBold no tamanho ASS).
    Retorna (largura_max, n_linhas). Se não conseguir medir com a fonte, estima por caracteres."""
    brutas = texto.replace(r"\N", "\n").split("\n")
    escalas = [int(m.group(1)) / fe.TITULO_TAM if (m := re.search(r"\\fs(\d+)", l)) else 1.0 for l in brutas]
    linhas = [re.sub(r"\{[^}]*\}", "", l).strip() for l in brutas]
    font = _carregar_fonte()
    if font:
        from PIL import ImageDraw, Image
        img = Image.new("L", (fe.W * 2, 200))
        draw = ImageDraw.Draw(img)
        larguras = [draw.textlength(l, font=font) * k for l, k in zip(linhas, escalas)]
    else:
        larguras = [len(l) * fe.TITULO_TAM * 0.55 * k for l, k in zip(linhas, escalas)]
    return max(larguras) if larguras else 0, len(linhas), linhas


def sonda(ff, arq):
    out = subprocess.run([ff, "-nostdin", "-i", arq], capture_output=True, text=True).stderr
    codec = re.search(r"Video: (\w+)", out)
    res = re.search(r"Video: .*?(\d{3,4})x(\d{3,4})", out)
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    d = int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 0
    return (codec[1] if codec else "?"), (res and (int(res[1]), int(res[2]))), d


def ts(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def ler_ass(caminho):
    titulo, legendas = [], []
    for linha in open(caminho, encoding="utf-8"):
        if not linha.startswith("Dialogue:"):
            continue
        p = linha.rstrip("\n").split(",", 9)
        s, e, estilo = ts(p[1]), ts(p[2]), p[3]
        txt = re.sub(r"\{[^}]*\}", "", p[9]).replace("\\N", " ").strip()
        (titulo if estilo == "Titulo" else legendas).append((s, e, txt))
    return titulo, legendas


def revisar(cfg, v, folhas=None):
    ff, erros, aten = cfg["ffmpeg"], [], []
    mp4, ass = v["saida"], v["saida"].rsplit(".", 1)[0] + ".ass"
    if not os.path.exists(mp4):
        return [f"arquivo final não existe: {mp4}"], []

    # 1. formato de entrega
    codec, res, dur = sonda(ff, mp4)
    if codec != "h264":
        erros.append(f"codec {codec}: tem que ser H.264 (HEVC abre com tela preta)")
    if res != (1080, 1920):
        erros.append(f"resolução {res}: tem que ser 1080x1920")
    # limite vale para cada parte também (antes a Parte 1/2 passava sem conferir)
    if dur > LIMITE_S + 0.05:
        erros.append(f"{dur:.1f} s com CTA: passa de 3 min" + (" (cada parte também tem que caber)" if v.get("parte") else
                     ", cortar o que é parado ou dividir em Parte 1/2"))

    # 2. título: exatamente o da imagem, nos 3 primeiros segundos
    titulo, legendas = ler_ass(ass)
    txt_tit = " ".join(t for s, e, t in titulo if s < 1)
    esperado = re.sub(r"\s+", " ", v["titulo"] + (f" Parte {v['parte']}" if v.get("parte") else ""))
    if re.sub(r"\s+", " ", txt_tit) != esperado:
        erros.append(f"título \"{txt_tit}\" diferente de \"{esperado}\"")
    if titulo and max(e for s, e, t in titulo if s < 1) > fe.TITULO_DUR + 0.01:
        erros.append("título passa dos 3 s")
    if v.get("parte") == 1 and not any(s > 1 and "Parte 2" in t for s, e, t in titulo):
        erros.append("Parte 1 sem a cartela \"Parte 2 no perfil\" no final")

    # 2b. headline: margem e comprimento
    titulo_formatado = fe.formatar_titulo(v)
    larg_px, n_linhas, linhas_txt = medir_titulo_px(titulo_formatado)
    if larg_px > LARGURA_SEGURA:
        erros.append(f"headline estoura a margem ({larg_px:.0f} px, máximo {LARGURA_SEGURA} px): enxugar o título \"{v['titulo']}\"")
    elif larg_px > LARGURA_SEGURA * 0.92:
        aten.append(f"headline quase encostando na margem ({larg_px:.0f} px / {LARGURA_SEGURA} px): considerar enxugar")
    for li in linhas_txt:
        if len(li) > MAX_CHARS_TITULO_LINHA + 4 and not li.startswith("Parte "):
            erros.append(f"linha de headline com {len(li)} chars (\"{li}\"): máximo ~{MAX_CHARS_TITULO_LINHA}, enxugar o título")
    if n_linhas > 3 + (1 if v.get("parte") else 0) and fe.TITULO_TAM_LONGO not in [0]:
        aten.append(f"headline com {n_linhas} linhas (fonte {fe.TITULO_TAM_LONGO}): título longo da imagem, conferir na tela")
    elif n_linhas > 2 and not v.get("parte"):
        aten.append(f"headline com {n_linhas} linhas: título longo, considerar enxugar")

    # 2b'. título inventado (sem imagem de títulos) nunca leva nome de produto (Keila, 02/10/2026)
    if v.get("titulo_origem") != "imagem":
        for marca in MARCAS_TITULO:
            if re.search(rf"\b{marca}\b", v["titulo"], re.I):
                erros.append(f"título \"{v['titulo']}\" com nome de produto ({marca}): sem imagem de títulos, tirar o produto")

    # 2c. nomes de produto no título (Whisper pode errar o título se veio da transcrição)
    for rx, nome_certo, motivo in PRODUTOS_CONHECIDOS:
        if any(m.group(0).strip() not in {nome_certo, *nome_certo.split()} for m in re.finditer(rx, v["titulo"])):
            erros.append(f"título contém grafia errada de {nome_certo}: \"{v['titulo']}\"")

    # 3. legenda: texto proibido, só depois do título, sem legenda sobre silêncio
    db, lim, ps = fe.perfil_voz(ff, mp4)
    # "fala_paciente": [[a, b], ...] em segundos do bruto: resposta baixa do paciente, conferida no
    # áudio, que fica na legenda (Keila 02/10) mesmo sem passar na régua de volume do Dr.
    _m = fe.encaixar_cortes(v["manter"], *fe.perfil_voz(ff, v["entrada"])[::2]) if v.get("fala_paciente") else []
    def _ts(t):
        off = 0.0
        for a, b in _m:
            if a <= t < b:
                return off + t - a
            off += b - a
        return -1
    pac_saida = [(_ts(a) - 0.3, _ts(b) + 0.3) for a, b in v.get("fala_paciente", []) if _ts(a) >= 0]
    def grafia_errada(rx, nome_certo, texto):
        # a regex pega variantes; a grafia oficial em si ("Letybo", "Neuramis") não é erro
        certos = {nome_certo, *nome_certo.split()}
        return any(m.group(0).strip() not in certos for m in re.finditer(rx, texto))
    for s, e, t in legendas:
        for rx, nome_certo, motivo in PRODUTOS_CONHECIDOS:
            if grafia_errada(rx, nome_certo, t):
                erros.append(f"[{s:5.1f}s] \"{t}\": {motivo} (nome de produto errado na legenda)")
        for rx, motivo in PROIBIDO_LEGENDA:
            if re.search(rx, t):
                erros.append(f"[{s:5.1f}s] \"{t}\": {motivo}")
        if s < fe.TITULO_DUR - 0.01:
            erros.append(f"[{s:5.1f}s] legenda junto com o título")
        paciente = any(a <= s <= b for a, b in pac_saida)   # fala baixa do paciente, conferida no áudio
        seg = db[int(s / ps):int(e / ps) + 1]
        # régua: 6 dB acima do ruído de fundo (lim = ruído + 12); o Dr. às vezes fala baixo
        if len(seg) and (seg >= lim - 6).mean() < 0.35 and not paciente:
            erros.append(f"[{s:5.1f}s] \"{t}\": legenda sem o Dr. falando (palavra solta)")
        elif len(t.split()) == 1 and e - s < 0.35:
            aten.append(f"[{s:5.1f}s] \"{t}\": palavra sozinha piscando ({e - s:.2f} s)")
    # 3b. sincronia com o áudio (Keila 26/09 e 01/10: "legendas não estão sincronizadas")
    for k, (s, e, t) in enumerate(legendas):
        if s < fe.TITULO_DUR + 0.5:
            continue
        i = int(s / ps)
        # atrasada: o Dr. já fala antes da legenda aparecer
        antes = db[max(0, i - int(0.6 / ps)):i]
        fim_ant = legendas[k - 1][1] if k else 0
        if len(antes) and (antes >= lim).mean() > 0.7 and s - fim_ant > 0.5:
            erros.append(f"[{s:5.1f}s] \"{t}\": legenda atrasada (o Dr. já fala antes da legenda)")
        # adiantada: legenda entra e ainda não tem voz
        depois = db[i:i + int(0.5 / ps)]
        if len(depois) and (depois >= lim - 6).mean() < 0.1:
            erros.append(f"[{s:5.1f}s] \"{t}\": legenda entra antes da fala (adiantada)")
        # legenda termina muito depois da fala (Dr. parou, legenda ainda na tela)
        j = int(e / ps)
        antes_fim = db[max(0, j - int(0.8 / ps)):j]
        if e - s > 1.5 and len(antes_fim) and (antes_fim >= lim - 6).mean() < 0.15:
            aten.append(f"[{s:5.1f}s] \"{t}\": legenda fica na tela {e - s:.1f} s depois da fala acabar")
    texto_todo = " ".join(t for _, _, t in legendas)
    if re.search(r"(?<!ácido )\bhialurônico", texto_todo):
        erros.append("\"hialurônico\" sem \"ácido\" na frente: é ácido hialurônico")
    for (s1, e1, _), (s2, _, _) in zip(legendas, legendas[1:]):
        if s2 < e1 - 0.01 and s2 != s1:
            erros.append(f"[{s2:5.1f}s] duas legendas ao mesmo tempo")

    # 4. começo e fim na fala
    k = 0
    while k < len(db) - 10 and (db[k:k + 10] >= max(lim - 4, 42)).mean() < 0.8:   # sala com ruído alto: voz baixa fica só ~8 dB acima
        k += 1
    if k * ps > 0.8:
        erros.append(f"começa com {k * ps:.1f} s de silêncio (tem que começar quando o Dr. fala)")
    # fim: som subindo no último instante = começo de outra palavra (o bruto às vezes acaba assim)
    if len(db) > 6 and db[-2:].max() >= lim + 6 and db[-2:].mean() > db[-6:-3].mean() + 6:
        erros.append("som subindo no último instante: começo de outra palavra no fim")

    # 5. pontos de corte: voz atravessando o corte = pedaço de palavra
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    palavras = [w for seg in trans for w in seg["words"]]
    db_b, lim_b, ps_b = fe.perfil_voz(ff, v["entrada"])
    manter = fe.encaixar_cortes(v["manter"], db_b, ps_b)
    # corte no meio da fala, medido no áudio do bruto: voz forte dos dois lados do ponto
    for a2, b2 in manter:
        for t, lado in ((a2, "começo"), (b2, "fim")):
            i = int(t / ps_b)
            if 0.3 < t < len(db_b) * ps_b - 0.3 and all(db_b[k] >= lim_b + 8 for k in (i - 1, i, i + 1)):
                aten.append(f"{lado} de trecho em {t:.2f}s do bruto em fala contínua, sem respiro: ouvir se cortou palavra")
    t0 = 0.0
    for i, (a, b) in enumerate(manter):
        t0 += b - a
        if i < len(manter) - 1:
            j = int(t0 / ps)
            if 1 <= j < len(db) - 1 and all(db[x] >= lim + 6 for x in (j - 1, j, j + 1)):
                aten.append(f"[{t0:5.1f}s] voz encostada no corte (conferir se cortou palavra)")
    # frase terminando no meio: última palavra mantida sem pontuação e próxima fala logo depois
    b = manter[-1][1]
    for a2, b2 in manter:
        for w in palavras:
            if w["s"] < b2 - 0.05 < w["e"] - 0.1 and w["e"] - w["s"] < 1.2:
                aten.append(f"corte em {b2:.2f}s do bruto perto do fim de \"{w['w'].strip()}\" (pela transcrição): ouvir")
            if a2 > 0.3 and w["s"] + 0.1 < a2 < w["e"] - 0.05 and w["e"] - w["s"] < 1.2:
                aten.append(f"começo em {a2:.2f}s do bruto perto de \"{w['w'].strip()}\" (pela transcrição): ouvir")
    dentro = [w for w in palavras if (w["s"] + w["e"]) / 2 < b]
    depois = [w for w in palavras if (w["s"] + w["e"]) / 2 >= b]
    if dentro and depois and depois[0]["s"] - dentro[-1]["e"] < 0.8 and not re.search(r"[.?!]$", dentro[-1]["w"].strip()):
        aten.append(f"final \"...{' '.join(w['w'].strip() for w in dentro[-4:])}\" seguido de \"{depois[0]['w'].strip()}\": conferir se a frase terminou")

    # 5b. palavra faltando na legenda (buraco deixa a legenda fora de sincronia)
    ditas = [w for w in palavras if any(a <= (w["s"] + w["e"]) / 2 < b for a, b in manter)
             and not any(a <= (w["s"] + w["e"]) / 2 < b for a, b in v.get("remover_legenda", []) + v.get("silenciar", []))
             and w["w"].startswith(" ")]
    n_leg = sum(len(t.split()) for _, _, t in legendas)
    def t_saida(t):
        off = 0.0
        for a, b in manter:
            if a <= t < b:
                return off + t - a
            off += b - a
        return -1
    mantido_total = sum(b - a for a, b in manter)
    n_dit = sum(1 for w in ditas if t_saida((w["s"] + w["e"]) / 2) > fe.TITULO_DUR + 0.2)
    if n_dit and n_leg / n_dit < 0.9:
        erros.append(f"legenda com {n_leg} palavras para {n_dit} faladas: faltam palavras (buracos na legenda)")

    # 5c. palavra a palavra (Keila, 02/10/2026): enumeração completa ("pertuito 1, 2, 3, 4, 5, 6") e
    # nenhum trecho falado sem legenda (inclusive a resposta do paciente). Compara a fala transcrita
    # (com as mesmas correções da legenda) com o texto da legenda.
    import difflib
    mut = []
    for w in palavras:   # mesmo agrupamento da legenda: "0" + ",2" = "0,2", "1" + "%" = "1%"
        if mut and not w["w"].startswith(" "):
            mut[-1]["w"] += w["w"]
        else:
            mut.append(dict(w))
    fe.numerar_enumeracao(mut)
    falado = []
    for w in mut:
        m = (w["s"] + w["e"]) / 2
        if any(a <= m < b for a, b in v.get("remover_legenda", []) + v.get("silenciar", [])):
            continue
        ts_ = t_saida(m)
        if ts_ > fe.TITULO_DUR + 0.3 and ts_ < mantido_total - 0.3:
            falado += [(t, ts_) for t in _tok(fe.corrigir(w["w"], v.get("correcoes", ())))]
    leg = [t for _, _, txt in legendas for t in _tok(txt)]
    sm = difflib.SequenceMatcher(None, [t for t, _ in falado], leg, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op not in ("delete", "replace"):
            continue
        faltam = falado[i1:i2]
        nums = [t for t, _ in faltam if PALAVRA_NUMERO.match(t)]
        if nums and op == "delete":
            erros.append(f"[{faltam[0][1]:5.1f}s] número falado fora da legenda ({', '.join(nums)}): enumeração incompleta")
        if op == "delete" and len(faltam) >= 3:
            erros.append(f"[{faltam[0][1]:5.1f}s] fala sem legenda: \"{' '.join(t for t, _ in faltam)}\" (fala do paciente ou palavra cortada?)")

    # 5d. voz no áudio sem legenda nem palavra transcrita (fala baixa que a transcrição pulou,
    # ex.: resposta da paciente): conferir ouvindo
    no_ar = np.zeros(len(db), bool)
    for s_, e_, _ in legendas:
        no_ar[int(s_ / ps):int(e_ / ps) + 1] = True
    voz = db >= lim
    k, ini_v = int((fe.TITULO_DUR + 0.5) / ps), None
    fim_conteudo = int((mantido_total - 0.3) / ps)
    while k < min(fim_conteudo, len(db)):
        if voz[k] and not no_ar[k]:
            j = k
            while j < fim_conteudo and not no_ar[j] and (voz[j] or voz[j:j + 4].any()):
                j += 1
            if (voz[k:j].sum()) * ps >= 1.0:
                aten.append(f"[{k * ps:5.1f}s a {j * ps:5.1f}s] voz no áudio sem legenda: ouvir (fala do paciente? fala baixa?)")
            k = j
        k += 1

    # 5e. voz falhando/picotando (Keila, 02/10/2026, pasta 7 vídeo 1): o áudio final, trecho a trecho,
    # tem que ter o mesmo volume do bruto. Queda forte onde o bruto tem a voz do Dr. = corte, silêncio
    # ou concat comendo a fala. Compara o volume do .mp4 com o do bruto nos trechos mantidos.
    # envelope de 5 ms e alinhamento fino por trecho: o concat do CTA desloca o áudio ~21 ms
    # (priming do AAC) e, em janelas de 50 ms, isso parecia queda de voz (falso alarme)
    db5, _, p5 = fe.perfil_voz(ff, mp4, passo=0.005)
    db5b, lim5b, _ = fe.perfil_voz(ff, v["entrada"], passo=0.005)
    mudo_int = [(t_saida(a), t_saida(b)) for a, b in v.get("silenciar", [])]
    quedas, off = [], 0.0
    for a, b in manter:
        esp = db5b[int(a / p5):int(b / p5)]
        i_ini = int(round(off / p5))
        fin = db5[i_ini:i_ini + len(esp)]
        n = min(len(esp), len(fin))
        off += b - a
        if n < 200:
            continue
        def corr(L):
            x, y = fin[max(0, L):n + min(0, L)], esp[max(0, -L):n - max(0, L)]
            return np.corrcoef(x, y)[0, 1] if len(x) > 50 and x.std() and y.std() else -1
        L = max(range(-20, 21), key=corr)
        for i in range(25, n - 25):
            j = i - L
            if not 4 <= j < n - 4:
                continue
            viz = esp[j - 4:j + 5]          # 45 ms de voz forte em volta, no bruto
            t = (i_ini + i) * p5
            if viz.min() >= lim5b + 6 and fin[i] < viz.min() - 20 and fin[i + 1] < viz.min() - 20 and \
                    not any(x <= t <= y for x, y in mudo_int if x >= 0):
                if not quedas or t - quedas[-1] > 0.1:
                    quedas.append(t)
    if quedas:
        erros.append(f"voz falhando: {len(quedas)} quedas de volume no meio da fala (ex.: "
                     + ", ".join(f"{t:.1f}s" for t in quedas[:6]) + "), o bruto tem voz nesses pontos")

    # 6. silêncio longo (outro lado do rosto, procurando pertuito)
    fala = [(s, e) for s, e, _ in legendas]
    ult = fe.TITULO_DUR
    for s, e in fala + [(dur, dur)]:
        if s - ult > 8:
            aten.append(f"[{ult:5.1f}s a {s:5.1f}s] {s - ult:.0f} s sem fala: conferir nos quadros se o Dr. está parado (cortar) ou fazendo a técnica (fica)")
        ult = max(ult, e)

    # 6b. vídeo picotado: técnica cortada (Keila 26/09: "só corta quando o Dr. não está fazendo nada")
    _, _, dur_bruto = sonda(ff, v["entrada"])
    mantido = sum(b - a for a, b in manter)
    if dur_bruto and mantido / dur_bruto < 0.6 and dur_bruto < 200:
        aten.append(f"mantido só {mantido / dur_bruto:.0%} do bruto: conferir nos quadros cada trecho cortado (técnica não pode sair)")
    for (a1, b1), (a2, b2) in zip(manter, manter[1:]):
        if a2 - b1 > 6:
            aten.append(f"corte de {a2 - b1:.0f} s no bruto ({b1:.1f}s a {a2:.1f}s): o Dr. estava parado? se fazia técnica, devolver")

    # 7. falas que as regras mandam cortar
    texto_mantido = [(w["s"], w["w"]) for w in palavras if any(a <= (w["s"] + w["e"]) / 2 < b for a, b in manter)]
    frase = " ".join(w for _, w in texto_mantido).lower()
    for rx, motivo in FALA_SUSPEITA:
        for m in re.finditer(rx, frase):
            trecho = frase[max(0, m.start() - 40):m.end() + 30].replace("\n", " ")
            aten.append(f"fala mantida \"...{trecho}...\": {motivo}")

    # 8. folha de contato para a revisão visual
    if folhas:
        os.makedirs(folhas, exist_ok=True)
        nome = os.path.join(folhas, os.path.basename(mp4).rsplit(".", 1)[0] + ".png")
        subprocess.run([ff, "-nostdin", "-v", "error", "-y", "-i", mp4, "-vf",
                        "fps=1/2,scale=120:213,tile=15x6", "-frames:v", "1", nome], check=False)
        aten.append(f"revisão visual: {nome}")
    return erros, aten


def main():
    args = sys.argv[1:]
    folhas = None
    if "--folhas" in args:
        i = args.index("--folhas")
        folhas = args[i + 1]
        args = args[:i] + args[i + 2:]
    total_err = 0
    for proj in args:
        cfg = json.load(open(proj, encoding="utf-8"))
        for v in cfg["videos"]:
            erros, aten = revisar(cfg, v, folhas)
            total_err += len(erros)
            status = "REPROVADO" if erros else "OK"
            print(f"\n## {os.path.basename(v['saida'])}: {status}")
            for x in erros:
                print(f"  ERRO     {x}")
            for x in aten:
                print(f"  ATENÇÃO  {x}")
    print(f"\nTotal de erros: {total_err}")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
