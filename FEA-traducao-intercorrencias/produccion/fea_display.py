"""Páginas de abertura (Índice, Introdução, Conclusão, Referências): letras gigantes
em Advent Pro Bold com degradê dourado. O texto vetorial é apagado (o fundo, que é
imagem, fica intacto) e cada linha nova é desenhada como imagem com o mesmo degradê,
amostrado das letras originais, na mesma linha de base e no mesmo corpo."""
import pymupdf, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
FONTE = 'produccion/fontes-extra/AdventPro-Bold-OFL.ttf'
DPI = 300; K = DPI / 72
# página: {texto original da linha: texto ES}; linhas ausentes ficam como estão
# Toda linha de display da página é apagada e redesenhada (as caixas das letras se
# sobrepõem: apagar só uma linha levaria pedaços da vizinha).
TROCAS = {
    2:   {'SU': 'ÍN', 'MÁ': 'DI', 'RIO': 'CE'},
    4:   {'IN': 'IN', 'TRO': 'TRO', 'DU': 'DUC', 'ÇAO': 'CIÓN', '˜': None},
    203: {'CON': 'CON', 'CLU': 'CLU', 'SAO': 'SIÓN', '˜': None},
    207: {'RE': 'RE', 'FE': 'FE', 'REN': 'REN', 'CIAS': 'CIAS', 'ˆ': None},
}
def spans(page):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if s['size'] > 40: yield s
def gradiente(orig_page, bbox):
    pix = orig_page.get_pixmap(dpi=DPI, clip=bbox)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ouro = (r > 150) & (r - b > 60)          # pixel dourado (letra)
    cores = []
    for y in range(a.shape[0]):
        m = ouro[y]
        cores.append(a[y][m].mean(0) if m.sum() > 3 else None)
    # preenche linhas sem amostra com a vizinha
    ult = next(c for c in cores if c is not None)
    for i, c in enumerate(cores):
        if c is None: cores[i] = ult
        else: ult = c
    return np.array(cores), pix.height
def desenha(page, orig_page, s, texto):
    tam = s['size']; x0 = s['bbox'][0]; base = s['origin'][1]
    fnt = ImageFont.truetype(FONTE, int(round(tam * K)))
    asc, desc = fnt.getmetrics()
    w = int(fnt.getlength(texto)) + 10
    h = asc + desc
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).text((0, 0), texto, font=fnt, fill=255)
    cores, ph = gradiente(orig_page, pymupdf.Rect(s['bbox']))
    # alinha o degradê à linha de base: topo da caixa original = base - ascender
    topo_pdf = base - asc / K
    img = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        yy = int(round((topo_pdf + y / K - s['bbox'][1]) * K))
        yy = min(max(yy, 0), len(cores) - 1)
        img[y, :, :3] = cores[yy]
    img[..., 3] = np.array(mask)
    im = Image.fromarray(img, 'RGBA')
    import io; buf = io.BytesIO(); im.save(buf, 'PNG')
    rect = pymupdf.Rect(x0, topo_pdf, x0 + w / K, topo_pdf + h / K)
    if rect.x1 > page.rect.x1 - 8:
        f = (page.rect.x1 - 8 - x0) / rect.width
        rect = pymupdf.Rect(x0, base - (base - topo_pdf) * f, x0 + rect.width * f, base + (rect.y1 - base) * f)
    page.insert_image(rect, stream=buf.getvalue(), overlay=True)
def main(orig, entrada, saida):
    o = pymupdf.open(orig); d = pymupdf.open(entrada)
    for n, trocas in TROCAS.items():
        pg, po = d[n - 1], o[n - 1]
        alvo = [s for s in spans(pg) if s['text'].strip() in trocas]
        for s in alvo:
            pg.add_redact_annot(pymupdf.Rect(s['bbox']))
        pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
        for s in alvo:
            novo = trocas[s['text'].strip()]
            if novo: desenha(pg, po, s, novo)
    d.save(saida, garbage=3, deflate=True)
if __name__ == '__main__':
    main(*sys.argv[1:4])
