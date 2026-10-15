# -*- coding: utf-8 -*-
"""Aplica no PDF espanhol os achados da revisao cega (relatorio-revision-es.md).

Onze trocas, em tres familias:

A. LINHA UNICA — a troca nao muda a largura de forma perceptivel (delta
   medido abaixo de 2,3 pt numa linha de 344 pt). A linha e reescrita com a
   mesma fonte, corpo e cor, rejustificada exatamente ate a margem direita
   original. Nada ao redor se move.

B. PARAGRAFO — a troca encurta a linha entre 27 e 56 pt, o que deixaria um
   vao visivel num paragrafo justificado. Ai o paragrafo inteiro e
   recomposto: as palavras sobem de linha e a quebra muda de lugar. O
   paragrafo nunca cresce; se a economia zerar a ultima linha, ele termina
   uma linha antes — o que acontece na pagina 52, onde a ultima linha tinha
   so 123 dos 344 pt e o bloco seguinte esta a 270 pt de distancia.

C. TRAVESSAO DA PAGINA 20 — a Helvetica Neue Bold embutida no PDF do cliente
   nao tem U+2014 (82 glifos, nenhum travessao), e trocar de fonte mudaria o
   tipo do titulo. A barra e desenhada a partir da barra do proprio hifen do
   arquivo: mesma altura, mesma espessura, largura de um em. O titulo sai em
   duas metades, com a barra entre elas.

O texto antigo sai por REDACAO, nao por mascara branca. Mascara esconde do
olho mas nao do extrator: quem copiasse a pagina receberia a linha velha e a
nova, uma atras da outra. Cada linha deste PDF e um operador de texto
proprio (o traduzir_pdf.py assentou uma por uma), e por isso a redacao
retira exatamente a linha visada sem levar a vizinha — o script confere isso
comparando a camada de texto antes e depois, pagina por pagina, e para se
sair mais linha do que o previsto. A redacao entra com `fill=None` e sem
tocar em imagem nem em traco, de modo que o fundo original permanece: branco
em dez pontos e o bege (239, 231, 219) do painel de abertura na pagina 20,
ambos amostrados pixel a pixel antes de comecar.

Uso:
    python3 correcciones_revision.py entrada.pdf saida.pdf
"""
import sys
import pymupdf

ENTRADA, SAIDA = sys.argv[1:3]

FONTES = {
    'R': 'fontes-completas/GuardianTextEgyp-Regular.otf',
    'B': 'fontes-completas/GuardianTextEgyp-Bold.otf',
    # o corte ES e o que tem o 'ó' de «código»: o arquivo base, extraido do
    # PDF portugues, nunca precisou dele em italico.
    'HI': 'fontes-completas/HelveticaNeue-ItalicES.ttf',
    'HB': 'fontes-completas/HelveticaNeue-Bold.ttf',
}
ALIAS = {'R': 'gteR', 'B': 'gteB', 'HI': 'hnI', 'HB': 'hnB'}

face = {k: pymupdf.Font(fontfile=v) for k, v in FONTES.items()}


