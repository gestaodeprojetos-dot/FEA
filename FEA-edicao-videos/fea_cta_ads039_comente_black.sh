#!/usr/bin/env bash
# FEA: monta o CTA "Ads 039 + Comente BLACK digitando" (28/10/2026, pendente aprovação da Keila).
#
# Ads 039 - Depoimento intercorrência labial - BFV.mp4 (Drive 117umHT5ZdBspGB3BqzblE-31H5oeyW63, 63,50 s, 30 fps)
# até o quadro 1237 (41,267 s) + FEA-CTA-digitando-comente-black.mp4 (Drive 1EsPTxpi2UHWzZlUtg5HQoNfilPRPw2OV, 5,00 s)
# inteira, sem re-renderizar a cartela.
#
# Corte: última fala mantida "...todos que eu for fazer até o fim da vida." (voz termina em 41,20 s).
# Sai "Se você quiser ter acesso ao combo Vitalício (...) você vai clicar em saiba mais (...)
# Te espero clicando aqui e a gente se vê lá." (voz começa em 41,53 s) e a vinheta final
# "Toque em Saiba Mais". Em 41,267 s (quadro 1238) há a troca de plano; a legenda queimada
# "da vida" vai até o quadro 1237 e "se você quiser ter acesso ao combo" só entra no 1240.
# Os quadros 1233 a 1237 são a dissolução da grade de cursos com o plano seguinte aparecendo
# por trás, por isso o vídeo segura o quadro 1232 e escurece até o preto em 6 quadros
# (a cartela já começa preta). Áudio com fade de 0,10 s (41,167 a 41,267 s) na cauda da voz.
#
# Uso: bash fea_cta_ads039_comente_black.sh "Ads 039 ....mp4" FEA-CTA-digitando-comente-black.mp4 SAIDA.mp4
set -euo pipefail
ADS="${1:?Ads 039}"; CART="${2:?cartela digitando}"; OUT="${3:?saída}"
ffmpeg -v error -y -i "$ADS" -i "$CART" -filter_complex "\
[0:v]trim=end_frame=1233,setpts=PTS-STARTPTS,fps=30,scale=1080:1920,format=yuv420p,setsar=1,\
tpad=stop_mode=clone:stop=5,fade=t=out:start_frame=1232:nb_frames=6[v0];\
[0:a]atrim=0:41.266667,asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,\
afade=t=out:st=41.166667:d=0.1[a0];\
[1:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v1];\
[1:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -profile:v high -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_name,duration,nb_frames -of compact "$OUT"
