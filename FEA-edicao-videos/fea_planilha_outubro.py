"""Reescreve as linhas de outubro na aba EDIÇÕES: apaga o caso 3 excluído e grava 1 a 8 com links."""
import sys, json, urllib.parse
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
import fea_atualizar_planilha as fp
SH = fp.SHEET_NAME
def ler(rng, render="FORMULA"):
    r = fp.sheets_request("GET", f"values/{urllib.parse.quote(SH + '!' + rng)}?valueRenderOption={render}")
    return r.get("values", [])
F = "https://drive.google.com/drive/folders/"
def link(fid, txt): return f'=HYPERLINK("{F}{fid}";"{txt}")'
LINHAS = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None
if sys.argv[1] == "ler":
    for i, row in enumerate(ler("A118:H135"), 118): print(i, row)
elif sys.argv[1] == "ler-texto":
    for i, row in enumerate(ler("A118:H135", "FORMATTED_VALUE"), 118): print(i, row)
elif sys.argv[1] == "gravar":
    # estado esperado (lido de novo agora): 123 = 1- Toxina, 124 = caso 3 excluído, 125-127 = pastas 3, 4, 5
    rows = ler("A123:H128")
    txt = [str(r) for r in rows]
    assert "1- Toxina" in txt[0] and "Full face e Botox e bio" in txt[1] and "Preench, fios e toxina" in txt[2] \
        and "Retorno botox" in txt[3] and "Retorno toxina" in txt[4], txt
    meta = fp.sheets_request("GET", "?fields=sheets.properties")
    sid = [s["properties"]["sheetId"] for s in meta["sheets"] if s["properties"]["title"] == SH][0]
    def dim(op, a, b, **kw):
        return {op: dict({"range": {"sheetId": sid, "dimension": "ROWS", "startIndex": a, "endIndex": b}}, **kw)}
    fp.sheets_request("POST", ":batchUpdate", {"requests": [
        dim("deleteDimension", 123, 124),                         # caso 3 excluído
        dim("insertDimension", 123, 124, inheritFromBefore=True),  # linha da pasta 2 (antes da 3)
        dim("insertDimension", 127, 130, inheritFromBefore=True),  # pastas 6, 7, 8 (depois da 5)
    ]})
    valores = []
    for l in LINHAS:
        valores.append([l["projeto"], link(l["brutos_id"], l["brutos_nome"]), l["solicitada"], l["entrega"],
                        l["qtd"], link(l["editados_id"], l["pasta"]), l["status"], l["obs"]])
    rng = urllib.parse.quote(f"{SH}!A124:H{123 + len(valores)}")
    print(fp.sheets_request("PUT", f"values/{rng}?valueInputOption=USER_ENTERED", {"values": valores}))
