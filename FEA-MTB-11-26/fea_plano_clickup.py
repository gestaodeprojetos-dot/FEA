#!/usr/bin/env python3
"""Converte o backlog do MTB 08/26 no plano do MTB 11/26 (datas, sprint, descrição com links novos).

Regra de data: fase de preparação (antes de 03/08) é comprimida linearmente em 22/10 a 30/10;
da captação em diante, mantém a distância até o evento (11/08 -> 09/11). Fim de semana vai para
a sexta anterior. Saída: FEA-plano-clickup-mtb-1126.json
"""
import json, re, unicodedata
from datetime import date, datetime, timedelta, timezone

BRT = timezone(timedelta(hours=-3))
EV_VELHO, EV_NOVO = date(2026, 8, 11), date(2026, 11, 9)
PREP_VELHO, PREP_NOVO = (date(2026, 6, 21), date(2026, 8, 2)), (date(2026, 10, 22), date(2026, 10, 30))
CAPT_NOVO = date(2026, 11, 2)
LISTAS = {"S1": "1400270000004209", "S2": "1400270000004210", "S3": "1400270000004211"}
PESSOAS = {44232914: "Leo Quirino", 49092607: "Letícia Marangon", 99934269: "Keila", 118026144: "Gabriela Borges",
           82024913: "Matheus Saar", 194479496: "Equipe IAutomate (Júlio Couto)", 81993945: "André Vivas",
           55090440: "Adriane Möbbs", 82063965: "Matheus van der Ham"}
SEM_DATA = {"86ajerwkw": ("2026-10-22", "2026-10-27"), "86ajzkmz9": ("2026-11-06", "2026-11-06"),
            "86ajzkmu0": ("2026-11-06", "2026-11-06"), "86ajuyfcu": ("2026-10-26", "2026-10-30"),
            "86ajdpd0t": ("2026-10-22", "2026-10-23")}

mapa = json.load(open("FEA-mapa-drive-mtb-1126.json"))
por_caminho = {unicodedata.normalize("NFC", v["caminho"]): v for v in mapa.values()}


def url(caminho):
    v = por_caminho[unicodedata.normalize("NFC", caminho)]
    if v["mime"] == "application/vnd.google-apps.folder": return f"https://drive.google.com/drive/folders/{v['id']}"
    if v["mime"] == "application/vnd.google-apps.document": return f"https://docs.google.com/document/d/{v['id']}/edit"
    if v["mime"] == "application/vnd.google-apps.presentation": return f"https://docs.google.com/presentation/d/{v['id']}/edit"
    return f"https://drive.google.com/file/d/{v['id']}/view"


