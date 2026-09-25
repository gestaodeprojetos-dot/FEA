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
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402

LIMITE_MB = 30
LIMITE_S = 180

# texto que nunca pode aparecer na legenda (regra -> motivo)
PROIBIDO_LEGENDA = [
    (r"\b[Pp]ra\b|\b[Pp]ros?\b", "\"pra/pro\": sempre \"para\""),
    (r"(^|\s)ó(\s|$|[,.!?])", "interjeição \"ó\""),
    (r"\bpr[ée]dio\b", "\"prédio\": é pré-jowl"),
    (r"\bG linha\b|\bG duas linhas\b", "G linha: escrever G' ou G''"),
    (r"\b(18|2[0-7])[ -]?(38|40|50|70)\b", "cânula sem o x (ex.: 22x70)"),
    (r"\bml\b", "unidade: mL"),
    (r"\bid[ée]ia\b".replace("[ée]", "é"), "grafia antiga \"idéia\""),
]

# falas que as regras mandam cortar: se aparecem no trecho mantido, conferir
FALA_SUSPEITA = [
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
    mb = os.path.getsize(mp4) / 1024 / 1024
    if codec != "h264":
        erros.append(f"codec {codec}: tem que ser H.264 (HEVC abre com tela preta)")
    if res != (1080, 1920):
        erros.append(f"resolução {res}: tem que ser 1080x1920")
    if mb >= LIMITE_MB:
        erros.append(f"{mb:.1f} MB: acima de {LIMITE_MB} MB")
    if dur > LIMITE_S and not v.get("parte"):
        erros.append(f"{dur:.0f} s: passa de 3 min sem divisão em Parte 1/2")

    # 2. título: exatamente o da imagem, nos 3 primeiros segundos
    titulo, legendas = ler_ass(ass)
    txt_tit = " ".join(t for s, e, t in titulo if s < 1)
    esperado = v["titulo"] + (f" Parte {v['parte']}" if v.get("parte") else "")
    if re.sub(r"\s+", " ", txt_tit) != esperado:
        erros.append(f"título \"{txt_tit}\" diferente de \"{esperado}\"")
    if titulo and max(e for s, e, t in titulo if s < 1) > fe.TITULO_DUR + 0.01:
        erros.append("título passa dos 3 s")
    if v.get("parte") == 1 and not any(s > 1 and "Parte 2" in t for s, e, t in titulo):
        erros.append("Parte 1 sem a cartela \"Parte 2 no perfil\" no final")

    # 3. legenda: texto proibido, só depois do título, sem legenda sobre silêncio
    db, lim, ps = fe.perfil_voz(ff, mp4)
    for s, e, t in legendas:
        for rx, motivo in PROIBIDO_LEGENDA:
            if re.search(rx, t):
                erros.append(f"[{s:5.1f}s] \"{t}\": {motivo}")
        if s < fe.TITULO_DUR - 0.01:
            erros.append(f"[{s:5.1f}s] legenda junto com o título")
        seg = db[int(s / ps):int(e / ps) + 1]
        # régua: 6 dB acima do ruído de fundo (lim = ruído + 12); o Dr. às vezes fala baixo
        if len(seg) and (seg >= lim - 6).mean() < 0.35:
            erros.append(f"[{s:5.1f}s] \"{t}\": legenda sem o Dr. falando (palavra solta)")
        elif len(t.split()) == 1 and e - s < 0.35:
            aten.append(f"[{s:5.1f}s] \"{t}\": palavra sozinha piscando ({e - s:.2f} s)")
    for (s1, e1, _), (s2, _, _) in zip(legendas, legendas[1:]):
        if s2 < e1 - 0.01 and s2 != s1:
            erros.append(f"[{s2:5.1f}s] duas legendas ao mesmo tempo")

    # 4. começo e fim na fala
    k = 0
    while k < len(db) - 10 and (db[k:k + 10] >= max(lim, 42)).mean() < 0.8:
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

    # 6. silêncio longo (outro lado do rosto, procurando pertuito)
    fala = [(s, e) for s, e, _ in legendas]
    ult = fe.TITULO_DUR
    for s, e in fala + [(dur, dur)]:
        if s - ult > 8:
            aten.append(f"[{ult:5.1f}s a {s:5.1f}s] {s - ult:.0f} s sem fala: repetição do outro lado ou procurando pertuito?")
        ult = max(ult, e)

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
