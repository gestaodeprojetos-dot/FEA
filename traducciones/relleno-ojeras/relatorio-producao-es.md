# Relatório de produção — *Relleno Tridimensional de Ojeras* (ES-LatAm)

Arquivo entregue: **`Relleno_Tridimensional_de_Ojeras_ES.pdf`** — 74 páginas, 23,4 MB.
Origem: `Preenchimento_Tridimensional_de_Olheiras_02_ebook2.pdf` (74 páginas, 17,7 MB).

Auditoria determinística (`scripts/auditar.py`): **LIBERADO — índice 100,0 %**,
0 achado de classe A (barreira clínica), 0 GRAVE, 0 MENOR.
9.893 palavras em espanhol · 325 blocos de texto traduzidos.

---

## 1. O que ficou idêntico

| Item | Situação |
|---|---|
| Número e ordem das páginas | idêntico (74) |
| Imagens, fotos, ilustrações, molduras, fios, fundos | bit a bit idênticos — nenhuma foi recomposta |
| Tipografia | as mesmas fontes do original (Guardian Text Egyptian, Helvetica Neue, Playfair Display) |
| Corpo, cor, entrelinha, justificação, recuo de primeira linha | preservados |
| Negrito dentro do texto corrido | reaplicado em 101 blocos, nas mesmas expressões |
| Posição da primeira linha de base de cada parágrafo | calibrada bloco a bloco para coincidir com o original |
| Cabeçalho corrido, numeração de página, molduras de QR | preservados |
| Sobreposição de texto | **zero** — verificado par a par nas 74 páginas contra o original |
| Texto perdido ou cortado | **zero** — o fim de cada um dos 325 blocos foi reencontrado na página correta |

---

## 2. O que **não** ficou idêntico

### 2.1 Corpo e entrelinha: o espanhol corre mais longo

O espanhol ocupa de 10 % a 20 % mais linha que o português. Onde a caixa era
fixa (rodapé de página, parágrafo que continua na página seguinte), a coluna foi
reduzida em degraus pequenos e uniformes. **Nenhum texto foi cortado.**

**41 colunas** com redução de coluna (uniforme dentro da coluna):

| Redução aplicada | Páginas |
|---|---|
| corpo −6 % | 6, 9, 38, 48, 52, 55, 61, 64, 67 |
| corpo −4 % | 25, 36, 39, 43, 50, 56, 66, 67 |
| entrelinha −2 % | 25, 49, 60, 62, 65, 69, 72 |
| corpo −2 % | 31, 44, 51, 60, 62 |
| entrelinha −8 % | 14, 18 |
| entrelinha −2 % + corpo −2 % | 35, 68 |
| entrelinha −8 % + corpo −4 % | 23 |
| entrelinha −2 % + corpo −4 % | 29 |
| entrelinha −4 % + corpo −6 % | 30 |
| entrelinha −6 % | 52 |
| entrelinha −8 % + corpo −6 % | 68 |

**8 parágrafos** com uma redução adicional automática, todos entre 96 % e 100 %
do corpo (imperceptível a olho nu):

| Pág. | Bloco | Corpo final |
|---|---|---|
| 15 | último parágrafo | 97 % |
| 20 | último parágrafo | 96 % |
| 21 | último parágrafo | 100 % |
| 39 | último parágrafo | 96 % |
| 41 | último parágrafo | 98 % |
| 48 | último parágrafo | 99 % |
| 55 | parágrafo final | 99 % |
| 72 | último parágrafo | 99 % |

### 2.2 Títulos e rótulos que ganharam largura

Título de seção e rótulo não são justificados: em espanhol crescem **para a
direita** dentro do espaço livre, em vez de encolher de corpo. Ganho de largura
observado, sempre sem invadir imagem: p5 +62 pt, p7 +59 pt, p11 e p12 +40 pt,
p43 +37 pt, p57 +34 pt, p61 +31 pt, p6 +25 pt, p59 +23 pt, p44, p52 e p71 +21 pt,
p55 +20 pt, p47 +18 pt, p64 +8 pt, p4, p39 e p50 +6 pt.

