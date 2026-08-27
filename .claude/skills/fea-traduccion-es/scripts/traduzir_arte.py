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

def mascara_cor(img, faixa_hsv=((15,60,90),(40,255,255)), modo='cor', corte=140):
    """modo='cor': dourado sobre fundo escuro (padrão do material da FEA).
       modo='luz': texto claro sobre fundo escuro sem matiz (a capa em P&B)."""
    import cv2
    if modo == 'luz':
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.inRange(g, corte, 255)
    return cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), faixa_hsv[0], faixa_hsv[1])

def detecta_faixas(img, margem=0.08, corte=0.06, min_alt=12, modo='cor'):
    """Faixas horizontais com concentração de texto colorido."""
    m = mascara_cor(img, modo=modo); H, W = m.shape
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

def traduz(img, faixas, linhas, centro_x, margem=0.08, modo='cor',
           fundo_modo='inpaint'):
    import cv2
    from PIL import Image, ImageDraw, ImageFont
    H, W = img.shape[:2]
    m = mascara_cor(img, modo=modo)
    alvo = np.zeros_like(m)
    for a, b in faixas:
        alvo[a:b, int(W*margem):int(W*(1-margem))] = m[a:b, int(W*margem):int(W*(1-margem))]

    if fundo_modo == 'gradiente':
        # o fundo das faixas de título é um degradê liso: reconstruí-lo por
        # interpolação entre as linhas de cima e de baixo apaga TUDO — inclusive
        # a sombra projetada das letras, que o inpainting deixa passar
        fundo = img.copy()
        x0f, x1f = int(W*margem), int(W*(1-margem))
        for a, b in faixas:
            topo = img[max(a-4, 0):a, x0f:x1f].mean(axis=0)
            base = img[b:min(b+4, H), x0f:x1f].mean(axis=0)
            if not len(topo) or not len(base): continue
            n = b - a
            for i in range(n):
                t = (i + 1) / (n + 1)
                fundo[a+i, x0f:x1f] = (topo*(1-t) + base*t).astype(np.uint8)
    else:
        fundo = cv2.inpaint(img, cv2.dilate(alvo, np.ones((5,5),np.uint8), 2),
                            7, cv2.INPAINT_TELEA)

    # campo de textura: parte dos pixels do texto e espalha a folha metálica
    campo = img.copy()
    for a, b in faixas:
        campo[a:b] = cv2.inpaint(img[a:b], cv2.bitwise_not(alvo)[a:b], 12, cv2.INPAINT_TELEA)

    mascara = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(mascara)
    med = ImageDraw.Draw(Image.new('L', (8, 8)))

    def pedacos(l):
        """Uma linha pode misturar fontes (ex.: itálico + 'ARTI' em sans)."""
        return l.get('partes') or [dict(es=l['es'], fonte=l['fonte'])]

    def medida(l, s):
        larg = 0; topo = 10**9; base = -10**9
        for pc in pedacos(l):
            f = ImageFont.truetype(pc['fonte'], s)
            bb = med.textbbox((0, 0), pc['es'], font=f)
            larg += bb[2] - bb[0] if len(pedacos(l)) == 1 else f.getlength(pc['es'])
            topo = min(topo, bb[1]); base = max(base, bb[3])
        return larg, topo, base

    def corpo_que_cabe(l, lw, lh):
        melhor = None
        for s in range(14, 400):
            larg, topo, base = medida(l, s)
            if larg > lw or (base - topo) > lh*1.3: break
            melhor = s
        return melhor

    # corpo único por grupo, para as linhas de um mesmo bloco não desalinharem
    grupos = {}
    for l in linhas: grupos.setdefault(l.get('grupo', l['fonte']), []).append(l)
    usados = {}
    for g, ls in grupos.items():
        cands = [corpo_que_cabe(l, (l['x1']-l['x0'])*1.02, l['y1']-l['y0']) for l in ls]
        cands = [c for c in cands if c]
        if not cands: continue
        s = min(cands); usados[g] = s
        for l in ls:
            larg, topo, base = medida(l, s)
            x = l.get('x_centro', centro_x) - larg/2
            y = l['y0'] - topo
            pcs = pedacos(l)
            if len(pcs) == 1:
                f = ImageFont.truetype(pcs[0]['fonte'], s)
                bb = med.textbbox((0,0), pcs[0]['es'], font=f)
                dr.text((x - bb[0], l['y0'] - bb[1]), pcs[0]['es'], font=f, fill=255)
            else:
                for pc in pcs:
                    f = ImageFont.truetype(pc['fonte'], s)
                    dr.text((x, y), pc['es'], font=f, fill=255)
                    x += f.getlength(pc['es'])

    tm = (np.array(mascara).astype(np.float32)/255.0)[..., None]
    saida = (campo.astype(np.float32)*tm + fundo.astype(np.float32)*(1-tm)).astype(np.uint8)
    return saida, usados