# --------------------------------------------------------------------------
# A. trocas de linha unica
# --------------------------------------------------------------------------
LINHAS = [
    # [4] «metodología ARTI» com caixa oscilante: seis ocorrencias em
    #     maiuscula (p7, p8 x2, p9 x2 e p72) contra esta.
    dict(pag=6, y=413.68, x0=56.70, dir=400.43, tam=10.34, estilo='R',
         cor=0x000000, justificar=True,
         de='metodología ARTI —que contempla Anatomía, Reología, Técnica e',
         para='Metodología ARTI —que contempla Anatomía, Reología, Técnica e',
         nota='[4] caixa de «Metodología ARTI»'),

    # [1] falta a preposicao: «apunte el celular AL código QR». A frase
    #     equivalente da p6 ja esta certa, o que confirma o lapso isolado.
    #     Legenda alinhada a esquerda, sem justificacao.
    dict(pag=12, y=435.01, x0=315.00, dir=417.23, tam=8.0, estilo='HI',
         cor=0x000000, justificar=False,
         de='el código QR para descargar',
         para='al código QR para descargar',
         nota='[1] preposicao «al código QR»'),

    # [2] quinta forma do rebordo orbitario -> forma do glossario.
    dict(pag=21, y=474.92, x0=56.67, dir=400.42, tam=10.29977798461914,
         estilo='R', cor=0x000000, justificar=True,
         de='del borde inferior de la órbita, tiende a desplazarse con la edad,',
         para='del reborde orbitario inferior, tiende a desplazarse con la edad,',
         nota='[2] «reborde orbitario inferior» (p21)'),

    # [3] eixo anatomico: «craneal» emparelha com «caudal», nao com «distal»,
    #     que pertence ao eixo proximal/distal. O livro usa craneal/caudal
    #     corretamente nas paginas 12, 33 e 34.
    #     Ultima linha do paragrafo, sem justificacao.
    dict(pag=30, y=391.01, x0=56.69, dir=393.13, tam=10.34, estilo='R',
         cor=0x000000, justificar=False,
         de='craneal y la región malar, muchas veces ya atrófica, en sentido distal.',
         para='craneal y la región malar, muchas veces ya atrófica, en sentido caudal.',
         nota='[3] «en sentido caudal»'),

    # [Q1] a sigla contradizia o adjetivo: ORL e *Orbital* Retaining
    #      Ligament. E o livro ja escreve «ligamento retenedor orbitario
    #      (LRO)» nas paginas 12 e 49 — aqui tambem a sigla estava invertida.
    #      A pagina 6 fica como esta: e o artigo em ingles, onde ORL e a
    #      sigla correta.
    dict(pag=34, y=140.69, x0=56.70, dir=400.45, tam=11.0, estilo='R',
         cor=0x000000, justificar=True,
         de='orbicular (ORL). La gotera lagrimal es una estructura anatómica',
         para='orbitario (LRO). La gotera lagrimal es una estructura anatómica',
         nota='[Q1] «retenedor orbitario (LRO)»'),
    dict(pag=34, y=329.69, x0=56.70, dir=400.45, tam=11.0, estilo='R',
         cor=0x000000, justificar=True,
         de='(ORL), por encima de la unión entre la porción palpebral (craneal)',
         para='(LRO), por encima de la unión entre la porción palpebral (craneal)',
         nota='[Q1] sigla LRO (segunda ocorrencia)'),
]