RAIZ = url("")
LINKS = {
    "Links úteis": url("/Links úteis . MTB - FEB 08/2026.xlsx"), "Briefing": url("/0. PLANEJAMENTO/Briefing MTB 08/26.docx"),
    "Pasta Copy": url("/1. COPY"), "Pasta Artes": url("/2. ARTES"), "Briefing Design": url("/2. ARTES/Briefing Design - MTB 08/26"),
    "Pasta Tráfego": url("/4. TRÁFEGO"), "Criativos prontos": url("/4. TRÁFEGO/1. CRIATIVOS/2. CRIATIVOS PRONTOS"),
    "Pasta URA + SMS": url("/10. URA + SMS"), "Pasta Automação": url("/13. AUTOMAÇÃO"),
    "Informações do ingresso": url("/13. AUTOMAÇÃO/INFORMAÇÕES INGRESSO"), "Doc de automação": url("/13. AUTOMAÇÃO/Doc para captação - Automação.docx"),
    "Slides": url("/2. ARTES/10. SLIDES/Slides Masterclass em Toxina 07/26"), "Briefing Slides": url("/2. ARTES/10. SLIDES/BRIEFING SLIDES - MTB - 08/26"),
    "Pasta Ingresso": url("/2. ARTES/9. INGRESSO"), "Imagens API": url("/2. ARTES/1. WHATSAPP/IMAGENS API"),
    "Copy imagens API": url("/1. COPY/3. COMUNICAÇÃO/1. API/[MTB AGO/26] Copy imagens API"),
    "Copy captação WhatsApp": url("/1. COPY/3. COMUNICAÇÃO/2. WHATSAPP/[MTB AGO/26] Captação WPP"),
    "Copy página de captura": url("/1. COPY/1. PÁGINAS/Copy com as alterações na página de captura - MTB"),
    "Copy página de vendas": url("/1. COPY/1. PÁGINAS/Copy com as alterações na página de vendas - FEB"),
    "Copy página do Zoom": url("/1. COPY/1. PÁGINAS/MTB - Copy da página de link pro Zoom"),
    "Copy obrigado + check-in": url("/1. COPY/1. PÁGINAS/Página de obrigado + checkin - MTB"),
    "Legendas": url("/1. COPY/4. LEGENDAS"), "Copy de criativos": url("/1. COPY/2. CRIATIVOS"),
    "Comunicação (API, WhatsApp, e-mail)": url("/1. COPY/3. COMUNICAÇÃO"),
}
POR_TEMA = [  # palavra no nome da tarefa ou do grupo -> links que entram na descrição
    ("slide", ["Slides", "Briefing Slides"]), ("ingresso", ["Pasta Ingresso", "Informações do ingresso"]),
    ("imagens de api", ["Copy imagens API", "Imagens API"]), ("arte que vai nas mensagens de api", ["Copy imagens API"]),
    ("página de captura", ["Copy página de captura"]), ("página de vendas", ["Copy página de vendas"]),
    ("zoom", ["Copy página do Zoom"]), ("pesquisa", ["Copy obrigado + check-in"]), ("legenda", ["Legendas"]),
    ("criativos", ["Copy de criativos", "Briefing Design", "Criativos prontos"]), ("ura", ["Pasta URA + SMS"]),
    ("comunica", ["Comunicação (API, WhatsApp, e-mail)"]), ("onboarding", ["Comunicação (API, WhatsApp, e-mail)"]),
    ("whatsapp", ["Copy captação WhatsApp"]), ("tráfego", ["Pasta Tráfego"]), ("links úteis", ["Links úteis"]),
    ("drive", []), ("design", ["Pasta Artes", "Briefing Design"]), ("copy", ["Pasta Copy"]),
    ("automação", ["Pasta Automação", "Doc de automação"]), ("oferta", ["Briefing"]),
]


def d(ms): return datetime.fromtimestamp(int(ms) / 1000, BRT).date()


def converter(dv):
    if dv >= date(2026, 8, 3):
        n = EV_NOVO + (dv - EV_VELHO)
        n = max(n, CAPT_NOVO)
    else:
        (a, b), (c, e) = PREP_VELHO, PREP_NOVO
        frac = min(max((dv - a).days / (b - a).days, 0), 1)
        n = c + timedelta(days=round(frac * (e - c).days))
    while n.weekday() >= 5: n -= timedelta(days=1)
    return n


def sprint(n):
    return "S1" if n < CAPT_NOVO else ("S2" if n < EV_NOVO else "S3")


def descricao(t, grupo):
    nome = (t[1] + " " + (grupo or "")).lower()
    chaves = []
    for k, ls in POR_TEMA:
        if (re.search(r"\b" + k + r"\b", nome) if k == "design" else k in nome):
            chaves += [x for x in ls if x not in chaves]
    linhas = [f"Masterclass em Toxina Botulínica, aula ao vivo 09/11 às 20h (Zoom). Captação 02/11 a 09/11, carrinho FEB 09/11 a 11/11.", ""]
    for k in chaves: linhas.append(f"{k}: {LINKS[k]}")
    linhas += [f"Drive do lançamento: {RAIZ}", f"Links úteis: {LINKS['Links úteis']}", "",
               f"Tarefa espelhada do MTB 08/26: https://app.clickup.com/t/{t[0]}"]
    if t[6]: linhas.append("Responsável no MTB 08/26: " + ", ".join(PESSOAS.get(p, str(p)) for p in t[6]) + " (confirmar antes de atribuir)")
    return "\n".join(linhas)


