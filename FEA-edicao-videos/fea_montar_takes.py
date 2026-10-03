#!/usr/bin/env python3
"""FEA: insere takes de cobertura (só imagem) sobre o vídeo principal, mantendo o áudio original.
Usado no 9- Visita técnica Elite Injectors (03/10/2026). Uso: rodar na pasta com brutos/ e editar TAKES."""
# Monta o vídeo principal (fala do Dr.) com takes de cobertura (só imagem), áudio original.
import subprocess
W,H=1080,1920
# (início, fim na linha do tempo do bruto principal, take, início no take)
TAKES = [
 (6.6, 9.4,  "IMG_7336", 0.5),   # imaginando como vai ficar, tudo lindo
 (9.4, 13.2, "IMG_7378", 4.0),   # stands dos patrocinadores
 (13.2,16.9, "IMG_7388", 18.0),  # sala VIP, alunos do passaporte VIP
 (16.9,21.0, "IMG_7397", 7.0),   # confraternização com os palestrantes
 (28.0,31.0, "IMG_7385", 6.0),   # nossa parte, Formação Especialista Academy
 (39.2,44.0, "IMG_7383", 7.0),   # corredores dos patrocinadores
 (49.1,54.2, "IMG_7332", 6.0),   # aquário gigante, dois LEDs enormes
 (56.0,61.0, "IMG_7366", 0.5),   # primeiras fileiras VIP, depois Elite
 (71.7,75.7, "IMG_7331", 8.0),   # monumental, mais de mil pessoas
 (76.1,79.9, "IMG_7369", 1.0),   # entrega incrível para todo mundo
 (96.6,100.9,"IMG_7388", 40.5),  # palestrantes, pré-aula
 (107.4,110.4,"IMG_7366", 19.0), # estrutura gigantesca
 (110.4,113.7,"IMG_7354", 32.0), # quantas pessoas trabalhando (planejamento)
]
ent=["-i","brutos/IMG_7431.MOV"]
f=[f"[0:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[b0]"]
for i,(a,b,c,s) in enumerate(TAKES,1):
    ent+=["-ss",str(s),"-t",str(b-a+0.2),"-i",f"brutos/{c}.MOV"]
    f.append(f"[{i}:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,setpts=PTS-STARTPTS+{a}/TB[t{i}]")
    f.append(f"[b{i-1}][t{i}]overlay=eof_action=pass:enable='between(t,{a},{b})'[b{i}]")
fc=";".join(f)
cmd=["ffmpeg","-y","-v","error",*ent,"-filter_complex",fc,"-map",f"[b{len(TAKES)}]","-map","0:a",
     "-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p","-r","30","-c:a","copy","montagem.mp4"]
subprocess.run(cmd,check=True)
print("ok")
