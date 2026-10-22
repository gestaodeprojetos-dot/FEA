#!/usr/bin/env python3
"""Troca a data escrita numa arte estática (PNG/JPG) mantendo foto, layout e tipografia.

Para cada linha de texto que o OCR acha com a data antiga: separa as palavras pela projeção de
colunas, apaga só as palavras que mudam (e as que precisam andar), recompõe o fundo (inpaint) e
escreve o texto novo na mesma família, peso, tamanho, cor e linha de base. Linha centralizada
continua centralizada. Não gera imagem: é edição tipográfica sobre a arte original.
"""
import re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FONTES = "/tmp/claude-0/-home-user-FEA/ce2ef478-67a4-5284-b1d6-9d4c8f98649b/scratchpad/fontes"
FAMILIAS = {"sora": f"{FONTES}/Sora.ttf", "serif": f"{FONTES}/EBGaramond.ttf"}

# palavra antiga (normalizada) -> palavra nova
TROCAS = {
    "terça-feira,": "segunda,", "terca-feira,": "segunda,", "terça-feira": "segunda", "terca-feira": "segunda",
    "11/08": "09/11", "11/08,": "09/11,", "agosto,": "novembro,", "agosto": "novembro",
}


def nova_palavra(p, anterior=None, seguinte=None):
    base = p.lower()
    if base in TROCAS:
        n = TROCAS[base]
        if p.isupper(): return n.upper()
        if p[:1].isupper(): return n[:1].upper() + n[1:]
        return n
    if p == "11" and seguinte and seguinte.lower() == "de": return "9"
    return None


def normalizar(t):
    """Desfaz junções e trocas típicas do OCR para contar as palavras certas."""
    t = t.replace("·", "•").replace("▪", "•")
    t = re.sub(r"\b(ll|1l|l1)\b", "11", t)
    t = re.sub(r"/[oO]8", "/08", t)
    t = re.sub(r"(\d)\s*DE\s*AGOSTO", r"\1 DE AGOSTO", t)
    t = re.sub(r"AGOSTO\s*[:\-•]\s*", "AGOSTO • ", t)
    t = re.sub(r"\b2OH\b", "20H", t)
    t = re.sub(r"A[O0]\s*VIV[O0]", "AO VIVO", t)
    t = re.sub(r",(?=\S)", ", ", t)
    if "AO VIVO NO ZOOM" in t.upper().replace("0", "O"):
        t = re.sub(r"\s-\s", " • ", t)
    return t


def fonte(familia, peso, tamanho):
    f = ImageFont.truetype(FAMILIAS[familia], tamanho)
    try: f.set_variation_by_axes([peso])
    except Exception: pass
    return f


def desenhar(texto, familia, peso, tamanho):
    """Texto renderizado em 4x e reduzido. Devolve alfa (float 0..1) e a altura da linha de base."""
    esc = 4
    f = fonte(familia, peso, tamanho * esc)
    asc, desc = f.getmetrics()
    largura = int(f.getlength(texto)) + 8 * esc
    im = Image.new("L", (largura, asc + desc + 4 * esc), 0)
    ImageDraw.Draw(im).text((4 * esc, 2 * esc), texto, font=f, fill=255)
    im = im.resize((max(1, largura // esc), max(1, im.height // esc)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    return a, (2 * esc + asc) / esc


def caixa_tinta(a, lim=0.35):
    ys, xs = np.where(a > lim)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else None


def espessura(binaria):
    """Espessura média do traço (área / meio perímetro), relativa à altura: separa regular de negrito."""
    b = binaria.astype(np.uint8)
    if b.sum() == 0: return 0
    per = cv2.findContours(b, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    p = sum(cv2.arcLength(c, True) for c in per)
    return 2 * b.sum() / max(1, p) / b.shape[0]


def da_linha(b, faixa):
    """Componentes da linha: cruzam a faixa da caixa do OCR ou ficam soltos dentro da margem
    (acento, cedilha). Pedaço que encosta na borda de cima/baixo é letra da linha vizinha."""
    n, rot, st, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), 8)
    h = b.shape[0]; a, z = faixa
    ok = np.zeros(n, bool)
    for i in range(1, n):
        y, hh = st[i, 1], st[i, 3]
        cruza = min(y + hh, z) - max(y, a) > (z - a) * 0.15   # encostar na faixa não basta (cedilha de cima)
        solto = y > 0 and y + hh < h
        # solto só conta se estiver colado na faixa: cedilha da linha de cima fica longe dela
        perto = (y + hh >= a - (z - a) * 0.15) if y + hh < a else (y <= z + (z - a) * 0.15)
        ok[i] = (cruza and (y >= a - (z - a) * 0.6 and y + hh <= z + (z - a) * 0.6)) or (solto and not cruza and perto and hh < (z - a) * 0.5)
        if cruza and not ok[i]: ok[i] = True
    return ok[rot]


def so_da_linha(b):
    """Mantém só as letras que cruzam a faixa central (descarta pontas das linhas vizinhas)."""
    n, rot, st, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), 8)
    h = b.shape[0]; a, z = int(h * 0.3), int(h * 0.75)
    ok = np.zeros(n, bool)
    for i in range(1, n):
        y, hh = st[i, 1], st[i, 3]
        ok[i] = y <= z and y + hh >= a
    # acento e cedilha da própria palavra: componente pequeno colado em letra mantida
    return ok[rot]