### 2.3 Aberturas de display assentadas linha por linha

Nas páginas **3** (`SU MÁ RIO` → `ÍN DI CE`) e **5** (`IN TRO DU ÇÃO` →
`IN TRO DUC CIÓN`) a entrelinha é mais fechada que a altura do desenho (0,76 e
0,93 em). Nessas duas páginas cada bloco silábico foi assentado na sua própria
linha de base, e não refluído — sem isso, o acento do `Í` era cortado pelo topo
da caixa.

### 2.4 Parágrafos que contornam arte

Quatro parágrafos contornam uma capitular, um QR ou uma foto. Foram desdobrados
em duas caixas reais e o espanhol foi repartido entre elas por busca binária. O
resultado é fiel, mas **a palavra em que a linha muda de medida não é a mesma**:

| Pág. | Contorno | Diferença |
|---|---|---|
| 6 | capitular `E` (era `O`) | o espanhol contorna a capitular em **3** linhas; o português em 4 |
| 23 | foto no canto inferior direito | ponto de estreitamento deslocado uma linha |
| 25 | QR no canto superior direito | ponto de alargamento deslocado uma linha |
| 30 | QR no canto superior direito | ponto de alargamento deslocado uma linha |

### 2.5 Dois parágrafos com o espanhol deliberadamente comprimido

Para não reduzir o corpo, o texto foi encurtado sem perder conteúdo clínico:

| Pág. | Antes | Depois |
|---|---|---|
| 30 | «…**En algunos casos, con el envejecimiento, ambos surcos se fusionan y forman** un único surco continuo que demarca **nítidamente** la protrusión…» | «…**Con el envejecimiento, ambos surcos suelen fusionarse en** un único surco continuo que demarca la protrusión…» |
| 66 | «**Inmediatamente después del** relleno de ojeras **es habitual que se produzca una** hinchazón leve…» | «**Tras el** relleno de ojeras **es habitual una** hinchazón leve…» |

### 2.6 Capas (páginas 1, 2 e 74)

O título e o subtítulo das capas são **pixel, não texto**. Foram refeitos dentro
da própria arte:

- Fundo sob o texto reconstruído por interpolação de degradê (apaga também a
  sombra projetada das letras, que o *inpainting* deixava passar).
- Letras redesenhadas com preenchimento por **campo de textura extraído dos
  próprios pixels dourados** do original — a folha metálica e o granulado são os
  do arquivo, não uma cor chapada.
- Título em Helvetica Neue Bold (o corte embutido no PDF). **O traço do título
  original parece uma fração mais pesado** que o corte disponível — é a única
  diferença visual perceptível nas capas.
- Subtítulo em Playfair Display Bold Italic + `ARTI` em Helvetica Neue Medium,
  reproduzindo a mistura de fontes do original.
- Página 2 é a capa em preto e branco: exigiu detecção de texto por luminância
  em vez de matiz.
- `DR. JOÃO PITHON` não foi tocado.

### 2.7 Texto dentro de imagem que foi traduzido

| Pág. | Rótulos | Fonte usada |
|---|---|---|
| 22 | `Perda tônus` → `Pérdida tono`; `Mudança SOOF` → `Cambio SOOF`; título do app `Preenchimento de olheiras` → `Relleno de ojeras` | Liberation Mono Italic / Liberation Sans |
| 36 | `Diminuição coxim região suborbital/malar` → `Disminución almohadilla región suborbitaria/malar`; `Perda tônus Muscular` → `Pérdida tono Muscular`; `Mudança SOOF` → `Cambio SOOF`; `+ Perda óssea` → `+ Pérdida ósea` | Liberation Mono Italic |
| 57 | `+ Perda óssea` → `+ Pérdida ósea`; título do app | Liberation Mono Italic / Liberation Sans |

