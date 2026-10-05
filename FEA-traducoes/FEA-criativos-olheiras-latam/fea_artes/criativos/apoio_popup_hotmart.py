"""Pop-up Hotmart (Ebook Olheiras) -> FEA-Pop-up Hotmart - LATAM.png. Só a copy muda.
Os livros desfocados nas bordas (sem texto legível) ficam como estão."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_apoio import *

im = abrir(T + 'popup.png')
a0 = im.copy()
VERDE = lambda r, g, b: (g > r + 40) & (g > b + 20)
OURO = lambda r, g, b: (r > 150) & (r - b > 45)
NAO_FUNDO = lambda r, g, b: (r + g + b < 680) | ((r - b) > 25)

c_esc = cor_texto(a0, (150, 380, 900, 560), ESCURO)
c_ver = cor_texto(a0, (150, 680, 900, 800), VERDE)

# ---- título pequeno dourado com textura (3 linhas centradas)
CX = (221 + 806) / 2   # centro medido do corpo original (o bloco não está no centro exato da arte)
TT = fonte('PlusJakartaSans_800ExtraBold')
f_tt, tr_tt = ajustar(TT, 'TRIDIMENSIONAL', 278 - 252 + 1, 683 - 388 + 1)
cx_tt = (360, 205, 720, 322)
tex_tt = campo_textura(a0, cx_tt, OURO)
im = apagar(im, (360, 205, 720, 320), NAO_FUNDO, dil=2)
m = Image.new('L', im.size, 0)
for s_es, s_pt, y in [('RELLENO', 'PREENCHIMENTO', 218), ('TRIDIMENSIONAL', 'TRIDIMENSIONAL', 252), ('DE OJERAS', 'DE OLHEIRAS', 286)]:
    linha(None, [(s_es, 255)], f_tt, tr_tt, y, s_pt, x0=386, x1=687, alinh='centro', mascara_out=m)
im = colar_textura(im, m, tex_tt, cx_tt)

# ---- chamada principal (Geist SemiBold, tracking negativo medido)
H = fonte('Geist_600SemiBold')
f_h, tr_h = ajustar(H, 'ESSA OFERTA', 460 - 399 + 1, 784 - 256 + 1)
im = apagar(im, (150, 390, 905, 563), NAO_FUNDO, dil=3)
linha(im, [('ESTA OFERTA', c_esc)], f_h, tr_h, 399, 'ESSA OFERTA', x0=256, x1=785, alinh='centro')
linha(im, [('ESPECIAL ES POR', c_esc)], f_h, tr_h, 476, 'ESPECIAL É POR', x0=209, x1=831, alinh='centro')

# TEMPO LIMITADO em dourado degradê: textura reaproveitada do original
cx_ou = (130, 578, 930, 660)
tex_ou = campo_textura(a0, cx_ou, OURO)
im = apagar(im, (150, 578, 905, 660), NAO_FUNDO, dil=3)
m = Image.new('L', im.size, 0)
w = linha(None, [('TIEMPO LIMITADO', 255)], f_h, tr_h, 588, 'TEMPO LIMITADO', x0=170, x1=862, alinh='centro', mascara_out=m)
assert w < 790, w
im = colar_textura(im, m, tex_ou, cx_ou)

# ---- corpo: Light escuro + Bold verde
CL = fonte('Geist_300Light')
CB = fonte('Geist_700Bold')
xh = altura_x(a0, (221, 745, 465, 782), lambda r, g, b: r + g + b < 400)[0]
f_l, tr_l = ajustar_x(CL, 'enquanto é tempo!', altura_x(a0, (470, 745, 800, 782), lambda r, g, b: r + g + b < 400)[0], 799 - 476 + 1)
f_b, tr_b = ajustar_x(CB, 'seu desconto', xh, 464 - 223 + 1)
im = apagar(im, (200, 695, 830, 790), NAO_FUNDO, dil=2)
d = ImageDraw.Draw(im)
ref = 'Finalize a sua inscrição e garanta o'
yb1 = 702 - f_l.getbbox(ref)[1] + f_l.getmetrics()[0]       # mesma linha de base do original


def seq(segs, yb):
    tot = sum(f.getlength(t) + tr * len(t) for t, f, tr, _ in segs)
    x = CX - tot / 2
    for t, f, tr, cor in segs:
        x = desenhar(d, x, yb - f.getmetrics()[0], t, f, cor, tr)
    return tot


seq([('¡Finalice su inscripción y ', f_l, tr_l, c_esc), ('asegure su', f_b, tr_b, c_ver)], yb1)
seq([('descuento', f_b, tr_b, c_ver), (' mientras aún hay tiempo!', f_l, tr_l, c_esc)], yb1 + (745 - 702))

# ---- palavra gigante cortada na base (Plus Jakarta Sans ExtraBold, faixa visível de 23 px)
GIG = fonte('PlusJakartaSans_800ExtraBold')
f_G = ImageFont.truetype(GIG, 203.0)
TR_G = 0.5
_, topo_rel = faixas(f_G, 'OLHEIRAS', TR_G, 23)
c_gig = cor_texto(a0, (57, 1060, 860, 1080), VERDE)
# só até x 880: dali para a direita o livro desfocado cobre a palavra
im = apagar(im, (40, 1045, 885, 1080), VERDE, dil=3, raio=8)
camada = Image.new('L', im.size, 0)
desenhar(ImageDraw.Draw(camada), 25, 1057 - topo_rel, 'OJERAS', f_G, 255, TR_G)
# a palavra passa por trás do livro: não pinta sobre ele (x > 880)
arr = np.array(camada); arr[:, 880:] = 0
im.paste(Image.new('RGB', im.size, c_gig), (0, 0), Image.fromarray(arr))

print(salvar(im, 'FEA-Pop-up Hotmart - LATAM.png'), im.size)
previa(im, T + 'popup-es-prev.jpg', 1080)
