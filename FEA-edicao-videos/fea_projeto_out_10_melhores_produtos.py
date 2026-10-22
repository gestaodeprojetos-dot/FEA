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


def video(n, bruto, titulo, faixa, prods, casos, **kw):
    nome = titulo.replace("?", "").replace(":", " -")
    V.append(dict(entrada=f"{T}/b3/{bruto}.MOV", transcricao=f"{T}/tr/{bruto}.json",
                  saida=f"{T}/out_mp/{n}- {nome}.mp4", titulo=titulo, titulo_origem="inventado",
                  faixas=[faixa], pausa_max=999, cartela=True, correcoes=COMUNS + EXTRAS,
                  produtos=produtos(prods, faixa[1]), casos=casos, **kw))


video(1, "IMG_7934", "Os 3 melhores produtos para os lábios", [3.5, 51.0],
      [(11.3, "neuramis_deep"), (12.4, "revanesse_kiss"), (15.0, "restylane_refyne"),
       (24.3, "belotero_intense"), (29.2, "restylane_kiss"), (31.4, "eptq_s100")],
      [[36.0, 42.5, f"{C}/IMG_0719.MOV", 0.3]])
video(2, "IMG_7935", "Os 3 melhores produtos para olheiras", [0.0, 66.8],
      [(19.7, "yvoire_contour"), (20.9, "perfectha_subskin"), (22.3, "juvederm_voluma"), (24.6, "restylane_lyft")],
      [[33.6, 39.6, f"{C}/IMG_2661.MOV", 24.0], [50.4, 56.2, f"{C}/IMG_2661.MOV", 12.0]])
video(3, "IMG_7936", "Os 3 melhores produtos para a linha de marionete", [0.0, 56.2],
      [(11.1, "neauvia_stimulate"), (22.8, "biogelis_volume"), (23.9, "singderm")],
      [[27.0, 33.0, f"{C}/IMG_1420.MOV", 0.5], [38.0, 44.0, f"{C}/IMG_2612.MOV", 14.0]])
video(4, "IMG_7937", "Os 3 melhores produtos para a mandíbula", [0.8, 50.2],
      [(9.9, "biogelis"), (16.2, "yvoire_contour"), (20.2, "perfectha_subskin"),
       (25.9, "neauvia_intense"), (27.8, "singderm")],
      [[30.5, 36.0, f"{C}/IMG_7582.MOV", 9.0], [38.5, 44.0, f"{C}/IMG_7582.MOV", 39.0]])
video(5, "IMG_7938", "Os 3 melhores produtos para o mento", [0.8, 63.6],
      [(20.5, "restylane_shape"), (27.3, "biogelis"), (31.8, "yvoire_contour"),
       (37.3, "perfectha_subskin"), (39.6, "neauvia_intense")],
      [[9.0, 15.5, f"{C}/IMG_1420.MOV", 64.0], [47.0, 53.0, f"{C}/IMG_1420.MOV", 72.0]])
video(6, "IMG_7941", "Os 3 melhores produtos para o bigode chinês", [0.6, 60.0],
      [(23.7, "neauvia_stimulate"), (25.9, "biogelis_volume"), (27.5, "neuramis_volume"),
       (42.7, "restylane_defyne"), (44.2, "singderm")],
      [[7.0, 13.5, f"{C}/IMG_1420.MOV", 15.0], [47.0, 53.0, f"{C}/IMG_1420.MOV", 21.0]])
video(7, "IMG_7942", "Os 3 melhores produtos para as têmporas", [0.0, 88.6],
      [(38.5, "neuramis_deep"), (40.0, "neuramis_volume"), (42.3, "restylane_refyne"),
       (44.9, "restylane_volyme"), (48.5, "eptq_s100"), (50.1, "eptq_s300"),
       (69.2, "belotero_intense"), (70.5, "belotero_volume"), (72.7, "biogelis_global")],
      [[8.0, 14.0, f"{C}/IMG_1238.MOV", 6.0], [22.0, 28.0, f"{C}/IMG_1238.MOV", 47.0]])

CTA = glob.glob(f"{T}/cta/*COMENTE*.mp4")
json.dump({"ffmpeg": FF, "fontsdir": f"{T}/fonts", "whoosh": f"{AQUI}/FEA-som-arrasto-titulo.wav",
           "cartela": CTA[0], "musica": f"{T}/audio/musica_piano.wav", "musica_vol": 0.07,
           "sfx_pop": f"{T}/audio/pop.mp3", "sfx_split": f"{T}/audio/whoosh_split.mp3",
           "videos": V}, sys.stdout, ensure_ascii=False, indent=1)
