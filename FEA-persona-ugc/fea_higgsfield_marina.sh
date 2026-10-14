#!/usr/bin/env bash
# FEA, persona UGC fictícia "Marina": gera retratos no Higgsfield Soul V2 via API oficial.
# Credenciais lidas do ambiente (nunca hardcoded): HF_API_KEY_ID e HF_API_KEY_SECRET.
# Uso: ./fea_higgsfield_marina.sh [A|B|C|todas] [--estimar]
set -euo pipefail

: "${HF_API_KEY_ID:?Defina HF_API_KEY_ID no ambiente}"
: "${HF_API_KEY_SECRET:?Defina HF_API_KEY_SECRET no ambiente}"

API="https://api.higgsfield.ai"
ENDPOINT="higgsfield-ai/soul/v2/standard"
AUTH="Authorization: Key ${HF_API_KEY_ID}:${HF_API_KEY_SECRET}"
OUT="$(cd "$(dirname "$0")" && pwd)/output"
mkdir -p "$OUT"

BASE_1="Extreme close-up front-camera selfie, face filling most of the frame, a breathtakingly beautiful Brazilian woman, 28,"
BASE_2="naturally flushed cheeks, glossy nude-pink lips, mid-sentence genuine smile showing teeth, leaning slightly toward the camera, thin black tank top, dim cozy room behind her with a plant and warm lamp light, soft daylight on her face from a window, real skin texture with visible pores, peach fuzz, tiny imperfections, no makeup look, iPhone front camera, slight motion blur, candid, unedited, authentic UGC."

declare -A LOOK=(
  [A]="honey-brown hair in a messy high bun with loose strands framing her face, striking light hazel-green eyes looking directly into the lens, soft freckles across the nose,"
  [B]="long dark brown wavy hair loosely tied, deep warm brown eyes with golden highlights looking directly into the lens,"
  [C]="copper-red hair in a messy bun, light blue-grey eyes looking directly into the lens, pronounced freckles,"
)

VARIANTE="${1:-todas}"
ESTIMAR="${2:-}"
[[ "$VARIANTE" == "todas" ]] && LISTA=(A B C) || LISTA=("$VARIANTE")

for V in "${LISTA[@]}"; do
  BODY=$(jq -n --arg p "$BASE_1 ${LOOK[$V]} $BASE_2" \
    '{prompt:$p, aspect_ratio:"9:16", resolution:"1080p", enhance_prompt:false, batch_size:4}')

  if [[ "$ESTIMAR" == "--estimar" ]]; then
    echo "Variante $V, custo estimado:"
    curl -sS --fail-with-body -X POST "$API/estimate/$ENDPOINT" -H "$AUTH" -H "Content-Type: application/json" -d "$BODY" | jq
    continue
  fi

  RESP=$(curl -sS --fail-with-body -X POST "$API/$ENDPOINT" -H "$AUTH" \
    -H "Content-Type: application/json" -H "Idempotency-Key: $(cat /proc/sys/kernel/random/uuid)" -d "$BODY")
  REQ=$(jq -r '.request_id' <<<"$RESP")
  echo "Variante $V enviada, request $REQ"

  ESPERA=5
  while :; do
    ST=$(curl -sS --fail-with-body "$API/requests/$REQ/status" -H "$AUTH")
    S=$(jq -r '.status' <<<"$ST")
    case "$S" in
      completed)
        i=1
        for URL in $(jq -r '.images[].url' <<<"$ST"); do
          curl -sSL "$URL" -o "$OUT/FEA-marina-$V-$i.jpg"; echo "  salvo FEA-marina-$V-$i.jpg"; i=$((i+1))
        done
        break ;;
      failed|nsfw|canceled) echo "  Variante $V terminou como $S"; break ;;
      *) sleep "$ESPERA"; ESPERA=$(( ESPERA < 30 ? ESPERA*2 : 30 )) ;;
    esac
  done
done
