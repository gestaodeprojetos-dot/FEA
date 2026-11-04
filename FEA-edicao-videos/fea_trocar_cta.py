#!/usr/bin/env python3
"""FEA: troca o CTA de um vídeo já entregue sem mexer no conteúdo aprovado.

Recorta o conteúdo do vídeo entregue por stream copy (sem recompressão: os quadros são os
mesmos bytes que a Keila aprovou) e cola o CTA novo no final, também por stream copy, do
mesmo jeito que o fea_render_com_cta.py faz depois de renderizar.

Por que existe (03/11/2026, lote 1-4 de novembro): a re-renderização pelos projetos depende
do JSON da transcrição, que fica só na máquina temporária da edição. Quando a edição original
teve ajustes à mão nesse JSON (palavra trocada, tempo corrigido), a retranscrição do Whisper
não os traz de volta e a legenda nova sai diferente da aprovada. Recortando o entregue, a
legenda, os cortes, os zooms e os silenciados ficam exatamente como foram aprovados.

Conferências (o script para com ERRO se qualquer uma falhar):
1. O final do vídeo entregue é, quadro a quadro, o CTA antigo (framemd5 do vídeo igual).
2. No vídeo novo, os quadros do conteúdo são idênticos aos do entregue (framemd5).
3. No vídeo novo, os quadros finais são idênticos aos do CTA novo (framemd5).
4. Duração total até 180 s; H.264 1080x1920 30 fps, AAC 48 kHz.
   Com --limite-conteudo, os 180 s valem só para o conteúdo: o total acima de 180 s sai como
   ATENÇÃO e o vídeo é gerado mesmo assim (pedido da Keila em 04/11/2026, CTA criativo Ads 12 MTB
   de 25 s nas pastas 2 em diante de novembro).

5. Quando o SPS/PPS (parâmetros do H.264) do CTA difere do vídeo entregue, o ffmpeg grava o do
   CTA dentro do fluxo, no começo do CTA (como já acontecia no fea_render_com_cta.py); o script
   confere que esses bytes estão na saída.

Uso:
    python3 fea_trocar_cta.py FFMPEG ENTREGUE.mp4 CTA_ANTIGO.mp4 CTA_NOVO.mp4 SAIDA.mp4 [--limite-conteudo]
"""
import os, re, subprocess, sys, tempfile

LIMITE_TOTAL_S = 180


def md5s_video(ff, arq):
    r = subprocess.run([ff, "-nostdin", "-v", "error", "-i", arq, "-map", "0:v:0", "-f", "framemd5", "-"],
                       capture_output=True, text=True, check=True).stdout
    return [ln.split(",")[-1].strip() for ln in r.splitlines() if ln and not ln.startswith("#")]


def info(ff, arq):
    err = subprocess.run([ff, "-hide_banner", "-i", arq], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return float(h) * 3600 + float(m) * 60 + float(s), err


def avcc(arq):
    """Bytes do avcC (SPS/PPS) do primeiro vídeo do MP4."""
    with open(arq, "rb") as f:
        b = f.read(64 * 1024 * 1024) if os.path.getsize(arq) > 64 * 1024 * 1024 else f.read()
    i = b.find(b"avcC")
    if i < 0:
        with open(arq, "rb") as f:
            b = f.read()
        i = b.find(b"avcC")
    n = int.from_bytes(b[i - 4:i], "big")
    return b[i + 4:i - 4 + n]


def main(ff, entregue, cta_antigo, cta_novo, saida, limite_conteudo=False):
    q_ent, q_ant, q_novo = md5s_video(ff, entregue), md5s_video(ff, cta_antigo), md5s_video(ff, cta_novo)
    n = len(q_ent) - len(q_ant)
    if n <= 0 or q_ent[n:] != q_ant:
        sys.exit(f"ERRO: o final de {os.path.basename(entregue)} não é o CTA antigo quadro a quadro")
    t = n / 30.0
    pasta = os.path.dirname(os.path.abspath(saida))
    with tempfile.TemporaryDirectory(dir=pasta) as tmp:
        conteudo = os.path.join(tmp, "conteudo.mp4")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-i", entregue, "-map", "0:v:0", "-map", "0:a:0",
                        "-c", "copy", "-frames:v", str(n), "-t", f"{t:.6f}", conteudo], check=True)
        lista = os.path.join(tmp, "lista.txt")
        with open(lista, "w") as f:
            f.write(f"file '{conteudo}'\nfile '{os.path.abspath(cta_novo)}'\n")
        subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista,
                        "-c", "copy", "-movflags", "+faststart", saida], check=True)
    q_sai = md5s_video(ff, saida)
    if q_sai[:n] != q_ent[:n]:
        sys.exit(f"ERRO: conteúdo de {os.path.basename(saida)} difere do entregue")
    if q_sai[n:] != q_novo:
        sys.exit(f"ERRO: CTA de {os.path.basename(saida)} difere do CTA novo "
                 f"({len(q_sai) - n} quadros, esperado {len(q_novo)})")
    a_ent, a_cta = avcc(entregue), avcc(cta_novo)
    if a_ent != a_cta:
        # avcC: versão, perfil, compat., nível, tam. NAL, nº SPS, tamanho (2 bytes), SPS
        sps = a_cta[8:8 + int.from_bytes(a_cta[6:8], "big")]
        with open(saida, "rb") as f:
            if sps not in f.read():
                sys.exit(f"ERRO: SPS do CTA novo não está dentro do fluxo de {os.path.basename(saida)}")
    d, err = info(ff, saida)
    # 29,99 fps: o áudio do conteúdo passa uns ms do último quadro e a emenda ganha meio quadro de
    # folga, igual ao que o fea_render_com_cta.py já gerava no vídeo entregue (não é quadro perdido)
    if "1080x1920" not in err or "h264" not in err or not re.search(r"(29\.9\d|30) fps", err) \
            or "48000 Hz" not in err:
        sys.exit(f"ERRO: formato inesperado em {saida}")
    marca = "OK" if d <= LIMITE_TOTAL_S else ("ATENÇÃO, ACIMA DE 3 MIN COM O CTA" if limite_conteudo
                                                else "ACIMA DE 3 MIN")
    print(f"{marca}: {os.path.basename(saida)} | conteúdo {n} quadros ({t:.2f} s, idêntico ao entregue) "
          f"+ CTA {len(q_novo)} quadros | total {d:.2f} s", flush=True)
    if limite_conteudo and t > LIMITE_TOTAL_S:
        sys.exit("ERRO: o conteúdo passa de 3 min")
    if not limite_conteudo and d > LIMITE_TOTAL_S:
        sys.exit("ERRO: passa de 3 min com o CTA")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--limite-conteudo"]
    if len(args) != 5:
        sys.exit(__doc__)
    main(*args, limite_conteudo="--limite-conteudo" in sys.argv)
