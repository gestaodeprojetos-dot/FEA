"""Estáticos de venda do MTB 11/26 (a venda é a Black Friday Vitalícia) sobre o modelo ADS 043 da Black BR
(logo Black Friday Vitalícia + foto do Dr. João + título + apoio + faixa dourada de chamada).

Apaga os textos do modelo com inpaint (OpenCV, sem IA generativa) e escreve a copy nova em Montserrat,
nas mesmas posições e cores. Palavras entre [colchetes] no apoio saem em dourado.
Fatos da oferta conferidos na página lp.joaopithon.com.br/black-friday/vitalicia/ em 28/10/2026.

Uso: python3 fea_criativos_venda_black.py PASTA_SAIDA [GRUPO ...]  (modelos em PASTA_SAIDA/modelo-story.png e modelo-feed.png)"""
import os, re, sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTE = "/tmp/claude-0/-home-user-FEA/ce2ef478-67a4-5284-b1d6-9d4c8f98649b/scratchpad/fontes/Montserrat.ttf"
DOURADO_TIT, DOURADO, BRANCO, ESCURO = (246, 215, 166), (229, 173, 106), (242, 240, 238), (24, 18, 8)

# caixas medidas no ADS 043 (x0, y0, x1, y1): título, apoio, faixa de chamada
LAYOUT = {
    "story": dict(tit=(89, 1047, 1002, 1175), apoio=(75, 1270, 990, 1400), cta=(79, 1554, 990, 1624),
                  tit_px=176, apoio_px=50, cta_px=31, larg_tit=930, larg_apoio=900, larg_cta=860),
    "feed": dict(tit=(82, 455, 740, 540), apoio=(79, 628, 470, 750), cta=(79, 901, 760, 972),
                 tit_px=118, apoio_px=34, cta_px=33, larg_tit=660, larg_apoio=430, larg_cta=860),
}

