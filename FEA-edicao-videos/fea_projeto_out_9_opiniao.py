#!/usr/bin/env python3
"""Gera o projeto.json do lote "opinião / mito ou verdade" (out/2026, pasta de brutos
14KGpMgRFA7nz99mqFYyqYh-mHt0CvVKZ + pasta completa 1KdavwGgzXrVDnaxG8lUiTIMxo31g4q3Y).

Já editados pela Keila (não reeditar): IMG_7828 (1- Olheiras), IMG_7834 (2- Anestesia),
IMG_7835 (3- Toxina), IMG_7836 (4- Lábios). Sem conclusão do Dr. (não editar): IMG_7831
(rinomodelação, para no "por quê?"; a versão completa é a IMG_7833) e IMG_7900 (take
interrompido da IMG_7902).

Uso: python3 fea_projeto_out_9_opiniao.py PASTA_DE_TRABALHO > projeto.json
"""
import glob
import json
import os
import sys

T = sys.argv[1]
FF = open(f"{T}/env.sh").read().split("=", 1)[1].strip()
AQUI = os.path.dirname(os.path.abspath(__file__))


def foto(nome):
    achou = sorted(glob.glob(f"{T}/produtos/{nome}.*"))
    if not achou:
        print(f"AVISO: sem foto de {nome}", file=sys.stderr)
    return achou[0] if achou else None


def produtos(lista, fim):
    """[(t, nome)] -> [[t, arquivo, duração]]: cada foto fica até a próxima (máx. 2,5 s)."""
    out = []
    for i, (t, nome) in enumerate(lista):
        prox = lista[i + 1][0] if i + 1 < len(lista) else fim
        f = foto(nome)
        if f:
            out.append([t, f, round(max(1.2, min(2.5, prox - t - 0.1)), 2)])
    return out


# correções de transcrição comuns ao lote
COMUNS = [
    [r"\bVitalice\b", "Vitalícia"], [r"\bitalícias\b", "vitalícias"],
    [r"\bSaba ?[Mm]ais\b", "Saiba Mais"], [r"\bimunização facial\b", "harmonização facial"],
    [r"\bMD-? ?[Cc]odes\b", "MD Codes"], [r"\bMDCodes\b", "MD Codes"],
    [r"\bperiostal\b", "periosteal"], [r"\bacelerônico\b", "ácido hialurônico"],
    [r"\bácido alurônico\b", "ácido hialurônico"], [r"\baluronidase\b", "hialuronidase"],
    [r"\bBiestimulador\b", "Bioestimulador"], [r"\bgelinha\b", "G'"],
    [r"\bNeurom[iy]s\b", "Neuramis"], [r"\bNeuronis Jeep\b", "Neuramis Deep"],
    [r"\bResilane\b", "Restylane"], [r"\bRestylane Refine\b", "Restylane Refyne"],
    [r"\bRefine\b", "Refyne"], [r"\bRestylane Define\b", "Restylane Defyne"],
    [r"\bEptik S100\b", "e.p.t.q. S100"], [r"\bRenova\b", "Rennova"], [r"\bDeepline\b", "Deep Line"],
    [r"\b[IE] ?voar\b", "Yvoire"], [r"\bYvoire,? [Cc]ont(ou|our)\b", "Yvoire Contour"],
    [r"\bsubskin\b", "Subskin"], [r"\bJuvederm\b", "Juvéderm"],
    [r"\bNuve Estimulate\b", "Neauvia Stimulate"], [r"\bBiogealiz\b", "Biogelis"],
    [r"\bsuco naslobial\b", "sulco nasolabial"], [r"\bbigot?inês\b", "bigode chinês"],
    [r"\breino de modulação\b", "rinomodelação"], [r"\bRino modelação\b", "Rinomodelação"],
    [r"\bProfilo\b", "Profhilo"], [r"\bperdo de tempo\b", "perda de tempo"],
    [r"\bGHKCU\b", "GHK-Cu"], [r"\bComo Vitalício\b", "Combo Vitalício"],
    [r"\blado especial\b", "lote especial"], [r"\bOver Delivery\b", "over delivery"],
    [r"\barteiras\b", "artérias"], [r"\brosteiro\b", "rosto inteiro"], [r"\bM face\b", "hemiface"],
    [r"\bFace for face\b", "Full face"], [r"\b1250\b", "1.250"],
    [r"\bparticipar, da nossa\b", "participar da nossa"], [r"\bclica aqui em cima a mais\b", "clica aqui em Saiba Mais"],
    [r"\b[Vv]italícia, está\b", "Vitalícia está"], [r"\bnaslobial\b", "nasolabial"],
    [r"\bRestylane Lift\b", "Restylane Lyft"], [r"\bbotox\b", "Botox"], [r"\bRestylane Kiss\b", "Restylane Kysse"], [r"\bYoutube\b", "YouTube"],
    [r"\bmais, de 1\.250\b", "mais de 1.250"], [r"\bnós vemos\b", "nos vemos"], [r"\bo rinomodelação\b", "a rinomodelação"],
]

V = []


