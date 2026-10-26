"""Rótulos em português dentro de figuras (gráfico, esquema, tabela em imagem).
Cada rótulo: retângulo exato na imagem (px), apagado com a cor de fundo local e
redesenhado em espanhol, centrado/alinhado como o original, em Liberation Sans
(métrica da Arial, a mais próxima da Helvetica dos rótulos)."""
import pymupdf, numpy as np, sys, cv2
from PIL import Image, ImageDraw, ImageFont
R = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
B = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
# página: [(x0,y0,x1,y1, texto ES, alinhamento 'l'|'r'|'c', negrito)]
TAM = {20: 17, 39: 18, 54: 23, 122: 22}
TAM_ESP = {(122,'Clasificación de la presión arterial en adultos'): 30, (122,'Adaptado de las Directrices de la Sociedad Brasileña de Cardiología'): 20, (39,'Tejido cicatricial'): 30}
P = {
 20: [(118,18,262,40,'Punta nasal (8%)','r',0),(66,71,252,92,'Labio superior (6%)','r',0),
      (450,98,508,120,'Surco','c',1),(14,126,217,148,'Mentón/Mandíbula (3%)','r',0),
      (54,170,212,191,'Labio inferior (1%)','r',0),(2,208,168,230,'Mejilla anterior','r',0),
      (94,260,175,281,'Sien','r',0),(140,306,233,327,'Frente (3%)','r',0),
      (103,445,227,466,'Sien (2%)','r',0),(66,489,232,511,'Punta nasal (4%)','r',0),
      (111,563,226,584,'Frente (11%)','r',0),(252,862,348,879,'Punta nasal','c',0),
      (278,947,358,969,'Sien','c',0)],
 39: [(785,122,1135,150,'Relleno intraarterial','l',0),(36,286,168,310,'Flujo arterial','l',0),
      (735,341,1048,368,'Trayecto de la aguja','c',0),(735,368,1048,395,'(el relleno sigue el','c',0),
      (735,395,1048,423,'camino de menor resistencia)','c',0),(205,436,360,491,'Tejido cicatricial','l',0),
      (496,574,645,599,'Relleno','l',0)],
 54: [(15,69,188,99,'región frontal','c',0),(54,101,151,126,'inferior','c',0),
      (210,68,368,99,'tercio medio','c',0),(232,101,346,130,'superior','c',0),
      (427,69,522,93,'nariz y','c',0),(424,101,524,131,'glabela','c',0),
      (566,68,765,99,'tercio medio de','c',0),(584,100,746,125,'la cara y surco','c',0),
      (796,70,908,93,'mentón y','c',0),(781,100,924,125,'mandíbula','c',0),(994,68,1077,93,'labios','c',0)],
 122:[(150,22,980,70,'Clasificación de la presión arterial en adultos','c',0),
      (80,118,272,156,'Clasificación','c',1),(790,118,1090,156,'Interpretación clínica','c',1),
      (128,180,224,214,'Óptima','c',0),(850,184,1030,214,'niveles ideales','c',0),
      (766,248,1115,284,'sin alteraciones relevantes','c',0),(820,313,1060,342,'riesgo aumentado','c',0),
      (30,377,316,412,'Hipertensión estadio 1','c',0),(820,377,1060,412,'requiere evaluación','c',0),
      (30,441,320,476,'Hipertensión estadio 2','c',0),(815,444,1066,476,'requiere tratamiento','c',0),
      (30,505,320,540,'Hipertensión estadio 3','c',0),(870,505,1012,534,'alto riesgo','c',0),
      (200,575,930,607,'Adaptado de las Directrices de la Sociedad Brasileña de Cardiología','c',0)],
}
def fundo(a, x0, y0, x1, y1):
    borda = np.concatenate([a[y0-2:y0, x0:x1].reshape(-1,3), a[y1:y1+2, x0:x1].reshape(-1,3),
                            a[y0:y1, x0-2:x0].reshape(-1,3), a[y0:y1, x1:x1+2].reshape(-1,3)])
    return tuple(int(v) for v in np.median(borda, 0))
def tinta(a, x0, y0, x1, y1, bg):
    reg = a[y0:y1, x0:x1].reshape(-1,3).astype(int)
    dist = np.abs(reg - np.array(bg)).sum(1)
    escuros = reg[dist > dist.max()*0.6] if dist.max() > 60 else reg
    return tuple(int(v) for v in np.median(escuros, 0))
def main(entrada, saida):
    d = pymupdf.open(entrada)
    for n, rot in P.items():
        pg = d[n-1]
        info = max(pg.get_images(full=True), key=lambda i: i[2]*i[3]); xref = info[0]
        px = pymupdf.Pixmap(d, xref)
        if px.n > 3 or px.alpha: px = pymupdf.Pixmap(pymupdf.csRGB, px)
        a = np.frombuffer(px.samples, np.uint8).reshape(px.height, px.width, 3).copy()
        for x0,y0,x1,y1,txt,al,ng in rot:
            x0 = max(x0 - 5, 3); x1 += 3
            bg = fundo(a, x0, y0, x1, y1); cor = tinta(a, x0, y0, x1, y1, bg)
            reg = a[y0:y1, x0:x1].astype(int)
            m = (np.abs(reg - np.array(bg)).sum(2) > 90).astype(np.uint8)
            # fios da tabela e linhas de chamada longas não são texto: ficam
            def escuro(px): return np.abs(px.astype(int) - np.array(bg)).sum(-1) > 90
            col = (m.sum(0) > 0.8 * (y1 - y0)) & escuro(a[y0-3, x0:x1]) & escuro(a[min(y1+2, a.shape[0]-1), x0:x1])
            lin = (m.sum(1) > 0.8 * (x1 - x0)) & escuro(a[y0:y1, x0-3]) & escuro(a[y0:y1, min(x1+2, a.shape[1]-1)])
            m[:, col] = 0; m[lin, :] = 0
            m = cv2.dilate(m * 255, np.ones((3, 3), np.uint8))
            a[y0:y1, x0:x1] = cv2.inpaint(np.ascontiguousarray(a[y0:y1, x0:x1]), m, 4, cv2.INPAINT_TELEA)
            im = Image.fromarray(a); dr = ImageDraw.Draw(im)
            x1 -= 3
            alt = TAM_ESP.get((n, txt), TAM[n])
            f = ImageFont.truetype(B if ng else R, max(8, int(alt)))
            w = f.getlength(txt)
            if al == 'c' and w > (x1 - x0) * 1.15:
                f = ImageFont.truetype(B if ng else R, max(8, int(alt * (x1-x0)*1.15 / w))); w = f.getlength(txt)
            x = {'l': x0, 'r': x1 - w, 'c': (x0 + x1 - w) / 2}[al]
            asc, desc = f.getmetrics()
            dr.text((x, (y0 + y1)/2 - (asc + desc)/2 + desc*0.3), txt, font=f, fill=cor)
            a = np.array(im)
        import io; buf = io.BytesIO(); Image.fromarray(a).save(buf, 'PNG')
        pg.replace_image(xref, stream=buf.getvalue())
    d.save(saida, garbage=3, deflate=True)
if __name__ == '__main__':
    main(*sys.argv[1:3])
