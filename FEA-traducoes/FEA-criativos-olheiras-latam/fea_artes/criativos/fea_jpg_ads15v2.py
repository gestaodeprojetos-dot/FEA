#!/usr/bin/env python3
"""[FEED] ADS 15_V2 (jpg) em espanhol LATAM. Troca só a copy.
Livro e tablet com página do ebook (mockup, página gerada por IA no original) ficam intactos: fase 2.
Rodar de fea_artes/:  python3 criativos/fea_jpg_ads15v2.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_jpg14a20 import *  # noqa

ORIG = 'trabalho/ads15v2-feed.jpg'
SAIDA_NOME = 'FEA-[FEED] ADS 15_V2 - LATAM.jpg'

BRANCO = lambda r, g, b: (r > 110) & (g > 110) & (b > 100) & (abs(r - g) < 40)
VERDE_CL = lambda r, g, b: (g > r + 25) & (g > 70)
OURO = lambda r, g, b: (r > 110) & (r - b > 45)
Y_TOPO_PILULA, Y_BASE_PILULA = 846, 865
MENTA = lambda r, g, b: (g > 110) & (g > r + 20)  # texto da pílula
LETRA_SELO = lambda r, g, b: ((r + g + b) < 330) & (r > b + 15)
TIT = 'LibreCaslonText_700Bold'
ITAL = 'Gelasio_500Medium_Italic'
TXT = 'Tinos_400Regular'
SANS = 'Inter_400Regular'
CAPS = 'NotoSerif_600SemiBold'
PRECO = 'PlayfairDisplay_600SemiBold'


def gerar():
    im0 = abrir(ORIG)
    im = im0.copy()

    # título branco (degradê suave)
    grad_t = grad_rel(im0, (118, 627, 990, 664), BRANCO)
    im = apagar(im, (110, 618, 1000, 682), BRANCO, 3, 6)
    im = apagar(im, (110, 686, 470, 750), BRANCO, 3, 6)
    tam = tam_por_largura(lambda t: [('Preenchimento Tridimensional', TIT, t, (0, 0, 0))], 989 - 120)
    b1 = base_de(TIT, tam, 'Preenchimento Tridimensional', 627)
    b2 = base_de(TIT, tam, 'de Olheiras:', 695)
    cap = F(TIT, tam).getbbox('T', anchor='ls')[1]
    linha(im, [('Relleno tridimensional', TIT, tam, ('grad', grad_t, b1 + cap, b1))], b1, 120)
    linha(im, [('de ojeras:', TIT, tam, ('grad', grad_t, b2 + cap, b2))], b2, 120)

    # subtítulo itálico verde
    cor_s = cor_nucleo(im0, (118, 760, 960, 808), VERDE_CL, 50, escuro=False)
    im = apagar(im, (110, 756, 980, 815), VERDE_CL, 3, 6)
    pt = 'Um Guia Completo com a Metodologia ARTI'
    tam = tam_por_largura(lambda t: [(pt, ITAL, t, cor_s)], 958 - 123)
    linha(im, [('Una guía completa con la metodología ARTI', ITAL, tam, cor_s)], base_de(ITAL, tam, pt, 766), 123)

    # pílula: 'ESSE EBOOK É PRA VOCÊ QUE:' -> 'ESTE EBOOK ES PARA USTED SI:'
    cor_p = cor_nucleo(im0, (130, 845, 510, 866), MENTA, 40, escuro=False)
    im = apagar(im, (128, 836, 600, 872), lambda r, g, b: (g > 80) & (g > r + 18), 3, 5)
    tam = tam_por_cap(SANS, Y_BASE_PILULA - Y_TOPO_PILULA, 'E')
    tr = track_para('ESSE EBOOK É PRA VOCÊ QUE:', SANS, tam, 588 - 135)
    es = 'ESTE EBOOK ES PARA USTED SI:'
    if largura_segs([(es, SANS, tam, cor_p)], tr) > 588 - 135:  # não passar da borda da pílula
        tr = track_para(es, SANS, tam, 588 - 135)
    x0, x1 = linha(im, [('ESTE EBOOK ES PARA USTED SI:', SANS, tam, cor_p)], Y_BASE_PILULA, 135, tr=tr)

    # lista
    cor_l = cor_nucleo(im0, (180, 906, 600, 932), BRANCO, 50, escuro=False)
    tam = tam_por_largura(lambda t: [('Evita tratar olheiras por insegurança', TXT, t, cor_l)], 596 - 184)
    itens = [('Evita tratar olheiras por insegurança', 906, 'Evita tratar ojeras por inseguridad'),
             ('Já faz, mas sem previsibilidade', 958, 'Ya lo hace, pero sin previsibilidad'),
             ('Quer reduzir risco e ter mais controle técnico', 1010, 'Quiere reducir riesgos y tener más control técnico'),
             ('Tudo isso com método estruturado por apenas', 1064, 'Todo esto con un método estructurado por solo')]
    for pt, yt, es in itens:
        im = apagar(im, (176, yt - 10, 1040, yt + 34), BRANCO, 3, 6)
        t = caber(lambda s: [(es, TXT, s, cor_l)], tam, 1030 - 183, 0.15)
        linha(im, [(es, TXT, t, cor_l)], base_de(TXT, tam, pt, yt), 183, peso=0.15)

    # preço na caixa de borda dourada (358..675)
    grad_p = grad_rel(im0, (495, 1125, 595, 1195), OURO)
    im = apagar(im, (380, 1118, 655, 1198), OURO, 3, 6)
    moeda, valor = dividir_preco(PRECOS['preco'])
    t_m = tam_por_cap(PRECO, 1191 - 1144, 'R')
    t_v = tam_por_cap(PRECO, 1191 - 1124, '9')
    k = 1.0
    while True:
        segs = [(moeda + ' ', PRECO, t_m * k, ('grad', grad_p, 1124, 1191)), (valor, PRECO, t_v * k, ('grad', grad_p, 1124, 1191))]
        if largura_segs(segs) <= (675 - 358) - 50 or k < 0.4:
            break
        k -= 0.01
    linha(im, segs, 1191 - (1 - k) * 34, (358 + 675) / 2, 'centro')
    k_preco = k

    # CTA: 'TOQUE EM SAIBA MAIS' / 'E GARANTA O SEU.' (alinhado à esquerda em x=329; seta curva começa em x~718)
    cor_c = cor_nucleo(im0, (329, 1239, 500, 1264), BRANCO, 50, escuro=False)
    cor_g = cor_nucleo(im0, (516, 1239, 771, 1264), VERDE_CL, 50, escuro=False)
    im = apagar(im, (320, 1232, 780, 1268), lambda r, g, b: BRANCO(r, g, b) | VERDE_CL(r, g, b), 3, 6)
    im = apagar(im, (320, 1268, 600, 1294), BRANCO, 3, 6)
    t1 = tam_por_cap(CAPS, 1264 - 1240, 'T')
    tr1 = track_para('TOQUE EM SAIBA MAIS', CAPS, t1, 771 - 329)
    seg1 = lambda t: [('TOQUE EN ', CAPS, t, cor_c), ('MÁS INFORMACIÓN', CAPS, t, cor_g)]
    LIM = 762 - 329  # a seta curva começa em x~780
    tr1b = tr1
    while largura_segs(seg1(t1), tr1b) > LIM and tr1b > tr1 * 0.5:
        tr1b -= 0.05
    t1b = caber(seg1, t1, LIM, 0.15, tr1b)
    k = t1b / t1
    base1 = 1264
    linha(im, seg1(t1b), base1, 329, tr=tr1b)
    t2 = tam_por_cap(CAPS, 1288 - 1272, 'E') * k
    tr2 = track_para('E GARANTA O SEU.', CAPS, t2 / k, 587 - 331) * k * max(0.5, tr1b / tr1)
    linha(im, [('Y ASEGURE EL SUYO.', CAPS, t2, cor_c)], 1288, 331, tr=tr2)

    # selo: arco superior e acento de CÓPIAS
    info = trocar_arco_selo(im, 913.7, 204.6, 67, 77, 'O PRIMEIRO E MAIS VENDIDO', 'MÉTODO EXCLUSIVO DEL',
                            'Montserrat_700Bold', ang_lim=(-145, 2), cond=LETRA_SELO, ang_fixo=(-130, -11), escala=0.68, pct_cor=12)

    # CÓPIAS -> COPIAS: só os pixels escuros do acento, acima do O
    acento = (873, 203, 879, 207)
    im = apagar(im, acento, lambda r, g, b: (0.299 * r + 0.587 * g + 0.114 * b) < 168, 0, 3)

    p = salvar(im, SAIDA_NOME)
    print('ok', p, im.size, 'selo', info, 'CTA reducao %.0f%% tracking %.2f->%.2f' % ((1 - k) * 100, tr1, tr1b), 'preco k %.2f' % k_preco)


if __name__ == '__main__':
    gerar()
