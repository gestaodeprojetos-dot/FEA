#!/usr/bin/env bash
# FEA: prepara a máquina para editar Reels (FFmpeg, Whisper e fontes Montserrat).
# Uso: bash fea_preparar_ambiente.sh PASTA_DE_TRABALHO
# Precisa de rede liberada para: pypi.org, huggingface.co (+ cdn-lfs.huggingface.co,
# cas-bridge.xethub.hf.co), raw.githubusercontent.com, drive.google.com e drive.usercontent.google.com.
set -euo pipefail
TRAB="${1:?informe a pasta de trabalho}"
mkdir -p "$TRAB/fonts"
pip install -q imageio-ffmpeg faster-whisper pillow numpy scipy 2>&1 | grep -v WARNING || true
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
echo "F=$FF" > "$TRAB/env.sh"
for p in ExtraBold Bold SemiBold Medium; do
  [ -s "$TRAB/fonts/Montserrat-$p.ttf" ] || curl -sSL -o "$TRAB/fonts/Montserrat-$p.ttf" \
    "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-$p.ttf"
done
mkdir -p "$TRAB/rnn"; [ -s "$TRAB/rnn/sh.rnnn" ] || curl -sSL -o "$TRAB/rnn/sh.rnnn" https://raw.githubusercontent.com/richardpl/arnndn-models/master/sh.rnnn
file "$TRAB"/fonts/*.ttf | grep -q "TrueType" || { echo "ERRO: fontes não baixaram"; exit 1; }
grep -q " ass " <<< "$("$FF" -hide_banner -filters 2>/dev/null)" || { echo "ERRO: FFmpeg sem libass"; exit 1; }
FEA_MODELOS="$TRAB/models" python3 -c "
from faster_whisper import WhisperModel
WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', download_root='$TRAB/models')" 2>&1 | grep -v Warning || true
echo "Ambiente pronto. FFmpeg: $FF"
