"""Aberturas de capítulo (págs. 10, 78, 129, 145, 172): o cabeçalho corrido em
português fica escondido sob a arte, invisível, mas continua na camada de texto
(busca, cópia, leitor de tela). Remove só o texto, sem tocar imagem nem vetor."""
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
for n in (10, 78, 129, 145, 172):
    p = d[n - 1]
    for r in p.search_for('INTERCORRÊNCIAS NO PREENCHIMENTO COM ÁCIDO HIALURÔNICO'):
        p.add_redact_annot(r + (-1, -1, 1, 1))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                       graphics=pymupdf.PDF_REDACT_LINE_ART_NONE, text=pymupdf.PDF_REDACT_TEXT_REMOVE)
d.save(sys.argv[2], garbage=3, deflate=True)
