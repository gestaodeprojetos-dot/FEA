"""Texto dentro das imagens de página inteira (capa, contracapa, aberturas de capítulo).
Apaga as letras portuguesas por inpainting, só nos pixels da cor do texto e só dentro
da faixa medida, e redesenha em espanhol com Advent Pro (a fonte da arte, SIL OFL), no
mesmo centro, mesma altura de maiúscula e mesma cor. O dourado é preenchido com o campo
de textura extraído das próprias letras douradas do original."""
import pymupdf, cv2, numpy as np, sys, io
from PIL import Image, ImageDraw, ImageFont
F = {'bold': 'produccion/fontes-extra/AdventPro-Bold-OFL.ttf',
     'semi': 'produccion/fontes-extra/AdventPro-SemiBold-OFL.ttf',
     'medium': 'produccion/fontes-extra/AdventPro-Medium-OFL.ttf'}
CAP = 0.70
# (y0 apagar, y1 apagar, x0, x1, y0 maiúscula, y1 maiúscula, cor, texto ES, peso)
SUB = 'EN EL RELLENO CON ÁCIDO HIALURÓNICO'
CAIXA = 'DIAGNÓSTICO Y CONDUCTAS CLÍNICAS ANTE COMPLICACIONES ESTÉTICAS'
L = {
 1:   [(50, 228, 70, 1440, 89, 224, 'ouro', 'INTERCURRENCIAS', 'bold'),
       (234, 322, 80, 1440, 262, 313, 'branco', SUB, 'medium'),
       (1858, 1936, 100, 1420, 1874, 1922, 'branco', CAIXA, 'medium')],
 221: [(820, 976, 150, 1360, 854, 972, 'ouro', 'INTERCURRENCIAS', 'bold'),
       (976, 1058, 160, 1360, 993, 1049, 'branco', SUB, 'medium'),
       (1106, 1170, 185, 1332, 1117, 1158, 'branco', CAIXA, 'medium')],
}
def abertura(l1, l2, l1x=(423, 1101), l2x=(375, 1146)):
    return [(300, 397, l1x[0] - 10, l1x[1] + 10, 322, 393, 'branco', l1, 'medium'),
            (402, 508, l2x[0] - 10, l2x[1] + 10, 424, 504, 'branco', l2, 'medium')]
L[10] = abertura('INTERCURRENCIAS', 'AGUDAS ISQUÉMICAS')
L[78] = abertura('INTERCURRENCIAS', 'AGUDAS NO ISQUÉMICAS', l2x=(284, 1238))
L[129] = abertura('INTERCURRENCIAS', 'TARDÍAS ISQUÉMICAS', l2x=(366, 1154))
L[145] = abertura('INTERCURRENCIAS TARDÍAS', 'INFECCIOSAS E INFLAMATORIAS', l1x=(256, 1270), l2x=(185, 1345))
L[172] = abertura('INTERCURRENCIAS TARDÍAS', 'NO INFECCIOSAS', l1x=(255, 1269), l2x=(434, 1088))

def mascara(img, cor):
    if cor == 'ouro':
        return cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), (8, 60, 110), (42, 255, 255))
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    s = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 1]
    return ((g > 150) & (s < 80)).astype(np.uint8) * 255

def traduz(img, linhas):
    out = img.copy()
    for (a, b, x0, x1, c0, c1, cor, txt, peso) in linhas:
        reg = img[a:b, x0:x1]
        m = mascara(reg, cor)
        textura = None
        if cor == 'ouro':
            textura = cv2.inpaint(reg, cv2.bitwise_not(m), 5, cv2.INPAINT_TELEA)
        m = cv2.dilate(m, np.ones((5, 5), np.uint8))
        out[a:b, x0:x1] = cv2.inpaint(out[a:b, x0:x1], m, 9, cv2.INPAINT_TELEA)
        # texto novo
        capH = c1 - c0; tam = capH / CAP
        fnt = ImageFont.truetype(F[peso], int(round(tam)))
        larg = fnt.getlength(txt); disp = (x1 - x0) * 1.0
        if larg > disp:
            tam *= disp / larg; fnt = ImageFont.truetype(F[peso], int(round(tam)))
            larg = fnt.getlength(txt)
        asc, _ = fnt.getmetrics()
        cx = (x0 + x1) / 2
        W, H = out.shape[1], out.shape[0]
        mk = Image.new('L', (W, H), 0)
        ImageDraw.Draw(mk).text((cx - larg / 2, c1 - asc), txt, font=fnt, fill=255)
        mk = np.array(mk).astype(np.float32) / 255
        if cor == 'ouro':
            campo = out.copy().astype(np.float32)
            # campo de textura: repete o dourado original ao longo da faixa
            t = cv2.resize(textura, (W, b - a)) if textura.shape[1] < W else textura
            campo[a:b, :t.shape[1]] = t[:, :W]
            camada = campo
        else:
            amostra = reg[mascara(reg, cor) > 0]
            c = amostra.mean(0) if len(amostra) else np.array([255, 255, 255])
            camada = np.zeros_like(out, np.float32); camada[:] = c
        out = (out.astype(np.float32) * (1 - mk[..., None]) + camada * mk[..., None]).astype(np.uint8)
    return out

def main(entrada, saida, previa=None):
    d = pymupdf.open(entrada)
    for n, linhas in L.items():
        pg = d[n - 1]
        info = max(pg.get_images(full=True), key=lambda i: i[2] * i[3]); xref = info[0]
        px = pymupdf.Pixmap(d, xref)
        if px.n > 3 or px.alpha: px = pymupdf.Pixmap(pymupdf.csRGB, px)
        arr = np.frombuffer(px.samples, np.uint8).reshape(px.height, px.width, px.n)
        img = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        novo = traduz(img, linhas)
        ok, buf = cv2.imencode('.jpg', novo, [cv2.IMWRITE_JPEG_QUALITY, 93])
        pg.replace_image(xref, stream=buf.tobytes())
        if previa: cv2.imwrite(f'{previa}/arte{n}.jpg', novo)
    d.save(saida, garbage=3, deflate=True)
if __name__ == '__main__':
    main(*sys.argv[1:])
