#!/usr/bin/env python3
"""FEA: criativo de anúncio (Ads) a partir de bruto do Dr., com trilha, destaques, inserts e CTA.

Diferente do Reels de procedimento (fea_editar_video.py): sem título de 3 s, com trilha sonora,
frases de impacto em fonte maior (dourado da Black Friday Vitalícia), inserts de gravação de
tela e CTA curto no final. A legenda segue o padrão conteúdo (Montserrat Bold 56, branca).

Uso:
    python3 fea_criativo_ads.py projeto.json [--so-legenda] [trecho_do_nome ...]

projeto.json:
{
  "ffmpeg": "...", "fontsdir": "fonts",
  "musica": ["musica/m1.wav", "musica/m2.wav"],   # emendadas com crossfade, em loop
  "musica_cortes": [66, 51],                       # até onde cada faixa vai (s) antes do crossfade
  "cta": "id/CTA-5s.mp4",
  "videos": [{
    "entrada": "brutos/IMG.MOV", "transcricao": "tr/IMG.json", "saida": "out/Ads.mp4",
    "manter": [[0, 44.9], ...],                     # segundos do bruto
    "apertar_pausas": 0.5,                          # pausa maior que isso (s) encolhe para ~0,25 s
    "destaques": [[28.1, 29.9, "120 mil reais"]],   # s do bruto: no lugar da legenda, fonte maior
    "tela": {"arquivo": "tela.mov", "offset": 2.09, "crop": [x, y, w, h]},
    "inserts": [[4.0, 13.2, "split"], [30.3, 33.7, "card", 30.0]],
        # s do bruto. "split": tela em cima (sincronizada pelo offset), Dr. embaixo.
        # "card": tela num cartão sobre o vídeo; o 4º valor é o tempo da tela (sem sincronia).
    "logo": ["id/logo_gold.png", 0, 3.0],          # logo no topo nos primeiros segundos
    "correcoes": [["regex", "troca"]]
  }]
}
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fea_editar_video as E  # noqa: E402

W, H = E.W, E.H
DOURADO = "&H0072BFED"        # #EDBF72, dourado da LP Black Friday Vitalícia
DESTAQUE_TAM = 92
DESTAQUE_Y = 1500
MUSICA_VOL = 0.07             # trilha por baixo da voz (0,13 ficou alta, Keila 22/10/2026)
MUSICA_VOL_CTA = 0.10         # no CTA a trilha sobe só um pouco, em rampa de 1 s (0,45 incomodou, Keila 22/10/2026)


def palavras_do_projeto(v, db_voz):
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    palavras = []
    for seg in trans:
        for i, w in enumerate(seg["words"]):
            w = dict(w)
            if i and palavras and not w["w"].startswith(" "):
                palavras[-1]["w"] += w["w"]
                palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                continue
            palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), e0=w["e"], ini=(i == 0)))
    palavras.sort(key=lambda p: p["s"])
    palavras = E.numerar_enumeracao(palavras)
    for a, b in v.get("remover_legenda", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    return E.ancorar_na_voz(palavras, *db_voz)


def apertar_pausas(manter, db, passo, maximo):
    """Encolhe as pausas longas dentro de cada trecho: o criativo fica sem respiro morto."""
    import numpy as np
    limiar = max(38.0, float(np.percentile(db, 5)) + 12)
    novo = []
    for a, b in manter:
        i0, i1 = int(a / passo), min(len(db), int(b / passo))
        ini = a
        k = i0
        while k < i1:
            if db[k] < limiar:
                j = k
                while j < i1 and db[j] < limiar:
                    j += 1
                s, e = k * passo, j * passo
                if e - s > maximo and s > ini + 0.3 and e < b - 0.1:
                    novo.append([ini, s + 0.12])
                    ini = e - 0.12
                k = j
            else:
                k += 1
        novo.append([ini, b])
    return [t for t in novo if t[1] - t[0] > 0.2]


def para_editado(t, manter):
    """Tempo do bruto -> tempo na linha editada (None se cortado)."""
    off = 0.0
    for a, b in manter:
        if a <= t <= b:
            return off + t - a
        off += b - a
    return None


def gerar_ass(v, palavras_brutas, manter, caminho):
    destaques = v.get("destaques", [])
    # palavras dentro de um destaque saem da legenda normal
    normais = [p for p in palavras_brutas
               if not any(a <= (p["s"] + p["e"]) / 2 <= b for a, b, _ in destaques)]
    # palavra com o meio numa pausa encolhida, mas com a fala dentro do trecho mantido
    # ("Curso" de "Curso de preenchimento express" sumia da legenda): encaixa no trecho
    for p in normais:
        meio = (p["s"] + p["e"]) / 2
        if not any(a <= meio < b for a, b in manter):
            sobra = [(min(p["e"], b) - max(p["s"], a), a, b) for a, b in manter]
            ov, a, b = max(sobra)
            if ov > 0.05:
                p["s"], p["e"] = max(p["s"], a), min(p["e"], b)
    palavras, duracao = E.remapear_palavras(normais, manter)
    linhas = [E.ass_header().replace(
        "[Events]",
        f"Style: Destaque,Montserrat ExtraBold,{DESTAQUE_TAM},{DOURADO},{DOURADO},&H00000000,"
        f"&H80000000,0,0,0,0,100,100,0,0,1,5,3,5,60,60,0,1\n\n[Events]")]
    janelas = []
    for a, b, texto in destaques:
        ws = [p for p in palavras_brutas if a <= (p["s"] + p["e"]) / 2 <= b]
        s0 = para_editado(ws[0]["s"] if ws else a, manter)
        e0 = para_editado(ws[-1]["e"] if ws else b, manter)
        if s0 is None or e0 is None:
            print(f"  AVISO: destaque fora dos trechos mantidos: {texto}")
            continue
        e0 = max(e0 + 0.35, s0 + 1.2)
        janelas.append((s0, e0))
        partes = E.quebrar_linhas(texto).split(r"\N")
        h = DESTAQUE_TAM * 0.85
        y0 = DESTAQUE_Y - (len(partes) - 1) * h / 2
        for i, parte in enumerate(partes):
            linhas.append(
                f"Dialogue: 2,{E.ts(s0)},{E.ts(e0)},Destaque,,0,0,0,,"
                rf"{{\an5\pos({W // 2},{y0 + i * h:.0f})\fscx60\fscy60\t(0,160,\fscx108\fscy108)"
                rf"\t(160,260,\fscx100\fscy100)\fad(0,120)}}{parte}" "\n")
    blocos = E.blocos_legenda(palavras)
    for i, bloco in enumerate(blocos):
        s, e = bloco[0]["s"], bloco[-1]["e"] + 0.15
        prox = blocos[i + 1] if i + 1 < len(blocos) else None
        if prox:
            e = min(e, prox[0]["s"])
        for js, je in janelas:      # legenda normal nunca embaixo do destaque
            if s < je and e > js:
                if s >= js:
                    s = je
                else:
                    e = js
        if e - s < 0.2:
            continue
        if len(bloco) == 1 and re.sub(r"[^\w]", "", bloco[0]["w"]).lower() in E.LIGACAO | {"é", "eu"}:
            continue
        texto = E.quebrar_linhas(E.limpar(E.pontuar(E.corrigir(E.juntar_texto(bloco),
                                                                v.get("correcoes", ())))))
        linhas += E.dialogos_linhas(0, s, min(e, duracao), "Legenda", texto)
    open(caminho, "w", encoding="utf-8").write("".join(linhas))
    return duracao




def renderizar(cfg, v, so_legenda=False):
    ff = cfg["ffmpeg"]
    db_voz = E.perfil_voz(ff, v["entrada"])
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    manter = E.encaixar_cortes(v["manter"], db_voz[0], db_voz[2],
                               [w for seg in trans for w in seg["words"]])
    manter = E.inicio_na_fala(manter, db_voz[0], db_voz[2])
    if v.get("apertar_pausas"):
        manter = apertar_pausas(manter, db_voz[0], db_voz[2], v["apertar_pausas"])
    palavras = palavras_do_projeto(v, db_voz)
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    duracao = gerar_ass(v, palavras, manter, ass)
    if so_legenda:
        return duracao

    # ---- vídeo: trechos do bruto, com o layout de cada instante (normal, split, card)
    tela = v.get("tela")
    inserts = v.get("inserts", [])
    entradas = ["-i", v["entrada"]]
    if tela:
        entradas += ["-i", tela["arquivo"]]
    partes, vrot, arot = [], [], []
    n = 0
    for i, (a, b) in enumerate(manter):
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02):.3f}:d=0.02[a{i}]")
        arot.append(f"[a{i}]")
        cortes = sorted({a, b} | {t for z in inserts for t in z[:2] if a < t < b})
        for x0, x1 in zip(cortes, cortes[1:]):
            if x1 - x0 < 0.02:
                continue
            ins = next((z for z in inserts if z[0] <= x0 + 1e-3 and x1 <= z[1] + 1e-3), None)
            dr = f"[0:v]trim={x0}:{x1},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
            if ins and tela:
                cx, cy, cw, ch = tela["crop"]
                if ins[2] == "split":
                    t0, t1 = x0 + tela["offset"], x1 + tela["offset"]
                    # tela inteira na largura (sem cortar as laterais), Dr. no resto do quadro
                    alt_t = int(W * ch / cw) // 2 * 2
                    alt_dr = H - alt_t
                    yfoco = min(v.get("split_dr_y", 420), H - alt_dr)
                    partes.append(f"[1:v]trim={t0}:{t1},setpts=PTS-STARTPTS,fps=30,crop={cw}:{ch}:{cx}:{cy},"
                                  f"scale={W}:{alt_t},setsar=1[t{n}]")
                    partes.append(f"{dr},crop={W}:{alt_dr}:0:{yfoco}[d{n}]")
                    partes.append(f"[t{n}][d{n}]vstack,drawbox=x=0:y={alt_t - 3}:w={W}:h=6:color=0xEDBF72@1:t=fill[v{n}]")
                else:   # card
                    t0 = ins[3] + (x0 - ins[0])
                    t1 = t0 + (x1 - x0)
                    cw2 = W - 80
                    ch2 = int(cw2 * ch / cw) // 2 * 2
                    partes.append(f"[1:v]trim={t0}:{t1},setpts=PTS-STARTPTS,fps=30,crop={cw}:{ch}:{cx}:{cy},"
                                  f"scale={cw2}:{ch2},pad={cw2 + 12}:{ch2 + 12}:6:6:color=0xEDBF72,setsar=1[t{n}]")
                    partes.append(f"{dr}[d{n}]")
                    partes.append(f"[d{n}][t{n}]overlay=(W-w)/2:{v.get('card_y', 330)}:shortest=1[v{n}]")
            else:
                partes.append(f"{dr}[v{n}]")
            vrot.append(f"[v{n}]")
            n += 1
    esc = os.path.abspath(ass).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    fontes = os.path.abspath(cfg["fontsdir"])
    filtro = ";".join(partes) + ";" + "".join(vrot) + f"concat=n={len(vrot)}:v=1:a=0[vc];" \
        + "".join(arot) + f"concat=n={len(arot)}:v=0:a=1[ac];"
    ultimo = "[vc]"
    if v.get("logo"):
        arq, l0, l1 = v["logo"]
        entradas += ["-loop", "1", "-t", str(l1), "-i", arq]
        il = 1 + (1 if tela else 0)
        filtro += (f"[{il}:v]scale=560:-1,format=rgba,fade=t=out:st={l1 - 0.4}:d=0.4:alpha=1[lg];"
                   f"[vc][lg]overlay=(W-w)/2:150:enable='between(t,{l0},{l1})'[vl];")
        ultimo = "[vl]"
    filtro += f"{ultimo}ass='{esc}':fontsdir='{fontes}',fps=30,format=yuv420p[vo]"

    # ---- CTA no fim, trilha por baixo da voz e subindo no CTA
    cta = cfg["cta"]
    ic = len([x for x in entradas if x == "-i"])
    entradas += ["-i", cta]
    r = subprocess.run([ff, "-i", cta], capture_output=True, text=True).stderr
    hh, mm, ss = re.search(r"Duration: ([\d:.]+)", r).group(1).split(":")
    dcta = float(hh) * 3600 + float(mm) * 60 + float(ss)
    total = duracao + dcta
    filtro += (f";[{ic}:v]scale={W}:{H},setsar=1,fps=30,format=yuv420p[vcta];[vo][vcta]concat=n=2:v=1:a=0[vfim]"
               + (f";[ac]aresample=48000,aformat=channel_layouts=stereo[acv];[{ic}:a]aresample=48000,"
                  f"aformat=channel_layouts=stereo[acta];[acv][acta]concat=n=2:v=0:a=1[voz]"
                  if cfg.get("cta_com_som") else f";[ac]apad=whole_dur={total:.3f}[voz]"))
    faixas, cortes = cfg["musica"], cfg["musica_cortes"]
    im = ic + 1
    soma, k, ms = 0.0, 0, []
    while soma < total + 1:
        j = k % len(faixas)
        entradas += ["-i", faixas[j]]
        ms.append((im + k, cortes[j]))
        soma += cortes[j] - (2 if k else 0)
        k += 1
    cad = f"[{ms[0][0]}:a]atrim=0:{ms[0][1]},aresample=48000,aformat=channel_layouts=stereo[m0]"
    for q, (idx, c) in enumerate(ms[1:], 1):
        cad += (f";[{idx}:a]atrim=0:{c},aresample=48000,aformat=channel_layouts=stereo[mi{q}]"
                f";[m{q - 1}][mi{q}]acrossfade=d=2[m{q}]")
    v0, v1 = cfg.get("musica_vol", MUSICA_VOL), cfg.get("musica_vol_cta", MUSICA_VOL_CTA)
    # compressor achata o crescendo da própria faixa (o "subir o tom" no final incomodava)
    vol = (f"acompressor=threshold=-24dB:ratio=6:attack=20:release=400,"
           f"volume='if(lt(t,{duracao:.3f}),{v0},if(lt(t,{duracao + 1:.3f}),{v0}+({v1}-{v0})*(t-{duracao:.3f}),{v1}))':eval=frame,"
           f"atrim=0:{total:.3f},afade=t=in:d=0.6,"
           # CTA com som próprio (impacto da logo + digitação, Keila 22/10/2026): a trilha sai antes dele
           + (f"afade=t=out:st={duracao - 0.4:.3f}:d=0.4" if cfg.get("cta_com_som")
              else f"afade=t=out:st={total - 1.5:.3f}:d=1.5"))
    filtro += f";{cad};[m{len(ms) - 1}]{vol}[mus];[voz]aresample=48000,aformat=channel_layouts=stereo[voz2]" \
              f";[voz2][mus]amix=inputs=2:duration=first:normalize=0[afim]"
    cmd = [ff, "-y", "-v", "error", *entradas, "-filter_complex", filtro,
           "-map", "[vfim]", "-map", "[afim]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-t", f"{total:.3f}", "-movflags", "+faststart", v["saida"]]
    subprocess.run(cmd, check=True)
    return total


def main():
    args = sys.argv[1:]
    so_legenda = "--so-legenda" in args
    args = [a for a in args if a != "--so-legenda"]
    cfg = json.load(open(args[0], encoding="utf-8"))
    so = args[1:]
    for v in cfg["videos"]:
        if so and not any(x in v["saida"] for x in so):
            continue
        d = renderizar(cfg, v, so_legenda)
        print(f"{v['saida']}: {d:.1f}s", flush=True)


if __name__ == "__main__":
    main()
