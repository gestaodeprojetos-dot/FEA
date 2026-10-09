#!/usr/bin/env python3
"""Drive da FEA pela API (upload de vídeo grande, criar e renomear pasta).

As chaves vêm só das variáveis do ambiente, nunca do código:
    FEA_GDRIVE_CLIENT_ID, FEA_GDRIVE_CLIENT_SECRET, FEA_GDRIVE_REFRESH_TOKEN

Uso:
    python3 fea_drive.py upload PASTA_ID video1.mp4 [video2.mp4 ...] [--substituir]
    python3 fea_drive.py pasta PASTA_PAI_ID "9- Espasmos"      # imprime o ID (reaproveita se já existe)
    python3 fea_drive.py renomear ARQUIVO_ID "OK. Espasmos"
    python3 fea_drive.py testar                                 # confere chave e escopos
    python3 fea_drive.py baixar PASTA_OU_ARQUIVO_ID DESTINO     # baixa a pasta inteira (ou 1 arquivo)
    python3 fea_drive.py listar PASTA_ID                        # id | nome | MB | duração
    python3 fea_drive.py trocar ARQUIVO_ID video.mp4            # novo conteúdo, mesmo ID e link

--substituir manda para a lixeira o arquivo de mesmo nome na pasta antes de subir.
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

API = "https://www.googleapis.com/drive/v3/files"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
PASTA_MIME = "application/vnd.google-apps.folder"
BLOCO = 32 * 1024 * 1024


def token():
    faltando = [k for k in ("FEA_GDRIVE_CLIENT_ID", "FEA_GDRIVE_CLIENT_SECRET", "FEA_GDRIVE_REFRESH_TOKEN")
                if not os.environ.get(k)]
    if faltando:
        sys.exit("ERRO: faltam variáveis do ambiente: " + ", ".join(faltando))
    dados = urllib.parse.urlencode({
        "client_id": os.environ["FEA_GDRIVE_CLIENT_ID"],
        "client_secret": os.environ["FEA_GDRIVE_CLIENT_SECRET"],
        "refresh_token": os.environ["FEA_GDRIVE_REFRESH_TOKEN"],
        "grant_type": "refresh_token"}).encode()
    try:
        r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", dados))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO ao renovar o acesso ({e.code}): {e.read().decode()[:300]}\n"
                 "Rode: bash fea_setup_google_oauth.sh")
    return r["access_token"], r.get("scope", "")


def chamar(tk, metodo, url, corpo=None, cabecalhos=None, bruto=None):
    h = {"Authorization": f"Bearer {tk}", **(cabecalhos or {})}
    dados = bruto
    if corpo is not None:
        dados = json.dumps(corpo).encode()
        h["Content-Type"] = "application/json; charset=UTF-8"
    req = urllib.request.Request(url, data=dados, headers=h, method=metodo)
    return urllib.request.urlopen(req)


def listar(tk, pasta, nome, mime=None):
    q = f"'{pasta}' in parents and trashed = false and name = '{nome.replace(chr(39), chr(92) + chr(39))}'"
    if mime:
        q += f" and mimeType = '{mime}'"
    url = API + "?" + urllib.parse.urlencode({
        "q": q, "fields": "files(id,name)", "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true"})
    return json.load(chamar(tk, "GET", url))["files"]


def subir(tk, pasta, caminho, arquivo_id=None):
    """Sobe um arquivo novo na pasta ou, com arquivo_id, troca o conteúdo daquele arquivo
    (mesmo ID e mesmo link; a versão anterior fica no histórico de versões do Drive)."""
    nome = os.path.basename(caminho)
    tam = os.path.getsize(caminho)
    cab = {"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)}
    if arquivo_id:
        r = chamar(tk, "PATCH", f"{UPLOAD}/{arquivo_id}?uploadType=resumable&supportsAllDrives=true&fields=id",
                   corpo={}, cabecalhos=cab)
    else:
        r = chamar(tk, "POST", UPLOAD + "?uploadType=resumable&supportsAllDrives=true&fields=id",
                   corpo={"name": nome, "parents": [pasta]}, cabecalhos=cab)
    sessao = r.headers["Location"]
    print(f"  subindo {tam / 1024 / 1024:.1f} MB...", flush=True)
    with open(caminho, "rb") as f:
        ini = 0
        while ini < tam:
            pedaco = f.read(BLOCO)
            fim = ini + len(pedaco) - 1
            req = urllib.request.Request(sessao, data=pedaco, method="PUT", headers={
                "Content-Length": str(len(pedaco)), "Content-Range": f"bytes {ini}-{fim}/{tam}"})
            try:
                resp = urllib.request.urlopen(req)
                return json.load(resp)["id"]
            except urllib.error.HTTPError as e:
                if e.code != 308:
                    raise
            ini = fim + 1
            print(f"  {100 * ini // tam}%", end="", flush=True)
    raise RuntimeError("upload terminou sem resposta do Drive")


def cmd_upload(args):
    substituir = "--substituir" in args
    args = [a for a in args if a != "--substituir"]
    pasta, arquivos = args[0], args[1:]
    tk, _ = token()
    for i, arq in enumerate(arquivos, 1):
        nome = os.path.basename(arq)
        print(f"[{i}/{len(arquivos)}] {nome}", flush=True)
        if substituir:
            for velho in listar(tk, pasta, nome):
                chamar(tk, "PATCH", f"{API}/{velho['id']}?supportsAllDrives=true", corpo={"trashed": True})
                print(f"  versão antiga na lixeira: {velho['id']}")
        fid = subir(tk, pasta, arq)
        print(f"\n  OK id={fid}", flush=True)


def cmd_trocar(args):
    arquivo_id, caminho = args
    tk, _ = token()
    print(f"trocando o conteúdo de {arquivo_id} por {os.path.basename(caminho)}", flush=True)
    fid = subir(tk, None, caminho, arquivo_id)
    print(f"\n  OK id={fid} (mesmo link, versão antiga no histórico do Drive)", flush=True)


def cmd_pasta(args):
    pai, nome = args
    tk, _ = token()
    existe = listar(tk, pai, nome, PASTA_MIME)
    if existe:
        print(existe[0]["id"])
        return
    r = json.load(chamar(tk, "POST", API + "?supportsAllDrives=true&fields=id",
                         corpo={"name": nome, "mimeType": PASTA_MIME, "parents": [pai]}))
    print(r["id"])


def cmd_renomear(args):
    fid, nome = args
    tk, _ = token()
    chamar(tk, "PATCH", f"{API}/{fid}?supportsAllDrives=true", corpo={"name": nome})
    print(f"OK: {nome}")


def filhos(tk, pasta):
    url = API + "?" + urllib.parse.urlencode({
        "q": f"'{pasta}' in parents and trashed = false", "pageSize": "1000", "orderBy": "name",
        "fields": "files(id,name,mimeType,size,videoMediaMetadata)", "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true"})
    return json.load(chamar(tk, "GET", url))["files"]


def cmd_listar(args):
    tk, _ = token()
    for f in filhos(tk, args[0]):
        d = int(f.get("videoMediaMetadata", {}).get("durationMillis", 0)) / 1000
        print(f"{f['id']} | {f['name']} | {int(f.get('size', 0)) / 1e6:.0f} MB | {d:.1f} s")


def baixar_arquivo(tk, fid, destino, tamanho=None, tentativas=5):
    """Baixa em blocos (vídeo grande), retomando de onde parou se a conexão cair, e só renomeia
    no fim: arquivo pela metade nunca fica com o nome final (a conexão às vezes fecha sem erro
    e o .MOV ficava truncado, "moov atom not found")."""
    tmp = destino + ".parcial"
    open(tmp, "wb").close()
    for _ in range(tentativas):
        feito = os.path.getsize(tmp)
        h = {"Range": f"bytes={feito}-"} if feito else {}
        try:
            with chamar(tk, "GET", f"{API}/{fid}?alt=media&supportsAllDrives=true", cabecalhos=h) as r, \
                    open(tmp, "ab") as f:
                while True:
                    bloco = r.read(1024 * 1024)
                    if not bloco:
                        break
                    f.write(bloco)
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            print(f"  conexão caiu ({e}), retomando...", flush=True)
        if tamanho is None or os.path.getsize(tmp) >= tamanho:
            break
    if tamanho is not None and os.path.getsize(tmp) != tamanho:
        raise RuntimeError(f"download incompleto: {destino} ({os.path.getsize(tmp)} de {tamanho} bytes)")
    os.replace(tmp, destino)


def cmd_baixar(args):
    from concurrent.futures import ThreadPoolExecutor
    alvo, destino = args
    tk, _ = token()
    os.makedirs(destino, exist_ok=True)
    meta = json.load(chamar(tk, "GET", f"{API}/{alvo}?supportsAllDrives=true&fields=id,name,mimeType,size"))
    itens = filhos(tk, alvo) if meta["mimeType"] == PASTA_MIME else [meta]
    itens = [f for f in itens if f["mimeType"] != PASTA_MIME]

    def um(f):
        caminho = os.path.join(destino, f["name"])
        if os.path.exists(caminho) and os.path.getsize(caminho) == int(f.get("size", -1)):
            return f"já existe: {f['name']}"
        baixar_arquivo(tk, f["id"], caminho, int(f["size"]) if "size" in f else None)
        return f"OK: {f['name']} ({os.path.getsize(caminho) / 1e6:.0f} MB)"

    with ThreadPoolExecutor(4) as ex:
        for msg in ex.map(um, itens):
            print(msg, flush=True)


def cmd_testar(_):
    _, escopos = token()
    print("acesso OK. escopos:", escopos)
    print("Drive inteiro:", "sim" if "auth/drive " in escopos + " " else "não (só arquivos criados pelo app)")
    print("Sheets:", "sim" if "spreadsheets" in escopos else "não")


if __name__ == "__main__":
    cmds = {"upload": cmd_upload, "pasta": cmd_pasta, "renomear": cmd_renomear, "testar": cmd_testar,
            "baixar": cmd_baixar, "listar": cmd_listar, "trocar": cmd_trocar}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
