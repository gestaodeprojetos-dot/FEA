#!/usr/bin/env python3
"""Padrão dos reposts que viralizam de novo no Instagram do Dr. João Pithon (@drjoaopithon).

Usa as mesmas fontes do fea_curadoria_reposts.py (export do Meta Business Suite ou a
planilha de controle) e responde a duas perguntas:

1. Perfil inteiro: quais características (região anatômica, procedimento, tipo de
   gancho do título, duração, linha de conteúdo) aparecem mais nos posts de melhor
   desempenho?
2. Pares original x repost: o script encontra sozinho o mesmo vídeo postado mais de
   uma vez (título parecido, ou mesma duração com título próximo) e mede quanto o
   repost rendeu contra o original. Depois compara as características dos reposts
   que viralizaram de novo com as dos que não viralizaram.

"Viralizou" = visualizações no quartil superior da conta (acima do percentil 75).

Uso:
    python3 fea_padroes_reposts.py --csv export1.csv export2.csv
    python3 fea_padroes_reposts.py --planilha
    python3 fea_padroes_reposts.py --csv export.csv --pares-manuais pares.csv

pares.csv (opcional, separador ; ou ,): link_original;link_repost, uma linha por par
que a equipe sabe que é repost, para completar o que a detecção automática não achar.
"""
import argparse, collections, csv, datetime as dt, os, re, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_curadoria_reposts import classificar, ler_csv, ler_planilha, sem_acento  # noqa: E402

REGIOES = [
    ("Lábio e perioral", r"labi|perioral|comissura|bigode|codigo de barra|pertuito|intraoral|intra-oral|mentoniano|sulco ?nasolabial|sulconasolabial|gaivota"),
    ("Nariz", r"rino|nariz|nasal|septo"),
    ("Olheiras e pálpebra", r"olheira|palpebra|orbicular|papula"),
    ("Mento e mandíbula", r"\bmento\b|mentual|mandibula|jowl|papada|submento|\bdao\b|mandibular"),
    ("Terço superior", r"tempora|glabela|front|testa|sobrancelha|coroa|nefertiti|supraorbit|supratroclear|wi-?fi"),
    ("Terço médio", r"malar|zigom|bochecha|terco medio"),
    ("Pescoço e corpo", r"pescoco|platisma|cervical|cotovelo|abdomen|corporal|couro cabeludo|tragus|tragal"),
]
PROCEDIMENTOS = [
    ("Toxina", r"toxina|botox|nefertiti|coroa|glabela|orbicular|mesobotox|wi-?fi|\bdao\b|platisma|espasmo|letybo|dysport|reconstitu"),
    ("Fios", r"\bfios?\b|pdo|pla/?pcl|biofils|ancoragem"),
    ("Bioestimulador", r"bioestimul|hidroxiapatita|caha|plla|poli-?l|policaprolactona|sculptra|radiesse|ellans|ellense"),
    ("Anestesia", r"anestesi|sanep|bloqueio|forame|nervo"),
    ("Rinomodelação", r"rino"),
    ("Preenchimento", r"preench|preenchedor|reologia|hialuron|labial|olheira|\bmento\b|mandibula|tempora|bigode|comissura|malar"),
]
GANCHOS = [
    ("Pergunta", r"\?"),
    ("Número", r"\d"),
    ("Alerta ou erro", r"nunca|erro|errar|errei|evit|perig|nao (faca|foque|deixe)|sem (deixar|perder|dor)|cuidado|intercorr"),
    ("Primeira pessoa", r"\b(fiz|eu|meus?|minhas?|me fez|errei|perdi)\b"),
    ("Como fazer", r"\bcomo\b|passo a passo|dica"),
]
DURACOES = [(0, 30, "até 30 s"), (30, 60, "30 a 60 s"), (60, 90, "60 a 90 s"), (90, 180, "90 s a 3 min"), (180, 10**6, "mais de 3 min")]
MIN_DIAS_REPOST = 21
STOP = set("de da do das dos em no na nos nas para pra com e o a os as um uma por que se ao parte pt final".split())


def milhar(n):
    return f"{int(n):,}".replace(",", ".")


def vezes(x):
    return f"{x:.1f}×".replace(".", ",")


def primeira_linha(t):
    return (t or "").strip().split("\n")[0][:140]


def atributos(p):
    t = sem_acento(primeira_linha(p["titulo"]))
    attrs = {"Linha": [p["linha"]]}
    attrs["Região"] = [n for n, rx in REGIOES if re.search(rx, t)] or ["Sem região específica"]
    attrs["Procedimento"] = [next((n for n, rx in PROCEDIMENTOS if re.search(rx, t)), "Outro")]
    attrs["Gancho do título"] = [n for n, rx in GANCHOS if re.search(rx, t)] or ["Descritivo (só o nome da técnica)"]
    if p.get("duracao"):
        attrs["Duração"] = [next(r for a, b, r in DURACOES if a <= p["duracao"] < b)]
    return attrs


