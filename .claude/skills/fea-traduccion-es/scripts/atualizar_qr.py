#!/usr/bin/env python3
"""
Regenera os QR Codes de um PDF para apontar aos ativos traduzidos.

Por que não basta trocar o link: **o QR é imagem**. Não existe link a editar —
o destino está codificado nos módulos preto-e-branco. Trocar o destino exige
gerar um QR novo e substituir a imagem na arte.

Como funciona:
  1. Detecta e decodifica cada QR da página (OpenCV, 300 e 450 dpi).
  2. Casa o destino decodificado com o mapa de links traduzidos, pelo ID do
     arquivo — não pela URL inteira, que muda de forma (?usp=, ?t=).
  3. Gera o QR novo no mesmo tamanho e na mesma posição, com zona de silêncio
     branca, e o sobrepõe. A moldura decorativa da arte é preservada.
  4. Confere lendo de volta o QR gerado: se não decodificar para o link
     esperado, aborta a página e reporta.

Uso:
    python3 atualizar_qr.py entrada.pdf links_es.json --saida saida.pdf
    python3 atualizar_qr.py entrada.pdf links_es.json --conferir   # só relatório

O mapa é {id_do_destino_original: url_traduzida}.
"""
import sys, os, json, re, argparse, io

def id_de(url):
    m = re.search(r'/d/([\w-]+)', url) or re.search(r'(?:v=|shorts/)([\w-]+)', url)
    return m.group(1) if m else None

def detecta(page, dpis=(300, 450)):
    """QRs da página: (quad em coordenadas do PDF, texto decodificado)."""
    import pymupdf, cv2, numpy as np
    achados = []
    for dpi in dpis:
        pix = page.get_pixmap(dpi=dpi)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        img = cv2.cvtColor(img, {1: cv2.COLOR_GRAY2BGR, 3: cv2.COLOR_RGB2BGR,
                                 4: cv2.COLOR_RGBA2BGR}[pix.n])
        ok, textos, pts, _ = cv2.QRCodeDetectorAruco().detectAndDecodeMulti(img) \
             if hasattr(cv2, 'QRCodeDetectorAruco') else cv2.QRCodeDetector().detectAndDecodeMulti(img)
        if not ok: continue
        esc = 72.0/dpi
        novos = []
        for t, quad in zip(textos, pts):
            if not t.strip(): continue
            xs = [p[0]*esc for p in quad]; ys = [p[1]*esc for p in quad]
            r = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
            if any(t == a[1] for a in achados): continue
            novos.append((r, t))
        achados.extend(novos)
        if novos: break
    return achados

def gera_qr(texto, lado_px):
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=1)
    qr.add_data(texto); qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
    return img.resize((lado_px, lado_px))

def confere(png_bytes, esperado):
    import cv2, numpy as np
    arr = cv2.imdecode(np.frombuffer(png_bytes, np.uint8), cv2.IMREAD_COLOR)
    t, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
    return t == esperado

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('mapa')
    ap.add_argument('--saida', default='qr_atualizado.pdf')
    ap.add_argument('--conferir', action='store_true')
    ap.add_argument('--paginas', default='')
    a = ap.parse_args()
    import pymupdf
    from PIL import Image

    links = json.load(open(a.mapa, encoding='utf-8'))
    doc = pymupdf.open(a.pdf)
    alvo = ([int(x) for x in a.paginas.split(',')] if a.paginas
            else list(range(1, doc.page_count+1)))
    trocados, mantidos, erros = [], [], []

    for n in alvo:
        page = doc[n-1]
        for rect, texto in detecta(page):
            ident = id_de(texto)
            destino = links.get(ident)
            if not destino:
                mantidos.append(dict(pagina=n, id=ident, motivo='sem link ES (artigo)'))
                continue
            if a.conferir:
                trocados.append(dict(pagina=n, de=texto, para=destino)); continue
            lado = int(max(rect.width, rect.height)*300/72)
            img = gera_qr(destino, lado)
            buf = io.BytesIO(); img.save(buf, 'PNG'); png = buf.getvalue()
            if not confere(png, destino):
                erros.append(dict(pagina=n, id=ident, erro='QR gerado não decodifica para o destino'))
                continue
            # zona de silêncio branca antes de assentar o novo QR
            folga = max(rect.width, rect.height)*0.03
            alvoR = pymupdf.Rect(rect.x0-folga, rect.y0-folga, rect.x1+folga, rect.y1+folga)
            page.draw_rect(alvoR, color=None, fill=(1, 1, 1))
            page.insert_image(alvoR, stream=png, keep_proportion=True)
            trocados.append(dict(pagina=n, de=texto, para=destino,
                                 rect=[round(v, 1) for v in rect]))
    if not a.conferir:
        doc.save(a.saida, garbage=3, deflate=True)
    print(json.dumps(dict(saida=None if a.conferir else a.saida,
                          trocados=len(trocados), mantidos=len(mantidos),
                          erros=erros, detalhe=trocados), ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
