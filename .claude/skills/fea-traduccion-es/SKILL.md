---
name: fea-traduccion-es
description: Traduz conteúdo FEA de medicina e estética avançada de português para espanhol latino-americano com terminologia clínica travada por glossário. Use para traduzir ou revisar qualquer material do catálogo — ebook, apostila, aula, transcrição de vídeo, slide, roteiro, legenda, e-mail, página de vendas, post — sobre preenchimento com ácido hialurônico, toxina botulínica, bioestimuladores de colágeno, fios de sustentação, skinboosters, peelings, anatomia facial, harmonização facial, complicações vasculares, hialuronidase ou protocolos de injetáveis. Também use quando o usuário pedir para padronizar, auditar ou expandir a terminologia espanhola desse material.
---

# Tradução FEA: português → espanhol latino-americano

Este material é lido por injetores que vão reproduzir a técnica em pacientes.
Um termo anatômico trocado, uma unidade mal convertida ou uma dose ambígua não
é erro de estilo — é risco clínico e perda de autoridade diante de um público
que reconhece terminologia. O processo abaixo existe para que nenhum termo
técnico seja decidido no improviso.

## Carregue os glossários antes de traduzir

**Dois arquivos são obrigatórios em toda tradução, sem exceção:**

- `references/00-nucleo.md` — a terminologia que vale para todo o catálogo.
- `references/01-voz-y-estilo.md` — o que separa espanhol correto de espanhol
  que soa nativo. O glossário garante o termo; este garante o texto. Um material
  pode ter todos os termos certos e ainda denunciar português na sintaxe, na
  pontuação e nos conectores — e o leitor injetor percebe em três parágrafos.

Depois carregue o módulo do tema tratado:

