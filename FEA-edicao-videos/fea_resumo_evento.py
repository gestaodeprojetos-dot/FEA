#!/usr/bin/env python3
"""FEA: vídeo-resumo de evento (FEP Experience, imersões IFF/IAR/PSP, congressos), 9:16.

Junta trechos de vários vídeos e fotos do evento num vídeo curto (~45 s), com o mesmo título e a
mesma legenda dos Reels (Montserrat), áudio real das falas, trilha opcional que abaixa sozinha
quando alguém fala, e cartela final com a logo. Ideia tirada do guia "O Seu Editor de Vídeo de IA"
(06/11/2026), adaptada ao padrão FEA. Regras de conteúdo na skill fea-resumo-evento.

Uso:
    python3 fea_resumo_evento.py projeto_resumo.json [--previa]

projeto_resumo.json:
{
  "ffmpeg": "/caminho/ffmpeg",
  "fontsdir": "fonts",
  "saida": "out/FEP Experience 12 - resumo.mp4",
  "titulo": "FEP Experience 12",                 # 3 s iniciais, estilo do título dos Reels
  "clipes": [
    {"arquivo": "raw/IMG_9001.MOV", "ini": 12.4, "fim": 15.9},                     # áudio original
    {"arquivo": "raw/IMG_9002.MOV", "ini": 40.0, "fim": 46.5,
     "legendas": [[0.2, 2.8, "a anatomia muda o raciocínio clínico"], [2.9, 6.3, "..."]]},
    {"arquivo": "raw/IMG_9005.MOV", "ini": 3.0, "fim": 5.0, "audio": "mudo"},     # só a trilha
    {"arquivo": "raw/palco.MOV", "ini": 8.0, "fim": 12.0, "encaixe": "desfoque"},  # deitado, sem cortar as laterais
    {"arquivo": "fotos/turma.jpg", "dur": 2.0}                                     # foto com movimento leve
  ],
  "musica": "trilha_licenciada.mp3",            # opcional; só trilha com licença de uso comercial
  "musica_db": -16,                              # volume da trilha (abaixa mais quando há fala)
  "final": {"imagem": "logo_fea.png", "dur": 2.5, "fundo": "#5B4599", "texto": null}
}

"legendas": tempos em segundos a partir do início do trecho (não do bruto). Texto escrito a partir
da transcrição e passado pelas mesmas correções dos Reels (nunca "pra", grafias técnicas).
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402

W, H, FPS = fe.W, fe.H, 30
FOTO_EXT = (".jpg", ".jpeg", ".png", ".heic", ".webp")
ALVO_S = (30, 60)   # resumo de evento: entre 30 s e 1 min (ideal ~45 s)


def tem_audio(ff, arq):
    info = subprocess.run([ff, "-nostdin", "-i", arq], capture_output=True, text=True).stderr
    return "Audio:" in info


def duracao_clipe(c):
    return float(c["dur"]) if "dur" in c else float(c["fim"]) - float(c["ini"])


def esc(caminho):
    return caminho.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def gerar_ass(cfg, clipes, total, caminho):
    linhas = [fe.ass_header()]
    if cfg.get("titulo"):
        linhas += fe.dialogos_linhas(1, 0, fe.TITULO_DUR, "Titulo", fe.quebrar_titulo(cfg["titulo"]),
                                     r"\fad(0,250)")
    t0 = 0.0
    for c in clipes:
        d = duracao_clipe(c)
        for a, b, texto in c.get("legendas", []):
            s, e = t0 + float(a), min(t0 + float(b), t0 + d)
            s = max(s, fe.TITULO_DUR if cfg.get("titulo") else 0)   # legenda só depois do título
            if e - s < 0.3:
                continue
            txt = fe.quebrar_linhas(fe.limpar(fe.corrigir(texto, cfg.get("correcoes", ()))))
            linhas += fe.dialogos_linhas(0, s, e, "Legenda", txt)
        t0 += d
    final = cfg.get("final") or {}
    if final.get("texto"):
        linhas += fe.dialogos_linhas(1, t0, total, "Titulo", fe.quebrar_titulo(final["texto"]), r"\fad(250,0)")
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def montar(cfg, previa=False):
    ff = cfg["ffmpeg"]
    clipes = cfg["clipes"]
    final = cfg.get("final") or {}
    entradas, partes, rot = [], [], []
    for i, c in enumerate(clipes):
        d = duracao_clipe(c)
        arq = c["arquivo"]
        foto = arq.lower().endswith(FOTO_EXT)
        if foto:
            entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", arq]
            # movimento leve (aproxima 6% ao longo da foto), sem efeito chamativo
            v = (f"[{i}:v]scale={int(W * 1.06)}:{int(H * 1.06)}:force_original_aspect_ratio=increase,"
                 f"crop={W}:{H}:x='(iw-{W})/2*(1-t/{d:.3f})':y='(ih-{H})/2*(1-t/{d:.3f})'")
        else:
            entradas += ["-ss", f"{float(c['ini']):.3f}", "-t", f"{d:.3f}", "-i", arq]
            base = f"[{i}:v]setpts=PTS-STARTPTS{fe.filtro_hdr(ff, arq)}"
            if c.get("encaixe") == "desfoque":
                # vídeo deitado inteiro no centro, com o próprio vídeo desfocado preenchendo o fundo
                # (palco, plateia, slide: "recortar" cortaria as laterais)
                v = (f"{base},split=2[f{i}][b{i}];[f{i}]scale={W}:-2[fg{i}];"
                     f"[b{i}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2[bg{i}];"
                     f"[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2")
            else:
                v = f"{base},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        partes.append(v + f",fps={FPS},setsar=1,format=yuv420p,trim=duration={d:.3f}[v{i}]")
        if not foto and c.get("audio", "original") == "original" and tem_audio(ff, arq):
            vol = f",volume={c['volume_db']}dB" if c.get("volume_db") else ""
            partes.append(f"[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo{vol},"
                          f"apad,atrim=duration={d:.3f},afade=t=in:d=0.03,"
                          f"afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03[a{i}]")
        else:
            partes.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}]")
        rot.append(f"[v{i}][a{i}]")
    n = len(clipes)
    total = sum(duracao_clipe(c) for c in clipes)
    if final:
        df = float(final.get("dur", 2.5))
        fundo = final.get("fundo", "#5B4599").replace("#", "0x")
        partes.append(f"color=c={fundo}:s={W}x{H}:r={FPS}:d={df:.3f},format=yuv420p,setsar=1[fundo]")
        if final.get("imagem"):
            entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{df:.3f}", "-i", final["imagem"]]
            partes.append(f"[{len(clipes)}:v]scale={int(W * 0.6)}:-1[logo]")   # logo = entrada logo após os clipes
            partes.append("[fundo][logo]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p[vfim]")
        else:
            partes.append("[fundo]null[vfim]")
        partes.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={df:.3f}[afim]")
        rot.append("[vfim][afim]")
        n += 1
        total += df
    partes.append("".join(rot) + f"concat=n={n}:v=1:a=1[vc][ac]")

    if cfg.get("musica"):
        idx = len(clipes) + (1 if final.get("imagem") else 0)   # trilha = depois dos clipes (e da logo)
        entradas += ["-stream_loop", "-1", "-i", cfg["musica"]]
        mdb = cfg.get("musica_db", -16)
        partes.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={total:.3f},"
                      f"volume={mdb}dB,afade=t=in:d=0.5,afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[mus]")
        # a trilha abaixa sozinha quando há fala (sidechain): a fala real do evento é a protagonista
        partes.append("[ac]asplit=2[voz][chave];[mus][chave]sidechaincompress=threshold=0.015:ratio=10:"
                      "attack=15:release=450[musd];[voz][musd]amix=inputs=2:normalize=0:duration=first[aout]")
        aout = "[aout]"
    else:
        aout = "[ac]"

    saida = cfg["saida"]
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
    ass = saida.rsplit(".", 1)[0] + ".ass"
    gerar_ass(cfg, clipes, total, ass)
    partes.append(f"[vc]ass='{esc(ass)}':fontsdir='{cfg.get('fontsdir', 'fonts')}',"
                 "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[vo]")
    if previa:
        partes.append("[vo]scale=720:1280[vp]")
        mapa, cod = "[vp]", ["-c:v", "libx264", "-preset", "fast", "-crf", "26"]
        pasta, nome = os.path.split(saida)
        saida = os.path.join(pasta, "PREVIA " + nome)
    else:   # mesma entrega dos Reels: H.264 CRF 18, nunca HEVC (tela preta no computador da Keila)
        mapa, cod = "[vo]", ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high"]
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", ";".join(partes),
           "-map", mapa, "-map", aout, *cod, "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-r", str(FPS), "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    aviso = "" if ALVO_S[0] <= total <= ALVO_S[1] else f"  ATENÇÃO: fora da faixa {ALVO_S[0]}-{ALVO_S[1]} s"
    print(f"{saida}: {total:.1f}s, {n} trechos{aviso}", flush=True)
    return saida, total


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    previa = "--previa" in args
    args = [a for a in args if a != "--previa"]
    projeto = os.path.abspath(args[0])
    os.chdir(os.path.dirname(projeto))
    cfg = json.load(open(projeto, encoding="utf-8"))
    for c in cfg["clipes"]:
        if duracao_clipe(c) <= 0:
            sys.exit(f"ERRO: trecho com duração zero ou negativa: {c}")
        if re.search(r"\bpra\b|\bpro\b", " ".join(t for *_, t in c.get("legendas", []))):
            print(f"  aviso: 'pra/pro' na legenda de {c['arquivo']} será trocado por 'para'")
    montar(cfg, previa)


if __name__ == "__main__":
    main()
