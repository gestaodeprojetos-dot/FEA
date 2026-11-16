#!/usr/bin/env python3
"""FEA: corta trechos e/ou o começo de um vídeo JÁ ENTREGUE COM CTA, sem re-renderizar pelo projeto.

Por que existe (16/11/2026, pasta 19 de "11- Novembro"): a Keila pediu (1) total com CTA nunca acima
de 3:00, com corte generoso nos que passaram (meta 2:30 a 2:45), e (2) vídeo abrindo já com o Dr.
falando. Re-renderizar pelo projeto exige retranscrever o bruto, e a transcrição nova muda a legenda
aprovada (PR #86). Aqui a fonte é o próprio vídeo entregue, com a legenda aprovada queimada, a
transição e o CTA já aplicados (fea_aplicar_cta_entregue.py): o final (transição + CTA) fica
exatamente como foi aprovado.

Como monta (tempos em segundos DO ENTREGUE; cada corte vira um número inteiro de quadros, n/30):
1. Começo (--inicio T): os 3 s do título são refeitos sobre o BRUTO a partir do quadro do bruto que
   corresponde a T no entregue (alinhamento de quadros, como o fea_alinhar.py), com o mesmo .ass do
   título do fea_editar_video.py. Assim o título continua com 3 s inteiros.
2. Cortes (--cortar A B, repetível): o trecho [A, B) do entregue sai. Os cortes devem cair entre
   blocos de legenda (sem legenda na tela nos dois pontos) e num respiro da fala: o script confere
   a faixa da legenda nos quadros A-1, A, B-1 e B e a voz no áudio (ERRO se houver legenda ou voz).
3. Vídeo: os trechos do entregue entre quadros-chave vão por stream copy (os mesmos bytes
   aprovados); só os quadros perto de cada emenda (do ponto de corte até o próximo quadro-chave, e
   do último quadro-chave até o ponto de corte) são recodificados com os mesmos parâmetros x264 do
   entregue (preset medium, CRF 18, High, bt709). Confere SPS/PPS, DTS crescente e framemd5 de
   cada pedaço. Se a emenda por cópia falhar, recodifica o vídeo inteiro com CRF 16.
4. Áudio: o áudio do entregue nos mesmos trechos, com fade de 15 ms em cada emenda (no respiro) e
   fade-in de 30 ms no começo, codificado uma vez em AAC 192k 48 kHz.

Conferências (para com ERRO se falhar): legenda e voz nos pontos de corte; quadros copiados idênticos
ao entregue; quadros recodificados com PSNR >= 40 dB; áudio em sincronia com o entregue (±2 ms) em
cada trecho; voz começando entre 0,25 e 0,60 s (fea_revisar.checar_inicio); H.264 1080x1920 30 fps,
AAC 48 kHz; total até 180 s.

Uso:
    python3 fea_recortar_entregue.py FFMPEG FONTS ENTREGUE.mp4 BRUTO.MOV "Título" SAIDA.mp4 \
        [--inicio T] [--cortar A B ...] [--titulo-origem imagem|inventado] [--modo cauda|inteiro]
        [--cta-quadros 1185]   (quadros do CTA no fim do entregue, para o .emenda.json da revisora)
"""
import json, os, re, subprocess, sys, tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fea_editar_video as fe  # noqa: E402
import fea_trocar_cta as tc  # noqa: E402
import fea_aplicar_cta_entregue as ac  # noqa: E402
import fea_alinhar as al  # noqa: E402

