#!/usr/bin/env python3
"""FEA: coloca o CTA (com a transição de ~0,5 s) num vídeo já entregue SEM CTA, sem re-renderizar.

Por que existe (12/11/2026, pastas 17 a 20 de "11- Novembro"): o lote saiu sem CTA (regra de
09/11) e a Keila pediu o CTA "que criamos" (Ads 22 MTI + card "Comente AULA"). Re-renderizar pelo
projeto exige retranscrever o bruto, e a transcrição nova muda a legenda aprovada (PR #86). Aqui a
fonte é o próprio vídeo entregue, com a legenda aprovada já queimada.

Como monta (t = 0 no começo do entregue):
1. Mede o fade_final do entregue (os ~0,3 s finais escurecendo) quadro a quadro, pela luminância,
   e corta o conteúdo no último quadro antes do fade (fs quadros). O áudio é cortado no mesmo ponto.
2. Mede o fim da voz do Dr. no áudio do entregue (fea_render_com_cta.fim_da_voz, janelas de 10 ms).
   A transição só começa 0,10 s depois da última palavra; se o conteúdo acaba colado na fala, o
   último quadro é estendido (tpad clone) e o áudio ganha silêncio, igual ao fea_render_com_cta.py.
3. Crossfade de vídeo (xfade fade) e de áudio (acrossfade) para o CTA inteiro.
4. Vídeo (modo "cauda", padrão): do começo até o último quadro-chave (IDR) antes da transição, o
   fluxo do entregue por stream copy (os mesmos bytes aprovados); dali em diante, cauda recodificada
   com os mesmos parâmetros x264 do entregue (preset medium, CRF 18, High, bt709), e as duas partes
   emendadas por stream copy. Confere SPS/PPS, DTS crescente na emenda e framemd5.
   Modo "inteiro" (fallback, ou --modo inteiro): recodifica o vídeo inteiro a partir do entregue
   com CRF 16 (perda de geração mínima).
   Áudio: o áudio do entregue até o corte + CTA, com o acrossfade, codificado uma vez em AAC 192k
   48 kHz (o AAC não emenda por cópia sem estalo na junção).
5. Grava NOME.emenda.json ao lado da saída (lido pela revisora, checar_emenda).

Conferências (para com ERRO se falhar):
- modo cauda: quadros até o quadro-chave idênticos ao entregue (framemd5); modo inteiro: PSNR;
- quadros recodificados do conteúdo parecidos com o entregue (PSNR >= 40 dB);
- CTA depois da transição parecido com o CTA (PSNR >= 38 dB) e áudio do CTA em sincronia;
- áudio do conteúdo em sincronia com o entregue (±2 ms);
- transição começa depois do fim da voz; H.264 1080x1920 30 fps, AAC 48 kHz.

Uso:
    python3 fea_aplicar_cta_entregue.py FFMPEG ENTREGUE.mp4 CTA.mp4 SAIDA.mp4 [--transicao 0.5] [--modo cauda|inteiro]
"""
import json, os, re, subprocess, sys, tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fea_render_com_cta as rc  # noqa: E402
import fea_trocar_cta as tc  # noqa: E402

FPS = 30
W, H = 1080, 1920
FOLGA_S = rc.FOLGA_S
X264 = ["-c:v", "libx264", "-preset", "medium", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
        "-r", str(FPS)]


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def n_quadros(arq):
    r = run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
             "stream=nb_read_packets", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    return int(r.strip().strip(","))


