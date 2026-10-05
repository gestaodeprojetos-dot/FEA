"""Avatar I Grupo de Alunos -> FEA-Avatar Grupo de Alumnos - LATAM.png. Só a copy muda.
'Dr. João Pithon' (nome próprio) e os filetes roxos ficam intactos."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_apoio import *

im = abrir(T + 'avatar.png')
a0 = im.copy()
cor = cor_texto(a0, (240, 760, 1012, 1045), CLARO)
CX = (247 + 1007) / 2

REG = fonte('Montserrat_400Regular')
BOLD = fonte('Montserrat_700Bold')
f1, tr1 = ajustar(REG, 'Comunidade de', 844 - 768 + 1, 1007 - 247 + 1)
f2, tr2 = ajustar(BOLD, 'Alunos', 1039 - 872 + 1, 1010 - 242 + 1)

im = apagar(im, (225, 752, 1030, 1050), lambda r, g, b: (r + g + b) > 230, dil=4, raio=10)

linha(im, [('Comunidad de', cor)], f1, tr1, 768, 'Comunidade de', x0=CX, x1=CX, alinh='centro')

# 'Alumnos' tem uma letra a mais: limita a largura a 900 px (margem lateral de 177 px),
# reduzindo o corpo no máximo 15 % e mantendo a linha de base do original
base2 = 872 - f2.getbbox('Alunos')[1] + f2.getmetrics()[0]
f2es, tr2es = f2, tr2
for k in np.arange(1.0, 0.849, -0.01):
    f2es = ImageFont.truetype(BOLD, round(f2.size * k * 4) / 4)
    tr2es = tr2 * k
    if larg(f2es, 'Alumnos', tr2es) <= 900:
        break
w = larg(f2es, 'Alumnos', tr2es)
desenhar(ImageDraw.Draw(im), CX - w / 2 - f2es.getbbox('Alumnos')[0], base2 - f2es.getmetrics()[0], 'Alumnos', f2es, cor, tr2es)
print('Alumnos corpo', f2es.size, 'de', f2.size, 'largura', round(w))

print(salvar(im, 'FEA-Avatar Grupo de Alumnos - LATAM.png'), im.size)
previa(im, T + 'avatar-es-prev.jpg', 900)
