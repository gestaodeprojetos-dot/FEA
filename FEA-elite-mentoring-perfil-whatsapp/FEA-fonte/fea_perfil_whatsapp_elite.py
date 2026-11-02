"""Gera a foto de perfil de WhatsApp do Elite Mentoring (1080x1080).

Usa somente assets oficiais do KV Elite (logo ELITE e monograma TT, PNG transparentes)
e composição vetorial/gradiente; nenhuma imagem gerada por IA.
Uso: python3 fea_perfil_whatsapp_elite.py [pasta_saida]
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..')
S = 1080          # lado final
K = 2             # supersampling
N = S * K

def lerp(a, b, t):
    return a + (b - a) * t

# ---------- fundo: azul-petróleo escuro com feixe de luz no alto à esquerda ----------
yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) / N
base_top = np.array([10, 38, 52], np.float32)     # petróleo
base_bot = np.array([3, 10, 15], np.float32)      # quase preto
t = np.clip(yy * 0.9 + xx * 0.25, 0, 1)[..., None]
img = base_top * (1 - t) + base_bot * t
# feixe principal (radial, canto superior esquerdo)
d = np.sqrt((xx - 0.12) ** 2 + (yy + 0.05) ** 2)
glow = np.clip(1 - d / 0.75, 0, 1) ** 2.2
img += glow[..., None] * np.array([120, 175, 195], np.float32)
# raio diagonal suave (luz rasante)
diag = np.exp(-((yy - (0.30 - xx * 0.55)) ** 2) / 0.010) * np.clip(1 - xx * 1.3, 0, 1)
img += diag[..., None] * np.array([14, 26, 32], np.float32)
# vinheta
v = np.sqrt((xx - 0.5) ** 2 + (yy - 0.5) ** 2)
img *= (1 - np.clip(v - 0.45, 0, 1) * 0.9)[..., None]
fundo = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')

# ---------- monograma TT fantasma ao fundo ----------
mono = Image.open(os.path.join(AQUI, 'FEA-elite-monograma.png')).convert('RGBA')
mw = int(N * 1.18)
mh = int(mono.height * mw / mono.width)
mono = mono.resize((mw, mh), Image.LANCZOS)
alpha = mono.split()[3]
borda_px = 3 * K
contorno = ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(borda_px * 2 + 1)), alpha)
ma = np.array(alpha, np.float32) / 255
ca = np.array(contorno, np.float32) / 255
# a luz vem do alto à esquerda: contorno mais visível em cima
_l = np.linspace(0, 1, mh)
gy = (np.linspace(1.0, 0.35, mh) * np.clip((0.97 - _l) / 0.22, 0, 1))[:, None]
gx = np.linspace(1.0, 0.55, mw)[None, :]
luz = gy * gx
camada = np.zeros((mh, mw, 4), np.float32)
camada[..., :3] = np.array([190, 225, 238], np.float32)
camada[..., 3] = np.clip(ca * 0.55 * luz + ma * 0.07 * luz, 0, 1) * 255
fantasma = Image.fromarray(camada.astype(np.uint8), 'RGBA')
brilho = fantasma.filter(ImageFilter.GaussianBlur(10 * K))
mx = (N - mw) // 2
my = int(-0.035 * N)
fundo.alpha_composite(brilho, (mx, my))
fundo.alpha_composite(fantasma, (mx, my))

# ---------- palavra ELITE (recorte do logo oficial) ----------
logo = Image.open(os.path.join(AQUI, 'FEA-elite-logo-claro.png')).convert('RGBA')
elite = logo.crop(logo.crop((0, 0, logo.width, 610)).getbbox())
ew = int(N * 0.74)
eh = int(elite.height * ew / elite.width)
elite = elite.resize((ew, eh), Image.LANCZOS)

# subtítulo MENTORING no mesmo desenho do "INJECTORS CONGRESS"
txt = 'MENTORING'
fonte = ImageFont.truetype(os.path.join(AQUI, 'Outfit.ttf'), 10)
fonte.set_variation_by_axes([420])
cap_alvo = eh * (156 / 603) * 0.92        # mesma proporção ELITE x subtítulo do logo
tam = 10
while True:
    f = ImageFont.truetype(os.path.join(AQUI, 'Outfit.ttf'), tam)
    f.set_variation_by_axes([420])
    bb = f.getbbox('E')
    if bb[3] - bb[1] >= cap_alvo:
        break
    tam += 2
larg_letras = sum(f.getlength(c) for c in txt)
espaco = (ew - larg_letras) / (len(txt) - 1)   # justificado na largura do ELITE
bb = f.getbbox('M')
cap = bb[3] - bb[1]
sub = Image.new('RGBA', (ew, int(cap * 1.6)), (0, 0, 0, 0))
ds = ImageDraw.Draw(sub)
x = 0.0
for c in txt:
    ds.text((x, -bb[1]), c, font=f, fill=(232, 240, 244, 255))
    x += f.getlength(c) + espaco
sub = sub.crop(sub.getbbox())

gap = int(eh * 0.20)
bloco_h = eh + gap + sub.height
ey = (N - bloco_h) // 2 + int(N * 0.01)
ex = (N - ew) // 2
# halo discreto atrás do logo para descolar do fundo
halo = Image.new('RGBA', (N, N), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hd.ellipse((ex - 60 * K, ey - 80 * K, ex + ew + 60 * K, ey + bloco_h + 80 * K), fill=(0, 8, 12, 150))
fundo.alpha_composite(halo.filter(ImageFilter.GaussianBlur(70 * K)))
# brilho suave do próprio logo
sombra = Image.new('RGBA', (N, N), (0, 0, 0, 0))
sombra.alpha_composite(elite, (ex, ey))
r, g, b, a = sombra.split()
glow_logo = Image.merge('RGBA', (r, g, b, a.point(lambda p: p * 0.35))).filter(ImageFilter.GaussianBlur(18 * K))
fundo.alpha_composite(glow_logo)
fundo.alpha_composite(elite, (ex, ey))
fundo.alpha_composite(sub, ((N - sub.width) // 2, ey + eh + gap))

final = fundo.convert('RGB').resize((S, S), Image.LANCZOS)
os.makedirs(SAIDA, exist_ok=True)
p_png = os.path.join(SAIDA, 'FEA-elite-mentoring-perfil-whatsapp-1080.png')
p_jpg = os.path.join(SAIDA, 'FEA-elite-mentoring-perfil-whatsapp-1080.jpg')
final.save(p_png, optimize=True)
final.save(p_jpg, quality=95, subsampling=0)

# prévia com a máscara circular do WhatsApp
prev = final.copy().convert('RGBA')
m = Image.new('L', (S, S), 0)
ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
circ = Image.new('RGBA', (S, S), (240, 242, 245, 255))
circ.paste(prev, (0, 0), m)
circ.convert('RGB').save(os.path.join(SAIDA, 'FEA-elite-mentoring-perfil-whatsapp-PREVIA-circulo.jpg'), quality=90)
print(p_png)