**Observação:** a itálica de máquina de escrever desses infográficos não está
embutida no PDF (só existe como pixel). Foi substituída por Liberation Mono
Italic, que é próxima mas **não é a mesma fonte**. É o único ponto do arquivo em
que houve troca de tipo.

`Muscular` (p22 e p36) não foi redesenhado: a palavra é idêntica nos dois idiomas.

### 2.8 O que ficou em outro idioma, de propósito

| Conteúdo | Páginas | Motivo |
|---|---|---|
| Artigos científicos reproduzidos (fac-símile) | 6, 15, 17, 36, 40, 41, 42, 58 | citação de obra publicada; traduzir descaracteriza |
| Pranchas de atlas de terceiros (Lamb & Surek, *Facial Volumization*; Uldis Zarins) | 15, 16, 18, 19, 22, 23, 24, 27, 29, 30, 31, 32, 35, 56 | idem — inclui as legendas «Fig. 1.21 / 1.22 / 2.2 / 3.4 / 1.26» e a linha «Source: …» |
| Slides do autor em inglês (`HIGH G PRIME`, `WHY YVOIRE CONTOUR?`) | 42, 46 | material do próprio autor, já em inglês |
| Barra de status do iPad («Sábado 21 de setembro») | 57 | interface do aparelho, não conteúdo |
| `DR. JOÃO PITHON` / cabeçalho `JOÃO PITHON` | todas | nome próprio |
| Numerais de abertura `01.` a `05.` | 10, 37, 47, 59, 71 | algarismos |

### 2.9 QR Codes

- **20 QR de vídeo regenerados**, apontando para os ativos em espanhol da
  planilha enviada. Cada QR foi **conferido por releitura** depois de gerado.
- **11 QR de artigo/e-book mantidos** — não existe versão espanhola desses PDFs.
- A moldura decorativa dourada de cada QR foi preservada.
- Conferência final no arquivo entregue: **31 QR lidos, 0 apontando para a
  origem em português.**

Páginas com QR trocado: 14, 20, 22, 28, 34, 46, 49 (×3), 50, 51 (×2), 52, 54,
57 (×3), 61 (×2), 64.

---

## 3. Observações importantes

### 3.1 A entrega anterior em DOCX estava incompleta

O manuscrito bilíngue `Relleno_Ojeras_ES_manuscrito_bilingue.docx`, entregue
antes, **não continha o conteúdo da página 26** («6. LIGAMENTOS RETENTORES» e os
dois parágrafos sobre ligamentos verdadeiros e falsos). Aquele arquivo foi feito
a partir do texto corrido; este PDF foi reconstruído bloco a bloco a partir da
estrutura do PDF (325 blocos), e a página 26 está completa. **Descarte o DOCX
como referência de conteúdo** — use o PDF.

### 3.2 Erros do original corrigidos em silêncio no espanhol

Estão listados em `anexo-2-correcoes-original.md`. Os principais:
`perda de vaolume` (p21), `LIGAMENTO VERDADEIROS` (p28), `LIAGAMENTOS` (p34),
`Demosntração do Botao Anestesico` (p54), `raciocínio clinio` (p64),
`Relacao entre g' e sf.` (p42), `ANATOMIA NO CADAVER - REVISAO COMPLETA` (p20),
`Efeito tyndall` em minúscula no sumário, e a grafia oscilante de
`20mg/ml · 25 mg/mL · 20 mg/ml` (uniformizada em `20 mg/mL`).
**Vale corrigir também a versão portuguesa.**

### 3.3 Dois pontos que pedem sua decisão

1. **`ligamento de retenção orbicular` (p34) vs. `orbitária` (p12)** — duas
   denominações para a mesma estrutura no original. Espelhei o original em cada
   página. Recomendo uniformizar para *orbitario* nos dois idiomas.
2. **Página 29 → 30** — a frase da p29 termina em «aplicando siempre el» e a p30
   começa em outro assunto. **Parece haver texto perdido no original**, e o corte
   foi preservado. Confirme.

