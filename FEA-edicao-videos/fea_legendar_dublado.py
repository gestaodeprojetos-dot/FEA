#!/usr/bin/env python3
"""FEA: legenda e cartela final na versão dublada em espanhol (HeyGen) dos depoimentos Ads FEP.

A dublagem muda o tempo da fala, então a legenda sai da transcrição do áudio dublado
(Whisper, espanhol, tempo por palavra), no mesmo estilo da versão em português
(fea_editar_depoimento.py). Os destaques são procurados pelo texto no áudio dublado.

Uso:
    python3 fea_legendar_dublado.py projeto.json ID dublado.mp4 saida.mp4 PASTA_MODELOS
"""
import json
import os
import re
import subprocess
import sys
import unicodedata
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_editar_depoimento import W, LEG_Y, DEST_Y, quebrar, ts  # noqa: E402

CORRECOES = [
    (r"\b(FEB|Fep|fep|feb|FEV|Fev)\b", "FEP"),
    (r"\bFEP online\b", "FEP Online"),
    (r"\b(Piton|Pitón|Pitton)\b", "Pithon"),
    (r"\bJuan Pithon\b", "João Pithon"),
]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def corrigir(t):
    for a, b in CORRECOES:
        t = re.sub(a, b, t)
    return t


def transcrever(mp4, modelos, tmp):
    wav = tmp + ".wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    from faster_whisper import WhisperModel
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=modelos)
    w = wave.open(wav)
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="es", word_timestamps=True, vad_filter=True,
                           condition_on_previous_text=False,
                           initial_prompt="FEP Online, FEP Experience, doctor João Pithon, armonización orofacial.")
    return [{"s": x.start, "e": x.end, "w": x.word.strip()} for s in segs for x in s.words]


def blocos(pal):
    out, cur = [], []
    for i, p in enumerate(pal):
        cur.append(p)
        txt = " ".join(x["w"] for x in cur)
        prox = pal[i + 1] if i + 1 < len(pal) else None
        fim_frase = p["w"][-1] in ".?!"
        pausa = prox is not None and prox["s"] - p["e"] > 0.45
        virgula = p["w"][-1] in ",;:" and len(txt) >= 18
        longo = prox is not None and len(txt) + 1 + len(prox["w"]) > 46
        if prox is None or fim_frase or pausa or virgula or longo:
            out.append([cur[0]["s"], p["e"], corrigir(txt)])
            cur = []
    for i, b in enumerate(out):
        if i + 1 < len(out) and out[i + 1][0] - b[1] < 0.7:
            b[1] = out[i + 1][0]
        else:
            b[1] += 0.25
    return out


def achar(pal, frase):
    alvo = norm(frase).split()
    ns = [norm(p["w"]) for p in pal]
    for i in range(len(ns) - len(alvo) + 1):
        if ns[i:i + len(alvo)] == alvo:
            a, b = pal[i]["s"], pal[i + len(alvo) - 1]["e"]
            return a, max(b, a + 1.3)
    return None


def main():
    proj_p, vid, dub, saida, modelos = sys.argv[1:6]
    proj = json.load(open(proj_p, encoding="utf-8"))
    v = next(x for x in proj["videos"] if x["id"] == vid)
    tmp = os.path.join(os.path.dirname(saida), f"{vid}_dub")
    pal = transcrever(dub, modelos, tmp)
    json.dump(pal, open(tmp + ".json", "w"), ensure_ascii=False)
    legs = blocos(pal)
    cab = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", "PlayResY: 1920",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Leg,Montserrat,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,"
        "3.2,1.5,5,60,60,0,1",
        "Style: Dest,Oswald,92,&H00F2EEEC,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,1,0,1,"
        "0,3,2,60,60,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for a, b, t in legs:
        t = t[0].upper() + t[1:]
        cab.append(f"Dialogue: 0,{ts(a)},{ts(b)},Leg,,0,0,0,,{{\\pos({W // 2},{LEG_Y})}}{quebrar(t)}")
    for d in v.get("destaques", []):
        r = achar(pal, d[3])
        print(f"  destaque {d[3]!r}: {'%.1f-%.1f' % r if r else 'NÃO ACHADO'}")
        if r:
            cab.append(f"Dialogue: 1,{ts(r[0])},{ts(r[1])},Dest,,0,0,0,,{{\\pos({W // 2},{DEST_Y})"
                       f"\\fad(120,80)}}{quebrar(d[3].upper(), 16)}")
    ass = tmp + ".ass"
    open(ass, "w", encoding="utf-8").write("\n".join(cab) + "\n")
    for a, b, t in legs:
        print(f"  {a:6.2f}-{b:6.2f} {t}")
    filtros = [f"[0:v]scale=1080:1920,fps=30,format=yuv420p,subtitles='{ass}':fontsdir='{proj['fontes']}',setsar=1[vl]",
               "[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[vk]",
               "[1:a]aresample=48000,aformat=channel_layouts=stereo[ak]",
               "[0:a]aresample=48000,aformat=channel_layouts=stereo[ac]",
               "[vl][ac][vk][ak]concat=n=2:v=1:a=1[vo][ao]"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dub, "-i", proj["cta"]["es"],
                    "-filter_complex", ";".join(filtros), "-map", "[vo]", "-map", "[ao]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-profile:v", "high",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", saida], check=True)


if __name__ == "__main__":
    main()
