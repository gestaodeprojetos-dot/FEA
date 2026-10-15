"""Biblioteca comum para recompor artes FEA em espanhol trocando SÓ a copy.

Princípio: foto, layout, cores e fontes do original ficam intactos. O texto
original é apagado com inpainting clássico (OpenCV Telea, sem IA generativa) e
a tradução é escrita na mesma fonte, tamanho (calibrado pela largura medida do
texto original), cor e linha de base. Nunca gerar imagem por IA.

Uso típico num script de criativo:
    from fea_arte_lib import *
    im = abrir('trabalho/ads03-feed.png')
    caixa = (x0, y0, x1, y1)                       # região do texto
    cor = cor_texto(im, caixa, CLARO)
    im = apagar(im, caixa, CLARO)
    escrever(im, ['linha pt 1', 'linha pt 2'], ['linea es 1', 'linea es 2'],
             [(y_topo1, x0_1, x1_1), (y_topo2, x0_2, x1_2)], fonte('Montserrat_700Bold'), cor)
    salvar(im, 'FEA-Ads 03 - PTO-LATAM - Feed.png')

Medição: medir(im, caixa, cond) imprime topo, base e x de cada linha de texto.
Fontes: fonte('Montserrat_700Bold') procura em fea_artes/fontes; se faltar a
família, baixar_fonte('poppins') usa o npm (@expo-google-fonts/<familia>).
Preço: PRECOS['preco'] etc. vêm de precos.json (dólar, formato LATAM US$19,00).
"""
import glob, json, os, subprocess, tarfile, tempfile
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, 'fontes')
SAIDA = os.path.join(os.path.dirname(AQUI), 'FEA-artes-ES')
PRECOS = json.load(open(os.path.join(AQUI, 'precos.json'), encoding='utf-8'))

CLARO = lambda r, g, b: (r > 150) & (g > 150) & (b > 150)
ESCURO = lambda r, g, b: (r < 110) & (g < 110) & (b < 110)


def abrir(caminho):
    return Image.open(caminho).convert('RGB')


def salvar(im, nome, qualidade=95):
    os.makedirs(SAIDA, exist_ok=True)
    p = os.path.join(SAIDA, nome)
    if nome.lower().endswith(('.jpg', '.jpeg')):
        im.save(p, quality=qualidade, subsampling=0)
    else:
        im.save(p, optimize=True)
    return p


def decodificar_download(json_salvo, destino):
    """O download_file_content do Drive salva um JSON com base64 em 'content'."""
    import base64
    d = json.load(open(json_salvo))
    open(destino, 'wb').write(base64.b64decode(d['content']))
    return destino


def baixar_fonte(familia):
    """familia no formato do npm: 'poppins', 'open-sans', 'bebas-neue'..."""
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['npm', 'pack', f'@expo-google-fonts/{familia}', '--silent'], cwd=t, check=True, capture_output=True)
        tgz = glob.glob(os.path.join(t, '*.tgz'))[0]
        with tarfile.open(tgz) as tf:
            for m in tf.getmembers():
                if m.name.endswith('.ttf'):
                    m.name = os.path.basename(m.name)
                    tf.extract(m, FONTES)
    return sorted(os.path.basename(x) for x in glob.glob(os.path.join(FONTES, '*.ttf')))


def fonte(nome):
    p = glob.glob(os.path.join(FONTES, nome if nome.endswith('.ttf') else nome + '.ttf'))
    if not p:
        raise SystemExit(f'fonte {nome} ausente: rode baixar_fonte("<familia>") ou escolha outra em {FONTES}')
    return p[0]


def mascara(im, caixa, cond):
    x0, y0, x1, y1 = caixa
    a = np.array(im)[y0:y1, x0:x1].astype(int)
    return cond(a[..., 0], a[..., 1], a[..., 2])


def medir(im, caixa, cond, rotulo=''):
    """Imprime (y_topo, y_base, x0, x1) de cada linha de texto na caixa."""
    m = mascara(im, caixa, cond)
    linhas, ini = [], None
    tem = m.any(1)
    for i, v in enumerate(list(tem) + [False]):
        if v and ini is None:
            ini = i
        if not v and ini is not None:
            cols = np.where(m[ini:i].any(0))[0]
            linhas.append((ini + caixa[1], i - 1 + caixa[1], cols.min() + caixa[0], cols.max() + caixa[0]))
            ini = None
    for l in linhas:
        print(rotulo, 'y', l[0], l[1], 'x', l[2], l[3])
    return linhas


def caixas_cor(im, cond, area_min=3000):
    """Caixas sólidas (botões, faixas) de uma cor: [(x0, y0, x1, y1, cor_media)]."""
    a = np.array(im).astype(int)
    m = cond(a[..., 0], a[..., 1], a[..., 2]).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, ar = st[i]
        if ar >= area_min:
            out.append((int(x), int(y), int(x + w), int(y + h), tuple(int(v) for v in a[lab == i].mean(0))))
    return out


