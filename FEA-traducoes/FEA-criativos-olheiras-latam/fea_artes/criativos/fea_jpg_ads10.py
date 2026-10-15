#!/usr/bin/env python3
"""FEA · [FEED] ADS 10 e [STORIES] ADS 10 (jpg, Ebook Olheiras) em espanhol LATAM. Lote G.

Troca só a copy (fundo preto chapado: texto apagado repintando de preto, faixas
amarelas e faixa verde do CTA redesenhadas na mesma cor e altura, largura ajustada ao ES).
Copy ES: ../FEA-copy-criativos-final.py. Preço: precos.json (de_297 riscado, preco).
Rodar a partir de fea_artes/:  python3 criativos/fea_jpg_ads10.py
Originais (Drive Brasil): trabalho/G-ads10-feed.jpg ([FEED] ADS 10.jpg 1FbdZ9y1ig4lZdiXca8koVJFCVkiqNA7F),
trabalho/G-ads10-story.jpg ([STORIES] ADS 10.jpg 1EJDhyb9OR8oMEVj-BEvVKmxeAcYcMq75).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads10a13 import *  # noqa
from fea_arte_lib import abrir, salvar, preencher, PRECOS
from PIL import ImageDraw

PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
AMARELO, VERDE_CTA = (239, 193, 107), (17, 54, 34)
VERMELHO, VERDE = (243, 23, 23), (36, 255, 75)
SERIF, REG, BOLD = 'NotoSerif_400Regular', 'OpenSans_400Regular', 'OpenSans_700Bold'

FAIXA_PT = ['Se você ainda depende de tentativa e', 'erro, você está em risco.']
FAIXA_ES = ['Si todavía depende del ensayo y', 'error, está en riesgo.']
APRENDA_PT = ['Aprenda um método seguro,', 'replicável e clínico.']
APRENDA_ES = ['Aprenda un método seguro,', 'replicable y clínico.']
EBOOK_PT = ['Ebook com passo a passo completo da', 'primeira avaliação ao resultado final.']
EBOOK_ES = ['Ebook con el paso a paso completo, desde la', 'primera evaluación hasta el resultado final.']
CTA_PT = 'TOQUE EM SAIBA MAIS E GARANTA O SEU.'
CTA_ES = 'TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO.'

# medidas do original (px): faixas = (caixa, x0_texto, x1_texto, topo_texto); blocos = (topo, x0, x1) por linha
MED = {
    'feed': dict(arq='G-ads10-feed.jpg', saida='FEA-[FEED] ADS 10 - LATAM.jpg',
                 faixas=[((161, 393, 891, 449), 171, 868, 408), ((276, 454, 776, 510), 293, 746, 462)],
                 aprenda=[(536, 249, 788), (590, 337, 701)], ebook=[(684, 253, 827), (728, 266, 814)],
                 preco=dict(topo_De=884, x_apenas=(530, 635), centro=520, area=(300, 875, 740, 925)),
                 cta=dict(caixa=(262, 973, 818, 1018), cap=17, topo=990, x=(273, 806))),
    'story': dict(arq='G-ads10-story.jpg', saida='FEA-[STORIES] ADS 10 - LATAM.jpg',
                  faixas=[((60, 560, 993, 631), 72, 965, 580), ((207, 638, 846, 709), 228, 808, 650)],
                  aprenda=[(744, 171, 862), (814, 285, 750)], ebook=[(934, 178, 912), (989, 194, 896)],
                  preco=dict(topo_De=1189, x_apenas=(532, 667), centro=519, area=(240, 1175, 800, 1240)),
                  cta=dict(caixa=(189, 1303, 900, 1360), cap=22, topo=1324, x=(203, 886))),
}
LARG_MAX = 960  # tinta máxima de uma linha (60 px de margem em cada lado)


def bloco(im, pt, es, med, nome_fonte, cor):
    """Apaga (preto) e reescreve linhas centradas, mantendo a linha de base de cada linha."""
    i = max(range(len(pt)), key=lambda k: med[k][2] - med[k][1])
    f = calib(nome_fonte, pt[i], med[i][2] - med[i][1] + 1)
    while max(largura_spans([(s, f, cor)]) for s in es) > LARG_MAX:
        f = F(nome_fonte, f.size - 0.25)
    for (topo, x0, x1) in med:
        preencher(im, (x0 - 12, topo - 14, x1 + 13, topo + int(f.size * 1.05)), PRETO)
    for s_pt, s_es, (topo, x0, x1) in zip(pt, es, med):
        desenhar_spans(im, [(s_es, f, cor)], base_de(f, s_pt, topo), centro=(x0 + x1) / 2)
    return f


def gerar(fmt):
    M = MED[fmt]
    im = abrir(os.path.join('trabalho', M['arq']))
    d = ImageDraw.Draw(im)

    # 1. faixas amarelas (texto preto, Noto Serif); cada faixa mantém as folgas do original
    _, a1, b1, _ = M['faixas'][0]
    f = calib(SERIF, FAIXA_PT[0], b1 - a1 + 1)
    centro = (a1 + b1) / 2
    for cx, *_ in M['faixas']:
        preencher(im, (cx[0] - 4, cx[1] - 4, cx[2] + 4, cx[3] + 4), PRETO)  # inclui a borda suavizada do jpg
    for (cx, x0, x1, topo), s_pt, s_es in zip(M['faixas'], FAIXA_PT, FAIXA_ES):
        pad_e, pad_d = x0 - cx[0], cx[2] - x1
        base = base_de(f, s_pt, topo)
        w = largura_spans([(s_es, f, PRETO)])
        d.rectangle([round(centro - w / 2 - pad_e), cx[1], round(centro + w / 2 + pad_d) - 1, cx[3] - 1], fill=AMARELO)
        desenhar_spans(im, [(s_es, f, PRETO)], base, centro=centro)

    # 2. "Aprenda..." (Noto Serif branco) e 3. "Ebook..." (Open Sans branco)
    bloco(im, APRENDA_PT, APRENDA_ES, M['aprenda'], SERIF, BRANCO)
    bloco(im, EBOOK_PT, EBOOK_ES, M['ebook'], REG, BRANCO)

    # 4. preço: De [riscado vermelho] a solo [verde negrito]; Bold = 0,96 do Regular (medido no feed)
    P = M['preco']
    fl = calib(REG, 'apenas', P['x_apenas'][1] - P['x_apenas'][0] + 1)
    fv = F(BOLD, fl.size * 0.96)
    base = base_de(fl, 'De', P['topo_De'])
    preencher(im, P['area'], PRETO)

    def spans():
        return [('De ', fl, BRANCO), (PRECOS['de_297'], fl, VERMELHO, VERMELHO), (' a solo ', fl, BRANCO), (PRECOS['preco'], fv, VERDE)]
    while largura_spans(spans()) > LARG_MAX:
        fl, fv = F(REG, fl.size - 0.25), F(BOLD, fv.size - 0.25)
    desenhar_spans(im, spans(), base, centro=P['centro'])

    # 5. CTA (Open Sans Bold branco com entreletra, faixa verde-escura alargada)
    C = M['cta']
    fc = por_altura_maiuscula(BOLD, C['cap'])
    tr = entreletra(fc, CTA_PT, C['x'][1] - C['x'][0] + 1)
    cx = C['caixa']
    preencher(im, (cx[0] - 4, cx[1] - 4, cx[2] + 4, cx[3] + 4), PRETO)
    pad = ((C['x'][0] - cx[0]) + (cx[2] - C['x'][1])) / 2
    w = largura_spans([(CTA_ES, fc, BRANCO, None, tr)])
    while w + 2 * pad > 1080 - 2 * 40:
        fc = F(BOLD, fc.size - 0.25)
        w = largura_spans([(CTA_ES, fc, BRANCO, None, tr)])
    centro = (C['x'][0] + C['x'][1]) / 2
    d.rectangle([round(centro - w / 2 - pad), cx[1], round(centro + w / 2 + pad) - 1, cx[3] - 1], fill=VERDE_CTA)
    desenhar_spans(im, [(CTA_ES, fc, BRANCO, None, tr)], C['topo'] + C['cap'], centro=centro)

    print('ok', salvar(im, M['saida']), im.size)
    return im


if __name__ == '__main__':
    for fmt in MED:
        gerar(fmt)
