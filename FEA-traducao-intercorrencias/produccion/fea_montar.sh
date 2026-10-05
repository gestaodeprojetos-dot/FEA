#!/usr/bin/env bash
# Monta o PDF espanhol do livro de Intercorrências do zero, a partir do original e do mapa.
set -euo pipefail
cd "$(dirname "$0")/.."
S=../.claude/skills/fea-traduccion-es/scripts
OUT=${1:-produccion/FEA-Intercurrencias-ES.pdf}
python3 $S/traduzir_pdf.py original.pdf produccion/mapa-es.json --fontes fontes --saida produccion/etapa1.pdf > produccion/log-refluxo.json 2>produccion/refluxo.err
python3 produccion/fea_display.py original.pdf produccion/etapa1.pdf produccion/etapa2.pdf
python3 produccion/fea_arte.py produccion/etapa2.pdf produccion/etapa3.pdf
python3 produccion/fea_rotulos.py produccion/etapa3.pdf produccion/etapa4.pdf
# QR de artigo quebrados no original: destinos confirmados (págs. 23, 61, 64, 68 e, só na 18, o HDPH)
python3 $S/atualizar_qr.py produccion/etapa4.pdf produccion/FEA-links-qr-corrigidos.json --paginas 23,61,64,68 --saida produccion/etapa5.pdf > produccion/log-qr.json
python3 $S/atualizar_qr.py produccion/etapa5.pdf produccion/FEA-links-qr-pag18.json --paginas 18 --saida produccion/etapa6.pdf >> produccion/log-qr.json
python3 - "$OUT" <<'PY'
import pymupdf, sys
d = pymupdf.open('produccion/etapa6.pdf'); d.subset_fonts()
d.set_metadata({**d.metadata, 'title': 'Intercurrencias en el relleno con ácido hialurónico', 'author': 'Dr. João Pithon'})
d.ez_save(sys.argv[1])
PY
rm -f produccion/etapa*.pdf
ls -la "$OUT"
