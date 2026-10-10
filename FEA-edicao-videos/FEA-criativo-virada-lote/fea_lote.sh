#!/usr/bin/env bash
# FEA: roda o lote inteiro de criativos de virada de lote (quadros, áudio, montagem).
# Uso: bash fea_lote.sh PASTA_TRABALHO NOME1 [NOME2 ...]
# PASTA_TRABALHO precisa de: brutos/NOME.MOV, cfg/NOME.json (fea_configs.py), comp/ (composição + imagens), fonts/
set -euo pipefail
W=$1; shift; AQUI=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W/aud" "$W/saida"
for N in "$@"; do
  rm -rf "$W/quadros/$N"
  node "$AQUI/fea_render_quadros.js" "$W/comp" "$W/cfg/$N.json" "$W/quadros/$N" all
  python3 "$AQUI/fea_audio.py" "$W/cfg/$N.json" "$W/aud/${N}_sfx.wav" "$W/aud/${N}_trilha.wav"
  bash "$AQUI/fea_montar.sh" "$W/brutos/$N.MOV" "$W/quadros/$N" "$W/cfg/$N.json" "$W/aud/${N}_sfx.wav" "$W/aud/${N}_trilha.wav" "$W/saida/$N.mp4"
  rm -rf "$W/quadros/$N"
  echo "--- FEITO: $N ---"
done
