# FEA · Encaixa cada página 16:9 na janela central do fundo Elite 4032x1344
import sys, os, subprocess, glob
from PIL import Image
pdf, saida, fundo = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(saida, exist_ok=True)
tmp = saida + '/_p'; os.makedirs(tmp, exist_ok=True)
subprocess.run(['pdftoppm', '-png', '-scale-to-x', '2390', '-scale-to-y', '1344', pdf, tmp + '/p'], check=True)
bg = Image.open(fundo).convert('RGB'); assert bg.size == (4032, 1344)
for i, f in enumerate(sorted(glob.glob(tmp + '/p-*.png')), 1):
    pg = Image.open(f).convert('RGB')
    if pg.size != (2390, 1344): pg = pg.resize((2390, 1344), Image.LANCZOS)
    out = bg.copy(); out.paste(pg, (821, 0))
    out.save(f'{saida}/slide-{i:02d}.jpg', quality=92, subsampling=0)
    os.remove(f)
os.rmdir(tmp)
print(saida, i)
