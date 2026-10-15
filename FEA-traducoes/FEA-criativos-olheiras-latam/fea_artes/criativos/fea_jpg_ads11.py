#!/usr/bin/env python3
"""FEA · [FEED] ADS 11 e [STORIES] ADS 11 (jpg, Ebook Olheiras) em espanhol LATAM. Lote G.

Troca só a copy. Fundo preto chapado: texto apagado repintando de preto. Ícones ✅ do
original preservados (só o texto ao lado é trocado). Logo dourado do título do ebook:
"PREENCHIMENTO / TRIDIMENSIONAL / DE OLHEIRAS" vira "RELLENO / TRIDIMENSIONAL / DE OJERAS"
(linha do meio é a original, intacta); a textura/degradê dourado das linhas novas é
transferida do próprio logo original (campo de cor por inpainting clássico, sem IA).
O Story é o mesmo layout do Feed deslocado 155 px para baixo.
Copy ES: ../FEA-copy-criativos-final.py. Preço: precos.json (de_297 riscado, preco).
Rodar a partir de fea_artes/:  python3 criativos/fea_jpg_ads11.py
Originais (Drive Brasil): trabalho/G-ads11-feed.jpg ([FEED] ADS 11.jpg 14fLmZdyzqeWMjujtqHa2brLeheO9YCrJ),
trabalho/G-ads11-story.jpg ([STORIES] ADS 11.jpg 1k4Ir1JiONGuGxmJcMz4rVS_8fkDaPqYH).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads10a13 import *  # noqa
from fea_arte_lib import abrir, salvar, preencher, PRECOS

PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
VERMELHO, VERDE = (254, 0, 0), (36, 255, 75)
SERIF, SANS, OS_REG, OS_BOLD, LOGO = ('NotoSerif_400Regular', 'NotoSans_400Regular', 'OpenSans_400Regular',
                                       'OpenSans_700Bold', 'Arimo_700Bold')
LARG_MAX = 960

# lista: (topo_pt, x_tinta_pt, texto_pt, texto_es, tem_icone)
LISTA = [
    (558, 332, 'Metodologia ARTI aplicada ao', 'Metodología ARTI aplicada al', True),
    (602, 292, 'preenchimento de olheiras;', 'relleno de ojeras;', False),
    (661, 329, 'Técnica tridimensional passo', 'Técnica tridimensional paso', True),
    (712, 290, 'a passo;', 'a paso;', False),
    (764, 331, 'Casos clínicos comentados +', 'Casos clínicos comentados +', True),
    (808, 289, 'video aulas explicativas;', 'videoclases explicativas;', False),
    (867, 329, 'Tudo organizado para', 'Todo organizado para su', True),
    (911, 290, 'aplicação prática imediata.', 'aplicación práctica inmediata.', False),
]
CTA_PT = ('TOQUE EM SAIBA MAIS E ', 'GARANTA O SEU')
CTA_ES = ('TOQUE EN MÁS INFORMACIÓN Y ', 'ASEGURE EL SUYO')


def pena_x(f, texto, x_tinta):
    """Origem horizontal da linha (pena) a partir da tinta medida do texto PT."""
    return x_tinta - f.getbbox(texto, anchor='ls')[0]


def gerar(fmt, dy, arq, saida):
    im = abrir(os.path.join('trabalho', arq))
    Y = lambda y: y + dy

    # 1. título de preço (Noto Serif com entreletra; linha 1 maior que a linha 2, como no original)
    f1 = por_altura_maiuscula(SERIF, 69)                     # altura do 'D' (285 a 353)
    t1 = entreletra(f1, 'De R$297', 731 - 312 + 1)
    f2 = por_altura_maiuscula(SERIF, 57)                     # altura do 'P' (398 a 454)
    t2 = entreletra(f2, 'Por apenas R$97', 850 - 187 + 1)
    b1, b2 = Y(353 + 1), Y(454 + 1)
    preencher(im, (150, Y(270), 930, Y(480)), PRETO)

    def l1(f, t):
        return [('De ', f, BRANCO, None, t), (PRECOS['de_297'], f, VERMELHO, VERMELHO, t)]

    def l2(f, t):
        return [('A solo ', f, BRANCO, None, t), (PRECOS['preco'], f, VERDE, None, t)]
    while largura_spans(l1(f1, t1)) > LARG_MAX:
        k = (f1.size - 0.5) / f1.size
        f1, t1 = F(SERIF, f1.size - 0.5), t1 * k
    while largura_spans(l2(f2, t2)) > LARG_MAX:
        k = (f2.size - 0.5) / f2.size
        f2, t2 = F(SERIF, f2.size - 0.5), t2 * k
    desenhar_spans(im, l1(f1, t1), b1, centro=(312 + 731) / 2, cap_risco=0.43)
    desenhar_spans(im, l2(f2, t2), b2, centro=(187 + 850) / 2)

    # 2. lista com ✅ (Noto Sans branco, alinhada à esquerda; ícones intactos)
    fl = calib(SANS, LISTA[0][2], 774 - 332 + 1)
    for topo, x, pt, es, icone in LISTA:
        preencher(im, (325 if icone else 280, Y(topo - 8), 860, Y(topo + 40)), PRETO)
    for topo, x, pt, es, icone in LISTA:
        base = base_de(fl, pt, Y(topo))
        pena = pena_x(fl, pt, x)
        desenhar_spans(im, [(es, fl, BRANCO)], base, x_esq=pena + fl.getbbox(es, anchor='ls')[0])

    # 3. CTA (Open Sans Regular branco + Bold verde, entreletra); altura do 'T' 1029 a 1051
    fr, fb = por_altura_maiuscula(OS_REG, 23), por_altura_maiuscula(OS_BOLD, 23)
    lo, hi = -2.0, 10.0
    for _ in range(40):
        tr = (lo + hi) / 2
        if largura_spans([(CTA_PT[0], fr, BRANCO, None, tr), (CTA_PT[1], fb, VERDE, None, tr)]) > 882 - 195 + 1:
            hi = tr
        else:
            lo = tr
    spans = [(CTA_ES[0], fr, BRANCO, None, tr), (CTA_ES[1], fb, VERDE, None, tr)]
    preencher(im, (150, Y(1015), 930, Y(1070)), PRETO)
    desenhar_spans(im, spans, Y(1051 + 1), centro=(195 + 882) / 2)

    # 4. logo do título: linhas 1 e 3 trocadas, linha 2 (TRIDIMENSIONAL) intacta
    im = logo_es(im, 0, dy)

    print('ok', salvar(im, saida), im.size)
    return im


if __name__ == '__main__':
    gerar('feed', 0, 'G-ads11-feed.jpg', 'FEA-[FEED] ADS 11 - LATAM.jpg')
    gerar('story', 155, 'G-ads11-story.jpg', 'FEA-[STORIES] ADS 11 - LATAM.jpg')
