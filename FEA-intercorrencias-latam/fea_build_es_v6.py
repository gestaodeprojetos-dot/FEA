"""Gera 'Intercorrencias ES v6.pdf' a partir do PDF ES atual + v6 do Gerson.
Uso: python3 -I fea_build_es_v6.py DIR_DL DIR_FONTES SAIDA.pdf
"""
import io
import re
import sys

import numpy as np
import pymupdf as fitz
from PIL import Image

DL, FD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
v = fitz.open(f"{DL}/v6.pdf")
e = fitz.open(f"{DL}/es.pdf")
log = []

FONTS = {
    "hnr": f"{FD}/HelveticaNeue.ttf",
    "hnb": f"{FD}/HelveticaNeue-Bold.ttf",
    "hncb": f"{FD}/HelveticaNeue-CondensedBold.ttf",
    "gter": f"{FD}/GuardianTextEgyp-Regular.otf",
    "hpdb": f"{FD}/HeadingProDouble-Bold.otf",
}
FOBJ = {k: fitz.Font(fontfile=p) for k, p in FONTS.items()}


def pil_of(doc, xref):
    d = doc.extract_image(xref)
    return Image.open(io.BytesIO(d["image"])).convert("RGB"), d


def jpeg(im, q=93):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, subsampling=0, optimize=True)
    return b.getvalue()


def bbox_of(page, xref):
    for i in page.get_image_info(xrefs=True):
        if i["xref"] == xref:
            return fitz.Rect(i["bbox"])
    raise KeyError(xref)


def cover_crop(im, w, h, anchor_y=0.5):
    """Recorta im para a proporção w:h (sem distorcer), centralizado."""
    W, H = im.size
    tgt = w / h
    if W / H > tgt:  # imagem mais larga: corta laterais
        nw = round(H * tgt)
        x0 = (W - nw) // 2
        return im.crop((x0, 0, x0 + nw, H))
    nh = round(W / tgt)
    y0 = round((H - nh) * anchor_y)
    return im.crop((0, y0, W, y0 + nh))


def replace(p, es_xref, v6_xref, anchor_y=0.5):
    page = e[p - 1]
    r = bbox_of(page, es_xref)
    im, d = pil_of(v, v6_xref)
    a_es = r.width / r.height
    a_v6 = im.size[0] / im.size[1]
    if abs(a_es / a_v6 - 1) < 0.015 and d["ext"] in ("jpeg", "jpg") and d.get("colorspace") == 3:
        page.replace_image(es_xref, stream=d["image"])
        log.append(f"p{p}: imagem xref {es_xref} trocada pela v6 (xref {v6_xref}), mesmo enquadramento")
    else:
        im2 = cover_crop(im, r.width, r.height, anchor_y)
        page.replace_image(es_xref, stream=jpeg(im2))
        log.append(f"p{p}: imagem xref {es_xref} trocada pela v6 (xref {v6_xref}) recortada para o quadro ES "
                   f"({a_v6:.2f}->{a_es:.2f})")


# ---------- texto ----------
def redact(page, rects):
    for r in rects:
        page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)




def stripped(doc, pno, keep_span, drop_images=False, keep_rect=None):
    """Cópia de 1 página sem o texto que não interessa (para show_pdf_page não carregar texto oculto)."""
    t = fitz.open()
    t.insert_pdf(doc, from_page=pno, to_page=pno)
    tp = t[0]
    n = 0
    for b in tp.get_text("dict")["blocks"]:
        if b["type"]:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if not keep_span(s):
                    tp.add_redact_annot(fitz.Rect(s["bbox"]), fill=False)
                    n += 1
    if n:
        tp.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                            text=fitz.PDF_REDACT_TEXT_REMOVE)
    if drop_images:
        for im in tp.get_images(full=True):
            tp.delete_image(im[0])
    return t

# 1) Aberturas de capitulo: imagem v6 com a faixa do titulo vinda do ES (titulo em espanhol gravado na arte)
for p, xv, xe in [(10, 57, 62), (78, 1244, 264), (129, 1119, 14905), (145, 962, 14928)]:
    A, _ = pil_of(v, xv)
    B, _ = pil_of(e, xe)
    a = np.asarray(A).astype(np.int16)
    b = np.asarray(B).astype(np.int16)
    rows = np.abs(a - b).mean(axis=(1, 2))
    lo, hi = 480, 545
    cut = lo + int(np.argmin(rows[lo:hi]))
    out = np.asarray(A).copy()
    # costura suave de 6 px
    out[:cut - 3] = np.asarray(B)[:cut - 3]
    for k in range(6):
        y = cut - 3 + k
        t = (k + 1) / 7
        out[y] = (np.asarray(B)[y] * (1 - t) + np.asarray(A)[y] * t).astype(np.uint8)
    e[p - 1].replace_image(xe, stream=jpeg(Image.fromarray(out), 94))
    log.append(f"p{p}: abertura de capítulo com a imagem nova da v6; faixa do título (linhas 0-{cut}px) "
               f"mantida do ES (diferença na costura {rows[cut]:.1f}/255)")

