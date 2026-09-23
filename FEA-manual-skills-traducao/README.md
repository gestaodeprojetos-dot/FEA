# Manual das skills de tradução FEA

Duas entregas nesta pasta, geradas por script e regeneráveis:

| Arquivo | O que é | Para quem |
|---------|---------|-----------|
| `FEA-guia-instalacao-skills.pdf` | Passo a passo de instalação, 5 páginas, com checklist | quem vai instalar |
| `FEA-manual-skill-tradutora.pdf` | O manual de uso, 8 páginas | quem vai usar |
| `FEA-skills-traducao-es.zip` | As duas skills prontas para instalar | acompanha o guia |

## Regenerar os PDFs

```
PYTHONPATH=producao python3 producao/FEA-gerar-instalacao-pdf.py
PYTHONPATH=producao python3 producao/FEA-gerar-manual-pdf.py
```

O conteúdo de cada documento vive dentro do próprio script, em HTML. A
identidade visual e a composição ficam em `producao/FEA_estilo.py`, comum aos
dois: cores, capa, miolo, rodapé numerado e as três restrições do motor de
composição do pymupdf que a folha de estilo contorna.

Identidade FEP Experience por regra da skill `identidades-visuais`: material
sem produto envolvido usa a identidade do evento, sem logo, só cores e
elementos de design.

## Refazer o pacote das skills

```
cd .claude/skills && zip -qr ../../FEA-manual-skills-traducao/FEA-skills-traducao-es.zip \
    fea-traduccion-es fea-revision-es INSTALAR.md -x "*.DS_Store"
```

## As fontes em `producao/fontes/`

El Messiri, Manrope e JetBrains Mono, recortes latinos, vindos do Fontsource
via `npm pack` e convertidos de WOFF para TTF com fontTools. A Manrope entra no
lugar da Satoshi, que não está em host permitido. A JetBrains Mono serve só aos
blocos de comando do guia de instalação.

`producao/FEA-ligaduras.py` dá a essas fontes os glifos `fi` e `fl`. Sem eles o
motor de HTML do pymupdf, que troca esses pares pelas ligaduras U+FB01 e
U+FB02 por conta própria, corrompe a palavra: «verificação» saía
«verizcação». Os glifos são compostos de `f` mais `i` na largura natural, com
os nomes PostScript `fi` e `fl`, que é o que faz a camada de texto do PDF
extrair o par correto. Rodar uma vez após baixar fontes novas.
