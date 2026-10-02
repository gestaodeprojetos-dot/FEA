#!/usr/bin/env python3
"""Renderiza Ads 097 e 098 - BFV com headline, legendas e CTA."""
import subprocess, os

W, H = 1080, 1920
TITULO_TAM = 140
LEGENDA_TAM = 56
LEGENDA_Y = 1540
CTA_DUR = 5.0
TITULO_DUR = 3.0
FONTSDIR = "../fonts"

def ts(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def ass_header():
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat ExtraBold,{TITULO_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H78000000,0,0,0,0,100,100,0,0,1,5,4,5,80,80,0,1
Style: Legenda,Montserrat Bold,{LEGENDA_TAM},&H00FFFFFF,&H00FFFFFF,&H10000000,&H80000000,0,0,0,0,100,100,0,0,1,3.5,2,2,90,90,{H - LEGENDA_Y - 20},1
Style: CTA,Montserrat ExtraBold,{int(TITULO_TAM * 0.85)},&H00FFFFFF,&H00FFFFFF,&H10000000,&H78000000,0,0,0,0,100,100,0,0,1,5,4,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def quebrar_titulo(texto, limite=16):
    palavras = texto.split()
    melhor = None
    for k in range(1, 4):
        def particoes(ps, k):
            if k == 1:
                yield [" ".join(ps)]
                return
            for i in range(1, len(ps) - k + 2):
                for resto in particoes(ps[i:], k - 1):
                    yield [" ".join(ps[:i])] + resto
        if k > len(palavras):
            break
        opcao = min(particoes(palavras, k), key=lambda ls: max(map(len, ls)))
        if melhor is None or max(map(len, opcao)) < max(map(len, melhor)):
            melhor = opcao
        if max(map(len, opcao)) <= limite:
            melhor = opcao
            break
    return r"\N".join(melhor)

def quebrar_linhas(texto, max_chars=22):
    if len(texto) <= max_chars:
        return texto
    palavras = texto.split()
    melhor, dif = texto, 10**9
    for i in range(1, len(palavras)):
        l1, l2 = " ".join(palavras[:i]), " ".join(palavras[i:])
        d = abs(len(l1) - len(l2))
        if d < dif:
            melhor, dif = l1 + r"\N" + l2, d
    return melhor


ADS = [
    {
        "id": "097",
        "entrada": "raw/IMG_7197.MOV",
        "saida": "out/Ads 097 - BFV.mp4",
        "titulo": "Chegou a hora de se tornar\nmeu aluno vitalício",
        "legendas": [
            (3.0, 4.8, "por isso eu vou até colocar o bonezinho"),
            (4.8, 7.5, "para te lembrar que dia 20 de outubro teremos"),
            (7.5, 9.5, "a abertura das inscrições"),
            (9.5, 11.0, "da Black Friday Vitalícia"),
            (11.2, 13.0, "teu último curso de harmonização facial para o"),
            (13.0, 14.2, "resto da sua vida"),
            (14.5, 15.1, "o que vai acontecer?"),
            (15.2, 16.5, "dia 20 de outubro eu vou fazer uma live"),
            (16.5, 17.0, "de abertura"),
            (17.0, 20.0, "onde você vai ter acesso e vai entender como"),
            (20.0, 21.5, "que vai funcionar a Black Friday"),
            (21.5, 23.5, "a gente vai ter muitos bônus"),
            (23.5, 25.5, "inclusive bônus presenciais"),
            (25.5, 26.5, "pós-graduação incluída"),
            (26.5, 27.5, "então assim, loucura"),
            (27.5, 29.5, "isso aqui é coisa de doido"),
            (29.5, 31.0, "não perca essa oportunidade"),
            (31.0, 33.0, "então esteja comigo dia 20 de outubro"),
            (33.0, 36.0, "participe da nossa abertura de inscrições"),
            (36.0, 38.5, "esteja ao vivo para você poder ter acesso"),
            (38.5, 40.5, "a todos os bônus especiais"),
            (40.5, 42.0, "e compre o seu último curso de harmonização"),
            (42.0, 43.5, "facial da vida"),
            (43.5, 45.0, "aqui você vai ter acesso"),
            (45.0, 47.0, "a todos os cursos de toxina"),
            (47.0, 49.0, "preenchedores, bioestimuladores"),
            (49.0, 51.0, "fios, anatomia, intercorrências"),
            (51.0, 53.0, "procedimentos corporais"),
            (53.0, 55.5, "todas as atualizações, todas as novidades"),
            (55.5, 57.5, "tudo que eu for estudar até o fim da minha"),
            (57.5, 58.0, "vida"),
            (58.0, 60.5, "você vai ter acesso se inscrevendo"),
            (60.5, 62.5, "dia 20 de outubro e nunca mais precisando"),
            (62.5, 63.0, "pagar"),
            (63.0, 65.0, "um real a mais por isso, então não perca"),
            (65.0, 67.0, "essa oportunidade, quem se inscreveu"),
            (67.0, 68.0, "nas anteriores não se arrependeu"),
            (68.0, 69.5, "não perde essa oportunidade"),
            (69.5, 70.5, "é para o resto da vida"),
        ],
    },
    {
        "id": "098",
        "entrada": "raw/ADS098_joined.mp4",
        "saida": "out/Ads 098 - BFV.mp4",
        "titulo": "Todos os cursos,\npara o resto da vida",
        "legendas": [
            (4.0, 6.0, "então vou colocar aqui até"),
            (6.0, 8.0, "o bonezinho para lembrar vocês que dia 20"),
            (8.0, 10.5, "do 10 eu vou abrir as inscrições para você"),
            (10.5, 13.0, "comprar o seu último curso de harmonização"),
            (13.0, 14.0, "facial da vida"),
            (14.0, 17.0, "o curso vitalício vai te dar acesso a todos"),
            (17.0, 18.5, "os cursos que eu já fiz"),
            (18.5, 20.5, "todos que eu for fazer com acesso vitalício"),
            (21.0, 22.5, "ou seja"),
            (23.0, 25.5, "todas as abordagens, todos os cursos"),
            (25.5, 27.5, "todas as técnicas"),
            (27.5, 29.0, "todas as novidades"),
            (29.0, 31.5, "todas as atualizações para o resto da vida"),
            (31.5, 33.5, "se inscrevendo dia 20 de outubro e nunca"),
            (33.5, 35.5, "mais precisando pagar um real a mais"),
            (35.5, 36.5, "por isso"),
            (36.5, 38.5, "então aproveita essa oportunidade"),
            (38.5, 40.5, "dia 20 de outubro eu vou fazer uma live"),
            (40.5, 41.0, "de abertura"),
            (41.0, 43.5, "onde você vai entender melhor todos os bônus"),
            (43.5, 45.5, "teremos bônus presenciais"),
            (45.5, 48.5, "teremos bônus especiais como pós-graduação"),
            (48.5, 49.0, "incluída"),
            (49.0, 51.5, "então assim, é muita, muita, muita coisa"),
            (51.5, 54.0, "inclusive é até assustador o que eu estou"),
            (54.0, 54.5, "fazendo"),
            (54.5, 56.5, "isso é loucura, não perca essa oportunidade"),
            (56.5, 58.5, "esteja ao vivo comigo na live de abertura"),
            (58.5, 59.5, "20 de outubro a gente se vê"),
            (59.5, 60.5, "na Black Friday Vitalícia"),
        ],
    },
]


def gerar_ass(ad, duracao, caminho):
    linhas = [ass_header()]
    titulo = ad["titulo"].replace("\n", r"\N")
    linhas.append(f"Dialogue: 1,{ts(0)},{ts(TITULO_DUR)},Titulo,,0,0,0,,{{\\fad(0,250)}}{titulo}\n")

    cta_inicio = duracao - CTA_DUR
    for s, e, texto in ad["legendas"]:
        if s >= cta_inicio:
            break
        e = min(e, cta_inicio)
        if s < TITULO_DUR:
            s = TITULO_DUR
        if s >= e:
            continue
        linhas.append(f"Dialogue: 0,{ts(s)},{ts(e)},Legenda,,0,0,0,,{quebrar_linhas(texto)}\n")

    linhas.append(f"Dialogue: 1,{ts(cta_inicio)},{ts(duracao)},CTA,,0,0,0,,{{\\fad(250,0)}}Toque em\\NSaiba Mais\n")
    open(caminho, "w", encoding="utf-8").write("".join(linhas))


def renderizar(ad, previa=False):
    entrada = ad["entrada"]
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", entrada]
    ).decode().strip())
    print(f"  Duração bruta: {dur:.1f}s")

    ass_path = ad["saida"].rsplit(".", 1)[0] + ".ass"
    gerar_ass(ad, dur, ass_path)

    esc = ass_path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filtro = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
              f"ass='{esc}':fontsdir='{FONTSDIR}'")

    vb = int(min(8000, 26.5 * 8 * 1024 * 1024 / 1000 / dur - 96))
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", entrada,
        "-vf", filtro,
        "-c:v", "libx264", "-preset", "medium",
        "-b:v", f"{vb}k", "-maxrate", f"{vb * 3 // 2}k", "-bufsize", f"{vb * 2}k",
        "-profile:v", "high",
        "-c:a", "aac", "-b:a", "96k",
        "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart",
        ad["saida"],
    ]
    subprocess.run(cmd, check=True)
    sz = os.path.getsize(ad["saida"]) / 1024 / 1024
    print(f"  Saída: {ad['saida']} ({sz:.1f} MB)")


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    for ad in ADS:
        print(f"\n--- Ads {ad['id']} ---")
        renderizar(ad)
    print("\nPronto.")
