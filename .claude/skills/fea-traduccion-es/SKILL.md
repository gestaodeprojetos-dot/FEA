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

## Passagem obrigatória — inventário de mídia e QR Codes

**Todo vídeo referenciado no material precisa de versão em espanhol.** Um ebook
traduzido cujos QR levam a vídeo em português está entregue pela metade: o aluno
hispano-hablante lê em espanhol e assiste em português.

Nos materiais FEA os botões de vídeo são **arte, não anotação de link** — o
destino está codificado dentro da imagem do QR. Extração normal de PDF não vê
nada. Rode:

```
python3 scripts/inventario_midia.py material.pdf
```

O script decodifica os QR (OpenCV, 300 e 450 dpi), separa YouTube de Drive,
detecta marcador de tempo `?t=` e aponta quais IDs do Drive classificar. Depois,
classifique cada destino do Drive pelo **mimeType real** (`video/mp4` = traduzir;
`application/pdf` = artigo, permanece em inglês).

Produza a tabela de inventário com, para cada ativo:

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
