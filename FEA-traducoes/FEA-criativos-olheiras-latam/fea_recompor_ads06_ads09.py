#!/usr/bin/env python3
"""Recompõe as artes Ads 06 e Ads 09 (Ebook Olheiras) em espanhol.

Troca única e exclusivamente a copy: apaga o texto original com inpainting
clássico (OpenCV Telea, sem IA generativa) e escreve a tradução na mesma
fonte, no mesmo tamanho (calibrado pela largura do texto original), na mesma
cor e na mesma linha de base. Foto, preço e layout ficam intactos.

    python3 fea_recompor_ads06_ads09.py PASTA_ARTES PASTA_FONTES

PASTA_ARTES precisa ter ads06-feed.png, ads06-story.png, ads09-feed.png e
ads09-story.png (originais do Drive Brasil). Saída: FEA-ES-*.png na mesma pasta.
"""
import glob, os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ARTES, FONTES = sys.argv[1], sys.argv[2]


def fonte(nome):
    return glob.glob(os.path.join(FONTES, '**', nome), recursive=True)[0]


ROBOTO_LIGHT = fonte('Roboto_300Light.ttf')
ROBOTO_COND_BOLD = fonte('RobotoCondensed_700Bold.ttf')
MONT_SEMI = fonte('Montserrat_600SemiBold.ttf')
MONT_BOLD = fonte('Montserrat_700Bold.ttf')
FONTE_PRECO = fonte('Montserrat_300Light.ttf')


def calibrar(caminho, texto, largura):
    """Tamanho de fonte em que o texto original ocupa a largura medida na arte."""
    melhor = None
    for t in np.arange(10, 140, 0.25):
        f = ImageFont.truetype(caminho, float(t))
        l, _, r, _ = f.getbbox(texto)
        if melhor is None or abs((r - l) - largura) < abs(melhor[1] - largura):
            melhor = (float(t), r - l)
    return ImageFont.truetype(caminho, melhor[0])


