"""FEA: transcrição LITERAL (mantém hesitações e repetições) dos WAVs de SP/wav em SP/trv. Uso: python3 -I fea_transcrever_literal.py SP"""
import json, sys, os
from faster_whisper import WhisperModel
sp = sys.argv[1]
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=sp + "/models")
PROMPT = ("Transcrição literal, com hesitações e repetições: Então, é... eu, eu vou te... hum, "
          "a gente, a gente vai, você vai ser, você vai, você vai completar. Ã... tipo assim, né? "
          "Isso não é, não é sorte. Pra, pra você, é...")
for f in sorted(os.listdir(sp + "/wav")):
    b = f[:-4]
    out = f"{sp}/trv/{b}.json"
    if os.path.exists(out):
        continue
    segs, _ = m.transcribe(f"{sp}/wav/{f}", language="pt", initial_prompt=PROMPT, word_timestamps=True,
                           vad_filter=False, condition_on_previous_text=False, temperature=0.0, beam_size=5)
    dados = [{"start": s.start, "end": s.end, "text": s.text,
              "words": [{"s": w.start, "e": w.end, "w": w.word, "p": w.probability} for w in s.words]} for s in segs]
    json.dump(dados, open(out, "w"), ensure_ascii=False)
    print(b, "ok", flush=True)
