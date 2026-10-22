"""Cria a aba "Novembro26" na planilha "Disparos - João Pithon" com o cronograma de disparos do
MTB 11/26, espelhando o bloco do MTB 08/26 da aba "✅ Agosto26" (âncora no dia do evento:
11/08 -> 09/11), com o nome e o link das copys novas.

A aba é inserida direto no XML do .xlsx: as outras abas, estilos, imagens e tabelas ficam
byte a byte como estão. Antes de subir, a versão atual do arquivo é fixada no histórico do
Drive (rollback em Arquivo > Histórico de versões).

Uso: python3 fea_planilha_disparos_mtb_1126.py PASTA_TRABALHO [--subir]"""
import copy, io, json, re, sys, unicodedata, zipfile
from datetime import date
from xml.sax.saxutils import escape
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, chamar, API, UPLOAD

PLANILHA = "1GMOXAPAiPi8I1YBZIP3EC8Fii0lX-2wc"
ORIGEM, NOVA = "✅ Agosto26", "Novembro26"
CAMPANHA = "MTB - NOV/26"
DIA1 = (date(2026, 11, 1) - date(1899, 12, 30)).days  # número de série do Excel para 01/11/2026
MAPA = "/home/user/FEA/FEA-MTB-11-26/FEA-mapa-drive-mtb-1126.json"

# Blocos de origem (linhas da aba Agosto26) por dia de novembro. 03 e 04/08 caem os dois em 02/11
# (a captação ficou um dia mais curta): seis disparos no dia, redistribuídos por horário.
DIA_02 = [(11, "10:00"), (12, "11:30"), (13, "15:00"), (17, "18:00"), (16, "19:00"), (18, "20:30")]
BLOCOS = {3: range(21, 25), 4: range(26, 30), 5: range(31, 35), 6: range(36, 40), 7: range(41, 45),
          8: range(46, 57), 9: range(58, 78), 10: range(79, 83), 11: range(84, 93)}
CORRIGIR = {52}  # vídeo "12 mil inscritos" do 08/26: precisa ser regravado
LINHA_DIA, LINHA_VAZIA = 93, 94


def ler(z, nome): return z.read(nome).decode("utf-8")


