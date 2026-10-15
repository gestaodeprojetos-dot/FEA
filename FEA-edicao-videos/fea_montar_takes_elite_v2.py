#!/usr/bin/env python3
"""FEA: versão 2 da visita técnica Elite Injectors (05/10/2026), takes diferentes da versão 1 e trilha HeyGen e1a58ece (orquestral heroica, -12,2 dB com sidechain)."""
# Monta o vídeo principal (fala do Dr.) com takes de cobertura (só imagem), áudio original.
import subprocess
W,H=1080,1920
# (início, fim na linha do tempo do bruto principal, take, início no take)
TAKES = [
 (6.6, 9.4,  "IMG_7369", 0.5),   # imaginando como vai ficar (salão com palco)
 (9.4, 13.2, "IMG_7381", 0.0),   # stands dos patrocinadores (hall de exposição)
 (13.2,16.9, "IMG_7402", 0.0),   # sala VIP
 (16.9,21.0, "IMG_7399", 0.0),   # confraternização com os palestrantes
 (28.0,31.0, "IMG_7378", 13.0),  # nossa parte, Formação Especialista Academy
 (39.2,44.0, "IMG_7386", 0.0),   # corredores dos patrocinadores
 (49.1,56.0, "IMG_7343", 6.0),   # aquário gigante, dois LEDs enormes
 (56.0,61.0, "IMG_7365", 5.0),   # primeiras fileiras VIP (palco)
 (71.7,76.1, "IMG_7364", 0.0),   # monumental, mais de mil pessoas
 (76.1,79.9, "IMG_7330", 0.0),   # entrega incrível para todo mundo
 (96.6,100.9,"IMG_7400", 0.0),   # palestrantes, pré-aula
 (107.4,110.4,"IMG_7341", 0.0),  # estrutura gigantesca
 (110.4,113.7,"IMG_7358", 11.0), # quantas pessoas trabalhando
]
ent=["-i","brutos/IMG_7431.MOV"]
f=[f"[0:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[b0]"]
for i,(a,b,c,s) in enumerate(TAKES,1):
    ent+=["-ss",str(s),"-t",str(b-a+0.2),"-i",f"brutos/{c}.MOV"]
    f.append(f"[{i}:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,setpts=PTS-STARTPTS+{a}/TB[t{i}]")
    f.append(f"[b{i-1}][t{i}]overlay=eof_action=pass:enable='between(t,{a},{b})'[b{i}]")
fc=";".join(f)
cmd=["ffmpeg","-y","-v","error",*ent,"-filter_complex",fc,"-map",f"[b{len(TAKES)}]","-map","0:a",
     "-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p","-r","30","-c:a","copy","montagem_v2.mp4"]
subprocess.run(cmd,check=True)
print("ok")