# --------------------------------------------------------------------------
# B. paragrafos recompostos
# --------------------------------------------------------------------------
# linhas: (x de partida, margem direita, linha de base), lidas do PDF
# corridas: (texto, estilo)
PARAGRAFOS = [
    # [2] «borde superior del hueso orbitario» -> forma do glossario.
    dict(pag=17, tam=11.0, cor=0x000000,
         nota='[2] «reborde orbitario superior» (p17)',
         linhas=[(56.69, 400.46, 434.69), (56.69, 400.47, 455.69),
                 (56.69, 400.45, 476.69), (56.69, 400.48, 497.69),
                 (56.69, 400.43, 518.69), (56.69, 400.40, 539.69),
                 (56.69, 400.39, 560.69), (56.69, 400.40, 581.69)],
         corridas=[('El ', 'R'), ('músculo orbicular del ojo', 'B'),
                   (', que rodea toda la órbita, es el responsable del cierre '
                    'de los párpados y de las expresiones alrededor de los ojos '
                    'a través de su movimiento esfinteriano. Debemos entender el '
                    'orbicular como una lámina fina que se extiende desde la '
                    'inserción palpebral, pasando y haciendo contacto íntimo con '
                    'el reborde orbitario superior, y descendiendo hacia la '
                    'región malar, donde permanece entre dos estructuras grasas: '
                    'la SOOF y la grasa nasolabial superficial.', 'R')]),

    # [2] «reborde óseo de la órbita» -> forma do glossario.
    dict(pag=22, tam=11.0, cor=0x000000,
         nota='[2] «reborde orbitario» (p22)',
         linhas=[(70.90, 400.40, 518.70), (56.70, 400.46, 539.70),
                 (56.70, 400.44, 560.70), (56.70, 400.44, 581.70)],
         corridas=[('Por último, la ', 'R'),
                   ('grasa orbitaria profunda', 'B'),
                   (', que se sitúa más hacia el reborde orbitario, también '
                    'pierde volumen con el tiempo y, con el aumento de la '
                    'flacidez, se produce un prolapso de esta grasa que '
                    'evidencia las bolsas infraorbitarias.', 'R')]),

    # [2] «reborde óseo orbitario» -> forma do glossario, e
    # [5] «el soporte al ligamento LCC» dizia «ligamento ligamento»: LCC ja e
    #     ligamento cigomático-cutáneo.
    dict(pag=52, tam=11.0, cor=0x000000,
         nota='[2] e [5] «reborde orbitario» e «soporte al LCC»',
         linhas=[(56.69, 400.40, 77.69), (56.69, 400.39, 97.43),
                 (56.69, 400.37, 117.17), (56.69, 400.41, 136.91),
                 (56.69, 400.39, 156.65), (56.69, 400.38, 176.39),
                 (56.69, 400.38, 196.13)],
         corridas=[('3. Tercer pertuito:', 'B'),
                   (' este pertuito se posiciona en la ', 'R'),
                   ('cara lateral del reborde orbitario', 'B'),
                   (', una ubicación que permite alcanzar las capas más '
                    'profundas de la región infraorbitaria, incluido el ', 'R'),
                   ('soporte al LCC', 'B'),
                   ('. Al rellenar esta área conseguimos restaurar el volumen '
                    'de modo que se suavicen los surcos más profundos y se '
                    'corrija la pérdida de volumen que da origen a la formación '
                    'de las ojeras.', 'R')]),

    # [7] a unidade `20 mg/mL` quebrava entre a primeira e a segunda linha.
    #     Na recomposicao `mg/mL` e um token unico e por isso desce inteiro.
    #     A cifra pode ficar no fim da linha: o que nao se parte e a unidade.
    dict(pag=44, tam=11.0, cor=0xcf9f53,
         nota='[7] unidade `20 mg/mL` inteira na mesma linha',
         linhas=[(56.69, 321.93, 98.69), (56.69, 321.92, 119.69),
                 (56.69, 321.92, 140.69)],
         corridas=[('• Concentración de AH: aproximadamente 20 mg/mL '
                    '• G’ (módulo elástico): 411 • Tamaño de partícula: '
                    '> 1000 micrómetros', 'B')]),
]


# --------------------------------------------------------------------------
# C. o titulo com travessao desenhado
# --------------------------------------------------------------------------
# [6] `ANATOMÍA EN CADÁVER - REVISIÓN`: o alvo registrado no
#     anexo-1-texto-en-arte.md traz travessao, e as demais aberturas do livro
#     usam travessao.
TITULO_TRACO = dict(
    pag=20, y=218.31, x0=67.78, dir=264.73, tam=11.0, estilo='HB',
    cor=0xae7d2a,
    de='ANATOMÍA EN CADÁVER - REVISIÓN',
    antes='ANATOMÍA EN CADÁVER', depois='REVISIÓN',
    # as duas linhas do titulo estao no mesmo operador de texto, de modo que
    # a redacao leva as duas: a segunda e reescrita igual.
    segunda=('COMPLETA', 67.78, 129.71, 230.31),
    nota='[6] travessao na abertura do capitulo')


# --------------------------------------------------------------------------
def rgb(cor):
    return pymupdf.sRGB_to_pdf(cor)


