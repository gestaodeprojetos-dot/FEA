"""Cria a aba do mês na planilha central "Criativos para Tráfego.xlsx" (pasta 14. Tráfego),
no mesmo padrão das abas Outubro26/Setembro26: uma linha por dia (A:G mesclado) e, logo abaixo
do dia em que a captação começa, o bloco do lançamento com uma linha por fase
(Status, Campanha, Fase, Deadline, Legenda, Link de Criativos, Links Úteis).

Edita o xlsx no nível do XML (só acrescenta a aba, sem regravar as outras), fixa a revisão
atual para rollback e confere se ninguém mexeu na planilha desde o download.

Uso: python3 fea_criativos_trafego_aba_mes.py SAIDA_DIR [--subir]"""
import datetime, html, io, json, re, sys, zipfile
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, chamar, API, UPLOAD

PLANILHA = "1Uj9doFiSNDTOn9z3weT83NdQHvEB-y3e"
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
MODELO = "xl/worksheets/sheet2.xml"          # Outubro26: estilos de cabeçalho, dia e bloco
ABA, ANO, MES = "Novembro26", 2026, 11
PASTA = "https://drive.google.com/drive/folders/{}?usp=drive_link"
LEGENDAS = ("4. LEGENDAS", PASTA.format("18rZyg34nqp1IBBdrk-3Xexv0qzjwgSMn"))
LINKS_UTEIS = ("Links úteis . MTB - FEB 11/2026.xlsx",
               "https://docs.google.com/spreadsheets/d/1Psxwt2QCTgqeOf7pU5NvSbNq3R8bEhwp/edit")
# dia de início da captação -> (campanha, [(fase, deadline, nome da pasta, id da pasta)])
BLOCOS = {2: ("[BR] MTB 11/26", [
    ("Captação", 2, "CAPTAÇÃO", "18xhXlR5m0Rdhirg1318HRns6G-ovLfDk"),
    ("Rmkt", 3, "REMARKETING", "1Ezp6zGkA7TGa-9uMVH0ZH2-6vpxIN8Sc"),
    ("Antecipação", 3, "ANTECIPAÇÃO", "1WoP8Xl-OwuzJzM_KEpqaqq4l9z41jNR6"),
    ("Lembrete", 6, "LEMBRETE", "1NWyLybtsqN6DwcoJC93tOZWsQqY6LFLl"),
    ("Aquecimento FEP", 6, "AQUECIMENTO FEP", "1r3S6WKMmVG5Pw9mCcb8K4buixFWYk9Pj"),
    ("Vendas", 9, "2. VENDAS", "1IG0DxG3XE9k9QY65bNp34T4Fsp-xcEVy"),
    ("RMKT Vendas", 10, "RMKT VENDAS", "1f6mduvh1UZuqoAU1mBXMLcRhCPPfPhEW"),
])}
STATUS_SS = "36"                              # "Agendar 📅" já existe em sharedStrings
CAUDA_VAZIA = 60                              # linhas vazias formatadas depois do último dia


def serial(dia):
    return (datetime.date(ANO, MES, dia) - datetime.date(1899, 12, 30)).days


def esc(t):
    return html.escape(t, quote=True)


