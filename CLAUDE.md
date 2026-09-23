# FEA — orientações do projeto

## Identidade visual: consultar antes de produzir qualquer peça

**Sempre que o trabalho for sobre um projeto, produto ou evento específico da FEA
— criativo, página, documento, apresentação, e-mail, qualquer peça que alguém
vá ver — consulte primeiro a planilha de identidades visuais:**

<https://docs.google.com/spreadsheets/d/1llysTySv6se2-qtvc4io2zbuhh6-3gj1KTYhyE5VdhE/edit>

A planilha é o índice mestre. Cada linha traz **categoria**, **nome**, **link
para a pasta de identidade** no Drive e se existe **KV** (key visual). As
categorias cobrem institucional, eventos, produtos, lançamentos pagos,
masterclasses gratuitas, ebooks e LatAm.

Nunca invente paleta, tipografia ou tom visual de um projeto da FEA. Se a
identidade não estiver na planilha, pergunte — não deduza a partir de outro
material.

### Como achar a identidade de um projeto

1. Abra a planilha e localize a linha do projeto pelo nome ou pela sigla.
2. Vá à pasta de identidade ligada naquela linha. A estrutura é padronizada:

   ```
   <N>. ID <PROJETO>/
   ├── 01 - ID VISUAL/      PNG, PDF e PSD do manual de marca
   ├── 02 - LOGOTIPO/       SVG, PNG, PDF
   ├── 03 - ELEMENTOS DE APOIO/   GRAFISMOS e IMAGENS
   ├── 04 - TIPOGRAFIA/     uma pasta por família
   ├── 05 - ENTREGÁVEIS/
   └── 06 - MOTION/
   ```

3. As cores saem das páginas do manual em `01 - ID VISUAL`. O manual costuma
   ser imagem, sem camada de texto: **amostre os pixels**, não confie em
   memória nem em descrição.

### Ferramentas que funcionam nesse Drive

- `mcp__Google_Drive__search_files` com `parentId = '<id da pasta>'` para
  navegar a árvore.
- `mcp__Google_Drive__read_file_content` faz OCR de PNG — barato, e às vezes
  já entrega o texto do manual. Devolve vazio quando a página não tem texto
  reconhecível.
- `mcp__Google_Drive__download_file_content` devolve base64. Para arquivo
  grande o resultado é gravado em disco pelo harness: decodifique com
  `jq -r '.content' <arquivo> | base64 -d > saida.png` e amostre com pymupdf,
  em vez de trazer o base64 para a conversa.

### Siglas já mapeadas

| Sigla | Projeto |
|---|---|
| FEPEXP | FEP Experience (evento) |
| FEP | Formação Especialista em Preenchimento |
| FEB | Formação Especialista em Botox |
| FEEL | Formação em Escultura Labial |
| FEF | Formação Especialista em Fios |
| ATSD | Atenda Todo Santo Dia |
| CAC | Curso Avançado de Complicações |
| ARTI | Protocolo ARTI (faz parte da FEP) |

### FEPEXP — FEP Experience

Aferido em 23/09/2026 a partir de `3. ID FEP Experience` no Drive, amostrando
os pixels do manual.

| Papel | Valor |
|---|---|
| Gradiente da marca | `#4757FF` → `#A641FF` (azul-índigo a roxo) |
| Preto de fundo | `#020202` — o key visual é preto-dominante |
| Cinza de apoio | `#969FA9` |
| Branco | `#FFFFFF` |
| Tipografia | TT Firs Neue · Satoshi · El Messiri |

O gradiente aparece como **filete fino**, não como fundo chapado. Das três
famílias, só El Messiri está no Google Fonts; em peça web, substituir Satoshi
por Manrope e registrar a troca.

## Tradução PT → ES

Duas skills, em `.claude/skills/`, que trabalham em sequência: `fea-traduccion-es`
traduz e produz o arquivo final; `fea-revision-es` revisa às cegas e emite
veredito. Tradução própria não se auto-aprova — a revisão não recebe as
justificativas do tradutor.
