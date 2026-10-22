#!/usr/bin/env python3
"""Gera o projeto.json do lote "Melhores tratamentos" (pasta de brutos 1QWcXrtE2oh04fAXn6jluvpZVEYOdmwZJ).

Mesmo padrão do lote "Melhores produtos" (fea_projeto_out_10_melhores_produtos.py), mais B-roll de
pele e envelhecimento quando o Dr. descreve o problema (Keila, 22/10/2026). O B-roll vem da
00 - Brutos: "FEA-B-roll pele flácida e envelhecida (face)" (Pexels e Mixkit, licença livre) e
"B roll pele flácida" (IMG_7683 a 7685, da clínica). Nada gerado por IA.

Uso: python3 fea_projeto_out_11_melhores_tratamentos.py PASTA_DE_TRABALHO > projeto.json
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_correcoes_marcas import COMUNS  # noqa: E402

T = sys.argv[1]
FF = open(f"{T}/env.sh").read().split("=", 1)[1].strip()
AQUI = os.path.dirname(os.path.abspath(__file__))
C = f"{T}/casos"
B = f"{T}/broll"

# B-roll de pele e envelhecimento
PELE_MAOS_PAPADA = f"{B}/IMG_7684.MOV"            # mãos de luva mostrando a flacidez do terço inferior
PELE_PESCOCO = f"{B}/IMG_7685.MOV"                # flacidez de pescoço
RUGAS_IDOSA = f"{B}/FEA-broll-01-close-idosa-rugas-frontais-pexels-5534415.mp4"
OLHO_IDOSO = f"{B}/FEA-broll-06-olho-homem-idoso-vertical-pexels-7299474.mp4"
PERFIL_IDOSO = f"{B}/FEA-broll-07-perfil-homem-idoso-vertical-pexels-7299468.mp4"
PELE_HOMEM = f"{B}/FEA-broll-05-close-pele-homem-idoso-vertical-pexels-7299472.mp4"
SKINCARE = f"{B}/10222560-uhd_4096_2160_25fps.mp4"   # mulher limpando o rosto
ESPELHO_OLHO = f"{B}/7545829-uhd_3840_2160_25fps.mp4"  # olhar a olheira no espelho
TECNOLOGIA = f"{B}/FEA-broll-15-laser-facial-mixkit-52153.mp4"

# casos clínicos da 00 - Brutos
BIO = f"{C}/IMG_2119.MOV"          # 53.OK- Bioestimulador (cânula)
DAO = f"{C}/IMG_2043.MOV"          # 47.OK- Paciente flacidez no pescoço (agulha na região do DAO)
NEFERTITI = f"{C}/IMG_6756.MOV"    # Toxina estética e Nefertiti (agulha na mandíbula)
FIOS = f"{C}/IMG_4730.MOV"         # Fios lisos de pdo
FIOS_OLHEIRA = f"{C}/IMG_1544.MOV"  # 12- OK. Fios de pdo para olheiras
RINO = f"{C}/IMG_5883.MOV"         # Rino (columela e base nasal)
GLABELA = f"{C}/IMG_2502.MOV"      # 42.OK- Profundidade agulha botox (glabela)
LABIO = f"{C}/IMG_0719.MOV"        # 23- Preenchimento paciente ruiva (lábio)
MARIONETE = f"{C}/IMG_1420.MOV"    # 18- OK. Mento (cânula no canto da boca)
OLHEIRA_MARCACAO = f"{C}/IMG_2661.MOV"  # 34.OK- Preenchimento de olheiras (marcação)


def foto(nome):
    achou = sorted(glob.glob(f"{T}/produtos/{nome}.*"))
    return achou[0] if achou else None


EXTRAS = [
    [r"\baço (al|hial)urônico\b", "ácido hialurônico"], [r"\bna cantinho\b", "no cantinho"],
    [r"\bfica tendo marcado\b", "fica tudo marcado"], [r"\bacilurônico\b", "ácido hialurônico"],
    [r"\bnefertite\b", "Nefertiti"], [r"\bsmas\b", "SMAS"], [r"\bTiamidol\b", "Thiamidol"],
    [r"\brinco\b", "vinco"], [r"\bencoragem\b", "ancoragem"], [r"\bdama propriamente\b", "derme propriamente"],
    [r"\bpropriedade sendo comprimida\b", "região sendo comprimida"], [r"\bde líquido\b", "de lifting"],
]

V = []


def video(n, bruto, titulo, faixa, casos, prods=(), **kw):
    nome = titulo.replace("?", "").replace(":", " -")
    ps = []
    for t, nome_p, dur in prods:
        f = foto(nome_p)
        if f:
            ps.append([t, f, dur])
        else:
            print(f"AVISO: sem foto de {nome_p}", file=sys.stderr)
    V.append(dict(entrada=f"{T}/b4/{bruto}.MOV", transcricao=f"{T}/tr/{bruto}.json",
                  saida=f"{T}/out_mt/{n}- {nome}.mp4", titulo=titulo, titulo_origem="inventado",
                  faixas=[faixa], pausa_max=999, cartela=True, correcoes=COMUNS + EXTRAS,
                  produtos=ps, casos=casos, **kw))


video(1, "IMG_7922", "3 melhores tratamentos para a linha de marionete", [0.2, 87.6], [
    [15.2, 21.0, PELE_MAOS_PAPADA, 1.0],
    [25.9, 31.5, DAO, 13.0],
    [43.3, 49.0, NEFERTITI, 12.0],
    [55.5, 61.5, MARIONETE, 0.5],
    [63.0, 69.0, BIO, 6.0],
    [73.6, 78.6, FIOS, 30.0]])
video(2, "IMG_7923", "3 melhores tratamentos para a flacidez do pescoço", [0.2, 79.2], [
    [4.9, 10.3, PELE_PESCOCO, 1.0],
    [16.0, 21.8, NEFERTITI, 3.0],
    [26.8, 32.0, NEFERTITI, 12.0],
    [38.2, 44.0, BIO, 6.0],
    [53.4, 59.0, TECNOLOGIA, 1.0]])
video(3, "IMG_7924", "3 melhores tratamentos para o código de barras", [0.2, 70.8], [
    [5.5, 11.0, RUGAS_IDOSA, 2.0],
    [28.4, 34.5, LABIO, 0.3],
    [46.1, 51.8, FIOS, 30.0],
    [57.4, 62.6, SKINCARE, 1.0]])
video(4, "IMG_7927", "Olheiras profundas e escuras: como tratar?", [0.3, 52.1], [
    [5.5, 10.1, OLHO_IDOSO, 1.0],
    [10.2, 14.6, OLHEIRA_MARCACAO, 24.0],
    [20.7, 26.0, FIOS_OLHEIRA, 20.0],
    [33.7, 39.0, ESPELHO_OLHO, 0.5]],
    prods=[(37.0, "eucerin_thiamidol", 2.5)])
video(5, "IMG_7928", "Ponta do nariz caindo: como tratar?", [0.0, 62.6], [
    [5.0, 9.5, PERFIL_IDOSO, 1.0],
    [19.8, 25.5, RINO, 18.0],
    [40.5, 45.6, RINO, 24.0]])
video(6, "IMG_7929", "Ruga profunda entre as sobrancelhas: como tratar?", [0.2, 79.7], [
    [5.8, 10.9, PELE_HOMEM, 1.0],
    [11.0, 16.5, GLABELA, 12.0],
    [27.6, 33.3, FIOS, 30.0],
    [38.0, 43.5, GLABELA, 19.0],
    [66.8, 72.8, SKINCARE, 3.0]])

CTA = glob.glob(f"{T}/cta/*COMENTE*.mp4")
json.dump({"ffmpeg": FF, "fontsdir": f"{T}/fonts", "whoosh": f"{AQUI}/FEA-som-arrasto-titulo.wav",
           "cartela": CTA[0], "musica": f"{T}/audio/musica_piano.wav", "musica_vol": 0.025,
           "sfx_pop": f"{T}/audio/pop.mp3", "sfx_split": f"{T}/audio/whoosh_split.mp3",
           "videos": V}, sys.stdout, ensure_ascii=False, indent=1)
