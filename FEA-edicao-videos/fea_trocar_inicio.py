#!/usr/bin/env python3
"""FEA: reedita só o INÍCIO de um vídeo já entregue, sem mexer no resto aprovado.

Por que existe (05/11/2026, pasta 4 de novembro): quem posta os vídeos estava cortando o começo
("às vezes ele demora para falar, ou não está iniciando num momento que prende") e a Keila notou
palavra cortada no começo. Re-renderizar o vídeo inteiro pelo projeto exige retranscrever o bruto,
e a transcrição nova muda palavras da legenda aprovada (PR #86). Aqui a legenda aprovada não é
recalculada: ela já está queimada nos quadros do vídeo entregue e é reaproveitada.

Como monta o vídeo novo (t' = 0 no novo início, que é o quadro do bruto em `inicio`):
1. 0 a 3 s: quadros do BRUTO a partir do novo início, com o título (mesmo .ass, fonte e posição
   do fea_editar_video.py). Legenda só depois do título, como no padrão.
2. 3 s até o próximo quadro-chave (IDR) do entregue: quadros DO ENTREGUE (já com a legenda
   aprovada queimada), decodificados e codificados de novo com os mesmos parâmetros x264.
3. Do quadro-chave até o fim do conteúdo: o fluxo de vídeo do entregue por stream copy (os mesmos
   bytes aprovados). Depois, o CTA por stream copy, como no fea_trocar_cta.py.
4. Áudio do conteúdo: o áudio do entregue a partir do novo início (mesma sincronia do aprovado),
   com fade-in de 30 ms, AAC 192k 48 kHz. Com --mudo-ate, o áudio fica mudo até esse instante
   (segundos do bruto) e entra com fade-in de 30 ms terminando nele: serve para tirar um
   aquecimento colado na frase do gancho ("Então são só alguns pontinhos" -> "São só...").

Só funciona quando o novo início é igual ou posterior ao início entregue (cortar o começo).

Conferências (para com ERRO se falhar):
- o final do entregue é o CTA, quadro a quadro (framemd5);
- o SPS/PPS do trecho recodificado é igual ao do entregue (a emenda por cópia decodifica certo);
- no vídeo novo, os quadros do quadro-chave em diante são idênticos ao entregue e o CTA idêntico;
- H.264 1080x1920 30 fps, AAC 48 kHz; conteúdo até 180 s;
- a voz começa pelo menos 0,40 s depois do início (fea_revisar.checar_inicio).

Uso:
    python3 fea_trocar_inicio.py FFMPEG FONTS ENTREGUE.mp4 CTA.mp4 BRUTO.MOV INICIO_ENTREGUE INICIO_NOVO \
        "Título" SAIDA.mp4 [--mudo-ate SEG_DO_BRUTO]
INICIO_ENTREGUE e INICIO_NOVO em segundos do bruto (o primeiro quadro do entregue é o quadro do
bruto em ceil(INICIO_ENTREGUE*30); use `auto` para medir pelo áudio).
"""
import math, os, re, subprocess, sys, tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402
import fea_trocar_cta as tc  # noqa: E402

FPS = 30
LIMITE_CONTEUDO_S = 180


def pcm(ff, arq, ss=0.0, t=None, sr=8000):
    c = [ff, "-nostdin", "-v", "error", "-ss", f"{ss:.6f}", "-i", arq] + (["-t", str(t)] if t else []) + \
        ["-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(c, capture_output=True, check=True).stdout, np.int16).astype(float)


def medir_inicio(ff, entregue, bruto, aprox=0.0):
    """Instante do bruto que corresponde ao t=0 do entregue (correlação do áudio, 0,5 a 4,5 s)."""
    e = pcm(ff, entregue, 0.5, 4.0)
    a = max(0.0, aprox - 1.0)
    r = pcm(ff, bruto, a, 12.0)
    c = np.correlate(r, e, "valid")
    k = int(np.argmax(c))
    return a + k / 8000 - 0.5


def keyframes(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey",
                        "-show_entries", "frame=pts_time", "-of", "csv=p=0", arq],
                       capture_output=True, text=True, check=True).stdout
    return [float(x.strip(",")) for x in r.split() if x.strip(",")]


