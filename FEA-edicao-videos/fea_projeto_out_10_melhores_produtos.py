#!/usr/bin/env python3
"""Gera o projeto.json do lote "Melhores produtos" (pasta de brutos 1Ix_QI3i_LHsqBwIhriMupqLTLCDEChti).

Pedido da Keila (22/10/2026): mesmo padrão do "17- Amanhã começa a Black Friday Vitalícia"
(título em caixas com som de arrasto, legenda, CTA da Black no fim), mais:
  - foto de cada produto citado, com efeito sonoro de "pop";
  - trilha de fundo baixa;
  - tela dividida com caso clínico (da pasta 00 - Brutos) quando o Dr. explica a ação do
    produto: caso em cima, Dr. embaixo, faixa esfumaçada no meio (modelo do Reel DdGmQEspUfZ),
    com whoosh na entrada.
Sem corte de pausa (reação inteira, pedido de 19/10).

Uso: python3 fea_projeto_out_10_melhores_produtos.py PASTA_DE_TRABALHO > projeto.json
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_correcoes_marcas import COMUNS  # noqa: E402  (mesmas correções de marca)

T = sys.argv[1]
FF = open(f"{T}/env.sh").read().split("=", 1)[1].strip()
AQUI = os.path.dirname(os.path.abspath(__file__))
C = f"{T}/casos"   # brutos de caso clínico baixados da 00 - Brutos


def foto(nome):
    achou = sorted(glob.glob(f"{T}/produtos/{nome}.*"))
    if not achou:
        print(f"AVISO: sem foto de {nome}", file=sys.stderr)
    return achou[0] if achou else None


def produtos(lista, fim):
    out = []
    for i, (t, nome) in enumerate(lista):
        prox = lista[i + 1][0] if i + 1 < len(lista) else fim
        f = foto(nome)
        if f:
            out.append([t, f, round(max(1.2, min(2.5, prox - t - 0.1)), 2)])
    return out


EXTRAS = [
    [r"\bTandel? ?(está|delta)\b", "tan delta"], [r"\bTandelta\b", "tan delta"],
    [r"\bHestlani Kiss\b", "Restylane Kysse"], [r"\bRechilane\b", "Restylane"], [r"\bVolime\b", "Volyme"],
    [r"\bEpetique\b", "e.p.t.q."], [r"\bsolo infector\b", "swelling factor"], [r"\bTirtrof\b", "tear trough"],
    [r"\bPerfecta\b", "Perfectha"], [r"\b[NnN][uú]via\b", "Neauvia"], [r"\bDoutor Piton\b", "Doutor Pithon"],
    [r"\bgelinho\b", "G'"], [r"\bbelotero intenso\b", "Belotero Intense"], [r"\bbelotero volume\b", "Belotero Volume"],
    [r"\bbiogelis global\b", "Biogelis Global"], [r"\bRestylane Shape\b", "Restylane Shaype"],
]

V = []

# banco de B-roll de stock (Pexels, licença livre, sem IA), baixado em PASTA/stock
K = f"{T}/stock"
OLHO1 = f"{K}/olhos_close-olho-olheira_pexels-7297802.mp4"
OLHO2 = f"{K}/olhos_close-olho-pele-madura_pexels-7299471.mp4"
OLHO_ESP = f"{K}/olhos_espelho-olheira_pexels-6654154.mp4"
LAB1 = f"{K}/labios_sorriso-batom-rosa_pexels-3762905.mp4"
LAB2 = f"{K}/labios_dedo-tocando-labio_pexels-9698152.mp4"
LAB3 = f"{K}/labios_aplicando-hidratante-labial_pexels-7346519.mp4"
MAND1 = f"{K}/mandibula_mento_perfil-mandibula_pexels-7059130.mp4"
MAND2 = f"{K}/mandibula_mento_perfil-queixo-olhando-cima_pexels-5366721.mp4"
MAND3 = f"{K}/mandibula_mento_close-queixo-terco-inferior_pexels-13770935.mp4"
MAND4 = f"{K}/mandibula_mento_maos-contorno-mandibula_pexels-9465411.mp4"
TEMP1 = f"{K}/temporas_face_mao-tocando-temporas-perfil_pexels-6961757.mp4"
TEMP2 = f"{K}/temporas_face_tres-quartos-deitada_pexels-10273120.mp4"
TEMP3 = f"{K}/temporas_face_mao-tocando-rosto_pexels-8955756.mp4"
TEMP4 = f"{K}/temporas_face_mao-rosto-espelho_pexels-6443768.mp4"
SULCO1 = f"{K}/sulco_bigode_terco-inferior-sulco-nasolabial_pexels-3761533.mp4"
SULCO2 = f"{K}/sulco_bigode_sorriso-sulco_pexels-8724246.mp4"
SULCO3 = f"{K}/sulco_bigode_sorriso-terco-inferior_pexels-8724459.mp4"
P3D = f"{K}/pele_3d_proteinas-moleculas-vertical_pexels-25935022_1080.mp4"   # ilustração de artista (DeepMind)
HA1 = f"{K}/acido_hialuronico_gota-serum-palma-vertical_pexels-8131887.mp4"
HA2 = f"{K}/acido_hialuronico_gel-textura-espalhando_pexels-10098025.mp4"
CLIN1 = f"{K}/clinica_marcacao-e-injecao-facial-luvas_pexels-30365546.mp4"
CLIN2 = f"{K}/clinica_aplicacao-labial-profissional_pexels-7423547.mp4"
CLIN3 = f"{K}/clinica_luvas-preparando-seringa_pexels-5883925.mp4"
ENV1 = f"{K}/envelhecimento_idosa-maos-no-rosto_pexels-10251377.mp4"


def video(n, bruto, titulo, faixa, prods, casos, musica, **kw):
    nome = titulo.replace("?", "").replace(":", " -")
    V.append(dict(entrada=f"{T}/b3/{bruto}.MOV", transcricao=f"{T}/tr/{bruto}.json",
                  saida=f"{T}/out_mp/{n}- {nome}.mp4", titulo=titulo, titulo_origem="inventado",
                  faixas=[faixa], pausa_max=999, cartela=True, correcoes=COMUNS + EXTRAS,
                  produtos=produtos(prods, faixa[1]), casos=casos, musica=f"{T}/musicas/{musica}.wav", **kw))


# casos: [ini, fim, clipe, início no clipe, "split" (caso em cima, Dr. embaixo) ou "cheia" (tela cheia)]
# Keila (22/10): vídeo rico de inserts, um a cada poucos segundos, desde logo depois do título.
video(1, "IMG_7934", "Os 3 melhores produtos para os lábios", [3.5, 51.0],
      [(11.3, "neuramis_deep"), (12.4, "revanesse_kiss"), (15.0, "restylane_refyne"),
       (24.3, "belotero_intense"), (29.2, "restylane_kiss"), (31.4, "eptq_s100")],
      [[7.6, 11.0, HA2, 1.0, "split"],
       [16.5, 20.5, LAB2, 1.0, "cheia"],
       [20.6, 24.1, CLIN2, 2.0, "split"],
       [26.9, 29.1, LAB3, 2.0, "cheia"],
       [33.9, 36.0, LAB1, 3.0, "cheia"],
       [36.0, 42.5, f"{C}/IMG_0719.MOV", 0.3, "split"],
       [42.6, 46.0, HA2, 4.0, "split"],
       [46.2, 49.5, LAB2, 5.0, "cheia"]], "m01")
video(2, "IMG_7935", "Os 3 melhores produtos para olheiras", [0.0, 66.8],
      [(19.7, "yvoire_contour"), (20.9, "perfectha_subskin"), (22.3, "juvederm_voluma"), (24.6, "restylane_lyft")],
      [[4.1, 8.0, OLHO_ESP, 1.0, "cheia"],
       [8.0, 12.0, HA1, 2.0, "split"],
       [12.2, 16.0, OLHO1, 1.0, "cheia"],
       [16.0, 19.5, P3D, 2.0, "split"],
       [27.2, 31.8, OLHO2, 1.0, "cheia"],
       [33.6, 39.6, f"{C}/IMG_2661.MOV", 24.0, "split"],
       [39.8, 44.5, CLIN3, 8.0, "split"],
       [45.0, 50.2, OLHO1, 3.0, "cheia"],
       [50.4, 56.2, f"{C}/IMG_2661.MOV", 12.0, "split"],
       [56.3, 60.8, HA1, 8.0, "split"],
       [61.0, 65.5, OLHO_ESP, 2.0, "cheia"]], "m02")
video(3, "IMG_7936", "Os 3 melhores produtos para a linha de marionete", [0.0, 56.2],
      [(11.1, "neauvia_stimulate"), (22.8, "biogelis_volume"), (23.9, "singderm")],
      [[4.1, 7.4, SULCO3, 2.0, "cheia"],
       [7.4, 11.0, ENV1, 3.0, "split"],
       [13.7, 20.8, P3D, 5.0, "split"],
       [27.0, 33.0, f"{C}/IMG_1420.MOV", 0.5, "split"],
       [33.2, 37.6, HA2, 2.0, "cheia"],
       [38.0, 44.0, f"{C}/IMG_2612.MOV", 14.0, "split"],
       [44.2, 48.4, SULCO1, 2.0, "cheia"],
       [48.6, 53.0, CLIN3, 6.0, "split"],
       [53.0, 55.8, SULCO2, 3.0, "cheia"]], "m03")
video(4, "IMG_7937", "Os 3 melhores produtos para a mandíbula", [0.8, 50.2],
      [(9.9, "biogelis"), (16.2, "yvoire_contour"), (20.2, "perfectha_subskin"),
       (25.9, "neauvia_intense"), (27.8, "singderm")],
      [[4.9, 9.8, MAND1, 1.0, "cheia"],
       [12.4, 16.0, MAND4, 3.0, "split"],
       [22.8, 25.8, MAND2, 2.0, "cheia"],
       [30.5, 36.0, f"{C}/IMG_7582.MOV", 9.0, "split"],
       [36.0, 38.4, MAND3, 2.0, "cheia"],
       [38.5, 44.0, f"{C}/IMG_7582.MOV", 39.0, "split"],
       [44.2, 49.0, MAND1, 5.0, "cheia"]], "m04")
video(5, "IMG_7938", "Os 3 melhores produtos para o mento", [0.8, 63.6],
      [(20.5, "restylane_shape"), (27.3, "biogelis"), (31.8, "yvoire_contour"),
       (37.3, "perfectha_subskin"), (39.6, "neauvia_intense")],
      [[4.9, 8.6, MAND3, 1.0, "cheia"],
       [9.0, 15.5, f"{C}/IMG_1420.MOV", 64.0, "split"],
       [15.6, 20.4, HA2, 3.0, "split"],
       [23.0, 27.2, MAND2, 1.0, "cheia"],
       [33.0, 37.2, CLIN1, 4.0, "split"],
       [42.1, 46.9, MAND3, 5.0, "cheia"],
       [47.0, 53.0, f"{C}/IMG_1420.MOV", 72.0, "split"],
       [53.2, 58.0, P3D, 8.0, "split"],
       [58.3, 63.2, MAND1, 3.0, "cheia"]], "m05")
video(6, "IMG_7941", "Os 3 melhores produtos para o bigode chinês", [0.6, 60.0],
      [(23.7, "neauvia_stimulate"), (25.9, "biogelis_volume"), (27.5, "neuramis_volume"),
       (42.7, "restylane_defyne"), (44.2, "singderm")],
      [[4.7, 7.0, SULCO2, 1.0, "cheia"],
       [7.0, 13.5, f"{C}/IMG_1420.MOV", 15.0, "split"],
       [13.6, 17.0, SULCO1, 1.0, "cheia"],
       [17.2, 23.5, HA2, 1.0, "split"],
       [30.0, 35.0, SULCO3, 5.0, "cheia"],
       [35.2, 42.5, CLIN3, 3.0, "split"],
       [47.0, 53.0, f"{C}/IMG_1420.MOV", 21.0, "split"],
       [53.2, 59.6, SULCO2, 6.0, "cheia"]], "m06")
video(7, "IMG_7942", "Os 3 melhores produtos para as têmporas", [0.0, 88.6],
      [(38.5, "neuramis_deep"), (40.0, "neuramis_volume"), (42.3, "restylane_refyne"),
       (44.9, "restylane_volyme"), (48.5, "eptq_s100"), (50.1, "eptq_s300"),
       (69.2, "belotero_intense"), (70.5, "belotero_volume"), (72.7, "biogelis_global")],
      [[4.1, 6.3, TEMP1, 1.0, "cheia"],
       [8.0, 14.0, f"{C}/IMG_1238.MOV", 6.0, "split"],
       [14.2, 21.8, TEMP2, 2.0, "split"],
       [22.0, 28.0, f"{C}/IMG_1238.MOV", 47.0, "split"],
       [28.2, 32.9, TEMP4, 2.0, "cheia"],
       [33.0, 38.3, HA2, 2.0, "split"],
       [52.8, 58.4, TEMP3, 11.0, "cheia"],
       [58.5, 62.6, HA1, 3.0, "split"],
       [62.7, 68.9, CLIN1, 1.0, "split"],
       [75.4, 80.5, TEMP1, 5.0, "cheia"],
       [80.6, 87.5, TEMP4, 6.0, "split"]], "m07")

CTA = glob.glob(f"{T}/cta/*COMENTE*.mp4")
json.dump({"ffmpeg": FF, "fontsdir": f"{T}/fonts", "whoosh": f"{AQUI}/FEA-som-arrasto-titulo.wav",
           "cartela": CTA[0], "musica_vol": 0.08,
           "sfx_pop": f"{T}/audio/pop.mp3", "sfx_split": f"{T}/audio/whoosh_split.mp3",
           "videos": V}, sys.stdout, ensure_ascii=False, indent=1)
