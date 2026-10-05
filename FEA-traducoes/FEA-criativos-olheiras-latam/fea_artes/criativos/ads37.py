#!/usr/bin/env python3
"""Ads 37 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Rodar a partir de fea_artes/:  python3 criativos/ads37.py
Originais: trabalho/Jads37-feed.png, trabalho/Jads37-story.png (Drive BR).
Faixa de mockups do ebook (capa e páginas em PT) NÃO é tocada: fase 2.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads36a40 import *  # noqa

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESC = lambda r, g, b: (r + g + b) < 250
ESC_APAGAR = lambda r, g, b: (r + g + b) < 560
ESC_SELO = lambda r, g, b: (r + g + b) < 330
OURO = lambda r, g, b: (r > 150) & (r - b > 70)
OURO_APAGAR = lambda r, g, b: (r > 90) & (r - b > 35)
ACENTO_DESFOCADO = lambda r, g, b: (r + g + b) < 540

HL_PT = ['Depois de mais', 'de 20 mil alunos...', 'percebemos um padrão.']
HL_ES = ['Después de formar a', 'más de 30.000 alumnos…', 'notamos un patrón.']
SUB_PT = 'As profissionais com melhores resultados em olheiras:'
SUB_ES = 'Las profesionales con mejores resultados en ojeras:'
IT_PT = ['não aplicam mais produto.', 'aplicam no plano correto.']
IT_ES = ['no aplican más producto.', 'lo aplican en el plano correcto.']


def ads37(arq, P):
    im = abrir(os.path.join(AQ, 'trabalho', arq))
    W = im.width
    ls = medir(im, P['texto'], ESC)
    assert len(ls) == 6, ls
    hl, sub, its = ls[:3], ls[3], ls[4:]
    cor_hl = cor_texto(im, (hl[2][2], hl[2][0], hl[2][3], hl[2][1]), ESC)
    cx = (hl[2][2] + hl[2][3]) / 2
    for l in hl:  # apaga só a área de cada linha original (não encosta no selo do canto)
        im = apagar_liso(im, (l[2] - 14, l[0] - 10, l[3] + 14, l[1] + 10), ESC_APAGAR, 4)
    im, _ = titulo_linhas(im, hl, HL_PT, HL_ES, SERIF_SEMI, 2, cor_hl, cx, P['lim_hl'], rotulo=arq)
    # subtítulo
    fs = calibrar_larg(SANS_REG, SUB_PT, sub[3] - sub[2] + 1)
    cor = cor_texto(im, (sub[2], sub[0], sub[3], sub[1]), ESC)
    im = apagar_liso(im, (sub[2] - 10, sub[0] - 10, sub[3] + 10, sub[1] + 10), ESC_APAGAR, 3)
    d = ImageDraw.Draw(im)
    cxs = (sub[2] + sub[3]) / 2
    d.text((cxs - largura(fs, SUB_ES) / 2 - fs.getbbox(SUB_ES)[0], sub[0] - fs.getbbox(SUB_PT)[1]), SUB_ES, font=fs, fill=cor)
    # itens (alinhados à esquerda, ao lado dos ícones ✗ ✓)
    fi = calibrar_larg(SANS_REG, IT_PT[0], its[0][3] - its[0][2] + 1)
    xe = min(l[2] for l in its)
    for l, p, e in zip(its, IT_PT, IT_ES):
        im = apagar_liso(im, (l[2] - 10, l[0] - 10, l[3] + 12, l[1] + 10), ESC_APAGAR, 3)
        d = ImageDraw.Draw(im)
        assert xe + largura(fi, e) < W - 80
        d.text((xe - fi.getbbox(e)[0], l[0] - fi.getbbox(p)[1]), e, font=fi, fill=cor)
    # CTA (texto dourado em botão verde-escuro)
    im = trocar_cta(im, P['cta'], OURO, OURO_APAGAR, P['seta'], SANS_XBOLD, 'APRENDA O QUE ELAS FAZEM',
                    'APRENDA LO QUE ELLAS HACEN', rotulo=arq)
    # selos: CÓPIAS -> COPIAS (selo nítido do centro e selo grande desfocado do canto)
    im, _ = tirar_acento_selo(im, P['selo'], ESC_SELO)
    im = tirar_acento_desfocado(im, *P['acento_desfocado'])
    return im


FEED = dict(texto=(250, 150, 1845, 1050), lim_hl=[(150, 1735), (150, 1715), (150, 1760)],
            cta=(543, 2098, 1630, 2270), seta=1476, selo=(1415, 1218, 1530, 1250),
            acento_desfocado=(1994, 2021, 233, 249, 275, False))
STORY = dict(texto=(150, 600, 1990, 1600), lim_hl=[(120, 1800), (120, 2040), (120, 2040)],
             cta=(530, 2634, 1630, 2806), seta=None, selo=(1405, 1797, 1510, 1820),
             acento_desfocado=(1940, 1992, 352, 376, 416, True))

if __name__ == '__main__':
    import numpy as _np
    for arq, P, nome in [('Jads37-feed.png', FEED, 'FEA-Ads 37 Feed - PTO-LATAM.png'),
                         ('Jads37-story.png', STORY, 'FEA-Ads 37 Story - PTO-LATAM.png')]:
        if P['seta'] is None:  # story: mesma posição horizontal do feed, medir de novo
            im0 = abrir(os.path.join(AQ, 'trabalho', arq))
            cs = [c for c in componentes(im0, P['cta'], OURO) if 60 < c[4] < 200]
            P['seta'] = max(c[0] for c in cs)
        print('ok', salvar(ads37(arq, P), nome))
