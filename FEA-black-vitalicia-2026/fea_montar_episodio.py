#!/usr/bin/env python3
"""FEA Black Vitalícia: monta um episódio de historinha a partir das cenas geradas em IA.

Uso:
    python3 fea_montar_episodio.py projeto.json

projeto.json:
{
  "saida": "FEA-ep01-julgamento.mp4",
  "fontsdir": "/caminho/fonts",            # Montserrat-Bold.ttf
  "card": {"arquivo": "card.mp4", "inicio": 2.5},   # arte final oficial, entra depois da última cena
  "cenas": [{"arquivo": "c1.mp4", "inicio": 0, "fim": 7.6}, ...],
  "correcoes": [["\\\\bpra\\\\b", "para"]],          # regex aplicadas na legenda
  "ass_manual": "legenda-revisada.ass",             # opcional: usa esta legenda em vez de transcrever
  "textos": [{"texto": "POV: ...", "inicio": 0, "fim": 3}],  # opcional: textos de tela do roteiro
  "acabamento_filme": true                          # opcional: grão, cor e vinheta de cinema nas cenas
}

A legenda gerada é salva ao lado da saída (.ass) para revisão; corrigida, volta pelo "ass_manual".

Faz: padroniza cada cena em 1080x1920/30 fps/48 kHz, corta, concatena, adiciona o card
e queima a legenda amarela (Montserrat Bold, contorno preto, no máximo 5 palavras por bloco)
a partir da transcrição com tempo por palavra. Na legenda, "pra" vira sempre "para".
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

AMARELO = "&H0000D4FF"  # ASS usa BGR: #FFD400
ROXO = "&H0099455B"     # #5B4599, caixa dos textos de tela
MAX_PALAVRAS = 5


def run(cmd):
    subprocess.run(cmd, check=True)


# Acabamento de cinema (Keila, 07/10: "está muito com cara de IA"): cor menos saturada,
# grão de filme e vinheta leve tiram o brilho liso típico de vídeo gerado.
FILME = ",eq=saturation=0.86:contrast=1.04:gamma=0.98,noise=alls=7:allf=t,vignette=PI/5"


def normalizar(entrada, saida, inicio=0.0, fim=None, filme=False):
    corte = ["-ss", str(inicio)] + (["-to", str(fim)] if fim else [])
    run(["ffmpeg", "-v", "error", "-y", *corte, "-i", entrada,
         "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
         + (FILME if filme else ""),
         "-af", "aresample=48000,aformat=channel_layouts=stereo",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", saida])


def concatenar(partes, saida, pasta):
    lista = os.path.join(pasta, "lista.txt")
    with open(lista, "w") as f:
        f.writelines(f"file '{p}'\n" for p in partes)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", saida])


def palavras(video, pasta):
    from faster_whisper import WhisperModel
    wav = os.path.join(pasta, "a.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav])
    with wave.open(wav) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    modelo = WhisperModel(os.environ.get("FEA_WHISPER", "small"), device="cpu", compute_type="int8")
    segs, _ = modelo.transcribe(a, language="pt", word_timestamps=True, vad_filter=True,
                                initial_prompt="Doutor João Pithon, Meritíssimo, pós-graduação, cânula, "
                                               "anamnese, Black Friday Vitalícia, vinte de outubro.")
    return [(p.start, p.end, p.word.strip()) for s in segs for p in s.words if p.word.strip()]


def tempo(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def legenda_ass(ps, correcoes, limite, caminho):
    blocos, atual = [], []
    for p in ps:
        if p[0] >= limite:
            break
        atual.append(p)
        fim_frase = re.search(r"[.!?…:]$", p[2])
        if len(atual) >= MAX_PALAVRAS or fim_frase:
            blocos.append(atual)
            atual = []
    if atual:
        blocos.append(atual)
    linhas = []
    for i, b in enumerate(blocos):
        ini = b[0][0]
        fim = min(b[-1][1] + 0.25, blocos[i + 1][0][0] if i + 1 < len(blocos) else b[-1][1] + 0.6, limite)
        texto = " ".join(w for _, _, w in b)
        for padrao, troca in correcoes:
            texto = re.sub(padrao, troca, texto, flags=re.I)
        linhas.append(f"Dialogue: 0,{tempo(ini)},{tempo(fim)},Fala,,0,0,0,,{texto}")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
                "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
                "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
                "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                f"Style: Fala,Montserrat,66,{AMARELO},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,"
                "4,1,2,90,90,560,1\n"
                f"Style: Tela,Montserrat ExtraBold,54,&H00FFFFFF,&H000000FF,{ROXO},{ROXO},-1,0,0,0,100,100,0,0,3,"
                "18,0,8,90,90,240,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, "
                "MarginV, Effect, Text\n" + "\n".join(linhas) + "\n")


def main():
    proj = json.load(open(sys.argv[1]))
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    caminho = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    correcoes = [[r"\bpra\b", "para"]] + proj.get("correcoes", [])
    with tempfile.TemporaryDirectory() as tmp:
        partes = []
        for i, c in enumerate(proj["cenas"]):
            p = os.path.join(tmp, f"c{i:02d}.mp4")
            normalizar(caminho(c["arquivo"]), p, c.get("inicio", 0), c.get("fim"), proj.get("acabamento_filme"))
            partes.append(p)
        historia = os.path.join(tmp, "historia.mp4")
        concatenar(partes, historia, tmp)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", historia]))
        # legenda revisada à mão tem prioridade; senão gera pela transcrição e salva ao lado da saída
        ass = caminho(proj["ass_manual"]) if proj.get("ass_manual") else os.path.join(tmp, "leg.ass")
        if not proj.get("ass_manual"):
            legenda_ass(palavras(historia, tmp), correcoes, dur, ass)
            shutil.copy(ass, os.path.splitext(caminho(proj["saida"]))[0] + ".ass")
        if proj.get("textos"):  # textos de tela do roteiro (caixa roxa no topo)
            final = os.path.join(tmp, "final.ass")
            shutil.copy(ass, final)
            with open(final, "a", encoding="utf-8") as f:
                for t in proj["textos"]:
                    f.write(f"Dialogue: 1,{tempo(t['inicio'])},{tempo(t['fim'])},Tela,,0,0,0,,{t['texto']}\n")
            ass = final
        com_leg = os.path.join(tmp, "historia_leg.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", historia,
             "-vf", f"ass={ass}:fontsdir={proj['fontsdir']}", "-c:v", "libx264", "-preset", "medium",
             "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", com_leg])
        finais = [com_leg]
        if proj.get("card"):
            card = os.path.join(tmp, "card.mp4")
            normalizar(caminho(proj["card"]["arquivo"]), card, proj["card"].get("inicio", 0),
                       proj["card"].get("fim"))
            finais.append(card)
        concatenar(finais, caminho(proj["saida"]), tmp)
    print("Pronto:", caminho(proj["saida"]))


if __name__ == "__main__":
    main()
