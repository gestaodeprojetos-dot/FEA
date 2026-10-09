"""Banner Checkout (Ebook Olheiras) -> FEA-Banner Checkout - LATAM.png. Só a copy muda.
Mockup do ebook (x 690 a 1000, y 0 a 400) fica intacto: fase 2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_apoio import *

im = abrir(T + 'banner-checkout.png')
a0 = im.copy()
VERDE = lambda r, g, b: (g > r + 40) & (g > b + 20)
OURO = lambda r, g, b: (r > 170) & (r - b > 70)
ESC_OU_VERDE = lambda r, g, b: ESCURO(r, g, b) | VERDE(r, g, b) | ((r < 200) & (abs(r - g) < 12) & (abs(g - b) < 12) & (r < 170))

# cores originais
c_esc = cor_texto(a0, (50, 74, 440, 110), ESCURO)
c_ver = cor_texto(a0, (50, 186, 520, 220), VERDE)
c_ouro = cor_texto(a0, (75, 240, 268, 262), OURO)
c_cinza = cor_texto(a0, (66, 312, 310, 334), lambda r, g, b: r < 150)
c_pill = cor_texto(a0, (370, 312, 548, 334), lambda r, g, b: r < 90)

# ---- título (Geist SemiBold, tracking negativo medido)
TIT = fonte('Geist_600SemiBold')
f_t, tr_t = ajustar(TIT, 'Domine o preenchimento', 106 - 78 + 1, 432 - 57 + 1)
cond_t = lambda r, g, b: (r + g + b < 560) | VERDE(r, g, b)
im = apagar(im, (50, 72, 650, 223), cond_t, dil=3)
linha(im, [('Domine el relleno', c_esc)], f_t, tr_t, 78, 'Domine o preenchimento', x0=57)
linha(im, [('tridimensional de ojeras con la', c_esc)], f_t, tr_t, 115, 'tridimensional de olheiras, com a', x0=55)
linha(im, [('metodología ARTI y ', c_esc), ('logre resultados', c_ver)], f_t, tr_t, 152, 'metodologia ARTI, e alcance resultados', x0=57)
linha(im, [('naturales, seguros y duraderos.', c_ver)], f_t, tr_t, 189, 'naturais, seguros e duradouros.', x0=57)

# ---- corpo (Plus Jakarta Sans Regular + destaque dourado em ExtraBold)
CORPO = fonte('PlusJakartaSans_400Regular')
xh = altura_x(a0, (270, 240, 640, 266), ESCURO)[0]
f_c, tr_c = ajustar_x(CORPO, 'do procedimento mais desafiador', xh, 623 - 271 + 1)
NEG = fonte('PlusJakartaSans_800ExtraBold')
f_n, tr_n = ajustar(NEG, 'GUIA DEFINITIVO', 259 - 244 + 1, 264 - 79 + 1)
im = apagar(im, (50, 238, 640, 297), lambda r, g, b: (r + g + b < 560) | OURO(r, g, b), dil=2)
# linha 1 em três segmentos com fontes diferentes: escreve em sequência
d = ImageDraw.Draw(im)
y1 = 243 - f_c.getbbox('O GUIA DEFINITIVO do procedimento mais desafiador')[1]
x = 56 - f_c.getbbox('L')[0]
x = desenhar(d, x, y1, 'La ', f_c, c_esc, tr_c)
yb = y1 + f_c.getmetrics()[0]          # linha de base comum
x = desenhar(d, x, yb - f_n.getmetrics()[0], 'GUÍA DEFINITIVA', f_n, c_ouro, tr_n)
x = desenhar(d, x, y1, ' del procedimiento más desafiante', f_c, c_esc, tr_c)
assert x < 680, x
linha(im, [('de la armonización facial.', c_esc)], f_c, tr_c, 270, 'da harmonização facial.', x0=56)

# ---- pílula cinza (texto centralizado na pílula 55..317)
def apagar_dentro(im, caixa, cond, dil=2, raio=4):
    # inpainting restrito ao miolo da pílula: o fundo de fora não contamina
    sub = apagar(im.crop(caixa), (0, 0, caixa[2] - caixa[0], caixa[3] - caixa[1]), cond, dil, raio)
    im.paste(sub, caixa[:2])
    return im


im = apagar_dentro(im, (60, 311, 314, 335), lambda r, g, b: r < 185)
CP = fonte('PlusJakartaSans_300Light')
f_p, tr_p = ajustar(CP, 'Preencha os campos abaixo', 331 - 314 + 1, 307 - 69 + 1)
linha(im, [('Complete sus datos abajo', c_cinza)], f_p, tr_p, 314, 'Preencha os campos abaixo', x0=55, x1=318, alinh='centro')

# ---- pílula dourada: texto, depois encurta a pílula (só o miolo é comprimido, cadeado e ponta intactos)
im = apagar_dentro(im, (368, 311, 556, 335), lambda r, g, b: (r < 150), dil=2)
PG = fonte('PlusJakartaSans_700Bold')
f_g, tr_g = ajustar(PG, 'Pagamento seguro', 332 - 315 + 1, 542 - 376 + 1)
w = larg(f_g, 'Pago seguro', tr_g)
PX0, PX1, PY0, PY1 = 336, 562, 305, 341        # pílula 336..561 x 309..336 (com margem)
fim_novo = int(round(376 + w + (561 - 542)))
PONTA = 22                                      # ponta arredondada + fundo à direita
miolo = im.crop((370, PY0, PX1 - PONTA, PY1))
ponta = im.crop((PX1 - PONTA, PY0, PX1 + 6, PY1))
novo_miolo = miolo.resize((fim_novo - PONTA + 1 - 370, PY1 - PY0), Image.LANCZOS)
# fundo cinza onde a pílula deixa de existir: interpolação vertical entre as linhas acima e abaixo
arr = np.array(im).astype(float)
for x in range(fim_novo - 2, PX1 + 7):
    top, bot = arr[PY0 - 1, x], arr[PY1, x]
    for y in range(PY0, PY1):
        k = (y - PY0 + 1) / (PY1 - PY0 + 1)
        arr[y, x] = top * (1 - k) + bot * k
im = Image.fromarray(arr.round().astype(np.uint8))
im.paste(novo_miolo, (370, PY0))
im.paste(ponta, (fim_novo - PONTA + 1, PY0))
linha(im, [('Pago seguro', c_pill)], f_g, tr_g, 315, 'Pagamento seguro', x0=376)

# ---- palavra gigante cortada na base (Plus Jakarta Sans ExtraBold, faixa de 18 px visível)
GIG = fonte('PlusJakartaSans_800ExtraBold')
f_G = ImageFont.truetype(GIG, 128.0)
TR_G = -0.5
_, topo_rel = faixas(f_G, 'OLHEIRAS', TR_G, 18)
c_gig = cor_texto(a0, (37, 385, 660, 400), VERDE)
im = apagar(im, (30, 372, 672, 400), VERDE, dil=3, raio=8)
desenhar(ImageDraw.Draw(im), 20, 382 - topo_rel, 'OJERAS', f_G, c_gig, TR_G)

print('pilulas', f_p.size, tr_p, f_g.size, tr_g)
print(salvar(im, 'FEA-Banner Checkout - LATAM.png'), im.size)
previa(im, T + 'banner-checkout-es-prev.jpg', 1000)