def apagar(im, caixa, cond, dil=3):
    """Inpainting só nos pixels de texto dentro da caixa."""
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    sub = a[y0:y1, x0:x1].astype(int)
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = cond(sub[..., 0], sub[..., 1], sub[..., 2]).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(bgr, m, 6, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def cor_texto(im, caixa, cond):
    a = np.array(im)[caixa[1]:caixa[3], caixa[0]:caixa[2]].astype(int)
    m = cond(a[..., 0], a[..., 1], a[..., 2])
    px = a[m]
    lum = px.sum(1)
    claro = np.median(lum) > 382
    sel = px[lum >= np.percentile(lum, 60)] if claro else px[lum <= np.percentile(lum, 40)]
    return tuple(int(v) for v in np.median(sel, 0))


def escrever(d, linhas_pt, linhas_es, medidas, caminho, cor):
    """medidas: [(y_topo, x0, x1)] de cada linha original. Mantém centro e linha de base."""
    i_larga = max(range(len(medidas)), key=lambda i: medidas[i][2] - medidas[i][1])
    f = calibrar(caminho, linhas_pt[i_larga], medidas[i_larga][2] - medidas[i_larga][1])
    for pt, es, (ytop, x0, x1) in zip(linhas_pt, linhas_es, medidas):
        _, t_pt, _, _ = f.getbbox(pt)
        y = ytop - t_pt  # origem que reproduz o topo medido do original = mesma linha de base
        l, _, r, _ = f.getbbox(es)
        cx = (x0 + x1) / 2
        d.text((cx - (r - l) / 2 - l, y), es, font=f, fill=cor)
    return f


def alargar_caixa(im, caixa, cor, largura_texto, folga):
    x0, y0, x1, y1 = caixa
    precisa = largura_texto + 2 * folga
    if precisa <= x1 - x0:
        return caixa
    cx = (x0 + x1) / 2
    nova = (int(cx - precisa / 2), y0, int(cx + precisa / 2), y1)
    ImageDraw.Draw(im).rectangle([nova[0], y0, nova[2], y1 - 1], fill=cor)
    return nova


CLARO = lambda r, g, b: (r > 150) & (g > 150) & (b > 150)
ESCURO = lambda r, g, b: (r < 110) & (g < 110) & (b < 110)
CTA_PT = ['CLIQUE E GARANTA', 'O SEU DESCONTO']
CTA_ES = ['HAGA CLIC Y ASEGURE', 'SU DESCUENTO']


def ads06(nome, corpo, cta_caixa, cta_med):
    im = Image.open(os.path.join(ARTES, nome)).convert('RGB')
    # corpo sobre a foto
    caixa = (min(m[1] for m in corpo) - 12, corpo[0][0] - 8, max(m[2] for m in corpo) + 12, corpo[-1][0] + 70)
    caixa = (caixa[0], caixa[1], caixa[2], min(caixa[3], cta_caixa[1] - 4))
    cor = cor_texto(im, caixa, CLARO)
    im = apagar(im, caixa, CLARO, 3)
    escrever(ImageDraw.Draw(im), ['É isso que te separa de', 'dominar o preenchimento', 'tridimensional de olheiras.'],
             ['Es lo que lo separa de', 'dominar el relleno', 'tridimensional de ojeras.'], corpo, ROBOTO_LIGHT, cor)
    # CTA verde (caixa sólida)
    verde = tuple(int(v) for v in np.median(np.array(im)[cta_caixa[1] + 3:cta_caixa[1] + 8, cta_caixa[0] + 3:cta_caixa[2] - 3].reshape(-1, 3), 0))
    ImageDraw.Draw(im).rectangle([cta_caixa[0], cta_caixa[1], cta_caixa[2] - 1, cta_caixa[3] - 1], fill=verde)
    f = calibrar(ROBOTO_COND_BOLD, CTA_PT[0], cta_med[0][2] - cta_med[0][1])
    l, _, r, _ = f.getbbox(CTA_ES[0])
    folga = cta_med[0][1] - cta_caixa[0]
    alargar_caixa(im, cta_caixa, verde, r - l, folga)
    escrever(ImageDraw.Draw(im), CTA_PT, CTA_ES, cta_med, ROBOTO_COND_BOLD, (255, 255, 255))
    return im


def ads09(nome, dx, dy):
    im = Image.open(os.path.join(ARTES, nome)).convert('RGB')
    S = lambda c: (c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy)
    M = lambda ms: [(y + dy, x0 + dx, x1 + dx) for y, x0, x1 in ms]
    # caixa escura semitransparente
    cx = S((90, 300, 646, 400))
    cor = cor_texto(im, cx, CLARO)
    im = apagar(im, cx, CLARO, 3)
    escrever(ImageDraw.Draw(im), ['Aprenda o preenchimento', 'tridimensional de olheiras.'],
             ['Aprenda el relleno', 'tridimensional de ojeras.'], M([(314, 108, 626), (358, 109, 628)]), MONT_SEMI, cor)
    # caixa laranja
    cx = S((50, 429, 671, 525))
    cor = cor_texto(im, cx, ESCURO)
    im = apagar(im, cx, ESCURO, 3)
    escrever(ImageDraw.Draw(im), ['eBook Preenchimento', 'Tridimensional de Olheiras:'],
             ['Ebook Relleno', 'tridimensional de ojeras:'], M([(437, 118, 605), (486, 65, 656)]), MONT_SEMI, cor)
    # linha 'De R$ 200 por' na caixa branca inclinada (texto Montserrat Light quase preto + risco vermelho)
    a = np.array(im).astype(int)
    px0, py0, px1, py1 = S((178, 565, 575, 619))  # só o miolo da caixa, sem o fundo escuro dos cantos
    sub = a[py0:py1, px0:px1]
    escuro = (sub.sum(2) < 380) & (abs(sub[..., 0] - sub[..., 2]) < 30)
    vermelho = (sub[..., 0] > 180) & (sub[..., 1] < 140)
    cor_txt = tuple(int(v) for v in np.median(sub[escuro & (sub.sum(2) < 200)], 0))
    cor_verm = tuple(int(v) for v in np.median(sub[vermelho & (sub[..., 1] < 90)], 0))
    vy, vx = np.where(vermelho)
    inc = np.polyfit(vx, vy, 1)[0]
    ang = np.degrees(np.arctan(inc))
    ys, xs = np.where(escuro)
    esq, dir_ = xs.min() + px0, xs.max() + px0
    colD = ys[xs < xs.min() + 6]  # base do 'D' = linha de base no início da frase
    base_esq = colD.max() + py0
    im = apagar(im, (px0, py0, px1, py1), lambda r, g, b: ((r + g + b) < 600) | ((r > 180) & (g < 160)), 2)
    f = calibrar(FONTE_PRECO, 'De R$ 200 por', (dir_ - esq) / np.cos(np.radians(ang)))
    camada = Image.new('RGBA', (900, 300), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    ox, oy = 150, 120
    dc.text((ox, oy), 'De R$ 200 a', font=f, fill=cor_txt + (255,), anchor='ls')  # origem na linha de base
    xa = ox + f.getlength('De ')
    xb = ox + f.getlength('De R$ 200')
    _, t, _, _ = f.getbbox('R$ 200', anchor='ls')
    ym = oy + t * 0.45
    dc.line([(xa - f.size * 0.15, ym), (xb + f.size * 0.25, ym)], fill=cor_verm + (255,), width=max(2, round(f.size / 13)))
    l0 = f.getbbox('D', anchor='ls')[0]
    piv = (ox + l0, oy)
    rot = camada.rotate(-ang, resample=Image.BICUBIC, center=piv)
    im.paste(rot, (int(round(esq - piv[0])), int(round(base_esq - piv[1]))), rot)
    # CTA branco sólido
    cc = S((182, 744, 549, 833))
    branco = (247, 247, 247)
    ImageDraw.Draw(im).rectangle([cc[0], cc[1], cc[2] - 1, cc[3] - 1], fill=branco)
    med = M([(758, 196, 536), (797, 212, 519)])
    f = calibrar(MONT_BOLD, CTA_PT[0], med[0][2] - med[0][1])
    l, _, r, _ = f.getbbox(CTA_ES[0])
    alargar_caixa(im, cc, branco, r - l, 14)
    escrever(ImageDraw.Draw(im), CTA_PT, CTA_ES, med, MONT_BOLD, (0, 0, 0))
    return im, ang


saidas = {
    'FEA-ES-Ads 06 - PTO - Feed.png': ads06('ads06-feed.png', [(716, 329, 744), (771, 302, 769), (819, 298, 770)],
                                            (346, 903, 727, 1006), [(920, 361, 712), (965, 378, 694)]),
    'FEA-ES-Ads 06 - PTO - Story.png': ads06('ads06-story.png', [(1300, 273, 800), (1369, 240, 832), (1430, 233, 834)],
                                             (295, 1537, 778, 1668), [(1558, 314, 760), (1615, 335, 737)]),
}
for nome, (dx, dy) in {'FEA-ES-Ads 09 - PTO - Feed.png': (0, 0), 'FEA-ES-Ads 09 - PTO - Story.png': (-9, 414)}.items():
    img, ang = ads09('ads09-feed.png' if dy == 0 else 'ads09-story.png', dx, dy)
    print(nome, 'inclinação da caixa de preço: %.2f°' % ang)
    saidas[nome] = img
for nome, img in saidas.items():
    img.save(os.path.join(ARTES, nome), optimize=True)
    print('ok', nome, img.size)
