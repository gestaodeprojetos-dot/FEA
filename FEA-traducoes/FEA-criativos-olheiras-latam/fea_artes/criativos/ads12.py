#!/usr/bin/env python3
"""FEA · Ads 12 (Feed e Story) em espanhol LATAM. Troca só a copy.

Originais em trabalho/C-ads12-feed.png e trabalho/C-ads12-story.png (Drive Brasil).
Fontes: Plus Jakarta Sans ExtraBold (título e CTA) e Regular (corpo).
O corpo em espanhol é mais longo: é requebrado em linhas equilibradas, no mesmo número
de linhas do original, reduzindo a fonte no máximo 15 % se precisar.
Rodar a partir de fea_artes/:  python3 criativos/ads12.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ads10 import *  # noqa: F401,F403  (fea_arte_lib + linha_cores, PJS, cores)

PJS_REG = fonte('PlusJakartaSans_400Regular')
CINZA = (239, 239, 239)
TEXTO = lambda r, g, b: (r > 150) & (g > 130)

TIT_PT = ['Preenchimento Tridimensional', 'de Olheiras: Um Guia Completo', 'com a Metodologia ARTI']
TIT_ES = [[('Relleno tridimensional', LARANJA)],
          [('de ojeras:', LARANJA), (' una guía completa', BRANCO)],
          [('con la metodología ARTI', BRANCO)]]
CORPO_ES = ('Esta guía muestra cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e '
            'Intercurrencias) en el relleno de ojeras, la región más delicada del rostro, para obtener '
            'resultados superiores donde la mayoría falla.')
CTA_PT12 = ['Toque em “Saiba mais”', 'e libere o seu acesso!']
CTA_ES12 = [[('Toque en ', BRANCO), ('“Más información”', LARANJA)], [('y obtenga su acceso.', BRANCO)]]


def quebrar(f, texto, n, larg_max):
    """Quebra em n linhas o mais equilibradas possível (menor largura máxima). None se não couber."""
    pal = texto.split()
    w = lambda s: f.getbbox(s)[2] - f.getbbox(s)[0]
    melhor = None
    lo, hi = max(w(p) for p in pal), larg_max
    while hi - lo > 2:  # busca binária na largura limite
        mid = (lo + hi) / 2
        linhas, cur = [], ''
        for p in pal:
            t = (cur + ' ' + p).strip()
            if w(t) <= mid:
                cur = t
            else:
                linhas.append(cur)
                cur = p
        linhas.append(cur)
        if len(linhas) <= n:
            melhor, hi = linhas, mid
        else:
            lo = mid
    return melhor


def corpo(im, pt, tops, larg_ref, larg_max, cx):
    f0 = calibrar(PJS_REG, pt[0], larg_ref)
    base1 = tops[0] - f0.getbbox(pt[0])[1]
    baseN = tops[-1] - f0.getbbox(pt[-1])[1]
    passo = (baseN - base1) / (len(pt) - 1)
    f = f0
    while True:
        linhas = quebrar(f, CORPO_ES, len(pt), larg_max)
        if linhas or f.size <= f0.size * 0.85:
            break
        f = ImageFont.truetype(PJS_REG, f.size - 0.25)
    linhas = linhas or quebrar(f, CORPO_ES, len(pt) + 1, larg_max)
    # se a fonte reduziu, mantém o bloco centrado verticalmente no mesmo espaço
    passo_es = passo * f.size / f0.size
    meio = base1 + passo * (len(pt) - 1) / 2
    b0 = meio - passo_es * (len(linhas) - 1) / 2
    d = ImageDraw.Draw(im)
    for i, s in enumerate(linhas):
        l, _, r, _ = f.getbbox(s, anchor='ls')
        d.text((cx - (r - l) / 2 - l, b0 + i * passo_es), s, font=f, fill=CINZA, anchor='ls')
    return linhas, f.size / f0.size


def montar(arquivo, rect, tit_tops, tit_larg, tit_cx, corpo_pt, corpo_tops, corpo_larg, corpo_max, corpo_cx,
           cta_tops, cta_larg, cta_cx):
    im = abrir(arquivo)
    im = apagar(im, rect, TEXTO, 3)
    f = calibrar(PJS, TIT_PT[1], tit_larg)
    bloco_cores(im, TIT_PT, TIT_ES, tit_tops, f, tit_cx)
    linhas, esc = corpo(im, corpo_pt, corpo_tops, corpo_larg, corpo_max, corpo_cx)
    f = calibrar(PJS, CTA_PT12[0], cta_larg)
    bloco_cores(im, CTA_PT12, CTA_ES12, cta_tops, f, cta_cx)
    print(os.path.basename(arquivo), 'corpo em %d linhas, escala %.0f%%' % (len(linhas), esc * 100))
    for s in linhas:
        print('   ', s)
    return im


def feed():
    return montar('trabalho/C-ads12-feed.png', (90, 584, 995, 992),
                  [588, 629, 669], 808 - 279 + 1, 545,
                  ['Este guia revela como aplicar a metodologia ARTI',
                   '— Anatomia, Reologia, Técnica e Intercorrências',
                   '— no preenchimento de olheiras, a região mais delicada da',
                   'face, conquistando resultados superiores onde a maioria falha.'],
                  [742, 779, 820, 860], 887 - 202 + 1, 880, 544,
                  [918, 957], 742 - 347 + 1, 544.5)


def story():
    return montar('trabalho/C-ads12-story.png', (90, 1030, 995, 1696),
                  [1037, 1090, 1143], 884 - 193 + 1, 541,
                  ['Este guia revela como aplicar a',
                   'metodologia ARTI — Anatomia, Reologia,',
                   'Técnica e Intercorrências— no preenchimento',
                   'de olheiras, a região mais delicada da',
                   'face, conquistando resultados superiores',
                   'onde a maioria falha.'],
                  [1238, 1289, 1337, 1390, 1443, 1494], 817 - 263 + 1, 850, 539.5,
                  [1601, 1652], 797 - 281 + 1, 539)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print('ok', salvar(feed(), 'FEA-Ads 12 - PTO-LATAM - Feed.png'))
    print('ok', salvar(story(), 'FEA-Ads 12 - PTO-LATAM - Story.png'))
