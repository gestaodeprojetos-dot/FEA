#!/usr/bin/env python3
"""FEA: edição de criativos de anúncio (Reels/Stories 9:16) com a identidade Elite Mentoring.

Diferente do fea_editar_video.py (Reels de procedimento): aqui não há título de 3 s, porque o
gancho é a própria fala do primeiro quadro (roteiro "Roteiros dos criativos", v4 05/11/2026).
A legenda entra desde o 0 s, e as cartelas de texto do roteiro ("Tela") entram por cima.

Uso:
    python3 fea_editar_criativo.py projeto.json [--so-legenda] [trecho_do_nome ...]

projeto.json:
{
  "ffmpeg": "...", "fontsdir": "fonts", "assets": "assets",   # assets: logo_elite_h.png
  "brutos": "brutos", "transcricoes": "tr",
  "videos": [
    {
      "saida": "out/01A- Quase 100% na cadeira.mp4",
      "trechos": [["IMG_9008", 0.4, 12.3], ["IMG_9009", 3.1, 40.0, "exato"]],  # s do bruto
      "remover_legenda": [["IMG_9008", 5.0, 6.0]],
      "correcoes": [["regex", "troca"]],
      "cartelas": [
        {"tipo": "gancho", "ini": 0, "fim": 3.2, "eyebrow": "Pela primeira vez",
         "texto": "Quase 100% na cadeira"},
        {"tipo": "card", "ancora": "roteiro", "dur": 4, "eyebrow": "...", "texto": "...",
         "chips": ["A", "B"]},                    # ancora = 1ª palavra (texto) a partir do início
        {"tipo": "cta", "ancora": "clica", "fim": "final"}
      ]
    }
  ]
}
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

import fea_editar_video as fe

W, H = 1080, 1920
fe.TITULO_DUR = 0.0           # sem título: a legenda começa no primeiro quadro (gancho legendado)
fe.formatar_titulo = lambda v: ""   # criativo não tem título de 3 s
fe.LEGENDA_Y = 1500

# identidade Elite Mentoring (mesma da página da oferta e do roteiro)
BG = (1, 26, 36)
LINHA = (22, 66, 79)
TEAL = (98, 185, 180)
AQUA = (134, 249, 248)
INK = (234, 246, 246)
MUTED = (147, 179, 184)


def fonte(cfg, nome, tam, peso=None):
    f = ImageFont.truetype(os.path.join(cfg["fontsdir"], nome), tam)
    if peso:
        try:
            f.set_variation_by_axes([peso])
        except Exception:
            pass
    return f


def quebrar(draw, texto, f, largura):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if draw.textlength(t.replace("*", ""), font=f) <= largura or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    # equilibra 2 linhas (evita viúva)
    if len(linhas) == 2:
        ps = texto.split()
        melhor = min(range(1, len(ps)), key=lambda i: max(
            draw.textlength(" ".join(ps[:i]).replace("*", ""), font=f),
            draw.textlength(" ".join(ps[i:]).replace("*", ""), font=f)))
        a, b = " ".join(ps[:melhor]), " ".join(ps[melhor:])
        if max(draw.textlength(a.replace("*", ""), font=f), draw.textlength(b.replace("*", ""), font=f)) <= largura:
            linhas = [a, b]
    return linhas


def desenhar_linha(draw, x, y, linha, f, cor, destaque):
    """Texto com trechos entre *asteriscos* na cor de destaque."""
    partes = re.split(r"(\*[^*]+\*)", linha)
    for p in partes:
        if not p:
            continue
        c = destaque if p.startswith("*") else cor
        p = p.strip("*")
        draw.text((x, y), p, font=f, fill=c)
        x += draw.textlength(p, font=f)


def espacado(draw, xy, texto, f, cor, esp=0.22, centro=False):
    tam = f.size
    larg = sum(draw.textlength(ch, font=f) + tam * esp for ch in texto) - tam * esp
    x, y = xy
    if centro:
        x -= larg / 2
    for ch in texto:
        draw.text((x, y), ch, font=f, fill=cor)
        x += draw.textlength(ch, font=f) + tam * esp
    return larg


def icone(d, x, y, ok, tam=30):
    """Check (aqua) ou X (cinza) desenhados à mão: as fontes não têm os glifos."""
    if ok:
        d.ellipse((x, y, x + tam, y + tam), fill=AQUA + (255,))
        d.line((x + tam * .25, y + tam * .52, x + tam * .43, y + tam * .70, x + tam * .76, y + tam * .32),
               fill=BG + (255,), width=4, joint="curve")
    else:
        d.ellipse((x, y, x + tam, y + tam), outline=MUTED + (255,), width=3)
        k = tam * .32
        d.line((x + k, y + k, x + tam - k, y + tam - k), fill=MUTED + (255,), width=3)
        d.line((x + tam - k, y + k, x + k, y + tam - k), fill=MUTED + (255,), width=3)


def dividida_png(cfg, c, caminho):
    """Tela dividida: o Dr. fica na metade de cima e a metade de baixo compara
    a venda de hoje com o método (roteiro: SUA AVALIAÇÃO × O MÉTODO)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y0 = 960
    d.rectangle((0, y0, W, H), fill=BG + (246,))
    d.rectangle((0, y0, W, y0 + 6), fill=AQUA + (255,))
    eyeb = fonte(cfg, "Urbanist.ttf", 25, 700)
    cab = fonte(cfg, "Gloock-Regular.ttf", 50)
    item = fonte(cfg, "Urbanist.ttf", 33, 600)
    espacado(d, (W / 2, y0 + 34), c.get("eyebrow", "Diagnóstico gratuito").upper(), eyeb, TEAL + (255,), 0.3, centro=True)
    col = [(60, c.get("esq_titulo", "Sua venda hoje"), c["esq"], False),
           (W // 2 + 30, c.get("dir_titulo", "O método"), c["dir"], True)]
    d.line((W // 2, y0 + 100, W // 2, y0 + 440), fill=LINHA + (255,), width=2)
    for x, tit, itens, ok in col:
        d.text((x, y0 + 86), tit, font=cab, fill=(AQUA if ok else MUTED) + (255,))
        y = y0 + 176
        for it in itens:
            icone(d, x, y + 4, ok, 32)
            linhas = quebrar(d, it, item, W // 2 - 140)
            for ln in linhas:
                d.text((x + 48, y), ln, font=item, fill=(INK if ok else MUTED) + (255,))
                y += 40
            y += 26
    img.save(caminho)


def whats_png(cfg, c, caminho):
    """Conversa de direct/WhatsApp desenhada (mensagens que a avatar recebe)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = fonte(cfg, "Urbanist.ttf", 34, 600)
    fh = fonte(cfg, "Urbanist.ttf", 27, 700)
    largura, x0, y0 = 760, (W - 760) // 2, c.get("y", 930)
    msgs = c["mensagens"]
    alt = 92 + 104 * len(msgs) + 30
    d.rounded_rectangle((x0, y0, x0 + largura, y0 + alt), radius=34, fill=(7, 43, 56, 240), outline=LINHA + (255,), width=2)
    d.rounded_rectangle((x0, y0, x0 + largura, y0 + 80), radius=34, fill=BG + (255,))
    d.rectangle((x0, y0 + 46, x0 + largura, y0 + 80), fill=BG + (255,))
    d.ellipse((x0 + 28, y0 + 18, x0 + 72, y0 + 62), fill=TEAL + (255,))
    espacado(d, (x0 + 92, y0 + 26), c.get("cabecalho", "Direct · novas mensagens").upper(), fh, INK + (255,), 0.14)
    y = y0 + 106
    for m in msgs:
        tw = d.textlength(m, font=f)
        d.rounded_rectangle((x0 + 30, y, x0 + 30 + tw + 56, y + 78), radius=26, fill=(234, 246, 246, 255))
        d.text((x0 + 58, y + 18), m, font=f, fill=BG + (255,))
        y += 104
    img.save(caminho)


def cartela_png(cfg, c, caminho):
    """Desenha a cartela em PNG transparente 1080x1920."""
    if c["tipo"] == "dividida":
        return dividida_png(cfg, c, caminho)
    if c["tipo"] == "whats":
        return whats_png(cfg, c, caminho)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    serif = fonte(cfg, "Gloock-Regular.ttf", c.get("tam", 66 if c["tipo"] != "gancho" else 72))
    eyeb = fonte(cfg, "Urbanist.ttf", 25, 700)
    chipf = fonte(cfg, "Urbanist.ttf", 31, 700)
    if c["tipo"] == "cta":
        # botão "Saiba mais" com seta para baixo, logo acima da legenda não: abaixo dela
        bw, bh, by = 420, 96, 1660
        bx = (W - bw) // 2
        d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=bh // 2, fill=AQUA + (255,))
        f = fonte(cfg, "Urbanist.ttf", 38, 800)
        espacado(d, (W / 2, by + 26), "SAIBA MAIS", f, BG + (255,), 0.12, centro=True)
        ax, ay = W // 2, by + bh + 22
        d.polygon([(ax - 18, ay), (ax + 18, ay), (ax, ay + 20)], fill=AQUA + (255,))
        if c.get("texto"):
            c = dict(c, tipo="card")
        else:
            img.save(caminho)
            return
    largura = c.get("largura", 900)
    pad = 46
    linhas = quebrar(d, c["texto"], serif, largura - 2 * pad)
    # destaque *...* que quebra de linha: fecha numa linha e reabre na seguinte
    aberto = False
    for i, ln in enumerate(linhas):
        if aberto:
            ln = "*" + ln
        aberto = ln.count("*") % 2 == 1
        linhas[i] = ln + "*" if aberto else ln
    lh = int(serif.size * 1.12)
    alt = pad + (44 if c.get("eyebrow") else 0) + lh * len(linhas) + pad
    linhas_chips = []
    if c.get("chips"):
        chipf0 = fonte(cfg, "Urbanist.ttf", 31, 700)
        lc, larg = [], 0
        for ch in c["chips"]:
            lw = d.textlength(ch.upper(), font=chipf0) + 3.5 * len(ch) + 52
            if lc and larg + 26 + lw > largura - 60:
                linhas_chips.append(lc)
                lc, larg = [], 0
            larg += (26 if lc else 0) + lw
            lc.append(ch)
        linhas_chips.append(lc)
        alt += 92 + 84 * (len(linhas_chips) - 1)
    x0 = (W - largura) // 2
    y0 = c.get("y", 1000)   # no peito: o rosto (y 330 a 900) fica livre
    # sombra suave
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 10, x0 + largura, y0 + alt + 10), radius=30, fill=(0, 0, 0, 90))
    from PIL import ImageFilter
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y0, x0 + largura, y0 + alt), radius=30, fill=BG + (232,), outline=LINHA + (255,), width=2)
    d.rounded_rectangle((x0, y0, x0 + largura, y0 + 7), radius=3, fill=AQUA + (255,))
    y = y0 + pad - 6
    if c.get("eyebrow"):
        espacado(d, (W / 2, y), c["eyebrow"].upper(), eyeb, TEAL + (255,), 0.3, centro=True)
        y += 44
    for ln in linhas:
        lw = d.textlength(ln.replace("*", ""), font=serif)
        desenhar_linha(d, (W - lw) / 2, y, ln, serif, INK + (255,), AQUA + (255,))
        y += lh
    if linhas_chips:
        y += 22
        for chips in linhas_chips:
            larguras = [d.textlength(ch.upper(), font=chipf) + 3.5 * len(ch) + 52 for ch in chips]
            sep = 26
            total = sum(larguras) + sep * (len(chips) - 1)
            x = (W - total) / 2
            for i, (ch, lw) in enumerate(zip(chips, larguras)):
                d.rounded_rectangle((x, y, x + lw, y + 66), radius=33, outline=TEAL + (255,), width=2,
                                    fill=(7, 43, 56, 255))
                espacado(d, (x + lw / 2, y + 16), ch.upper(), chipf, INK + (255,), 0.12, centro=True)
                if c.get("riscar"):
                    d.line((x + 16, y + 34, x + lw - 16, y + 34), fill=AQUA + (255,), width=4)
                x += lw + sep
                if i < len(chips) - 1 and c.get("seta"):
                    d.text((x - sep + 2, y + 12), "→", font=chipf, fill=AQUA + (255,))
            y += 84
    img.save(caminho)


def palavras_do_bruto(cfg, nome, extras_remover):
    trans = json.load(open(os.path.join(cfg["transcricoes"], nome + ".json"), encoding="utf-8"))
    palavras = []
    for seg in trans:
        ws = [dict(w) for w in seg["words"]]
        for i, w in enumerate(ws):
            if i and palavras and not w["w"].startswith(" "):
                palavras[-1]["w"] += w["w"]
                palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                continue
            palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), e0=w["e"], ini=(i == 0)))
    palavras.sort(key=lambda p: p["s"])
    palavras = fe.numerar_enumeracao(palavras)
    for a, b in extras_remover:
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    return palavras


def apertar_pausas(db, lim, passo, a, b, minimo=0.45, margem=0.12):
    """Silêncios de mais de `minimo` s dentro de [a, b] (bem abaixo do limiar de voz) ficam
    com `margem` s de cada lado. Devolve os cortes [(fim_fala, volta_fala), ...]."""
    cortes, ini = [], None
    i0, i1 = int(a / passo) + 4, int(b / passo) - 4
    for i in range(i0, i1):
        if db[i] < lim - 6:
            ini = i if ini is None else ini
        else:
            if ini is not None and (i - ini) * passo > minimo:
                cortes.append((round(ini * passo + margem, 3), round(i * passo - margem, 3)))
            ini = None
    return cortes


def montar(cfg, v):
    ff = cfg["ffmpeg"]
    entradas, cache_db = [], {}
    trechos = []
    for t in v["trechos"]:
        nome, a, b = t[0], t[1], t[2]
        arq = os.path.join(cfg["brutos"], nome + ".MOV")
        if nome not in cache_db:
            cache_db[nome] = fe.perfil_voz(ff, arq)
        db, lim, passo = cache_db[nome]
        if len(t) > 3 and t[3] == "exato":
            a2, b2 = a, b
        else:
            a2, b2 = fe.encaixar_cortes([[a, b]], db, passo)[0]
        if not trechos:
            # o vídeo abre com o Dr. já falando (Keila, 07/11: "o respiro no começo parece edição ruim")
            i0 = int(a2 / passo)
            for i in range(i0, min(len(db) - 6, i0 + int(3 / passo))):
                if all(db[j] >= lim for j in range(i, i + 6)):
                    # volta até a 1ª sílaba, que costuma ser mais baixa ("Quase" de "Quase todo
                    # paciente" saía comido, Keila 09/11)
                    while i > i0 and db[i - 1] >= lim - 10:
                        i -= 1
                    a2 = max(a2, i * passo - 0.12)
                    break
        # pausa longa no meio da fala vira respiro curto (ritmo de anúncio)
        for x, y in (apertar_pausas(db, lim, passo, a2, b2) if v.get("apertar", False) else []):
            trechos.append((nome, arq, a2, x))
            a2 = y
        trechos.append((nome, arq, a2, b2))
    # legenda
    todas, offset = [], 0.0
    por_bruto = {}
    for nome, arq, a, b in trechos:
        if nome not in por_bruto:
            rem = [(x[1], x[2]) for x in v.get("remover_legenda", []) if x[0] == nome]
            ps = palavras_do_bruto(cfg, nome, rem)
            # palavra que a transcrição juntou com um tropeço cortado ("para o seu... para a tua"):
            # entra à mão, com o tempo medido no áudio
            for x in v.get("inserir_legenda", []):
                if x[0] == nome:
                    ps.append({"s": x[1], "e": x[2], "e0": x[2], "w": " " + x[3], "ini": False,
                               "fixo": (x[1], x[2])})
            ps.sort(key=lambda p: p["s"])
            ps = [p for p in ps if re.sub(r"[^\w]", "", p["w"]).lower() != "ó"]
            ps = fe.ancorar_na_voz(ps, *cache_db[nome])
            # palavra inserida à mão fica no tempo medido (o ajuste puxava "método" para dentro
            # do tropeço cortado e ela sumia da legenda)
            por_bruto[nome] = [dict(p, s=p["fixo"][0], e=p["fixo"][1]) if p.get("fixo") else p for p in ps]
        ps, dur = fe.remapear_palavras(por_bruto[nome], [[a, b]])
        for p in ps:
            p["s"] += offset
            p["e"] += offset
        # o 1º bloco do trecho só começa frase nova se a fala recomeça mesmo (maiúscula na
        # transcrição ou ponto antes); corte curto dentro da frase não ganha vírgula ("meu, método")
        if ps:
            fim_ant = todas[-1]["w"].strip()[-1:] if todas else "."
            ps[0]["ini"] = ps[0]["w"].strip()[:1].isupper() or fim_ant in ".?!"
        todas += ps
        offset += dur
    duracao = offset
    base = v["saida"].rsplit(".", 1)[0]
    ass = base + ".ass"
    vv = dict(v, titulo="-")
    fe.gerar_ass(vv, todas, duracao, ass)
    # tempos das cartelas
    texto_tl = [(p["s"], re.sub(r"[^\w%]", "", p["w"]).lower()) for p in todas]

    def achar(ancora, depois=0.0):
        alvo = [re.sub(r"[^\w%]", "", x).lower() for x in ancora.split()]
        for i in range(len(texto_tl)):
            if texto_tl[i][0] < depois:
                continue
            if all(i + k < len(texto_tl) and texto_tl[i + k][1].startswith(alvo[k]) for k in range(len(alvo))):
                return texto_tl[i][0]
        raise SystemExit(f"{v['saida']}: âncora não encontrada: {ancora!r}")

    cartelas = []
    for k, c in enumerate(v.get("cartelas", [])):
        ini = c["ini"] if "ini" in c else achar(c["ancora"], c.get("depois", 0.0)) - 0.1
        ini = max(0.0, ini)
        fim = c.get("fim")
        if fim == "final" or fim is None and "dur" not in c:
            fim = duracao
        elif fim is None:
            fim = ini + c["dur"]
        fim = min(fim, duracao)
        png = f"{base}.cart{k}.png"
        # "cartelas_y": posição das cartelas no vídeo (com zoom o rosto desce no quadro e a cartela
        # no peito cobria o queixo e a boca; Keila 11/11: "coloca em cima do rosto dele")
        if v.get("cartelas_y") and c["tipo"] in ("card", "gancho", "cta") and "y" not in c:
            c = dict(c, y=v["cartelas_y"])
        cartela_png(cfg, c, png)
        cartelas.append((png, ini, fim))
    broll = []
    for b in v.get("broll", []):
        t0 = achar(b["ancora"], b.get("depois", 0.0)) - 0.05
        for arq, ss, dur in b["clipes"]:
            if t0 >= duracao - 0.5:
                break
            dur = min(dur, duracao - t0)
            broll.append((os.path.join(cfg["broll"], arq + ".MOV"), ss, t0, dur))
            t0 += dur
    return trechos, ass, duracao, cartelas, todas, broll


def renderizar(cfg, v, so_legenda=False):
    trechos, ass, duracao, cartelas, palavras, broll = montar(cfg, v)
    if so_legenda:
        return duracao
    ff = cfg["ffmpeg"]
    cmd = [ff, "-y", "-v", "error"]
    arquivos = []
    for nome, arq, a, b in trechos:
        if arq not in arquivos:
            arquivos.append(arq)
    for arq in arquivos:
        cmd += ["-i", arq]
    n = len(arquivos)
    logo = os.path.join(cfg["assets"], "logo_elite_h.png")
    cmd += ["-i", logo]
    for png, ini, fim in cartelas:
        cmd += ["-loop", "1", "-t", f"{fim - ini:.3f}", "-framerate", "30", "-i", png]
    nb = n + 1 + len(cartelas)
    for arq, ss, t0, dur in broll:
        cmd += ["-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", arq]
    # trilha de fundo (Keila 10/11: "uma musiquinha baixa"): original, composta por fea_trilha.py
    trilha = v.get("trilha", cfg.get("trilha"))
    if trilha:
        it = nb + len(broll)
        cmd += ["-stream_loop", "-1", "-i", trilha]
    partes, vr, ar = [], [], []
    zoom = v.get("zoom")   # [fator, cx, cy]: aproxima no Dr. (sem pernas no quadro)
    for i, (nome, arq, a, b) in enumerate(trechos):
        j = arquivos.index(arq)
        zf = ""
        if zoom:
            f = zoom[0] * (v.get("zoom_alterna", 1.0) if i % 2 else 1.0)   # troca de "câmera" a cada corte
            zw, zh = int(W / f) // 2 * 2, int(H / f) // 2 * 2
            zx = min(max(0, int(zoom[1] * W - zw / 2)), W - zw)
            zy = min(max(0, int(zoom[2] * H - zh / 2)), H - zh)
            zf = f",crop={zw}:{zh}:{zx}:{zy},scale={W}:{H}:flags=lanczos"
        partes.append(f"[{j}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H}{zf},setsar=1[v{i}]")
        # "limpar_audio" (Keila 10/11, vídeo 6: "silenciar o fundo e deixar somente a voz do Dr."):
        # faixa da voz, redução de ruído por FFT e portão que fecha o fundo entre as falas
        # (a 1ª versão cortava acima de 9 kHz e a voz ficou abafada, Keila 10/11: redução mais leve,
        # sem corte de agudos e com leve realce acima de 6 kHz; medido: agudos iguais ao bruto)
        limpa = ("highpass=f=70,afftdn=nr=12:nf=-45:tn=1,"
                 "agate=threshold=0.018:ratio=3:attack=10:release=280:range=0.12,treble=g=2:f=6000,"
                 if v.get("limpar_audio") else "")
        partes.append(f"[{j}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,{limpa}aresample=48000,"
                      f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03[a{i}]")
        vr.append(f"[v{i}]")
        ar.append(f"[a{i}]")
    partes.append("".join(vr) + f"concat=n={len(vr)}:v=1:a=0[vc]")
    partes.append("".join(ar) + f"concat=n={len(ar)}:v=0:a=1[ac0]")
    if trilha:
        tdb = v.get("trilha_db", cfg.get("trilha_db", -24))
        # a trilha abaixa sozinha quando o Dr. fala (sidechain) e some no fim
        partes.append(f"[{it}:a]aresample=48000,atrim=0:{duracao:.3f},asetpts=PTS-STARTPTS,volume={tdb}dB,"
                      f"afade=t=in:d=0.6,afade=t=out:st={max(0, duracao - 1.5):.3f}:d=1.5[tr]")
        partes.append("[ac0]asplit=2[voz][chave]")
        partes.append("[tr][chave]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=400[trd]")
        partes.append("[voz][trd]amix=inputs=2:duration=first:normalize=0[ac]")
    else:
        partes.append("[ac0]anull[ac]")
    base_v = "vc"
    for k, (arq, ss, t0, dur) in enumerate(broll):
        partes.append(f"[{nb + k}:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                      f"setpts=PTS-STARTPTS+{t0:.3f}/TB[b{k}]")
        partes.append(f"[{base_v}][b{k}]overlay=0:0:eof_action=pass[vb{k}]")
        base_v = f"vb{k}"
    # logo no topo e barra de progresso aqua
    partes.append(f"[{n}:v]scale=300:-1,format=rgba,colorchannelmixer=aa=0.95[lg]")
    partes.append(f"[{base_v}][lg]overlay=x=(W-w)/2:y=64[v0x]")
    partes.append(f"color=c=0x86F9F8:s={W}x8:r=30:d={duracao:.3f}[bar]")
    partes.append(f"[v0x][bar]overlay=x='-W+W*t/{duracao:.3f}':y=0:shortest=1[vb]")
    atual = "vb"
    for k, (png, ini, fim) in enumerate(cartelas):
        idx = n + 1 + k
        d = fim - ini
        fo = max(0.0, d - 0.25)
        partes.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1,"
                      f"fade=t=out:st={fo:.3f}:d=0.22:alpha=1,setpts=PTS+{ini:.3f}/TB[c{k}]")
        partes.append(f"[{atual}][c{k}]overlay=0:0:eof_action=pass[o{k}]")
        atual = f"o{k}"
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    partes.append(f"[{atual}]ass='{esc}':fontsdir='{cfg['fontsdir']}'[vo]")
    cmd += ["-filter_complex", ";".join(partes), "-map", "[vo]", "-map", "[ac]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", f"{duracao:.3f}", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return duracao


def main():
    args = sys.argv[1:]
    so_legenda = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:] or None
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = renderizar(cfg, v, so_legenda)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
