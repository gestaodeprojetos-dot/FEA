#!/usr/bin/env python3
"""FEA · [FEED] ADS 13 e [STORIES] ADS 13 (jpg, Ebook Olheiras) em espanhol LATAM. Lote G.

Troca só a copy. Fundo é foto desfocada do mockup do ebook (tablet com a capa em PT):
o mockup NÃO é tocado (fase 2). Texto apagado por inpainting clássico OpenCV (Telea),
sem IA generativa. Parágrafo com estilos mistos (Noto Serif Regular branco; "su" Bold
Italic branco; trecho de destaque Bold Italic dourado), quebrado por palavras dentro da
mesma largura do original (Feed alinhado à esquerda, Story centralizado).
Copy ES: ../FEA-copy-criativos-final.py. Preço: precos.json (de_297 riscado, preco).
Rodar a partir de fea_artes/:  python3 criativos/fea_jpg_ads13.py
Originais (Drive Brasil): trabalho/G-ads13-feed.jpg ([FEED] ADS 13.jpg 19akeAE38SsbFFCK_apTlVlhrhOcPAISt),
trabalho/G-ads13-story.jpg ([STORIES] ADS 13.jpg 15Kgi-NCFcaAyLqrcp4RCGZlcJVFitPcm).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads10a13 import *  # noqa
from fea_arte_lib import abrir, salvar, apagar, PRECOS

BRANCO, DOURADO, VERDE_P, VERMELHO = (255, 255, 255), (216, 175, 96), (94, 232, 154), (254, 0, 0)
REG, BI, BOLD = 'NotoSerif_400Regular', 'NotoSerif_700Bold_Italic', 'NotoSerif_700Bold'
OS_BOLD = 'OpenSans_700Bold'
PASSO = 87  # entrelinha do parágrafo no original (Feed e Story)

# texto ES em trechos de estilo: (texto, estilo) estilo: r = regular branco, bi = bold itálico branco, bio = bold itálico dourado
PARAGRAFO = [('Convierta el relleno de ojeras en ', 'r'), ('su ', 'bi'), ('mayor diferencial al dominar una habilidad', 'bio'),
             (' que pocos profesionales tienen.', 'r')]
CTA_PT, CTA_ES = 'GARANTA JÁ O SEU', 'ASEGURE EL SUYO AHORA'

MED = {
    'feed': dict(arq='G-ads13-feed.jpg', saida='FEA-[FEED] ADS 13 - LATAM.jpg', alinhar='esquerda',
                 par_topo=336, par_x=(143, 952), par_area=(120, 320, 975, 852), par_ult_base_max=834 + 10,
                 preco_D=(980, 1007), preco_x=(276, 803), risco_cor=BRANCO, preco_area=(250, 955, 830, 1030),
                 btn_txt=(596, 913, 1218, 1238), btn=(535, 976),
                 logo=(-332, 26)),
    'story': dict(arq='G-ads13-story.jpg', saida='FEA-[STORIES] ADS 13 - LATAM.jpg', alinhar='centro',
                  par_topo=435, par_x=(146, 956), par_area=(120, 420, 975, 950), par_ult_base_max=933 + 10,
                  preco_D=(1013, 1040), preco_x=(276, 803), risco_cor=VERMELHO, preco_area=(250, 990, 830, 1063),
                  btn_txt=(381, 698, 1123, 1143), btn=(320, 761),
                  logo=(0, 85)),
}

TEXTO = lambda r, g, b: ((r + g + b) > 430) | ((r > 140) & (g > 105) & (b < 120) & (r > b + 55))


def fontes(tam):
    return {'r': (F(REG, tam), BRANCO), 'bi': (F(BI, tam), BRANCO), 'bio': (F(BI, tam), DOURADO)}


def quebrar(tam, largura):
    fs = fontes(tam)
    palavras = []  # cada palavra: lista de (texto, estilo)
    for txt, est in PARAGRAFO:
        partes = txt.split(' ')
        for j, p in enumerate(partes):
            if j > 0 or not palavras:
                palavras.append([])
            if p:
                palavras[-1].append((p, est))
    palavras = [w for w in palavras if w]
    linhas, atual = [], []
    for w in palavras:
        teste = atual + ([(' ', atual[-1][1])] if atual else []) + w
        spans = [(t, fs[e][0], fs[e][1]) for t, e in teste]
        if atual and largura_spans(spans) > largura:
            linhas.append(atual)
            atual = list(w)
        else:
            atual = teste
    linhas.append(atual)
    return [[(t, fs[e][0], fs[e][1]) for t, e in l] for l in linhas]


def gerar(fmt):
    M = MED[fmt]
    im = abrir(os.path.join('trabalho', M['arq']))

    # 1. parágrafo
    x0, x1 = M['par_x']
    tam = calib(REG, 'preenchimento de olheiras', 952 - 143 + 1).size
    base0 = base_de(F(REG, tam), 'Transforme o', M['par_topo'])
    im = apagar(im, M['par_area'], TEXTO, dil=3, raio=7)
    t = tam
    while True:
        linhas = quebrar(t, x1 - x0)
        ult = base0 + PASSO * (t / tam) * (len(linhas) - 1)
        if ult <= M['par_ult_base_max'] or t < tam * 0.85:
            break
        t -= 0.25
    # o original tem 6 linhas; com menos linhas o bloco desce meia entrelinha por linha a menos,
    # para manter o mesmo centro vertical e o respiro até o preço
    desl = PASSO * (t / tam) * max(0, 6 - len(linhas)) / 2
    for i, l in enumerate(linhas):
        b = base0 + desl + PASSO * (t / tam) * i
        if M['alinhar'] == 'esquerda':
            desenhar_spans(im, l, b, x_esq=x0)
        else:
            desenhar_spans(im, l, b, centro=(x0 + x1) / 2)
    print(fmt, 'parágrafo:', len(linhas), 'linhas, fonte %.2f (orig %.2f)' % (t, tam))

    # 2. preço: De [Bold riscado] a solo [Bold verde maior]
    d0, d1 = M['preco_D']
    fr = por_altura_maiuscula(REG, d1 - d0 + 1)
    fb = F(BOLD, fr.size)
    fg = F(BOLD, fr.size * 1.27)  # R$97 do original é ~27 % maior (altura 970-1011 x 980-1007)
    cor297 = BRANCO if M['risco_cor'] == BRANCO else VERMELHO
    im = apagar(im, M['preco_area'], lambda r, g, b: ((r + g + b) > 430) | ((g > 170) & (r < 170)) | ((r > 170) & (g < 90)), dil=3, raio=7)

    def spans(fr, fb, fg):
        return [('De ', fr, BRANCO), (PRECOS['de_297'], fb, cor297, M['risco_cor']), (' a solo ', fr, BRANCO), (PRECOS['preco'], fg, VERDE_P)]
    while largura_spans(spans(fr, fb, fg)) > 960:
        k = 0.99
        fr, fb, fg = F(REG, fr.size * k), F(BOLD, fb.size * k), F(BOLD, fg.size * k)
    desenhar_spans(im, spans(fr, fb, fg), d1 + 1, centro=sum(M['preco_x']) / 2, cap_risco=0.45)

    # 3. botão (gradiente verde intacto; só o texto é trocado)
    tx0, tx1, c0, c1 = M['btn_txt']
    fc = por_altura_maiuscula(OS_BOLD, c1 - c0)  # 'G' tem overshoot de ~1 px
    tr = entreletra(fc, CTA_PT, tx1 - tx0 + 1)
    folga = 36
    lim = (M['btn'][1] - M['btn'][0]) - 2 * folga
    tam0 = fc.size
    while largura_spans([(CTA_ES, fc, BRANCO, None, tr)]) > lim and tr > 0.6 * entreletra(F(OS_BOLD, tam0), CTA_PT, tx1 - tx0 + 1):
        tr -= 0.1
    while largura_spans([(CTA_ES, fc, BRANCO, None, tr)]) > lim and fc.size > tam0 * 0.85:
        fc = F(OS_BOLD, fc.size - 0.25)
    im = apagar(im, (tx0 - 6, c0 - 12, tx1 + 6, c1 + 8), lambda r, g, b: (r > 200) & (g > 200) & (b > 200), dil=2, raio=5)
    centro = sum(M['btn']) / 2
    desenhar_spans(im, [(CTA_ES, fc, BRANCO, None, tr)], c1, centro=centro)
    print(fmt, 'botão: fonte %.2f (orig %.2f), entreletra %.2f' % (fc.size, tam0, tr))

    # 4. logo dourado sobre a foto: apagado por inpainting
    dx, dy = M['logo']
    gold = lambda r, g, b: (r > 120) & (g > 90) & (r > b + 50)
    im = logo_es(im, dx, dy, apagar_linha=lambda im, cx: apagar(im, cx, gold, dil=2, raio=6))

    print('ok', salvar(im, M['saida']), im.size)
    return im


if __name__ == '__main__':
    for fmt in MED:
        gerar(fmt)
