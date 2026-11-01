#!/usr/bin/env python3
"""FEA: arte do elevador Elite (Modelo 2, 1024x1024) adaptada ao totem LED 344x1032.

Mantém o fundo da arte do elevador (arena azul + brilho e estrelas no alto, sem a porta),
os mesmos elementos (Bem-vindos, logo Elite, FEA, Elite Mentoring horizontal) e o mesmo
movimento de fundo do vídeo do elevador (diferença quadro a quadro do 2B aplicada ao fundo limpo).

Uso: python3 fea_totem_led_elite.py PASTA_ELEVADOR PASTA_ELEMENTOS SAIDA_PREFIXO [--efeito]
  PASTA_ELEVADOR: com '2A ...mp4' e '2B ...mp4' do elevador
  PASTA_ELEMENTOS: bemvindos.png, elite_logo.png, fea.png, ment_h.png (RGBA)
Gera SAIDA_PREFIXO.png (quadro estático) e SAIDA_PREFIXO.mp4 (12 s, 30 fps, sem áudio).
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H = 344, 1024           # monta em 1024 de altura (escala do elevador) e estica para 1032 no fim
HF = 1032
TOPO_FIM, EMENDA = 250, 330  # topo vem do centro da arte; abaixo disso, das laterais da arena
COL_E, COL_D = (36, 208), (816, 988)


def quadros(video):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(1024 * 1024 * 3)
        if len(b) < 1024 * 1024 * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(1024, 1024, 3).astype(np.float32)


def remontar(f):
    """1024x1024 do elevador -> 344x1024 sem porta."""
    topo = f[:, 340:684]
    lat = np.concatenate([f[:, COL_E[0]:COL_E[1]], f[:, COL_D[0]:COL_D[1]]], 1)
    a = np.clip((np.arange(1024) - TOPO_FIM) / (EMENDA - TOPO_FIM), 0, 1)[:, None, None]
    return topo * (1 - a) + lat * a


class Moldura:
    """Linha de luz em volta do totem, com o mesmo jogo da moldura da porta do elevador (medido no 2B):
    dois pontos de luz saem do centro do topo, um para cada lado, e descem até o centro de baixo
    (quadros 14-90 e 194-270), ficando mais fortes no caminho; entre 288 e 344 a moldura toda acende e apaga."""
    INSET, RAIO = 6, 12
    NUCLEO = np.array([150, 196, 214], np.float32)   # cor da linha (porta do elevador)
    BRILHO = np.array([40, 110, 140], np.float32)    # halo azul em volta
    LUZ = np.array([205, 240, 255], np.float32)      # cor do ponto de luz

    def __init__(self):
        from scipy.spatial import cKDTree
        i, r = self.INSET, self.RAIO
        x0, y0, x1, y1 = i, i, W - 1 - i, HF - 1 - i
        pts = []
        def reta(a, b, n):
            for t in np.linspace(0, 1, n, endpoint=False):
                pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        def arco(cx, cy, a0, a1):
            for t in np.linspace(a0, a1, 24, endpoint=False):
                pts.append((cx + r * np.cos(t), cy + r * np.sin(t)))
        cxm = W / 2
        reta((cxm, y0), (x1 - r, y0), 200); arco(x1 - r, y0 + r, -np.pi / 2, 0)
        reta((x1, y0 + r), (x1, y1 - r), 1000); arco(x1 - r, y1 - r, 0, np.pi / 2)
        reta((x1 - r, y1), (x0 + r, y1), 400); arco(x0 + r, y1 - r, np.pi / 2, np.pi)
        reta((x0, y1 - r), (x0, y0 + r), 1000); arco(x0 + r, y0 + r, np.pi, 1.5 * np.pi)
        reta((x0 + r, y0), (cxm, y0), 200)
        P = np.array(pts)
        seg = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
        self.per = seg[-1]
        yy, xx = np.mgrid[0:HF, 0:W]
        d, k = cKDTree(P).query(np.c_[xx.ravel(), yy.ravel()])
        self.d = d.reshape(HF, W).astype(np.float32)
        self.s = seg[k].reshape(HF, W).astype(np.float32)   # posição ao longo da moldura, 0 = centro do topo
        self.nucleo = np.exp(-(self.d / 1.1) ** 2)[..., None]
        self.halo = np.exp(-(self.d / 6.0) ** 2)[..., None]
        self.halo_luz = np.exp(-(self.d / 11.0) ** 2)[..., None]

    def intensidade(self, n):
        meio = self.per / 2
        dist = np.minimum(self.s, self.per - self.s)      # distância ao centro do topo pelos dois lados
        luz = np.zeros_like(self.s)
        for n0, n1 in ((14, 90), (194, 270)):
            if n0 <= n <= n1 + 6:
                prog = min((n - n0) / (n1 - n0), 1.0)
                cab = prog * meio
                forca = (0.3 + 0.7 * prog) * (1 if n <= n1 else (n1 + 6 - n) / 6)
                luz += forca * (np.exp(-((dist - cab) / 30) ** 2) + 0.45 * np.exp(-((dist - cab + 70) / 90) ** 2) * (dist < cab))
        if 288 <= n <= 344:
            g = (n - 288) / 28 if n <= 316 else (344 - n) / 28
            luz += 0.45 * g
        return luz[..., None]

    def aplicar(self, img, n):
        a = np.array(img).astype(np.float32)
        luz = self.intensidade(n)
        a = a * (1 - 0.85 * self.nucleo) + self.NUCLEO * 0.85 * self.nucleo     # linha fixa
        a += self.BRILHO * 0.55 * self.halo                                     # halo fixo
        a += self.LUZ * luz * (1.6 * self.nucleo + 0.9 * self.halo_luz)        # ponto de luz (com rastro) e acendimento
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def camada(pasta, nome, largura):
    im = Image.open(os.path.join(pasta, nome)).convert("RGBA")
    h = round(im.height * largura / im.width)
    return im.resize((largura, h), Image.LANCZOS)


def main():
    elev, elem, saida = sys.argv[1:4]
    efeito = "--efeito" in sys.argv
    a2 = glob.glob(os.path.join(elev, "2A*.mp4"))[0]
    b2 = glob.glob(os.path.join(elev, "2B*.mp4"))[0]
    limpo = next(quadros(a2))  # quadro 0 do 2A: fundo sem nenhum texto
    b_ini = next(quadros(b2))
    # onde o 2B tem texto (ou a porta), o movimento não é do fundo: brilho que passa no logo virava
    # um "ELITE" fantasma atrás do logo do totem. Nessas áreas o movimento é zerado.
    txt = (np.abs(b_ini - limpo).sum(2) > 12).astype(np.uint8) * 255
    txt[350:, 222:802] = 255
    txt = np.array(Image.fromarray(txt).filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(6)))
    livre = (1 - txt.astype(np.float32) / 255)[..., None]
    moldura = Moldura()

    # posições no padrão do elevador (Bem-vindos y=67, logo logo abaixo; FEA e mentoria sobre a arena)
    # tempos medidos quadro a quadro no 2A do elevador: (entra_ini, entra_fim, sai_ini, sai_fim) em quadros
    itens = [
        (camada(elem, "bemvindos.png", 230), 67, (9, 22, 337, 345)),
        (Image.new("RGBA", (48, 2), (190, 205, 212, 140)), 117, (15, 24, 332, 341)),
        (camada(elem, "elite_logo.png", 300), 136, (14, 28, 340, 350)),
        (camada(elem, "fea.png", 172), 548, (19, 30, 333, 343)),
        (camada(elem, "ment_h.png", 196), 672, (22, 30, 331, 340)),
    ]

    def compor(fundo, n):
        img = Image.fromarray(np.clip(fundo, 0, 255).astype(np.uint8)).convert("RGBA")
        for im, y, (e0, e1, s0, s1) in itens:
            dy = 0
            if efeito:
                if n < s0:
                    u = float(np.clip((n - e0) / (e1 - e0), 0, 1))
                    k = 1 - (1 - u) ** 3            # entra desacelerando (curva medida)
                    dy = round(8 * (1 - k))          # sobe ~8 px enquanto entra
                else:
                    u = float(np.clip((n - s0) / (s1 - s0), 0, 1))
                    k = 1 - u ** 2                   # sai acelerando
                if k <= 0.002:
                    continue
                c = im.filter(ImageFilter.GaussianBlur(5 * (1 - k))) if k < 1 else im.copy()
                al = np.array(c)[..., 3].astype(np.float32) * k
                c.putalpha(Image.fromarray(al.astype(np.uint8)))
            else:
                c = im
            img.alpha_composite(c, ((W - im.width) // 2, y + dy))
        return img.convert("RGB").resize((W, HF), Image.LANCZOS)

    b0 = None
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HF}",
                            "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", saida + ".mp4"], stdin=subprocess.PIPE)
    for n, fb in enumerate(quadros(b2)):
        if b0 is None:
            b0 = fb
        fundo = remontar(limpo + (fb - b0) * livre)
        q = moldura.aplicar(compor(fundo, n), n)
        if n == 60:
            q.save(saida + ".png")
        enc.stdin.write(q.tobytes())
    enc.stdin.close()
    enc.wait()
    print("OK", saida, n + 1, "quadros")


if __name__ == "__main__":
    main()
