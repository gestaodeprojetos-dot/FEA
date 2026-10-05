#!/usr/bin/env python3
"""FEA · Ads 02 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Arte imita uma caixinha de pergunta do Instagram do próprio Dr. João (não é
depoimento de aluno), então é traduzida normalmente. Fundo laranja chapado,
caixas de destaque pretas/cinza-claras com serifada (EB Garamond) e sticker
de pergunta em Roboto. Rodar a partir de fea_artes/: python3 criativos/ads02.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads01a04 import *  # noqa

SERIF = fonte('EBGaramond_400Regular')
ROBOTO_M = fonte('Roboto_500Medium')
NBSP = '\u00a0'
PRECO_NB = PRECOS['preco'].replace(' ', NBSP)  # preço não quebra entre linhas
CLARO_TXT = lambda r, g, b: (r > 130) & (g > 130) & (b > 130)
ESCURO_TXT = lambda r, g, b: (r < 140) & (g < 140) & (b < 140)

P1_PT = ['Injetor, o preenchimento de olheiras é um', 'dos procedimentos mais desafiadores e',
         'lucrativos da harmonização facial.']
P2_PT = ['Sou o Dr. João Pithon, médico, pesquisador e', 'co-autor do livro Arquitetura Facial. Se tem',
         'alguém que pode te mostrar como dominar', 'essa região de forma segura e previsível, sou eu.']
P3_PT = ['Por um valor simbólico, apenas R$ 97,00 ,', 'você terá acesso ao meu eBook: Preenchimento',
         'Tridimensional de Olheiras: Um Guia', 'Completo com a Metodologia ARTI']
CTA_PT = ['Toque em SAIBA MAIS e garanta o seu!']

P1_ES = ('Estimado inyector: el relleno de ojeras es uno de los procedimientos más desafiantes '
         'y rentables de la armonización facial.')
P2_ES = ('Soy el Dr. João Pithon, médico, investigador y coautor del libro Arquitetura Facial. '
         'Si hay alguien que pueda mostrarle cómo dominar esta región de forma segura y previsible, soy yo.')
P3_ES = (f'Por un valor simbólico, solo {PRECO_NB}, tendrá acceso a mi ebook Relleno '
         'tridimensional de ojeras: una guía completa con la metodología ARTI.')
CTA_ES = 'Toque en MÁS INFORMACIÓN y asegure el suyo.'

PERG_PT = ['Dr. João, preenchimento', 'de olheiras é o meu pesadelo.', 'O que fazer?']
PERG_ES = ['Dr. João, el relleno de', 'ojeras es mi pesadilla.', '¿Qué hago?']


def sticker(im, cab, corpo):
    """Cabeçalho escuro 'Faça uma pergunta' + emoji, e corpo branco com a pergunta."""
    a = np.array(im).astype(int)
    # emoji: pixels saturados no miolo do cabeçalho
    x0, y0, x1, y1 = cab[0] + 30, cab[1] + 12, cab[2] - 30, cab[3] - 5
    s = a[y0:y1, x0:x1]
    ys, xs = np.where((s.max(2) - s.min(2)) > 25)
    ex0, ex1, ey0, ey1 = xs.min() + x0 - 3, xs.max() + x0 + 4, ys.min() + y0 - 3, ys.max() + y0 + 4
    emoji = im.crop((ex0, ey0, ex1, ey1))
    cor_cab = cor_fundo(im, (cab[0] + 40, cab[1] + 4, cab[0] + 80, cab[1] + 10))
    med = linhas_texto(im, (cab[0] + 20, cab[1] + 5, ex0 - 1, cab[3] - 5), lambda r, g, b: (r > 120) & (abs(r - b) < 25))
    ty0, ty1, tx0, tx1 = med[0]
    f = calibrar(ROBOTO_M, 'Faça uma pergunta', tx1 - tx0 + 1)
    base = ty0 - f.getbbox('Faça uma pergunta', anchor='ls')[1]
    cor_t = cor_texto(im, (tx0, ty0, tx1 + 1, ty1 + 1), lambda r, g, b: (r > 120) & (abs(r - b) < 25))
    gap = ex0 + 3 - tx1
    centro = (tx0 + ex1) / 2
    preencher(im, (cab[0] + 25, min(ty0, ey0) - 6, cab[2] - 25, max(ty1, ey1) + 6), cor_cab)
    t = 'Haga una pregunta'
    w = f.getlength(t)
    total = w + gap + (ex1 - ex0)
    xt = centro - total / 2
    ImageDraw.Draw(im).text((xt, base), t, font=f, fill=cor_t, anchor='ls')
    im.paste(emoji, (int(round(xt + w + gap - 3)), ey0))
    # corpo branco: a pergunta (caixa interna, sem tocar nos cantos arredondados)
    cor_corpo = cor_fundo(im, (corpo[0] + 40, corpo[1] + 4, corpo[0] + 80, corpo[1] + 10))
    paragrafo(im, (corpo[0] + 18, corpo[1] + 6, corpo[2] - 18, corpo[3] - 14), PERG_PT, None, ROBOTO_M, ESCURO,
              linhas_es=PERG_ES, cor_caixa=cor_corpo, larg_max=corpo[2] - corpo[0] - 60, verbose='  pergunta')


def ads02(origem, saida, cx, larg_max):
    im = abrir(origem)
    laranja = cor_fundo(im, (0, 0, 40, 40))
    print(saida)
    sticker(im, cx['cab'], cx['corpo'])
    paragrafo(im, cx['p1'], P1_PT, P1_ES, SERIF, CLARO_TXT, fundo_ext=laranja, larg_max=larg_max, verbose='  p1')
    paragrafo(im, cx['p2'], P2_PT, P2_ES, SERIF, ESCURO_TXT, fundo_ext=laranja, larg_max=larg_max, verbose='  p2')
    paragrafo(im, cx['p3'], P3_PT, P3_ES, SERIF, CLARO_TXT, fundo_ext=laranja, larg_max=larg_max, verbose='  p3')
    paragrafo(im, cx['cta'], CTA_PT, CTA_ES, SERIF, ESCURO_TXT, fundo_ext=laranja, larg_max=larg_max,
              linhas_es=[CTA_ES], verbose='  cta')
    return salvar(im, saida)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ads02('trabalho/ads02-feed.png', 'FEA-Ads 02 - PTO-LATAM - Feed.png',
          dict(cab=(313, 53, 791, 132), corpo=(313, 132, 791, 261), p1=(200, 289, 891, 431),
               p2=(140, 489, 935, 691), p3=(149, 750, 936, 943), cta=(202, 988, 880, 1038)), 820)
    ads02('trabalho/ads02-story.png', 'FEA-Ads 02 - PTO-LATAM - Story.png',
          dict(cab=(255, 382, 826, 476), corpo=(255, 476, 826, 630), p1=(152, 713, 934, 873),
               p2=(84, 940, 984, 1169), p3=(94, 1234, 985, 1453), cta=(154, 1504, 922, 1561)), 900)
