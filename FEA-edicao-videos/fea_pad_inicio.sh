#!/usr/bin/env bash
# FEA: bruto que já começa com o Dr. falando a frase-gancho (o iPhone começou a gravar no meio da fala).
# Regra da Keila (16/11/2026): o vídeo abre 0,25 a 0,40 s antes da voz. Este script cria um bruto
# intermediário com PAD segundos de 1º quadro congelado e silêncio no começo (fica embaixo do título),
# em H.264 CRF 10 (perda imperceptível) e áudio PCM, e desloca a transcrição pelo mesmo tempo.
# Uso: bash fea_pad_inicio.sh FFMPEG BRUTO.MOV TRANSCRICAO.json PAD SAIDA.mov SAIDA.json
set -euo pipefail
FF="$1"; IN="$2"; TR="$3"; PAD="$4"; OUT="$5"; TROUT="$6"
MS=$(python3 -c "print(int(round($PAD*1000)))")
"$FF" -nostdin -v error -y -i "$IN" -filter_complex \
  "[0:v]tpad=start_duration=$PAD:start_mode=clone[v];[0:a]adelay=$MS:all=1,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 10 -pix_fmt yuv420p -r 30 -c:a pcm_s16le "$OUT"
python3 - "$TR" "$PAD" "$TROUT" <<'PY'
import json, sys
t = json.load(open(sys.argv[1])); d = float(sys.argv[2])
for s in t:
    for k in ("start", "end"):
        if k in s: s[k] = round(s[k] + d, 3)
    for w in s["words"]:
        w["s"] = round(w["s"] + d, 3); w["e"] = round(w["e"] + d, 3)
json.dump(t, open(sys.argv[3], "w"), ensure_ascii=False)
PY
echo "ok: $OUT (+$PAD s)"