def rotulos_em_caixa(img, rotulos, pad=3):
    """Segundo caminho, para rótulos de infográfico: em vez de detectar a cor do
    texto, recebe o retângulo exato de cada rótulo, apaga-o com a cor de fundo
    local e redesenha o espanhol centrado. Serve para texto escuro sobre fundo
    claro, onde a máscara por matiz não se aplica."""
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    pil = Image.fromarray(img[:, :, ::-1].copy())
    dr = ImageDraw.Draw(pil)
    med = ImageDraw.Draw(Image.new('L', (8, 8)))

    def cabe(r, s):
        f = ImageFont.truetype(r['fonte'], s)
        bb = med.textbbox((0, 0), r['es'], font=f)
        larg = (r['rect'][2] - r['rect'][0]) * r.get('folga', 1.06)
        alt = (r['rect'][3] - r['rect'][1]) * r.get('folga_alt', 2.2)
        return (bb[2]-bb[0]) <= larg and (bb[3]-bb[1]) <= alt

    grupos = {}
    for r in rotulos: grupos.setdefault(r.get('grupo', 'g'), []).append(r)
    usados = {}
    for g, rs in grupos.items():
        s = None
        for t in range(6, 200):
            if all(cabe(r, t) for r in rs): s = t
            else: break
        if s is None: s = 6
        usados[g] = s
    # 1) apaga
    for r in rotulos:
        x0, y0, x1, y1 = r['rect']
        cor = tuple(r.get('fundo') or cor_de_fundo(img, r['rect']))
        dr.rectangle([x0-pad, y0-pad, x1+pad, y1+pad], fill=cor)
    # 2) redesenha
    for r in rotulos:
        x0, y0, x1, y1 = r['rect']
        f = ImageFont.truetype(r['fonte'], usados[r.get('grupo', 'g')])
        bb = med.textbbox((0, 0), r['es'], font=f)
        cx = (x0 + x1)/2 - (bb[2]-bb[0])/2 - bb[0]
        cy = (y0 + y1)/2 - (bb[3]-bb[1])/2 - bb[1]
        if r.get('ancora') == 'esquerda': cx = x0 - bb[0]
        dr.text((cx, cy), r['es'], font=f, fill=tuple(r.get('cor', [0, 0, 0])))
    return np.array(pil)[:, :, ::-1].copy(), usados

def cor_de_fundo(img, rect, folga=6):
    """Cor mais frequente na moldura em volta do rótulo."""
    import numpy as np
    x0, y0, x1, y1 = [int(v) for v in rect]
    H, W = img.shape[:2]
    fora = img[max(y0-folga, 0):min(y1+folga, H), max(x0-folga, 0):min(x1+folga, W)]
    dentro = np.zeros(fora.shape[:2], bool)
    dentro[folga:folga+(y1-y0), folga:folga+(x1-x0)] = True
    px = fora[~dentro].reshape(-1, 3)
    if not len(px): return (255, 255, 255)
    med = np.median(px, axis=0).astype(int)
    return (int(med[2]), int(med[1]), int(med[0]))   # BGR -> RGB para o PIL

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('--pagina', type=int, required=True)
    ap.add_argument('--mapa'); ap.add_argument('--saida', default='arte_traduzida.pdf')
    ap.add_argument('--detectar', action='store_true')
    ap.add_argument('--png')
    ap.add_argument('--modo', default='cor', choices=['cor','luz'])
    ap.add_argument('--margem', type=float, default=0.08)
    a = ap.parse_args()
    import cv2
    doc, pg, xref, img = carrega(a.pdf, a.pagina)
    if a.detectar:
        print(json.dumps(dict(dimensoes=[img.shape[1], img.shape[0]],
                              faixas=detecta_faixas(img, modo=a.modo, margem=a.margem)), ensure_ascii=False, indent=1)); return
    cfg = json.load(open(a.mapa, encoding='utf-8'))
    if cfg.get('rotulos'):
        saida, corpos = rotulos_em_caixa(img, cfg['rotulos'])
    else:
      saida, corpos = traduz(img, cfg['faixas'], cfg['linhas'],
                           cfg.get('centro_x', img.shape[1]//2),
                           modo=cfg.get('modo', a.modo),
                           margem=cfg.get('margem', a.margem),
                           fundo_modo=cfg.get('fundo', 'inpaint'))
    tmp = a.png or '_arte_es.png'
    cv2.imwrite(tmp, saida)
    pg.replace_image(xref, filename=tmp)
    doc.save(a.saida, garbage=3, deflate=True)
    print(json.dumps(dict(saida=a.saida, pagina=a.pagina, corpos=corpos,
                          imagem=tmp), ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
