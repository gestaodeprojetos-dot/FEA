#!/usr/bin/env python3
"""FEA: envia arquivos grandes (vídeos) para uma pasta do Google Drive.

Uso:
    python3 FEA-edicao-videos/fea_subir_drive.py ID_DA_PASTA arquivo1.mp4 [arquivo2.mp4 ...]

Autentica com a conta de serviço fea-upload-69@fea-edicao-videos.iam.gserviceaccount.com.
A chave JSON vem da variável de ambiente FEA_DRIVE_SA_KEY (conteúdo do JSON), configurada
nas configurações do ambiente na nuvem. Nunca gravar a chave em arquivo do repositório.
Envio "resumable" em blocos de 8 MB, sem limite prático de tamanho.
"""
import json
import mimetypes
import os
import sys

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

ESCOPO = ["https://www.googleapis.com/auth/drive"]
BLOCO = 8 * 1024 * 1024
API = "https://www.googleapis.com/upload/drive/v3/files"


def credenciais():
    bruto = os.environ.get("FEA_DRIVE_SA_KEY")
    if not bruto:
        sys.exit("ERRO: variável FEA_DRIVE_SA_KEY ausente. Configure a chave da conta de serviço "
                 "nas configurações do ambiente e abra uma sessão nova.")
    cred = service_account.Credentials.from_service_account_info(json.loads(bruto), scopes=ESCOPO)
    cred.refresh(Request())
    return cred


def enviar(cred, pasta, caminho):
    nome = os.path.basename(caminho)
    tamanho = os.path.getsize(caminho)
    tipo = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
    inicio = requests.post(
        f"{API}?uploadType=resumable&supportsAllDrives=true&fields=id,name,webViewLink",
        headers={"Authorization": f"Bearer {cred.token}",
                 "X-Upload-Content-Type": tipo,
                 "X-Upload-Content-Length": str(tamanho)},
        json={"name": nome, "parents": [pasta]},
        timeout=60,
    )
    inicio.raise_for_status()
    sessao = inicio.headers["Location"]

    with open(caminho, "rb") as f:
        enviado = 0
        while enviado < tamanho:
            dados = f.read(BLOCO)
            fim = enviado + len(dados) - 1
            r = requests.put(sessao, data=dados, timeout=300, headers={
                "Content-Range": f"bytes {enviado}-{fim}/{tamanho}"})
            if r.status_code not in (200, 201, 308):
                r.raise_for_status()
            enviado = fim + 1
            print(f"  {nome}: {enviado * 100 // tamanho}%", flush=True)
    info = r.json()
    print(f"OK {info['name']} -> {info.get('webViewLink', info['id'])}", flush=True)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta, arquivos = sys.argv[1], sys.argv[2:]
    cred = credenciais()
    for caminho in arquivos:
        enviar(cred, pasta, caminho)


if __name__ == "__main__":
    main()
