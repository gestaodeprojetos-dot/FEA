# Manual das skills de tradução FEA

Duas entregas nesta pasta, geradas por script e regeneráveis:

| Arquivo | O que é |
|---------|---------|
| `FEA-manual-skill-tradutora.pdf` | O manual em 9 páginas, para circular no time |
| `FEA-skills-traducao-es.zip` | As duas skills prontas para instalar |

## Regenerar o PDF

```
python3 producao/FEA-gerar-manual-pdf.py
```

O conteúdo vive dentro do próprio script, em HTML. Identidade FEP Experience
por regra da skill `identidades-visuais`: material sem produto envolvido usa a
identidade do evento, sem logo, só cores e elementos de design.

## Refazer o pacote das skills

```
cd .claude/skills && zip -qr ../../FEA-manual-skills-traducao/FEA-skills-traducao-es.zip \
    fea-traduccion-es fea-revision-es INSTALAR.md -x "*.DS_Store"
```

## As fontes em `producao/fontes/`

El Messiri e Manrope, recortes latinos, vindos do Fontsource via `npm pack` e
convertidos de WOFF para TTF com fontTools. A Manrope entra no lugar da
Satoshi, que não está em host permitido.

`producao/FEA-ligaduras.py` dá a essas fontes os glifos `fi` e `fl`. Sem eles o
motor de HTML do pymupdf, que troca esses pares pelas ligaduras U+FB01 e
U+FB02 por conta própria, corrompe a palavra: «verificação» saía
«verizcação». Os glifos são compostos de `f` mais `i` na largura natural, com
os nomes PostScript `fi` e `fl`, que é o que faz a camada de texto do PDF
extrair o par correto. Rodar uma vez após baixar fontes novas.
