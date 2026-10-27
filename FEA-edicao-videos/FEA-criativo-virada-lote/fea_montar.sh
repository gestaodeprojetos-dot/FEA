#!/usr/bin/env bash
# FEA: monta o criativo animado (vídeo do Dr. + quadros animados + efeitos + trilha [+ CTA no fim]).
# Uso: bash fea_montar.sh BRUTO PASTA_QUADROS CFG.json SFX.wav TRILHA.wav SAIDA.mp4 [CTA.mp4]
# Do CFG: dur, fim_fala, zoom, inicio (corta o começo do bruto), tremor (imagem tremendo, abertura "ATENÇÃO").
# Os PNG do Chromium saem RGB quando o quadro é opaco; converter tudo para RGBA antes,
# senão o FFmpeg para a sequência no primeiro quadro opaco (vídeo saía com 10 s).
# Trilha "de leve" (Keila, 09/10/2026): volume baixo e abaixando sozinha quando o Dr. fala.
set -euo pipefail
BRUTO=$1; QUADROS=$2; CFG=$3; SFX=$4; TRILHA=$5; SAIDA=$6; CTA=${7:-}
read DUR FIMFALA INICIO VOLTRILHA ZOOM TREMOR CORTE < <(python3 -c "
import json; c=json.load(open('$CFG'))
m=c.get('manter') or [(c.get('inicio',0),9999)]
# trechos mantidos do bruto (corte do começo e cortes no meio). Vídeo num select só: vários trim do mesmo
# [0:v] juntados com concat guardam os quadros na memória e o FFmpeg morria (Killed) com 3 ou mais cortes.
sel='+'.join(f'between(t,{a},{b})' for a,b in m)
v='[0:v]fps=30,select='+chr(39)+sel+chr(39)+',setpts=N/30/TB[src];'
a=''.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i,(a,b) in enumerate(m))
corte=v+a+''.join(f'[a{i}]' for i in range(len(m)))+f'concat=n={len(m)}:v=0:a=1[srca];'

z='+'.join(f'between(t,{a},{b})' for a,b in c['zoom']+c.get('tremor',[])) or '0'
tr='+'.join(f'between(t,{a},{b})' for a,b in c.get('tremor',[])) or '0'
print(c['dur'], c['fim_fala'], c.get('inicio',0), c.get('vol_trilha',0.2), z, tr, corte)")
python3 -c "
import glob
from PIL import Image
for f in glob.glob('$QUADROS/f_*.png'):
    im=Image.open(f)
    if im.mode!='RGBA': im.convert('RGBA').save(f,compress_level=1)"
TMP=$(mktemp -d)
# imagens de apoio ("inserts": [{s, e, src, de}], tempos do vídeo editado): vídeo de outro arquivo em tela cheia,
# sem som, por baixo das animações e da legenda. crop_h corta a legenda gravada no vídeo de apoio (visita técnica).
python3 - "$CFG" "$TMP" <<'PY'
import json, sys
c = json.load(open(sys.argv[1])); ins = c.get('inserts', [])
args, filt = [], ''
for k, x in enumerate(ins):
    args += ['-ss', str(x['de']), '-t', str(round(x['e'] - x['s'] + .1, 3)), '-i', x['src']]
    ch = x.get('crop_h', 1920)
    filt += (f"[{4 + k}:v]fps=30,crop=1080:{ch}:0:0,scale=-2:1920,crop=1080:1920,setsar=1,"
             f"setpts=PTS-STARTPTS+{x['s']}/TB[ins{k}];[vi{k}][ins{k}]overlay=0:0:eof_action=pass:enable='between(t,{x['s']},{x['e']})'[vi{k + 1}];")
open(sys.argv[2] + '/args', 'w').write('\n'.join(args))
open(sys.argv[2] + '/filt', 'w').write(filt + f"[vi{len(ins)}]null[v1]")
PY
mapfile -t INS < "$TMP/args"; INSF=$(cat "$TMP/filt")
ffmpeg -v error -y -i "$BRUTO" -framerate 30 -i "$QUADROS/f_%05d.png" -i "$SFX" -i "$TRILHA" "${INS[@]}" -filter_complex "$CORTE\
[src]fps=30,scale=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=5,trim=0:$DUR,setpts=PTS-STARTPTS,split[b][z];\
[z]scale=1210:2152,crop=1080:1920:'65+if($TREMOR,18*sin(t*97),0)':'88+if($TREMOR,14*cos(t*83),0)'[zz];\
[b][zz]overlay=0:0:enable='$ZOOM'[vi0];$INSF;\
[v1][1:v]overlay=0:0:format=auto,format=yuv420p[v];\
[srca]aresample=48000,apad,atrim=0:$DUR,afade=t=out:st=$FIMFALA:d=0.3,asplit[voz][chave];\
[2:a]volume=0.5[fx];\
[3:a]volume=$VOLTRILHA[mus0];[mus0][chave]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350[mus];\
[voz][fx][mus]amix=inputs=3:duration=first:normalize=0,aformat=channel_layouts=stereo[a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p \
-c:a aac -b:a 192k -ar 48000 -movflags +faststart -t "$DUR" "$TMP/corpo.mp4"
if [ -n "$CTA" ]; then
  # CTA da campanha no fim (já em 1080x1920, 30 fps, AAC 48 kHz estéreo)
  ffmpeg -v error -y -i "$TMP/corpo.mp4" -i "$CTA" -filter_complex \
    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 \
    -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$SAIDA"
else
  mv "$TMP/corpo.mp4" "$SAIDA"
fi
rm -rf "$TMP"
