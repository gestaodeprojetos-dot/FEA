#!/usr/bin/env python3
"""FEA: transcrição com tempo por palavra (Whisper large-v3-turbo).

Uso:
    python3 fea_transcrever.py PASTA_SAIDA audio1.wav audio2.wav ...
    python3 fea_transcrever.py --idioma es PASTA_SAIDA audio1.wav ...   # áudio em espanhol (dublado)

Gera PASTA_SAIDA/<nome>.json com segmentos e palavras ({s, e, w}).
O filtro de voz (VAD) pula silêncio e evita que o modelo "invente" fala
(ex.: "tchau" repetido) nos trechos só de procedimento.
"""
import json
import os
import sys

from faster_whisper import WhisperModel

PROMPT = ("Harmonização orofacial, preenchimento com ácido hialurônico, full face, olheiras, "
          "bigode chinês, código de barras, têmporas, pertuito labial, comissura, pré-jowl, "
          "sulco nasolabial, SANEP, anestesia, mentoniano, bolus, retroinjeção, cânula, agulha, mL, "
          "toxina botulínica, glabela, frontal, orbiculares, nasal, lifting, bioestimulador.")

PROMPT_ES = ("Armonización facial, relleno con ácido hialurónico, full face, ojeras, surco nasogeniano, "
             "sienes, pertuito, comisura labial, pre-jowl, anestesia, bolo, retroinyección, cánula, aguja, mL, "
             "toxina botulínica, glabela, músculo frontal, orbicular, bioestimulador, plano supraperióstico.")

args = sys.argv[1:]
lingua = "pt"
if args[:1] == ["--idioma"]:
    lingua, args = args[1], args[2:]
saida = args[0]
os.makedirs(saida, exist_ok=True)
modelo = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8",
                      download_root=os.environ.get("FEA_MODELOS", "models"), cpu_threads=os.cpu_count())
for wav in args[1:]:
    segs, _ = modelo.transcribe(wav, language=lingua, word_timestamps=True,
                                initial_prompt=PROMPT_ES if lingua == "es" else PROMPT,
                                vad_filter=True, condition_on_previous_text=False)
    out = [{"start": s.start, "end": s.end, "text": s.text,
            "words": [{"s": x.start, "e": x.end, "w": x.word} for x in s.words]} for s in segs]
    nome = os.path.basename(wav).rsplit(".", 1)[0]
    json.dump(out, open(f"{saida}/{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(nome, "ok", flush=True)
