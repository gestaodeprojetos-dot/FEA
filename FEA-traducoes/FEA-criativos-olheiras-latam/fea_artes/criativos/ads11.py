#!/usr/bin/env python3
"""FEA · Ads 11 (Feed e Story) em espanhol LATAM. Troca só a copy.

Originais em trabalho/C-ads11-feed.png e trabalho/C-ads11-story.png (Drive Brasil).
Fonte: Plus Jakarta Sans ExtraBold (mesma família do Ads 10).
Caixa laranja de preço levemente inclinada (cerca de 1,5°): é redesenhada no quadro
endireitado, alargada só se o preço em dólar não couber, e girada de volta.
Preço lido de precos.json: PRECOS['de_200'] (preço anterior) e PRECOS['preco'].
Rodar a partir de fea_artes/:  python3 criativos/ads11.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ads10 import *  # noqa: F401,F403  (fea_arte_lib + linha_cores, bloco_cores, ajustar, PJS, cores)

LARANJA_CAIXA = (252, 183, 83)
TIT_PT2 = ['Aprenda o preenchimento', 'tridimensional de olheiras ao dominar:']
TIT_ES2 = [[('Aprenda el relleno', BRANCO)], [('tridimensional de ojeras dominando:', BRANCO)]]
TIT_PT3 = ['Aprenda o preenchimento', 'tridimensional de olheiras', 'ao dominar:']
TIT_ES3 = [[('Aprenda el relleno', BRANCO)], [('tridimensional de ojeras', BRANCO)], [('dominando:', BRANCO)]]
LISTA_ES_B = [[('1.', LARANJA), (' Técnicas de inyección', BRANCO)],
              [('2.', LARANJA), (' Zonas de riesgo', BRANCO)],
              [('3.', LARANJA), (' Plano anatómico correcto', BRANCO)]]
PRECO_PT = ['De R$200,00', 'por apenas R$ 97,00']


def caixa_preco(im, C, ang, caixa, tops, larg_ref, raio, margem):
    """caixa e tops no quadro endireitado (im.rotate(-ang, center=C))."""
    es = [f"De {PRECOS['de_200']}", f"a solo {PRECOS['preco']}"]
    f = calibrar(PJS, PRECO_PT[1], larg_ref)
    x0, y0, x1, y1 = caixa
    cx = (x0 + x1) / 2
    larg_max_canvas = im.width - 2 * 60
    f = ajustar(f, PJS, es, larg_max_canvas - 2 * margem)  # só reduz se nem alargando couber
    larg_es = max(f.getbbox(s)[2] - f.getbbox(s)[0] for s in es)
    larg_caixa = max(x1 - x0, larg_es + 2 * margem)
    nx0, nx1 = cx - larg_caixa / 2 - 1, cx + larg_caixa / 2 + 1
    camada = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    # cantos arredondados só no superior direito e inferior esquerdo, como no original
    d.rounded_rectangle([nx0, y0 - 1, nx1, y1 + 1], radius=raio, fill=LARANJA_CAIXA + (255,),
                        corners=(False, True, False, True))
    for p, e, yt in zip(PRECO_PT, es, tops):
        l, _, r, _ = f.getbbox(e)
        d.text((cx - (r - l) / 2 - l, yt - f.getbbox(p)[1]), e, font=f, fill=PRETO + (255,))
    camada = camada.rotate(ang, center=C, resample=Image.BICUBIC)
    out = im.convert('RGBA')
    out.alpha_composite(camada)
    return out.convert('RGB'), larg_caixa - (x1 - x0), f.size


def bloco(im, rect, pt, es, tops, larg_ref, cx, pt_ref):
    im = apagar(im, rect, BRILHO, 3)
    f = calibrar(PJS, pt_ref, larg_ref)
    bloco_cores(im, pt, es, tops, f, cx)
    return im


def lista_b(im, rect, tops, larg_ref, cx):
    im = apagar(im, rect, BRILHO, 3)
    f = calibrar(PJS, LISTA_PT[2], larg_ref)
    f = ajustar(f, PJS, LISTA_ES_TXT, larg_ref)
    bloco_cores(im, LISTA_PT, LISTA_ES_B, tops, f, cx)
    return im


def feed():
    im = abrir('trabalho/C-ads11-feed.png')
    im, extra, t = caixa_preco(im, (541, 553), 1.5, (295, 508, 788, 627), [519, 574], 767 - 311 + 1, 30, 18)
    im = bloco(im, (150, 660, 935, 755), TIT_PT2, TIT_ES2, [670, 714], 917 - 167 + 1, 542, TIT_PT2[1])
    im = lista_b(im, (280, 780, 800, 905), [788, 829, 868], 778 - 303 + 1, 540.5)
    im = bloco(im, (340, 940, 745, 1020), CTA_PT, CTA_ES, [944, 984], 719 - 364 + 1, 541.5, CTA_PT[0])
    print('feed: caixa de preço alargada em %d px, fonte %.2f' % (extra, t))
    return im


def story():
    im = abrir('trabalho/C-ads11-story.png')
    im, extra, t = caixa_preco(im, (541, 982), 1.51, (190, 913, 892, 1083), [929, 1005], 868 - 212 + 1, 42, 22)
    im = bloco(im, (150, 1132, 935, 1323), TIT_PT3, TIT_ES3, [1142, 1205, 1268], 910 - 173 + 1, 542, TIT_PT3[0])
    im = lista_b(im, (180, 1361, 900, 1538), [1371, 1429, 1485], 878 - 201 + 1, 539.5)
    im = bloco(im, (260, 1584, 820, 1694), CTA_PT, CTA_ES, [1594, 1651], 794 - 286 + 1, 540, CTA_PT[0])
    print('story: caixa de preço alargada em %d px, fonte %.2f' % (extra, t))
    return im


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print('ok', salvar(feed(), 'FEA-Ads 11 - PTO-LATAM - Feed.png'))
    print('ok', salvar(story(), 'FEA-Ads 11 - PTO-LATAM - Story.png'))
