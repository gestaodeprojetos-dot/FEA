#!/usr/bin/env bash
# FEA: teste de credenciais dos WordPress via API REST (somente leitura).
# Lê WP_USER e WP_PASS_SITE / WP_PASS_FEB / WP_PASS_IFF / WP_PASS_FEF / WP_PASS_PL do ambiente.
# Nunca grava nem imprime senha. Só faz GET em /wp-json/wp/v2/users/me.
# O servidor tem WAF que devolve 406 para User-Agent genérico, por isso o UA de navegador.

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

sites=(
  "joaopithon.com.br|WP_PASS_SITE"
  "feb.joaopithon.com.br|WP_PASS_FEB"
  "iff.joaopithon.com.br|WP_PASS_IFF"
  "fef.joaopithon.com.br|WP_PASS_FEF"
  "pl.joaopithon.com.br|WP_PASS_PL"
)

printf "| Site | Variável | HTTP | Resultado |\n|------|----------|------|-----------|\n"

for item in "${sites[@]}"; do
  host="${item%%|*}"; var="${item##*|}"; pass="${!var}"
  if [[ -z "$WP_USER" || -z "$pass" ]]; then
    printf "| %s | %s | - | variável ausente |\n" "$host" "$var"; continue
  fi
  body=$(mktemp)
  code=$(curl -s -o "$body" -w "%{http_code}" -m 25 \
    -A "$UA" -H "Accept: application/json" \
    -u "$WP_USER:$pass" "https://$host/wp-json/wp/v2/users/me?context=edit")
  case "$code" in
    200) res="OK, logado como $(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('name','?'),'/',', '.join(d.get('roles',[])))" "$body" 2>/dev/null)";;
    401) res="credencial recusada (usuário ou senha de aplicativo errados)";;
    403) res="bloqueado (WAF ou plugin de segurança)";;
    406) res="bloqueado pelo WAF";;
    *)   res="erro inesperado";;
  esac
  rm -f "$body"
  printf "| %s | %s | %s | %s |\n" "$host" "$var" "$code" "$res"
done
