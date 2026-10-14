#!/usr/bin/env bash
# FEA: monta o bruto do Ads 113 (alunos19): alunos até "clique em Saiba Mais" (29,0 s, silêncio)
# + final do IMG_0869 "então esteja comigo ao vivo 19 do 10, te espero lá" (19,6 a 22,9 s).
# A transcrição combinada (tr/alunos19.json) junta as palavras do alunos antes de 28,85 s
# e as do 0869 a partir de 19,6 s deslocadas para 29,0 s.
B=$1
ffmpeg -v error -y -i $B/brutos/alunos.mp4 -i $B/brutos/IMG_0869.MOV -filter_complex "\
[0:v]trim=0:29.0,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=30[v0];[0:a]atrim=0:29.0,asetpts=PTS-STARTPTS,aresample=48000[a0];\
[1:v]trim=19.6:22.9,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=30[v1];[1:a]atrim=19.6:22.9,asetpts=PTS-STARTPTS,aresample=48000[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k $B/brutos/alunos19.mp4