# 2) Figuras com o mesmo enquadramento no ES e na v6
SAME = [(25, 109, 147), (44, 14760, 300), (70, 14823, 453), (70, 235, 456), (98, 14869, 1381),
        (98, 14870, 1382), (135, 14913, 1189), (148, 14932, 1003), (153, 14938, 1032), (179, 14967, 861),
        (180, 14969, 866), (180, 14971, 867), (181, 14974, 871), (181, 14975, 872), (182, 14978, 876),
        (185, 564, 886)]
for p, xe, xv in SAME:
    replace(p, xe, xv)

# 3) Figuras em que o ES tem quadro diferente (texto ES mais longo): v6 recortada para o quadro ES
for p, xe, xv in [(31, 14731, 191), (31, 14732, 193), (34, 14738, 218), (34, 14739, 220), (34, 14740, 222),
                  (177, 14964, 849)]:
    replace(p, xe, xv)

# 4) p167: duas fotos novas da v6 no lugar da montagem unica do ES (mesma area)
pg = e[166]
pg.delete_image(505)
R = fitz.Rect(55, 178, 399, 348)
pg.show_pdf_page(R, stripped(v, 166, lambda sp: False), 0, clip=R)
log.append("p167: Fig. 51 passou a ter as 2 fotos da v6 (área 55-399 x 178-348 copiada da v6)")

# 5) p72: Fig. 32 da v6 com rotulos; 'CASE n' -> 'CASO n'
case_spans = [sp for b in v[71].get_text("dict")["blocks"] if not b["type"] for l in b["lines"]
              for sp in l["spans"] if sp["text"].startswith("CASE")]
tmp = stripped(v, 71, lambda sp: sp["text"].strip() in list("ABCDEF"))
pg = e[71]
pg.delete_image(14830)
R = fitz.Rect(55, 97, 399, 257)
pg.show_pdf_page(R, tmp, 0, clip=R)
pg.insert_font(fontname="hncb", fontfile=FONTS["hncb"])
for s in case_spans:
    txt = s["text"].replace("CASE", "CASO")
    pg.insert_text(fitz.Point(s["origin"]), txt, fontname="hncb", fontsize=s["size"], color=(1, 1, 1))
# legenda ES desce 5 pt para manter o respiro abaixo da figura v6 (que é 7 pt mais alta que a do ES)
src_es = fitz.open(f"{DL}/es.pdf")
redact(pg, [(55, 256.5, 401, 345)])
C = fitz.Rect(55, 255, 401, 345)
pg.show_pdf_page(C + (0, 5, 0, 5), stripped(src_es, 71, lambda sp: fitz.Rect(sp['bbox']) in C, drop_images=True), 0, clip=C)
log.append("p72: Fig. 32 trocada pela v6 com círculos A a F e rótulos traduzidos CASO 1 a CASO 6")


def layout(tokens, width, size):
    """tokens: [(palavra, fonte)] -> linhas (lista de tokens), quebra gulosa."""
    lines, cur, w = [], [], 0
    for t in tokens:
        if t == "\n":
            lines.append((cur, True))
            cur, w = [], 0
            continue
        tw = FOBJ[t[1]].text_length(t[0], size)
        sp = FOBJ["hnr" if t[1].startswith("hn") else t[1]].text_length(" ", size)
        add = tw if not cur else w + sp + tw
        if cur and add > width:
            lines.append((cur, False))
            cur, w = [t], tw
        else:
            cur.append(t)
            w = add
    if cur:
        lines.append((cur, True))
    return lines


def draw_par(page, tokens, x0, x1, y0, size, lead, color=(0, 0, 0), justify=True):
    for k in set(t[1] for t in tokens if t != "\n"):
        page.insert_font(fontname=k, fontfile=FONTS[k])
    y = y0
    out = []
    for words, last in layout(tokens, x1 - x0, size):
        widths = [FOBJ[f].text_length(w, size) for w, f in words]
        nat_sp = FOBJ["hnr" if words[0][1].startswith("hn") else words[0][1]].text_length(" ", size)
        if justify and not last and len(words) > 1:
            sp = (x1 - x0 - sum(widths)) / (len(words) - 1)
        else:
            sp = nat_sp
        x = x0
        for (w, f), ww in zip(words, widths):
            page.insert_text(fitz.Point(x, y), w, fontname=f, fontsize=size, color=color)
            x += ww + sp
        out.append((" ".join(w for w, _ in words), round(y, 2), round(sp / nat_sp, 2)))
        y += lead
    return out


