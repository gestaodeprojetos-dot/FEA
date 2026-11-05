#!/usr/bin/env python3
"""Renderiza os vídeos do projeto e cola o CTA no final, em qualidade total.

Transição antes do CTA (padrão desde 05/11/2026, pedido da Keila: "quando tiver algum cta nos
conteúdos, faz uma transiçãozinha, porque do nada aparece o cta, fica ruim"):
  - vídeo: crossfade (xfade fade) de --transicao segundos (padrão 0,5 s);
  - áudio: acrossfade da mesma duração;
  - nada de efeito chamativo (wipe, zoom, glitch): padrão premium e clean.
A transição nunca engole a última palavra do Dr.: o fim da voz do conteúdo é medido no áudio do
bruto (janelas de 10 ms) e a transição só começa FOLGA_S depois dele. Se o conteúdo acaba colado na
fala, o último quadro é estendido (tpad clone) e o áudio ganha silêncio (apad), para a transição
cair no silêncio. Se a voz do CTA começar antes do fim da transição, o fade de entrada do áudio do
CTA encurta para não engolir a primeira palavra dele.

Como é feito: o CTA entra como 2ª entrada do próprio render do conteúdo (fea_editar_video.py
--entrega --cta CTA --transicao T), numa codificação só (H.264 CRF 18 High, AAC 192k 48 kHz).
A colagem por stream copy (corte seco) não serve para crossfade, e emendar uma cauda recodificada
por stream copy deu DTS repetido na junção por causa dos B-frames (testado em 05/11/2026). O CTA
passa a ser recodificado uma vez em CRF 18, como o conteúdo.
Grava ao lado do vídeo `NOME.emenda.json` com os tempos da emenda (lido pela revisora).

--transicao 0 volta ao corte seco por stream copy (só se a Keila pedir).

Limite de duração (Keila, 02/10/2026): vídeo final com CTA até 3 min.

Uso:
    python3 fea_render_com_cta.py projeto.json CTA.mp4 [--transicao 0.5] [trecho_do_nome ...]
"""
import json, os, subprocess, sys, tempfile

import numpy as np

LIMITE_TOTAL_S = 180
TRANSICAO_PADRAO = 0.5
FOLGA_S = 0.10          # silêncio mínimo entre o fim da voz do Dr. e o começo da transição
AQUI = os.path.dirname(os.path.abspath(__file__))


def duracao(ff, caminho):
    r = subprocess.run([ff, "-i", caminho], capture_output=True, text=True)
    for linha in r.stderr.splitlines():
        if "Duration:" in linha:
            h, m, s = linha.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0


