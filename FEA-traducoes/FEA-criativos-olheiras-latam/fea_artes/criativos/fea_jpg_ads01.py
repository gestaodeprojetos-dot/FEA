#!/usr/bin/env python3
"""[STORIES] ADS 01.jpg (Ebook Olheiras) em espanhol LATAM.

Troca só a copy. Original em trabalho/Jads01-story.jpg (Drive 1NqfHjmTbmnHokPZol2sdZPXPTLFAQOZU).
Mockup (capa do ebook + tablet com página gerada por IA) intacto: fase 2.
Selo dourado: arco 'O PRIMEIRO & MAIS VENDIDO' vira 'MÉTODO EXCLUSIVO DEL' (+ 'DR. JOÃO PITHON' do arco
de baixo) e 'CÓPIAS' perde o acento (COPIAS).
Preços de precos.json (de_297 riscado, preco): as pílulas claras são refeitas com a largura do texto,
esticando a própria pílula do original (tampas + coluna central); sobre o terno, a pílula fica
translúcida como no original.
Rodar a partir de fea_artes/: python3 criativos/fea_jpg_ads01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_jpg_util import *  # noqa

VERDE_ESC = (19, 54, 34)
OURO = (160, 110, 21)
PRETO = (20, 20, 20)
VERDE = (51, 148, 69)
VERM = (243, 23, 23)
CREME = (248, 243, 237)
TX = lambda r, g, b: ((r + g + b) < 640) & ~((b > r + 15) & (b > g))     # texto, exclui o terno azul


def recompor(orig, saida):
    im = abrir(orig)
    org = np.array(im).astype(int)
    terno = (org.sum(2) < 420) & (org[..., 2] > org[..., 0] + 15)
    # ---------- título (Noto Serif 53) ----------
    im = apagar(im, (110, 282, 712, 505), TX, 3)
    f = F('NotoSerif_400Regular', 53.0)
    b = base_de(f, 'Você ainda evita tratar', 296)
    passo = (441 - 296) / 2
    linha(im, 120, b, [('¿Todavía evita tratar', f, VERDE_ESC)])
    linha(im, 123, b + passo, [('ojeras por ', f, VERDE_ESC), ('miedo a las', f, OURO)])
    linha(im, 123, b + 2 * passo, [('complicaciones?', f, OURO)])
    # ---------- corpo ----------
    im = apagar(im, (110, 522, 598, 682), TX, 3)
    fb = F('OpenSans_700Bold', 23.75)
    b = base_de(fb, 'Domine a anatomia', 530)
    linha(im, 122, b, [('Domine la anatomía, la profundidad', fb, PRETO)])
    linha(im, 120, b + 33, [('y la técnica adecuada para cada caso.', fb, PRETO)])
    t = 24.0
    ls = ['Ebook con marcación, planos de', 'aplicación y elección correcta del producto.']
    while max(F('OpenSans_400Regular', t).getlength(s) for s in ls) > 470:
        t -= 0.25
    fr = F('OpenSans_400Regular', t)
    b = base_de(F('OpenSans_400Regular', 24.0), 'Ebook com marca', 616)
    linha(im, 122, b, [(ls[0], fr, (40, 40, 40))])
    linha(im, 121, b + 33, [(ls[1], fr, (40, 40, 40))])
    # ---------- pílulas de preço ----------
    PY0, PY1 = 711, 772
    # apaga texto e seta (inclusive o '7' que passava sobre o terno)
    im = apagar(im, (120, 718, 630, 768), lambda r, g, b: ((r + g + b) < 400) & ~((b > r + 15) & (b > g)) | ((r > 200) & (g < 90)) | ((g > r + 40) & (g > 110)), 3)
    a = np.array(im)
    ya, yb = PY0 - 8, PY1 + 14
    tampa_e = a[ya:yb, 104:147].copy()          # pílula 1 sem texto: tampa esquerda
    tampa_d = a[ya:yb, 253:296].copy()          # tampa direita
    meio = np.median(a[ya:yb, 180:230], 1).astype(np.uint8)
    # limpa a faixa das pílulas antigas sobre o creme (fundo do card é chapado)
    zona = np.zeros(a.shape[:2], bool)
    zona[ya - 2:yb + 2, 100:640] = True
    zona &= ~terno
    a[zona] = CREME
    k = 1.0
    while True:
        fr2, fbv, fbg = F('OpenSans_400Regular', 29.2 * k), F('OpenSans_700Bold', 29.2 * k), F('OpenSans_700Bold', 37.5 * k)
        s1 = [('De ', fr2, PRETO), (PRECOS['de_297'], fbv, VERM, 'risco')]
        s2 = [('a solo ', fr2, PRETO), (PRECOS['preco'], fbg, VERDE)]
        w1 = max(largura(s1) + 39, 86)
        w2 = max(largura(s2) + 39, 86)
        x1 = 115 + w1
        xs2 = x1 + 55
        if xs2 + w2 - 21 <= 616 or k < 0.4:     # texto da 2a pílula termina onde o original terminava (x 614)
            break
        k -= 0.01

    def desenha(a, x0, x1, opac_terno=0.2):
        x0, x1 = int(round(x0)), int(round(x1))
        p = a.copy()
        for x in range(x0 + 32, x1 - 10):
            p[ya:yb, x] = meio
        p[ya:yb, x0 - 11:x0 + 32] = tampa_e
        p[ya:yb, x1 - 32:x1 + 11] = tampa_d
        reg = np.zeros(a.shape[:2], bool)
        reg[ya:yb, x0 - 11:x1 + 11] = True
        sobre = reg & terno
        out = a.copy()
        out[reg & ~terno] = p[reg & ~terno]
        out[sobre] = (p[sobre] * opac_terno + a[sobre] * (1 - opac_terno)).astype(np.uint8)
        return out

    a = desenha(a, 115, x1)
    a = desenha(a, xs2, xs2 + w2)
    im = Image.fromarray(a)
    base = 753
    linha(im, 115 + 18, base, s1, sub_esp=VERM)
    d = ImageDraw.Draw(im)
    ya_ = 742
    d.line([(x1 + 11, ya_), (xs2 - 8, ya_)], fill=VERDE, width=2)
    d.line([(xs2 - 16, ya_ - 6), (xs2 - 8, ya_)], fill=VERDE, width=2)
    d.line([(xs2 - 16, ya_ + 6), (xs2 - 8, ya_)], fill=VERDE, width=2)
    linha(im, xs2 + 18, base, s2)
    # ---------- selo dourado ----------
    im, _ = trocar_texto_arco(im, 690.5, 931.5, 99.3, 'MÉTODO EXCLUSIVO DEL')
    im = apagar(im, (643, 938, 655, 946), lambda r, g, b: ((r + g + b) < 520) & (r - b > 50), 1, 3)  # acento de CÓPIAS
    # ---------- CTA (botão verde em degradê, texto branco) ----------
    im = apagar(im, (275, 1640, 805, 1690), lambda r, g, b: (r + g + b) > 330, 4)
    es = 'Toque en Más información y asegure el suyo.'
    t = 26.75
    while F('OpenSans_700Bold', t).getlength(es) > 818 - 262 - 2 * 24 and t > 26.75 * 0.85:
        t -= 0.25
    fc = F('OpenSans_700Bold', t)
    base = 1672 - (F('OpenSans_700Bold', 26.75).getbbox('T', anchor='ls')[1] - fc.getbbox('T', anchor='ls')[1]) / 2
    linha(im, 540, base, [(es, fc, (255, 255, 255))], 'centro')
    print(salvar(im, saida), 'escala do preço: %.2f' % k, 'corpo: %.2f' % t)
    return im


if __name__ == '__main__':
    recompor('trabalho/Jads01-story.jpg', 'FEA-[STORIES] ADS 01 - LATAM.jpg')
