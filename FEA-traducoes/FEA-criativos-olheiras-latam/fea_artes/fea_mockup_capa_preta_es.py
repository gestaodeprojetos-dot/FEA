#!/usr/bin/env python3
"""Ads 37 e 39: o mockup do livro de capa PRETA (letras prateadas) traz o título em português.
fea_mockup_capa_es.py foi feito para a capa verde com letras douradas e, na capa preta,
deixava o título rosado e o subtítulo vermelho; por isso ele agora ignora capa sem cor
e este script cuida dela. Sem IA generativa.

Como funciona: no painel de cima da capa (entre a moldura e a primeira divisória) as
linhas do título e do subtítulo são medidas no original, o texto é apagado por
inpainting clássico (o filete do meio fica) e o título ES entra em Arimo Bold (métrica da
Helvetica Bold) com a mesma altura de caixa alta, e o subtítulo em Playfair Display
Italic com "ARTI" em redondo, como no original. O prateado é o do próprio original:
o brilho das letras antigas, suavizado, vira o brilho das letras novas.
Rodar depois de fea_mockup_capa_es.py (rodar_todos.py chama no final).
"""
import os
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys

AQ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQ)
from fea_arte_lib import fonte

SAIDA = os.path.join(os.path.dirname(AQ), 'FEA-artes-ES')
ARIMO = fonte('Arimo_700Bold')
PF_IT = fonte('PlayfairDisplay_600SemiBold_Italic')
PF = fonte('PlayfairDisplay_600SemiBold')
TIT_PT = ['PREENCHIMENTO', 'TRIDIMENSIONAL', 'DE OLHEIRAS']
TIT_ES = ['RELLENO', 'TRIDIMENSIONAL', 'DE OJERAS']
SUB_PT = [('Um Guia Completo com a Metodologia ', PF_IT), ('ARTI', PF)]
SUB_ES = [('Una Guía Completa con la Metodología ', PF_IT), ('ARTI', PF)]
X0, X1 = 40, 368           # miolo do painel (dentro da moldura prateada)
# topo do miolo do painel em cada arte (linha logo abaixo da moldura de cima)
ALVOS = [('Jads37-feed.png', 'FEA-Ads 37 Feed - PTO-LATAM.png', 1342),
         ('Jads37-story.png', 'FEA-Ads 37 Story - PTO-LATAM.png', 1878),
         ('Jads39-feed.png', 'FEA-Ads 39 Feed - PTO-LATAM.png', 875),
         ('Jads39-story.png', 'FEA-Ads 39 Story - PTO-LATAM.png', 1351)]
ALT = 164                   # altura do miolo do painel


def faixas(m):
    r = np.where(m.any(1))[0]
    gr = []
    for y in r:
        if gr and y - gr[-1][1] <= 1:
            gr[-1][1] = y
        else:
            gr.append([y, y])
    return gr


def larg_runs(runs, tam):
    return sum(ImageFont.truetype(p, tam).getlength(t) for t, p in runs)


def painel_es(P):
    g = cv2.cvtColor(P, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m = g > 70
    linhas = faixas(m)
    tit = [l for l in linhas if l[1] - l[0] >= 18][:3]
    fil = [l for l in linhas if l[1] - l[0] <= 2]
    sub = [l for l in linhas if 8 <= l[1] - l[0] < 18 and l[0] > tit[-1][1]]
    assert len(tit) == 3 and fil and sub, linhas
    sub = sub[0]
    # brilho das letras antigas (normalizado) para pintar as novas
    let = (m & ~np.isin(np.arange(P.shape[0]), range(fil[0][0], fil[0][1] + 1))[:, None]).astype(np.float32)
    brilho = cv2.GaussianBlur(g * let, (0, 0), 14) / (cv2.GaussianBlur(let, (0, 0), 14) + 1e-3)
    # apagar título e subtítulo (filete fica)
    apaga = np.zeros(m.shape, np.uint8)
    for a, b in tit + [sub]:
        apaga[max(0, a - 3):b + 4] = (g[max(0, a - 3):b + 4] > 28)
    apaga = cv2.dilate(apaga, np.ones((3, 3), np.uint8))
    base = cv2.inpaint(P, apaga * 255, 4, cv2.INPAINT_TELEA)
    # máscara do texto ES, renderizada em 4x e reduzida (antisserrilhado)
    K = 4
    H, W = P.shape[:2]
    mk = Image.new('L', (W * K, H * K), 0)
    d = ImageDraw.Draw(mk)
    cx = W * K / 2
    # corpo pela largura: "TRIDIMENSIONAL" é igual nas duas línguas, então o ES fica com a
    # mesma largura da linha do meio original (a fonte original é um pouco mais estreita)
    xs2 = np.where(m[tit[1][0]:tit[1][1] + 1].any(0))[0]
    s = 6
    while ImageFont.truetype(ARIMO, (s + 1) * K).getlength('TRIDIMENSIONAL') <= (xs2.max() - xs2.min() + 1) * K:
        s += 1
    f = ImageFont.truetype(ARIMO, s * K)
    lmax = (X1 - X0 - 22) * K
    while max(f.getlength(t) for t in TIT_ES) > lmax:
        f = ImageFont.truetype(ARIMO, f.size - 1)
    for (a, b), t in zip(tit, TIT_ES):
        d.text((cx - f.getlength(t) / 2, (b + 1) * K), t, font=f, fill=255, anchor='ls')
    # subtítulo: mesmo corpo que reproduz a largura do PT; se o ES não couber, reduz
    xs = np.where(m[sub[0]:sub[1] + 1].any(0))[0]
    alvo = (xs.max() - xs.min() + 1) * K
    tam = 8 * K
    while larg_runs(SUB_PT, tam + 1) <= alvo:
        tam += 1
    while larg_runs(SUB_ES, tam) > lmax:
        tam -= 1
    # linha de base: a do original (fundo das letras sem descendente)
    base_y = (sub[0] + 0.78 * (sub[1] - sub[0] + 1)) * K
    x = cx - larg_runs(SUB_ES, tam) / 2
    for t, p in SUB_ES:
        ft = ImageFont.truetype(p, tam)
        d.text((x, base_y), t, font=ft, fill=255, anchor='ls')
        x += ft.getlength(t)
    al = np.array(mk.resize((W, H), Image.LANCZOS), np.float32)[..., None] / 255
    cor = np.clip(brilho * 1.12, 110, 235)[..., None]
    out = base.astype(np.float32) * (1 - al) + cor * al
    return np.clip(out, 0, 255).astype(np.uint8), s, tam / K


if __name__ == '__main__':
    for orig, saida, y0 in ALVOS:
        o = cv2.imread(os.path.join(AQ, 'trabalho', orig))
        ps = os.path.join(SAIDA, saida)
        arte = cv2.imread(ps)
        if o is None or arte is None:
            print('ausente', orig, saida)
            continue
        P = o[y0:y0 + ALT, X0:X1]
        novo, s, st = painel_es(P)
        arte[y0:y0 + ALT, X0:X1] = novo
        cv2.imwrite(ps, arte)
        print('capa preta ES', saida, 'título', s, 'subtítulo %.1f' % st)
