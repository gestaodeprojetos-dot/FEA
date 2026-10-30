#!/usr/bin/env python3
"""Duplica a pasta de um lançamento no Drive (cópia no servidor), trocando datas nos nomes.

Uso: python3 fea_duplicar_lancamento.py ORIGEM_ID PASTA_PAI_ID "NOME DA NOVA PASTA" mapa.json
Gera mapa.json com {id_antigo: {id, nome, mime, caminho}} para atualizar links depois.
Pula arquivos com dado pessoal de lead do evento anterior (PULAR).
"""
import json, re, sys, time, urllib.error, urllib.parse
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, chamar, API
from fea_drive_arvore import filhos

PASTA = "application/vnd.google-apps.folder"
ATALHO = "application/vnd.google-apps.shortcut"
TROCAS = [("08/2026", "11/2026"), ("08/26", "11/26"), ("07/26", "11/26"), ("0826", "1126"),
          ("AGO/26", "NOV/26"), ("ago/26", "nov/26"), ("AGO-26", "NOV-26")]
PULAR = [r"CONTROLE DE LEADS", r"DADOS DE PESQUISA DE LEADS.*Respostas", r"^Cópia de "]


def novo_nome(n):
    for a, b in TROCAS:
        n = n.replace(a, b)
    return n


def api(tk, metodo, url, corpo):
    for t in range(6):
        try:
            return json.load(chamar(tk, metodo, url, corpo))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503) and t < 5:
                time.sleep(2 ** t); continue
            raise


def copiar(tk, origem, destino, caminho, mapa):
    for f in sorted(filhos(tk, origem), key=lambda x: x["name"]):
        cam = caminho + "/" + f["name"]
        if any(re.search(p, f["name"]) for p in PULAR):
            print("PULADO  ", cam, flush=True); continue
        nome = novo_nome(f["name"])
        q = "?supportsAllDrives=true&fields=id,name,mimeType"
        if f["mimeType"] == PASTA:
            r = api(tk, "POST", API + q, {"name": nome, "mimeType": PASTA, "parents": [destino]})
            mapa[f["id"]] = {"id": r["id"], "nome": nome, "mime": PASTA, "caminho": cam}
            print("PASTA   ", cam, flush=True)
            copiar(tk, f["id"], r["id"], cam, mapa)
        elif f["mimeType"] == ATALHO:
            alvo = f.get("shortcutDetails", {}).get("targetId")
            r = api(tk, "POST", API + q, {"name": nome, "mimeType": ATALHO, "parents": [destino],
                                          "shortcutDetails": {"targetId": alvo}})
            mapa[f["id"]] = {"id": r["id"], "nome": nome, "mime": ATALHO, "caminho": cam}
            print("ATALHO  ", cam, flush=True)
        else:
            r = api(tk, "POST", f"{API}/{f['id']}/copy" + q, {"name": nome, "parents": [destino]})
            mapa[f["id"]] = {"id": r["id"], "nome": nome, "mime": f["mimeType"], "caminho": cam}
            print("COPIADO ", cam, "->", nome, flush=True)
        json.dump(mapa, open(sys.argv[4], "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    origem, pai, nome, saida = sys.argv[1:5]
    tk, _ = token()
    raiz = api(tk, "POST", API + "?supportsAllDrives=true&fields=id", {"name": nome, "mimeType": PASTA, "parents": [pai]})
    mapa = {origem: {"id": raiz["id"], "nome": nome, "mime": PASTA, "caminho": ""}}
    print("RAIZ", raiz["id"], flush=True)
    copiar(tk, origem, raiz["id"], "", mapa)
    json.dump(mapa, open(saida, "w"), ensure_ascii=False, indent=1)
    print("FIM", len(mapa), "itens")