def montar(z):
    m = z.read(MODELO).decode()
    linhas = {int(n): r for r, n in re.findall(r'(<row r="(\d+)"[^>]*>.*?</row>)', m, re.S)}
    extras = "".join(f'<c r="{c}{{r}}" s="23"/>' for c in "IJKLMNOPQRSTUVWXY")

    def dia_xml(r, valor, ant):
        f = f"<f>A{ant}+1</f>" if ant else ""
        return (f'<row r="{r}" ht="25.5" customHeight="1"><c r="A{r}" s="20">{f}<v>{valor}</v></c>'
                f'<c r="H{r}" s="22"/>' + extras.format(r=r) + "</row>")

    links, merges, bloco_rows = [], ["B1:C1"], []

    def txt(ref, s, t, url=None):
        if url: links.append((ref, url))
        return f'<c r="{ref}" s="{s}" t="inlineStr"><is><t>{esc(t)}</t></is></c>'

    def fase_xml(r, campanha, fase, prazo, pasta, pid, primeira):
        h = txt(f"H{r}", "40", *LINKS_UTEIS) if primeira else f'<c r="H{r}" s="22"/>'
        return (f'<row r="{r}" ht="25.5" customHeight="1" outlineLevel="1">'
                f'<c r="A{r}" s="36" t="s"><v>{STATUS_SS}</v></c>' + txt(f"B{r}", "32", campanha) +
                txt(f"D{r}", "32", fase) + f'<c r="E{r}" s="34"><v>{serial(prazo)}</v></c>' +
                txt(f"F{r}", "40", *LEGENDAS) + txt(f"G{r}", "40", pasta, PASTA.format(pid)) + h +
                extras.format(r=r) + "</row>")

    corpo, r, ant = [linhas[1]], 2, None
    dias = (datetime.date(ANO + MES // 12, MES % 12 + 1, 1) - datetime.timedelta(days=1)).day
    for d in range(1, dias + 1):
        corpo.append(dia_xml(r, serial(d), ant)); merges.append(f"A{r}:G{r}"); ant = r; r += 1
        if d in BLOCOS:
            campanha, fases = BLOCOS[d]
            for i, (fase, prazo, pasta, pid) in enumerate(fases):
                corpo.append(fase_xml(r, campanha, fase, prazo, pasta, pid, i == 0))
                merges.append(f"B{r}:C{r}"); bloco_rows.append(r); r += 1
    vazio = linhas[40]
    for _ in range(CAUDA_VAZIA):
        corpo.append(re.sub(r'(r=")([A-Z]*)40"', lambda x: f'{x.group(1)}{x.group(2)}{r}"', vazio)); r += 1

    sq = " ".join(f"A{x}" for x in bloco_rows)
    sqb = sq.replace("A", "B")
    camp_lista = re.search(r'sqref="B[^"]*"><formula1>&quot;(.*?)&quot;', m).group(1)
    novas = [c for _, (c, _) in BLOCOS.items() if c not in html.unescape(camp_lista).split(",")]
    camp_lista = ",".join([camp_lista] + [esc(c) for c in novas])
    status_lista = re.search(r'sqref="A[^"]*"><formula1>&quot;(.*?)&quot;', m).group(1)
    rels = "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                   f'Target="{esc(u)}" TargetMode="External"/>' for i, (_, u) in enumerate(links, 1))
    xml = (m[:m.index("<sheetData>")] + "<sheetData>" + "".join(corpo) + "</sheetData>"
           + f'<mergeCells count="{len(merges)}">' + "".join(f'<mergeCell ref="{x}"/>' for x in merges) + "</mergeCells>"
           + f'<dataValidations><dataValidation type="list" allowBlank="1" sqref="{sq}"><formula1>&quot;{status_lista}&quot;</formula1></dataValidation>'
           + f'<dataValidation type="list" allowBlank="1" sqref="{sqb}"><formula1>&quot;{camp_lista}&quot;</formula1></dataValidation></dataValidations>'
           + "<hyperlinks>" + "".join(f'<hyperlink r:id="rId{i}" ref="{ref}"/>' for i, (ref, _) in enumerate(links, 1))
           + "</hyperlinks></worksheet>")
    xml = xml.replace('<selection activeCell="B3" sqref="B3" pane="bottomLeft"/>',
                      '<selection activeCell="A2" sqref="A2" pane="bottomLeft"/>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships '
            'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + rels + "</Relationships>")
    return xml, rels


def gerar(orig, saida):
    zin = zipfile.ZipFile(io.BytesIO(orig))
    wb = zin.read("xl/workbook.xml").decode()
    if f'name="{ABA}"' in wb: raise SystemExit(f"A aba {ABA} já existe, nada a fazer.")
    nums = [int(n) for n in re.findall(r"worksheets/sheet(\d+)\.xml", "\n".join(zin.namelist()))]
    n = max(nums) + 1
    wrels = zin.read("xl/_rels/workbook.xml.rels").decode()
    rid = "rId%d" % (max(int(x) for x in re.findall(r'Id="rId(\d+)"', wrels)) + 1)
    sid = max(int(x) for x in re.findall(r'sheetId="(\d+)"', wb)) + 1
    nova = f'<sheet state="visible" name="{ABA}" sheetId="{sid}" r:id="{rid}"/>'
    # abas ficam do mês mais novo para o mais antigo, logo depois da NOV oculta
    wb = re.sub(r'(<sheets>(?:<sheet state="hidden"[^>]*/>)*)', lambda x: x.group(1) + nova, wb, count=1)
    wrels = wrels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                          f'officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{n}.xml"/></Relationships>')
    ct = zin.read("[Content_Types].xml").decode().replace("</Types>",
        f'<Override ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml" '
        f'PartName="/xl/worksheets/sheet{n}.xml"/></Types>')
    xml, rels = montar(zin)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            dados = {"xl/workbook.xml": wb, "xl/_rels/workbook.xml.rels": wrels, "[Content_Types].xml": ct}.get(it.filename)
            zout.writestr(it, dados.encode() if dados else zin.read(it.filename))
        zout.writestr(f"xl/worksheets/sheet{n}.xml", xml)
        zout.writestr(f"xl/worksheets/_rels/sheet{n}.xml.rels", rels)
    open(saida, "wb").write(buf.getvalue())
    return buf.getvalue()


if __name__ == "__main__":
    pasta = sys.argv[1]
    tk, _ = token()
    meta = json.load(chamar(tk, "GET", f"{API}/{PLANILHA}?fields=modifiedTime,headRevisionId&supportsAllDrives=true"))
    orig = chamar(tk, "GET", f"{API}/{PLANILHA}?alt=media&supportsAllDrives=true").read()
    open(f"{pasta}/antes.xlsx", "wb").write(orig)
    novo = gerar(orig, f"{pasta}/depois.xlsx")
    print("gerado", f"{pasta}/depois.xlsx", "| revisão atual", meta["headRevisionId"], meta["modifiedTime"])
    if "--subir" in sys.argv:
        agora = json.load(chamar(tk, "GET", f"{API}/{PLANILHA}?fields=modifiedTime&supportsAllDrives=true"))
        if agora["modifiedTime"] != meta["modifiedTime"]: raise SystemExit("Planilha mudou durante a geração, rodar de novo.")
        chamar(tk, "PATCH", f"{API}/{PLANILHA}/revisions/{meta['headRevisionId']}?supportsAllDrives=true", corpo={"keepForever": True})
        chamar(tk, "PATCH", f"{UPLOAD}/{PLANILHA}?uploadType=media&supportsAllDrives=true",
               bruto=novo, cabecalhos={"Content-Type": XLSX})
        print("SUBIU; rollback: revisão", meta["headRevisionId"])
