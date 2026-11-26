# FEA: 12- Dezembro / 19- Reavaliação e relato toxina no espasmo (estoque, sem CTA)

Pasta no Drive: `1d9MTVraLQw3-bsEUgMmrbKu0M901zsTg` · bruto: "OK. Reavaliação paralisia" (`11ukT28CobPFCrj6zwVzr9pOFnEbsfXZJ`) · planilha "🔴 EDIÇÕES" linhas 266 e 267 (uma por vídeo). Numeração: 1 a 17 ocupadas, 18 reservado ao artigo "Língua", então 19.

| Vídeo | Bruto | ID | Duração (s) | Voz (s) |
|---|---|---|---|---|
| 1- Reavaliação | IMG_9589 + IMG_9590 (0 a 50 s) com cartões "Antes" (`IMG_9589_9590a.mov`) | `1KlOQ8Eg6_HIw6p5tZ0OabyRpAVaEyuUv` | 113,1 | 0,39 |
| 2- Relato toxina | IMG_9590f (fea_pad_fim 104,84 + 0,30) | `1eksYuYrE05YXRlrRX3RPAgmGok-dMI7Q` | 49,0 | 0,32 |

Conteúdo da pasta bruta (16 arquivos): IMG_9589.MOV e IMG_9590.MOV (23/11, reavaliação de toxina no espasmo, editados), IMG_9591.PNG (imagem de títulos: "1. Reavaliação (colocar no vídeo fotos do antes)", "2. Relato toxina"), IMG_9853.MOV (05/11, 4K HDR, 28,6 s, paciente fazendo as expressões da avaliação, não editado) e IMG_9841 a IMG_9852.HEIC (05/11, 12 fotos de documentação clínica com faixa e fundo branco).

Paciente: a mesma de "12- Dezembro / 2- Espasmo facial" (`181UW4IcqaoBKiwhzjNYPTjivkfK9IiSN`, primeira aplicação em 05/11, mesma faixa e blusa das fotos), conferida por comparação de rosto. NÃO é a paciente da pasta 14 (paralisia, IMG_9509) nem a do espasmo da pasta 11 (IMG_9242).

## Bruto intermediário do vídeo 1 (cartões "Antes")

Cartões (Pillow): foto recortada (560,600)-(2460,3133) do HEIC em 270x360, borda branca de 5 px com raio 12, chip "Antes" roxo `#5B4599` com Montserrat Bold 34 branca; total 280x432 em x=770, y=110 (canto superior direito, sobre o encosto da cadeira, sem cobrir o rosto).

```
$F -i IMG_9589.MOV -i IMG_9590.MOV -loop 1 -framerate 30 -i IMG_9845.png -loop 1 -framerate 30 -i IMG_9843.png \
 -loop 1 -framerate 30 -i IMG_9847.png -loop 1 -framerate 30 -i IMG_9846.png -filter_complex "\
[0:v]trim=end_frame=2046,setpts=PTS-STARTPTS,fps=30,format=yuv420p[v0];[0:a]atrim=0:68.2,asetpts=PTS-STARTPTS,aresample=48000,apad=whole_dur=68.2[a0];\
[1:v]trim=0:50,setpts=PTS-STARTPTS,fps=30,format=yuv420p[v1];[1:a]atrim=0:50,asetpts=PTS-STARTPTS,aresample=48000[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[vb][ab];\
[2:v]trim=0:1.35,setpts=PTS-STARTPTS[c1];[3:v]trim=0:3.95,setpts=PTS-STARTPTS[c2];[4:v]trim=0:5.0,setpts=PTS-STARTPTS[c3];\
[c1][c2][c3]concat=n=3:v=1:a=0,format=rgba,fade=in:st=0:d=0.2:alpha=1,fade=out:st=10.1:d=0.2:alpha=1,setpts=PTS+8.0/TB[g1];\
[5:v]trim=0:2.8,setpts=PTS-STARTPTS,format=rgba,fade=in:st=0:d=0.2:alpha=1,fade=out:st=2.6:d=0.2:alpha=1,setpts=PTS+24.6/TB[g2];\
[vb][g1]overlay=770:110:eof_action=pass[vo1];[vo1][g2]overlay=770:110:eof_action=pass,format=yuv420p[v]" \
 -map "[v]" -map "[ab]" -c:v libx264 -preset medium -crf 10 -pix_fmt yuv420p -r 30 -c:a pcm_s16le IMG_9589_9590a.mov
```

Janelas (s do IMG_9589): 8,0 a 9,35 brava (IMG_9845), 9,35 a 13,3 sobrancelha (IMG_9843), 13,3 a 18,3 sorriso com o olho fechando pelo espasmo (IMG_9847), 24,6 a 27,4 beijinho (IMG_9846). Áudio do intermediário conferido por correlação contra os dois brutos: 0 ms. Transcrição `IMG_9589_9590a.json` = IMG_9589 + IMG_9590 deslocada 68,2 s (palavras até 49,5 s).

Ajustes à mão na transcrição (tempos medidos no áudio, 10 a 50 ms): "Mas" 116,44 (era 116,10), "sutil" fim 107,90, "na" 109,12, "unidadezinha." e "Uma." (82,6 a 83,0) num segmento próprio, para a contagem não sair como conectivo solto.
