#!/usr/bin/env python3
"""FEA: transcrição com tempo por palavra (Whisper large-v3-turbo).

Uso:
    python3 fea_transcrever.py PASTA_SAIDA audio1.wav audio2.wav ...
    python3 fea_transcrever.py --complementar PASTA_SAIDA audio1.wav ...   # só a 2ª passada
    python3 fea_transcrever.py --idioma es PASTA_SAIDA audio.wav             # vídeo traduzido (LATAM)

Gera PASTA_SAIDA/<nome>.json com segmentos e palavras ({s, e, w}).
O filtro de voz (VAD) pula silêncio e evita que o modelo "invente" fala
(ex.: "tchau" repetido) nos trechos só de procedimento.

2ª passada (Keila, 02/10/2026): o VAD também pula fala BAIXA, como o fim de uma enumeração
("pertuitos 1, 2, 3" e o "4, 5, 6" sumia) e a resposta da paciente longe do microfone
("o que você achou da anestesia?" sem a resposta). Cada buraco entre palavras em que o áudio
tem voz é transcrito de novo sem VAD; as palavras novas entram como segmento próprio,
marcado com "complemento": true. Antes disso, segmento longo (> 15 s) é retranscrito em pedaços
cortados nos silêncios ("refinado": true), porque o tempo das palavras vinha esticado.
"""
import json
import os
import re
import sys

import numpy as np

PROMPT = ("Harmonização orofacial, preenchimento com ácido hialurônico, full face, olheiras, "
          "bigode chinês, código de barras, têmporas, pertuito labial, comissura, pré-jowl, "
          "sulco nasolabial, SANEP, anestesia, mentoniano, bolus, retroinjeção, cânula, agulha, mL, "
          "toxina botulínica, glabela, frontal, orbiculares, nasal, lifting, bioestimulador.")

# vídeo traduzido para o espanhol (anúncios LATAM): --idioma es
PROMPT_ES = ("Armonización facial, relleno con ácido hialurónico, full face, ojeras, surco nasolabial, "
             "mentón, mandíbula, cuello, toxina botulínica, platisma, bandas platismales, cánula, aguja, mL.")
IDIOMA = "pt"

# o que o Whisper inventa em trecho sem fala (não entra no complemento)
ALUCINACAO = re.compile(r"obrigad|tchau|legenda|inscreva|amara|transcri|música|aplausos|risos|"
                        r"\bvaleu\b|até a próxima|até mais|gracias|suscr[ií]b|subt[ií]tul", re.I)
PASSO = 0.05


def carregar_audio(wav):
    import wave
    with wave.open(wav) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a


def perfil(a):
    h = int(16000 * PASSO)
    n = len(a) // h
    db = 20 * np.log10(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(axis=1)) + 1e-9) + 90
    return db, max(38.0, float(np.percentile(db, 5)) + 12)


def buracos_com_voz(segs, db, limiar, dur):
    """Intervalos sem palavra transcrita (> 0,8 s) em que há pelo menos 0,1 s de voz."""
    palavras = [w for s in segs for w in s["words"]]
    marcos = [(0.0, 0.0)] + [(w["s"], w["e"]) for w in palavras] + [(dur, dur)]
    textos = [""] + [w["w"] for w in palavras] + [""]
    saida = []
    for k, ((_, e0), (s1, _)) in enumerate(zip(marcos, marcos[1:])):
        if s1 - e0 < 0.8:
            continue
        i0, i1 = int((e0 + 0.15) / PASSO), int((s1 - 0.15) / PASSO)   # sem o rabo das palavras vizinhas
        voz = db[i0:i1] >= limiar - 3
        if voz.sum() * PASSO >= 0.1:   # o "Ótimo" baixinho da paciente tem só ~0,15 s acima do ruído
            saida.append((e0, s1, {norm(t) for t in textos[max(0, k - 1):k + 1]},
                          {norm(t) for t in textos[k + 1:k + 3]}))
    return saida


def norm(w):
    return re.sub(r"[^\w]", "", w).lower()


