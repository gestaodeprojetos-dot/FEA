#!/usr/bin/env bash
# Gera URL de autorização OAuth com escopo para editar planilhas Google Sheets.
# Executar uma única vez. Depois, salvar o REFRESH_TOKEN_SHEETS no .env.
#
# Requer GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET no .env (não hardcoded).
#
# Uso:
#   bash fea_setup_sheets_oauth.sh          # gera a URL
#   bash fea_setup_sheets_oauth.sh CODIGO   # troca o código pelo refresh token

set -euo pipefail

# Carrega .env
if [ -f .env ]; then set -a; source .env; set +a; fi
if [ -f "$(dirname "$0")/.env" ]; then set -a; source "$(dirname "$0")/.env"; set +a; fi

: "${GOOGLE_CLIENT_ID:?Defina GOOGLE_CLIENT_ID no .env}"
: "${GOOGLE_CLIENT_SECRET:?Defina GOOGLE_CLIENT_SECRET no .env}"

REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob"
SCOPES="https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/spreadsheets"

if [ -z "${1:-}" ]; then
    ENCODED_SCOPES=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SCOPES'))")
    echo "Abra este link no navegador e autorize:"
    echo ""
    echo "https://accounts.google.com/o/oauth2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${ENCODED_SCOPES}&access_type=offline&prompt=consent"
    echo ""
    echo "Depois, cole o código aqui:"
    echo "  bash fea_setup_sheets_oauth.sh CODIGO_AQUI"
else
    CODE="$1"
    echo "Trocando código por refresh token..."
    curl -sS -X POST "https://oauth2.googleapis.com/token" \
      -d "client_id=${GOOGLE_CLIENT_ID}" \
      -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
      -d "code=${CODE}" \
      -d "redirect_uri=${REDIRECT_URI}" \
      -d "grant_type=authorization_code" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'refresh_token' in data:
    print('REFRESH_TOKEN_SHEETS=' + data['refresh_token'])
    print()
    print('Adicione essa linha no .env do projeto.')
else:
    print('ERRO:', json.dumps(data, indent=2))
"
fi
