#!/usr/bin/env python3
"""FEA: transcrição com ElevenLabs Scribe, no MESMO formato do fea_transcrever.py (Whisper).

Uso:
    python3 fea_transcrever_scribe.py PASTA_SAIDA audio1.wav [audio2.wav ...] [--modelo scribe_v1]

Gera PASTA_SAIDA/<nome>.json com segmentos e palavras ({s, e, w}), igual ao Whisper, então
fea_editar_video.py e fea_revisar.py funcionam sem mudança. Cada segmento ganha "falante"
(speaker_0, speaker_1...), para separar a fala do Dr. da resposta da paciente.

Por que existe (06/11/2026): o Whisper precisa de 3 passadas e vários remendos (tempo de
palavra esticado em segmento longo, fala baixa sumindo com o VAD, "tchau" inventado no silêncio).
Ideia tirada do guia "O Seu Editor de Vídeo de IA". Antes de trocar o padrão, comparar os dois
num lote já entregue com fea_comparar_transcricao.py.

Chave: só na variável do ambiente ELEVENLABS_API_KEY, nunca no código nem no git.
Na criação da chave na ElevenLabs, desligar "Restrict Key" (ligada, a transcrição falha).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

ENDPOINT = "https://api.elevenlabs.io/v1/speech-to-text"
PAUSA_SEGMENTO = 0.8   # pausa (s) que abre segmento novo, como o VAD do Whisper
FIM_DE_FRASE = (".", "?", "!")


def enviar(caminho, chave, modelo, tentativas=3):
    """POST multipart só com a biblioteca padrão (sem instalar nada)."""
    limite = uuid.uuid4().hex
    campos = {"model_id": modelo, "language_code": "por", "timestamps_granularity": "word",
              "diarize": "true", "tag_audio_events": "false"}
    corpo = b""
    for k, v in campos.items():
        corpo += f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    nome = os.path.basename(caminho)
    corpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nome}\"\r\n"
              "Content-Type: application/octet-stream\r\n\r\n").encode()
    corpo += open(caminho, "rb").read() + f"\r\n--{limite}--\r\n".encode()
    req = urllib.request.Request(ENDPOINT, data=corpo, method="POST", headers={
        "xi-api-key": chave, "Content-Type": f"multipart/form-data; boundary={limite}"})
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            if e.code in (401, 403):
                sys.exit(f"ERRO {e.code}: chave recusada. Conferir ELEVENLABS_API_KEY e se "
                         f"'Restrict Key' foi desligada ao criar a chave.\n{msg}")
            if e.code == 402 or "quota" in msg.lower():
                sys.exit(f"ERRO {e.code}: sem crédito na conta ElevenLabs.\n{msg}")
            if n == tentativas - 1 or e.code < 500 and e.code != 429:
                sys.exit(f"ERRO {e.code} da ElevenLabs:\n{msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            if n == tentativas - 1:
                sys.exit(f"ERRO de conexão com a ElevenLabs: {e}")
        time.sleep(5 * (n + 1))


def para_segmentos(resposta):
    """Resposta do Scribe -> lista de segmentos no formato do fea_transcrever.py.

    O Scribe devolve "words" com type word/spacing/audio_event. As palavras do Whisper vêm com
    espaço na frente (" palavra") e o fea_editar_video.py usa isso para juntar "0" + ",2";
    aqui toda palavra ganha o espaço, porque o Scribe já entrega "0,2" inteiro.
    Segmento novo quando: muda o falante, pausa >= 0,8 s, ou a frase anterior terminou."""
    segs, atual = [], None
    for w in resposta.get("words", []):
        if w.get("type") != "word" or not w.get("text", "").strip():
            continue
        p = {"s": round(float(w["start"]), 3), "e": round(float(w["end"]), 3), "w": " " + w["text"].strip()}
        falante = w.get("speaker_id")
        novo = (atual is None or falante != atual["falante"]
                or p["s"] - atual["end"] >= PAUSA_SEGMENTO
                or atual["words"][-1]["w"].endswith(FIM_DE_FRASE))
        if novo:
            atual = {"start": p["s"], "end": p["e"], "text": "", "words": [], "falante": falante,
                     "motor": "scribe"}
            segs.append(atual)
        atual["words"].append(p)
        atual["end"] = p["e"]
    for s in segs:
        s["text"] = "".join(x["w"] for x in s["words"])
    return segs


def main():
    args = sys.argv[1:]
    modelo = "scribe_v1"
    if "--modelo" in args:
        i = args.index("--modelo")
        modelo = args[i + 1]
        del args[i:i + 2]
    if len(args) < 2:
        sys.exit(__doc__)
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("ERRO: falta a variável do ambiente ELEVENLABS_API_KEY "
                 "(configurar nas variáveis do ambiente, nunca no código)")
    saida = args[0]
    os.makedirs(saida, exist_ok=True)
    for audio in args[1:]:
        nome = os.path.basename(audio).rsplit(".", 1)[0]
        t0 = time.time()
        bruto = enviar(audio, chave, modelo)
        json.dump(bruto, open(f"{saida}/{nome}.scribe-bruto.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        segs = para_segmentos(bruto)
        json.dump(segs, open(f"{saida}/{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        n = sum(len(s["words"]) for s in segs)
        falantes = sorted({str(s["falante"]) for s in segs})
        print(f"{nome} ok | {n} palavras | falantes: {', '.join(falantes)} | {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
