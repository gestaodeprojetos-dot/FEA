#!/usr/bin/env python3
"""[FEED] ADS 04.jpg e [STORIES] ADS 04.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Originais em trabalho/Jads04-feed.jpg e trabalho/Jads04-story.jpg
(Drive 1rLBELyMJpQagh0UEqivvqrOQBax3cLRB e 1itU4M9hs1BCuq0HPHdPGal5fLHoVxOS3).
Story = título e corpo do feed deslocados 45 px para baixo (caixa com barra dourada na mesma altura), mais a faixa CTA dourada.
Capa do ebook (mockup em português) intacta: fase 2.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads04.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_jpg_util import *  # noqa

VERDE = (51, 148, 69)
TEXTO = lambda r, g, b: ((r + g + b) < 620) & (b <= g + 8)   # texto verde/escuro, exclui o terno azul


def recompor(orig, dy, saida, cta=None, dyb=0):
    im = abrir(orig)
    # ---------- título (Noto Serif) ----------
    cx = (110, 120 + dy, 672, 392 + dy)
    escuro = cor_texto(im, (120, 300 + dy, 540, 375 + dy), lambda r, g, b: (r + g + b) < 300)
    im = apagar(im, cx, TEXTO, 3)
    fr = F('NotoSerif_400Regular', 62.0)
    fi = F('NotoSerif_400Regular_Italic', 62.0)
    b1 = base_de(fr, 'Você estudou…', 134 + dy)
    b2 = base_de(fi, 'mas na hora de', 225 + dy)
    b3 = base_de(fi, 'aplicar, trava?', 310 + dy)
    linha(im, 121, b1, [('Usted estudió…', fr, VERDE)])
    linha(im, 124, b2, [('pero, a la hora de', fi, escuro)])
    # 3a linha: no máximo até x 660 (faixa dourada começa em 677)
    f3 = fi
    while f3.getlength('aplicar, ¿se bloquea?') > 660 - 123:
        f3 = F('NotoSerif_400Regular_Italic', f3.size - 0.5)
    linha(im, 123, b3, [('aplicar, ¿se bloquea?', f3, escuro)])
    # ---------- corpo (Open Sans Regular) ----------
    cx = (110, 395 + dy, 545, 530 + dy)
    corpo = cor_texto(im, cx, lambda r, g, b: (r + g + b) < 300)
    im = apagar(im, cx, TEXTO, 3)
    fo = F('OpenSans_400Regular', 32.5)
    b = base_de(fo, 'Aqui você aprende o', 402 + dy)
    for i, t in enumerate(['Aquí aprende lo que', 'realmente importa:', 'una ejecución segura.']):
        linha(im, 121, b + 43 * i, [(t, fo, corpo)])
    # ---------- caixa com barra dourada (Open Sans Bold + Regular, verde-escuro) ----------
    cx = (145, 628 + dyb, 545, 770 + dyb)
    vesc = cor_texto(im, (150, 635 + dyb, 300, 660 + dyb), lambda r, g, b: (r + g + b) < 300)
    im = apagar(im, cx, TEXTO, 3)
    fb = F('OpenSans_700Bold', 24.0)
    fn = F('OpenSans_400Regular', 24.0)
    b = base_de(fb, 'EBOOK COM', 637 + dyb)
    linhas = [[('EBOOK CON', fb, vesc)], [('DEMOSTRACIÓN', fb, vesc)],
              [('PRÁCTICA', fb, vesc), (' Y DECISIONES', fn, vesc)], [('CLÍNICAS EXPLICADAS.', fn, vesc)]]
    for i, segs in enumerate(linhas):
        linha(im, 153, b + 33 * i, segs)
    # ---------- CTA dourado (só story) ----------
    if cta:
        x0, y0, x1, y1 = cta
        ouro = cor_fundo(im, (x0 + 4, y0 + 4, x0 + 20, y1 - 4))
        txt = cor_texto(im, cta, lambda r, g, b: (r + g + b) < 200)
        preencher(im, cta, ouro)
        fc = F('OpenSans_700Bold', 26.0)
        es = 'TOQUE EN MÁS INFORMACIÓN Y ASEGURE EL SUYO.'
        while fc.getlength(es) > (x1 - x0) - 46 and fc.size > 26 * 0.85:
            fc = F('OpenSans_700Bold', fc.size - 0.25)
        alargar_caixa(im, cta, ouro, fc.getlength(es), 23)
        base = base_de(F('OpenSans_700Bold', 26.0), 'TOQUE EM SAIBA MAIS', 1551)
        # mantém o centro vertical do texto
        base += (F('OpenSans_700Bold', 26.0).getbbox('T', anchor='ls')[1] - fc.getbbox('T', anchor='ls')[1]) / 2
        linha(im, (x0 + x1) / 2, base, [(es, fc, txt)], 'centro')
    print(salvar(im, saida))
    return im


if __name__ == '__main__':
    recompor('trabalho/Jads04-feed.jpg', 0, 'FEA-[FEED] ADS 04 - LATAM.jpg')
    recompor('trabalho/Jads04-story.jpg', 45, 'FEA-[STORIES] ADS 04 - LATAM.jpg', cta=(241, 1520, 839, 1592))
