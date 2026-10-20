"""Capa do módulo Imersão -> FEA-Capa do modulo Imersion - LATAM.png. Só a copy muda.
A arte original diz IMERSÃO AVANÇADA / PREENCHIMENTO / LABIAL: traduzida fielmente.
LABIAL é idêntico em espanhol e fica intacto (pixels originais)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_apoio import *

im = abrir(T + 'capa-modulo.png')
a0 = im.copy()
VERM = lambda r, g, b: (r > 150) & (r - g > 60) & (r - b > 40)
NAO_FUNDO = lambda r, g, b: (r + g + b < 600)

# ---- IMERSÃO (Montserrat Light, tracking largo) -> INMERSIÓN
c_im = cor_texto(a0, (125, 240, 330, 292), lambda r, g, b: r < 120)
LIGHT = fonte('Montserrat_300Light')
f_i, tr_i = ajustar(LIGHT, 'IMERSAO', 278 - 254 + 1, 319 - 139 + 1)
im = apagar(im, (130, 244, 329, 287), NAO_FUNDO, dil=2, raio=4)
LIM = 333 - 14 - 139                         # mesmo respiro de 14 px antes da caixa escura
# 9 letras no lugar de 7: reduz o corpo no máximo 15 % e o tracking na mesma proporção,
# preservando o desenho espaçado do original
f_es, tr_es = f_i, tr_i
for k in np.arange(1.0, 0.849, -0.01):
    f_es = ImageFont.truetype(LIGHT, round(f_i.size * k * 4) / 4)
    tr_es = (LIM - larg(f_es, 'INMERSIÓN')) / 8
    if tr_es >= tr_i * k * 0.75:
        break
# mantém a linha de base: base do original = topo medido + altura de 'IMERSAO' no corpo original
base = 254 - f_i.getbbox('IMERSAO')[1] + f_i.getmetrics()[0]
desenhar(ImageDraw.Draw(im), 139 - f_es.getbbox('I')[0], base - f_es.getmetrics()[0], 'INMERSIÓN', f_es, c_im, tr_es)

# ---- AVANÇADA (Montserrat Bold creme sobre caixa chapada) -> AVANZADA
caixa_esc = (338, 249, 584, 286)
cor_caixa = cor_fundo(a0, (336, 246, 342, 286))
c_av = cor_texto(a0, (335, 246, 586, 287), lambda r, g, b: (r > 200) & (g > 200) & (b > 200))
BOLD = fonte('Montserrat_700Bold')
f_a, _ = ajustar(BOLD, 'AVANADA', 278 - 253 + 1, 579 - 344 + 1)       # corpo pela altura das maiúsculas
tr_a = (579 - 344 + 1 - larg(f_a, 'AVANÇADA')) / 7                    # tracking pela largura real
preencher(im, caixa_esc, cor_caixa)
linha(im, [('AVANZADA', c_av)], f_a, tr_a, 253, 'AVANADA', x0=344, x1=579, alinh='centro')

# ---- PREENCHIMENTO (Barlow Condensed Regular, justificado na largura do bloco) -> RELLENO
c_vm = cor_texto(a0, (115, 300, 600, 352), VERM)
COND = fonte('BarlowCondensed_400Regular')
f_p, tr_p = ajustar(COND, 'PREENCHIMENTO', 348 - 303 + 1, 589 - 123 + 1)
im = apagar(im, (112, 296, 602, 356), lambda r, g, b: VERM(r, g, b) | ((r - g) > 35), dil=3, raio=6)
# o bloco do título é justificado (todas as linhas de 123 a 589): RELLENO mantém o corpo e
# distribui o espaço entre as letras para fechar a mesma largura
tr_r = (589 - 123 + 1 - larg(f_p, 'RELLENO')) / (len('RELLENO') - 1)
linha(im, [('RELLENO', c_vm)], f_p, tr_r, 303, 'PREENCHIMENTO', x0=123)
print('tracking RELLENO', round(tr_r, 1), 'original', round(tr_p, 1), '| INMERSIÓN', f_es.size, 'de', f_i.size, round(tr_es, 2), 'de', round(tr_i, 2))

print(salvar(im, 'FEA-Capa do modulo Imersion - LATAM.png'), im.size)
previa(im, T + 'capa-modulo-es-prev.jpg', 1280)