def limpa(texto):
    """O espaco inquebravel serve so para manter `20 mg/mL` num unico token;
    no papel ele volta a ser espaco comum."""
    return texto.replace(' ', ' ')


def escreve(page, x, y, texto, estilo, tam, cor):
    page.insert_text(pymupdf.Point(x, y), limpa(texto), fontname=ALIAS[estilo],
                     fontfile=FONTES[estilo], fontsize=tam, color=rgb(cor))


def larg(palavra, estilo, tam):
    return face[estilo].text_length(limpa(palavra), tam)


def faixa(x0, x1, y, tam):
    """A faixa da linha: altura derivada do corpo, com folga de meio ponto."""
    return pymupdf.Rect(x0 - 0.6, y - tam * 0.92, x1 + 1.2, y + tam * 0.32)


def palavras(corridas):
    """Quebra as corridas em (palavra, estilo), preservando o estilo de cada
    palavra. O espaco que separa duas corridas nao pertence a nenhuma."""
    saida, pend, pend_est = [], '', None
    for texto, est in corridas:
        for ch in texto:
            if ch == ' ':
                if pend:
                    saida.append((pend, pend_est))
                    pend, pend_est = '', None
            else:
                if not pend:
                    pend_est = est
                pend += ch
    if pend:
        saida.append((pend, pend_est))
    return saida


def compoe(toks, linhas, tam):
    """Preenche as linhas com as palavras, guloso."""
    esp = {e: larg(' ', e, tam) for e in ALIAS}
    saida, i = [], 0
    for x0, dirx, _ in linhas:
        cabe = dirx - x0
        linha, usado = [], 0.0
        while i < len(toks):
            p, e = toks[i]
            w = larg(p, e, tam)
            add = w if not linha else esp[e] + w
            if linha and usado + add > cabe:
                break
            linha.append((p, e))
            usado += add
            i += 1
        saida.append(linha)
        if i >= len(toks):
            break
    if i < len(toks):
        raise SystemExit('ERRO: sobraram palavras — %r' % (toks[i:],))
    if len(saida) > len(linhas):
        raise SystemExit('ERRO: %d linhas compostas contra %d originais'
                         % (len(saida), len(linhas)))
    return saida


def justifica(page, linha, x0, dirx, y, tam, cor, ragged):
    """Desenha a linha. Se for justificada, distribui a sobra nos espacos."""
    if not linha:
        return
    lp = [larg(p, e, tam) for p, e in linha]
    espacos = len(linha) - 1
    if ragged or espacos == 0:
        vao = larg(' ', linha[0][1], tam)
    else:
        vao = (dirx - x0 - sum(lp)) / espacos
    x = x0
    for k, (p, e) in enumerate(linha):
        escreve(page, x, y, p, e, tam, cor)
        x += lp[k] + vao