def mascara(rgb, fundo):
    d = np.sqrt(((rgb.astype(np.float32) - fundo) ** 2).sum(-1))
    return d


def palavras_da_linha(dist, n_esperado, altura):
    tinta = dist > 60
    # só a faixa central da linha: acento ou cedilha da linha vizinha não cria palavra falsa
    h = tinta.shape[0]
    col = tinta[int(h * 0.25):int(h * 0.8)].sum(0) > 0
    xs = np.where(col)[0]
    if not len(xs): return []
    for fator in (0.30, 0.24, 0.36, 0.20, 0.42, 0.16, 0.5):
        gap = max(2, int(altura * fator))
        segs, ini, ult = [], xs[0], xs[0]
        for x in xs[1:]:
            if x - ult > gap:
                segs.append((ini, ult + 1)); ini = x
            ult = x
        segs.append((ini, ult + 1))
        if len(segs) == n_esperado: return refinar(segs, tinta)
    return None


def refinar(segs, tinta):
    """A faixa central não vê a barra do T nem a vírgula: estende cada palavra pela altura
    toda, sem passar do meio do espaço até a vizinha."""
    col = np.where(tinta.any(0))[0]
    out = []
    for i, (a, b) in enumerate(segs):
        lim_e = (segs[i - 1][1] + a) // 2 if i else 0
        lim_d = (b + segs[i + 1][0]) // 2 if i + 1 < len(segs) else tinta.shape[1]
        c = col[(col >= lim_e) & (col < lim_d)]
        out.append((int(c.min()), int(c.max()) + 1) if len(c) else (a, b))
    return out


