#!/usr/bin/env python3
"""Atualiza a planilha de controle de edições (aba EDIÇÕES) via Google Sheets API.

Uso:
    python3 fea_atualizar_planilha.py append \\
        --projeto "Instagram" \\
        --doc "Brutos" \\
        --data-solicitada "02/10" \\
        --data-entrega "02/10" \\
        --quantidade 13 \\
        --salvar "2- Preenchimento e toxina" \\
        --link-brutos "https://drive.google.com/drive/folders/ID_BRUTOS" \\
        --link-editados "https://drive.google.com/drive/folders/ID_EDITADOS" \\
        --status "Entregue"

    python3 fea_atualizar_planilha.py read --range "A120:H140"

    python3 fea_atualizar_planilha.py delete-row --row 126

Usa FEA_GDRIVE_CLIENT_ID, FEA_GDRIVE_CLIENT_SECRET e FEA_GDRIVE_REFRESH_TOKEN das variáveis
do ambiente (o mesmo acesso do Drive, com escopo spreadsheets: fea_setup_google_oauth.sh).
"""
import argparse, json, os, sys, urllib.request, urllib.parse, urllib.error

SPREADSHEET_ID = "1RYzwrbbCFZCTVZ-pJosMhDpwNdSDLoFEZVHpIQjWzNQ"
SHEET_NAME = "🔴 EDIÇÕES"

def load_env():
    for p in [".env", os.path.join(os.path.dirname(__file__), ".env")]:
        if os.path.isfile(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def get_token():
    load_env()
    rt = os.environ.get("FEA_GDRIVE_REFRESH_TOKEN", "")
    client_id = os.environ.get("FEA_GDRIVE_CLIENT_ID", "")
    client_secret = os.environ.get("FEA_GDRIVE_CLIENT_SECRET", "")
    if not (rt and client_id and client_secret):
        print("ERRO: faltam FEA_GDRIVE_CLIENT_ID, FEA_GDRIVE_CLIENT_SECRET ou FEA_GDRIVE_REFRESH_TOKEN "
              "nas variáveis do ambiente. Rode: bash fea_setup_google_oauth.sh", file=sys.stderr)
        sys.exit(1)
    data = urllib.parse.urlencode({
        "client_id": client_id, "client_secret": client_secret,
        "refresh_token": rt, "grant_type": "refresh_token"
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["access_token"]

def sheets_request(method, path, body=None):
    token = get_token()
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"ERRO {e.code}: {err}", file=sys.stderr)
        if e.code in (403, 404):
            print("O acesso não inclui Sheets. Rode: bash fea_setup_google_oauth.sh", file=sys.stderr)
        sys.exit(1)

def cmd_read(args):
    range_str = urllib.parse.quote(f"{SHEET_NAME}!{args.range}")
    result = sheets_request("GET", f"values/{range_str}")
    for i, row in enumerate(result.get("values", []), 1):
        print(f"{i:3d} | " + " | ".join(row))

def cmd_append(args):
    row = [
        args.projeto or "Instagram",
        args.doc or "Brutos",
        args.data_solicitada or "",
        args.data_entrega or "",
        str(args.quantidade) if args.quantidade else "",
        args.salvar or "",
        args.status or "Entregue",
        args.obs or ""
    ]
    if args.link_brutos:
        row[1] = f'=HYPERLINK("{args.link_brutos}";"{args.doc or "Brutos"}")'   # planilha em pt-BR: separador ";"
    if args.link_editados:
        row[5] = f'=HYPERLINK("{args.link_editados}";"{args.salvar}")'

    range_str = urllib.parse.quote(f"{SHEET_NAME}!A:H")
    body = {"values": [row]}
    result = sheets_request("POST",
        f"values/{range_str}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS",
        body)
    print(f"OK: linha adicionada em {result.get('updates', {}).get('updatedRange', '?')}")

def cmd_delete_row(args):
    sheet_id = None
    meta = sheets_request("GET", "?fields=sheets.properties")
    for s in meta.get("sheets", []):
        if s["properties"]["title"] == SHEET_NAME:
            sheet_id = s["properties"]["sheetId"]
            break
    if sheet_id is None:
        print(f"ERRO: aba '{SHEET_NAME}' não encontrada.", file=sys.stderr)
        sys.exit(1)
    body = {"requests": [{"deleteDimension": {
        "range": {"sheetId": sheet_id, "dimension": "ROWS",
                  "startIndex": args.row - 1, "endIndex": args.row}
    }}]}
    sheets_request("POST", ":batchUpdate", body)
    print(f"OK: linha {args.row} deletada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_read = sub.add_parser("read")
    p_read.add_argument("--range", default="A1:H10")

    p_append = sub.add_parser("append")
    p_append.add_argument("--projeto")
    p_append.add_argument("--doc")
    p_append.add_argument("--data-solicitada")
    p_append.add_argument("--data-entrega")
    p_append.add_argument("--quantidade", type=int)
    p_append.add_argument("--salvar")
    p_append.add_argument("--link-brutos")
    p_append.add_argument("--link-editados")
    p_append.add_argument("--status", default="Entregue")
    p_append.add_argument("--obs", default="")

    p_del = sub.add_parser("delete-row")
    p_del.add_argument("--row", type=int, required=True)

    args = parser.parse_args()
    if args.cmd == "read": cmd_read(args)
    elif args.cmd == "append": cmd_append(args)
    elif args.cmd == "delete-row": cmd_delete_row(args)
    else: parser.print_help()
