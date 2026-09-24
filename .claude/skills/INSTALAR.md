# Como instalar as skills FEA de tradução

Duas skills, que trabalham em sequência:

- **`fea-traduccion-es`** — traduz PT-BR → ES (LatAm)
- **`fea-revision-es`** — revisa e libera ou retém a entrega

## Instalação

### Opção 1 — pessoal (vale em qualquer projeto seu)

Descompacte e mova as duas pastas para `~/.claude/skills/`:

```bash
unzip skills-fea-traducao.zip
mkdir -p ~/.claude/skills
cp -r fea-traduccion-es fea-revision-es ~/.claude/skills/
```

### Opção 2 — por projeto (vale só na pasta do projeto, e vai para o Git)

```bash
unzip skills-fea-traducao.zip -d .claude/skills/
```

Reinicie o Claude Code. As skills aparecem sozinhas quando você pedir uma
tradução ou uma revisão — não precisa chamá-las pelo nome.

## Dependências

O auditor e o inventário de mídia usam bibliotecas Python:

```bash
pip install pymupdf opencv-python-headless python-docx openpyxl
```

Para OCR do texto embutido em arte:

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por tesseract-ocr-spa
# macOS
brew install tesseract tesseract-lang
```

Sem essas dependências a tradução funciona, mas as verificações automáticas e o
levantamento de arte e QR não rodam.

## Como usar

Basta pedir em linguagem natural:

- «traduza este ebook para espanhol»
- «revise esta tradução antes de eu publicar»
- «levante os vídeos e QR deste material»

A skill começa pela **Passagem 0 — curadoria**: levanta o que existe no material
(texto, arte, vídeos, artigos), classifica o que traduz e o que não traduz, e
mostra o mapa antes de traduzir qualquer palavra.

## Uso pelos scripts, sem passar pela conversa

```bash
# auditoria de uma tradução já feita
python3 fea-traduccion-es/scripts/auditar.py texto_es.txt
# exit 0 = liberado ou com ressalvas · exit 1 = retido

# inventário de vídeos e QR de um PDF
python3 fea-traduccion-es/scripts/inventario_midia.py material.pdf
```

## Estrutura

```
fea-traduccion-es/
├── SKILL.md                       processo: curadoria + 3 passagens
├── FICHA.md                       resumo do sistema em linguagem acessível
├── references/
│   ├── 00-nucleo.md               terminologia de todo o catálogo
│   ├── 01-voz-y-estilo.md         voz nativa: lusismos, falsos amigos, tipografia
│   ├── 11-rellenos-ah-ojeras.md   ácido hialurônico, reologia, olheiras
│   ├── 15-intercurrencias.md      30 complicações, doses, vias
│   ├── 90-decisiones.md           decisões terminológicas registradas
│   └── 91-catalogo-aulas.txt      mapa de 684 aulas em 62 módulos
└── scripts/
    ├── auditar.py                 auditor determinístico com veredito
    └── inventario_midia.py        decodificador de QR e inventário

fea-revision-es/
├── SKILL.md                       revisão cega em 4 camadas
└── references/rubrica.md          rubrica de severidade e veredito
```

## Onde ampliar

Faltam os módulos de toxina, bioestimuladores, fios, corporais, tecnologias,
dermatologia e gestão — 33 dos 62 módulos do catálogo. Cada um se constrói a
partir de material real com texto extraível. Ver `90-decisiones.md` para o
critério.
