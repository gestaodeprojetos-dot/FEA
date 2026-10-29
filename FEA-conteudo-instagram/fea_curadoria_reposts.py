#!/usr/bin/env python3
"""Curadoria de reposts do Instagram do Dr. João Pithon (@drjoaopithon).

Lê o export de conteúdo do Meta Business Suite (CSV, cabeçalho em português ou inglês)
ou a aba POSTAGENS INSTAGRAM da planilha de controle, calcula a nota de curadoria de
cada post e devolve o ranking de candidatos a repost, separado por linha de conteúdo.

Uso:
    python3 fea_curadoria_reposts.py --csv export1.csv export2.csv
    python3 fea_curadoria_reposts.py --planilha
    python3 fea_curadoria_reposts.py --csv export.csv --dias-min 90 --top 10 --saida output/

Nota de curadoria (0 a 100), percentil dentro da própria conta, não número absoluto:
    compartilhamentos/alcance 30 · salvamentos/alcance 25 · visualizações 25 ·
    seguidores ganhos/alcance 10 · comentários/alcance 10
Compartilhamento e salvamento pesam mais porque indicam conteúdo que o público técnico
guarda e repassa a colegas, o sinal mais forte de que o tema continua útil meses depois.

Elegível para repost: postado há pelo menos --dias-min dias, sem tema datado
(lançamento, live, congresso, inscrições) e com nota acima do corte (--nota-min).
Menção a marca de produto não bloqueia, mas sai marcada para a Keila confirmar.
"""
import argparse, csv, datetime as dt, os, re, statistics, sys, unicodedata

# Linhas de conteúdo (ordem importa: a primeira que casar vence)
LINHAS = [
    ("Segurança e intercorrência", r"intercorr|necrose|hematoma|hialuronidase|angioedema|ptose|complica|pmma|isquem|oclus|risco|perig|evitar|nunca fa"),
    ("Anatomia que protege", r"anatomi|vasculariz|fluxo de sangue|ligamento|forame|nervo|glandula|muscul|plano|camada|cervical|art[eé]ria|profundidade"),
    ("Produto e preparo", r"reconstitu|dilui|preparo|reologia|diferen[cç]a entre|qual a diferen|bioestimulador(es)? de|tipos de preenchedor|preenchedores|como guardar|o que [eé]"),
    ("Pergunta de consultório", r"\?|pode ou n[aã]o|onde fazer|agulha ou c[aâ]nula|qual lado|por que|porque|vale a pena|pesa"),
    ("Planejamento de caso", r"planejamento|avalia[cç][aã]o|reavalia|resultado|full face|caso cl[ií]nico|relato de caso"),
    ("Técnica em 1 minuto", r"t[eé]cnica|anestesi|sanep|pertuito|aplica[cç][aã]o|preenchimento|fios?|toxina|botox|n[oó]s? |ancoragem|compactar|glabela|orbicular|nasal|frontal|coroa|mento|l[aá]bio|olheira|t[eê]mpora|mand[ií]bula|comissura|bigode|rino"),
]
LINHA_PADRAO = "Bastidores e autoridade"

# Tema datado: não reciclar
DATADO = r"black|lan[cç]amento|inscri[cç]|vagas|masterclass|live\b|ao vivo|congresso|hoje|amanh[aã]|[uú]ltim[oa]s? dias|cupom|oferta|evento|yap ?session|casamento|foto "

# Marcas: repost só com ok da Keila (linha vermelha 3 do CLAUDE.md)
MARCAS = (r"eptq|belotero|neuramis|revanesse|juvederm|restylane|saypha|neauvia|yvoire|letybo|dysport|"
          r"retoxin|hugel|sculptra|radiesse|ellans|ellense|elanse|harmonyca|biofils|kirialys|angelis|lafullen|"
          r"bioplus|subskin|biogelis|etip|volumax|xeomin|botox\b")

# Cabeçalhos aceitos (export do Meta Business Suite em PT ou EN, e a planilha de controle)
CAMPOS = {
    "titulo": ["descricao", "description", "nome", "titulo", "legenda", "caption"],
    "data": ["horario de publicacao", "publish time", "data da postagem", "data de publicacao", "date"],
    "link": ["link permanente", "permalink", "link do post", "link"],
    "tipo": ["tipo de publicacao", "post type", "tipo"],
    "views": ["visualizacoes", "views", "reproducoes", "plays"],
    "alcance": ["alcance", "reach", "contas alcancadas"],
    "curtidas": ["curtidas", "likes", "reacoes"],
    "comentarios": ["comentarios", "comments"],
    "compart": ["compartilhamentos", "shares"],
    "salv": ["salvamentos", "saves", "salvos"],
    "seguidores": ["seguimentos", "seguidores", "follows", "novos seguidores"],
    "duracao": ["duracao (s)", "duracao (seg)", "duration (sec)", "duracao"],
}
PESOS = {"tx_compart": 30, "tx_salv": 25, "views": 25, "tx_seg": 10, "tx_com": 10}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower().strip()


