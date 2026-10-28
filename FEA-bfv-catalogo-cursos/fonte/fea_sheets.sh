#!/bin/bash
# uso: fea_sheets.sh nome drive_id  -> folha com 8 quadros espalhados do vídeo
OUT=/tmp/claude-0/-home-user-FEA/570307b6-bb2f-5ff2-b02a-3f6fff2d3202/scratchpad/bfv2/sheets
N=$1; ID=$2
U="https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$U" | cut -d. -f1)
T=$(mktemp -d)
for k in 1 2 3 4 5 6 7 8; do
  s=$(( D * k / 9 ))
  ffmpeg -v error -y -ss $s -i "$U" -frames:v 1 -vf "scale=480:-1,drawtext=text='$N  ${s}s':x=6:y=6:fontcolor=yellow:fontsize=20:box=1:boxcolor=black@0.6" $T/$k.jpg
done
ffmpeg -v error -y -i $T/%d.jpg -vf "tile=4x2" -frames:v 1 $OUT/$N.jpg
echo "$N dur=${D}s"
rm -rf $T
