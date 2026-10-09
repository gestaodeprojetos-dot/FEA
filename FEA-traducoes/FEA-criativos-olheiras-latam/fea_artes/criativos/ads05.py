#!/usr/bin/env python3
"""FEA · Ads 05 (Ebook Olheiras) em espanhol LATAM, Feed e Story.

Fundo chapado (16,16,16): o texto PT é apagado repintando o fundo (preencher),
sem inpainting. Emoji ✅ é recortado do original e reposicionado (não redesenhado).
Fontes identificadas: título Roboto SemiBold; demais blocos EB Garamond Regular.
Preço: PRECOS['de_200'] riscado em vermelho e PRECOS['preco'] em verde.
Rodar a partir de fea_artes/:  python3 criativos/ads05.py
Originais: trabalho/pto05-feed.png (Drive 1BJmhWAmX2ZrNNKZonrCPY5MlJyWmtmZe)
           trabalho/pto05-story.png (Drive 1A-Bke14HHbVaOD-HA0EFLNdrbFeOP93y)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

TITULO = fonte('Roboto_600SemiBold')
SERIFA = fonte('EBGaramond_400Regular')
FUNDO = (16, 16, 16)
BRANCO = (239, 239, 239)
VERMELHO = (255, 31, 35)
VERDE = (0, 191, 9)
MARGEM = 60  # nenhuma linha encosta na borda

T_PT = ['eBook Preenchimento Tridimensional', 'de Olheiras: Um Guia Completo', 'com a Metodologia ARTI']
T_ES = ['Ebook Relleno tridimensional', 'de ojeras: una guía completa', 'con la metodología ARTI']


def tam(f, s):
    l, _, r, _ = f.getbbox(s)
    return r - l


def caber(caminho, f, textos, largura):
    """Reduz a fonte só se alguma linha passar da largura útil."""
    while max(tam(f, s) for s in textos) > largura and f.size > 8:
        f = ImageFont.truetype(caminho, f.size - 0.5)
    return f


def linha(im, segs, f, cx, y):
    """segs = [(texto, cor)] numa linha centralizada em cx; y = origem do texto (mesma do PT).
    Devolve [(x_ini, x_fim)] de cada segmento."""
    d = ImageDraw.Draw(im)
    tudo = ''.join(s for s, _ in segs)
    l, _, r, _ = f.getbbox(tudo)
    x = cx - (r - l) / 2 - l
    pos = []
    for s, cor in segs:
        d.text((x, y), s, font=f, fill=cor)
        pos.append((x + f.getbbox(s)[0], x + f.getbbox(s)[2]))
        x += f.getlength(s)
    return pos


def ads05(arq, M):
    im = abrir(arq)
    W = im.width
    cx = W / 2
    # emoji ✅: recorta antes de repintar
    ey0, ey1 = M['s1'][0] - 4, M['s1'][1] + 4
    emoji = im.crop((M['emoji'][0] - 2, ey0, M['emoji'][1] + 2, ey1))
    gap_emoji = M['s1_txt'] - M['emoji'][1]
    # repinta todo o miolo de texto (fundo chapado)
    preencher(im, (0, M['t'][0][0] - 20, W, M['c'][1][1] + 25), FUNDO)

    # 1) título (Roboto SemiBold, 3 linhas centralizadas, linha de base de cada linha PT)
    f = calibrar(TITULO, T_PT[0], M['t'][0][3] - M['t'][0][2])
    f = caber(TITULO, f, T_ES, W - 2 * MARGEM)
    for pt, es, (yt, yb, x0, x1) in zip(T_PT, T_ES, M['t']):
        linha(im, [(es, BRANCO)], f, cx, yt - f.getbbox(pt)[1])

    # 2) ✅ Aprenda el relleno / tridimensional de ojeras (EB Garamond)
    f = calibrar(SERIFA, 'tridimensional de olheiras', M['s2'][3] - M['s2'][2])
    pt1, es1 = 'Aprenda o preenchimento', 'Aprenda el relleno'
    # origem da linha 1: alinhar o topo do 'A' do original (topo medido do texto, não do emoji)
    y1 = M['s1_top_txt'] - f.getbbox(pt1)[1]
    larg = emoji.width - 4 + gap_emoji + tam(f, es1)
    x_emoji = cx - larg / 2
    im.paste(emoji, (int(round(x_emoji - 2)), ey0))
    ImageDraw.Draw(im).text((x_emoji + emoji.width - 4 + gap_emoji - f.getbbox(es1)[0], y1), es1, font=f, fill=BRANCO)
    linha(im, [('tridimensional de ojeras', BRANCO)], f, cx, M['s2'][0] - f.getbbox('tridimensional de olheiras')[1])

    # 3) preço: "De <riscado>" / "a solo <verde>"
    f0 = calibrar(SERIFA, 'Por apenas R$ 97,00', M['p2'][3] - M['p2'][2])
    l1 = [('De ', BRANCO), (PRECOS['de_200'], VERMELHO)]
    l2 = [('a solo ', BRANCO), (PRECOS['preco'], VERDE)]
    f = caber(SERIFA, f0, [''.join(s for s, _ in l1), ''.join(s for s, _ in l2)], W - 2 * MARGEM)
    k = f.size / f0.size
    oy1 = M['p1'][0] - f0.getbbox('De R$200,00')[1]   # origem original (fonte calibrada)
    oy2 = M['p2'][0] - f0.getbbox('Por apenas R$ 97,00')[1]
    risco_rel = (M['risco'][0] + M['risco'][1]) / 2 - oy1  # altura do risco acima da origem
    # se a fonte encolheu, mantém a linha de base (origem + ascent) e escala o risco
    base1 = oy1 + f0.getmetrics()[0]
    base2 = oy2 + f0.getmetrics()[0]
    y1 = base1 - f.getmetrics()[0]
    y2 = base2 - f.getmetrics()[0]
    pos = linha(im, l1, f, cx, y1)
    ym = base1 - (f0.getmetrics()[0] - risco_rel) * k
    esp = max(2, round((M['risco'][1] - M['risco'][0] + 1) * k))
    xa, xb = pos[1]
    ImageDraw.Draw(im).rectangle([xa - 0.02 * f.size, ym - esp / 2, xb + 0.02 * f.size, ym + esp / 2 - 1], fill=VERMELHO)
    linha(im, l2, f, cx, y2)

    # 4) CTA: "HAGA CLIC Y ASEGURE" (branco + verde) / "SU DESCUENTO" (verde)
    f = calibrar(SERIFA, 'CLIQUE E GARANTA', M['c'][0][3] - M['c'][0][2])
    linha(im, [('HAGA CLIC Y ', BRANCO), ('ASEGURE', VERDE)], f, cx, M['c'][0][0] - f.getbbox('CLIQUE E GARANTA')[1])
    linha(im, [('SU DESCUENTO', VERDE)], f, cx, M['c'][1][0] - f.getbbox('O SEU DESCONTO')[1])
    return im


# medidas (y_topo, y_base, x0, x1) tiradas com medir() nos originais
FEED = dict(t=[(120, 154, 202, 908), (173, 216, 262, 849), (226, 269, 323, 787)],
            s1=(337, 398), s1_top_txt=348, emoji=(247, 297), s1_txt=308,
            s2=(406, 445, 283, 794), p1=(539, 625), p2=(645, 729, 186, 893), risco=(578, 581),
            c=[(845, 883, 337, 741), (895, 924, 360, 718)])
STORY = dict(t=[(517, 553, 184, 928), (572, 618, 247, 865), (628, 674, 310, 799)],
             s1=(746, 809), s1_top_txt=757, emoji=(231, 283), s1_txt=295,
             s2=(818, 859, 268, 808), p1=(959, 1049), p2=(1074, 1158, 166, 889), risco=(1000, 1003),
             c=[(1281, 1321, 326, 751), (1334, 1364, 350, 727)])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for arq, M, nome in [('trabalho/pto05-feed.png', FEED, 'FEA-Ads 05 - PTO-LATAM - Feed.png'),
                         ('trabalho/pto05-story.png', STORY, 'FEA-Ads 05 - PTO-LATAM - Story.png')]:
        im = ads05(arq, M)
        print('ok', salvar(im, nome), im.size)
        previa(im, 'trabalho/pto05-es-' + ('feed' if 'Feed' in nome else 'story') + '-prev.jpg')