def tokens(t):
    t = re.sub(r"[^a-z0-9 ]", " ", sem_acento(primeira_linha(t)))
    return {w for w in t.split() if w not in STOP and not w.isdigit() and len(w) > 1}


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a and b) else 0.0


def mesmo_video(p, q):
    ta, tb = tokens(p["titulo"]), tokens(q["titulo"])
    j = jaccard(ta, tb)
    if j >= 0.75:
        return True
    # mesmo arquivo de vídeo tem a mesma duração; com título próximo, é o mesmo conteúdo
    return bool(p.get("duracao") and q.get("duracao") and abs(p["duracao"] - q["duracao"]) <= 0.5 and j >= 0.25)


def agrupar(posts, manuais):
    pai = list(range(len(posts)))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    def unir(i, j):
        pai[raiz(i)] = raiz(j)

    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            if mesmo_video(posts[i], posts[j]):
                unir(i, j)
    por_link = {p["link"].split("?")[0].rstrip("/"): i for i, p in enumerate(posts) if p["link"]}
    for a, b in manuais:
        if a in por_link and b in por_link:
            unir(por_link[a], por_link[b])
    grupos = collections.defaultdict(list)
    for i, p in enumerate(posts):
        grupos[raiz(i)].append(p)
    return [sorted(g, key=lambda p: p["data"] or dt.date.min) for g in grupos.values() if len(g) > 1]


def ler_manuais(caminho):
    if not caminho:
        return []
    with open(caminho, encoding="utf-8-sig") as f:
        linhas = [re.split(r"[;,\t]", l.strip()) for l in f if l.strip()]
    norm = lambda u: u.strip().split("?")[0].rstrip("/")
    return [(norm(l[0]), norm(l[1])) for l in linhas if len(l) >= 2 and l[0].startswith("http")]


