#!/usr/bin/env bash
# Prepara um áudio de fala para o vídeo: corta silêncio do começo e do fim,
# deixa 0,2 s de folga antes e 0,3 s depois, normaliza o volume e salva em mp3.
# Uso: fea_preparar_audio.sh entrada.(ogg|m4a|wav|mp3) saida.mp3
set -euo pipefail
in="$1"; out="$2"
ffmpeg -y -loglevel error -i "$in" -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,adelay=200,apad=pad_dur=0.3,loudnorm=I=-16:TP=-1.5" -ar 44100 -ac 1 -b:a 160k "$out"
printf '%s: %s s\n' "$out" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")"
