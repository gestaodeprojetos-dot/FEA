#!/usr/bin/env python3
"""FEA · Ads 09 (Feed e Story) em espanhol LATAM. Troca só a copy.

Originais em trabalho/ads09-feed.png e trabalho/ads09-story.png (Drive Brasil).
Preço lido de precos.json (PRECOS['de_200'] riscado, PRECOS['preco'] em vermelho).
Rodar a partir de fea_artes/:  python3 criativos/ads09.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

MONT_SEMI = fonte('Montserrat_600SemiBold')
MONT_BOLD = fonte('Montserrat_700Bold')
MONT_LIGHT = fonte('Montserrat_300Light')
MONT_PRECO = fonte('Montserrat_800ExtraBold')
CTA_PT = ['CLIQUE E GARANTA', 'O SEU DESCONTO']
CTA_ES = ['HAGA CLIC Y ASEGURE', 'SU DESCUENTO']


def escrever_linhas(im, pt, es, medidas, caminho):
    """Calibra pela linha PT mais larga e mantém centro e linha de base de cada linha."""
    d = ImageDraw.Draw(im)
    i = max(range(len(medidas)), key=lambda k: medidas[k][2] - medidas[k][1])
    f = calibrar(caminho, pt[i], medidas[i][2] - medidas[i][1])
    for p, e, (ytop, x0, x1) in zip(pt, es, medidas):
        y = ytop - f.getbbox(p)[1]
        l, _, r, _ = f.getbbox(e)
        d.text(((x0 + x1) / 2 - (r - l) / 2 - l, y), e, font=f, fill=cor)
    return f


def tamanho_cap(caminho, letra, altura):
    for s in np.arange(10, 200, 0.25):
        f = ImageFont.truetype(caminho, float(s))
        if -f.getbbox(letra, anchor='ls')[1] >= altura:
            return f
    return f


def caixa_preco(im, dx, dy):
    """Caixa branca inclinada: 'De <de_200> a' (Light, riscado) + preço vermelho grande."""
    a = np.array(im).astype(int)
    # inclinação pelo risco vermelho da 1ª linha
    px0, py0, px1, py1 = 178 + dx, 565 + dy, 575 + dx, 619 + dy
    sub = a[py0:py1, px0:px1]
    verm = (sub[..., 0] > 180) & (sub[..., 1] < 140)
    vy, vx = np.where(verm)
    ang = np.degrees(np.arctan(np.polyfit(vx, vy, 1)[0]))
    C = (380 + dx, 640 + dy)
    reto = np.array(im.rotate(ang, center=C, resample=Image.BICUBIC)).astype(int)
    # medidas no quadro endireitado
    box = reto[548 + dy:722 + dy]
    linha_branca = np.where(box[box.shape[0] // 2].sum(1) > 690)[0]
    linha_branca = linha_branca[(linha_branca > 100 + dx) & (linha_branca < 700 + dx)]
    bx0, bx1 = int(linha_branca.min()), int(linha_branca.max())
    s1 = reto[550 + dy:625 + dy, bx0:bx1]
    dk = (s1.sum(2) < 380) & (abs(s1[..., 0] - s1[..., 2]) < 30)
    ys, xs = np.where(dk)
    l1_x0, l1_x1 = xs.min() + bx0, xs.max() + bx0
    l1_base = ys[xs < xs.min() + 5].max() + 550 + dy
    cor_txt = tuple(int(v) for v in np.median(s1[dk & (s1.sum(2) < 200)], 0))
    rv = (s1[..., 0] > 180) & (s1[..., 1] < 90)
    cor_verm_risco = tuple(int(v) for v in np.median(s1[rv], 0))
    s2 = reto[612 + dy:720 + dy, bx0:bx1]
    red = (s2[..., 0] > 180) & (s2[..., 1] < 100) & (s2[..., 2] < 100)
    ys, xs = np.where(red)
    p_x0, p_x1 = xs.min() + bx0, xs.max() + bx0
    p_base = ys[xs < xs.min() + 12].max() + 612 + dy  # base do 'R'
    p_cap = p_base - ys[xs < xs.min() + 12].min() - 612 - dy + 1
    cor_preco = tuple(int(v) for v in np.median(s2[red & (s2[..., 1] < 40)], 0))

    # apagar: 1ª linha (texto escuro + risco) e preço vermelho, só dentro do miolo branco
    cond1 = lambda r, g, b: ((r + g + b) < 600) | ((r > 180) & (g < 160))
    im = apagar(im, (px0, py0, px1, py1), cond1, 2)
    cond2 = lambda r, g, b: (r > 150) & (r - g > 40)
    im = apagar(im, (bx0 + 25 + dx * 0, 600 + dy, bx1 - 15, 722 + dy), cond2, 3)
    # o apagar acima é retangular no quadro original; a caixa só tem branco + vermelho nessa faixa

    margem = 36
    larg_max = (bx1 - bx0) - 2 * margem
    cx_box = (bx0 + bx1) / 2

    camada = Image.new('RGBA', im.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)

    # linha 1: Montserrat Light calibrada pela largura do original, reduzida só se não couber
    f1 = calibrar(MONT_LIGHT, 'De R$ 200 por', l1_x1 - l1_x0)
    ant = PRECOS['de_200']
    t1 = f'De {ant} a'
    while f1.getlength(t1) > larg_max and f1.size > 10:
        f1 = ImageFont.truetype(MONT_LIGHT, f1.size - 0.5)
    w1 = f1.getbbox(t1, anchor='ls')
    x1 = cx_box - (w1[2] - w1[0]) / 2 - w1[0]
    dc.text((x1, l1_base), t1, font=f1, fill=cor_txt + (255,), anchor='ls')
    xa = x1 + f1.getlength('De ')
    xb = x1 + f1.getlength('De ' + ant)
    t = f1.getbbox(ant, anchor='ls')[1]
    ym = l1_base + t * 0.45
    dc.line([(xa - f1.size * 0.15, ym), (xb + f1.size * 0.25, ym)], fill=cor_verm_risco + (255,),
            width=max(2, round(f1.size / 13)))

    # preço: Montserrat ExtraBold pela altura do 'R', estreitada na mesma proporção do original
    fp = tamanho_cap(MONT_PRECO, 'R', p_cap)
    bb = fp.getbbox('R$ 97,00', anchor='ls')
    sx = (p_x1 - p_x0 + 1) / (bb[2] - bb[0])
    preco = PRECOS['preco']
    bp = fp.getbbox(preco, anchor='ls')
    wl = int(bp[2] - bp[0] + 20)
    hl = int(fp.size * 1.6)
    tmp = Image.new('RGBA', (wl, hl), (0, 0, 0, 0))
    base_tmp = int(fp.size * 1.15)
    ImageDraw.Draw(tmp).text((10 - bp[0], base_tmp), preco, font=fp, fill=cor_preco + (255,), anchor='ls')
    escala = sx
    if (bp[2] - bp[0]) * escala > larg_max:  # placeholder longo: reduz por inteiro, proporcional
        red_f = larg_max / ((bp[2] - bp[0]) * escala)
    else:
        red_f = 1.0
    tmp = tmp.resize((max(1, round(wl * escala * red_f)), max(1, round(hl * red_f))), Image.LANCZOS)
    # linha de base mantida; centro na caixa
    larg_ink = (bp[2] - bp[0]) * escala * red_f
    ox = cx_box - larg_ink / 2 - 10 * escala * red_f
    oy = p_base - base_tmp * red_f
    camada.alpha_composite(tmp, (int(round(ox)), int(round(oy))))

    camada = camada.rotate(-ang, center=C, resample=Image.BICUBIC)
    out = im.convert('RGBA')
    out.alpha_composite(camada)
    return out.convert('RGB'), ang, f1.size, red_f


def ads09(nome, dx, dy):
    global cor
    im = abrir(os.path.join('trabalho', nome))
    S = lambda c: (c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy)
    M = lambda ms: [(y + dy, x0 + dx, x1 + dx) for y, x0, x1 in ms]
    # caixa escura semitransparente
    cx = S((90, 300, 646, 400))
    cor = cor_texto(im, cx, CLARO)
    im = apagar(im, cx, CLARO, 3)
    escrever_linhas(im, ['Aprenda o preenchimento', 'tridimensional de olheiras.'],
                    ['Aprenda el relleno', 'tridimensional de ojeras.'], M([(314, 108, 626), (358, 109, 628)]), MONT_SEMI)
    # caixa laranja
    cx = S((50, 429, 671, 525))
    cor = cor_texto(im, cx, ESCURO)
    im = apagar(im, cx, ESCURO, 3)
    escrever_linhas(im, ['eBook Preenchimento', 'Tridimensional de Olheiras:'],
                    ['Ebook Relleno', 'tridimensional de ojeras:'], M([(437, 118, 605), (486, 65, 656)]), MONT_SEMI)
    # caixa de preço inclinada
    im, ang, t1, red_f = caixa_preco(im, dx, dy)
    # CTA branco sólido
    cc = S((182, 744, 549, 833))
    branco = (247, 247, 247)
    preencher(im, cc, branco)
    med = M([(758, 196, 536), (797, 212, 519)])
    f = calibrar(MONT_BOLD, CTA_PT[0], med[0][2] - med[0][1])
    l, _, r, _ = f.getbbox(CTA_ES[0])
    alargar_caixa(im, cc, branco, r - l, 14)
    cor = (0, 0, 0)
    escrever_linhas(im, CTA_PT, CTA_ES, med, MONT_BOLD)
    print(nome, 'inclinação %.2f°, fonte linha 1 %.1f, redução preço %.0f%%' % (ang, t1, (1 - red_f) * 100))
    return im


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for saida, (orig, dx, dy) in {'FEA-Ads 09 - PTO-LATAM - Feed.png': ('ads09-feed.png', 0, 0),
                                  'FEA-Ads 09 - PTO-LATAM - Story.png': ('ads09-story.png', -9, 412)}.items():
        print('ok', salvar(ads09(orig, dx, dy), saida))
