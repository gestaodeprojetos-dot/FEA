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

`references/00-nucleo.md` é **obrigatório em toda tradução**. Depois carregue o
módulo do tema tratado:

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

## As três passagens

Não pule nenhuma. Cada uma pega uma classe de erro diferente.

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

### Passagem 2 — Revisão terminológica contra o glossário
Varra o texto ES procurando cada entrada dos módulos carregados. Confirme que
toda ocorrência usa a forma ES obrigatória, que nenhuma armadilha da seção de
alto risco passou, que as unidades estão normalizadas e que as marcas têm
grafia exata. Rode um `grep -n` pelas armadilhas do núcleo antes de fechar.

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

## Entregável padrão

Manuscrito bilíngue lado a lado (PT | ES), página por página do original, para
quem for aplicar no arquivo de diagramação — o espanhol corre 15% a 20% mais
longo que o português, e essa folga tem de ser resolvida por quem tem o arquivo
aberto. Mais dois anexos: o inventário de texto em arte e a lista de correções
do original.
