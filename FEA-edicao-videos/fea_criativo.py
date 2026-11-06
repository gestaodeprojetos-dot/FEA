#!/usr/bin/env python3
"""FEA: edição de CRIATIVO (anúncio) vertical, Dr. João falando para a câmera.

Diferente do Reels de procedimento (fea_editar_video.py), aqui o vídeo é anúncio:
  - jump cuts: os silêncios entre frases saem (ritmo de anúncio)
  - zoom alternado a cada corte (punch-in), para dar dinâmica sem B-roll
  - headline (gancho) no topo, em cartão roxo, nos primeiros segundos
  - legenda desde o início, em blocos curtos, com palavra-chave destacada
  - inserts animados (cartões lavanda) quando o Dr. fala a palavra-gatilho, com whoosh
  - botão "SAIBA MAIS" com seta quando ele manda clicar
  - barra de progresso roxa no topo
  - trilha sonora diferente por vídeo, abaixando sozinha quando o Dr. fala (ducking)

Uso:
    python3 fea_criativo.py projeto.json [--so-legenda] [trecho_do_nome ...]

projeto.json:
{
  "ffmpeg": "...", "fontsdir": "fonts", "sfx": {"whoosh": "...", "pop": "..."},
  "videos": [{
     "entrada": "brutos/IMG_9008.MOV", "transcricao": "tr/IMG_9008.json",
     "saida": "out/1- Gancho.mp4",
     "gancho": "O método por trás de cada tratamento fechado",
     "manter": [[0.4, 63.6]],              # trechos do bruto (antes do jump cut automático)
     "remover_legenda": [], "correcoes": [],
     "destaques": ["método", "roteiro"],     # palavras com destaque na legenda
     "inserts": [["método", "MÉTODO REPLICÁVEL"], ["formulário", "FORMULÁRIO DE 2 MINUTOS"]],
     "saiba_mais": "saiba mais",             # gatilho do botão (null = sem botão)
     "trilha": "trilhas/03.wav", "trilha_db": -20
  }]
}
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
ROXO, AZUL, LAVANDA, BRANCO, PRETO = "&H0099455B", "&H00BB4638", "&H00E9D1D0", "&H00FFFFFF", "&H00000000"
LEG_TAM, LEG_Y = 76, 1480
GANCHO_TAM, GANCHO_Y, GANCHO_DUR = 70, 250, 4.0
INSERT_TAM, INSERT_Y, INSERT_DUR = 70, 1130, 2.2
ZOOM_B, ZOOM_CY = 1.12, 0.40
SILENCIO_MIN, MARGEM = 0.40, 0.12


def cabecalho():
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,Montserrat ExtraBold,{LEG_TAM},{BRANCO},{BRANCO},{PRETO},&H80000000,0,0,0,0,100,100,0,0,1,5,2,5,60,60,0,1
Style: Card,Montserrat ExtraBold,{INSERT_TAM},{ROXO},{ROXO},{PRETO},&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Gancho,Montserrat ExtraBold,{GANCHO_TAM},{BRANCO},{BRANCO},{PRETO},&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Forma,Montserrat ExtraBold,20,{ROXO},{ROXO},{ROXO},&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t):
    return fe.ts(t)


def retangulo(w, h, r):
    """Desenho ASS de retângulo com cantos arredondados (origem no canto superior esquerdo)."""
    k = r * 0.45
    return (f"m {r} 0 l {w - r} 0 b {w - k} 0 {w} {k} {w} {r} l {w} {h - r} "
            f"b {w} {h - k} {w - k} {h} {w - r} {h} l {r} {h} b {k} {h} 0 {h - k} 0 {h - r} "
            f"l 0 {r} b 0 {k} {k} 0 {r} 0")


def largura_txt(txt, tam):
    # Montserrat ExtraBold: ~0,66 do tamanho por caractere em caixa alta, ~0,58 em minúscula
    return sum(tam * (0.62 if c.isupper() or c.isdigit() else 0.30 if c == " " else 0.55) for c in txt)


def quebrar(txt, maxc):
    if len(txt) <= maxc:
        return [txt]
    ps = txt.split()
    melhor = min(((" ".join(ps[:i]), " ".join(ps[i:])) for i in range(1, len(ps))),
                 key=lambda p: max(len(p[0]), len(p[1])))
    return list(melhor)


POP = r"\fscx0\fscy0\t(0,160,\fscx112\fscy112)\t(160,260,\fscx100\fscy100)"


def cartao(s, e, txt, y, tam, cor_fundo, cor_txt, maxc=18, pad=(46, 26)):
    """Cartão arredondado com texto, entrando com 'pop' (escala) e saindo com fade."""
    linhas = quebrar(txt, maxc)
    lh = tam * 1.08
    w = max(largura_txt(l, tam) for l in linhas) + pad[0] * 2
    h = lh * len(linhas) + pad[1] * 2
    w, h = int(min(w, W - 80)), int(h)
    ev = [f"Dialogue: 2,{ts(s)},{ts(e)},Forma,,0,0,0,,"
          f"{{\\an7\\pos({(W - w) // 2},{int(y - h / 2)})\\org({W // 2},{y})\\1c{cor_fundo}\\bord0\\shad0"
          f"\\fad(0,180){POP}\\p1}}{retangulo(w, h, 28)}{{\\p0}}\n"]
    y0 = y - lh * (len(linhas) - 1) / 2
    for i, l in enumerate(linhas):
        ev.append(f"Dialogue: 3,{ts(s)},{ts(e)},Card,,0,0,0,,"
                  f"{{\\an5\\pos({W // 2},{int(y0 + i * lh)})\\org({W // 2},{y})\\fs{tam}\\1c{cor_txt}"
                  f"\\fad(0,180){POP}}}{l}\n")
    return ev


def botao_saiba_mais(s, e):
    ev = cartao(s, e, "SAIBA MAIS", 1020, 64, ROXO, BRANCO, maxc=20, pad=(60, 30))
    # seta para baixo (aponta para o botão do anúncio), quicando
    seta = "m 0 0 l 60 0 l 60 50 l 95 50 l 30 115 l -35 50 l 0 50 l 0 0"
    x, y = W // 2 - 30, 1120
    t, k = s + 0.25, 0
    while t < e:
        dy = 0 if k % 2 == 0 else 28
        ev.append(f"Dialogue: 2,{ts(t)},{ts(min(e, t + 0.45))},Forma,,0,0,0,,"
                  f"{{\\an7\\move({x},{y + dy},{x},{y + 28 - dy})\\1c{BRANCO}\\3c{ROXO}\\bord5\\p1}}{seta}{{\\p0}}\n")
        t += 0.45
        k += 1
    return ev


def barra_progresso(d):
    return [f"Dialogue: 4,{ts(0)},{ts(d)},Forma,,0,0,0,,"
            f"{{\\an7\\pos(0,0)\\1c{ROXO}\\clip(0,0,0,14)\\t(0,{int(d * 1000)},\\clip(0,0,{W},14))\\p1}}"
            f"m 0 0 l {W} 0 l {W} 14 l 0 14{{\\p0}}\n"]


def gancho(txt):
    # cartão roxo no topo, texto branco; fica os primeiros segundos
    return cartao(0.0, GANCHO_DUR, txt, GANCHO_Y, GANCHO_TAM, ROXO, BRANCO, maxc=24, pad=(44, 24))


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


def legenda(blocos, destaques, correcoes, ini=0.0):
    ev = []
    dest = {norm(d) for d in destaques}
    for i, b in enumerate(blocos):
        s, e = b[0]["s"], b[-1]["e"] + 0.12
        if i + 1 < len(blocos):
            e = min(e, blocos[i + 1][0]["s"])
        if e <= ini:
            continue
        s = max(s, ini)
        if e - s < 0.25:
            e = s + 0.25
        texto = fe.limpar(fe.pontuar(fe.corrigir(fe.juntar_texto(b), correcoes)))
        if not texto.strip():
            continue
        linhas = quebrar(texto.replace("Saiba Mais", "Saiba\x00Mais"), 18)
        out = []
        for l in linhas:
            ws = []
            for w in l.split(" "):
                w = w.replace("\x00", " ")
                ws.append(f"{{\\3c{ROXO}\\bord8}}{w}{{\\3c{PRETO}\\bord5}}" if norm(w) in dest else w)
            out.append(" ".join(ws))
        lh = LEG_TAM * 0.92
        y0 = LEG_Y - lh * (len(out) - 1) / 2
        for k, l in enumerate(out):
            ev.append(f"Dialogue: 1,{ts(s)},{ts(e)},Leg,,0,0,0,,"
                      f"{{\\an5\\pos({W // 2},{int(y0 + k * lh)})\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{l}\n")
    return ev


def jump_cuts(manter, db, limiar, passo):
    """Divide cada trecho mantido nos silêncios longos (> SILENCIO_MIN), deixando MARGEM de respiro."""
    novo = []
    for a, b in manter:
        i0, i1 = int(a / passo), min(len(db), int(b / passo))
        fala = db[i0:i1] >= limiar
        ini, k = a, 0
        while k < len(fala):
            if not fala[k]:
                j = k
                while j < len(fala) and not fala[j]:
                    j += 1
                t0, t1 = a + k * passo, a + j * passo
                if t1 - t0 >= SILENCIO_MIN and k > 0 and j < len(fala):
                    if t0 + MARGEM - ini > 0.3:
                        novo.append([round(ini, 3), round(t0 + MARGEM, 3)])
                    ini = t1 - MARGEM
                k = j
            else:
                k += 1
        if b - ini > 0.3:
            novo.append([round(ini, 3), round(b, 3)])
    return novo


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
    # "Saiba Mais" (botão do anúncio) numa palavra só, para nunca quebrar entre duas legendas
    # e sair com a grafia certa ("Sabamais", "Seba Mais", "sabe a mais", "Saiba / mais")
    saida, i = [], 0
    while i < len(palavras):
        p = palavras[i]
        for n in (3, 2):
            grupo = palavras[i:i + n]
            junto = "".join(norm(x["w"]) for x in grupo)
            if len(grupo) == n and junto in ("saibamais", "sabeamais", "sebamais", "sabamais", "saibaamais"):
                fim = re.sub(r"^.*?([.,?!]*)$", r"\1", grupo[-1]["w"].strip())
                saida.append(dict(p, w=" Saiba Mais" + fim, e=grupo[-1]["e"]))
                i += n
                break
        else:
            if norm(p["w"]) == "sabamais":
                p = dict(p, w=" Saiba Mais" + re.sub(r"^.*?([.,?!]*)$", r"\1", p["w"].strip()))
            saida.append(p)
            i += 1
    return saida


def achar(palavras, gatilho, depois=0.0):
    """Instante em que o Dr. fala o gatilho. Compara sem espaço e com tolerância, porque a
    transcrição escreve "Saiba Mais" como "Sabamais", "Seba Mais" ou "sabe a mais"."""
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


def remapear(palavras, segs, manter):
    """Como fe.remapear_palavras, mas a palavra cujo meio caiu num silêncio tirado pelo jump cut
    (tempo da transcrição esticado) vai para o trecho mais próximo, em vez de sumir da legenda
    ("Clique agora em Saiba Mais" saía sem o "Clique")."""
    ini, acc = [], 0.0
    for a, b in segs:
        ini.append(acc)
        acc += b - a
    saida = []
    for p in palavras:
        m = (p["s"] + p["e"]) / 2
        if not any(a <= m < b for a, b in manter):
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


def processar(cfg, v, so_legenda=False):
    ff = cfg["ffmpeg"]
    db_voz = fe.perfil_voz(ff, v["entrada"])
    db, limiar, passo = db_voz
    manter = fe.encaixar_cortes(v["manter"], db, passo)
    segs = jump_cuts(manter, db, limiar, passo)
    palavras = palavras_do_video(v, db_voz)
    pal, dur = remapear(palavras, segs, manter)

    fe.MAX_CHARS_LINHA, fe.MAX_PALAVRAS_BLOCO, fe.PAUSA_QUEBRA = 14, 5, 0.35
    blocos = fe.blocos_legenda(pal)

    fe.NOMES_PROPRIOS.update({"Saiba", "Instagram"})
    ev = [cabecalho()]
    ev += barra_progresso(dur)
    ev += gancho(v["gancho"])
    ev += legenda(blocos, v.get("destaques", []), v.get("correcoes", ()))
    sfx = []
    ocupado = [(0, GANCHO_DUR)]
    for gat, txt in v.get("inserts", []):
        t = achar(pal, gat, 0.5)
        if t is None:
            print(f"  AVISO: gatilho '{gat}' não encontrado")
            continue
        t = max(t - 0.1, 0.2)
        if any(a - 0.2 < t < b + 0.2 for a, b in ocupado):
            t = max(b for a, b in ocupado if a - 0.2 < t < b + 0.2) + 0.25
        fim = min(t + INSERT_DUR, dur - 0.3)
        ev += cartao(t, fim, txt, INSERT_Y, INSERT_TAM, LAVANDA, ROXO)
        ocupado.append((t, fim))
        sfx.append(("whoosh", t))
    if v.get("saiba_mais"):
        t = achar(pal, v["saiba_mais"], 3.0)
        if t is not None:
            fim = min(t + 3.2, dur - 0.2)
            ev += botao_saiba_mais(t, fim)
            sfx.append(("pop", t))
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    os.makedirs(os.path.dirname(ass) or ".", exist_ok=True)
    open(ass, "w", encoding="utf-8").write("".join(ev))
    if so_legenda:
        return dur

    # vídeo: cada trecho com zoom alternado (1,00 / ZOOM_B), centro no rosto
    partes, vr, ar = [], [], []
    for i, (a, b) in enumerate(segs):
        z = 1.0 if i % 2 == 0 else ZOOM_B
        f = (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
             f"crop={W}:{H}")
        if z > 1:
            zw, zh = int(W / z) // 2 * 2, int(H / z) // 2 * 2
            zy = min(max(0, int(ZOOM_CY * H - zh * ZOOM_CY)), H - zh)
            f += f",crop={zw}:{zh}:{(W - zw) // 2}:{zy},scale={W}:{H}"
        partes.append(f + f",setsar=1[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
                      f"afade=t=out:st={max(0, b - a - 0.015)}:d=0.015[a{i}]")
        vr.append(f"[v{i}]")
        ar.append(f"[a{i}]")
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filtro = ";".join(partes) + ";" + "".join(vr) + f"concat=n={len(vr)}:v=1:a=0[vc];" + \
        "".join(ar) + f"concat=n={len(ar)}:v=0:a=1,aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[voz];" + \
        f"[vc]ass='{esc}':fontsdir='{cfg['fontsdir']}'[vo];"
    # trilha em loop, abaixando quando há voz (sidechain), com fade
    tdb = v.get("trilha_db", 0)   # ajuste fino sobre o nível padrão da trilha (-28 LUFS, ~13 dB abaixo da voz)
    filtro += (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,"
               f"loudnorm=I=-28:TP=-8,aresample=48000,volume={tdb}dB,afade=t=in:d=0.6,afade=t=out:st={max(0, dur - 1.8)}:d=1.8[tri];"
               f"[voz]asplit=2[voz1][vozsc];"
               f"[tri][vozsc]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=450[trid];")
    entradas = ["-i", v["entrada"], "-stream_loop", "-1", "-i", v["trilha"]]
    mix = ["[voz1]", "[trid]"]
    for k, (nome, t) in enumerate(sfx):
        entradas += ["-i", cfg["sfx"][nome]]
        ms = int(max(0, t - 0.25) * 1000)
        filtro += (f"[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-9dB,"
                   f"adelay={ms}|{ms}[s{k}];")
        mix.append(f"[s{k}]")
    filtro += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95[ao]"
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", filtro, "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{dur:.3f}",
           "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return dur


def main():
    args = sys.argv[1:]
    so = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    filtro = args[1:]
    for v in cfg["videos"]:
        if filtro and not any(x in v["saida"] for x in filtro):
            continue
        d = processar(cfg, v, so)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