| Módulo | Cobre | Base |
|---|---|---|
| `00-nucleo.md` | Anatomia facial, planos e camadas, produtos e ativos, técnica e instrumental, avaliação e registro clínico, linguagem didática e comercial, convenções de formato | 2 ebooks + 684 títulos de aula |
| `11-rellenos-ah-ojeras.md` | Ácido hialurônico, reologia (G', SF), região infraorbital, ligamentos retentores, pertuitos, efeito Tyndall | ebook de olheiras |
| `15-intercurrencias.md` | 30 intercorrências, farmacologia de emergência, doses e vias, protocolos PDRR e PithonNapoli | ebook de intercorrências |
| `12-toxina-botulinica.md` | Toxina, unidades, diluição, músculos da mímica, ptose | ⏳ 8 módulos no catálogo, material pendente |
| `13-bioestimuladores.md` | PLLA, CaHA, PDRN, skinboosters, neocolagênese | ⏳ 3 módulos no catálogo, material pendente |
| `14-hilos.md` | Fios de colágeno e de tração, vetores, previsibilidade | ⏳ 9 módulos no catálogo, material pendente |
| `16-corporales.md` | Glúteo, mama, membros, celulite, estrias | ⏳ 4 módulos no catálogo, material pendente |
| `17-tecnologias.md` | Laser, ultrassom, radiofrequência | ⏳ 2 módulos no catálogo, material pendente |
| `18-dermatologia.md` | Peelings, skincare, tricologia, intradermoterapia | ⏳ 4 módulos no catálogo, material pendente |
| `19-gestion.md` | Gestão de clínicas, marketing, vendas, precificação | ⏳ 7 módulos no catálogo, material pendente |
| `90-decisiones.md` | Registro de decisões terminológicas e pendências do autor | vivo |
| `91-catalogo-aulas.txt` | Mapa das 684 aulas em 62 módulos, para dimensionar escopo | planilha de produção |

Se o tema não tem módulo, traduza com o núcleo, **registre os termos novos** e
crie o módulo ao final. Um glossário que não cresce a cada trabalho é um
glossário que vai sendo abandonado.

## Passagem 0 — Curadoria do material (antes de traduzir uma única palavra)

**Nada é traduzido antes desta passagem.** Traduzir primeiro e inventariar depois
produz retrabalho garantido: o texto sai pronto, e só então se descobre que
metade do material não é texto — é arte, vídeo e QR Code apontando para conteúdo
em português.

O objetivo é responder, antes de começar: **o que exatamente existe neste
material, e o que de tudo isso precisa de versão em espanhol?**

### 0.1 — Levantar as quatro camadas do material

Um material FEA tem quatro camadas, e três delas são invisíveis à extração
normal de texto.

| Camada | Como levantar | Se pular |
|---|---|---|
| **1. Texto corrido** | extração normal (pymupdf, python-docx) | — |
| **2. Texto embutido em arte** | **OCR de todas as páginas** + diff contra a camada de texto | O designer descobre o que falta durante a diagramação |
| **3. Vídeos e QR Codes** | `scripts/inventario_midia.py` — decodifica os QR | O aluno lê em espanhol e assiste em português |
| **4. Artigos e citações** | classificar cada destino pelo mimeType real | Traduz-se citação que deveria ficar em inglês |

```
python3 scripts/inventario_midia.py material.pdf
tesseract pagina.png stdout -l por+eng --psm 3     # camada 2, página a página
```

Medida no ebook de olheiras: a camada 2 tinha **194 linhas em 29 páginas** que a
extração normal não via — inclusive o título da capa. A camada 3 tinha **32 QR
Codes**, e o PDF não tinha **nenhuma** anotação de link: todo destino existia só
dentro da imagem do QR.

### 0.2 — Classificar cada item: traduz, não traduz, ou decide o autor

Esta é a curadoria propriamente dita. Todo item levantado recebe **uma** destas
marcas:

- **TRADUZ** — texto corrido, rótulo em português na arte, vídeo do autor.
- **NÃO TRADUZ** — citação bibliográfica, abstract, prancha de atlas de
  terceiros, marca, princípio ativo, artigo científico linkado.
- **DECIDE O AUTOR** — rótulo em inglês dentro de arte de terceiros; slide do
  próprio autor que está em inglês no material português; destino de QR que
  aponta para material em outro idioma.

Item sem marca é item que vai dar problema depois. Não deixe nenhum.

### 0.3 — Entregar o mapa do material antes de traduzir

Produza e **mostre ao autor** antes de começar:

1. **Contagem por camada** — palavras de texto corrido, linhas em arte, QR por
   tipo de destino.
2. **Inventário de mídia** — a tabela completa (ver 0.4).
3. **Lista de decisões pendentes** — tudo que caiu em DECIDE O AUTOR.
4. **Estimativa do que não é tradução de texto** — quantos vídeos precisam de
   versão em espanhol; quantos QR precisam ser regerados; quantos rótulos de arte
   precisam ser reaplicados pelo designer.

> **Fronteira do escopo.** A skill **lista** os vídeos, com página, rótulo,
> assunto e link, para que sejam localizados depois. Ela **não** produz, não
> legenda, não dubla e não recomenda método de produção — isso é decisão e
> execução da FEA.

O ponto 4 é o que evita a surpresa de orçamento. Traduzir 8.000 palavras é
barato; produzir 18 vídeos em espanhol não é. O autor precisa saber disso
**antes**, não depois de aprovar a tradução.

### 0.4 — A tabela de inventário de mídia

Para cada ativo, registre:

| Campo | Por quê |
|---|---|
| **Página** do PDF | Para localizar o QR na arte |
| **Rótulo PT** e **rótulo ES** | Para o designer saber qual botão é qual |
| **Assunto** | Para achar o ativo depois sem abrir o vídeo |
| **Arquivo de origem** | Nome real no Drive, não o rótulo do botão |
| **Link atual** | Destino de hoje |
| **Link ES** | Em branco, a preencher quando o ativo ES existir |
| **Marcador de tempo** | Se havia `?t=`, **recalcular** — corte diferente move o trecho |
| **Status** | pendente / em produção / pronto |

Três regras que evitam erro de planejamento:

1. **Ativos únicos ≠ QR a regerar.** Um mesmo vídeo pode ser chamado de várias
   páginas. No ebook de olheiras: 19 ativos a produzir, 22 QR a regerar.
2. **QR de artigo científico não se toca.** Citação permanece em inglês, link
   permanece igual.
3. **O QR é imagem.** Trocar o link não muda o QR — a imagem tem de ser regerada
   e substituída na arte, e conferida por escaneamento real antes de fechar.

Se o material não for PDF (slide, página, aula), levante os links pelo formato
de origem, mas produza a **mesma tabela**: sem ela o vídeo em português passa.


### 0.5 — Só então comece a traduzir

Com o mapa aprovado, siga para as três passagens. Se durante a tradução aparecer
item novo que a curadoria não pegou, **volte e atualize o mapa** — não resolva de
improviso, porque a revisão vai cobrar o inventário completo.

## As três passagens de tradução

Só começam depois da Passagem 0. Não pule nenhuma — cada uma pega uma classe
de erro diferente.

### Passagem 1 — Tradução
Traduza por blocos de sentido, não linha a linha. PDFs exportados de InDesign
quebram palavras com hífen no fim da linha ("reconhe-cido", "Swell-ing"): junte
antes de traduzir, ou o resultado sai com palavras partidas.

Mantenha:
- a estrutura de títulos e a numeração das seções;
- **acrônimos de autor recalculados sem quebrar a sigla** — a metodologia ARTI
  só sobrevive em espanhol porque "Intercorrências" vira "Intercurrencias", não
  "Complicaciones". Sempre verifique se a sigla fecha no idioma-alvo;
- o registro: técnico, dirigido a profissional, tratamento formal (usted).

### Passagem 2 — Auditoria mecânica (script, não olho)

```
python3 scripts/auditar.py texto_es.txt
```

Cobre resíduo de português, lusismo sintático, falso amigo clínico, posologia,
via de administração, ortotipografia e tratamento. Exit code 1 = há
BLOQUEANTE; não entregue nesse estado.

Depois do script, varra à mão o que ele não modela: cada entrada dos módulos
carregados, grafia exata de marca, e coerência do mesmo termo ao longo de todo
o material — inconsistência interna é o achado mais frequente e o mais danoso,
porque o aluno vê dois nomes para a mesma estrutura.

Falso positivo do script não se ignora: ajuste a regra. Um auditor que cria
ruído deixa de ser lido.

### Passagem 3 — Back-translation dos trechos técnicos
Retraduza para português **apenas** as passagens com carga técnica — doses,
diluições, anatomia, valores reológicos, passo a passo, manejo de complicações —
e compare com o original. Divergência de sentido aqui é erro real, não estilo.
É esta passagem que pega o erro silencioso: o número certo na estrutura errada,
o ligamento trocado, a camada invertida, o plano de injeção deslocado.

## Regras que valem para todo o catálogo

- **Não traduza citação bibliográfica.** Abstracts, títulos de revista, autores,
  filiações, DOI e capas de artigo reproduzidos no material ficam em inglês.
- **Não traduza marca nem denominação de princípio ativo.** Grafia exata, com ®
  onde o original traz.
- **Texto embutido em arte exige OCR, não inspeção.** Rótulos dentro de JPG/PNG
  não têm camada de texto e **não aparecem na extração normal** — a camada de
  texto do PDF mente por omissão. Rode OCR em todas as páginas e faça diff
  contra a camada de texto para isolar o que só existe como imagem:

  ```
  tesseract pagina.png stdout -l por+eng --psm 3
  ```

  No ebook de olheiras essa passagem encontrou 194 linhas em 29 páginas que a
  extração normal não via — incluindo o título na capa. Sem OCR, o inventário
  de arte sai incompleto e o designer descobre o que falta na diagramação.

  Classifique o achado em três categorias, porque o tratamento difere:
  **(A)** português na arte → traduzir; **(B)** prancha de atlas de terceiros em
  inglês → manter e legendar por fora; **(C)** slide do próprio autor em inglês
  → decisão do autor.
- **Erros de digitação do original** são corrigidos em silêncio no espanhol e
  listados à parte para o autor. Nunca replique o erro por fidelidade.
- **Nunca invente dose, unidade ou nome de produto** que não esteja no original.
  Se o original é ambíguo, traduza mantendo a ambiguidade e sinalize ao autor.

## Produção do PDF final — sem designer

O material sai traduzido no próprio arquivo, com imagens, posição, fonte, corpo,
cor e entrelinha preservados. Três scripts, nesta ordem:

### 1. Completar as fontes

```
python3 scripts/fundir_subconjuntos.py material.pdf --saida fontes/   # 1º: fundir
python3 scripts/completar_fonte.py     material.pdf --saida fontes/   # CFF/Type1
python3 scripts/completar_fonte_ttf.py fontes/ --precisa 'éíúóáñÑ¿—’' # TrueType
python3 scripts/limpar_cmap.py  fontes/    # remove entradas de glifo vazio
python3 scripts/achatar_compostos.py fontes/  # acentos por point-matching
# ultimo recurso, antes de trocar de tipo: doar de outro corte da familia
python3 scripts/doar_glifos.py fontes/HelveticaNeue.ttf fontes/HelveticaNeue-Italic.ttf \
    --chars 'Hjyíó' --inclinar 12 --saida fontes/HelveticaNeue-ItalicES.ttf
python3 scripts/doar_glifos.py fontes/HelveticaNeue-Bold.ttf fontes/HelveticaNeue-Bold.ttf \
    --girar '¿:?,¡:!' --saida fontes/HelveticaNeue-BoldES.ttf
```

**A mesma família aparece em vários subconjuntos.** Um PDF de 74 páginas trazia
6 subconjuntos de Helvetica Neue, cada um com as letras de um punhado de páginas.
Extrair um só dá uma fonte com 38 glifos; fundir os 6 dá 73. Funda **antes** de
medir cobertura. Subconjunto Type0/Identity-H não tem cmap: o mapa
caractere → glifo vem do `ToUnicode` do próprio PDF (parseie `beginbfchar` e
`beginbfrange` **em blocos separados** — um regex único casa através das linhas e
importa lixo).

PDFs de InDesign embutem apenas o **subconjunto** de glifos do idioma original.
Um subconjunto português não tem `ñ ¿ ¡ « » —`. Os scripts montam os que faltam
a partir dos que a fonte já tem — til de `ã`, acento de `ó`, `¿` girando o `?` —
em vez de trocar a fonte e alterar a tipografia do material inteiro.

⚠️ **O cmap mente.** Nos subconjuntos, glifos como `ñ` e `¿` continuam listados
no cmap com contorno **vazio**. Medir cobertura pelo cmap dá falso positivo: a
medida válida é «o glifo tem contorno?». Foi assim que um `¿` sumiu de um título
que a checagem por cmap dava como coberto.

Pior: o motor de HTML do pymupdf **substitui `fi`/`fl` por ligadura** por conta
própria. Se o cmap declara `U+FB01`/`U+FB02` com contorno vazio — e declara —,
`influencia` sai `in uencia`. `limpar_cmap.py` apaga as entradas fantasma, e o
motor volta a compor `f`+`l`.

⚠️ **Acento por *point matching*.** Alguns tipos (Playfair Display) posicionam o
acento do glifo composto por índice de ponto, não por deslocamento x/y. Motores
de PDF ignoram e o acento sai atravessado sobre a letra. `achatar_compostos.py`
decompõe esses glifos — o desenho não muda, a posição passa a ser absoluta.

⚠️ **Quando não há como sintetizar.** Playfair Display só trazia as letras de
`SUMÁRIO` e `INTRODUÇÃO`; `ÍNDICE` precisa de `C D E N`, que não existem em
lugar nenhum do arquivo e não se derivam de nada. Aí a saída é o tipo **genuíno**
(Playfair Display é SIL OFL, disponível via `npm pack @fontsource/<familia>`, que
o proxy libera) — e a obrigação é **conferir glifo a glifo contra o subconjunto
embutido**: contorno e largura de avanço têm de coincidir unidade por unidade.
Se não coincidirem, não é o mesmo tipo, e trocar mudaria a tipografia do material.

### 2. Substituir o texto

```
python3 scripts/traduzir_pdf.py material.pdf --estrutura > estrutura.json
# preencher o mapa id → texto ES, com <b> onde o original tem negrito
python3 scripts/traduzir_pdf.py material.pdf mapa.json --fontes fontes/ --saida es.pdf
```

O PDF exporta **uma linha por bloco**; o script reagrupa em parágrafos pela
**margem esquerda** — a última linha de um parágrafo justificado é curta, então
agrupar pela margem direita quebraria o parágrafo ali. Depois remove o original
por redação (imagens preservadas) e refluí o espanhol.

O que o script resolve, e que o refluxo ingênuo erra:

- **Coluna, não parágrafo isolado.** O espanhol corre 10 % a 20 % mais longo.
  Parágrafos que correm juntos são compostos como uma **coluna**: a primeira
  linha de base fica onde estava, os respiros entre parágrafos são os do
  original, e a coluna cresce **para baixo** até o próximo obstáculo — parágrafo,
  imagem ou fio desenhado. Sem isso o texto encolhe onde havia espaço livre.
- **Linha de base calibrada.** O htmlbox posiciona a primeira linha em função da
  entrelinha; com entrelinha fechada ela sobe vários pontos. O script compõe num
  rascunho, mede onde a linha caiu e desloca a caixa para que coincida com a do
  original.
- **Título cresce para a direita, corpo não.** Título, rótulo e parágrafo de uma
  só linha ganham largura até o próximo obstáculo, em vez de encolher de corpo.
  Parágrafo justificado de várias linhas mantém a largura da coluna.
- **Contorno de arte.** Parágrafo que contorna capitular, QR ou foto tem linhas
  com medida diferente do corpo. O script detecta essas linhas (medida **igual
  entre si** e ≥ 20 pt diferente do resto — linha só curta é ragged, não
  contorno), desdobra em caixas reais e reparte o espanhol entre elas por busca
  binária, com o `<b>` fechado e reaberto no corte.
- **Display de entrelinha fechada.** Quando a entrelinha é menor que a altura do
  desenho (`SU MÁ RIO`, 0,76 em), a caixa corta o acento da primeira linha. Esses
  títulos são assentados **linha por linha** na linha de base de cada uma.
- **O que não é nosso é preservado.** A redação apaga todo texto que toca o
  retângulo. Numerais de abertura (`03.`) cruzam a caixa do título e
  desapareciam. Agora são guardados antes e redesenhados idênticos depois.

Se ainda não couber, reduz entrelinha até 8 % e corpo até 6 %, **uniformemente na
coluna**, e registra. Só então deixa o htmlbox reduzir aquele parágrafo, e
registra quanto. **Texto cortado nunca**: no fim, confira que o final de cada
bloco reaparece na página certa.

### 3. Traduzir o texto que está dentro das imagens

```
python3 scripts/traduzir_arte.py material.pdf --pagina 1 --detectar
python3 scripts/traduzir_arte.py material.pdf --pagina 1 --mapa capa.json --saida capa_es.pdf
```

Detecta os pixels do texto por cor, delimita as faixas por perfil de linha (para
nunca tocar moldura ou fotografia), reconstrói o fundo e redesenha em espanhol.
Para o acabamento de folha metálica, preenche as letras com um **campo de
textura** extraído dos próprios pixels dourados do original — cor chapada
denunciaria o retoque.

Três variantes, escolhidas pelo mapa:

- `"modo": "luz"` — texto claro sobre fundo escuro sem matiz (a capa em P&B).
  A máscara por matiz não pega.
- `"fundo": "gradiente"` — reconstrói a faixa por interpolação entre as linhas de
  cima e de baixo. Use sempre que o texto tiver **sombra projetada**: o
  inpainting apaga o traço e deixa a sombra, e o fantasma do português aparece
  atrás do espanhol.
- `"rotulos": [...]` — segundo caminho, para rótulo de infográfico: em vez de
  detectar cor, recebe o **retângulo exato** de cada rótulo, apaga com a cor de
  fundo local e redesenha centrado. Serve para texto escuro sobre fundo claro.
  `"partes"` numa linha permite misturar fontes (itálica + sigla em sans).
  `"margem"` afasta a análise da moldura; sem ela o filete entra na máscara e é
  apagado junto.

⚠️ Se a fonte do rótulo só existe como pixel (uma itálica de máquina de escrever,
por exemplo), não há como recuperá-la: escolha a mais próxima disponível e
**registre a troca no relatório**. É o único caso em que o material entregue
troca de tipo.

### 4. Apontar os QR Codes para os ativos traduzidos

```
python3 scripts/atualizar_qr.py es.pdf links_es.json --conferir   # relatório
python3 scripts/atualizar_qr.py es.pdf links_es.json --saida final.pdf
```

**O QR é imagem — não existe link a editar.** O destino está codificado nos
módulos preto-e-branco, então trocar de destino exige gerar um QR novo e
substituir a imagem. O script decodifica cada QR, casa o destino com o mapa
**pelo ID do arquivo** (não pela URL inteira, que muda de forma com `?usp=` e
`?t=`), gera o QR novo no mesmo lugar preservando a moldura decorativa, e
**confere lendo de volta** o QR gerado. Se não decodificar para o destino
esperado, aborta e reporta em vez de entregar um QR quebrado.

QR de artigo científico não é tocado: sem link no mapa, fica como está.

⚠️ **Marcador de tempo não sobrevive à retradução do vídeo.** Se o link original
tinha `?t=`, o ativo em espanhol quase sempre foi reencodado com duração
diferente — no ebook de olheiras, um vídeo de 667 MB virou 98 MB. Sem o
timestamp novo, o QR abre o vídeo do início. Sinalize ao autor; não invente
tempo.

### Verificação obrigatória

Quatro checagens, nesta ordem. As três primeiras são automáticas e não admitem
achado; a quarta é olho, e é a que pega o que log nenhum pega.

1. **Nada perdido** — o final de cada bloco do mapa reaparece na sua página.
2. **Nada sobreposto** — conte pares de linhas que se cruzam, no original e no
   traduzido: o traduzido não pode ter mais que o original em nenhuma página.
   Compare também a caixa de texto de cada página, para pegar invasão de imagem.
3. **Nada em português** — OCR das 74 páginas com diff contra a camada de texto
   isola o que só existe em imagem; regex de marca portuguesa (`ã õ ç ê`) sobre o
   que sobrou. Rode o `auditar.py` sobre a camada de texto do PDF **entregue**,
   não sobre o rascunho.
4. **Render lado a lado, página por página.** Defeito de glifo, acento cortado,
   fantasma de inpainting e refluxo sobre imagem **só aparecem no render**.

## Handoff obrigatório para a revisão

Tradução própria não se auto-aprova. Ao fechar, passe o material para a skill
**`fea-revision-es`**, que revisa como par especialista e emite veredito.

A revisão é deliberadamente **cega**: não forneça a ela as suas justificativas
de escolha. Quem traduz acumula razões para as próprias decisões, e essas razões
cegam para o erro. Entregue o texto ES, o original PT e os glossários — nada
mais. Se uma escolha sua precisa de justificativa para sobreviver, ela pertence
a `90-decisiones.md`, não a uma explicação avulsa ao revisor.

## Entregável padrão

Manuscrito bilíngue lado a lado (PT | ES), página por página do original, para
quem for aplicar no arquivo de diagramação — o espanhol corre 15% a 20% mais
longo que o português, e essa folga tem de ser resolvida por quem tem o arquivo
aberto. Mais dois anexos: o inventário de texto em arte e a lista de correções
do original.