def refinar(modelo, segs, a, limite=15.0):
    """Segmento longo (> 15 s) do VAD costuma vir com o tempo das palavras esticado: em vídeo de
    toxina com fala esparsa, "15 dias" aparecia 9 s depois da fala. Corta o áudio do segmento nos
    silêncios (pedaços de até ~12 s) e transcreve cada pedaço; os tempos voltam presos à voz."""
    db, limiar = perfil(a)
    saida = []
    for s in segs:
        if s["end"] - s["start"] <= limite or s.get("complemento"):
            saida.append(s)
            continue
        i0, i1 = int(s["start"] / PASSO), min(len(db), int(s["end"] / PASSO) + 1)
        cortes, k, ini = [], i0, i0
        while k < i1:
            if db[k] < limiar - 3:
                j = k
                while j < i1 and db[j] < limiar - 3:
                    j += 1
                if (j - k) * PASSO >= 0.5 and (k - ini) * PASSO >= 2.0:
                    cortes.append((ini * PASSO, (k + (j - k) // 2) * PASSO))
                    ini = k + (j - k) // 2
                k = j
            k += 1
        cortes.append((ini * PASSO, s["end"]))
        # junta pedaços curtos até ~12 s
        pedacos = []
        for c in cortes:
            if pedacos and c[1] - pedacos[-1][0] <= 12.0:
                pedacos[-1] = (pedacos[-1][0], c[1])
            else:
                pedacos.append(c)
        novos = []
        for ini_t, fim_t in pedacos:
            ini_t, fim_t = max(0.0, ini_t - 0.1), min(len(a) / 16000, fim_t + 0.1)
            tr, _ = modelo.transcribe(a[int(ini_t * 16000):int(fim_t * 16000)], language=IDIOMA,
                                      word_timestamps=True, vad_filter=False,
                                      condition_on_previous_text=False, initial_prompt=PROMPT_ES if IDIOMA == "es" else PROMPT)
            for x in tr:
                if ALUCINACAO.search(x.text) or x.no_speech_prob > 0.6 or x.avg_logprob < -1.0:
                    continue
                ws = [{"s": w.start + ini_t, "e": w.end + ini_t, "w": w.word} for w in x.words]
                if ws:
                    novos.append({"start": ws[0]["s"], "end": ws[-1]["e"], "refinado": True,
                                  "text": "".join(w["w"] for w in ws), "words": ws})
        # só troca se o texto novo cobre o antigo (nada some na troca)
        n_velho = len(s["words"])
        n_novo = sum(len(x["words"]) for x in novos)
        saida += novos if n_novo >= 0.8 * n_velho else [s]
    return saida


def complementar(modelo, segs, a):
    db, limiar = perfil(a)
    dur = len(a) / 16000
    novos = []
    for e0, s1, antes, depois in buracos_com_voz(segs, db, limiar, dur):
        ini, fim = max(0.0, e0 - 0.3), min(dur, s1 + 0.3)
        trecho, _ = modelo.transcribe(a[int(ini * 16000):int(fim * 16000)], language=IDIOMA,
                                      word_timestamps=True, vad_filter=False,
                                      condition_on_previous_text=False)
        for s in trecho:
            if ALUCINACAO.search(s.text) or s.no_speech_prob > 0.6 or s.avg_logprob < -1.0:
                continue
            ws = []
            for x in s.words:
                ws_, we_ = x.start + ini, x.end + ini
                meio = (ws_ + we_) / 2
                if not (e0 + 0.1 <= meio <= s1 - 0.1) or ws_ < e0 - 0.15:
                    continue
                # palavra precisa de voz no tempo dela (ou bem perto, o tempo do Whisper erra)
                j0, j1 = max(0, int((ws_ - 0.2) / PASSO)), min(len(db), int((we_ + 0.2) / PASSO) + 1)
                if not (db[j0:j1] >= limiar).any():
                    continue
                ws.append({"s": max(ws_, e0), "e": min(we_, s1), "w": x.word})
            # a palavra da borda que repete a vizinha já transcrita é a mesma fala (ex.: "três")
            if ws and norm(ws[0]["w"]) in antes:
                ws = ws[1:]
            if ws and norm(ws[-1]["w"]) in depois:
                ws = ws[:-1]
            if ws:
                novos.append({"start": ws[0]["s"], "end": ws[-1]["e"], "complemento": True,
                              "text": "".join(w["w"] for w in ws), "words": ws})
    return sorted(segs + novos, key=lambda s: s["start"])


def main():
    from faster_whisper import WhisperModel
    args = sys.argv[1:]
    so_complemento = "--complementar" in args
    args = [x for x in args if x != "--complementar"]
    global IDIOMA
    if "--idioma" in args:
        i = args.index("--idioma")
        IDIOMA = args[i + 1]
        del args[i:i + 2]
    saida = args[0]
    os.makedirs(saida, exist_ok=True)
    modelo = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8",
                          download_root=os.environ.get("FEA_MODELOS", "models"), cpu_threads=os.cpu_count())
    for wav in args[1:]:
        nome = os.path.basename(wav).rsplit(".", 1)[0]
        destino = f"{saida}/{nome}.json"
        if so_complemento:
            out = [s for s in json.load(open(destino, encoding="utf-8")) if not s.get("complemento")]
        else:
            segs, _ = modelo.transcribe(wav, language=IDIOMA, word_timestamps=True, initial_prompt=PROMPT_ES if IDIOMA == "es" else PROMPT,
                                        vad_filter=True, condition_on_previous_text=False)
            out = [{"start": s.start, "end": s.end, "text": s.text,
                    "words": [{"s": x.start, "e": x.end, "w": x.word} for x in s.words]} for s in segs]
        audio = carregar_audio(wav)
        if not any(s.get("refinado") for s in out):
            out = refinar(modelo, out, audio)
        out = complementar(modelo, out, audio)
        json.dump(out, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        n = sum(1 for s in out if s.get("complemento"))
        print(nome, "ok", f"({n} trechos de fala baixa recuperados)", flush=True)


if __name__ == "__main__":
    main()
