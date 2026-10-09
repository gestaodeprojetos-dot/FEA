#!/usr/bin/env bash
# FEA: monta o criativo de virada de lote (vídeo do Dr. + quadros animados + efeitos + trilha).
# Uso: bash fea_montar.sh BRUTO.MOV PASTA_QUADROS CFG.json SFX.wav TRILHA.wav SAIDA.mp4
# Os PNG do Chromium saem RGB quando o quadro é opaco; converter tudo para RGBA antes,
# senão o FFmpeg para a sequência no primeiro quadro opaco (vídeo saía com 10 s).
# Trilha "de leve" (Keila, 09/10/2026): volume baixo e abaixando sozinha quando o Dr. fala.
set -euo pipefail
BRUTO=$1; QUADROS=$2; CFG=$3; SFX=$4; TRILHA=$5; SAIDA=$6
read DUR FIMFALA ZOOM < <(python3 -c "
import json; c=json.load(open('$CFG'))
print(c['dur'], c['fim_fala'], '+'.join(f'between(t,{a},{b})' for a,b in c['zoom']) or '0')")
python3 -c "
import glob
from PIL import Image
for f in glob.glob('$QUADROS/f_*.png'):
    im=Image.open(f)
    if im.mode!='RGBA': im.convert('RGBA').save(f,compress_level=1)"
ffmpeg -v error -y -i "$BRUTO" -framerate 30 -i "$QUADROS/f_%05d.png" -i "$SFX" -i "$TRILHA" -filter_complex "\
[0:v]fps=30,scale=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=5,trim=0:$DUR,setpts=PTS-STARTPTS,split[b][z];\
[z]scale=1210:2152,crop=1080:1920:65:88[zz];\
[b][zz]overlay=0:0:enable='$ZOOM'[v1];\
[v1][1:v]overlay=0:0:format=auto,format=yuv420p[v];\
[0:a]aresample=48000,apad,atrim=0:$DUR,afade=t=out:st=$FIMFALA:d=0.3,asplit[voz][chave];\
[2:a]volume=0.5[fx];\
[3:a]volume=0.2[mus0];[mus0][chave]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350[mus];\
[voz][fx][mus]amix=inputs=3:duration=first:normalize=0[a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p \
-c:a aac -b:a 192k -ar 48000 -movflags +faststart -t "$DUR" "$SAIDA"
