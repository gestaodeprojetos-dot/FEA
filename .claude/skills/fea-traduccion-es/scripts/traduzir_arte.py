#!/usr/bin/env python3
"""
Traduz o texto que está DENTRO das imagens de um PDF — capa, aberturas de
capítulo, rótulos de infográfico. Esse texto não é texto: é pixel, e nenhuma
ferramenta de PDF o alcança.

Estratégia, em três passos:
  1. Detecta os pixels do texto por cor (o material da FEA usa dourado sobre
     fundo escuro) e delimita as FAIXAS de texto por perfil de linha, para nunca
     tocar em moldura nem em fotografia.
  2. Reconstrói o fundo sob o texto por inpainting (Telea). Como os traços são
     finos em relação ao fundo, o remendo fica invisível.
  3. Redesenha o texto em espanhol na mesma posição, corpo e cor — e, para
     reproduzir o acabamento de folha metálica, preenche as letras com um CAMPO
     DE TEXTURA extraído dos próprios pixels dourados do original, em vez de
     cor chapada.

Uso:
    python3 traduzir_arte.py original.pdf --pagina 1 --mapa capa.json --saida out.pdf
    python3 traduzir_arte.py original.pdf --pagina 1 --detectar   # mede as faixas

Formato do mapa (capa.json):
    {"faixas": [[185,535],[636,695]],
     "linhas": [{"es":"RELLENO","x0":231,"x1":1302,"y0":193,"y1":283,
                 "fonte":"fontes/HelveticaNeue-BoldES.ttf"}, ...],
     "centro_x": 760}
"""
import sys, os, json, argparse
import numpy as np

def carrega(pdf, pagina):
    import pymupdf, cv2
    doc = pymupdf.open(pdf)
    pg = doc[pagina-1]
    imgs = pg.get_images(full=True)
    if not imgs: raise SystemExit('a página %d não tem imagem' % pagina)
    imgs.sort(key=lambda i: -(i[2]*i[3]))          # a maior primeiro
    xref = imgs[0][0]
    px = pymupdf.Pixmap(doc, xref)
    if px.n == 4: px = pymupdf.Pixmap(pymupdf.csRGB, px)
    arr = np.frombuffer(px.samples, dtype=np.uint8).reshape(px.height, px.width, px.n)
    return doc, pg, xref, cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def mascara_cor(img, faixa_hsv=((15,60,90),(40,255,255))):
    import cv2
    return cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), faixa_hsv[0], faixa_hsv[1])

def detecta_faixas(img, margem=0.08, corte=0.06, min_alt=12):
    """Faixas horizontais com concentração de texto colorido."""
    m = mascara_cor(img); H, W = m.shape
    interior = m[:, int(W*margem):int(W*(1-margem))]
    perfil = interior.sum(axis=1)/255
    lim = perfil.max()*corte
    faixas, ini = [], None
    for y, v in enumerate(perfil):
        if v > lim and ini is None: ini = y
        elif v <= lim and ini is not None:
            if y-ini >= min_alt:
                xs = np.where(interior[ini:y].sum(axis=0) > 0)[0]
                faixas.append(dict(y0=ini, y1=y, alt=y-ini,
                                   x0=int(xs.min()+W*margem) if len(xs) else 0,
                                   x1=int(xs.max()+W*margem) if len(xs) else 0,
                                   px=int(perfil[ini:y].sum())))
            ini = None
    return faixas

def traduz(img, faixas, linhas, centro_x, margem=0.08):
    import cv2
    from PIL import Image, ImageDraw, ImageFont
    H, W = img.shape[:2]
    m = mascara_cor(img)
    alvo = np.zeros_like(m)
    for a, b in faixas:
        alvo[a:b, int(W*margem):int(W*(1-margem))] = m[a:b, int(W*margem):int(W*(1-margem))]

    fundo = cv2.inpaint(img, cv2.dilate(alvo, np.ones((5,5),np.uint8), 2), 7, cv2.INPAINT_TELEA)

    # campo de textura: parte dos pixels do texto e espalha a folha metálica
    campo = img.copy()
    for a, b in faixas:
        campo[a:b] = cv2.inpaint(img[a:b], cv2.bitwise_not(alvo)[a:b], 12, cv2.INPAINT_TELEA)

    mascara = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(mascara)
    med = ImageDraw.Draw(Image.new('L', (8, 8)))

    def corpo_que_cabe(fp, txt, lw, lh):
        melhor = None
        for s in range(14, 400):
            f = ImageFont.truetype(fp, s)
            bb = med.textbbox((0,0), txt, font=f)
            if (bb[2]-bb[0]) > lw or (bb[3]-bb[1]) > lh*1.3: break
            melhor = (s, f)
        return melhor

    # corpo único por grupo, para as linhas de um mesmo bloco não desalinharem
    grupos = {}
    for l in linhas: grupos.setdefault(l.get('grupo', l['fonte']), []).append(l)
    usados = {}
    for g, ls in grupos.items():
        cands = [corpo_que_cabe(l['fonte'], l['es'], (l['x1']-l['x0'])*1.02, l['y1']-l['y0'])
                 for l in ls]
        cands = [c for c in cands if c]
        if not cands: continue
        s = min(c[0] for c in cands); usados[g] = s
        for l in ls:
            f = ImageFont.truetype(l['fonte'], s)
            bb = med.textbbox((0,0), l['es'], font=f)
            x = l.get('x_centro', centro_x) - (bb[2]-bb[0])/2 - bb[0]
            dr.text((x, l['y0']-bb[1]), l['es'], font=f, fill=255)

    tm = (np.array(mascara).astype(np.float32)/255.0)[..., None]
    saida = (campo.astype(np.float32)*tm + fundo.astype(np.float32)*(1-tm)).astype(np.uint8)
    return saida, usados

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('--pagina', type=int, required=True)
    ap.add_argument('--mapa'); ap.add_argument('--saida', default='arte_traduzida.pdf')
    ap.add_argument('--detectar', action='store_true')
    ap.add_argument('--png')
    a = ap.parse_args()
    import cv2
    doc, pg, xref, img = carrega(a.pdf, a.pagina)
    if a.detectar:
        print(json.dumps(dict(dimensoes=[img.shape[1], img.shape[0]],
                              faixas=detecta_faixas(img)), ensure_ascii=False, indent=1)); return
    cfg = json.load(open(a.mapa, encoding='utf-8'))
    saida, corpos = traduz(img, cfg['faixas'], cfg['linhas'],
                           cfg.get('centro_x', img.shape[1]//2))
    tmp = a.png or '_arte_es.png'
    cv2.imwrite(tmp, saida)
    pg.replace_image(xref, filename=tmp)
    doc.save(a.saida, garbage=3, deflate=True)
    print(json.dumps(dict(saida=a.saida, pagina=a.pagina, corpos=corpos,
                          imagem=tmp), ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
