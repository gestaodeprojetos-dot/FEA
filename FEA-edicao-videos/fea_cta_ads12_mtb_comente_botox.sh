#!/usr/bin/env bash
# FEA: monta o CTA "Ads 12 MTB + Comente BOTOX digitando" (04/11/2026, pedido da Keila para
# novembro, pastas 2 em diante; a pasta 1 fica só com a cartela).
#
# Ads 12 - MTB.mov (Drive 1QedZKCbRoBUxSlesYPP0RUqrzV412o5N, 28,63 s, 859 quadros, 30 fps, legenda
# queimada, AAC 44,1 kHz; é o post https://www.instagram.com/p/DfSqd6VA4Wj/) até o quadro 603
# (20,133 s) + FEA-CTA-digitando-comente-botox-MTB.mp4 (Drive 1q0-UodYgi8FQpz4d1ViSCQwtMipBKmmx, 5,00 s)
# inteira.
#
# Corte: última fala mantida "Esse evento vai ser 100% ao vivo, gratuito e online e ele não vai ter
# reprise." (voz termina em ~20,07 s). Sai "Toque em saiba mais, se inscreve que eu te vejo no grupo
# do WhatsApp." (voz em ~20,33 s; legenda "Toque em SAIBA MAIS" a partir do quadro 610) e a vinheta
# final "MASTERCLASS em Toxina Botulínica / TOQUE EM SAIBA MAIS" (de ~23,9 s ao fim). No quadro 604
# há um corte seco de plano (jump cut) e a legenda "e ele não vai ter reprise." termina no 603: o
# corte cai nessa troca, no respiro, sem frase pela metade. Áudio com fade de 60 ms (20,073 a
# 20,133 s) na cauda da voz e da trilha, sem estalo; a cartela já começa preta e em silêncio.
#
# Codificação igual à da cartela (x264 preset slow, CRF 18, High, sem marcação de cor) para que o
# SPS/PPS do CTA novo seja o mesmo e ele cole por stream copy no fim dos vídeos entregues.
#
# Uso: bash fea_cta_ads12_mtb_comente_botox.sh "Ads 12 - MTB.mov" FEA-CTA-digitando-comente-botox-MTB.mp4 SAIDA.mp4
set -euo pipefail
ADS="${1:?Ads 12}"; CART="${2:?cartela digitando MTB}"; OUT="${3:?saída}"
ffmpeg -v error -y -i "$ADS" -i "$CART" -filter_complex "\
[0:v]trim=end_frame=604,setpts=PTS-STARTPTS,fps=30,scale=1080:1920,format=yuv420p,setsar=0,setparams=range=unknown:color_primaries=unknown:color_trc=unknown:colorspace=unknown[v0];\
[0:a]atrim=0:20.133333,asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,\
afade=t=out:st=20.073333:d=0.06[a0];\
[1:v]fps=30,scale=1080:1920,format=yuv420p,setsar=0,setparams=range=unknown:color_primaries=unknown:color_trc=unknown:colorspace=unknown,setpts=PTS-STARTPTS[v1];\
[1:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -r 30 \
  -color_primaries unknown -color_trc unknown -colorspace unknown -color_range unknown \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -map_metadata -1 "$OUT"
ffprobe -v error -show_entries stream=codec_name,duration,nb_frames -of compact "$OUT"
