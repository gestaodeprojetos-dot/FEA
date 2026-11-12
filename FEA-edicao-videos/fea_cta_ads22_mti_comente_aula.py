#!/usr/bin/env python3
"""FEA: "Ads 22 - MTI" + transição + CTA "Comente AULA" da Masterclass em Intercorrências (12/11/2026).

Pedido da Keila: cortar o trecho em que o Dr. manda clicar em "saiba mais", fazer a transição
e colar o card de 5 s FEA-CTA-digitando-comente-aula-MIC.mp4.

Origem: "Ads 22 - MTI" (Drive 1bPkJeUQ3nzJPI4x2Fk23GuDiMb6iotgW, pasta "1. CAPTAÇÃO"
1m1ShWBbR_ZzuohshnPh6vDUX6FUsF9UG; HEVC 1080x1920 30 fps, AAC 44,1 kHz, 48,23 s, legenda queimada).

Corte (medido no áudio em janelas de 10 ms e nos quadros da legenda queimada):
  - última frase mantida: "Qual seria a progressão de antibióticos?" (o "s" final termina em ~23,35 s);
  - sai a partir de "Se você quiser participar de uma Masterclass gratuita com aula onde eu vou trazer
    as atualizações em intercorrências na harmonização facial, você vai clicar aqui em Saiba Mais, vai
    se inscrever para participar dessa aula que não vai ter replay. Então é somente para quem estiver
    ao vivo com vagas limitadas. Se inscreve gratuitamente aqui nesse botão que eu te vejo lá."
    (fricativa do "Se" em 23,64 s) e a tela final azul "MASTERCLASS EM INTERCORRÊNCIAS / Toque em
    Saiba Mais" (~43,0 s ao fim);
  - o conteúdo vai até o quadro 708 (23,600 s), no respiro: a legenda "antibióticos" sai da tela no
    quadro 699 e a seguinte ("se você quiser participar de") só entra no 710.

Fim da voz: o "s" final de "antibióticos" acaba em ~23,35 s (energia acima de 4 kHz cai de 100 para
80 dB); de 23,36 a 23,58 s há só respiração, que o fim_da_voz automático (limiar de volume) contava
como fala (dava 23,59 s e 0,6 s de quadro congelado). Por isso --fim-voz 23.35 por padrão.

Emenda: mesma lógica do fea_render_com_cta.py (plano_emenda e filtro_emenda): crossfade de 0,5 s em
vídeo e áudio, começando 0,10 s depois do fim da voz; como o respiro até o corte é curto, o último
quadro é estendido (tpad clone) para a transição não engolir a última palavra.
Saída H.264 CRF 18 High, AAC 192k 48 kHz estéreo, 1080x1920, 30 fps (o original é HEVC: é preciso
recodificar; legenda e layout do original ficam como estão). Grava SAIDA.emenda.json.

Uso:
    python3 fea_cta_ads22_mti_comente_aula.py "Ads 22 - MTI" FEA-CTA-digitando-comente-aula-MIC.mp4 SAIDA.mp4
        [--quadro-corte 708] [--transicao 0.5] [--ffmpeg ffmpeg]
"""
import argparse, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fea_render_com_cta as rc  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("cta")
    ap.add_argument("saida")
    ap.add_argument("--quadro-corte", type=int, default=708, help="1º quadro que sai (30 fps)")
    ap.add_argument("--transicao", type=float, default=rc.TRANSICAO_PADRAO)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--fim-voz", type=float, default=23.35,
                    help="fim da última palavra (s do original), medido no espectro; o detector automático "
                         "conta a respiração de 23,36 a 23,58 s como voz")
    a = ap.parse_args()
    if a.fim_voz > 0:
        rc.fim_da_voz = lambda *_, **__: a.fim_voz

    fim = a.quadro_corte / 30
    info = rc.plano_emenda(a.ffmpeg, {"entrada": a.entrada}, [[0.0, fim]], a.cta, a.transicao)
    filtro = (f"[0:v]trim=end_frame={a.quadro_corte},setpts=PTS-STARTPTS[vo];"
              f"[0:a]atrim=0:{fim:.6f},asetpts=PTS-STARTPTS,aresample=48000[ac];"
              + rc.filtro_emenda(info, 1080, 1920))
    subprocess.run([a.ffmpeg, "-v", "error", "-y", "-i", a.entrada, "-i", a.cta, "-filter_complex", filtro,
                    "-map", "[vx]", "-map", "[ax]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", a.saida], check=True)
    rc.conferir(a.ffmpeg, a.saida, info)
    json.dump(info, open(a.saida.rsplit(".", 1)[0] + ".emenda.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(info, indent=1, ensure_ascii=False))
    print(f"duração final: {rc.duracao(a.ffmpeg, a.saida):.3f} s")


if __name__ == "__main__":
    main()
