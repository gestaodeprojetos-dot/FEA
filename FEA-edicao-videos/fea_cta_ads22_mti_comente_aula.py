#!/usr/bin/env python3
"""FEA: "Ads 22 - MTI" + transição + CTA "Comente AULA" da Masterclass em Intercorrências.

v2 (Keila, 12/11/2026): a v1 cortava no quadro 708 e tirava o anúncio inteiro da masterclass. Pedido literal:
"no vídeo precisa pegar falando que o doutor vai fazer uma masterclass gratuita só para quem estiver ao vivo
e que ele vai ensinar XYZ, precisa estar tudo isso. Você só vai cortar na hora que ele fala saiba mais".
Regra: sai só o pedido de clique (inscrever, tocar em saiba mais) e a tela final; o anúncio do evento fica.

Origem: "Ads 22 - MTI" (Drive 1bPkJeUQ3nzJPI4x2Fk23GuDiMb6iotgW, pasta "1. CAPTAÇÃO"
1m1ShWBbR_ZzuohshnPh6vDUX6FUsF9UG; HEVC 1080x1920 30 fps, AAC 44,1 kHz, 48,23 s, legenda queimada).

Trechos mantidos (quadros a 30 fps, fim exclusivo; medidos no áudio em janelas de 20 ms e na faixa da
legenda queimada, para nenhum quadro mostrar a legenda do pedido de clique):
  A. 0 a 938 (0 a 31,267 s): do começo até "...as atualizações em intercorrências na harmonização facial,"
     (voz acaba em ~31,05 s; vale de silêncio 31,24 a 31,30 s; a legenda "harmonização facial" sai no
     quadro 934 e a de "você vai clicar aqui em Saiba Mais" entra no 939; o "você" começa em ~31,32 s).
  B. 1109 a 1208 (36,967 a 40,267 s): "Então é somente para quem estiver ao vivo com vagas limitadas."
     (a legenda "então é somente..." entra no quadro 1109, voz do "Então" em ~37,06 s; "limitadas" acaba
     em ~40,03 s; a legenda "se inscreve gratuitamente aqui nesse botão" entra no quadro 1208 e a voz do
     "Se" em ~40,30 s).
  Sai: "você vai clicar aqui em Saiba Mais, vai se inscrever para participar dessa aula que não vai ter
  replay." (31,27 a 36,97 s), "Se inscreve gratuitamente aqui nesse botão que eu te vejo lá." e a tela
  final azul "Toque em Saiba Mais" (40,27 s ao fim).
Emenda A|B: corte seco de imagem (Dr. em quadro pequeno sobre a foto parada), áudio com fade de 20 ms
nos dois lados para não estalar.

Emenda com o card: mesma lógica do fea_render_com_cta.py (plano_emenda e filtro_emenda): crossfade de
0,5 s em vídeo e áudio, começando 0,10 s depois do fim da voz; como o respiro até o corte é curto, o
último quadro (sem legenda) é estendido (tpad clone). Fim da voz: o "s" de "limitadas" acaba em
~40,05 s (energia acima de 4 kHz cai de +19 para -4 dB); o detector automático contava o ruído de
sala até 40,22 s, por isso --fim-voz 40.05 por padrão. Saída H.264 CRF 18 High, AAC 192k 48 kHz estéreo,
1080x1920, 30 fps (o original é HEVC). Grava SAIDA.emenda.json.

Uso:
    python3 fea_cta_ads22_mti_comente_aula.py "Ads 22 - MTI" FEA-CTA-digitando-comente-aula-MIC.mp4 SAIDA.mp4
        [--trechos 0-938,1109-1208] [--transicao 0.5] [--fim-voz S] [--ffmpeg ffmpeg]
"""
import argparse, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fea_render_com_cta as rc  # noqa: E402

FADE_JUNTA = 0.02


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("cta")
    ap.add_argument("saida")
    ap.add_argument("--trechos", default="0-938,1109-1208", help="quadros mantidos, fim exclusivo (30 fps)")
    ap.add_argument("--transicao", type=float, default=rc.TRANSICAO_PADRAO)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--fim-voz", type=float, default=40.05, help="fim da última palavra (s do original), medido no espectro; o detector "
                    "automático conta o ruído de sala até 40,22 s como voz; 0 = automático")
    a = ap.parse_args()
    if a.fim_voz > 0:
        rc.fim_da_voz = lambda *_, **__: a.fim_voz

    quadros = [tuple(int(x) for x in t.split("-")) for t in a.trechos.split(",")]
    manter = [[q0 / 30, q1 / 30] for q0, q1 in quadros]
    info = rc.plano_emenda(a.ffmpeg, {"entrada": a.entrada}, manter, a.cta, a.transicao)
    info["trechos_quadros"] = quadros
    info["trechos_s"] = [[round(x, 3), round(y, 3)] for x, y in manter]
    n = len(quadros)
    partes, rot = [], ""
    for i, ((q0, q1), (t0, t1)) in enumerate(zip(quadros, manter)):
        fa = []
        if i > 0:
            fa.append(f"afade=t=in:d={FADE_JUNTA}")
        if i < n - 1:
            fa.append(f"afade=t=out:st={t1 - t0 - FADE_JUNTA:.4f}:d={FADE_JUNTA}")
        partes.append(f"[0:v]trim=start_frame={q0}:end_frame={q1},setpts=PTS-STARTPTS[v{i}];"
                      f"[0:a]atrim={t0:.6f}:{t1:.6f},asetpts=PTS-STARTPTS,aresample=48000"
                      + ("," + ",".join(fa) if fa else "") + f"[a{i}];")
        rot += f"[v{i}][a{i}]"
    filtro = "".join(partes) + f"{rot}concat=n={n}:v=1:a=1[vo][ac];" + rc.filtro_emenda(info, 1080, 1920)
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
