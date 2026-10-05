#!/usr/bin/env python3
"""[FEED] ADS 16 (jpg) em espanhol LATAM. Troca só a copy; fundo, ícones, faixas e botão intactos.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads16.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

ORIG = 'trabalho/ads16-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 16 - LATAM.jpg'

VERDE = lambda r, g, b: (g > r + 8) & (r < 110) & (g < 130)
VERDE_APAGAR = lambda r, g, b: ((r + g + b) < 560) & (g >= r) & (b < 200)
OURO = lambda r, g, b: (r > 120) & (r - b > 50) & (r < 240)
OURO_TXT = lambda r, g, b: (r > 100) & (r - b > 45) & (r < 215)
BRANCO = lambda r, g, b: (r > 150) & (g > 150) & (b > 130)
REG, BOLD, SEMI = 'Gelasio_400Regular', 'Gelasio_700Bold', 'Gelasio_600SemiBold'
CX = 540


def gerar():
    im0 = abrir(ORIG)
    im = im0.copy()

    # título: ATENCIÓN, (dourado) / PROFESIONALES DE LA / ARMONIZACIÓN (verde)
    grad_a = grad_rel(im0, (385, 144, 693, 189), OURO)
    verde_t = cor_nucleo(im0, (257, 215, 825, 254), VERDE, 50)
    im = apagar(im, (360, 136, 720, 212), OURO, 3, 6)
    im = apagar(im, (240, 208, 845, 337), VERDE_APAGAR, 3, 6)
    t1 = tam_por_cap(BOLD, 189 - 144, 'A')
    linha(im, [('ATENCIÓN,', BOLD, t1, ('grad', grad_a, 144, 189))], 189, CX, 'centro')
    t2 = tam_por_cap(BOLD, 254 - 212, 'P')
    linha(im, [('PROFESIONALES DE LA', BOLD, t2, verde_t)], 254, CX, 'centro')
    t3 = tam_por_cap(BOLD, 318 - 274, 'H')
    linha(im, [('ARMONIZACIÓN', BOLD, t3, verde_t)], 318, CX, 'centro')

    # faixa verde: 'Por apenas R$97,00 você recebe:' -> 'Por solo US$ [PRECIO] recibe:'
    branco = cor_nucleo(im0, (241, 400, 392, 432), BRANCO, 50, escuro=False)
    grad_p = grad_rel(im0, (416, 395, 656, 440), OURO)
    im = apagar(im, (228, 388, 856, 462), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    t_txt = tam_por_cap(REG, 426 - 403, 'P')
    t_pre = tam_por_cap(BOLD, 440 - 395, 'R')
    moeda, valor = dividir_preco(PRECOS['preco'])
    k = 1.0
    while True:
        segs = [('Por solo ', REG, t_txt, branco), (moeda + ' ' + valor, BOLD, t_pre * k, ('grad', grad_p, 440 - 45 * k, 440)),
                (' recibe:', REG, t_txt, branco)]
        if largura_segs(segs) <= 860 - 222 or k < 0.4:
            break
        k -= 0.01
    linha(im, segs, 440, CX, 'centro')
    k_preco = k

    # lista
    verde_l = cor_nucleo(im0, (308, 542, 653, 571), VERDE, 50)
    t = tam_por_largura(lambda s: [('preenchimento de olheiras', REG, s, verde_l)], 653 - 308)
    itens = [  # caixa a apagar, [(pt_ref para linha de base, y_topo, segmentos ES)]
        ((300, 498, 880, 582), [('Metodologia ARTI aplicado ao', 507, [('Metodología ', REG), ('ARTI', BOLD), (' aplicada al', REG)]),
                                ('preenchimento de olheiras', 542, [('relleno de ojeras', REG)])]),
        ((300, 645, 880, 684), [('passo a passo', 652, [('paso a paso', REG)])]),
        ((300, 703, 880, 780), [('Raciocínio clínico', 712, [('Razonamiento clínico', BOLD)]),
                                ('estruturado', 747, [('estructurado', REG)])]),
        ((300, 908, 880, 946), [('Videoaulas', 916, [('Videoclases', BOLD)])]),
    ]
    for caixa, linhas_ in itens:
        im = apagar(im, caixa, VERDE_APAGAR, 3, 6)
        for pt, yt, segs in linhas_:
            ref_nome = BOLD if pt in ('Raciocínio clínico', 'Videoaulas') else REG
            base = base_de(ref_nome, t, pt, yt)
            linha(im, [(s, n, t, verde_l) for s, n in segs], base, 308)

    # caixa clara: três linhas centradas, trechos em dourado negrito
    verde_b = cor_nucleo(im0, (305, 1039, 773, 1067), lambda r, g, b: (r < 120) & (g < 120), 50)
    ouro_b = cor_nucleo(im0, (294, 1075, 445, 1098), OURO_TXT, 40)
    im = apagar(im, (262, 1030, 820, 1146), lambda r, g, b: VERDE_APAGAR(r, g, b) | OURO_TXT(r, g, b), 3, 6)
    tb = tam_por_largura(lambda s: [('Tudo claro e organizado para melhorar', REG, s, verde_b)], 773 - 305)
    L = [
        ('Tudo claro e organizado para melhorar', 1039, [('Todo claro y organizado para mejorar', REG, verde_b)]),
        ('resultados e aumentar sua segurança ao', 1075, [('resultados', BOLD, ouro_b), (' y aumentar su seguridad al', REG, verde_b)]),
        ('tratar olheiras sem medo de complicações.', 1112, [('tratar ojeras ', REG, verde_b), ('sin miedo a las complicaciones', BOLD, ouro_b),
                                                            ('.', REG, verde_b)]),
    ]
    for pt, yt, segs in L:
        base = base_de(REG, tb, pt, yt)
        tt = caber(lambda s: [(x, n, s, c) for x, n, c in segs], tb, 840 - 240, 0.15)
        linha(im, [(x, n, tt, c) for x, n, c in segs], base, CX, 'centro')

    # CTA
    branco_c = cor_nucleo(im0, (345, 1232, 575, 1264), BRANCO, 50, escuro=False)
    grad_c = grad_rel(im0, (592, 1231, 841, 1264), OURO)
    im = apagar(im, (330, 1222, 880, 1276), lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b), 3, 6)
    CTA = 'NotoSerif_600SemiBold'
    tc = tam_por_largura(lambda s: [('TOQUE EM SAIBA MAIS', CTA, s, branco_c)], 841 - 345)
    seg = lambda s: [('TOQUE EN ', CTA, s, branco_c), ('MÁS INFORMACIÓN', CTA, s, ('grad', grad_c, 1232, 1264))]
    LIM = 872 - 328
    tc2 = caber(seg, tc, LIM, 0.15)
    linha(im, seg(tc2), 1264, (328 + 872) / 2, 'centro')

    p = salvar(im, SAIDA_NOME)
    print('ok', p, im.size, 'preco k %.2f' % k_preco, 'CTA reducao %.0f%%' % ((1 - tc2 / tc) * 100))


if __name__ == '__main__':
    gerar()
