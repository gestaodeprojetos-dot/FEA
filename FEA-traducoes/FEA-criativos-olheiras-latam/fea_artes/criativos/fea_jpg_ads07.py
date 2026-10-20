#!/usr/bin/env python3
"""[FEED] ADS 07.jpg e [STORIES] ADS 07.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Originais em trabalho/Fads07-feed.jpg e trabalho/Fads07-story.jpg
(Drive 1aKrMUsrNkKa9PX5ZjsksXwOcPmtbCUwE e 1VvYlEPiprd5wMUJrlkRwHE-PF7rPaii8).
Fontes identificadas: Noto Serif Regular / Bold Italic (título), Open Sans Regular e
Noto Sans SemiBold (corpo), Archivo ExtraBold (assinatura dourada), Noto Sans Bold com
espaçamento (CTA). 'Ebook' dourado e 'TRIDIMENSIONAL' ficam com os pixels originais.
Story = mesmo layout deslocado (título +25/+194, corpo +40/+149, faixa inferior +332).
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads07.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg06a09 import *  # noqa
from fea_arte_lib import abrir, salvar, apagar, cor_texto, mascara

SR, SBI = 'NotoSerif_400Regular', 'NotoSerif_700Bold_Italic'
OR, NSB = 'OpenSans_400Regular', 'NotoSans_600SemiBold'
ARC, NB = 'Archivo_800ExtraBold', 'NotoSans_700Bold'
ESC = lambda r, g, b: ((r + g + b) < 500) & ((r - b) < 50)          # texto verde-escuro, exclui o dourado
OURO = lambda r, g, b: (r > 170) & (g > 120) & (b < 140) & (r - b > 70)
PRETO = lambda r, g, b: (r + g + b) < 330
LIM = 16


def recompor(orig, saida, tdx, tdy, cdx, cdy, bdy):
    im = abrir(orig)
    verde = cor_texto(im, (400 + tdx, 135 + tdy, 930 + tdx, 300 + tdy), lambda r, g, b: (r + g + b) < 450)

    # ---------- título (Noto Serif), alinhado à esquerda ----------
    lin = [(139, 404, 'Existe um limite seguro e'), (198, 402, 'você precisa conhecer:'),
           (258, 404, 'aprenda anatomia'), (318, 404, 'aplicada sem achismo e'),
           (378, 403, 'sem risco desnecessário.')]
    tam_r = tamanho_por_largura('Existe um limite seguro e', SR, 924 - 404 + 1)
    tam_b = tam_r
    bases = [base_de(y + tdy, t, SR if i < 2 else SBI, tam_r) for i, (y, _, t) in enumerate(lin)]
    im.paste(apagar(im, (395 + tdx, 125 + tdy, 1010 + tdx, 425 + tdy), ESC, 3))
    es = [('Existe un límite seguro y', SR), ('usted necesita conocerlo:', SR),
          ('aprenda anatomía', SBI), ('aplicada sin suposiciones', SBI), ('y sin riesgos innecesarios.', SBI)]
    x0 = 404 + tdx
    for (t, n), b in zip(es, bases):
        # alinhamento pela origem da linha (como no layout original); compensa só a tinta de 'E'/'a'/'u'
        ref = 'E' if n == SR else 'a'
        pena = x0 - F(n, tam_r).getbbox(ref, anchor='ls')[0]
        xi = pena + F(n, tam_r).getbbox(t[0], anchor='ls')[0]
        desenhar(im, [(t, n, verde, False)], tam_r if n == SR else tam_b, b, xi, alinh='esquerda')
        assert x0 + larg(t, n, tam_r) < im.width - LIM

    # ---------- corpo (Open Sans / Noto Sans SemiBold); 'Ebook' dourado mantido ----------
    m = mascara(im, (530 + cdx, 530 + cdy, 1060, 580 + cdy), OURO)
    ebook_fim = np.where(m.any(0))[0].max() + 530 + cdx
    m = mascara(im, (ebook_fim + 2, 535 + cdy, 1070, 575 + cdy), ESC)
    com_ini = np.where(m.any(0))[0].min() + ebook_fim + 2
    tam_o = tamanho_por_largura('profundidade e cuidados', OR, 960 - 543 + 1)
    tam_s = tamanho_por_largura('para evitar complicações.', NSB, 994 - 542 + 1)
    b1 = base_de(539 + cdy, 'Ebook com zonas de risco,', OR, tam_o)
    b2 = base_de(588 + cdy, 'profundidade e cuidados', OR, tam_o)
    b3 = base_de(637 + cdy, 'para evitar complicações.', NSB, tam_s)
    im.paste(apagar(im, (ebook_fim + 3, 530 + cdy, 1075, 580 + cdy), ESC, 3))
    im.paste(apagar(im, (530 + cdx, 580 + cdy, 1075, 690 + cdy), ESC, 3))
    desenhar(im, [('con zonas de riesgo,', OR, verde, False)], tam_o, b1, com_ini, alinh='esquerda')
    x_esq = 543 + cdx
    desenhar(im, [('profundidad y cuidados', OR, verde, False)], tam_o, b2, x_esq, alinh='esquerda')
    t3 = 'para evitar complicaciones.'
    while x_esq + larg(t3, NSB, tam_s) > im.width - LIM:
        tam_s -= 0.25
    desenhar(im, [(t3, NSB, verde, False)], tam_s, b3, 542 + cdx, alinh='esquerda')

    # ---------- assinatura dourada (linhas 1 e 3; TRIDIMENSIONAL original) ----------
    ouro = (247, 188, 87)
    tam_a = tamanho_por_largura('PREENCHIMENTO', ARC, 328 - 50 + 1)
    ba1 = base_de(1160 + bdy, 'PREENCHIMENTO', ARC, tam_a)
    ba3 = base_de(1223 + bdy, 'DE OLHEIRAS', ARC, tam_a)
    im.paste(apagar(im, (30, 1150 + bdy, 360, 1188 + bdy), OURO, 3))
    im.paste(apagar(im, (30, 1219 + bdy, 360, 1252 + bdy), OURO, 3))
    cx = (52 + 325) / 2
    desenhar(im, [('RELLENO', ARC, ouro, False)], tam_a, ba1, cx, cx)
    desenhar(im, [('DE OJERAS', ARC, ouro, False)], tam_a, ba3, cx, cx)

    # ---------- CTA (caixa com borda dourada e degradê: miolo esticado) ----------
    tr = 1.5
    tam_c = tamanho_por_largura('GARANTA JÁ O SEU', NB, 656 - 421 + 1, tr)
    bc = base_de(1208 + bdy, 'GARANTA O SEU', NB, tam_c)
    cta_es = 'ASEGURE EL SUYO AHORA'
    # o ES é mais longo: a caixa cresce para a esquerda (à direita está o crânio, limite x=690),
    # espaçamento entre letras 1,0 e fonte reduzida no máximo 15 %
    tr, pad, dir_max, esq_min = 1.0, 22, 690, 372
    tam_es = tam_c
    while True:
        l, r = tinta([(cta_es, NB, 0, False)], tam_es, tr)
        if (r - l) + 2 * pad <= dir_max - esq_min or tam_es <= tam_c * 0.85:
            break
        tam_es -= 0.25
    larg_cx = max(686 - 395, (r - l) + 2 * pad)
    nova = caixa_esticada(im, (395, 1177 + bdy, 686, 1250 + bdy), larg_cx, PRETO, x0_novo=min(395, dir_max - larg_cx))
    bc_es = base_de(1208 + bdy, 'GARANTA O SEU', NB, tam_c) + (F(NB, tam_c).getbbox('H', anchor='ls')[1] - F(NB, tam_es).getbbox('H', anchor='ls')[1]) / 2
    desenhar(im, [(cta_es, NB, (0, 0, 0), False)], tam_es, bc_es, nova[0], nova[2], tracking=tr)
    tam_c = (tam_c, tam_es)
    print(saida, 'titulo', tam_r, 'corpo', tam_o, tam_s, 'assinatura', tam_a, 'cta', tam_c, nova)
    print(salvar(im, saida))


if __name__ == '__main__':
    recompor('trabalho/Fads07-feed.jpg', 'FEA-[FEED] ADS 07 - LATAM.jpg', 0, 0, 0, 0, 0)
    recompor('trabalho/Fads07-story.jpg', 'FEA-[STORIES] ADS 07 - LATAM.jpg', 25, 194, 40, 149, 332)