def main():
    args = sys.argv[1:]
    mudo = None
    if "--mudo-ate" in args:
        i = args.index("--mudo-ate")
        mudo = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    if len(args) != 9:
        sys.exit(__doc__)
    ff, fonts, entregue, cta, bruto, ini_ent, ini_novo, titulo, saida = args
    ini_novo = float(ini_novo)
    if ini_ent == "auto":
        ini_ent = medir_inicio(ff, entregue, bruto, ini_novo) + 0.0214   # 0,0214 s: atraso do vídeo no MP4
    ini_ent = float(ini_ent)
    r0 = math.ceil(ini_ent * FPS - 1e-6)            # quadro do bruto no t=0 do entregue
    n = round(ini_novo * FPS) - r0                  # quadros que saem do começo
    if n < 0:
        sys.exit("ERRO: o novo início é anterior ao entregue; este script só corta o começo")
    s1 = (r0 + n) / FPS
    tit = int(fe.TITULO_DUR * FPS)                   # 90 quadros de título

    q_ent, q_cta = tc.md5s_video(ff, entregue), tc.md5s_video(ff, cta)
    nc = len(q_ent) - len(q_cta)
    if nc <= 0 or q_ent[nc:] != q_cta:
        sys.exit(f"ERRO: o final de {os.path.basename(entregue)} não é o CTA quadro a quadro")
    if (nc - n) / FPS > LIMITE_CONTEUDO_S:
        sys.exit("ERRO: o conteúdo passa de 3 min")

    pasta = os.path.dirname(os.path.abspath(saida))
    with tempfile.TemporaryDirectory(dir=pasta) as tmp:
        conteudo = os.path.join(tmp, "conteudo.mp4")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-map", "0:v:0", "-map", "0:a:0",
                        "-c", "copy", "-frames:v", str(nc), "-t", f"{nc / FPS:.6f}", conteudo], check=True)
        # quadro-chave do entregue logo depois do título novo
        t0v = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=start_time", "-of", "csv=p=0", conteudo],
                                   capture_output=True, text=True).stdout.strip().strip(",") or 0)
        kfs = [round((t - t0v) * FPS) for t in keyframes(conteudo)]
        kd = next((k for k in kfs if k >= n + tit), None)
        if kd is None:
            sys.exit("ERRO: sem quadro-chave depois do título novo")

        # 1+2. trecho recodificado: título sobre o bruto + quadros do entregue até o quadro-chave
        v = {"titulo": titulo, "titulo_origem": "imagem"}
        ass = os.path.join(tmp, "titulo.ass")
        with open(ass, "w", encoding="utf-8") as f:
            f.write(fe.ass_header() + "".join(fe.dialogos_linhas(1, 0, fe.TITULO_DUR, "Titulo",
                                                                  fe.formatar_titulo(v), r"\fad(0,250)")))
        esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        W, H = fe.W, fe.H
        filtro = (f"[0:v]trim=start_frame={r0 + n}:end_frame={r0 + n + tit},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                  f"ass='{esc}':fontsdir='{fonts}'[t];"
                  f"[1:v]trim=start_frame={n + tit}:end_frame={kd},setpts=PTS-STARTPTS,setsar=1[e];"
                  f"[t][e]concat=n=2:v=1:a=0,fps={FPS}[v]")
        cabeca = os.path.join(tmp, "cabeca.mp4")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-i", bruto, "-i", conteudo, "-filter_complex", filtro,
                        "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
                        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-color_range", "tv", "-r", str(FPS), "-an", cabeca], check=True)
        if tc.avcc(cabeca) != tc.avcc(conteudo):
            sys.exit("ERRO: SPS/PPS do trecho recodificado difere do entregue (emenda por cópia quebraria)")
        # 3. resto do entregue por stream copy, a partir do quadro-chave
        cauda = os.path.join(tmp, "cauda.mp4")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-ss", f"{t0v + kd / FPS:.6f}", "-i", conteudo,
                        "-map", "0:v:0", "-c", "copy", "-avoid_negative_ts", "make_zero", cauda], check=True)
        lista = os.path.join(tmp, "v.txt")
        with open(lista, "w") as f:
            f.write(f"file '{cabeca}'\nfile '{cauda}'\n")
        video = os.path.join(tmp, "video.mp4")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista,
                        "-c", "copy", video], check=True)
        # 4. áudio do entregue a partir do novo início, fade-in de 30 ms (ou mudo até --mudo-ate)
        dur = (nc - n) / FPS
        af = "afade=t=in:st=0:d=0.03"
        if mudo is not None:
            st = max(0.0, mudo - s1 - 0.03)
            af = f"afade=t=in:st={st:.3f}:d=0.03"
        novo_cont = os.path.join(tmp, "conteudo_novo.mp4")
        # atrim por amostra, decodificando desde o começo. +1024 amostras: o conteúdo recortado por
        # cópia decodifica com 1 quadro AAC (21,3 ms) a mais no começo (atraso do codificador) e o
        # áudio novo saía 21 ms atrasado em relação ao vídeo; a conferência de sincronia abaixo pega
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-i", video, "-i", conteudo,
                        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                        "-af", f"atrim=start_sample={round(n / FPS * 48000) + 1024},asetpts=PTS-STARTPTS,{af}",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{dur:.6f}", novo_cont],
                       check=True)
        lista = os.path.join(tmp, "final.txt")
        with open(lista, "w") as f:
            f.write(f"file '{novo_cont}'\nfile '{os.path.abspath(cta)}'\n")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista,
                        "-c", "copy", "-movflags", "+faststart", saida], check=True)
        q_cab = tc.md5s_video(ff, cabeca)

    q_sai = tc.md5s_video(ff, saida)
    k = kd - n
    if q_sai[:k] != q_cab:
        sys.exit("ERRO: trecho inicial do vídeo novo difere do recodificado")
    if q_sai[k:k + nc - kd] != q_ent[kd:nc]:
        sys.exit("ERRO: o conteúdo depois do quadro-chave difere do entregue")
    if q_sai[k + nc - kd:] != q_cta:
        sys.exit("ERRO: o CTA do vídeo novo difere do CTA")
    # sincronia: o áudio novo em t é o áudio do entregue em t + n/30 (mesma sincronia aprovada)
    a_novo = pcm(ff, saida, 4.0, 4.0, sr=16000)
    a_ent = pcm(ff, entregue, 4.0 + n / FPS - 0.1, 4.2, sr=16000)
    c = np.correlate(a_ent, a_novo, "valid")
    lag = (int(np.argmax(c)) - 1600) / 16000
    if abs(lag) > 0.002:
        sys.exit(f"ERRO: áudio fora de sincronia com o entregue ({lag * 1000:+.0f} ms)")
    d, err = tc.info(ff, saida)
    if "1080x1920" not in err or "h264" not in err or not re.search(r"(29\.9\d|30) fps", err) \
            or "48000 Hz" not in err:
        sys.exit(f"ERRO: formato inesperado em {saida}")
    import fea_revisar as fr
    e_ini, a_ini, info_ini = fr.checar_inicio(ff, saida, transcrever=False)
    for x in e_ini:
        print(f"  ERRO     {x}")
    for x in a_ini:
        print(f"  ATENÇÃO  {x}")
    print(f"OK: {os.path.basename(saida)} | início entregue {r0 / FPS:.3f} s, novo {s1:.3f} s do bruto "
          f"({n / FPS:.2f} s a menos) | recodificado {k} quadros, cópia {nc - kd} + CTA {len(q_cta)} | "
          f"conteúdo {dur:.2f} s, total {d:.2f} s | voz em {info_ini['voz']:.2f} s", flush=True)
    if e_ini:
        sys.exit(1)


if __name__ == "__main__":
    main()
