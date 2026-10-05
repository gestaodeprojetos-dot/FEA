"""Verificação 3 (nada em português): OCR do PDF ENTREGUE e busca de palavras com
marca portuguesa (ã õ ç ê / -ção / -ões), que não existem em espanhol."""
import pymupdf, subprocess, re, json, sys, os
from concurrent.futures import ThreadPoolExecutor
pdf = sys.argv[1]; os.makedirs('produccion/ocr2', exist_ok=True)
MARCA = re.compile(r"\b\w*(?:[ãõçêÃÕÇÊ]|ção|ções|ões)\w*\b")
def pag(i):
    p = pymupdf.open(pdf)[i]
    png = f'produccion/ocr2/p{i+1}.png'; p.get_pixmap(dpi=150).save(png)
    txt = subprocess.run(['tesseract', png, 'stdout', '-l', 'por', '--psm', '11'],
                         capture_output=True, text=True, env={**os.environ, 'OMP_THREAD_LIMIT': '1'}).stdout
    camada = p.get_text()
    achados = sorted({w for w in MARCA.findall(txt) if len(w) > 3 and w not in camada})
    return i + 1, achados
with ThreadPoolExecutor(6) as ex:
    res = {k: v for k, v in ex.map(pag, range(len(pymupdf.open(pdf)))) if v}
json.dump(res, open('produccion/ocr-residuo.json', 'w'), ensure_ascii=False, indent=1)
for k, v in res.items(): print(k, v[:12])