def tabela_atributos(posts, corte, titulo):
    linhas = [f"### {titulo}\n", "| Característica | Posts | Mediana de views | % que viralizou |", "|---|---|---|---|"]
    por = collections.defaultdict(list)
    for p in posts:
        for v in p["attrs"].get(titulo, []):
            por[v].append(p)
    base = 100 * sum(1 for p in posts if p["views"] >= corte) / len(posts)
    itens = sorted(por.items(), key=lambda kv: -(sum(1 for p in kv[1] if p["views"] >= corte) / len(kv[1])))
    for v, g in itens:
        taxa = 100 * sum(1 for p in g if p["views"] >= corte) / len(g)
        aviso = " (amostra pequena)" if len(g) < 5 else ""
        linhas.append(f"| {v}{aviso} | {len(g)} | {milhar(statistics.median(p['views'] for p in g))} | {taxa:.0f}% |")
    linhas.append(f"\nReferência: {base:.0f}% de todos os posts viralizaram. Acima disso, a característica puxa para cima.\n")
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", nargs="*", default=[])
    ap.add_argument("--planilha", action="store_true")
    ap.add_argument("--pares-manuais", help="CSV com link_original;link_repost")
    ap.add_argument("--ano", type=int, default=dt.date.today().year)
    ap.add_argument("--saida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    a = ap.parse_args()
    if not a.csv and not a.planilha:
        ap.error("informe --csv ARQUIVO(S) ou --planilha")

    posts = []
    for c in a.csv:
        posts += ler_csv(c, a.ano)
    if a.planilha:
        posts += ler_planilha(a.ano)
    unicos = {}
    for p in posts:
        chave = p["link"].split("?")[0].rstrip("/") or (p["titulo"], p["data"])
        if chave not in unicos or (p["views"] or 0) > (unicos[chave]["views"] or 0):
            unicos[chave] = p
    posts = [p for p in unicos.values() if p["views"]]
    if len(posts) < 4:
        sys.exit("ERRO: poucos posts com visualizações para comparar.")
    for p in posts:
        classificar(p)
        p["attrs"] = atributos(p)
    vs = sorted(p["views"] for p in posts)
    corte = vs[int(0.75 * (len(vs) - 1))]
    mediana = statistics.median(vs)

    grupos = agrupar(posts, ler_manuais(a.pares_manuais))
    reposts = []
    for g in grupos:
        orig = g[0]
        for r in g[1:]:
            gap = (r["data"] - orig["data"]).days if (r["data"] and orig["data"]) else None
            reposts.append({"orig": orig, "rep": r, "gap": gap, "razao": r["views"] / orig["views"],
                            "viralizou": r["views"] >= corte,
                            # duas versões no ar ao mesmo tempo não são repost: ficam fora da comparação
                            "simultaneo": gap is not None and gap < MIN_DIAS_REPOST})
    todos, reposts = reposts, [x for x in reposts if not x["simultaneo"]]

    os.makedirs(a.saida, exist_ok=True)
    arq = os.path.join(a.saida, f"FEA-padroes-reposts-{dt.date.today():%Y-%m-%d}.md")
    with open(arq, "w", encoding="utf-8") as f:
        f.write(f"# FEA: padrão dos conteúdos que viralizam ({dt.date.today():%d/%m/%Y})\n\n")
        f.write(f"{len(posts)} posts com visualizações · mediana {milhar(mediana)} · "
                f"\"viralizou\" = {milhar(corte)} views ou mais (quartil superior da conta).\n\n")

        f.write(f"## 1. Pares original x repost ({len(reposts)} encontrados)\n\n")
        if todos:
            f.write("| Conteúdo | Original | Repost | Dias entre | Views original | Views repost | Repost/original | Viralizou? |\n|---|---|---|---|---|---|---|---|\n")
            for x in sorted(todos, key=lambda x: -x["razao"]):
                o, r = x["orig"], x["rep"]
                nome = primeira_linha(r["titulo"])[:60].replace("|", "/")
                d = lambda p: p["data"].strftime("%d/%m/%Y") if p["data"] else ""
                lk = lambda p, txt: f"[{txt}]({p['link']})" if p["link"] else txt
                status = "mesmo período, fora da comparação" if x["simultaneo"] else "sim" if x["viralizou"] else "não"
                f.write(f"| {nome} | {lk(o, d(o))} | {lk(r, d(r))} | {x['gap'] if x['gap'] is not None else ''} | "
                        f"{milhar(o['views'])} | {milhar(r['views'])} | {vezes(x['razao'])} | {status} |\n")
            vir = [x for x in reposts if x["viralizou"]]
            if reposts:
                f.write(f"\n{len(vir)} de {len(reposts)} reposts viralizaram. Mediana repost/original: "
                        f"{vezes(statistics.median(x['razao'] for x in reposts))}.\n\n")
            else:
                f.write("\nOs pares encontrados foram postados no mesmo período (menos de "
                        f"{MIN_DIAS_REPOST} dias entre um e outro), então não contam como repost.\n\n")
            if vir and len(vir) < len(reposts):
                f.write("### O que os reposts que viralizaram têm em comum\n\n| Característica | Nos que viralizaram | Nos que não viralizaram |\n|---|---|---|\n")
                cont = lambda grupo, k, v: sum(1 for x in grupo if v in x["rep"]["attrs"].get(k, []))
                nao = [x for x in reposts if not x["viralizou"]]
                vistos = set()
                for x in reposts:
                    for k, vals in x["rep"]["attrs"].items():
                        for v in vals:
                            if (k, v) in vistos:
                                continue
                            vistos.add((k, v))
                            pv, pn = cont(vir, k, v) / len(vir), cont(nao, k, v) / len(nao)
                            if abs(pv - pn) >= 0.2:
                                f.write(f"| {k}: {v} | {100 * pv:.0f}% | {100 * pn:.0f}% |\n")
                f.write("\nSó aparecem características com diferença de 20 pontos ou mais entre os dois grupos.\n\n")
            # o original já tinha sinal de que ia voltar a viralizar?
            if len(reposts) >= 4:
                f.write("### O desempenho do original prevê o repost?\n\n")
                for campo, nome in (("views", "visualizações"), ("tx_compart", "compartilhamentos por alcance"), ("tx_salv", "salvamentos por alcance")):
                    def taxa(p):
                        base = p["alcance"] or p["views"]
                        if campo == "views":
                            return p["views"]
                        bruto = p["compart"] if campo == "tx_compart" else p["salv"]
                        return bruto / base if (bruto is not None and base) else None
                    pares = [(taxa(x["orig"]), x["viralizou"]) for x in reposts if taxa(x["orig"]) is not None]
                    if len(pares) >= 4:
                        med = statistics.median(v for v, _ in pares)
                        alto = [v for t, v in pares if t >= med]
                        baixo = [v for t, v in pares if t < med]
                        if alto and baixo:
                            f.write(f"- Original com {nome} acima da mediana: {100 * sum(alto) / len(alto):.0f}% dos reposts viralizaram; "
                                    f"abaixo da mediana: {100 * sum(baixo) / len(baixo):.0f}%.\n")
                f.write("\n")
        else:
            f.write("Nenhum par encontrado automaticamente. Se a equipe souber quais posts são reposts, liste em um "
                    "pares.csv (link_original;link_repost) e rode de novo com --pares-manuais.\n\n")

        f.write("## 2. Padrões no perfil inteiro\n\n")
        for k in ("Linha", "Região", "Procedimento", "Gancho do título", "Duração"):
            if any(k in p["attrs"] for p in posts):
                f.write(tabela_atributos(posts, corte, k) + "\n")
    print(f"{len(posts)} posts, {len(reposts)} pares original x repost")
    print("relatório:", arq)


if __name__ == "__main__":
    main()
