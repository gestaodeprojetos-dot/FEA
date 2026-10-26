"""Correções de imagem do documento do autor (23/10/2026):
 12. Figura 22 (pág. 55): tarjas pretas opacas sobre os olhos nas fotos A e B,
     gravadas nos PIXELS da imagem (não só desenhadas por cima), para que a
     região ocular não possa ser recuperada extraindo a foto do PDF.
 13. Figura 53 (pág. 177): foto antiga trocada pela nova foto do autor, recortada
     na região labial na mesma proporção do quadro original (sem distorcer).
Uso: python3 fea_imagens.py entrada.pdf saida.pdf nova_foto_fig53.png"""
import sys, io, pymupdf
from PIL import Image

ent, sai, nova = sys.argv[1:4]
d = pymupdf.open(ent)

def tarja(page, xref, barra):
    """barra em coordenadas da página; pinta de preto os pixels correspondentes."""
    r = page.get_image_rects(xref)[0]
    info = d.extract_image(xref)
    im = Image.open(io.BytesIO(info['image'])).convert('RGB')
    sx, sy = im.width / r.width, im.height / r.height
    x0 = max(0, int((barra.x0 - r.x0) * sx)); x1 = min(im.width, int((barra.x1 - r.x0) * sx) + 1)
    y0 = max(0, int((barra.y0 - r.y0) * sy)); y1 = min(im.height, int((barra.y1 - r.y0) * sy) + 1)
    im.paste((0, 0, 0), (x0, y0, x1, y1))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=92)
    page.replace_image(xref, stream=buf.getvalue())

def acha(page, rect_aprox):
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            if abs(r.x0 - rect_aprox[0]) < 3 and abs(r.y0 - rect_aprox[1]) < 3:
                return im[0]
    raise SystemExit('imagem não encontrada em %s' % (rect_aprox,))

# 12 · Figura 22: foto A (56,273)-(168,519) e foto B (171,273)-(283,521)
p = d[54]
tarja(p, acha(p, (56, 273)), pymupdf.Rect(70, 320, 169, 350))
tarja(p, acha(p, (171, 273)), pymupdf.Rect(186, 338, 284, 370))

# 13 · Figura 53: quadro (57,164)-(276,272)
p = d[176]
xr = acha(p, (57, 164)); r = p.get_image_rects(xr)[0]
im = Image.open(nova).convert('RGB')
alvo = r.width / r.height                      # proporção do quadro do livro
# recorte centrado na boca: faixa do nariz ao queixo, largura total do rosto
cy = int(im.height * 0.80)                     # centro vertical dos lábios na foto do autor
w = im.width; h = int(w / alvo)
if h > im.height: h = im.height; w = int(h * alvo)
y0 = max(0, min(im.height - h, cy - h // 2)); x0 = (im.width - w) // 2
crop = im.crop((x0, y0, x0 + w, y0 + h))
buf = io.BytesIO(); crop.save(buf, 'JPEG', quality=92)
p.replace_image(xr, stream=buf.getvalue())
d.save(sai, garbage=3, deflate=True)
print('ok', crop.size, 'recorte y', y0, y0 + h)
