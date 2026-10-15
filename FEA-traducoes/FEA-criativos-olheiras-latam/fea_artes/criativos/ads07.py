#!/usr/bin/env python3
"""FEA · Ads 07 (Ebook Olheiras) em espanhol LATAM, Feed e Story.

Fundo degradê com textura: texto PT apagado com inpainting clássico (apagar).
Linhas idênticas em ES ficam intactas ("TRIDIMENSIONAL" e "48 horas .").
Fontes (identificadas por sobreposição de máscara): título Manrope ExtraBold,
chamada Red Hat Display ExtraBold, corpo e CTA Instrument Sans.
Caixa do CTA (fundo chapado com borda de 1 px) é repintada e alargada se precisar.
Rodar a partir de fea_artes/:  python3 criativos/ads07.py
Originais: trabalho/pto07-feed.png (Drive 1YhACYv-Euv7JpTPJGC_P0HldYrJHm2RV)
           trabalho/pto07-story.png (Drive 1sfIUcxMXZOBE6E4eaT1Zk_t0cpoGgs_a)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

TIT = fonte('Manrope_800ExtraBold')
CHAMADA = fonte('RedHatDisplay_800ExtraBold')
CORPO = fonte('InstrumentSans_400Regular')
CORPO_DEST = fonte('InstrumentSans_600SemiBold')
LARANJA_TXT = lambda r, g, b: (r > 150) & (r - b > 60)
CLARO_TXT = lambda r, g, b: (r + g + b) > 240
CAIXA_FUNDO = (25, 27, 26)
CAIXA_BORDA = (85, 85, 85)

CORPO_PT = ['É o tempo que você tem para garantir', 'o seu eBook PreenchimentoTridimensional',
            'de Olheiras: Um Guia Completo com a', 'Metodologia ARTI, com desconto!']
CORPO_ES = ['Es el tiempo que tiene para obtener', 'su ebook Relleno tridimensional de ojeras:',
            'una guía completa con la metodología', 'ARTI, con descuento.']


def larg(f, s):
    l, _, r, _ = f.getbbox(s)
    return r - l


def centro(im, texto, f, cx, y, cor):
    l, _, r, _ = f.getbbox(texto)
    ImageDraw.Draw(im).text((cx - (r - l) / 2 - l, y), texto, font=f, fill=cor)


def ads07(arq, M):
    im = abrir(arq)
    W = im.width
    cx = W / 2
    # 1) título laranja: só linhas 1 e 3 mudam (fonte calibrada pela linha 2, que fica intacta)
    t1, t2, t3 = M['tit']
    cor_tit = cor_texto(im, (t2[2], t2[0], t2[3] + 1, t2[1] + 1), LARANJA_TXT)
    f = calibrar(TIT, 'TRIDIMENSIONAL', t2[3] - t2[2])
    for (yt, yb, x0, x1), pt, es in [(t1, 'PREENCHIMENTO', 'RELLENO'), (t3, 'DE OLHEIRAS', 'DE OJERAS')]:
        im = apagar(im, (x0 - 8, yt - 5, x1 + 9, yb + 6), LARANJA_TXT, 2)
        centro(im, es, f, cx, yt - f.getbbox(pt)[1], cor_tit)
    # 2) "Ou menos." -> "O menos."
    yt, yb, x0, x1 = M['menos']
    cor = cor_texto(im, (x0, yt, x1 + 1, yb + 1), CLARO_TXT)
    f = calibrar(CHAMADA, 'Ou menos.', x1 - x0)
    im = apagar(im, (x0 - 10, yt - 6, x1 + 11, yb + 8), CLARO_TXT, 3)
    centro(im, 'O menos.', f, cx, yt - f.getbbox('Ou menos.')[1], cor)
    # 3) corpo (4 linhas centralizadas)
    caixa = (min(m[2] for m in M['corpo']) - 10, M['corpo'][0][0] - 8, max(m[3] for m in M['corpo']) + 11, M['corpo'][-1][1] + 12)
    cor = cor_texto(im, caixa, CLARO_TXT)
    i = max(range(4), key=lambda k: M['corpo'][k][3] - M['corpo'][k][2])
    f = calibrar(CORPO, CORPO_PT[i], M['corpo'][i][3] - M['corpo'][i][2])
    lim = W - 2 * 70
    while max(larg(f, s) for s in CORPO_ES) > lim:
        f = ImageFont.truetype(CORPO, f.size - 0.5)
    im = apagar(im, caixa, CLARO_TXT, 3)
    # origem de cada linha = mesma do PT; a linha 1 começa com 'É' (acento muda o topo),
    # então usa o passo regular das linhas 2 a 4
    ys = [yt - f.getbbox(pt)[1] for pt, (yt, yb, x0, x1) in zip(CORPO_PT, M['corpo'])]
    ys[0] = ys[1] - (ys[2] - ys[1])
    for es, y in zip(CORPO_ES, ys):
        centro(im, es, f, cx, y, cor)
    # 4) CTA na caixa: "TOQUE EN MÁS INFORMACIÓN" / "Y OBTENGA SU ACCESO"
    bx0, by0, bx1, by1 = M['caixa']   # coordenadas da borda de 1 px
    c1, c2 = M['cta']
    cor_l = cor_texto(im, (c1[2], c1[0], c1[3] + 1, c1[1] + 1), LARANJA_TXT)
    f = calibrar(CORPO, 'E LIBERE O SEU ACESSO', c2[3] - c2[2])
    fd = ImageFont.truetype(CORPO_DEST, f.size)
    a, b = 'TOQUE EN ', 'MÁS INFORMACIÓN'
    w1 = f.getlength(a) + larg(fd, b) + fd.getbbox(b)[0]
    folga = c2[2] - bx0
    w = max(w1, larg(f, 'Y OBTENGA SU ACCESO'))
    if w + 2 * folga > bx1 - bx0:
        nx0 = int(cx - (w / 2 + folga))
        nx1 = int(cx + (w / 2 + folga))
    else:
        nx0, nx1 = bx0, bx1
    d = ImageDraw.Draw(im)
    d.rectangle([nx0, by0, nx1, by1], fill=CAIXA_FUNDO, outline=CAIXA_BORDA, width=1)
    y1 = c1[0] - f.getbbox('TOQUE EM SAIBA MAIS')[1]
    x = cx - w1 / 2 - f.getbbox(a)[0]
    d.text((x, y1), a, font=f, fill=(255, 255, 255))
    d.text((x + f.getlength(a), y1), b, font=fd, fill=cor_l)
    centro(im, 'Y OBTENGA SU ACCESO', f, cx, c2[0] - f.getbbox('E LIBERE O SEU ACESSO')[1], (255, 255, 255))
    return im


# medidas (y_topo, y_base, x0, x1) via medir() nos originais
FEED = dict(tit=[(144, 171, 384, 695), (179, 206, 386, 691), (215, 241, 422, 658)],
            menos=(412, 489, 291, 803),
            corpo=[(553, 594, 232, 848), (607, 634, 184, 891), (654, 688, 223, 853), (700, 734, 259, 818)],
            caixa=(308, 779, 767, 891), cta=[(798, 832, 344, 741), (841, 868, 340, 746)])
STORY = dict(tit=[(528, 559, 359, 721), (569, 600, 361, 717), (610, 641, 403, 678)],
             menos=(840, 931, 251, 848),
             corpo=[(1005, 1053, 180, 899), (1068, 1099, 125, 950), (1122, 1162, 170, 904), (1178, 1217, 212, 865)],
             caixa=(270, 1269, 806, 1400), cta=[(1290, 1330, 311, 775), (1340, 1372, 306, 782)])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for arq, M, nome in [('trabalho/pto07-feed.png', FEED, 'FEA-Ads 07 - PTO-LATAM - Feed.png'),
                         ('trabalho/pto07-story.png', STORY, 'FEA-Ads 07 - PTO-LATAM - Story.png')]:
        im = ads07(arq, M)
        print('ok', salvar(im, nome), im.size)
        previa(im, 'trabalho/pto07-es-' + ('feed' if 'Feed' in nome else 'story') + '-prev.jpg')
