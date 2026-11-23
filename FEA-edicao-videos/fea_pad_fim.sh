#!/usr/bin/env bash
# FEA: bruto que termina colado na última palavra do Dr. (o iPhone parou de gravar logo depois da
# frase que conclui a ação, ex.: "Finito." no último quadro) ou com o começo de outra palavra logo
# depois dela. Regra da Keila (23/11/2026): o vídeo termina DEPOIS que o Dr. conclui a última frase e
# a ação, com 0,3 a 0,6 s de respiro. Este script cria um bruto intermediário cortado em CORTE (no
# respiro, antes de qualquer outro som) e com PAD segundos do último quadro congelado e silêncio no
# fim (fica embaixo do fade_final), em H.264 CRF 10 e áudio PCM. A transcrição não muda de tempo
# (só perde as palavras depois do corte).
# Uso: bash fea_pad_fim.sh FFMPEG BRUTO TRANSCRICAO.json CORTE PAD SAIDA.mov SAIDA.json
set -euo pipefail
FF="$1"; IN="$2"; TR="$3"; CORTE="$4"; PAD="$5"; OUT="$6"; TROUT="$7"
"$FF" -nostdin -v error -y -i "$IN" -filter_complex \
  "[0:v]trim=0:$CORTE,setpts=PTS-STARTPTS,tpad=stop_duration=$PAD:stop_mode=clone[v];[0:a]atrim=0:$CORTE,asetpts=PTS-STARTPTS,aresample=48000,apad=pad_dur=$PAD[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 10 -pix_fmt yuv420p -r 30 -c:a pcm_s16le "$OUT"
python3 - "$TR" "$CORTE" "$TROUT" <<'PY'
import json, sys
t = json.load(open(sys.argv[1])); c = float(sys.argv[2])
for s in t:
    s["words"] = [w for w in s["words"] if w["s"] < c]
    for w in s["words"]:
        w["e"] = min(w["e"], c)
t = [s for s in t if s["words"]]
json.dump(t, open(sys.argv[3], "w"), ensure_ascii=False)
PY
echo "ok: $OUT (corte em $CORTE s + $PAD s congelado)"
