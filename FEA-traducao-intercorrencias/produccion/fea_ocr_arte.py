"""Camada 2: texto que só existe dentro de imagem. OCR por página e diff contra a camada de texto."""
import pymupdf, subprocess, json, re, sys
from concurrent.futures import ThreadPoolExecutor
doc = pymupdf.open('original.pdf')
def norm(s): return re.sub(r'[^a-zà-ú0-9]', '', s.lower())
def pagina(i):
    p = pymupdf.open('original.pdf')[i]
    camada = norm(p.get_text())
    png = f'produccion/ocr/p{i+1}.png'
    p.get_pixmap(dpi=200).save(png)
    txt = subprocess.run(['tesseract', png, 'stdout', '-l', 'por+eng', '--psm', '3'],
                         capture_output=True, text=True).stdout
    so_imagem = []
    for linha in txt.splitlines():
        l = linha.strip()
        if len(norm(l)) < 4: continue
        if norm(l) not in camada: so_imagem.append(l)
    return i + 1, so_imagem
with ThreadPoolExecutor(8) as ex:
    res = dict(ex.map(pagina, range(len(doc))))
json.dump(res, open('produccion/ocr-arte.json', 'w'), ensure_ascii=False, indent=1)
pt = {k: v for k, v in res.items() if any(re.search(r'[ãõçêâ]|ção|ões', l.lower()) for l in v)}
print('paginas com linhas so na imagem:', sum(1 for v in res.values() if v), '| com marca de portugues:', len(pt))
print(sorted(pt))