def textos_compartilhados(z):
    sst = ler(z, "xl/sharedStrings.xml")
    return [re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<si>(.*?)</si>", sst, re.S)]


def montar(xlsx, nomes_docs):
    z = zipfile.ZipFile(io.BytesIO(xlsx))
    wb, rels = ler(z, "xl/workbook.xml"), ler(z, "xl/_rels/workbook.xml.rels")
    if f'name="{NOVA}"' in wb: sys.exit(f"A aba {NOVA} já existe: nada feito.")
    rid = re.search(rf'<sheet [^>]*name="{ORIGEM}"[^>]*r:id="(rId\d+)"', wb).group(1)
    alvo = re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
    folha = ler(z, "xl/" + alvo)
    folha_rels = ler(z, "xl/worksheets/_rels/" + alvo.split("/")[-1] + ".rels")
    links = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', folha_rels))
    link_cel = {}
    for h in re.findall(r"<hyperlink [^>]*>", folha):  # a ordem dos atributos varia
        ref, r = re.search(r'ref="([A-Z]+\d+)"', h), re.search(r'r:id="(rId\d+)"', h)
        if ref and r and r.group(1) in links: link_cel[ref.group(1)] = links[r.group(1)]
    sst = textos_compartilhados(z)
    linhas = {int(re.search(r'(?:^| )r="(\d+)"', m.group(1)).group(1)): (m.group(1), m.group(2))
              for m in re.finditer(r"<row ([^>]*)>(.*?)</row>", folha, re.S)}
    novo_id = {k: v["id"] for k, v in json.load(open(MAPA)).items()}

    saida, merges, hlinks, n = [], [], [], 0

    def emitir(origem, dia=None, hora=None, status=None, cabecalho=None):
        nonlocal n
        n += 1
        attrs, cels = linhas[origem]
        attrs = re.sub(r'(^| )r="\d+"', rf'\1r="{n}"', attrs)
        if cabecalho is not None: attrs = re.sub(r' hidden="1"', "", attrs)
        novas = []
        for c in re.finditer(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)', cels, re.S):
            col, resto, corpo = c.group(1), c.group(2), c.group(3)
            s = re.search(r' s="(\d+)"', resto); s = f' s="{s.group(1)}"' if s else ""
            ref = f"{col}{n}"
            if col == "A" and cabecalho is not None:
                v = DIA1 + cabecalho
                novas.append(f'<c r="{ref}"{s}><v>{v}</v></c>' if cabecalho == 0 else
                             f'<c r="{ref}"{s}><f>A2+{cabecalho}</f><v>{v}</v></c>')
                merges.append(f"A{n}:D{n}")
                continue
            if status is None and cabecalho is None:   # cabeçalho das colunas e linhas vazias: cópia fiel
                novas.append(f'<c r="{ref}"{resto}>{corpo}</c>' if corpo is not None else f'<c r="{ref}"{s}/>'); continue
            if corpo is None or cabecalho is not None or col not in "ABCDEFG":
                novas.append(f'<c r="{ref}"{s}/>'); continue  # métricas do 08/26 ficam em branco
            if col == "A": val = status
            elif col == "B": val = CAMPANHA
            elif col == "D" and hora:
                h, m = map(int, hora.split(":")); novas.append(f'<c r="{ref}"{s}><v>{(h * 60 + m) / 1440}</v></c>'); continue
            elif col == "G":
                destino = link_cel.get(f"G{origem}", "")
                velho = re.search(r"/d/([\w-]+)", destino)
                fid = novo_id.get(velho.group(1)) if velho else None
                val = nomes_docs.get(fid) or (sst[int(re.search(r"<v>(\d+)</v>", corpo).group(1))] if ' t="s"' in resto else None)
                if fid:
                    hlinks.append((ref, f"https://docs.google.com/document/d/{fid}/edit"))
                if val is None: novas.append(f'<c r="{ref}"{s}>{corpo}</c>'); continue
            else:
                novas.append(f'<c r="{ref}"{resto}>{corpo}</c>'); continue
            novas.append(f'<c r="{ref}"{s} t="inlineStr"><is><t>{escape(val)}</t></is></c>')
        saida.append(f"<row {attrs}>{''.join(novas)}</row>")

    status_txt = {"agendar": next(t for t in sst if t.startswith("Agendar")),
                  "corrigir": next((t for t in sst if t.startswith("Corrigir")), "Corrigir 🚫")}
    emitir(1)                                                  # cabeçalho das colunas
    emitir(2, cabecalho=0); emitir(LINHA_VAZIA)                # 01/11
    emitir(5, cabecalho=1)                                     # 02/11
    for origem, hora in DIA_02: emitir(origem, hora=hora, status=status_txt["agendar"])
    for dia in range(3, 31):
        emitir(LINHA_DIA, cabecalho=dia - 1)
        for origem in BLOCOS.get(dia, []):
            _, cels = linhas[origem]
            if re.search(r'<c r="B\d+"[^>]*t="s"', cels):
                emitir(origem, status=status_txt["corrigir" if origem in CORRIGIR else "agendar"])
            else: emitir(LINHA_VAZIA)
        if dia not in BLOCOS: emitir(LINHA_VAZIA)

    # listas suspensas: mesmas fórmulas da aba de origem, aplicadas a todas as linhas da aba nova
    formulas = {k: re.search(rf'<dataValidation [^>]*sqref="{k}[^"]*"[^>]*>\s*<formula1>(.*?)</formula1>', folha, re.S)
                for k in ("A4 ", "C55", "E11")}
    camp = re.search(r'sqref="B3"[^>]*>\s*<formula1>&quot;(.*?)&quot;', folha).group(1) + "," + CAMPANHA
    faixa = lambda col: f"{col}3:{col}{n}"
    dvs = "".join(f'<dataValidation type="list" allowBlank="1" sqref="{faixa(col)}"><formula1>{f.group(1)}</formula1></dataValidation>'
                  for col, f in (("A", formulas["A4 "]), ("C", formulas["C55"]), ("E", formulas["E11"])) if f)
    dvs += f'<dataValidation type="list" allowBlank="1" sqref="{faixa("B")}"><formula1>&quot;{camp}&quot;</formula1></dataValidation>'
    cabeca = folha[:folha.find("<sheetData>")]
    cabeca = re.sub(r"<dimension [^>]*/>", f'<dimension ref="A1:AG{n}"/>', cabeca)
    cabeca = re.sub(r"<selection [^>]*/>", "", cabeca)
    hl = "".join(f'<hyperlink ref="{ref}" r:id="rIdL{i}"/>' for i, (ref, _) in enumerate(hlinks))
    xml = (cabeca + "<sheetData>" + "".join(saida) + "</sheetData>"
           + f'<mergeCells count="{len(merges)}">' + "".join(f'<mergeCell ref="{m}"/>' for m in merges) + "</mergeCells>"
           + f'<dataValidations count="{dvs.count("<dataValidation ")}">{dvs}</dataValidations>'
           + (f"<hyperlinks>{hl}</hyperlinks>" if hl else "") + "</worksheet>")
    xml_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + "".join(f'<Relationship Id="rIdL{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(u)}" TargetMode="External"/>'
                          for i, (_, u) in enumerate(hlinks)) + "</Relationships>")

    # registra a aba: logo depois da oculta "Disparos URASMS", antes de "Outubro26"
    numeros = [int(x) for x in re.findall(r"worksheets/sheet(\d+)\.xml", rels)]
    arq = f"worksheets/sheet{max(numeros) + 1}.xml"
    novo_rid = f"rId{max(int(x) for x in re.findall(r'Id=\"rId(\d+)\"', rels)) + 1}"
    sheet_id = max(int(x) for x in re.findall(r'sheetId="(\d+)"', wb)) + 1
    primeira_visivel = re.search(r'<sheet state="visible"[^>]*/>', wb).group(0)
    wb = wb.replace(primeira_visivel, f'<sheet state="visible" name="{NOVA}" sheetId="{sheet_id}" r:id="{novo_rid}"/>' + primeira_visivel, 1)
    rels = rels.replace("</Relationships>", f'<Relationship Id="{novo_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="{arq}"/></Relationships>')
    tipos = ler(z, "[Content_Types].xml").replace("</Types>", f'<Override ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml" PartName="/xl/{arq}"/></Types>')

    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in z.infolist():
            dados = {"xl/workbook.xml": wb, "xl/_rels/workbook.xml.rels": rels, "[Content_Types].xml": tipos}.get(item.filename)
            zo.writestr(item, dados.encode("utf-8") if dados is not None else z.read(item.filename))
        zo.writestr("xl/" + arq, xml)
        zo.writestr(f"xl/worksheets/_rels/{arq.split('/')[-1]}.rels", xml_rels)
    return out.getvalue(), n


