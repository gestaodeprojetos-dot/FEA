#!/usr/bin/env python3
"""FEA · Ads 01 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Texto em caixa chapada cinza-clara (fonte condensada tipo "Strong" do Instagram,
reproduzida com Bebas Neue comprimida na horizontal) e CTA em caixa escura.
Rodar a partir de fea_artes/: python3 criativos/ads01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads01a04 import *  # noqa

BEBAS = fonte('BebasNeue_400Regular')
CORPO_ES = (PRECOS['pct_desconto'] + ' DE DESCUENTO PARA INYECTORES QUE QUIEREN DOMINAR EL PROCEDIMIENTO MÁS '
            'DESAFIANTE DE LA ARMONIZACIÓN FACIAL (EL RELLENO DE OJERAS) Y CONVERTIRSE EN REFERENTES DEL MERCADO.')
CTA_ES = 'TOQUE EN MÁS INFORMACIÓN'


def tipo_calibrado(cap_px, linha_pt, largura_pt):
    """Bebas no tamanho que reproduz a altura de caixa-alta e compressão kx que reproduz a largura."""
    base = ImageFont.truetype(BEBAS, 100)
    cap100 = -base.getbbox('H', anchor='ls')[1]
    tam = cap_px * 100 / cap100
    f = ImageFont.truetype(BEBAS, tam)
    l, _, r, _ = f.getbbox(linha_pt)
    return Tipo(BEBAS, tam, largura_pt / (r - l))


def ads01(origem, saida, corpo, cta):
    im = abrir(origem)
    # ---- corpo: caixa cinza-clara chapada
    cx0, cy0, cx1, cy1 = corpo['caixa']
    fundo = cor_fundo(im, (cx0 + 4, cy0 + 4, cx0 + 14, cy1 - 4))
    cor_txt = cor_texto(im, corpo['caixa'], ESCURO)
    t = tipo_calibrado(corpo['cap'], corpo['linha_pt'], corpo['larg_pt'])
    preencher(im, corpo['caixa'], fundo)
    f, ls = ajustar(CORPO_ES, t, corpo['larg_max'], corpo['n_linhas'])
    passo = corpo['passo'] * f.size / t.size
    cap = corpo['cap'] * f.size / t.size
    altura_bloco = cap + passo * (len(ls) - 1)
    base1 = corpo['centro_y'] - altura_bloco / 2 + cap
    escrever_bloco(im, ls, f, cor_txt, (cx0 + cx1) / 2, base1, passo)
    print(os.path.basename(saida), 'corpo', round(f.size / t.size, 3), ls)
    # ---- CTA: caixa escura chapada, cresce para caber o ES
    bx0, by0, bx1, by1 = cta['caixa']
    escuro = cor_fundo(im, (bx0 + 2, by0 + 2, bx0 + 8, by1 - 2))
    tc = tipo_calibrado(cta['cap'], 'TOQUE EM SAIBA MAIS', cta['larg_pt'])
    preencher(im, cta['caixa'], escuro)
    w = tc.getlength(CTA_ES)
    folga_x = cta['x_txt'] - bx0
    acento = -tc.getbbox('Á', anchor='ls')[1] - cta['cap']  # quanto o acento sobe acima da caixa-alta
    base = cta['base']
    nova = (int((bx0 + bx1) / 2 - w / 2 - folga_x), int(by0 - acento), int((bx0 + bx1) / 2 + w / 2 + folga_x), by1)
    nova = (min(nova[0], bx0), nova[1], max(nova[2], bx1), nova[3])
    preencher(im, nova, escuro)
    escrever_bloco(im, [CTA_ES], tc, (255, 255, 255), (bx0 + bx1) / 2, base, 0)
    print(os.path.basename(saida), 'cta caixa', nova)
    return salvar(im, saida)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ads01('trabalho/ads01-feed.png', 'FEA-Ads 01 - PTO-LATAM - Feed.png',
          dict(caixa=(167, 580, 906, 904), cap=45, linha_pt='76% DE DESCONTO PARA INJETORES O', larg_pt=638,
               passo=59.25, centro_y=(601 + 879) / 2, larg_max=692, n_linhas=5),
          dict(caixa=(329, 936, 735, 1001), cap=47, larg_pt=379, x_txt=342, base=994))
    ads01('trabalho/ads01-story.png', 'FEA-Ads 01 - PTO-LATAM - Story.png',
          dict(caixa=(148, 987, 930, 1619), cap=65, linha_pt='INJETORES O PROCEDIMENTO', larg_pt=725,
               passo=88, centro_y=(1006 + 1598) / 2, larg_max=740, n_linhas=7),
          dict(caixa=(241, 1672, 841, 1769), cap=61, larg_pt=559, x_txt=262, base=1750))
