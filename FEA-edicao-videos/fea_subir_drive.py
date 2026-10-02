"""Sobe vídeos finais para uma pasta do Google Drive em qualidade total (sem o limite de 30 MB da conversa).

Uso:
    python3 fea_subir_drive.py ID_DA_PASTA arquivo1.mp4 [arquivo2.mp4 ...]

Credenciais lidas do ambiente (nunca no código nem no git):
    FEA_GDRIVE_CLIENT_ID, FEA_GDRIVE_CLIENT_SECRET, FEA_GDRIVE_REFRESH_TOKEN
Geradas pela Keila no projeto Google Cloud FEA-edicao-videos (cliente OAuth + OAuth Playground,
escopo https://www.googleapis.com/auth/drive). Arquivo com o mesmo nome na pasta é substituído.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/drive/v3/files"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
BLOCO = 32 * 1024 * 1024   # múltiplo de 256 KiB


def token():
    dados = urllib.parse.urlencode({
        "client_id": os.environ["FEA_GDRIVE_CLIENT_ID"],
        "client_secret": os.environ["FEA_GDRIVE_CLIENT_SECRET"],
        "refresh_token": os.environ["FEA_GDRIVE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", dados) as r:
        return json.load(r)["access_token"]


def pedir(url, tok, metodo="GET", corpo=None, cab=None):
    req = urllib.request.Request(url, data=corpo, method=metodo,
                                 headers={"Authorization": f"Bearer {tok}", **(cab or {})})
    return urllib.request.urlopen(req)


def existente(tok, pasta, nome):
    q = f"'{pasta}' in parents and name = '{nome.replace(chr(39), chr(92) + chr(39))}' and trashed = false"
    url = API + "?" + urllib.parse.urlencode({"q": q, "fields": "files(id)", "supportsAllDrives": "true",
                                              "includeItemsFromAllDrives": "true"})
    with pedir(url, tok) as r:
        fs = json.load(r)["files"]
    return fs[0]["id"] if fs else None


def subir(tok, pasta, caminho):
    nome = os.path.basename(caminho)
    tam = os.path.getsize(caminho)
    fid = existente(tok, pasta, nome)
    meta = {"name": nome} if fid else {"name": nome, "parents": [pasta]}
    url = (f"{UPLOAD}/{fid}" if fid else UPLOAD) + "?uploadType=resumable&supportsAllDrives=true"
    with pedir(url, tok, "PATCH" if fid else "POST", json.dumps(meta).encode(),
               {"Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/mp4",
                "X-Upload-Content-Length": str(tam)}) as r:
        sessao = r.headers["Location"]
    with open(caminho, "rb") as f:
        ini = 0
        while ini < tam:
            parte = f.read(BLOCO)
            fim = ini + len(parte) - 1
            try:
                with pedir(sessao, tok, "PUT", parte, {"Content-Range": f"bytes {ini}-{fim}/{tam}"}) as r:
                    resp = json.load(r)
            except urllib.error.HTTPError as e:
                if e.code != 308:   # 308 = bloco recebido, continuar
                    raise
            ini = fim + 1
    print(f"{nome}: {tam / 1e6:.0f} MB no Drive ({'substituído' if fid else 'novo'}), id {resp['id']}")


def main():
    pasta, arquivos = sys.argv[1], sys.argv[2:]
    tok = token()
    for a in arquivos:
        subir(tok, pasta, a)


if __name__ == "__main__":
    main()