def calibrar(caminho, texto, largura):
    """Tamanho em que o texto original ocupa a largura medida na arte."""
    melhor = None
    for t in np.arange(8, 200, 0.25):
        f = ImageFont.truetype(caminho, float(t))
        l, _, r, _ = f.getbbox(texto)
        if melhor is None or abs((r - l) - largura) < abs(melhor[1] - largura):
            melhor = (float(t), r - l)
    return ImageFont.truetype(caminho, melhor[0])


def apagar(im, caixa, cond, dil=3, raio=6):
    """Inpainting só nos pixels de texto dentro da caixa (fundo foto ou degradê)."""
    a = np.array(im)
    x0, y0, x1, y1 = caixa
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = mascara(im, caixa, cond).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def preencher(im, caixa, cor):
    """Para fundo chapado (botão, faixa): repinta a caixa inteira com a cor."""
    ImageDraw.Draw(im).rectangle([caixa[0], caixa[1], caixa[2] - 1, caixa[3] - 1], fill=cor)
    return im


def cor_fundo(im, caixa):
    a = np.array(im)[caixa[1]:caixa[3], caixa[0]:caixa[2]].reshape(-1, 3)
    return tuple(int(v) for v in np.median(a, 0))


def cor_texto(im, caixa, cond):
    a = np.array(im)[caixa[1]:caixa[3], caixa[0]:caixa[2]].astype(int)
    px = a[cond(a[..., 0], a[..., 1], a[..., 2])]
    lum = px.sum(1)
    claro = np.median(lum) > 382
    sel = px[lum >= np.percentile(lum, 60)] if claro else px[lum <= np.percentile(lum, 40)]
    return tuple(int(v) for v in np.median(sel, 0))


def escrever(im, linhas_pt, linhas_es, medidas, caminho_fonte, cor, alinhamento='centro', f=None, largura_max=None):
    """medidas: [(y_topo, x0, x1)] de cada linha ORIGINAL. Mantém linha de base e alinhamento.
    Se o espanhol tiver outro número de linhas, passe medidas com o mesmo número de linhas ES
    (repita o passo de linha). largura_max: reduz a fonte se alguma linha ES passar disso."""
    d = ImageDraw.Draw(im)
    if f is None:
        i = max(range(len(linhas_pt)), key=lambda k: medidas[k][2] - medidas[k][1])
        f = calibrar(caminho_fonte, linhas_pt[i], medidas[i][2] - medidas[i][1])
    if largura_max:
        while max(f.getbbox(s)[2] - f.getbbox(s)[0] for s in linhas_es) > largura_max and f.size > 8:
            f = ImageFont.truetype(caminho_fonte, f.size - 0.5)
    ref = linhas_pt[0]
    _, t_ref, _, _ = f.getbbox(ref)
    for es, (ytop, x0, x1) in zip(linhas_es, medidas):
        y = ytop - t_ref
        l, _, r, _ = f.getbbox(es)
        if alinhamento == 'esquerda':
            x = x0 - l
        elif alinhamento == 'direita':
            x = x1 - r
        else:
            x = (x0 + x1) / 2 - (r - l) / 2 - l
        d.text((x, y), es, font=f, fill=cor)
    return f


def alargar_caixa(im, caixa, cor, largura_texto, folga):
    x0, y0, x1, y1 = caixa
    precisa = largura_texto + 2 * folga
    if precisa <= x1 - x0:
        return caixa
    cx = (x0 + x1) / 2
    nova = (int(cx - precisa / 2), y0, int(cx + precisa / 2), y1)
    ImageDraw.Draw(im).rectangle([nova[0], y0, nova[2], y1 - 1], fill=cor)
    return nova


def texto_rotacionado(im, texto, f, cor, ancora_xy, angulo_graus, riscar=None, cor_risco=None):
    """Escreve texto inclinado (caixa de preço torta). ancora = canto inferior esquerdo na linha de base.
    riscar=(inicio, fim) do trecho a riscar em caracteres."""
    camada = Image.new('RGBA', (2000, 500), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    ox, oy = 200, 300
    dc.text((ox, oy), texto, font=f, fill=tuple(cor) + (255,), anchor='ls')
    if riscar:
        xa = ox + f.getlength(texto[:riscar[0]])
        xb = ox + f.getlength(texto[:riscar[1]])
        t = f.getbbox(texto[riscar[0]:riscar[1]], anchor='ls')[1]
        ym = oy + t * 0.45
        dc.line([(xa, ym), (xb, ym)], fill=tuple(cor_risco or cor) + (255,), width=max(2, round(f.size / 13)))
    piv = (ox + f.getbbox(texto[0], anchor='ls')[0], oy)
    rot = camada.rotate(-angulo_graus, resample=Image.BICUBIC, center=piv)
    im.paste(rot, (int(round(ancora_xy[0] - piv[0])), int(round(ancora_xy[1] - piv[1]))), rot)
    return im


def previa(im, caminho, largura=540):
    """JPG reduzido para conferir visualmente com a ferramenta Read."""
    r = largura / im.width
    im.resize((largura, int(im.height * r))).save(caminho, quality=88)
    return caminho
