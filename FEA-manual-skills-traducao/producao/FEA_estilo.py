# -*- coding: utf-8 -*-
"""Identidade visual e composição dos PDFs desta pasta.

Identidade FEP Experience, aplicada pela regra da skill `identidades-visuais`:
material sem produto envolvido usa a identidade do evento, sem logo, só cores
e elementos de design. Os valores foram aferidos pixel a pixel no manual de
marca da pasta `3. ID FEP Experience` no Drive.

Capa preta, como o key visual do evento, e miolo claro, para o documento
continuar legível impresso e em leitor de PDF. O gradiente entra como filete
fino nas duas partes, que é o uso do próprio manual.

Três restrições do motor de composição do pymupdf que a folha de estilo
respeita, e que quebram o resultado se alguém mexer:

1. As corridas de uma linha são alinhadas pelo TOPO da caixa, não pela linha
   de base. Trocar de família no meio da frase desce a palavra. Negrito do
   mesmo desenho não desce, porque as métricas verticais são as mesmas, e por
   isso o negrito usado aqui é sempre do mesmo par de famílias. Monoespaçado
   só aparece em bloco inteiro (`pre.cmd`), nunca embutido numa frase.
2. Fundo de bloco é repintado em cada página por onde o fluxo passa, deixando
   faixas soltas. Por isso a capa é desenhada à mão e o miolo não usa fundo:
   hierarquia por cor, peso e filete.
3. O Story não numera página nem desenha fio: rodapé e filete entram depois,
   página a página, com o pymupdf comum.

As fontes de `fontes/` precisam ter passado pelo `FEA-ligaduras.py` antes,
senão o motor corrompe toda palavra com `fi` ou `fl`.
"""
import os

import pymupdf

PRODUCAO = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(PRODUCAO, 'fontes')

# ---- identidade FEP Experience, aferida no manual de marca -----------------
INDIGO = (0x47 / 255, 0x57 / 255, 0xFF / 255)
ROXO = (0xA6 / 255, 0x41 / 255, 0xFF / 255)
PRETO = (0x02 / 255, 0x02 / 255, 0x02 / 255)
CINZA = (0x96 / 255, 0x9F / 255, 0xA9 / 255)
BRANCO = (1, 1, 1)

LARG, ALT = 595, 842
MARGEM = 62

CSS = """
@font-face { font-family: titulo; src: url(ElMessiri-SemiBold.ttf); }
@font-face { font-family: titulo; font-weight: bold; src: url(ElMessiri-Bold.ttf); }
@font-face { font-family: corpo; src: url(Manrope-Regular.ttf); }
@font-face { font-family: corpo; font-weight: bold; src: url(Manrope-Bold.ttf); }
@font-face { font-family: mono; src: url(JetBrainsMono-Regular.ttf); }

* { font-family: corpo; }

h2 {
  font-family: titulo;
  font-size: 19px;
  color: #4757FF;
  margin: 26px 0 9px 0;
  line-height: 1.2;
}
h3 {
  font-size: 12px;
  color: #17172a;
  margin: 18px 0 5px 0;
}
p, li, td, th {
  font-size: 10.2px;
  line-height: 1.62;
  color: #2b2b3a;
}
p { margin: 0 0 11px 0; }
li { margin-bottom: 5px; }
ul, ol { margin: 0 0 11px 0; padding-left: 15px; }
b { color: #17172a; }

p.nota {
  border-left: 3px solid #A641FF;
  padding: 2px 0 2px 13px;
  margin: 14px 0 16px 0;
  color: #3a3a4d;
}
p.legenda { font-size: 9.2px; color: #6a6a7d; margin: 4px 0 14px 0; }

pre.cmd {
  font-family: mono;
  font-size: 9px;
  line-height: 1.55;
  color: #17172a;
  border-left: 3px solid #4757FF;
  padding: 3px 0 3px 13px;
  margin: 9px 0 13px 0;
}

table { width: 100%; border-collapse: collapse; margin: 10px 0 12px 0; }
th {
  font-size: 9px;
  color: #4757FF;
  text-align: left;
  padding: 0 11px 6px 0;
  border-bottom: 2px solid #A641FF;
}
td {
  padding: 8px 11px 8px 0;
  border-bottom: 1px solid #e3e3ec;
  vertical-align: top;
}
"""