def video(n, bruto, titulo, faixas, **kw):
    pasta = "b2" if bruto in ("IMG_7889", "IMG_7890", "IMG_7902") else "b"
    nome = titulo.replace("?", "").replace(":", " -").replace("/", "-")
    V.append(dict(entrada=f"{T}/{pasta}/{bruto}.MOV", transcricao=f"{T}/tr/{bruto}.json",
                  saida=f"{T}/out/{n}- {nome}.mp4", titulo=titulo, titulo_origem="inventado",
                  faixas=faixas, correcoes=COMUNS + kw.pop("correcoes", []), **kw))


video(5, "IMG_7830", "Olheiras com agulha tipo MD Codes: mito ou verdade?", [[0.0, 39.1]])
video(6, "IMG_7833", "Rinomodelação só com agulha é técnica ultrapassada?",
      [[0.3, 11.75], [18.15, 82.0]],
      correcoes=[[r"\beu assegurança\b", "eu, segurança"], [r"\bbolos periosteal\b", "bolus periosteal"]])
video(7, "IMG_7837", "MD Codes só com agulha é técnica ultrapassada?",
      [[4.55, 71.2], [84.65, 86.75]],
      remover_legenda=[[31.3, 32.2]])
video(8, "IMG_7839", "Preenchimento de glabela com agulha é técnica ultrapassada?",
      [[1.7, 63.2]], destaques=[[60.1, 63.2, "VITALÍCIO"]], cartela=True)
video(9, "IMG_7840", "Bioestimulador de hidroxiapatita: diluído ou puro?",
      [[4.6, 101.5]],
      correcoes=[[r"^[Ee]stimulador\b", "Bioestimulador"], [r"\bVitalício, até lá\b", "Vitalício, até lá"]],
      produtos=produtos([(5.88, "radiesse"), (74.32, "radiesse")], 101.5),
      destaques=[[95.0, 101.5, "VITALÍCIO"]], cartela=True)
video(10, "IMG_7841", "Bioremodelador: quando indicar na prática clínica?", [[2.75, 87.0]],
      remover_legenda=[[30.09, 30.13]],
      produtos=produtos([(43.71, "profhilo")], 87.0),
      destaques=[[83.17, 87.0, "VITALÍCIO"]], cartela=True)
video(11, "IMG_7843", "Pode misturar ácido hialurônico com bioestimulador?",
      [[0.85, 120.0]], remover_legenda=[[0.0, 0.88]],
      correcoes=[[r"\bSe eu estudo no mesmo combo\b", "Tudo isso no mesmo combo"]],
      destaques=[[116.7, 120.0, "VITALÍCIO"]], cartela=True)
video(12, "IMG_7845", "Os 3 melhores preenchedores para os lábios", [[0.0, 83.5]],
      remover_legenda=[[39.3, 42.0]],
      produtos=produtos([(6.80, "revanesse_kiss"), (8.66, "neuramis_deep"), (10.16, "belotero_intense"),
                         (14.66, "restylane_refyne"), (16.68, "eptq_s100"), (28.14, "rennova_deep_line"),
                         (43.18, "restylane_kiss")], 83.5))
video(13, "IMG_7846", "Os 3 melhores produtos para rinomodelação", [[0.0, 84.4]],
      produtos=produtos([(10.98, "yvoire_contour"), (12.90, "rennova_lift_plus"), (15.96, "perfectha_subskin"),
                         (34.62, "singderm"), (37.22, "restylane_lyft"), (40.98, "neuramis_deep"),
                         (53.20, "juvederm_voluma")], 84.4))
video(14, "IMG_7848", "Os 3 melhores produtos para o bigode chinês", [[0.0, 78.6]],
      produtos=produtos([(6.36, "neauvia_stimulate"), (10.10, "singderm"), (14.96, "restylane_defyne"),
                         (31.18, "sofiderm"), (39.12, "rennova_lift_plus"), (44.60, "biogelis")], 78.6))
video(15, "IMG_7851", "Preenchimento labial com seringa BD é perda de tempo?", [[0.8, 64.3]])
video(16, "IMG_7854", "Efeito vacina da toxina: mito ou verdade?", [[0.0, 70.1]])
video(17, "IMG_7890", "Amanhã começa a Black Friday Vitalícia", [[0.4, 137.9]], cartela=True)
video(18, "IMG_7889", "É hoje: Black Friday Vitalícia", [[1.4, 69.05], [70.12, 147.4]], cartela=True)
video(19, "IMG_7902", "Quanto você já investiu em cursos?", [[0.0, 76.45], [79.12, 173.25]], cartela=True)

# Ajuste da Keila (19/10/2026): aprovados sem mudança o 6, o 12 e o 14. Nos demais, a reação da
# pessoa entra inteira (sem cortar a pausa depois da pergunta) e todos terminam com o CTA da Black
# "Comente Vitalício" (arquivo FEA-02 BLACK VITALICIA_9x16_COPY01_DOURADO_COMENTE.mp4).
APROVADOS = {6, 12, 14}
for v in V:
    n = int(os.path.basename(v["saida"]).split("-")[0])
    if n not in APROVADOS:
        v["pausa_max"] = 999
        v["cartela"] = True

CTA = glob.glob(f"{T}/cta/*COMENTE*.mp4")
json.dump({"ffmpeg": FF, "fontsdir": f"{T}/fonts", "whoosh": f"{AQUI}/FEA-som-arrasto-titulo.wav",
           "cartela": CTA[0] if CTA else f"{T}/FEA-cartela-bf.mp4", "videos": V}, sys.stdout, ensure_ascii=False, indent=1)
