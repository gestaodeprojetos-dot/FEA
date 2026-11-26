#!/usr/bin/env bash
# Extrai um quadro a cada 0,5 s de um rascunho e monta uma folha de contato para revisão.
# Uso: fea_frames_rascunho.sh video.mp4 [pasta_saida]
set -euo pipefail
in="$1"; out="${2:-$(dirname "$in")/frames-$(basename "${in%.*}")}"
mkdir -p "$out"
ffmpeg -y -loglevel error -i "$in" -vf "fps=2,scale=360:-1" "$out/q_%03d.jpg"
n=$(ls "$out"/q_*.jpg | wc -l); cols=6; rows=$(( (n + cols - 1) / cols ))
ffmpeg -y -loglevel error -i "$in" -vf "fps=2,scale=240:-1,tile=${cols}x${rows}" -frames:v 1 "$out/folha-de-contato.jpg"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
echo "duração: $dur s · $n quadros em $out · folha: $out/folha-de-contato.jpg"
ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$in" | grep -q . && echo "tem áudio" || echo "sem áudio"