def toks(text, font, bold_prefix=None):
    r = []
    if bold_prefix:
        r.append((bold_prefix, "hnb"))
    r += [(w, font) for w in text.split()]
    return r


def center_line(page, text, cx, y, font, size, color):
    page.insert_font(fontname=font, fontfile=FONTS[font])
    w = FOBJ[font].text_length(text, size)
    page.insert_text(fitz.Point(cx - w / 2, y), text, fontname=font, fontsize=size, color=color)
    return round(cx - w / 2, 1), round(cx + w / 2, 1)


# p28 - fonte da Fig. 10 (SOARES, confirmado pela autora em 24/11/2026; a v6 trazia ISOARES)
pg = e[27]
redact(pg, [(283, 460.5, 401, 499)])
r = draw_par(pg, toks("SOARES, D. J. (2022), figura 13.", "hnr", "Fuente:"), 283.54, 399.8, 467.86, 7, 9.5,
             justify=False)
log.append(f"p28: fonte da Fig. 10 -> {r}")

# p93 - titulo da Fig. 36 com numero
pg = e[92]
redact(pg, [(95, 252, 392, 263.5), (200, 264.8, 285, 276)])
gold = (0xC7 / 255, 0x87 / 255, 0x1E / 255)
a = center_line(pg, "FIGURA 36. EDEMA AGUDO TRANSITORIO TRAS RELLENO", 226.77, 260.71, "hpdb", 10, gold)
b = center_line(pg, "CON ÁCIDO HIALURÓNICO", 226.77, 273.21, "hpdb", 10, gold)
log.append(f"p93: título Fig. 36 numerado (linhas x {a} e {b})")

# p177 - legenda Fig. 53
pg = e[176]
redact(pg, [(288, 161.5, 401, 192)])
t = toks("Migración del ácido hialurónico tras relleno labial. Se observa acumulación de producto en la "
         "región perioral, más allá de los límites anatómicos de la mucosa labial, lo que caracteriza la "
         "migración del relleno.", "hnr", "Fig. 53:")
t += ["\n"] + toks("archivo clínico de los autores. Caso autorizado para uso académico y científico.", "hnr",
                   "Fuente:")
r = draw_par(pg, t, 289.0, 400.0, 169.86, 7, 9.0)
log.append(f"p177: legenda Fig. 53 nova ({len(r)} linhas, última base y={r[-1][1]})")

# p200 - item reescrito
pg = e[199]
redact(pg, [(74, 446.5, 401, 459), (74, 467.5, 401, 480)])
r = draw_par(pg, toks("Los procedimientos repetidos innecesarios pueden causar fibrosis e irregularidades "
                      "permanentes.", "gter"), 74.69, 400.4, 455.69, 11, 21.0)
log.append(f"p200: item reescrito -> {r}")


# p2 (defeito herdado do ES antigo): acento do "Í" de ÍNDICE pintado com o padrão /P2, que estava sem
# definição nos recursos (/Shading <</P2 null>>). Copia o degradê dourado da v6 (mesmo padrão do SUMÁRIO).
def copy_obj(xref, memo):
    if xref in memo:
        return memo[xref]
    new = e.get_new_xref()
    memo[xref] = new
    src = v.xref_object(xref, compressed=True)
    src = re.sub(r"(\d+) 0 R", lambda m: f"{copy_obj(int(m.group(1)), memo)} 0 R", src)
    e.update_object(new, src)
    return new


pat = copy_obj(3, {})
pg2 = e[1]
e.xref_set_key(pg2.xref, "Resources/Shading", "null")
e.xref_set_key(pg2.xref, "Resources/Pattern", f"<</P2 {pat} 0 R>>")
log.append(f"p2: padrão /P2 do acento de ÍNDICE restaurado (obj {pat}, degradê da v6)")

e.set_metadata({**e.metadata, "title": "Intercurrencias en el relleno con ácido hialurónico",
                "author": "Dr. João Pithon", "subject": "Edición en español, actualizada a la v6",
                "modDate": fitz.get_pdf_now()})
e.save(OUT, garbage=3, deflate=True, clean=False)
print("\n".join(log))