def numero(s):
    s = (s or "").strip().replace(" ", "")
    if not s or s in {"-", "—"}:
        return None
    # "118.152" (pt-BR) ou "118,152" / "118152" (en)
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        s = re.sub(r"[.,]", "", s)
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def data(s, ano_padrao, dia_primeiro=True):
    s = (s or "").strip()
    # export em inglês vem MM/DD/AAAA; em português e na planilha, DD/MM/AAAA
    barra = ("%d/%m/%Y %H:%M", "%d/%m/%Y") if dia_primeiro else ("%m/%d/%Y %H:%M", "%m/%d/%Y")
    for fmt in barra + ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})", s)
    if m:
        return dt.date(ano_padrao, int(m.group(2)), int(m.group(1)))
    return None


def mapear(cabecalho):
    idx = {}
    norm = [sem_acento(c) for c in cabecalho]
    for campo, nomes in CAMPOS.items():
        for nome in nomes:
            if nome in norm:
                idx[campo] = norm.index(nome)
                break
    return idx


def ler_tabela(linhas, ano_padrao, origem):
    cab = linhas[0]
    idx = mapear(cab)
    dia_primeiro = "publish time" not in [sem_acento(c) for c in cab]
    if "views" not in idx and "alcance" not in idx:
        sys.exit(f"ERRO: {origem} sem coluna de visualizações ou alcance. Cabeçalho lido: {cab}")
    posts = []
    for r in linhas[1:]:
        r = list(r) + [""] * (len(cab) - len(r))
        g = lambda k: r[idx[k]] if k in idx else ""
        p = {"titulo": g("titulo").strip(), "link": g("link").strip(), "tipo": g("tipo").strip(),
             "data": data(g("data"), ano_padrao, dia_primeiro), "origem": origem}
        for k in ("views", "alcance", "curtidas", "comentarios", "compart", "salv", "seguidores", "duracao"):
            p[k] = numero(g(k))
        if p["views"] or p["alcance"]:
            posts.append(p)
    return posts


def ler_csv(caminho, ano_padrao):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        return ler_tabela(list(csv.reader(f, dialeto)), ano_padrao, os.path.basename(caminho))


def ler_planilha(ano_padrao):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "FEA-edicao-videos"))
    import urllib.parse
    import fea_atualizar_planilha as fp
    r = fp.sheets_request("GET", "values/" + urllib.parse.quote("POSTAGENS INSTAGRAM!A1:O1000") + "?valueRenderOption=FORMATTED_VALUE")
    return ler_tabela(r.get("values", []), ano_padrao, "planilha POSTAGENS INSTAGRAM")


def percentil(valores, v):
    validos = sorted(x for x in valores if x is not None)
    if v is None or not validos:
        return None
    abaixo = sum(1 for x in validos if x < v)
    iguais = sum(1 for x in validos if x == v)
    return 100 * (abaixo + 0.5 * iguais) / len(validos)


def classificar(p):
    t = sem_acento(p["titulo"])
    p["linha"] = next((nome for nome, rx in LINHAS if re.search(rx, t)), LINHA_PADRAO)
    p["datado"] = bool(re.search(DATADO, t))
    marcas = sorted(set(m.group(0) for m in re.finditer(MARCAS, t)))
    p["marcas"] = ", ".join(marcas)


def pontuar(posts):
    for p in posts:
        base = p["alcance"] or p["views"]
        tx = lambda k: (p[k] / base) if (p[k] is not None and base) else None
        p["tx_compart"], p["tx_salv"], p["tx_com"], p["tx_seg"] = tx("compart"), tx("salv"), tx("comentarios"), tx("seguidores")
    colunas = {k: [p[k] for p in posts] for k in PESOS}
    for p in posts:
        soma = peso = 0
        for k, w in PESOS.items():
            pc = percentil(colunas[k], p[k])
            if pc is not None:
                soma += w * pc
                peso += w
        p["nota"] = round(soma / peso, 1) if peso else 0.0
    mediana = statistics.median([p["views"] for p in posts if p["views"]] or [0])
    for p in posts:
        p["x_mediana"] = round(p["views"] / mediana, 2) if (p["views"] and mediana) else None