def perfil_db(ff, caminho, ini=0.0, dur=None, passo=0.01):
    """Volume em dB (janelas de 10 ms) do áudio mono 16 kHz."""
    cmd = [ff, "-nostdin", "-v", "error", "-ss", f"{ini:.3f}", "-i", caminho]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    pcm = subprocess.run(cmd + ["-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(float)
    n = int(16000 * passo)
    k = len(a) // n
    return 20 * np.log10(np.sqrt((a[:k * n].reshape(k, n) ** 2).mean(axis=1)) + 1)


def fim_da_voz(ff, caminho, a, b, passo=0.01, mudo=()):
    """Fim da última fala no trecho [a, b] do arquivo, medido no áudio: última janela com voz
    sustentada (média de 50 ms acima de piso + 12 dB) e, dali, segue enquanto o som está acima de
    piso + 6 dB (o fim da sílaba decai). Mesmo critério do ataque da voz no início
    (fea_revisar.onset_voz). Retorna segundos do arquivo, ou None se o trecho não tem voz.
    `mudo`: janelas [x, y] (s do arquivo) silenciadas no render, que não contam como voz."""
    ini = max(0.0, b - 8.0, a)
    db = perfil_db(ff, caminho, ini, b - ini, passo)
    for x, y in mudo:
        db[max(0, int((x - ini) / passo)):max(0, int((y - ini) / passo) + 1)] = 0
    piso = float(np.percentile(perfil_db(ff, caminho, 0, None, 0.05), 5))
    lim = max(38.0, piso + 12)
    sm = np.convolve(db, np.ones(5) / 5, "same")
    on = np.where(sm >= lim)[0]
    if not len(on):
        return None
    k = int(on[-1])
    while k + 1 < len(db) and db[k + 1] > piso + 6 and k - on[-1] < 40:
        k += 1
    return ini + (k + 1) * passo


def onset_voz_cta(ff, cta, ate=3.0):
    sys.path.insert(0, AQUI)
    import fea_revisar as rv
    t, _, _ = rv.onset_voz(perfil_db(ff, cta, 0, ate))
    return t


def plano_emenda(ff, v, manter, cta, transicao):
    """Tempos da emenda no vídeo final (s): fim da voz, tpad, começo da transição, fade do CTA."""
    d = sum(b - a for a, b in manter)
    a_ult, b_ult = manter[-1][:2]
    fim_bruto = fim_da_voz(ff, v["entrada"], a_ult, b_ult, mudo=v.get("silenciar", []))
    fim_voz = None if fim_bruto is None else d - (b_ult - fim_bruto)
    ini_tr, pad = d - transicao, 0.0
    if fim_voz is not None and fim_voz + FOLGA_S > ini_tr:
        pad = float(np.ceil((fim_voz + FOLGA_S - ini_tr) * 30 - 1e-6) / 30)   # quadros inteiros
        ini_tr = d + pad - transicao
    voz_cta = onset_voz_cta(ff, cta)
    fade_in = transicao if voz_cta is None or voz_cta >= transicao + 0.05 else max(0.03, voz_cta - 0.05)
    d_cta = duracao(ff, cta)
    return {"conteudo_s": round(d, 3), "fim_voz_conteudo_s": None if fim_voz is None else round(fim_voz, 3),
            "pad_s": round(pad, 3), "inicio_transicao_s": round(ini_tr, 3), "transicao_s": transicao,
            "fim_transicao_s": round(ini_tr + transicao, 3), "cta": os.path.basename(cta), "cta_s": round(d_cta, 3),
            "voz_cta_s": voz_cta, "fade_in_audio_cta_s": round(fade_in, 3),
            "total_esperado_s": round(d + pad + d_cta - transicao, 3)}


def filtro_emenda(info, w, h):
    """Trecho do filter_complex: [vo]/[ac] (conteúdo) + entrada 1 (CTA) -> [vx]/[ax]."""
    t, pad, ini = info["transicao_s"], info["pad_s"], info["inicio_transicao_s"]
    norm = "fps=30,format=yuv420p,setsar=1,settb=AVTB"
    fv = (f"[vo]{norm},tpad=stop_mode=clone:stop_duration={pad:.4f}[vct];"
          f"[1:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},{norm}[vcta];"
          f"[vct][vcta]xfade=transition=fade:duration={t}:offset={ini:.4f}[vx]")
    fmt = "aformat=sample_rates=48000:channel_layouts=stereo"
    if abs(info["fade_in_audio_cta_s"] - t) < 1e-6:
        fa = (f"[ac]{fmt},apad=pad_dur={pad:.4f}[act];[1:a]{fmt}[acta];"
              f"[act][acta]acrossfade=d={t}:c1=tri:c2=tri[ax]")
    else:   # voz do CTA cedo: o fade de entrada dele encurta para não engolir a 1ª palavra
        ms = int(round(ini * 1000))
        fa = (f"[ac]{fmt},apad=pad_dur={pad:.4f},afade=t=out:st={ini:.4f}:d={t}[act];"
              f"[1:a]{fmt},afade=t=in:d={info['fade_in_audio_cta_s']:.3f},adelay={ms}|{ms}[acta];"
              f"[act][acta]amix=inputs=2:normalize=0:duration=longest[ax]")
    return fv + ";" + fa


def conferir(ff, saida, info):
    err = subprocess.run([ff, "-v", "error", "-i", saida, "-f", "null", "-"], capture_output=True, text=True).stderr
    if err.strip():
        sys.exit(f"ERRO ao decodificar {saida}: {err[:300]}")
    d = duracao(ff, saida)
    if abs(d - info["total_esperado_s"]) > 0.1:
        sys.exit(f"ERRO: duração {d:.3f} s, esperado {info['total_esperado_s']:.3f} s ({saida})")
    if info["fim_voz_conteudo_s"] is not None and info["fim_voz_conteudo_s"] + FOLGA_S > info["inicio_transicao_s"] + 0.01:
        sys.exit(f"ERRO: a transição começa antes do fim da fala ({saida})")


def main(argv):
    transicao = TRANSICAO_PADRAO
    if "--transicao" in argv:
        i = argv.index("--transicao")
        transicao = float(argv[i + 1].replace(",", "."))
        argv = argv[:i] + argv[i + 2:]
    if len(argv) < 2:
        sys.exit(__doc__)
    projeto, cta, so = os.path.abspath(argv[0]), os.path.abspath(argv[1]), argv[2:]
    pasta = os.path.dirname(projeto)
    cfg = json.load(open(projeto, encoding="utf-8"))
    ff = cfg.get("ffmpeg", "ffmpeg")

    extra = ["--cta", cta, "--transicao", str(transicao)] if transicao > 0 else []
    subprocess.run([sys.executable, os.path.join(AQUI, "fea_editar_video.py"), projeto, "--entrega", *extra, *so],
                   cwd=pasta, check=True)

    acima = []
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        base = os.path.join(pasta, v["saida"])
        d = duracao(ff, base)
        if v.get("sem_cta"):   # versão sem o CTA de campanha (ex.: a do CTA da FEB falado pelo Dr.)
            print(f"{'OK' if d <= LIMITE_TOTAL_S else 'ACIMA DE 3 MIN'} (sem CTA): {v['saida']} | {d:.1f}s", flush=True)
            if d > LIMITE_TOTAL_S:
                acima.append(v["saida"])
            continue
        txt = ""
        if transicao > 0:      # CTA já entrou no render, com a transição
            info = json.load(open(base.rsplit(".", 1)[0] + ".emenda.json", encoding="utf-8"))
            conferir(ff, base, info)
            txt = (f" | transição {info['transicao_s']} s em {info['inicio_transicao_s']:.2f} s"
                   f" (voz termina em {info['fim_voz_conteudo_s']} s, tpad {info['pad_s']} s)")
        else:                  # corte seco por stream copy (padrão antigo, só se pedido)
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=pasta) as lista:
                lista.write(f"file '{base}'\nfile '{cta}'\n")
            final = base + ".final.mp4"
            subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista.name,
                            "-c", "copy", "-movflags", "+faststart", final], check=True)
            os.unlink(lista.name)
            os.replace(final, base)
            d = duracao(ff, base)
        mb = os.path.getsize(base) / 1024 / 1024
        marca = "OK" if d <= LIMITE_TOTAL_S else "ACIMA DE 3 MIN"
        if d > LIMITE_TOTAL_S:
            acima.append(v["saida"])
        print(f"{marca}: {v['saida']} | {d:.1f}s | {mb:.1f} MB{txt}", flush=True)

    if acima:
        sys.exit("ERRO: passam de 3 min com CTA, cortar mais: " + ", ".join(acima))


if __name__ == "__main__":
    main(sys.argv[1:])
