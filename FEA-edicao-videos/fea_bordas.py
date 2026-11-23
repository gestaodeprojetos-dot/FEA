#!/usr/bin/env python3
"""FEA: ajusta o começo e o fim de cada vídeo do projeto medindo a voz no áudio do bruto.

Regra da Keila (16/11/2026): o vídeo abre com o Dr. já falando, 0,25 a 0,40 s antes do ataque
da voz (a revisora exige pelo menos 0,30 s), sem silêncio inicial e sem cortar a primeira palavra.
Sem CTA, o fim fica 0,40 s depois da última sílaba (respiro de 0,3 a 0,5 s, fade_final de 0,3 s).

Uso:
    python3 fea_bordas.py projeto.json [--antes 0.35] [--respiro 0.42] [--gravar]

Para cada vídeo:
  - o 1º trecho do `manter` começa em (ataque da voz - antes), procurando o ataque a partir do
    início que está no projeto (que deve ficar no silêncio logo antes da frase escolhida);
  - o último trecho termina em (fim da voz + respiro), procurando a última voz até o fim que
    está no projeto; avisa se há outra voz começando antes do novo fim;
  - os pontos internos passam pelo `encaixar_cortes` de sempre;
  - todos os trechos viram "exato" (o render não mexe mais nos pontos medidos aqui).
Depois de medir, roda a checagem de frase completa da revisora (`checar_frases_borda`): o ataque
da voz não basta, o começo tem que ser o início de uma frase e o fim, a conclusão da frase e da ação
(Keila, 23/11/2026). Sem --gravar, só imprime. Com --gravar, reescreve o projeto (o original vira .bak).
"""
import json
import shutil
import subprocess
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import fea_editar_video as ed  # noqa: E402

PASSO = 0.01


def db_trecho(ff, arq, a, dur):
    pcm = subprocess.run([ff, "-nostdin", "-v", "error", "-ss", f"{max(0.0, a):.3f}", "-t", f"{dur:.3f}",
                          "-i", arq, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(float)
    n = len(x) // 160
    return 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(axis=1)) + 1)


def piso_arquivo(ff, arq):
    db = db_trecho(ff, arq, 0, 100000)
    db = db[db > 1]          # ignora silêncio digital
    return float(np.percentile(db, 5))


def ataque(ff, arq, a, piso, janela=4.0):
    """Ataque da 1ª voz sustentada a partir de `a` (mesmo critério de fea_revisar.onset_voz)."""
    db = db_trecho(ff, arq, a, janela)
    lim = max(38.0, piso + 12)
    sm = np.convolve(db, np.ones(5) / 5, "same")
    on = sm >= lim
    for i in range(len(db)):
        if on[i] and on[i:i + 15].mean() >= 0.7:
            k = i
            while k > 0 and db[k - 1] > piso + 6 and i - k < 40:
                k -= 1
            return a + k * PASSO, a + i * PASSO
    return None, None


def fim_voz(ff, arq, b, piso, janela=1.8):
    """Fim da fala que está em curso perto de `b` (fim da palavra pela transcrição): a partir de
    b - 0,4 s, primeiro trecho de 150 ms sem voz sustentada (média de 50 ms abaixo de piso + 12 dB);
    dali, segue enquanto o som decai acima de piso + 6 dB (máx. 0,4 s)."""
    a = max(0.0, b - 0.4)
    db = db_trecho(ff, arq, a, janela + 0.4)
    lim = max(38.0, piso + 12)
    sm = np.convolve(db, np.ones(5) / 5, "same")
    for i in range(len(db) - 15):
        if (sm[i:i + 15] < lim).all():
            k = i
            while k + 1 < len(db) and db[k] > piso + 6 and k - i < 40:
                k += 1
            return a + k * PASSO
    return None


def proxima_voz(ff, arq, t, piso, janela=1.0):
    """Primeiro instante com som acima de piso + 6 dB depois de t (por 30 ms)."""
    db = db_trecho(ff, arq, t, janela)
    alto = db > piso + 8
    for i in range(len(db) - 3):
        if alto[i:i + 3].all():
            return t + i * PASSO
    return None


def q(t):
    return round(round(t * 30) / 30, 3)   # quadro inteiro a 30 fps


def main():
    args = sys.argv[1:]
    gravar = "--gravar" in args
    antes = float(args[args.index("--antes") + 1]) if "--antes" in args else 0.35
    respiro = float(args[args.index("--respiro") + 1]) if "--respiro" in args else 0.42
    so = [x for x in args if not x.startswith("--") and not x.endswith(".json")
          and x not in (str(antes), str(respiro))]
    proj = args[0]
    cfg = json.load(open(proj, encoding="utf-8"))
    ff = cfg["ffmpeg"]
    pisos = {}
    for v in cfg["videos"]:
        if so and not any(s in v["saida"] for s in so):
            continue
        arq = v["entrada"]
        if arq not in pisos:
            pisos[arq] = piso_arquivo(ff, arq)
        piso = pisos[arq]
        m = [list(t[:2]) for t in v["manter"]]
        exatos = [len(t) > 2 and t[2] == "exato" for t in v["manter"]]
        # pontos internos: encaixe de sempre (os já exatos ficam)
        db, _, passo = ed.perfil_voz(ff, arq)[:3]
        enc = ed.encaixar_cortes([t if not e else t + ["exato"] for t, e in zip(m, exatos)], db, passo)
        a0, b0 = m[0][0], m[-1][1]
        at, sust = ataque(ff, arq, a0, piso)
        if at is None:
            print(f"!! {v['saida'].rsplit('/', 1)[-1]}: sem voz depois de {a0}")
            continue
        novo_a = q(max(0.0, at - antes))
        if novo_a > at - 0.30:
            novo_a = q(at - 0.30 - 0.02)
        fv = fim_voz(ff, arq, b0, piso)
        novo_b = q(fv + respiro) if fv else b0
        prox = proxima_voz(ff, arq, fv + 0.03, piso, 0.8) if fv else None
        enc[0][0] = novo_a
        enc[-1][1] = novo_b
        v["manter"] = [[round(x, 3), round(y, 3), "exato"] for x, y in enc]
        dur = sum(y - x for x, y, _ in v["manter"])
        aviso = ""
        if prox is not None and prox < novo_b:
            aviso = f"  !! outra voz em {prox:.2f} s, antes do fim {novo_b:.2f}"
        if fv is None:
            print("!! sem fim de voz perto de", b0)
            fv = b0
        # frase completa no começo e no fim (Keila, 23/11/2026): a mesma checagem da revisora
        import fea_revisar as rv
        trans = json.load(open(v["transcricao"], encoding="utf-8"))
        pal = [w for seg in trans for w in seg["words"]]
        db_b, lim_b, ps_b = ed.perfil_voz(ff, arq)[:3]
        e_fr, a_fr, _ = rv.checar_frases_borda(v, pal, v["manter"], db_b, lim_b, ps_b)
        for x in e_fr:
            print("   !! ERRO", x)
        print(f"{v['saida'].rsplit('/', 1)[-1]}: início {a0}->{novo_a} (ataque {at:.2f}, voz antes {at - novo_a:.2f} s) "
              f"| fim {b0}->{novo_b} (voz até {fv:.2f}) | conteúdo {dur:.2f} s{aviso}"
              + ("  !! ACIMA DE 135 s" if dur > 135 else ""))
    if gravar:
        shutil.copy(proj, proj + ".bak")
        json.dump(cfg, open(proj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("gravado:", proj)


if __name__ == "__main__":
    main()
