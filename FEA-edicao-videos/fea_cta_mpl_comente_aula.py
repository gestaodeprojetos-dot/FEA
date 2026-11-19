#!/usr/bin/env python3
"""FEA: CTA "Comente AULA" de masterclass (criativo sem o pedido de clique + transição + card).

Mesmo padrão do CTA MTI aprovado pela Keila em 12/11/2026 (`Ads 22 - MTI - CTA Comente AULA.mp4`,
39,50 s = Ads 22 cortado + xfade de 0,5 s + card `FEA-CTA-digitando-comente-aula-MIC.mp4` de 5 s),
generalizado com parâmetros de criativo, trechos, logo e cor. Primeiro uso: Masterclass em
Preenchimento Labial (MPL), pedido da Keila de 18/11/2026.

Três passos (cada um pode rodar sozinho):

1. logo para fundo preto (`logo-escuro`): a logo oficial da MPL (`5. LOGO/Logo-MPL.png`, Drive
   1rS1HuohV94seKgewliHyTTI9Qelc4Aj7) tem a linha "MASTERCLASS EM" em azul-petróleo #00323C, que
   some no preto. Só essa linha vira negativo (azul-petróleo -> branco, branco -> azul-petróleo);
   o vermelho #FF1A38 e o desenho ficam intactos. Sem redesenho, sem IA (linha vermelha FEA).
       python3 fea_cta_mpl_comente_aula.py logo-escuro Logo-MPL.png FEA-MPL-logo-fundo-escuro.png
2. card de 5 s (`card`): chama fea_cta_comente_black_digitando.py (logo com impacto + "Comente
   AULA" digitado com som de teclado, fundo preto), "AULA" na cor de destaque.
       python3 fea_cta_mpl_comente_aula.py card FEA-CTA-digitando-comente-aula-MPL.mp4 \
           --logo FEA-cta-digitando/FEA-MPL-logo-fundo-escuro.png --cor-destaque FF1A38
3. CTA final (`cta`): concatena os --trechos do criativo (segundos), estende o último quadro
   (tpad clone + silêncio) se a transição cairia antes de --fim-voz + 0,10 s, faz xfade fade e
   acrossfade de --transicao s e cola o card inteiro. H.264 High CRF 18 (preset slow), yuv420p,
   1080x1920, 30 fps, AAC 192k 48 kHz estéreo, nunca HEVC. Grava SAIDA.emenda.json.
       python3 fea_cta_mpl_comente_aula.py cta "Ads 55 - MPL.mp4" FEA-CTA-digitando-comente-aula-MPL.mp4 \
           "Ads 55 - MPL - CTA Comente AULA.mp4" --trechos 0-20.8333 --fim-voz 20.76

Criativo MPL usado (18/11/2026): `Ads 55 - MPL.mp4` (Drive 114q_NMpomSWPvzJAs2WyF7hHiirJNvUj, 25,91 s,
4. TRÁFEGO/CRIATIVOS PRONTOS/1. CAPTAÇÃO), que é o post https://www.instagram.com/p/DfnLVf-gRSv/
(correlação média de quadros 0,995, 25,913 s no post). A fala termina em "...para também ter acesso
a uma masterclass gratuito em preenchimento labial." (voz até ~20,76 s); a partir do quadro 625
(20,833 s) entra a vinheta "MASTERCLASS EM PREENCHIMENTO LABIAL / Toque em Saiba Mais" com whoosh,
que sai inteira. O Dr. não fala "toque em saiba mais" neste criativo: o pedido de clique é a vinheta.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FPS, W, H = 30, 1080, 1920
FOLGA_S = 0.10


def logo_escuro(entrada, saida, faixa_y=300):
    im = np.asarray(Image.open(entrada).convert("RGBA")).astype(np.float32)
    rgb, a = im[..., :3], im[..., 3]
    vermelho = (rgb[..., 0] > 180) & (rgb[..., 1] < 110)
    topo = np.zeros(a.shape, bool)
    topo[:faixa_y] = True
    alvo = topo & ~vermelho & (a > 0)
    petroleo = np.array([0, 50, 60], np.float32)
    # quanto o pixel é "claro" (0 = azul-petróleo, 1 = branco); inverte a mistura
    lum = rgb.mean(-1) / 255.0
    claro = np.clip((lum - petroleo.mean() / 255) / (1 - petroleo.mean() / 255), 0, 1)[..., None]
    novo = claro * petroleo + (1 - claro) * 255.0
    rgb[alvo] = novo[alvo]
    Image.fromarray(np.dstack([rgb, a]).round().astype(np.uint8), "RGBA").save(saida)
    print(f"logo para fundo escuro: {saida} ({int(alvo.sum())} px na faixa do topo)")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r.stdout


def duracao(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def cta(a):
    trechos = [tuple(map(float, t.split("-"))) for t in a.trechos.split(",")]
    d = sum(round((f - i) * FPS) for i, f in trechos) / FPS
    T = a.transicao
    ini_tr = d - T
    pad_q = 0
    if ini_tr < a.fim_voz + FOLGA_S:
        pad_q = int(np.ceil((a.fim_voz + FOLGA_S - ini_tr) * FPS - 1e-6))
    d2 = d + pad_q / FPS
    ini_tr = d2 - T
    d_card = duracao(a.card)
    fc, vs, as_ = [], [], []
    for k, (i, f) in enumerate(trechos):
        q0, q1 = round(i * FPS), round(f * FPS)
        fc.append(f"[0:v]trim=start_frame={q0}:end_frame={q1},setpts=PTS-STARTPTS,fps={FPS},"
                  f"scale={W}:{H},setsar=1,format=yuv420p[v{k}]")
        # micro-fade de 15 ms nas bordas internas e no fim do último trecho (sem estalo)
        fades = f"afade=t=in:d=0.015," if k else ""
        fc.append(f"[0:a]atrim={q0 / FPS:.6f}:{q1 / FPS:.6f},asetpts=PTS-STARTPTS,aresample=48000,"
                  f"aformat=sample_fmts=fltp:channel_layouts=stereo,{fades}"
                  f"afade=t=out:st={(q1 - q0) / FPS - 0.02:.4f}:d=0.02[a{k}]")
        vs.append(f"[v{k}]"); as_.append(f"[a{k}]")
    n = len(trechos)
    fc.append("".join(x for p in zip(vs, as_) for x in p) + f"concat=n={n}:v=1:a=1[vc][ac]")
    fc.append(f"[vc]tpad=stop_mode=clone:stop={pad_q},fps={FPS},settb=1/{FPS}[vp]")
    fc.append(f"[ac]apad=whole_dur={d2:.6f}[ap]")
    fc.append(f"[1:v]fps={FPS},scale={W}:{H},setsar=1,format=yuv420p,setpts=PTS-STARTPTS,settb=1/{FPS}[vk]")
    fc.append("[1:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[ak]")
    fc.append(f"[vp][vk]xfade=transition=fade:duration={T}:offset={ini_tr:.6f},format=yuv420p[v]")
    fc.append(f"[ap][ak]acrossfade=d={T}:c1=tri:c2=tri[a]")
    total = d2 + d_card - T
    run(["ffmpeg", "-v", "error", "-y", "-i", a.criativo, "-i", a.card, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-t", f"{total:.4f}", "-movflags", "+faststart", "-map_metadata", "-1", a.saida])
    info = {"criativo": os.path.basename(a.criativo), "trechos_s": trechos, "conteudo_s": round(d, 3),
            "fim_voz_s": a.fim_voz, "pad_quadros": pad_q, "inicio_transicao_s": round(ini_tr, 3),
            "transicao_s": T, "card": os.path.basename(a.card), "card_s": round(d_card, 3),
            "total_esperado_s": round(total, 3), "total_medido_s": round(duracao(a.saida), 3)}
    json.dump(info, open(os.path.splitext(a.saida)[0] + ".emenda.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(info, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("logo-escuro"); p.add_argument("entrada"); p.add_argument("saida")
    p.add_argument("--faixa-y", type=int, default=300)
    p = sp.add_parser("card"); p.add_argument("saida"); p.add_argument("--logo", required=True)
    p.add_argument("--texto", default="Comente AULA"); p.add_argument("--destaque", default="AULA")
    p.add_argument("--cor-destaque", default="FF1A38"); p.add_argument("--png-final")
    p = sp.add_parser("cta"); p.add_argument("criativo"); p.add_argument("card"); p.add_argument("saida")
    p.add_argument("--trechos", required=True, help="ini-fim[,ini-fim...] em segundos do criativo")
    p.add_argument("--fim-voz", type=float, required=True, help="fim da última palavra (s, no vídeo cortado)")
    p.add_argument("--transicao", type=float, default=0.5)
    a = ap.parse_args()
    if a.cmd == "logo-escuro":
        logo_escuro(a.entrada, a.saida, a.faixa_y)
    elif a.cmd == "card":
        cmd = [sys.executable, os.path.join(AQUI, "fea_cta_comente_black_digitando.py"), a.saida,
               "--texto", a.texto, "--destaque", a.destaque, "--logo", a.logo, "--cor-destaque", a.cor_destaque]
        if a.png_final:
            cmd += ["--png-final", a.png_final]
        print(run(cmd))
    else:
        cta(a)


if __name__ == "__main__":
    main()