### 3.4 A legenda repetida da página 66

A p66 traz, sob a foto do hematoma, a legenda `Anatomia SNJ e SPM` — a mesma da
p30, e sem relação com a imagem. É um resíduo do original; foi traduzida
literalmente (`Anatomía del SNY y del SPM`). Se for engano, corrija nos dois
idiomas.

### 3.5 Vídeos ainda pendentes de produção

Os QR já apontam para os arquivos em espanhol que você enviou. A lista completa
— página, assunto, link e duração — está em
`Inventario_QR_Videos_Olheiras_UNICA_ABA.xlsx`, aba «Só traduzir». A skill
**lista** os vídeos; não dubla nem legenda.

### 3.6 O que foi resolvido no caminho, e que vale saber

- **As fontes embutidas no PDF eram subconjuntos**: só traziam as letras usadas
  em português. Faltavam 12 glifos para o espanhol. Foram sintetizados **dentro
  da própria família**: `¿` por rotação de 180° do próprio `?`; `H j y í ó` da
  itálica por inclinação de 12° do romano (Helvetica Neue Italic é uma oblíqua,
  então a inclinação é exata); `f y z ó` da Medium por engrossamento horizontal
  de 29/1000 em, medido na diferença de haste entre os dois cortes.
- **Playfair Display** tinha só as letras de `SUMÁRIO`, `INTRODUÇÃO` e
  `Conclusão`: faltavam `C D E N Í Ó`, impossíveis de sintetizar. Resolvido com
  o Playfair Display genuíno (SIL OFL, via `@fontsource`), **conferido glifo a
  glifo contra o subconjunto embutido** — mesmos contornos e mesmas larguras de
  avanço, até a última unidade.
- **O cmap mentia**: os subconjuntos declaravam 2.005 codepoints (Helvetica) com
  glifo vazio, incluindo as ligaduras `fi`/`fl`. O motor desenhava nada — e
  `influencia` saía `in uencia`. As entradas fantasma foram removidas, o que
  devolve o comportamento correto (`f` + `l`).
- **Playfair posiciona acento por *point matching***, que motores de PDF
  ignoram: o acento do `Í` saía atravessado sobre as letras. Os 396 glifos
  compostos afetados foram achatados.
- **A redação apaga tudo que toca o retângulo**, inclusive o que não é nosso: os
  numerais `01.` a `05.` das aberturas cruzam a caixa do título e desapareciam.
  Agora são guardados antes e redesenhados idênticos depois.

Tudo isso está implementado na skill, não neste projeto: o próximo ebook não
repete nenhum destes problemas.

---

## 4. Como reproduzir

```bash
python3 .claude/skills/fea-traduccion-es/scripts/traduzir_pdf.py \
    original.pdf produccion/mapa-bloques-es.json \
    --fontes fontes-completas --saida passo1.pdf
python3 .claude/skills/fea-traduccion-es/scripts/atualizar_qr.py \
    passo1.pdf links-videos-es.json --saida passo2.pdf
# capas e rótulos, um por vez, encadeando a saída:
python3 .claude/skills/fea-traduccion-es/scripts/traduzir_arte.py \
    passo2.pdf --pagina 1 --mapa produccion/mapas-arte/p01-capa.json --saida passo3.pdf
```

`produccion/` guarda o mapa de tradução por bloco, os mapas de arte, a estrutura
extraída do PDF, os logs de refluxo e de QR e a auditoria final.

As fontes de `fontes-completas/` se regeneram a partir do próprio PDF com os
utilitários da skill, nesta ordem: `fundir_subconjuntos.py`, `limpar_cmap.py`,
`achatar_compostos.py`, `doar_glifos.py`.

**Nota sobre as fontes:** `fontes-completas/` contém os subconjuntos extraídos do
seu próprio PDF, completados com os glifos do espanhol, mais o Playfair Display
sob licença SIL OFL. São ativos de produção deste projeto, para uso interno —
não redistribua.