# (arquivo, título, apoio, chamada)
VENDAS = [
    ("Ads 101 - Acesso vitalício", "ACESSO VITALÍCIO",
     "A todos os meus cursos online atuais e a [todos os que eu ainda vou criar].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
    ("Ads 102 - Você viu a aula", "VOCÊ VIU A AULA.",
     "Agora tenha acesso vitalício à [Formação Especialista em Botox] e a todos os meus outros cursos.",
     "Toque em Saiba Mais e conheça a Black Friday Vitalícia."),
    ("Ads 103 - Um único valor", "UM ÚNICO VALOR",
     "Você nunca mais vai precisar comprar ou [renovar] nenhum curso online meu.",
     "Toque em Saiba Mais e conheça a Black Friday Vitalícia."),
    ("Ads 104 - 7 bônus", "7 BÔNUS INCLUSOS",
     "Pós-Graduação em Técnicas Injetáveis, Elite Injectors Congress 2027 e [mais 5 bônus].",
     "Toque em Saiba Mais e veja todos os bônus."),
    ("Ads 105 - Pós inclusa", "PÓS-GRADUAÇÃO INCLUSA",
     "A Pós-Graduação em Técnicas Injetáveis, [com certificação], vem como bônus na Black Friday Vitalícia.",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
    ("Ads 106 - Garantia", "GARANTIA DE 7 DIAS",
     "Entre, conheça os cursos por dentro e decida [com segurança].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
]
RMKT = [
    ("Ads 107 - Até 20-11", "ATÉ 20 DE NOVEMBRO",
     "Depois disso, o acesso vitalício a todos os meus cursos [não tem previsão de voltar].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
    ("Ads 108 - Dúvidas", "AINDA COM DÚVIDA?",
     "Fale com o meu time pelo WhatsApp e entenda a [condição para alunos e não alunos].",
     "Toque em Saiba Mais e fale com o meu time."),
    ("Ads 109 - Da toxina ao full face", "DA TOXINA AO FULL FACE",
     "Botox, preenchimento, bioestimuladores, anatomia e [todos os outros cursos] em um único acesso.",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
]

# fim da Black (20/11, conferir dia e horário de fechamento do carrinho antes de subir)
ULTIMO_DIA = [
    ("Ads 110 - Último dia", "ÚLTIMO DIA",
     "Hoje é o último dia da Black Friday Vitalícia: acesso vitalício a [todos os meus cursos online].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
    ("Ads 111 - Último dia com bônus", "ÚLTIMO DIA DA BLACK",
     "Hoje você ainda garante os [7 bônus], incluindo a Pós-Graduação em Técnicas Injetáveis.",
     "Toque em Saiba Mais e veja todos os bônus."),
    ("Ads 112 - Hoje é o último dia", "HOJE É O ÚLTIMO DIA",
     "Depois de hoje, a Black Friday Vitalícia [não tem previsão de voltar].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
]
ULTIMAS_HORAS = [
    ("Ads 113 - Últimas horas", "ÚLTIMAS HORAS",
     "A Black Friday Vitalícia termina hoje. Garanta [acesso vitalício] a todos os meus cursos online.",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
    ("Ads 114 - Termina hoje", "TERMINA HOJE",
     "Ainda dá tempo de entrar na Black Friday Vitalícia com [os 7 bônus inclusos].",
     "Toque em Saiba Mais e garanta seu acesso vitalício."),
]
GRUPOS = {"VENDAS": VENDAS, "RMKT VENDAS": RMKT, "ÚLTIMO DIA": ULTIMO_DIA, "ÚLTIMAS HORAS": ULTIMAS_HORAS}


def fonte(peso, px):
    f = ImageFont.truetype(FONTE, px)
    f.set_variation_by_name(peso)
    return f


def apagar(a, caixas_claras, caixa_cta):
    mask = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in caixas_claras:                  # texto claro sobre fundo escuro
        sub = a[y0 - 12:y1 + 12, x0 - 12:x1 + 12].max(axis=2)
        mask[y0 - 12:y1 + 12, x0 - 12:x1 + 12][sub > 70] = 255
    x0, y0, x1, y1 = caixa_cta                             # texto escuro sobre a faixa dourada
    sub = a[y0 - 8:y1 + 8, x0 - 6:x1].max(axis=2)
    mask[y0 - 8:y1 + 8, x0 - 6:x1][sub < 150] = 255
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    return cv2.inpaint(a, mask, 7, cv2.INPAINT_TELEA)


def quebrar(d, palavras, f, largura):
    linhas, atual = [], []
    for p in palavras:
        teste = " ".join(w for w, _ in atual + [p])
        if atual and d.textlength(teste, font=f) > largura:
            linhas.append(atual); atual = [p]
        else:
            atual.append(p)
    return linhas + ([atual] if atual else [])


def tokens(texto):
    """[trecho] vira dourado; devolve lista de (palavra, destaque)."""
    out = []
    for m in re.finditer(r"\[([^\]]+)\]|([^\[]+)", texto):
        parte, dest = m.group(1) or m.group(2), bool(m.group(1))
        for w in parte.split():
            if w[0] in ".,;:!?" and out:                    # pontuação nunca fica sozinha na linha
                out[-1] = (out[-1][0] + w, out[-1][1])
            else:
                out.append((w, dest))
    return out


def gerar(modelo, formato, titulo, apoio, cta, saida):
    L = LAYOUT[formato]
    a = np.asarray(Image.open(modelo).convert("RGB")).copy()
    a = apagar(a, [L["tit"], L["apoio"]], L["cta"])
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    # título: uma linha encolhendo até 62%; senão duas linhas equilibradas, encolhendo até caber
    px = L["tit_px"]
    f = fonte("ExtraBold", px)
    while d.textlength(titulo, font=f) > L["larg_tit"] and px > L["tit_px"] * 0.62:
        px -= 4; f = fonte("ExtraBold", px)
    linhas_tit = [titulo]
    if d.textlength(titulo, font=f) > L["larg_tit"]:
        ws = titulo.split()
        opcoes = [(" ".join(ws[:i]), " ".join(ws[i:])) for i in range(1, len(ws))]
        px = int(L["tit_px"] * 0.62); f = fonte("ExtraBold", px)
        linhas_tit = list(min(opcoes, key=lambda o: max(d.textlength(t, font=f) for t in o)))
        while max(d.textlength(t, font=f) for t in linhas_tit) > L["larg_tit"]:
            px -= 3; f = fonte("ExtraBold", px)
    x, y = L["tit"][0], L["tit"][1]
    topo = f.getbbox("H")[1]; alt = f.getbbox("H")[3] - topo
    for lin in linhas_tit:
        d.text((x, y - topo), lin, font=f, fill=DOURADO_TIT); y += int(alt * 1.32)
    # apoio: encolhe até terminar antes da faixa dourada
    y_ini = max(L["apoio"][1], y + int(L["apoio_px"] * 0.9))
    limite = L["cta"][1] - int(L["apoio_px"] * 1.4)
    tam = L["apoio_px"]
    while True:
        fa = fonte("SemiBold", tam); fb = fonte("Bold", tam)
        linhas_a = quebrar(d, tokens(apoio), fb, L["larg_apoio"])
        if y_ini + int(tam * 1.3) * len(linhas_a) <= limite or tam <= L["apoio_px"] * 0.7: break
        tam -= 2
    y = y_ini; topo_a = fa.getbbox("H")[1]
    for lin in linhas_a:
        cx = L["apoio"][0]
        for w, dest in lin:
            ff = fb if dest else fa
            if w[0] in ".,;:!?" and cx > L["apoio"][0]:      # pontuação colada na palavra anterior
                cx -= d.textlength(" ", font=ff)
            d.text((cx, y - topo_a), w, font=ff, fill=DOURADO if dest else BRANCO)
            cx += d.textlength(w + " ", font=ff)
        y += int(tam * 1.3)
    # chamada na faixa dourada
    fc = fonte("Bold", L["cta_px"])
    linhas_c = quebrar(d, [(w, 0) for w in cta.split()], fc, L["larg_cta"] if formato == "story" else 640)
    x0, y0, x1, y1 = L["cta"]
    passo = int(L["cta_px"] * 1.2); y = (y0 + y1) / 2 - passo * len(linhas_c) / 2
    topo_c = fc.getbbox("H")[1]
    for lin in linhas_c:
        d.text((x0, y - topo_c + 2), " ".join(w for w, _ in lin), font=fc, fill=ESCURO); y += passo
    im.save(saida)


if __name__ == "__main__":
    p = sys.argv[1]
    escolha = sys.argv[2:] or list(GRUPOS)            # opcional: só alguns grupos
    for pasta, pecas in ((g, GRUPOS[g]) for g in escolha):
        os.makedirs(f"{p}/{pasta}", exist_ok=True)
        for nome, tit, ap, cta in pecas:
            for formato in ("story", "feed"):
                rot = "Story" if formato == "story" else "Feed"
                gerar(f"{p}/modelo-{formato}.png", formato, tit, ap, cta,
                      f"{p}/{pasta}/{nome.split(' - ')[0]} {rot} - {nome.split(' - ', 1)[1]} - MTB Black.png")
                print("ok", pasta, nome, rot)
