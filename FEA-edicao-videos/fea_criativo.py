#!/usr/bin/env python3
"""FEA: edição de CRIATIVO (anúncio) vertical do Dr. João falando para a câmera.
Identidade do ELITE MENTORING (pasta "ELITE MENTORING" do Drive + página do diagnóstico).

v2 (06/11/2026, revisão da Keila: "legenda feia, cortes estranhos, Dr. comendo palavra"):
  - legenda no padrão dos conteúdos FEA: Montserrat Bold 56, branca, contorno preto,
    a ~80% da altura, 1 a 2 linhas de até 22 caracteres (a de blocos curtos foi reprovada)
  - cortes: só sai SILÊNCIO DE VERDADE (abaixo do ruído de fundo + 6 dB, por 0,55 s ou mais),
    com 0,2 s de respiro dos dois lados. A v1 usava o limiar de voz do Reels (ruído + 12 dB),
    que tratava sílaba fraca como silêncio e cortava pedaço de palavra
  - erros de fala (frase abandonada, gaguejada) saem pelo "manter" do projeto, com os pontos
    levados para o silêncio mais próximo (encaixar)
  - zoom alternado só em corte com trecho longo (sem pulo de enquadramento a cada segundo)
  - visual Elite: fundo #011A24, superfície #072B38, turquesa #62B9B4, água #86F9F8;
    títulos em Gloock (a Canela Deck do Drive é versão trial, sem acentos; a página do
    diagnóstico usa a Gloock como substituta) e textos em Galano Grotesque (Drive);
    logo oficial do Drive (EM_Asset 15) no topo; botão "SAIBA MAIS" em pílula água com texto
    escuro, igual ao botão da página
  - trilha diferente por vídeo, abaixando sozinha quando o Dr. fala

Uso:
    python3 fea_criativo.py projeto.json [--so-legenda] [trecho_do_nome ...]

projeto.json: {"ffmpeg", "fontsdir", "logo", "sfx": {"whoosh", "pop"}, "videos": [{
    "entrada", "transcricao", "saida", "gancho", "selo",
    "manter": [[a, b], ...],            # trechos do bruto; erros de fala ficam fora
    "remover_legenda", "correcoes", "inserts": [[gatilho, texto], ...],
    "saiba_mais": "saiba mais", "trilha", "trilha_db"}]}
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402

W, H = 1080, 1920
# cores ASS (&HAABBGGRR)
BG, SURF, TEAL, AQUA, LINE, BRANCO, PRETO = ("&H00241A01", "&H00382B07", "&H00B4B962", "&H00F8F986",
                                             "&H004F4216", "&H00FFFFFF", "&H00000000")
TITULO_FONTE, TEXTO_FONTE = "Gloock", "Galano Grotesque"
LOGO_W, LOGO_Y = 330, 92
GANCHO_DUR = 4.2
INSERT_Y, INSERT_DUR = 1215, 2.4
BOTAO_Y = 1735
ZOOM_B, ZOOM_CY = 1.10, 0.40
SIL_DB, SIL_MIN, RESPIRO = 6.0, 0.55, 0.20


def ts(t):
    return fe.ts(t)


def cabecalho():
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,Montserrat Bold,{fe.LEGENDA_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H80000000,0,0,0,0,100,100,0,0,1,3.5,2,2,90,90,{H - fe.LEGENDA_Y - 20},1
Style: Titulo,{TITULO_FONTE},66,{BRANCO},{BRANCO},{PRETO},&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Texto,{TEXTO_FONTE},40,{BRANCO},{BRANCO},{PRETO},&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Forma,{TEXTO_FONTE},20,{SURF},{SURF},{AQUA},&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def retangulo(w, h, r):
    k = r * 0.45
    return (f"m {r} 0 l {w - r} 0 b {w - k} 0 {w} {k} {w} {r} l {w} {h - r} "
            f"b {w} {h - k} {w - k} {h} {w - r} {h} l {r} {h} b {k} {h} 0 {h - k} 0 {h - r} "
            f"l 0 {r} b 0 {k} {k} 0 {r} 0")


def largura(txt, tam, esp=0.0, serif=False):
    f_up, f_lo = (0.66, 0.50) if serif else (0.66, 0.54)
    return sum(tam * (f_up if c.isupper() or c.isdigit() else 0.28 if c == " " else f_lo) + esp for c in txt)


def quebrar(txt, maxc):
    if len(txt) <= maxc:
        return [txt]
    ps = txt.split()
    return list(min(((" ".join(ps[:i]), " ".join(ps[i:])) for i in range(1, len(ps))),
                    key=lambda p: max(len(p[0]), len(p[1]))))


ENTRA = r"\fscx92\fscy92\t(0,220,\fscx100\fscy100)"


def caixa(s, e, x, y, w, h, cor, borda=None, r=24, alfa="&H18&", camada=2, anim=ENTRA):
    b = f"\\bord3\\3c{borda}" if borda else "\\bord0"
    return (f"Dialogue: {camada},{ts(s)},{ts(e)},Forma,,0,0,0,,{{\\an7\\pos({int(x)},{int(y)})"
            f"\\org({W // 2},{int(y + h / 2)})\\1c{cor}\\1a{alfa}{b}\\shad0\\fad(160,200){anim}\\p1}}"
            f"{retangulo(int(w), int(h), r)}{{\\p0}}\n")


def texto(s, e, x, y, txt, estilo, tam, cor, esp=0, camada=3, org_y=None, anim=ENTRA):
    org = f"\\org({W // 2},{int(org_y if org_y is not None else y)})"
    return (f"Dialogue: {camada},{ts(s)},{ts(e)},{estilo},,0,0,0,,{{\\an5\\pos({int(x)},{int(y)}){org}"
            f"\\fs{tam}\\fsp{esp}\\1c{cor}\\fad(160,200){anim}}}{txt}\n")


def gancho(txt, selo):
    """Cartão do topo nos primeiros segundos: selo em Galano espaçado (turquesa) + headline em
    Gloock branca, sobre a superfície escura da página, com fio água à esquerda."""
    linhas = quebrar(txt, 22)
    tam, lh = 66, 74
    w = max(max(largura(l, tam, serif=True) for l in linhas) + 120, largura(selo, 26, 6) + 120)
    w = min(w, W - 90)
    h = 70 + lh * len(linhas) + 40
    x, y = (W - w) / 2, LOGO_Y + 150
    ev = [caixa(0, GANCHO_DUR, x, y, w, h, SURF, LINE, r=26, alfa="&H10&")]
    ev.append(texto(0, GANCHO_DUR, W / 2, y + 48, selo, "Texto", 26, TEAL, esp=6, org_y=y + h / 2))
    for i, l in enumerate(linhas):
        ev.append(texto(0, GANCHO_DUR, W / 2, y + 70 + lh * i + lh / 2 + 6, l, "Titulo", tam, BRANCO,
                        org_y=y + h / 2))
    return ev


def insert(s, e, txt):
    """Cartão de destaque: superfície escura com borda água (o card de destaque da página) e
    texto em Galano caixa alta; antes do texto, um fio água curto."""
    linhas = quebrar(txt, 20)
    tam, lh, esp = 52, 62, 2
    w = min(max(largura(l, tam, esp) for l in linhas) + 110, W - 100)
    h = lh * len(linhas) + 70
    x, y = (W - w) / 2, INSERT_Y - h / 2
    ev = [caixa(s, e, x, y, w, h, SURF, AQUA, r=22, alfa="&H08&")]
    ev.append(f"Dialogue: 3,{ts(s)},{ts(e)},Forma,,0,0,0,,{{\\an7\\pos({int(W / 2 - 30)},{int(y + 18)})"
              f"\\org({W // 2},{INSERT_Y})\\1c{AQUA}\\bord0\\fad(160,200){ENTRA}\\p1}}m 0 0 l 60 0 l 60 5 l 0 5{{\\p0}}\n")
    y0 = INSERT_Y - lh * (len(linhas) - 1) / 2 + 8
    for i, l in enumerate(linhas):
        ev.append(texto(s, e, W / 2, y0 + i * lh, l, "Texto", tam, BRANCO, esp, org_y=INSERT_Y))
    return ev


def botao_saiba_mais(s, e):
    """Pílula água com texto escuro (o .btn da página) e seta água quicando abaixo."""
    w, h = 470, 104
    x, y = (W - w) / 2, BOTAO_Y - h / 2
    ev = [caixa(s, e, x, y, w, h, AQUA, None, r=52, alfa="&H00&", camada=4)]
    ev.append(texto(s, e, W / 2, BOTAO_Y + 3, "SAIBA MAIS", "Texto", 46, BG, esp=4, camada=5, org_y=BOTAO_Y))
    seta = "m 0 0 l 22 0 l 22 26 l 42 26 l 11 58 l -20 26 l 0 26 l 0 0"
    t, k = s + 0.2, 0
    while t < e:
        dy = 0 if k % 2 == 0 else 16
        ev.append(f"Dialogue: 4,{ts(t)},{ts(min(e, t + 0.45))},Forma,,0,0,0,,"
                  f"{{\\an7\\move({W // 2 - 11},{BOTAO_Y + 64 + dy},{W // 2 - 11},{BOTAO_Y + 80 - dy})"
                  f"\\1c{AQUA}\\bord0\\p1}}{seta}{{\\p0}}\n")
        t += 0.45
        k += 1
    return ev


def barra_progresso(d):
    return [f"Dialogue: 6,{ts(0)},{ts(d)},Forma,,0,0,0,,"
            f"{{\\an7\\pos(0,0)\\1c{AQUA}\\bord0\\clip(0,0,0,10)\\t(0,{int(d * 1000)},\\clip(0,0,{W},10))\\p1}}"
            f"m 0 0 l {W} 0 l {W} 10 l 0 10{{\\p0}}\n"]


def legendas(pal, correcoes):
    """Legenda no padrão dos conteúdos (fea_editar_video): mesmos blocos, quebra e estilo."""
    fe.NOMES_PROPRIOS.update({"Saiba", "Instagram"})
    ev = []
    blocos = fe.blocos_legenda(pal)
    livre = 0.0
    for i, b in enumerate(blocos):
        s, e = max(b[0]["s"], livre), b[-1]["e"] + 0.15
        if i + 1 < len(blocos):
            e = min(e, blocos[i + 1][0]["s"])
        if len(b) == 1 and re.sub(r"[^\w]", "", b[0]["w"]).lower() in fe.LIGACAO | {"é", "eu"}:
            continue
        txt = fe.limpar(fe.pontuar(fe.corrigir(fe.juntar_texto(b), correcoes)))
        if not txt.strip():
            continue
        minimo = max(0.35, 0.02 * len(txt))
        if e - s < minimo:
            e = s + minimo
            livre = e
        txt = fe.quebrar_linhas(txt.replace("Saiba Mais", "Saiba\x00Mais")).replace("\x00", " ")
        ev += fe.dialogos_linhas(1, s, e, "Legenda", txt)
    return ev


# ---------------------------------------------------------------- cortes

def silencio(db):
    return float(np.percentile(db, 5)) + SIL_DB


def encaixar(manter, db, passo, sil):
    """Leva cada ponto do "manter" para o meio do silêncio mais próximo (até 0,4 s)."""
    def ponto(t, inicio):
        i0, i1 = max(0, int((t - 0.4) / passo)), min(len(db) - 1, int((t + 0.4) / passo))
        quietos = [i for i in range(i0, i1 + 1) if db[i] < sil]
        if not quietos:
            return t
        # agrupa em trechos e escolhe o mais perto de t
        grupos, g = [], [quietos[0]]
        for i in quietos[1:]:
            if i == g[-1] + 1:
                g.append(i)
            else:
                grupos.append(g)
                g = [i]
        grupos.append(g)
        melhor = min(grupos, key=lambda g: abs((g[0] + g[-1]) / 2 * passo - t))
        # no começo do trecho fica perto do fim do silêncio (antes da voz); no fim, perto do início
        if inicio:
            return max(melhor[0] * passo, melhor[-1] * passo - RESPIRO)
        return min(melhor[-1] * passo, melhor[0] * passo + RESPIRO)
    return [[round(ponto(a, True), 3), round(ponto(b, False), 3)] for a, b in manter]


def jump_cuts(manter, db, passo, sil):
    """Tira só os silêncios reais (>= SIL_MIN) de dentro de cada trecho, com RESPIRO dos dois lados."""
    novo = []
    for a, b in manter:
        i0, i1 = int(a / passo), min(len(db), int(b / passo))
        q = db[i0:i1] < sil
        ini, k = a, 0
        while k < len(q):
            if q[k]:
                j = k
                while j < len(q) and q[j]:
                    j += 1
                t0, t1 = a + k * passo, a + j * passo
                if t1 - t0 >= SIL_MIN and k > 0 and j < len(q):
                    if t0 + RESPIRO - ini > 0.4:
                        novo.append([round(ini, 3), round(t0 + RESPIRO, 3)])
                        ini = t1 - RESPIRO
                k = j
            else:
                k += 1
        if b - ini > 0.3:
            novo.append([round(ini, 3), round(b, 3)])
    return novo


# ---------------------------------------------------------------- palavras

def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


def palavras_do_video(v, db_voz):
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    palavras = []
    for seg in trans:
        for i, w in enumerate(seg["words"]):
            if i and palavras and not w["w"].startswith(" "):
                palavras[-1]["w"] += w["w"]
                palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                continue
            palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), e0=w["e"], ini=(i == 0)))
    palavras.sort(key=lambda p: p["s"])
    palavras = fe.numerar_enumeracao(palavras)
    for a, b in v.get("remover_legenda", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    palavras = fe.ancorar_na_voz(palavras, *db_voz)
    # "Saiba Mais" numa palavra só ("Sabamais", "Seba Mais", "sabe a mais", "Saiba / mais")
    saida, i = [], 0
    while i < len(palavras):
        p = palavras[i]
        for n in (3, 2):
            g = palavras[i:i + n]
            if len(g) == n and "".join(norm(x["w"]) for x in g) in (
                    "saibamais", "sabeamais", "sebamais", "sabamais", "saibaamais"):
                fim = re.sub(r"^.*?([.,?!]*)$", r"\1", g[-1]["w"].strip())
                saida.append(dict(p, w=" Saiba Mais" + fim, e=g[-1]["e"]))
                i += n
                break
        else:
            if norm(p["w"]) == "sabamais":
                p = dict(p, w=" Saiba Mais" + re.sub(r"^.*?([.,?!]*)$", r"\1", p["w"].strip()))
            saida.append(p)
            i += 1
    return saida


def remapear(palavras, segs, manter):
    """Palavra cujo meio caiu num silêncio tirado pelo jump cut vai para o trecho mais próximo."""
    ini, acc = [], 0.0
    for a, b in segs:
        ini.append(acc)
        acc += b - a
    saida = []
    for p in palavras:
        m = (p["s"] + p["e"]) / 2
        if not any(a - 0.05 <= m < b + 0.05 for a, b in manter):
            continue
        k = min(range(len(segs)), key=lambda i: 0 if segs[i][0] <= m < segs[i][1]
                else min(abs(m - segs[i][0]), abs(m - segs[i][1])))
        a, b = segs[k]
        s, e = min(max(p["s"], a), b - 0.05), max(min(p["e"], b), a + 0.05)
        if e - s < 0.12:
            e = min(b, s + 0.15)
        w = p["w"].strip()
        if w:
            saida.append({"w": w, "ini": p.get("ini", False), "s": s - a + ini[k], "e": e - a + ini[k]})
    saida.sort(key=lambda x: x["s"])
    return saida, acc


def achar(palavras, gatilho, depois=0.0):
    from difflib import SequenceMatcher
    alvo = norm(gatilho.replace(" ", ""))
    for i, p in enumerate(palavras):
        if p["s"] < depois:
            continue
        for n in (1, 2, 3):
            junto = "".join(norm(x["w"]) for x in palavras[i:i + n])
            if junto == alvo or (len(alvo) > 6 and SequenceMatcher(None, junto, alvo).ratio() >= 0.8):
                return p["s"]
    return None


# ---------------------------------------------------------------- vídeo

def processar(cfg, v, so_legenda=False):
    ff = cfg["ffmpeg"]
    db_voz = fe.perfil_voz(ff, v["entrada"])
    db, _, passo = db_voz
    sil = silencio(db)
    manter = encaixar(v["manter"], db, passo, sil)
    segs = jump_cuts(manter, db, passo, sil)
    pal, dur = remapear(palavras_do_video(v, db_voz), segs, manter)

    ev = [cabecalho()]
    ev += barra_progresso(dur)
    ev += gancho(v["gancho"], v.get("selo", "DIAGNÓSTICO GRATUITO"))
    ev += legendas(pal, v.get("correcoes", ()))
    sfx, ocupado, botao = [], [(0, GANCHO_DUR)], None
    if v.get("saiba_mais"):
        t = achar(pal, v["saiba_mais"], 3.0)
        if t is not None:
            botao = (t, min(t + 3.2, dur - 0.2))
            ev += botao_saiba_mais(*botao)
            sfx.append(("pop", t))
    for gat, txt in v.get("inserts", []):
        t = achar(pal, gat, 0.5)
        if t is None:
            print(f"  AVISO: gatilho '{gat}' não encontrado")
            continue
        t = max(t - 0.1, 0.2)
        if any(a - 0.2 < t < b + 0.2 for a, b in ocupado):
            t = max(b for a, b in ocupado if a - 0.2 < t < b + 0.2) + 0.25
        fim = min(t + INSERT_DUR, dur - 0.3)
        if fim - t < 1.2:
            continue
        ev += insert(t, fim, txt)
        ocupado.append((t, fim))
        sfx.append(("whoosh", t))
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    os.makedirs(os.path.dirname(ass) or ".", exist_ok=True)
    open(ass, "w", encoding="utf-8").write("".join(ev))
    if so_legenda:
        return dur, segs

    # zoom: alterna 100% / 110% só quando o trecho anterior tem 2 s ou mais
    partes, vr, ar, z = [], [], [], 1.0
    for i, (a, b) in enumerate(segs):
        if i and segs[i - 1][1] - segs[i - 1][0] >= 2.0:
            z = ZOOM_B if z == 1.0 else 1.0
        f = (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
             f"crop={W}:{H}")
        if z > 1:
            zw, zh = int(W / z) // 2 * 2, int(H / z) // 2 * 2
            zy = min(max(0, int(ZOOM_CY * H - zh * ZOOM_CY)), H - zh)
            f += f",crop={zw}:{zh}:{(W - zw) // 2}:{zy},scale={W}:{H}"
        partes.append(f + f",setsar=1[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,"
                      f"afade=t=out:st={max(0, b - a - 0.03)}:d=0.03[a{i}]")
        vr.append(f"[v{i}]")
        ar.append(f"[a{i}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filtro = ";".join(partes) + ";" + "".join(vr) + f"concat=n={len(vr)}:v=1:a=0[vc];" + \
        "".join(ar) + f"concat=n={len(ar)}:v=0:a=1,aresample=48000,aformat=channel_layouts=stereo," \
        "loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[voz];"
    # logo oficial no topo (o vídeo inteiro), por baixo do texto
    filtro += (f"[2:v]scale={LOGO_W}:-1,format=rgba,colorchannelmixer=aa=0.95[logo];"
               f"[vc][logo]overlay=(W-w)/2:{LOGO_Y}[vl];"
               f"[vl]ass='{esc}':fontsdir='{cfg['fontsdir']}'[vo];")
    tdb = v.get("trilha_db", 0)
    filtro += (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,"
               f"loudnorm=I=-28:TP=-8,aresample=48000,volume={tdb}dB,afade=t=in:d=0.6,"
               f"afade=t=out:st={max(0, dur - 1.8)}:d=1.8[tri];"
               f"[voz]asplit=2[voz1][vozsc];"
               f"[tri][vozsc]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=450[trid];")
    entradas = ["-i", v["entrada"], "-stream_loop", "-1", "-i", v["trilha"], "-loop", "1", "-i", cfg["logo"]]
    mix = ["[voz1]", "[trid]"]
    for k, (nome, t) in enumerate(sfx):
        entradas += ["-i", cfg["sfx"][nome]]
        ms = int(max(0, t - 0.25) * 1000)
        filtro += (f"[{k + 3}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-10dB,"
                   f"adelay={ms}|{ms}[s{k}];")
        mix.append(f"[s{k}]")
    filtro += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95[ao]"
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", filtro, "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{dur:.3f}",
           "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return dur, segs


def main():
    args = sys.argv[1:]
    so = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    filtro = args[1:]
    for v in cfg["videos"]:
        if filtro and not any(x in v["saida"] for x in filtro):
            continue
        d, segs = processar(cfg, v, so)
        print(f"{v['saida']}: {d:.1f}s, {len(segs)} trechos", flush=True)


if __name__ == "__main__":
    main()
