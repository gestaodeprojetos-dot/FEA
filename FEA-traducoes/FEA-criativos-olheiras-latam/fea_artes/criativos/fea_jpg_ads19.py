#!/usr/bin/env python3
"""[FEED] ADS 19 (jpg) em espanhol LATAM. Troca só a copy; livro (mockup, fase 2), fundo e layout intactos.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads19.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

ORIG = 'trabalho/ads19-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 19 - LATAM.jpg'

ESCURO = lambda r, g, b: (r + g + b) < 420
OURO = lambda r, g, b: (r > 130) & (r - b > 55) & (g < 225)
BRANCO = lambda r, g, b: (r > 190) & (g > 190) & (b > 170)
MARROM = lambda r, g, b: ((r + g + b) < 360) & (r > b + 10)
TIT = 'Gelasio_600SemiBold'
SANS, SANS_B = 'NotoSans_400Regular', 'NotoSans_700Bold'
SANS_SB = 'NotoSans_600SemiBold'
CTA_G, CTA_W = 'PTSerif_700Bold', 'PTSerif_400Regular'


def gerar():
    im0 = abrir(ORIG)
    im = im0.copy()

    # título: 'Seja referência' / 'em olheiras' -> 'Conviértase en' / 'referente en ojeras'
    verde = cor_nucleo(im0, (83, 82, 688, 178), ESCURO, 30)
    grad = grad_rel(im0, (232, 191, 550, 266), OURO)
    im = apagar(im, (66, 70, 715, 190), ESCURO, 3, 6)
    im = apagar(im, (66, 186, 575, 278), lambda r, g, b: ESCURO(r, g, b) | OURO(r, g, b), 3, 6)
    pt1 = 'Seja referência'
    tt = tam_por_largura(lambda s: [(pt1, TIT, s, verde)], 688 - 83)
    b1, b2 = 156, 266  # linhas de base medidas ('S' da linha 1; 'em olheiras' não tem descendente)
    # L1 cabe acima do livro e à esquerda do selo; L2 curta para o 'j' não invadir o topo do livro (y~270, x>598)
    seg1 = lambda s: [('Conviértase en referente', TIT, s, verde)]
    t1 = caber(seg1, tt, 1095 - 83, 0.15)
    linha(im, seg1(t1), b1, 83)
    seg2 = lambda s: [('en ', TIT, s, verde), ('ojeras', TIT, s, ('grad', grad, b2 - (266 - 191) * s / tt, b2))]
    t2 = t1
    linha(im, seg2(t2), b2, 79)

    # pílula verde: 'por R$97' -> 'por US$ [PRECIO]'
    branco = cor_nucleo(im0, (109, 356, 235, 399), BRANCO, 50, escuro=False)
    grad_p = grad_rel(im0, (261, 315, 516, 409), OURO)
    im = apagar(im, (100, 305, 534, 420), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    t_por = tam_por_largura(lambda s: [('por', TIT, s, branco)], 235 - 109)
    t_pre = tam_por_cap('Gelasio_700Bold', 399 - 320, 'R')
    moeda, valor = dividir_preco(PRECOS['preco'])
    k = 1.0
    while True:
        segs = [('por ', TIT, t_por * max(0.62, min(1, k * 1.35)), branco),
                (moeda + ' ' + valor, 'Gelasio_700Bold', t_pre * k, ('grad', grad_p, 399 - 79 * (1 + k) / 2, 399 - 79 * (1 - k) / 2))]
        if largura_segs(segs) <= 524 - 104 or k < 0.35:
            break
        k -= 0.01
    linha(im, segs, 399 - 79 * (1 - k) / 2, (82 + 545) / 2, 'centro')  # pílula vai de x~82 a x~545
    k_preco = k

    # parágrafo
    cor_p = cor_nucleo(im0, (79, 534, 445, 563), ESCURO, 30)
    im = apagar(im, (66, 522, 588, 740), ESCURO, 3, 6)
    tp = tam_por_largura(lambda s: [('Transforme essa área', SANS, s, cor_p)], 445 - 79)
    passo = 53
    bp = base_de(SANS, tp, 'complicada em um grande', 587) - passo
    L = [[('Convierta esta área', SANS)], [('complicada en un gran', SANS)],
         [('diferencial', SANS_SB), (' en la', SANS_SB)], [('armonización facial', SANS_SB)]]
    for i, sg in enumerate(L):
        linha(im, [(x, n, tp, cor_p) for x, n in sg], bp + passo * i, 80)

    # lista
    cor_l = cor_nucleo(im0, (234, 831, 400, 861), ESCURO, 30)
    im = apagar(im, (225, 822, 588, 915), ESCURO, 3, 6)
    im = apagar(im, (225, 988, 588, 1078), ESCURO, 3, 6)
    tb = tam_por_largura(lambda s: [('de 30 mil', SANS_B, s, cor_l)], 400 - 234)
    tr_ = tam_por_largura(lambda s: [('cópias vendidas', SANS, s, cor_l)], 467 - 235)
    linha(im, [('+30 mil', SANS_B, tb, cor_l)], base_de(SANS_B, tb, 'de 30 mil', 831), 234)
    linha(im, [('copias vendidas', SANS, tr_, cor_l)], base_de(SANS, tr_, 'cópias vendidas', 877), 235)
    linha(im, [('Casos reales', SANS_B, tb, cor_l)], base_de(SANS_B, tb, 'Casos reais', 996), 235)
    linha(im, [('analizados', SANS, tr_, cor_l)], base_de(SANS, tr_, 'analisados', 1046), 235)

    # selo dourado: 'de 30 mil' -> '+30 mil' (o '30 mil' original fica), 'cópias' -> 'copias'
    marrom = cor_nucleo(im0, (1021, 262, 1059, 296), MARROM, 30)
    im = apagar(im, (990, 266, 1017, 291), MARROM, 2, 4)
    # '+' com a altura do 'de' (x-height ~17 px), centrado na mesma faixa vertical
    tmais = tam_por_cap('Gelasio_700Bold', 19, '+')
    fm_ = F('Gelasio_700Bold', tmais)
    _, tp_, _, bp_ = fm_.getbbox('+', anchor='ls')
    linha(im, [('+', 'Gelasio_700Bold', tmais, marrom)], 278.5 - (tp_ + bp_) / 2, 1015, 'direita')
    im = apagar(im, (996, 298, 1004, 303), lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 185, 0, 2)

    # CTA: 'SAIBA MAIS' (dourado) 'SOBRE ESSE MÉTODO' (branco)
    grad_c = grad_rel(im0, (342, 1207, 614, 1245), OURO)
    branco_c = cor_nucleo(im0, (638, 1216, 963, 1239), BRANCO, 50, escuro=False)
    im = apagar(im, (330, 1198, 980, 1252), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    tg = tam_por_largura(lambda s: [('SAIBA MAIS', CTA_G, s, branco_c)], 614 - 342)
    tw = tam_por_largura(lambda s: [('SOBRE ESSE MÉTODO', CTA_W, s, branco_c)], 963 - 638)
    seg = lambda s: [('CONOZCA MÁS', CTA_G, s, ('grad', grad_c, 1207, 1245)), (' SOBRE ESTE MÉTODO', CTA_W, tw * s / tg, branco_c)]
    LIM = 1010 - 342
    tg2 = caber(seg, tg, LIM, 0.15)
    w = largura_segs(seg(tg2))
    x_ini = 342 if 342 + w <= 1010 else 1010 - w
    x0, x1 = linha(im, seg(tg2), 1245, x_ini)

    p = salvar(im, SAIDA_NOME)
    print('ok', p, im.size, 'titulo L2 %.1f->%.1f' % (tt, t2), 'preco k %.2f' % k_preco, 'cta %.1f->%.1f fim %.0f' % (tg, tg2, x1))


if __name__ == '__main__':
    gerar()
