import sys
from PIL import Image
import numpy as np
src, out, prev = sys.argv[1:4]
l = np.array(Image.open(src).convert('RGB')).astype(float)
c = l[720:1080, 270:1000]
R, G, B = c[..., 0], c[..., 1], c[..., 2]
lum = 0.299*R + 0.587*G + 0.114*B
mn = c.min(axis=2)
a = np.clip((lum - 60) / 90, 0, 1)
# linha BLACKFRIDAY: mao/relogio atras, usar canal minimo (texto branco)
top = slice(0, 125)
a[top] = np.clip((mn[top] - 150) / 70, 0, 1)
Image.fromarray(np.uint8(a*255)).save(out + '.mask.png')
rgba = np.dstack([c, a*255]).astype(np.uint8)
im = Image.fromarray(rgba, 'RGBA')
bbox = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
im = im.crop(bbox); im.save(out)
bg = Image.new('RGBA', im.size, (90, 30, 120, 255)); bg.alpha_composite(im); bg.save(prev)
print(bbox, im.size)