def filete(page, x0, y, x1, espessura=3, passos=140):
    """O gradiente da marca como filete fino, em faixas de cor interpolada."""
    largura = (x1 - x0) / passos
    for i in range(passos):
        t = i / (passos - 1.0)
        cor = tuple(INDIGO[c] + (ROXO[c] - INDIGO[c]) * t for c in range(3))
        page.draw_rect(pymupdf.Rect(x0 + i * largura, y,
                                    x0 + (i + 1) * largura + 0.4, y + espessura),
                       color=None, fill=cor, width=0)


def _texto(page, x, y, txt, arq, tam, cor, espaco=0.0):
    """Escreve na capa. `espaco` abre entreletra, para os rótulos versais."""
    caminho = os.path.join(FONTES, arq)
    if espaco:
        face = pymupdf.Font(fontfile=caminho)
        for ch in txt:
            page.insert_text(pymupdf.Point(x, y), ch, fontname='f' + arq[:6],
                             fontfile=caminho, fontsize=tam, color=cor)
            x += face.text_length(ch, tam) + espaco
    else:
        page.insert_text(pymupdf.Point(x, y), txt, fontname='f' + arq[:6],
                         fontfile=caminho, fontsize=tam, color=cor)


def capa(doc, titulo, subtitulo, data, rotulo='DOCUMENTAÇÃO INTERNA'):
    """Capa preta, como o key visual do evento, desenhada à mão.

    `titulo` é uma lista de linhas, porque a quebra do título é decisão de
    composição e não pode ficar por conta do motor.
    """
    page = doc.new_page(width=LARG, height=ALT)
    page.draw_rect(pymupdf.Rect(0, 0, LARG, ALT), color=None, fill=PRETO, width=0)

    _texto(page, MARGEM, 214, rotulo, 'Manrope-SemiBold.ttf', 8.5, CINZA,
           espaco=2.6)
    filete(page, MARGEM, 236, MARGEM + 132, espessura=3)

    y = 322
    for linha in titulo:
        _texto(page, MARGEM, y, linha, 'ElMessiri-SemiBold.ttf', 40, BRANCO)
        y += 50

    y += 2
    for linha in subtitulo:
        _texto(page, MARGEM, y, linha, 'Manrope-Regular.ttf', 11.5,
               (0.72, 0.72, 0.79))
        y += 18

    filete(page, MARGEM, ALT - 138, LARG - MARGEM, espessura=2, passos=200)
    _texto(page, MARGEM, ALT - 112, 'FEA  ·  ' + data,
           'Manrope-SemiBold.ttf', 9.5, CINZA, espaco=1.0)


def _miolo(html, destino):
    """Compõe o corpo do documento num PDF separado, via Story."""
    story = pymupdf.Story(html=html, user_css=CSS,
                          archive=pymupdf.Archive(FONTES))
    escritor = pymupdf.DocumentWriter(destino)
    caixa = pymupdf.Rect(MARGEM, MARGEM + 14, LARG - MARGEM, ALT - MARGEM - 26)
    while True:
        dev = escritor.begin_page(pymupdf.Rect(0, 0, LARG, ALT))
        mais, _ = story.place(caixa)
        story.draw(dev)
        escritor.end_page()
        if not mais:
            break
    escritor.close()


def _acabamento(doc, rodape):
    """Filete no topo e rodapé numerado em cada página de miolo."""
    for i in range(1, len(doc)):
        page = doc[i]
        filete(page, MARGEM, MARGEM - 18, MARGEM + 46, espessura=2, passos=40)
        page.draw_line(pymupdf.Point(MARGEM, ALT - MARGEM + 4),
                       pymupdf.Point(LARG - MARGEM, ALT - MARGEM + 4),
                       color=(0.89, 0.89, 0.92), width=0.6)
        page.insert_text(
            pymupdf.Point(MARGEM, ALT - MARGEM + 20),
            '%s  ·  FEA  ·  %d de %d' % (rodape, i, len(doc) - 1),
            fontname='rod', fontfile=os.path.join(FONTES, 'Manrope-Regular.ttf'),
            fontsize=8, color=(0.52, 0.52, 0.58))


def montar(saida, titulo, subtitulo, data, html, rodape, metadados):
    """Capa, miolo e acabamento num único arquivo."""
    temporario = os.path.join(PRODUCAO, 'miolo-tmp.pdf')
    _miolo(html, temporario)

    doc = pymupdf.open()
    capa(doc, titulo, subtitulo, data)
    doc.insert_pdf(pymupdf.open(temporario))
    _acabamento(doc, rodape)
    doc.set_metadata(metadados)
    doc.save(saida, deflate=True, garbage=3)
    os.remove(temporario)
    print('paginas', len(doc), '->', saida)
    return len(doc)
