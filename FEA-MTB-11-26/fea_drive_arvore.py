#!/usr/bin/env python3
"""Lista a árvore inteira de uma pasta do Drive em JSON (id, nome, mime, tamanho, caminho)."""
import json, sys, urllib.parse
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, chamar, API

def filhos(tk, pasta):
    out, pt = [], None
    while True:
        p = {"q": f"'{pasta}' in parents and trashed=false", "pageSize": 1000,
             "fields": "nextPageToken,files(id,name,mimeType,size,shortcutDetails)",
             "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"}
        if pt: p["pageToken"] = pt
        r = json.load(chamar(tk, "GET", API + "?" + urllib.parse.urlencode(p)))
        out += r["files"]; pt = r.get("nextPageToken")
        if not pt: return out

def arvore(tk, pasta, caminho=""):
    res = []
    for f in sorted(filhos(tk, pasta), key=lambda x: x["name"]):
        f["caminho"] = caminho + "/" + f["name"]
        res.append(f)
        if f["mimeType"] == "application/vnd.google-apps.folder":
            res += arvore(tk, f["id"], f["caminho"])
    return res

if __name__ == "__main__":
    tk, _ = token()
    print(json.dumps(arvore(tk, sys.argv[1]), ensure_ascii=False, indent=1))