def elegibilidade(p, hoje, dias_min, nota_min):
    motivos = []
    if p["datado"]:
        motivos.append("tema datado")
    if p["data"] and (hoje - p["data"]).days < dias_min:
        motivos.append(f"postado há {(hoje - p['data']).days} dias")
    if p["nota"] < nota_min:
        motivos.append(f"nota {p['nota']} abaixo de {nota_min}")
    p["elegivel"] = not motivos
    p["motivo"] = "; ".join(motivos) if motivos else ("ok, confirmar marca: " + p["marcas"] if p["marcas"] else "ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", nargs="*", default=[], help="export(s) de conteúdo do Meta Business Suite")
    ap.add_argument("--planilha", action="store_true", help="ler a aba POSTAGENS INSTAGRAM da planilha de controle")
    ap.add_argument("--dias-min", type=int, default=90, help="idade mínima do post para repost (padrão 90)")
    ap.add_argument("--nota-min", type=float, default=60, help="nota mínima de curadoria (padrão 60)")
    ap.add_argument("--top", type=int, default=10, help="candidatos por linha no resumo")
    ap.add_argument("--ano", type=int, default=dt.date.today().year, help="ano para datas sem ano (dd/mm)")
    ap.add_argument("--hoje", help="data de referência AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--saida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    a = ap.parse_args()
    if not a.csv and not a.planilha:
        ap.error("informe --csv ARQUIVO(S) ou --planilha")

    posts = []
    for c in a.csv:
        posts += ler_csv(c, a.ano)
    if a.planilha:
        posts += ler_planilha(a.ano)
    # mesmo post em dois exports: fica a leitura com mais visualizações (a mais recente)
    unicos = {}
    for p in posts:
        chave = p["link"].split("?")[0].rstrip("/") or (p["titulo"], p["data"])
        if chave not in unicos or (p["views"] or 0) > (unicos[chave]["views"] or 0):
            unicos[chave] = p
    posts = list(unicos.values())
    if not posts:
        sys.exit("ERRO: nenhum post com métrica encontrado.")

    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else dt.date.today()
    for p in posts:
        classificar(p)
    pontuar(posts)
    for p in posts:
        elegibilidade(p, hoje, a.dias_min, a.nota_min)
    posts.sort(key=lambda p: -p["nota"])

    os.makedirs(a.saida, exist_ok=True)
    carimbo = hoje.strftime("%Y-%m-%d")
    arq_csv = os.path.join(a.saida, f"FEA-ranking-reposts-{carimbo}.csv")
    cols = ["nota", "elegivel", "motivo", "linha", "titulo", "data", "link", "tipo", "views", "x_mediana", "alcance",
            "compart", "salv", "comentarios", "seguidores", "tx_compart", "tx_salv", "tx_com", "tx_seg", "marcas", "origem"]
    with open(arq_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cols)
        for p in posts:
            w.writerow([f"{p[c]:.4f}".replace(".", ",") if isinstance(p[c], float) and c.startswith("tx_")
                        else p[c] if p[c] is not None else "" for c in cols])

    arq_md = os.path.join(a.saida, f"FEA-ranking-reposts-{carimbo}.md")
    with open(arq_md, "w", encoding="utf-8") as f:
        eleg = [p for p in posts if p["elegivel"]]
        f.write(f"# FEA: ranking de reposts do Instagram ({hoje.strftime('%d/%m/%Y')})\n\n")
        f.write(f"{len(posts)} posts com métrica · {len(eleg)} elegíveis (idade mínima {a.dias_min} dias, nota mínima {a.nota_min:g}, sem tema datado).\n\n")
        for nome in [l[0] for l in LINHAS] + [LINHA_PADRAO]:
            grupo = [p for p in eleg if p["linha"] == nome][: a.top]
            if not grupo:
                continue
            f.write(f"## {nome}\n\n| Nota | Post | Data | Views | x mediana | Observação |\n|---|---|---|---|---|---|\n")
            for p in grupo:
                titulo = (p["titulo"] or "(sem título)")[:70].replace("|", "/")
                link = f"[{titulo}]({p['link']})" if p["link"] else titulo
                f.write(f"| {p['nota']} | {link} | {p['data'].strftime('%d/%m/%Y') if p['data'] else ''} | "
                        f"{int(p['views']) if p['views'] else ''} | {p['x_mediana'] or ''} | {p['motivo']} |\n")
            f.write("\n")
    print(f"{len(posts)} posts lidos, {sum(p['elegivel'] for p in posts)} elegíveis")
    print("ranking:", arq_csv)
    print("resumo :", arq_md)


if __name__ == "__main__":
    main()
