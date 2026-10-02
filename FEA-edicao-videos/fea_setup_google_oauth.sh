#!/usr/bin/env bash
# Autoriza o app FEA no Google com Drive inteiro + Google Sheets (uma vez só).
# Lê FEA_GDRIVE_CLIENT_ID e FEA_GDRIVE_CLIENT_SECRET das variáveis do ambiente.
#
# Uso:
#   bash fea_setup_google_oauth.sh                       # 1. imprime o link para a Keila autorizar
#   bash fea_setup_google_oauth.sh "ENDERECO_LOCALHOST"  # 2. troca o código pelo acesso
#
# No passo 2 o novo FEA_GDRIVE_REFRESH_TOKEN vai para o arquivo FEA-novo-acesso-google.txt
# (fora do git), para colar nas variáveis do ambiente. Nunca sai no terminal.

set -euo pipefail

: "${FEA_GDRIVE_CLIENT_ID:?falta FEA_GDRIVE_CLIENT_ID nas variáveis do ambiente}"
: "${FEA_GDRIVE_CLIENT_SECRET:?falta FEA_GDRIVE_CLIENT_SECRET nas variáveis do ambiente}"

REDIRECT_URI="http://localhost"
SCOPES="https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/spreadsheets"
SAIDA="${FEA_OAUTH_SAIDA:-$(pwd)/FEA-novo-acesso-google.txt}"

if [ -z "${1:-}" ]; then
    python3 - <<EOF
import urllib.parse
print("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": "$FEA_GDRIVE_CLIENT_ID", "redirect_uri": "$REDIRECT_URI",
    "response_type": "code", "scope": "$SCOPES",
    "access_type": "offline", "prompt": "consent"}))
EOF
    exit 0
fi

ENTRADA="$1" SAIDA="$SAIDA" REDIRECT_URI="$REDIRECT_URI" python3 - <<'EOF'
import json, os, sys, urllib.error, urllib.parse, urllib.request
entrada = os.environ["ENTRADA"].strip()
codigo = urllib.parse.parse_qs(urllib.parse.urlparse(entrada).query).get("code", [entrada])[0]
dados = urllib.parse.urlencode({
    "client_id": os.environ["FEA_GDRIVE_CLIENT_ID"],
    "client_secret": os.environ["FEA_GDRIVE_CLIENT_SECRET"],
    "code": codigo, "redirect_uri": os.environ["REDIRECT_URI"],
    "grant_type": "authorization_code"}).encode()
try:
    r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", dados))
except urllib.error.HTTPError as e:
    sys.exit(f"ERRO {e.code}: {e.read().decode()[:300]}")
if "refresh_token" not in r:
    sys.exit("ERRO: o Google não devolveu refresh_token. Gere o link de novo e autorize outra vez.")
fd = os.open(os.environ["SAIDA"], os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as f:
    f.write(f"FEA_GDRIVE_REFRESH_TOKEN={r['refresh_token']}\n")
print("OK. Escopos:", r.get("scope"))
print("Novo acesso salvo em:", os.environ["SAIDA"])
EOF