FPS = 30
W, H = 1080, 1920
TIT = int(fe.TITULO_DUR * FPS)       # 90 quadros de título
LIMITE_TOTAL_S = 180.0
X264 = ac.X264


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def faixa_legenda(ff, arq, quadros):
    """Pixels brancos (texto) na faixa da legenda (72% a 90% da altura, reduzida para 270x86) em cada
    quadro pedido. Sem legenda: 0 a 3; legenda curta de 2 palavras ("se der"): ~20; normal: 100+."""
    out = {}
    for q in quadros:
        raw = run([ff, "-nostdin", "-v", "error", "-ss", f"{q / FPS + 0.001:.4f}", "-i", arq, "-vf",
                   f"crop={W}:{int(H * 0.18)}:0:{int(H * 0.72)},scale=270:86,format=gray",
                   "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True).stdout
        m = np.frombuffer(raw, np.uint8)
        out[q] = int((m > 235).sum())
    return out


def db_janelas(ff, arq, ini, dur, passo=0.01):
    a = ac.pcm(ff, arq, max(0.0, ini), dur)
    n = int(16000 * passo)
    k = len(a) // n
    return 20 * np.log10(np.sqrt((a[:k * n].reshape(k, n) ** 2).mean(axis=1)) + 1)


def mapa_bruto(ff, entregue, bruto, ate_q):
    """Quadro do bruto para cada quadro 0..ate_q-1 do entregue (offset por trecho, alinhamento de
    miniaturas da faixa de cima, sem título e sem legenda)."""
    e = al.miniaturas(ff, entregue)[:ate_q]
    b = al.miniaturas(ff, bruto)
    c = al.normalizar(e) @ al.normalizar(b).T
    j = c.argmax(1)
    off = j - np.arange(len(j))
    # offset por trecho: mediana numa janela de 15 quadros (tolera quadro parado)
    res = np.zeros(len(j), int)
    for i in range(len(j)):
        res[i] = int(np.median(off[max(0, i - 7):i + 8]))
    return np.arange(len(j)) + res, float(np.median(c.max(1)))


def main():
    args = sys.argv[1:]
    inicio, cortes, origem, modo = 0.0, [], "imagem", "cauda"
    cta_q, transicao = 1185, 0.5      # Ads 22 MTI Comente AULA: 39,50 s; transição de 0,5 s
    i = 0
    resto = []
    while i < len(args):
        if args[i] == "--inicio":
            inicio = float(args[i + 1]); i += 2
        elif args[i] == "--cortar":
            cortes.append((float(args[i + 1]), float(args[i + 2]))); i += 3
        elif args[i] == "--titulo-origem":
            origem = args[i + 1]; i += 2
        elif args[i] == "--cta-quadros":
            cta_q = int(args[i + 1]); i += 2
        elif args[i] == "--modo":
            modo = args[i + 1]; i += 2
        else:
            resto.append(args[i]); i += 1
    if len(resto) != 6:
        sys.exit(__doc__)
    ff, fonts, entregue, bruto, titulo, saida = resto
    nome = os.path.basename(saida)
    nq = ac.n_quadros(entregue)
    n0 = round(inicio * FPS)
    cq = sorted((round(a * FPS), round(b * FPS)) for a, b in cortes)
    erros = []

    # trechos mantidos (quadros do entregue)
    trechos, p = [], n0
    for a, b in cq:
        if a <= p + TIT or b <= a or b >= nq - cta_q - 15:
            sys.exit(f"ERRO: corte {a / FPS:.2f}-{b / FPS:.2f} inválido (dentro do título ou fora do vídeo)")
        trechos.append((p, a))
        p = b
    trechos.append((p, nq))
    total_q = sum(b - a for a, b in trechos)

    # ---- conferência dos pontos de corte: legenda e voz
    for a, b in cq:
        leg = faixa_legenda(ff, entregue, [a - 1, a, b - 1, b])
        if max(leg.values()) > 8:
            erros.append(f"corte {a / FPS:.2f}-{b / FPS:.2f}: legenda na tela no ponto de corte "
                         f"({', '.join(f'q{k}={v}' for k, v in leg.items())})")
        for t in (a / FPS, b / FPS):
            db = db_janelas(ff, entregue, t - 0.06, 0.12)
            if db.max() > 45:
                erros.append(f"corte {a / FPS:.2f}-{b / FPS:.2f}: voz no ponto {t:.2f} s ({db.max():.0f} dB)")

    # ---- mapa entregue -> bruto para o título novo
    mapa = None
    if n0 > 0:
        mapa, corr = mapa_bruto(ff, entregue, bruto, n0 + TIT + 30)
        if corr < 0.9:
            sys.exit(f"ERRO: o bruto não corresponde ao entregue (correlação {corr:.3f})")
        rq = mapa[n0:n0 + TIT]
        # trechos contínuos do bruto dentro dos 3 s do título
        runs, s = [], 0
        for k in range(1, TIT + 1):
            if k == TIT or rq[k] != rq[k - 1] + 1:
                runs.append((int(rq[s]), int(rq[k - 1]) + 1))
                s = k
        print(f"  título novo sobre o bruto: quadros {runs} (correlação {corr:.3f})", flush=True)

    # ---- sequência de saída: (fonte, quadro)
    #   cabeça: título sobre o bruto (se n0 > 0); depois quadros do entregue
    seq_ent = [q for a, b in trechos for q in range(a, b)]
    if n0 > 0:
        seq_ent = seq_ent[TIT:]
    keys = set(ac.keyframes_q(entregue))

    # pedaços: ("titulo", None) | ("enc", [quadros]) | ("copia", k1, k2)
    pedacos = []
    if n0 > 0:
        pedacos.append(("titulo", runs))
    # runs contínuos de quadros do entregue
    blocos, s = [], 0
    for k in range(1, len(seq_ent) + 1):
        if k == len(seq_ent) or seq_ent[k] != seq_ent[k - 1] + 1:
            blocos.append((seq_ent[s], seq_ent[k - 1] + 1))
            s = k
    for a, b in blocos:
        ks = sorted(k for k in keys if a <= k <= b)
        k1 = next((k for k in ks if k >= a), None)
        k2 = nq if b == nq else (max(k for k in ks if k <= b) if ks else None)
        if modo == "cauda" and k1 is not None and k2 is not None and k2 - k1 >= 15:
            if k1 > a:
                pedacos.append(("enc", a, k1))
            pedacos.append(("copia", k1, k2))
            if b > k2:
                pedacos.append(("enc", k2, b))
        else:
            pedacos.append(("enc", a, b))

    pasta = os.path.dirname(os.path.abspath(saida))
    q_ent = tc.md5s_video(ff, entregue)
    with tempfile.TemporaryDirectory(dir=pasta) as tmp:
        ass = os.path.join(tmp, "titulo.ass")
        with open(ass, "w", encoding="utf-8") as f:
            f.write(fe.ass_header() + "".join(fe.dialogos_linhas(1, 0, fe.TITULO_DUR, "Titulo",
                    fe.formatar_titulo({"titulo": titulo, "titulo_origem": origem}), r"\fad(0,250)")))
        esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        norm = "format=yuv420p,setsar=1"

        def gerar(modo_v):
            arqs, esperado = [], []
            if modo_v == "inteiro":
                partes = []
                if n0 > 0:
                    tr = "".join(f"[0:v]trim=start_frame={x}:end_frame={y},setpts=PTS-STARTPTS[r{i}];"
                                 for i, (x, y) in enumerate(runs))
                    partes.append(tr + "".join(f"[r{i}]" for i in range(len(runs))) +
                                  f"concat=n={len(runs)}:v=1:a=0,scale={W}:{H}:force_original_aspect_ratio=increase,"
                                  f"crop={W}:{H},{norm},ass='{esc}':fontsdir='{fonts}'[tt];")
                fl = "".join(partes)
                ent_bl = []
                for i, (a, b) in enumerate(blocos):
                    fl += f"[1:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,{norm}[e{i}];"
                    ent_bl.append(f"[e{i}]")
                ins = (["[tt]"] if n0 > 0 else []) + ent_bl
                fl += "".join(ins) + f"concat=n={len(ins)}:v=1:a=0,fps={FPS}[v]"
                out = os.path.join(tmp, "video.mp4")
                run([ff, "-nostdin", "-y", "-v", "error", "-i", bruto, "-i", entregue, "-filter_complex", fl,
                     "-map", "[v]", *X264, "-crf", "16", "-an", out])
                return out, None
            for i, pc in enumerate(pedacos):
                arq = os.path.join(tmp, f"p{i:02d}.mp4")
                if pc[0] == "titulo":
                    tr = "".join(f"[0:v]trim=start_frame={x}:end_frame={y},setpts=PTS-STARTPTS[r{j}];"
                                 for j, (x, y) in enumerate(pc[1]))
                    fl = (tr + "".join(f"[r{j}]" for j in range(len(pc[1]))) +
                          f"concat=n={len(pc[1])}:v=1:a=0,scale={W}:{H}:force_original_aspect_ratio=increase,"
                          f"crop={W}:{H},{norm},ass='{esc}':fontsdir='{fonts}',fps={FPS}[v]")
                    run([ff, "-nostdin", "-y", "-v", "error", "-i", bruto, "-filter_complex", fl, "-map", "[v]",
                         *X264, "-crf", "18", "-an", arq])
                    esperado.append(("enc", arq, TIT))
                elif pc[0] == "enc":
                    a, b = pc[1], pc[2]
                    fl = f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,{norm},fps={FPS}[v]"
                    run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-filter_complex", fl, "-map", "[v]",
                         *X264, "-crf", "18", "-an", arq])
                    esperado.append(("enc", arq, b - a))
                else:
                    k1, k2 = pc[1], pc[2]
                    run([ff, "-nostdin", "-y", "-v", "error", "-ss", f"{k1 / FPS:.6f}", "-i", entregue, "-map", "0:v:0",
                         "-c", "copy", "-frames:v", str(k2 - k1), "-avoid_negative_ts", "make_zero", arq])
                    esperado.append(("copia", arq, (k1, k2)))
                arqs.append(arq)
            av = tc.avcc(entregue)
            for _, arq, _x in esperado:
                if tc.avcc(arq) != av:
                    return None, f"SPS/PPS diferente em {os.path.basename(arq)}"
            lista = os.path.join(tmp, "v.txt")
            with open(lista, "w") as f:
                f.write("".join(f"file '{a}'\n" for a in arqs))
            out = os.path.join(tmp, "video.mp4")
            run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", out])
            ok_dts, _ = ac.dts_ok(out)
            if not ok_dts:
                return None, "DTS repetido/fora de ordem"
            q_v = tc.md5s_video(ff, out)
            pos = 0
            for tipo, arq, x in esperado:
                if tipo == "copia":
                    k1, k2 = x
                    if q_v[pos:pos + k2 - k1] != q_ent[k1:k2]:
                        return None, f"quadros copiados {k1}-{k2} diferem do entregue"
                    pos += k2 - k1
                else:
                    q_p = tc.md5s_video(ff, arq)
                    if len(q_p) != x or q_v[pos:pos + x] != q_p:
                        return None, f"quadros recodificados de {os.path.basename(arq)} diferem"
                    pos += x
            if pos != total_q or len(q_v) != total_q:
                return None, f"{len(q_v)} quadros, esperado {total_q}"
            return out, None

        video, motivo = (None, None)
        if modo == "cauda":
            video, motivo = gerar("cauda")
            if video is None:
                print(f"  {nome}: emenda por cópia falhou ({motivo}); recodifica inteiro com CRF 16", flush=True)
                modo = "inteiro"
        if video is None:
            video, _ = gerar("inteiro")

        # ---- áudio: trechos do entregue, fade de 15 ms nas emendas, 30 ms no começo
        fmt = "aformat=sample_rates=48000:channel_layouts=stereo"
        fa, ins = "", []
        for i, (a, b) in enumerate(trechos):
            ta, tb = a / FPS, b / FPS
            f_in = 0.03 if i == 0 else 0.015
            f_out = f"afade=t=out:st={tb - ta - 0.015:.4f}:d=0.015," if b != nq else ""
            fa += (f"[0:a]atrim=start={ta:.6f}:end={tb:.6f},asetpts=PTS-STARTPTS,{fmt},"
                   f"afade=t=in:st=0:d={f_in},{f_out}apad=whole_dur={tb - ta:.6f},atrim=end={tb - ta:.6f}[a{i}];")
            ins.append(f"[a{i}]")
        fa += "".join(ins) + f"concat=n={len(ins)}:v=0:a=1[ax]"
        audio = os.path.join(tmp, "audio.m4a")
        run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-filter_complex", fa, "-map", "[ax]",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", audio])
        run([ff, "-nostdin", "-y", "-v", "error", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
             "-c", "copy", "-movflags", "+faststart", saida])

    # ---- conferências finais
    err = subprocess.run([ff, "-v", "error", "-i", saida, "-f", "null", "-"], capture_output=True, text=True).stderr
    if err.strip():
        erros.append(f"decodificação com erro: {err[:200]}")
    nq_s = ac.n_quadros(saida)
    if nq_s != total_q:
        erros.append(f"{nq_s} quadros, esperado {total_q}")
    # sincronia do áudio em cada trecho (meio do trecho), contra o entregue
    pos, sinc = 0, []
    for a, b in trechos:
        d = (b - a) / FPS
        if d >= 3.5:
            meio = pos / FPS + d / 2 - 1.0
            lag, cr = ac.atraso_ms(ff, entregue, a / FPS + d / 2 - 1.0, saida, meio, 2.0)
            sinc.append(round(lag, 1))
            if abs(lag) > 2 or cr < 0.95:
                erros.append(f"áudio fora de sincronia no trecho {a / FPS:.2f}-{b / FPS:.2f} ({lag:+.1f} ms, corr {cr:.3f})")
        pos += b - a
    # PSNR dos quadros do entregue depois do título (pega erro de mapeamento de quadro)
    if n0 > 0 or cq:
        k = TIT if n0 > 0 else 0
        p_ini = ac.psnr(ff, saida, k, entregue, seq_ent[0] if n0 > 0 else 0, 60)
        if p_ini < 40:
            erros.append(f"quadros depois do título com PSNR {p_ini:.1f} dB (< 40)")
    dur, txt = tc.info(ff, saida)
    if "1080x1920" not in txt or "h264" not in txt or "hevc" in txt or "48000 Hz" not in txt \
            or not re.search(r"(29\.9\d|30) fps", txt):
        erros.append("formato inesperado")
    if dur > LIMITE_TOTAL_S + 0.05:
        erros.append(f"total {dur:.2f} s passa de 3:00 (Keila, 16/11/2026: total com CTA nunca acima de 180 s)")
    import fea_revisar as fr
    e_ini, a_ini, info_ini = fr.checar_inicio(ff, saida, transcrever=False)
    erros += e_ini
    info = {"entregue": os.path.basename(entregue), "inicio_s": n0 / FPS,
            "cortes_s": [[a / FPS, b / FPS] for a, b in cq], "trechos_s": [[a / FPS, b / FPS] for a, b in trechos],
            "modo": modo, "pedacos": [list(p[:1]) + [int(x) if not isinstance(x, list) else x for x in p[1:]]
                                      for p in pedacos] if modo == "cauda" else None,
            "voz_s": round(info_ini["voz"], 3), "total_s": round(dur, 3), "sincronia_ms": sinc}
    json.dump(info, open(saida.rsplit(".", 1)[0] + ".recorte.json", "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    # .emenda.json para a revisora (checar_emenda): a transição e o CTA são os do entregue, sem
    # mudança; só o instante muda (o que foi cortado antes dela). O CTA são os últimos cta_q quadros.
    ini_tr = (total_q - cta_q) / FPS
    import fea_render_com_cta as rc
    fv = rc.fim_da_voz(ff, saida, max(0.0, ini_tr - 8), ini_tr)
    if fv is not None and fv + 0.05 > ini_tr:
        erros.append(f"transição em {ini_tr:.2f} s e a voz termina em {fv:.2f} s")
    json.dump({"transicao_s": transicao, "inicio_transicao_s": round(ini_tr, 3),
               "fim_transicao_s": round(ini_tr + transicao, 3),
               "fim_voz_conteudo_s": None if fv is None else round(fv, 3), "cta_s": round(cta_q / FPS, 3),
               "total_s": round(dur, 3), "fonte": f"recorte de {os.path.basename(entregue)} (transição e CTA do entregue)"},
              open(saida.rsplit(".", 1)[0] + ".emenda.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{'ERRO' if erros else 'OK'}: {nome} | modo {modo} | início +{n0 / FPS:.2f} s | "
          f"{len(cq)} corte(s), {sum(b - a for a, b in cq) / FPS:.2f} s | voz em {info_ini['voz']:.2f} s | "
          f"total {dur:.2f} s | sinc {sinc} ms", flush=True)
    for x in a_ini:
        print(f"  ATENÇÃO  {x}")
    for e in erros:
        print(f"  ERRO {e}")
    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