def travessao(page, x, y, tam, estilo, cor):
    """Desenha um travessao com a barra do hifen da propria fonte e devolve o
    avanco. A Helvetica Neue embutida nao tem U+2014."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.boundsPen import BoundsPen
    t = TTFont(FONTES[estilo], fontNumber=0)
    gs = t.getGlyphSet()
    bp = BoundsPen(gs)
    gs[t.getBestCmap()[ord('-')]].draw(bp)
    _, ymin, _, ymax = bp.bounds
    upm = float(t['head'].unitsPerEm)
    esc = tam / upm
    barra = upm * 0.72          # a barra do travessao, nao o avanco do em
    page.draw_rect(pymupdf.Rect(x, y - ymax * esc, x + barra * esc,
                                y - ymin * esc),
                   color=None, fill=rgb(cor), width=0)
    return barra * esc      # so a barra: o respiro fica com quem chama


# --------------------------------------------------------------------------
doc = pymupdf.open(ENTRADA)
rel = []

# 1. o que cada pagina apaga e o que escreve no lugar
plano = {}

for it in LINHAS:
    pg = it['pag'] - 1
    if it['de'] not in doc[pg].get_text():
        raise SystemExit('ERRO: nao achei na p%d: %r' % (it['pag'], it['de']))
    plano.setdefault(pg, []).append(dict(
        tipo='texto', linhas=[(it['x0'], it['dir'], it['y'])],
        comp=[palavras([(it['para'], it['estilo'])])], tam=it['tam'],
        cor=it['cor'], ragged=not it['justificar'], paragrafo=False,
        nota=it['nota'], rotulo='linha  '))

for it in PARAGRAFOS:
    pg = it['pag'] - 1
    comp = compoe(palavras(it['corridas']), it['linhas'], it['tam'])
    plano.setdefault(pg, []).append(dict(
        tipo='texto', linhas=it['linhas'], comp=comp, tam=it['tam'],
        cor=it['cor'], ragged=False, paragrafo=True, nota=it['nota'],
        rotulo='%d linhas' % len(comp)))

tt = TITULO_TRACO
if tt['de'] not in doc[tt['pag'] - 1].get_text():
    raise SystemExit('ERRO: nao achei o titulo da p%d' % tt['pag'])
seg = tt['segunda']
plano.setdefault(tt['pag'] - 1, []).append(dict(
    tipo='titulo', linhas=[(tt['x0'], tt['dir'], tt['y']),
                           (seg[1], seg[2], seg[3])], dados=tt,
    tam=tt['tam'], nota=tt['nota'], rotulo='titulo '))

# 2. redacao: some com o texto antigo, preservando fundo, imagem e traco
antes = {}
for pg, itens in plano.items():
    page = doc[pg]
    antes[pg] = [l for l in page.get_text().split('\n') if l.strip()]
    for it in itens:
        for x0, dirx, y in it['linhas']:
            page.add_redact_annot(faixa(x0, dirx, y, it['tam']), fill=None)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

# 3. confere que a redacao nao levou vizinho
for pg, itens in plano.items():
    depois = [l for l in doc[pg].get_text().split('\n') if l.strip()]
    saiu = [l for l in antes[pg] if l not in depois]
    previsto = sum(len(it['linhas']) for it in itens)
    if len(saiu) > previsto:
        raise SystemExit('ERRO: a redacao na p%d levou %d linhas, previa no '
                         'maximo %d: %r' % (pg + 1, len(saiu), previsto, saiu))
    rel.append('p%-3d redacao  %d de %d linha(s) previstas'
               % (pg + 1, len(saiu), previsto))

# 4. escreve o texto novo
for pg, itens in plano.items():
    page = doc[pg]
    for it in itens:
        if it['tipo'] == 'titulo':
            d = it['dados']
            x = d['x0']
            escreve(page, x, d['y'], d['antes'], d['estilo'], d['tam'],
                    d['cor'])
            # um espaco de cada lado da barra, como nas outras aberturas
            x += larg(d['antes'] + ' ', d['estilo'], d['tam'])
            x += travessao(page, x, d['y'], d['tam'], d['estilo'], d['cor'])
            x += larg(' ', d['estilo'], d['tam'])
            escreve(page, x, d['y'], d['depois'], d['estilo'], d['tam'],
                    d['cor'])
            txt, sx, _, sy = d['segunda']
            escreve(page, sx, sy, txt, d['estilo'], d['tam'], d['cor'])
        else:
            for k, linha in enumerate(it['comp']):
                x0, dirx, y = it['linhas'][k]
                ragged = it['ragged'] or (
                    it['paragrafo'] and k == len(it['comp']) - 1)
                justifica(page, linha, x0, dirx, y, it['tam'], it['cor'],
                          ragged)
        rel.append('p%-3d %s  %s' % (pg + 1, it['rotulo'], it['nota']))

doc.save(SAIDA, garbage=3, deflate=True)
doc.close()

print('\n'.join(rel))
print('\n%d trocas aplicadas -> %s'
      % (len(LINHAS) + len(PARAGRAFOS) + 1, SAIDA))