def editar(img, linhas, familia="sora", log=None, alinhar=None, linha_inteira=None, largura_max=None):
    """img: np.uint8 RGB. linhas: lista de (texto_ocr, quad). Retorna a imagem editada."""
    out = img.copy()
    H, W = out.shape[:2]
    for texto, quad in linhas:
        q = np.array(quad)
        hq = q[:, 1].max() - q[:, 1].min()
        mv = int(hq * 0.22)
        bx0, y0 = max(0, q[:, 0].min() - 4), max(0, q[:, 1].min() - mv)
        bx1, y1 = min(W, q[:, 0].max() + 4), min(H, q[:, 1].max() + mv)
        faixa = (q[:, 1].min() - y0, q[:, 1].max() - y0)
        # região ampliada nas laterais: o texto novo pode ficar mais largo que o antigo
        folga = int((bx1 - bx0) * 0.35)
        x0, x1 = max(0, bx0 - folga), min(W, bx1 + folga)
        reg = img[y0:y1, x0:x1]          # leitura sempre na arte original
        atual = out[y0:y1, x0:x1]        # composição sobre o que já foi editado
        caixa = reg[:, bx0 - x0:bx1 - x0]
        borda = np.concatenate([caixa[0], caixa[-1], caixa[:, 0], caixa[:, -1]])
        fundo = np.median(borda, 0)
        dist = mascara(reg, fundo)
        dist[:, :bx0 - x0] = 0; dist[:, bx1 - x0:] = 0  # fora da caixa do texto nada é apagado
        dist = dist * da_linha(dist > 35, faixa)          # nem letra de linha vizinha
        base = normalizar(texto)
        variantes = [base, re.sub(r"(\dh), ", r"\1,", base), base.replace(" • ", " "), re.sub(r"(\dh), ", r"\1,", base).replace(" • ", " ")]
        segs = None
        for v in variantes:
            palavras = v.split()
            # o OCR troca ç por c e 0 por O: só a quantidade de palavras importa aqui
            for recorte in (dist[faixa[0]:faixa[1]], dist):
                segs = palavras_da_linha(recorte, len(palavras), faixa[1] - faixa[0])
                if segs: break
            if segs: break
        if not segs:
            if log is not None: log.append(f"PULADO (palavras não batem): {texto!r}")
            continue
        novos = []
        for i, p in enumerate(palavras):
            pn = p.replace("Terca", "Terça").replace("terca", "terça")
            novos.append(nova_palavra(pn, palavras[i - 1] if i else None, palavras[i + 1] if i + 1 < len(palavras) else None))
        if not any(novos): continue
        # medidas da primeira palavra trocada para achar peso e corpo
        i0 = next(i for i, n in enumerate(novos) if n)
        sx0, sx1 = segs[i0]
        tinta = so_da_linha(dist[:, sx0:sx1] > 60)
        ys = np.where(tinta.any(1))[0]
        alt_tinta, larg_tinta = ys.max() - ys.min() + 1, sx1 - sx0
        velho = palavras[i0].replace("Terca", "Terça").replace("terca", "terça").replace("O", "0") if re.match(r"\d", palavras[i0]) else palavras[i0].replace("Terca", "Terça").replace("terca", "terça")
        alvo = so_da_linha(dist[:, sx0:sx1] > 90)[ys.min():ys.max() + 1]
        esp_alvo = espessura(alvo)
        melhor = None
        for peso in range(300, 801, 50):
            a, _ = desenhar(velho, familia, peso, 100)
            cx = caixa_tinta(a)
            if not cx: continue
            esc = alt_tinta / (cx[3] - cx[1])
            # renderiza no tamanho real para comparar a espessura do traço com a da arte
            a2, _ = desenhar(velho, familia, peso, 100 * esc)
            c2 = caixa_tinta(a2)
            r = a2[c2[1]:c2[3], c2[0]:c2[2]] > 0.5
            erro_esp = abs(espessura(r) - esp_alvo) / max(1e-6, esp_alvo)
            erro_larg = abs((cx[2] - cx[0]) * esc - larg_tinta) / larg_tinta
            nota = -(erro_esp + 0.7 * erro_larg)
            if melhor is None or nota > melhor[0]: melhor = (nota, peso, 100 * esc)
        _, peso, corpo = melhor
        if peso <= 600 and not re.search(r"\d", velho): peso = 400
        # cor do texto: pixels mais distantes do fundo na palavra trocada
        dseg = dist[:, sx0:sx1]
        pix = reg[:, sx0:sx1][dseg >= np.percentile(dseg[dseg > 60], 70)]
        cor = np.median(pix, 0).astype(np.float32)
        # linha de base: medida na palavra trocada, corrigida pelo que a fonte desce abaixo dela
        a_v, base_v = desenhar(velho, familia, peso, corpo)
        cxv = caixa_tinta(a_v)
        base_y = ys.max() - (cxv[3] - 1 - base_v)
        # monta a linha nova: palavras mantidas (pixels originais) + palavras novas (renderizadas)
        alfa_linha = np.clip((dist - 40) / 80, 0, 1)
        espaco = desenhar("a b", familia, peso, corpo)[0].shape[1] - desenhar("ab", familia, peso, corpo)[0].shape[1]
        pecas, x = [], segs[0][0]
        for i, (s, n) in enumerate(zip(segs, novos)):
            if i: x += segs[i][0] - segs[i - 1][1]
            if n:
                a, base_n = desenhar(n, familia, peso, corpo)
                cx = caixa_tinta(a, 0.05)
                a = a[:, cx[0]:cx[2]]
                # cada palavra trocada herda a cor dela na arte (ex.: "11" verde, "AGOSTO" branco)
                dp = dist[:, s[0]:s[1]]
                cor_p = np.median(reg[:, s[0]:s[1]][dp >= np.percentile(dp[dp > 60], 70)], 0).astype(np.float32) if (dp > 60).any() else cor
                pecas.append(("novo", x, a, base_n, cor_p)); x += a.shape[1]
            else:
                pecas.append(("velho", x, s)); x += s[1] - s[0]
        largura_nova, largura_velha = x - segs[0][0], segs[-1][1] - segs[0][0]
        if linha_inteira:
            texto_novo = " ".join(n or p for p, n in zip(palavras, novos)) if linha_inteira is True else linha_inteira
            limite = largura_max or largura_velha
            c_l = corpo
            while True:
                a, base_n = desenhar(texto_novo, familia, peso, c_l)
                cx = caixa_tinta(a, 0.05); a = a[:, cx[0]:cx[2]]
                if a.shape[1] <= limite or c_l < corpo * 0.7: break
                c_l *= 0.97
            pecas = [("novo", segs[0][0], a, base_n, cor)]
            largura_nova = a.shape[1]
        centro = (x0 + segs[0][0] + x0 + segs[-1][1]) / 2
        centralizada = (alinhar == "centro") if alinhar else abs(centro - W / 2) < 0.03 * W
        # "Dia 11/08" e "terça-feira," abrem bloco de texto alinhado à esquerda, mesmo quando caem no meio da arte
        if not alinhar and re.match(r"(?i)(dia\b|ter[cç]a)", base): centralizada = False
        desloc = -(largura_nova - largura_velha) / 2 if centralizada else 0
        # apaga a linha inteira e recompõe o fundo
        m = (dist > 35).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((5, 5), np.uint8))
        limpo = cv2.inpaint(np.ascontiguousarray(atual), m, 7, cv2.INPAINT_TELEA)
        canvas = limpo.astype(np.float32)
        Hr, Wr = canvas.shape[:2]
        for p in pecas:
            if p[0] == "velho":
                _, xp, (s0, s1) = p
                xd = int(round(xp + desloc))
                if xd < 0 or xd + (s1 - s0) > Wr:
                    # linha cresceu além da caixa do OCR: amplia a região para a direita/esquerda
                    pass
                al = alfa_linha[:, s0:s1, None]
                xa, xb = max(0, xd), min(Wr, xd + s1 - s0)
                if xb <= xa: continue
                canvas[:, xa:xb] = canvas[:, xa:xb] * (1 - al[:, xa - xd:xb - xd]) + reg[:, s0:s1][:, xa - xd:xb - xd] * al[:, xa - xd:xb - xd]
            else:
                _, xp, a, base_n, c = p
                xd = int(round(xp + desloc)); yd = int(round(base_y - base_n))
                ya, yb = max(0, yd), min(Hr, yd + a.shape[0])
                xa, xb = max(0, xd), min(Wr, xd + a.shape[1])
                if xb <= xa or yb <= ya: continue
                al = a[ya - yd:yb - yd, xa - xd:xb - xd, None]
                canvas[ya:yb, xa:xb] = canvas[ya:yb, xa:xb] * (1 - al) + c * al
        out[y0:y1, x0:x1] = np.clip(canvas, 0, 255).astype(np.uint8)
        if log is not None:
            log.append(f"{texto!r} -> {' '.join(n or p for p, n in zip(palavras, novos))!r} (peso {peso}, corpo {corpo:.0f}, {'centro' if centralizada else 'esquerda'}, largura {largura_velha}->{largura_nova})")
    return out


