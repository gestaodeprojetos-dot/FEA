#!/usr/bin/env bash
# FEA: prepara o ambiente do modelo notícia numa pasta de trabalho.
# Uso: bash fea_preparar_ambiente.sh PASTA_DE_TRABALHO
# Cria PASTA/fonts (Sora e Montserrat, licença OFL), PASTA/models/sh.rnnn (RNNoise),
# PASTA/musica (Mixkit, licença livre para redes sociais) e instala as bibliotecas Python.
set -euo pipefail
T="${1:?informe a pasta de trabalho}"
mkdir -p "$T"/{fonts,models,musica,dl,tr,prod,out,an}

f() { curl -fsSL -o "$T/fonts/$2" "https://cdn.jsdelivr.net/fontsource/fonts/$1"; }
f sora@latest/latin-600-normal.ttf Sora-600.ttf
f sora@latest/latin-700-normal.ttf Sora-700.ttf
f sora@latest/latin-800-normal.ttf Sora-800.ttf
# Montserrat do repositório oficial: o arquivo do fontsource vem com o nome interno "Montserrat Thin"
# e a legenda (libass procura "Montserrat Bold") cairia numa fonte reserva
for w in Medium SemiBold Bold ExtraBold; do
  curl -fsSL -o "$T/fonts/Montserrat-$w.ttf" \
    "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-$w.ttf"
done

curl -fsSL -o "$T/models/sh.rnnn" \
  https://raw.githubusercontent.com/GregorR/rnnoise-models/master/somnolent-hogwash-2018-09-01/sh.rnnn

# Música: neutra estilo notícia (temas tensos e vídeos de artigo) e "Cat Walk" (produtos e tratamentos)
curl -fsSL -o "$T/musica/mixkit_747.mp3" https://assets.mixkit.co/music/747/747.mp3
curl -fsSL -o "$T/musica/mixkit_cat_walk_371.mp3" https://assets.mixkit.co/music/371/371.mp3

# faster-whisper com o PyAV 15+ quebra ("open() got an unexpected keyword argument 'metadata_errors'"):
# fixar o av entre 12 e 14
python3 -m pip install -q numpy pillow scipy faster-whisper
python3 -m pip install -q --only-binary :all: "av>=12,<15"
if command -v ffmpeg >/dev/null; then
  echo "ffmpeg: $(command -v ffmpeg)  (use esse caminho na chave \"ffmpeg\" do projeto)"
else
  python3 -m pip install -q imageio-ffmpeg
  echo "ffmpeg: $(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')"
fi
command -v pdftoppm >/dev/null || echo "AVISO: instale poppler-utils (pdftoppm, pdftotext) para vídeos de artigo"
echo "Pronto: $T"
