#!/usr/bin/env python3
"""FEA · Ads 08 (Ebook Olheiras) em espanhol LATAM, Feed e Story.

Texto sobre a área escura da foto, alinhado à esquerda: apagado com inpainting
clássico (apagar), sem IA generativa. Fontes identificadas: título Arimo Bold
(laranja), parágrafos e CTA Montserrat (SemiBold e Regular), preço Arimo Regular.
Caixa de preço laranja com caixa preta interna: refeita do tamanho do texto ES
(PRECOS['de_200'] riscado + PRECOS['preco']), limitada para não invadir o rosto.
Copy oficial ES troca os travessões do PT por parênteses.
Rodar a partir de fea_artes/:  python3 criativos/ads08.py
Originais: trabalho/pto08-feed.png (Drive 1U0Mv9Lxz5aZnDFRPIo5tlN5wgQVlKdyk)
           trabalho/pto08-story.png (Drive 18V6vlx9UR5DsBFQo7a74Z69yjzXVkV0k)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

TIT = fonte('Arimo_700Bold')
NEG = fonte('Montserrat_600SemiBold')
REG = fonte('Montserrat_400Regular')
PRECO = fonte('Arimo_400Regular')
LARANJA = (253, 184, 84)
ESCURO = (11, 11, 11)
TXT = lambda r, g, b: ((r + g + b) > 330) | ((r > 150) & (r - b > 60))
LAR = lambda r, g, b: (r > 150) & (r - b > 60)

NEG_PT = ['Domine o procedimento mais', 'desafiador da harmonização', 'facial — o preenchimento de',
          'olheiras — com a metodologia', 'ARTI, e alcance resultados', 'naturais, seguros e duradouros.']
# (texto, laranja?) por linha; a parte laranja termina em "facial", como no original
NEG_ES = [[('Domine el procedimiento más', 1)], [('desafiante de la armonización', 1)],
          [('facial', 1), (' (el relleno de ojeras) con', 0)], [('la metodología ARTI y logre', 0)],
          [('resultados naturales, seguros y', 0)], [('duraderos.', 0)]]
REG_PT = ['Este guia revela como aplicar a', 'metodologia ARTI — Anatomia,', 'Reologia, Técnica e Intercorrências',
          '— no preenchimento de olheiras,', 'a região mais delicada da face,', 'conquistando resultados superiores',
          'onde a maioria falha.']
REG_ES = ['Esta guía muestra cómo aplicar la', 'metodología ARTI (Anatomía,', 'Reología, Técnica e Intercurrencias)',
          'en el relleno de ojeras, la región', 'más delicada del rostro, para', 'obtener resultados superiores',
          'donde la mayoría falla.']
CTA_PT = ['Toque em SAIBA MAIS', 'e garanta o seu desconto']


def origens(f, pts, tops):
    """Origem y de cada linha (mesma linha de base do PT), suavizada por ajuste linear do entrelinhas."""
    ys = np.array([t - f.getbbox(p)[1] for p, t in zip(pts, tops)], float)
    i = np.arange(len(ys))
    a, b = np.polyfit(i, ys, 1)
    return [b + a * k for k in i]


def ads08(arq, M):
    im = abrir(arq)
    s = M['escala']
    # 1) título: linhas 1 e 3 (TRIDIMENSIONAL fica intacta), centradas no eixo do bloco
    t1, t2, t3 = M['tit']
    cor_t = cor_texto(im, (t2[2], t2[0], t2[3] + 1, t2[1] + 1), LAR)
    f = calibrar(TIT, 'TRIDIMENSIONAL', t2[3] - t2[2])
    cx = (t2[2] + t2[3]) / 2
    d = ImageDraw.Draw(im)
    for (yt, yb, x0, x1), pt, es in [(t1, 'PREENCHIMENTO', 'RELLENO'), (t3, 'DE OLHEIRAS', 'DE OJERAS')]:
        im = apagar(im, (x0 - 6, yt - 5, x1 + 7, yb + 6), LAR, 2)
        l, _, r, _ = f.getbbox(es)
        ImageDraw.Draw(im).text((cx - (r - l) / 2 - l, yt - f.getbbox(pt)[1]), es, font=f, fill=cor_t)

    # 2) caixa de preço: apaga a caixa antiga inteira e redesenha
    bx0, by0, bx1, by1 = M['caixa']
    ix0, iy0, ix1, iy1 = M['interna']
    tx0, ty0, tx1, ty1 = M['txt_caixa']
    px0, py0, px1, py1 = M['txt_preco']
    a = np.array(im)
    m = np.zeros(a.shape[:2], np.uint8)
    m[by0 - 2:by1 + 3, bx0 - 2:bx1 + 3] = 255
    im = Image.fromarray(cv2.cvtColor(cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, 5, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
    fc0 = calibrar(REG, 'DE R$ 200 POR', tx1 - tx0)
    fp0 = calibrar(PRECO, 'R$ 97,00', px1 - px0)
    pad_l, gap, ipad_l, ipad_r, pad_r = tx0 - bx0, ix0 - tx1, px0 - ix0, ix1 - px1, bx1 - ix1
    a1, a2, a3 = 'DE ', PRECOS['de_200'], ' A'
    k = 1.0
    while True:
        fc = ImageFont.truetype(REG, fc0.size * k)
        fp = ImageFont.truetype(PRECO, fp0.size * k)
        wt = fc.getlength(a1 + a2 + a3)
        wp = fp.getbbox(PRECOS['preco'])[2] - fp.getbbox(PRECOS['preco'])[0]
        larg = pad_l + wt + gap + ipad_l + wp + ipad_r + pad_r
        if bx0 + larg <= M['limite_x'] or k < 0.4:
            break
        k -= 0.01
    nbx1 = int(round(bx0 + larg))
    nix0 = int(round(bx0 + pad_l + wt + gap))
    nix1 = nbx1 - pad_r
    d = ImageDraw.Draw(im)
    d.rectangle([bx0, by0, nbx1 - 1, by1 - 1], fill=LARANJA)
    d.rectangle([nix0, iy0, nix1, iy1], fill=ESCURO)
    # linha de base do texto da caixa e do preço: mesma do original, centro vertical mantido se a fonte encolheu
    cap0 = fc0.getbbox('D')[3] - fc0.getbbox('D')[1]
    base_c = M['base_caixa'] - (1 - k) * cap0 / 2
    capp = fp0.getbbox('R')[3] - fp0.getbbox('R')[1]
    base_p = M['base_preco'] - (1 - k) * capp / 2
    x = bx0 + pad_l - fc.getbbox(a1)[0]
    d.text((x, base_c), a1 + a2 + a3, font=fc, fill=ESCURO, anchor='ls')
    xa = x + fc.getlength(a1)
    xb = xa + fc.getlength(a2.rstrip())
    cap = fc.getbbox('D', anchor='ls')
    ym = base_c + cap[1] * 0.42
    esp = max(2, round(3 * s * k))
    d.rectangle([xa, ym - esp / 2, xb, ym + esp / 2 - 1], fill=ESCURO)
    l, _, r, _ = fp.getbbox(PRECOS['preco'])
    d.text(((nix0 + nix1) / 2 - (r - l) / 2 - l, base_p), PRECOS['preco'], font=fp, fill=(255, 255, 255), anchor='ls')

    # 3) parágrafo em negrito (laranja até "facial", depois branco)
    tops = M['neg']
    fb = calibrar(NEG, 'ARTI, e alcance resultados', M['neg_ref'])
    cor_b = cor_texto(im, (M['x'], tops[-1], M['x'] + 400, tops[-1] + int(30 * s)), lambda r, g, b: (r + g + b) > 500)
    cor_o = cor_texto(im, (M['x'], tops[0], M['x'] + 400, tops[0] + int(30 * s)), LAR)
    im = apagar(im, (M['x'] - 8, tops[0] - 10, M['x1_neg'], tops[-1] + int(45 * s)), TXT, 3)
    d = ImageDraw.Draw(im)
    for segs, y in zip(NEG_ES, origens(fb, NEG_PT, tops)):
        x = M['x'] - fb.getbbox(segs[0][0])[0]
        for txt, lar in segs:
            d.text((x, y), txt, font=fb, fill=cor_o if lar else cor_b)
            x += fb.getlength(txt)

    # 4) parágrafo regular
    tops = M['reg']
    fr = calibrar(REG, 'a região mais delicada da face,', M['reg_ref'])
    cor_r = cor_texto(im, (M['x'], tops[0], M['x'] + 400, tops[-1] + int(25 * s)), lambda r, g, b: (r + g + b) > 500)
    im = apagar(im, (M['x'] - 8, tops[0] - 10, M['x1_reg'], tops[-1] + int(35 * s)), TXT, 3)
    d = ImageDraw.Draw(im)
    for es, y in zip(REG_ES, origens(fr, REG_PT, tops)):
        d.text((M['x'] - fr.getbbox(es)[0], y), es, font=fr, fill=cor_r)

    # 5) CTA: "Toque en MÁS INFORMACIÓN" / "y asegure su descuento"
    c1, c2 = M['cta']
    fcr = calibrar(REG, CTA_PT[1], c2[3] - c2[2])
    fcb = ImageFont.truetype(NEG, fcr.size)
    cor_c = cor_texto(im, (c2[2], c2[0], c2[3] + 1, c2[1] + 1), lambda r, g, b: (r + g + b) > 500)
    cor_cl = cor_texto(im, (c1[2], c1[0], c1[3] + 1, c1[1] + 1), LAR)
    im = apagar(im, (M['x'] - 8, c1[0] - 8, max(c1[3], c2[3]) + 10, c2[1] + 10), TXT, 3)
    d = ImageDraw.Draw(im)
    y1 = c1[0] - fcr.getbbox(CTA_PT[0])[1]
    x = M['x'] - fcr.getbbox('Toque')[0]
    d.text((x, y1), 'Toque en ', font=fcr, fill=cor_c)
    d.text((x + fcr.getlength('Toque en '), y1), 'MÁS INFORMACIÓN', font=fcb, fill=cor_cl)
    d.text((M['x'] - fcr.getbbox('y')[0], c2[0] - fcr.getbbox(CTA_PT[1])[1]), 'y asegure su descuento', font=fcr, fill=cor_c)
    return im


FEED = dict(escala=1.0, x=72,
            tit=[(90, 112, 72, 332), (119, 142, 74, 329), (149, 171, 104, 301)],
            caixa=(67, 241, 510, 299), interna=(352, 249, 501, 293), txt_caixa=(80, 256, 336, 284),
            txt_preco=(360, 254, 490, 287), base_caixa=282, base_preco=283, limite_x=615,
            neg=[342, 382, 422, 462, 502, 542], neg_ref=437, x1_neg=605,
            reg=[619, 652, 684, 717, 749, 781, 814], reg_ref=398, x1_reg=548,
            cta=[(890, 915, 72, 396), (926, 951, 72, 429)])
STORY = dict(escala=1.167, x=75,
             tit=[(466, 492, 75, 379), (501, 527, 77, 376), (536, 561, 112, 343)],
             caixa=(69, 644, 587, 712), interna=(402, 653, 577, 705), txt_caixa=(85, 662, 384, 695),
             txt_preco=(419, 661, 563, 697), base_caixa=692, base_preco=693, limite_x=650,
             neg=[763, 808, 855, 902, 949, 997], neg_ref=510, x1_neg=690,
             reg=[1086, 1124, 1162, 1199, 1238, 1276, 1312], reg_ref=466, x1_reg=630,
             cta=[(1403, 1431, 75, 453), (1443, 1472, 75, 491)])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for arq, M, nome in [('trabalho/pto08-feed.png', FEED, 'FEA-Ads 08 - PTO-LATAM - Feed.png'),
                         ('trabalho/pto08-story.png', STORY, 'FEA-Ads 08 - PTO-LATAM - Story.png')]:
        im = ads08(arq, M)
        print('ok', salvar(im, nome), im.size)
        previa(im, 'trabalho/pto08-es-' + ('feed' if 'Feed' in nome else 'story') + '-prev.jpg')