def lumas(ff, arq, ini_q, n):
    """Luminância média (0-255) dos quadros ini_q .. ini_q+n-1."""
    raw = run([ff, "-nostdin", "-v", "error", "-i", arq, "-vf",
               f"select=gte(n\\,{ini_q}),scale=108:192,format=gray", "-fps_mode", "passthrough",
               "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float).mean(axis=(1, 2))


def medir_fade(ff, arq, nq):
    """Primeiro quadro do fade_final (o conteúdo vai até o quadro anterior). Do fim para trás,
    enquanto cada quadro é claramente mais escuro que o anterior, está dentro do fade."""
    k = min(45, nq)
    m = lumas(ff, arq, nq - k, k)
    j = len(m) - 1
    while j > 0 and m[j - 1] - m[j] > max(0.8, 0.25 * (m[j - 1] - 16) / 9):
        j -= 1
    return nq - k + j, m


def keyframes_q(arq):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time,flags",
             "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    ts = sorted(float(a) for a, f in (ln.split(",")[:2] for ln in r.split()) if "K" in f)
    return [round(t * FPS) for t in ts]


def dts_ok(arq):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=dts",
             "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    d = [int(x.strip(",")) for x in r.split() if x.strip(",").lstrip("-").isdigit()]
    return all(b > a for a, b in zip(d, d[1:])), len(d)


def psnr(ff, a, ini_a, b, ini_b, n):
    f = (f"[0:v]trim=start_frame={ini_a}:end_frame={ini_a + n},setpts=PTS-STARTPTS,format=yuv420p[x];"
         f"[1:v]trim=start_frame={ini_b}:end_frame={ini_b + n},setpts=PTS-STARTPTS,format=yuv420p,"
         f"scale={W}:{H}[y];[x][y]psnr")
    err = subprocess.run([ff, "-nostdin", "-hide_banner", "-i", a, "-i", b, "-filter_complex", f, "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"average:([\d.]+|inf)", err)
    return float("inf") if m and m.group(1) == "inf" else (float(m.group(1)) if m else 0.0)


def pcm(ff, arq, ss, t, sr=16000):
    c = [ff, "-nostdin", "-v", "error", "-i", arq, "-ss", f"{ss:.4f}", "-t", f"{t:.4f}",
         "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    return np.frombuffer(run(c, capture_output=True).stdout, np.int16).astype(float)


def atraso_ms(ff, ref, ini_ref, novo, ini_novo, dur=3.0):
    """Atraso (ms) do áudio de `novo` em ini_novo em relação a `ref` em ini_ref (correlação ±100 ms)."""
    a = pcm(ff, ref, ini_ref - 0.1, dur + 0.2)
    b = pcm(ff, novo, ini_novo, dur)
    if np.abs(b).max() < 50:
        return 0.0, 0.0
    c = np.correlate(a, b, "valid")
    k = int(np.argmax(c))
    corr = c[k] / (np.linalg.norm(b) * np.linalg.norm(a[k:k + len(b)]) + 1e-9)
    return (1600 - k) / 16, float(corr)


def main():
    args = sys.argv[1:]
    transicao, modo = 0.5, "cauda"
    if "--transicao" in args:
        i = args.index("--transicao")
        transicao = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    if "--modo" in args:
        i = args.index("--modo")
        modo = args[i + 1]
        args = args[:i] + args[i + 2:]
    if len(args) != 4:
        sys.exit(__doc__)
    ff, entregue, cta, saida = args
    nome = os.path.basename(saida)

    nq = n_quadros(entregue)
    fs, m = medir_fade(ff, entregue, nq)
    if nq - fs < 3 or nq - fs > 15:
        sys.exit(f"ERRO: fade final de {nq - fs} quadros em {nome} (esperado ~9): conferir; lumas finais "
                 + " ".join(f"{x:.0f}" for x in m[-15:]))
    d = fs / FPS
    # fim da voz medido no arquivo inteiro (com o trecho do fade): se houver som de voz dentro do
    # fade, cortar ali engoliria o fim da palavra -> ERRO. Nos entregues de novembro o áudio do
    # trecho do fade já é silêncio digital, e a voz termina no máximo no primeiro quadro do fade.
    fim_voz = rc.fim_da_voz(ff, entregue, max(0.0, nq / FPS - 8), nq / FPS)
    if fim_voz is not None and fim_voz > d + 0.02:
        sys.exit(f"ERRO: a voz vai até {fim_voz:.2f} s e o fade começa em {d:.2f} s ({nome}): palavra dentro do fade")
    if fim_voz is not None:
        fim_voz = min(fim_voz, d)
    ini_tr, pad = d - transicao, 0.0
    if fim_voz is not None and fim_voz + FOLGA_S > ini_tr:
        pad = float(np.ceil((fim_voz + FOLGA_S - ini_tr) * FPS - 1e-6) / FPS)
        ini_tr = d + pad - transicao
    voz_cta = rc.onset_voz_cta(ff, cta)
    fade_in = transicao if voz_cta is None or voz_cta >= transicao + 0.05 else max(0.03, voz_cta - 0.05)
    nq_cta = n_quadros(cta)
    d_cta = nq_cta / FPS
    info = {"conteudo_s": round(d, 3), "fim_voz_conteudo_s": None if fim_voz is None else round(fim_voz, 3),
            "pad_s": round(pad, 3), "inicio_transicao_s": round(ini_tr, 3), "transicao_s": transicao,
            "fim_transicao_s": round(ini_tr + transicao, 3), "cta": os.path.basename(cta), "cta_s": round(d_cta, 3),
            "voz_cta_s": voz_cta, "fade_in_audio_cta_s": round(fade_in, 3),
            "total_esperado_s": round(d + pad + d_cta - transicao, 3),
            "fonte": "vídeo entregue sem CTA (fade_final removido)", "quadros_fade_removidos": nq - fs}
    q_ini_tr = round(ini_tr * FPS)
    n_total = q_ini_tr + nq_cta

    pasta = os.path.dirname(os.path.abspath(saida))
    with tempfile.TemporaryDirectory(dir=pasta) as tmp:
        # ---- áudio: entregue até o corte + CTA, com acrossfade (uma codificação AAC)
        fmt = "aformat=sample_rates=48000:channel_layouts=stereo"
        if abs(fade_in - transicao) < 1e-6:
            fa = (f"[0:a]atrim=end={d:.6f},asetpts=PTS-STARTPTS,{fmt},apad=pad_dur={pad:.4f}[act];"
                  f"[1:a]{fmt}[acta];[act][acta]acrossfade=d={transicao}:c1=tri:c2=tri[ax]")
        else:
            ms = int(round(ini_tr * 1000))
            fa = (f"[0:a]atrim=end={d:.6f},asetpts=PTS-STARTPTS,{fmt},apad=pad_dur={pad:.4f},"
                  f"afade=t=out:st={ini_tr:.4f}:d={transicao}[act];"
                  f"[1:a]{fmt},afade=t=in:d={fade_in:.3f},adelay={ms}|{ms}[acta];"
                  f"[act][acta]amix=inputs=2:normalize=0:duration=longest[ax]")
        audio = os.path.join(tmp, "audio.m4a")
        run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-i", cta, "-filter_complex", fa,
             "-map", "[ax]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", audio])

        norm = "fps=30,format=yuv420p,setsar=1,settb=AVTB"
        cta_v = f"[1:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{norm}[vcta]"
        video = os.path.join(tmp, "video.mp4")
        k_copia, q_ent = 0, None
        if modo == "cauda":
            kfs = [k for k in keyframes_q(entregue) if 0 < k <= q_ini_tr - 15 and k < fs]
            if not kfs:
                print(f"  {nome}: sem quadro-chave antes da transição, recodifica inteiro", flush=True)
                modo = "inteiro"
            else:
                k_copia = kfs[-1]
                cab = os.path.join(tmp, "cabeca.mp4")
                run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-map", "0:v:0", "-c", "copy",
                     "-frames:v", str(k_copia), cab])
                fv = (f"[0:v]trim=start_frame={k_copia}:end_frame={fs},setpts=PTS-STARTPTS,{norm},"
                      f"tpad=stop_mode=clone:stop={round(pad * FPS)}[vct];{cta_v};"
                      f"[vct][vcta]xfade=transition=fade:duration={transicao}:offset={(q_ini_tr - k_copia) / FPS - 1e-5:.6f}[vx]")
                cauda = os.path.join(tmp, "cauda.mp4")
                run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-i", cta, "-filter_complex", fv,
                     "-map", "[vx]", *X264, "-crf", "18", "-an", cauda])
                ok_sps = tc.avcc(cauda) == tc.avcc(cab)
                lista = os.path.join(tmp, "v.txt")
                with open(lista, "w") as f:
                    f.write(f"file '{cab}'\nfile '{cauda}'\n")
                run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista,
                     "-c", "copy", video])
                ok_dts, npk = dts_ok(video)
                q_v = tc.md5s_video(ff, video)
                q_ent = tc.md5s_video(ff, entregue)
                q_cau = tc.md5s_video(ff, cauda)
                ok_q = q_v[:k_copia] == q_ent[:k_copia] and q_v[k_copia:] == q_cau and len(q_v) == n_total
                if not ok_q:
                    print(f"  diag: cabeça {q_v[:k_copia] == q_ent[:k_copia]} cauda {q_v[k_copia:] == q_cau} "
                          f"n {len(q_v)}/{n_total} cauda {len(q_cau)}", flush=True)
                if not (ok_sps and ok_dts and ok_q):
                    print(f"  {nome}: emenda por cópia falhou (SPS/PPS {'ok' if ok_sps else 'diferente'}, "
                          f"DTS {'ok' if ok_dts else 'repetido/fora de ordem'}, quadros {'ok' if ok_q else 'diferentes'}); "
                          "recodifica inteiro com CRF 16", flush=True)
                    modo, k_copia = "inteiro", 0
        if modo == "inteiro":
            fv = (f"[0:v]trim=end_frame={fs},setpts=PTS-STARTPTS,{norm},"
                  f"tpad=stop_mode=clone:stop={round(pad * FPS)}[vct];{cta_v};"
                  f"[vct][vcta]xfade=transition=fade:duration={transicao}:offset={q_ini_tr / FPS - 1e-5:.6f}[vx]")
            run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-i", cta, "-filter_complex", fv,
                 "-map", "[vx]", *X264, "-crf", "16", "-an", video])
        run([ff, "-nostdin", "-y", "-v", "error", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
             "-c", "copy", "-movflags", "+faststart", saida])
    info["modo"] = modo
    info["quadros_copiados"] = k_copia

    # ---- conferências
    erros = []
    err = subprocess.run([ff, "-v", "error", "-i", saida, "-f", "null", "-"], capture_output=True, text=True).stderr
    if err.strip():
        erros.append(f"decodificação com erro: {err[:200]}")
    nq_s = n_quadros(saida)
    if nq_s != n_total:
        erros.append(f"{nq_s} quadros, esperado {n_total}")
    if modo == "cauda":
        if tc.md5s_video(ff, saida)[:k_copia] != q_ent[:k_copia]:
            erros.append("quadros copiados diferem do entregue")
        p_cont = psnr(ff, saida, k_copia, entregue, k_copia, fs - k_copia)
    else:
        p_cont = psnr(ff, saida, 0, entregue, 0, fs)
    p_cta = psnr(ff, saida, q_ini_tr + 15, cta, 15, nq_cta - 15)
    if p_cont < 40:
        erros.append(f"conteúdo recodificado com PSNR {p_cont:.1f} dB (< 40)")
    if p_cta < 38:
        erros.append(f"CTA com PSNR {p_cta:.1f} dB (< 38)")
    lag_c, corr_c = atraso_ms(ff, entregue, min(5.0, d / 2), saida, min(5.0, d / 2), min(3.0, d / 3))
    lag_f, corr_f = atraso_ms(ff, entregue, max(0.2, d - 3.5), saida, max(0.2, d - 3.5), 2.5)
    lag_t, corr_t = atraso_ms(ff, cta, 3.0, saida, ini_tr + 3.0, 3.0)
    for nm, lag, cr in (("conteúdo", lag_c, corr_c), ("fim do conteúdo", lag_f, corr_f), ("CTA", lag_t, corr_t)):
        if abs(lag) > 2 or cr < 0.95:
            erros.append(f"áudio do {nm} fora de sincronia ({lag:+.1f} ms, correlação {cr:.3f})")
    dur, txt = tc.info(ff, saida)
    if "1080x1920" not in txt or "h264" not in txt or "hevc" in txt or "48000 Hz" not in txt \
            or not re.search(r"(29\.9\d|30) fps", txt):
        erros.append("formato inesperado")
    info.update({"psnr_conteudo_db": round(p_cont, 2), "psnr_cta_db": round(p_cta, 2),
                 "sincronia_ms": [round(lag_c, 1), round(lag_f, 1), round(lag_t, 1)], "total_s": round(dur, 3)})
    json.dump(info, open(saida.rsplit(".", 1)[0] + ".emenda.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{'ERRO' if erros else 'OK'}: {nome} | modo {modo} (cópia {k_copia} quadros) | fade {nq - fs} q removido | "
          f"conteúdo {d:.2f} s | voz até {fim_voz} s | tpad {pad:.3f} s | transição {ini_tr:.2f} s | "
          f"total {dur:.2f} s | PSNR conteúdo {p_cont:.1f} CTA {p_cta:.1f} | sinc {lag_c:+.1f}/{lag_f:+.1f}/{lag_t:+.1f} ms",
          flush=True)
    for e in erros:
        print(f"  ERRO {e}")
    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