def cores_da_arte(reg, dist):
    """Verde e branco do texto, medidos nos próprios pixels da linha."""
    px = reg[dist > 90].astype(np.float32)
    verde = px[(px[:, 1] > px[:, 0] + 50) & (px[:, 1] > px[:, 2] + 30)]
    claro = px[px.min(1) > 170]
    return {"verde": np.median(verde, 0) if len(verde) else np.array([0, 210, 110], np.float32),
            "branco": np.median(claro, 0) if len(claro) else np.array([240, 240, 240], np.float32)}


def reescrever_linha(img, quad, velho, trechos, familia="sora", alinhar="centro", largura_max=None, log=None, inicio_x=None):
    """Reescreve uma linha inteira: trechos = [(texto, "verde"|"branco"), ...]. Mede corpo, peso e
    linha de base pelo texto antigo; apaga a linha e escreve a nova no mesmo lugar."""
    out = img.copy(); H, W = out.shape[:2]
    q = np.array(quad)
    hq = q[:, 1].max() - q[:, 1].min(); mv = int(hq * 0.22)
    bx0, y0 = max(0, q[:, 0].min() - 6), max(0, q[:, 1].min() - mv)
    bx1, y1 = min(W, q[:, 0].max() + 6), min(H, q[:, 1].max() + mv)
    faixa = (q[:, 1].min() - y0, q[:, 1].max() - y0)
    folga = int((bx1 - bx0) * 0.25)
    x0, x1 = max(0, bx0 - folga), min(W, bx1 + folga)
    reg = img[y0:y1, x0:x1]
    caixa = reg[:, bx0 - x0:bx1 - x0]
    fundo = np.median(np.concatenate([caixa[0], caixa[-1], caixa[:, 0], caixa[:, -1]]), 0)
    dist = mascara(reg, fundo); dist[:, :bx0 - x0] = 0; dist[:, bx1 - x0:] = 0
    dist = dist * da_linha(dist > 35, faixa)
    if inicio_x is not None:
        corte = max(0, int(inicio_x) - x0 - 2)
        # ícone à esquerda fica intacto, inclusive o pedaço dele que atravessa o corte
        n, rot, st, _ = cv2.connectedComponentsWithStats((dist > 35).astype(np.uint8), 8)
        for i in range(1, n):
            if st[i, 0] < corte - 3 and st[i, 0] + st[i, 2] > corte: dist[rot == i] = 0
        dist[:, :corte] = 0
    tinta = so_da_linha(dist > 60)
    ys, xs = np.where(tinta)
    lx0, lx1, ly0, ly1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    alvo = so_da_linha(dist > 90)[ly0:ly1, lx0:lx1]
    esp_alvo = espessura(alvo)
    melhor = None
    for peso in range(300, 801, 50):
        a, base = desenhar(velho, familia, peso, 100)
        cx = caixa_tinta(a)
        esc = (ly1 - ly0) / (cx[3] - cx[1])
        a2, _ = desenhar(velho, familia, peso, 100 * esc); c2 = caixa_tinta(a2)
        erro = abs(espessura(a2[c2[1]:c2[3], c2[0]:c2[2]] > 0.5) - esp_alvo) / esp_alvo + \
            0.7 * abs((cx[2] - cx[0]) * esc - (lx1 - lx0)) / (lx1 - lx0)
        if melhor is None or erro < melhor[0]: melhor = (erro, peso, 100 * esc, base, cx)
    _, peso, corpo, base, cx = melhor
    base_y = ly1 - (cx[3] - 1 - base) * corpo / 100
    cores = cores_da_arte(reg, dist)
    trechos = [(t[0], t[1], t[2] if len(t) > 2 else peso) for t in trechos]
    texto_todo = "".join(t for t, _, _ in trechos)
    limite = largura_max or (lx1 - lx0) * 1.15
    while True:
        a_todo, base_n = desenhar(texto_todo, familia, peso, corpo)
        ct = caixa_tinta(a_todo, 0.05)
        if ct[2] - ct[0] <= limite or corpo < 10: break
        corpo *= 0.97
    largura = ct[2] - ct[0]
    if alinhar == "centro": inicio = (lx0 + lx1) / 2 - largura / 2
    else: inicio = lx0
    # máscara mais larga que a da troca por palavra: borda suavizada do texto antigo não pode sobrar
    m = cv2.dilate((dist > 25).astype(np.uint8) * 255, np.ones((9, 9), np.uint8))
    canvas = cv2.inpaint(np.ascontiguousarray(out[y0:y1, x0:x1]), m, 7, cv2.INPAINT_TELEA).astype(np.float32)
    x_cursor = inicio - ct[0]  # posição da origem do texto para a tinta começar em "inicio"
    for texto, cor, peso_t in trechos:
        f = fonte(familia, peso_t, corpo)
        a, b_n = desenhar(texto, familia, peso_t, corpo)
        xd = int(round(x_cursor)); yd = int(round(base_y - b_n))
        ya, yb = max(0, yd), min(canvas.shape[0], yd + a.shape[0])
        xa, xb = max(0, xd), min(canvas.shape[1], xd + a.shape[1])
        if xb > xa and yb > ya:
            al = a[ya - yd:yb - yd, xa - xd:xb - xd, None]
            canvas[ya:yb, xa:xb] = canvas[ya:yb, xa:xb] * (1 - al) + cores[cor] * al
        x_cursor += f.getlength(texto)
    out[y0:y1, x0:x1] = np.clip(canvas, 0, 255).astype(np.uint8)
    if log is not None: log.append(f"linha reescrita {velho!r} -> {texto_todo!r} (peso {peso}, corpo {corpo:.0f})")
    return out