if __name__ == "__main__":
    trab, subir = sys.argv[1], "--subir" in sys.argv
    tk, _ = token()
    meta = json.load(chamar(tk, "GET", f"{API}/{PLANILHA}?fields=modifiedTime,headRevisionId&supportsAllDrives=true"))
    xlsx = chamar(tk, "GET", f"{API}/{PLANILHA}?alt=media&supportsAllDrives=true").read()
    nomes = {}
    for v in json.load(open(MAPA)).values():
        if "COMUNICA" in unicodedata.normalize("NFC", v["caminho"]):
            nomes[v["id"]] = json.load(chamar(tk, "GET", f"{API}/{v['id']}?fields=name&supportsAllDrives=true"))["name"]
    novo, n = montar(xlsx, nomes)
    open(f"{trab}/disparos_novo.xlsx", "wb").write(novo)
    print(f"aba {NOVA} montada: {n} linhas")
    if subir:
        agora = json.load(chamar(tk, "GET", f"{API}/{PLANILHA}?fields=modifiedTime&supportsAllDrives=true"))
        if agora["modifiedTime"] != meta["modifiedTime"]:
            sys.exit("A planilha mudou enquanto a aba era montada: rode de novo.")
        chamar(tk, "PATCH", f"https://www.googleapis.com/drive/v3/files/{PLANILHA}/revisions/{meta['headRevisionId']}",
               corpo={"keepForever": True})
        chamar(tk, "PATCH", f"{UPLOAD}/{PLANILHA}?uploadType=media&supportsAllDrives=true", bruto=novo,
               cabecalhos={"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        print("SUBIU (versão anterior fixada:", meta["headRevisionId"] + ")")
