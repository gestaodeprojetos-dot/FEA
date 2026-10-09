#!/usr/bin/env python3
"""FEA · [FEED] ADS 12 e [STORIES] ADS 12 (jpg, Ebook Olheiras) em espanhol LATAM. Lote G.

Troca só a copy. Fundo preto chapado: texto apagado repintando de preto.
Mantidos do original, por serem iguais em espanhol: selo vermelho "EVITE:", o item
"RESULTADOS INCONSISTENTES." e a linha "TRIDIMENSIONAL" do logo. Marcadores (•) intactos.
O Story é o mesmo layout do Feed deslocado 248 px para baixo.
Copy ES: ../FEA-copy-criativos-final.py. Preço: precos.json (preco).
Rodar a partir de fea_artes/:  python3 criativos/fea_jpg_ads12.py
Originais (Drive Brasil): trabalho/G-ads12-feed.jpg ([FEED] ADS 12.jpg 13HDyklywbvy79y8wT-yLmWijzhvmtdIZ),
trabalho/G-ads12-story.jpg ([STORIES] ADS 12.jpg 168ABz0MOoVKTT1YPFLofXpB7pBCFf_mh).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads10a13 import *  # noqa
from fea_arte_lib import abrir, salvar, preencher, PRECOS

PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
DOURADO, VERDE = (240, 194, 108), (36, 255, 75)
SERIF, OS_REG = 'NotoSerif_400Regular', 'OpenSans_400Regular'
LARG_MAX = 960

# blocos centrados: (linhas_pt, linhas_es, [(topo, x0, x1)], cor)
DOURADO_PT = ['Preenchimento de', 'olheiras não é difícil.']
DOURADO_ES = ['El relleno de', 'ojeras no es difícil.']
DOURADO_MED = [(166, 253, 799), (252, 215, 838)]
BRANCO_PT = ['É imprevisível pra quem', 'não tem método']
BRANCO_ES = ['Es imprevisible para quien', 'no tiene método.']
BRANCO_MED = [(361, 156, 897), (458, 283, 768)]
APRENDA_PT = ['Aprenda o raciocínio clínico', 'estruturado por R$97']
APRENDA_MED = [(967, 272, 806), (1021, 340, 741)]
# itens com marcador (texto Open Sans maiúsculo com entreletra); o 3º é igual em ES e fica intacto
ITENS = [(712, 254, 850, 'INSEGURANÇA NO PLANO CORRETO;', 'INSEGURIDAD SOBRE EL PLANO CORRECTO;'),
         (764, 256, 695, 'DÚVIDA NO DIAGNÓSTICO;', 'DUDAS EN EL DIAGNÓSTICO;')]
CAP_ITEM, TOPO_CAP_ITEM1 = 23, 712   # 'I' de INSEGURANÇA: 712 a 734


def bloco(im, pt, es, med, cor, dy, spans_extra=None):
    i = max(range(len(pt)), key=lambda k: med[k][2] - med[k][1])
    f = calib(SERIF, pt[i], med[i][2] - med[i][1] + 1)
    while max(largura_spans([(s, f, cor)]) for s in es) > LARG_MAX:
        f = F(SERIF, f.size - 0.25)
    for topo, x0, x1 in med:
        preencher(im, (x0 - 14, topo + dy - 6, x1 + 14, topo + dy + int(f.size * 1.3)), PRETO)
    for k, (s_pt, s_es, (topo, x0, x1)) in enumerate(zip(pt, es, med)):
        spans = [(s_es, f, cor)] + (spans_extra(f) if spans_extra and k == len(pt) - 1 else [])
        desenhar_spans(im, spans, base_de(f, s_pt, topo + dy), centro=(x0 + x1) / 2)
    return f


def gerar(dy, arq, saida):
    im = abrir(os.path.join('trabalho', arq))

    # 1. frase dourada e 2. frase branca (Noto Serif)
    bloco(im, DOURADO_PT, DOURADO_ES, DOURADO_MED, DOURADO, dy)
    bloco(im, BRANCO_PT, BRANCO_ES, BRANCO_MED, BRANCO, dy)

    # 3. itens com marcador: mesma fonte e entreletra; reduz (máx. 15 %) só se passar de x=960
    f = por_altura_maiuscula(OS_REG, CAP_ITEM)
    tr = entreletra(f, ITENS[0][3], ITENS[0][2] - ITENS[0][1] + 1)
    base1 = TOPO_CAP_ITEM1 + CAP_ITEM  # topos de maiúscula dos 3 itens: 712, 771, 830 (passo 59)
    while max(largura_spans([(es, f, BRANCO, None, tr)]) + x0 for _, x0, _, _, es in ITENS) > LARG_MAX:
        k = (f.size - 0.25) / f.size
        f, tr = F(OS_REG, f.size - 0.25), tr * k
    for topo, x0, x1, pt, es in ITENS:
        preencher(im, (245, topo + dy - 8, 900, topo + dy + 36), PRETO)
    for n, (topo, x0, x1, pt, es) in enumerate(ITENS):
        base = base1 + dy + 59 * n
        desenhar_spans(im, [(es, f, BRANCO, None, tr)], base, x_esq=x0)

    # 4. "Aprenda el razonamiento clínico / estructurado por US$ [PRECIO]"
    bloco(im, APRENDA_PT, ['Aprenda el razonamiento clínico', 'estructurado por '], APRENDA_MED, BRANCO, dy,
          spans_extra=lambda f: [(PRECOS['preco'], f, VERDE)])

    # 5. logo: linhas 1 e 3 trocadas (mesmo logo do ADS 11, 10 px abaixo)
    im = logo_es(im, 0, 10 + dy)
    print('ok', salvar(im, saida), im.size)
    return im


if __name__ == '__main__':
    gerar(0, 'G-ads12-feed.jpg', 'FEA-[FEED] ADS 12 - LATAM.jpg')
    gerar(248, 'G-ads12-story.jpg', 'FEA-[STORIES] ADS 12 - LATAM.jpg')
