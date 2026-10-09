#!/usr/bin/env bash
# FEA: monta o criativo de virada de lote (vídeo do Dr. + quadros animados + efeitos).
# Uso: bash fea_montar.sh BRUTO.MOV PASTA_QUADROS SFX.wav SAIDA.mp4 DURACAO "ZOOM_ENABLE"
# ZOOM_ENABLE: trechos com zoom no rosto, ex.: "between(t,4.36,7.22)+between(t,15.0,16.6)"
# Os PNG do Chromium saem RGB quando o quadro é opaco; converter tudo para RGBA antes,
# senão o FFmpeg para a sequência no primeiro quadro opaco (vídeo saía com 10 s).
set -euo pipefail
BRUTO=$1; QUADROS=$2; SFX=$3; SAIDA=$4; DUR=$5; ZOOM=$6
python3 -c "
import glob,sys
from PIL import Image
for f in glob.glob('$QUADROS/f_*.png'):
    im=Image.open(f)
    if im.mode!='RGBA': im.convert('RGBA').save(f,compress_level=1)"
ffmpeg -v error -y -i "$BRUTO" -framerate 30 -i "$QUADROS/f_%05d.png" -i "$SFX" -filter_complex "\
[0:v]fps=30,scale=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=5,trim=0:$DUR,setpts=PTS-STARTPTS,split[b][z];\
[z]scale=1210:2152,crop=1080:1920:65:88[zz];\
[b][zz]overlay=0:0:enable='$ZOOM'[v1];\
[v1][1:v]overlay=0:0:format=auto,format=yuv420p[v];\
[0:a]aresample=48000,apad,atrim=0:$DUR[voz];[2:a]volume=0.5[fx];\
[voz][fx]amix=inputs=2:duration=first:normalize=0[a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p \
-c:a aac -b:a 192k -ar 48000 -movflags +faststart -t "$DUR" "$SAIDA"