tarefas = json.load(open("FEA-backlog-mtb-0826.json"))
nomes = {t[0]: t[1].strip() for t in tarefas}
pais = {t[2] for t in tarefas if t[2]}
folhas = []
vazios = set()
for t in tarefas:
    if not t[2] and (t[0] in pais or not (t[4] or t[5])):
        if t[0] not in pais:  # grupo vazio no 08/26 (Suporte / CS, Comercial...): mantém o grupo na sprint
            vazios.add(({"680": "S2", "681": "S3"}.get(t[3], "S1"), t[1].strip()))
        continue  # grupo (Design, Gestão...): recriado por sprint
    if t[0] in SEM_DATA:
        ini, fim = [date.fromisoformat(x) for x in SEM_DATA[t[0]]]
    else:
        fim = converter(d(t[5] or t[4]))
        ini = min(converter(d(t[4] or t[5])), fim)
    grupo = nomes.get(t[2]) if t[2] else None
    if grupo == "Caminho lead para início de captação": grupo = "Gestão"
    folhas.append({"ref": t[0], "nome": t[1].strip(), "grupo": grupo or "Gestão", "inicio": ini.isoformat(),
                   "fim": fim.isoformat(), "sprint": sprint(fim), "descricao": descricao(t, grupo)})
# ajustes de texto de tarefas que citavam o evento anterior
for f in folhas:
    if f["ref"] == "86ahtp3vk":
        f["descricao"] = f["descricao"].replace("Masterclass em", "Atualizar data para 09/11 e o prazo do bônus para 23h59 de 9 de novembro. Masterclass em", 1)

NOVAS = [  # demandas extras do MTB 11/26
    ("Gestão", "Validar oferta FEB (R$997) em paralelo à Black Friday Vitalícia (vendas BF até 20/11)", "2026-10-22", "2026-10-23",
     "A captação (02/11 a 09/11) e o carrinho FEB (09/11 a 11/11) caem dentro da janela de vendas da Black Friday. Decidir se o FEB entra com preço cheio, condição BF ou bônus diferente, e alinhar com o comercial (Sabrina)."),
    ("Gestão", "Confirmar bônus da oferta FEB 11/26 (lista do 08/26 está marcada como 'confirmar' no briefing)", "2026-10-22", "2026-10-23", "Briefing: " + LINKS["Briefing"]),
    ("Copy", "Revisar copys com datas atualizadas para 09/11 (conferir dias da semana e agenda de disparos)", "2026-10-23", "2026-10-27",
     "Todas as copys foram duplicadas do MTB 08/26 com datas trocadas (evento 11/08 terça para 09/11 segunda). Conferir os disparos de abertura (02/11, Finados) e a véspera (domingo 08/11). Pasta: " + LINKS["Pasta Copy"]),
    ("Design", "Reexportar artes e criativos estáticos que têm data do evento gravada (11/08 para 09/11)", "2026-10-23", "2026-10-28",
     "Lista dos arquivos com data gravada no doc de auditoria de criativos (pasta 4. TRÁFEGO). Criativos prontos: " + LINKS["Criativos prontos"]),
    ("Design", "Atualizar slides: data 09/11 e bônus 'até 23h59 de 9 de novembro'", "2026-10-26", "2026-10-30", "Slides: " + LINKS["Slides"]),
    ("Automação", "Criar estrutura do MTB 1126: grupo SendFlow, lista e tag [1126] [MTB] no Active, planilha CONTROLE DE LEADS e webhook da pesquisa", "2026-10-23", "2026-10-29",
     "A planilha de controle e as respostas de pesquisa do 08/26 não foram copiadas (dado pessoal de lead). Atualizar a planilha de Links úteis com os novos links. " + LINKS["Links úteis"]),
]
for g, n, i, f, desc in NOVAS:
    folhas.append({"ref": None, "nome": n, "grupo": g, "inicio": i, "fim": f, "sprint": sprint(date.fromisoformat(f)),
                   "descricao": desc + f"\n\nDrive do lançamento: {RAIZ}"})

plano = {}
for f in folhas:
    plano.setdefault(f["sprint"], {}).setdefault(f["grupo"], []).append(f)
for s_, g in vazios:
    plano.setdefault(s_, {}).setdefault(g, [])
json.dump({"listas": LISTAS, "plano": plano}, open("FEA-plano-clickup-mtb-1126.json", "w"), ensure_ascii=False, indent=1)
for s, gs in sorted(plano.items()):
    print(s, {g: len(v) for g, v in gs.items()})
    for g, v in gs.items():
        for f in sorted(v, key=lambda x: x["fim"]): print(f"   {f['inicio']}..{f['fim']} [{g}] {f['nome']}")
