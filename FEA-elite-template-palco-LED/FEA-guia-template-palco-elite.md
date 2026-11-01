# FEA · Template de palco Elite Injectors Congress

Painel de LED **4032 x 1344 px** (proporção 3:1, 24 x 4 módulos de 168 x 336 px). Evento: 01 e 02 de novembro de 2026, Sheraton São Paulo WTC Hotel.

## O que tem nesta pasta

| Item | Para que serve |
|------|----------------|
| `FEA-elite-template-palco-LED-4032x1344.pptx` | Template editável com 16 layouts. Slide já no tamanho do painel: exportar ou projetar sem redimensionar. |
| `FEA-previas/` | Os 16 slides renderizados em JPG 4032 x 1344, para conferir e para usar direto em mesa de corte. |
| `FEA-fundos/` | Fundos limpos (sem texto), logo claro em PNG transparente, monograma T e a moldura 16:9 com centro transparente. |
| `FEA-fonte-scripts/` | Scripts que geram tudo de novo (fundos, PPTX e correções do arquivo). |

## Layouts

01 Abertura · 02 Palestrante · 03 Abertura de palestra · 04 Antes e depois · 05 Antes e depois, 2 casos · 06 Caso com foto complementar (igual à referência do palco) · 07 Tela 16:9 central · 08 Tela cheia 3:1 · 09 Três tópicos · 10 Alerta, zona de risco · 11 Citação · 12 Intervalo · 13 QR code · 14 Patrocinadores · 15 Encerramento · 16 Guia técnico (não exibir).

Para criar slide novo: **Página Inicial > Novo Slide > escolher o layout**. Fotos: clicar no ícone de imagem dentro do espaço reservado; o PowerPoint recorta e arredonda sozinho.

## Antes de abrir no computador do palco (obrigatório)

1. **Instalar a fonte Galano Grotesque** no computador que roda o PowerPoint (pasta do Drive: `2. KV Elite Injectors Congress > 03 - TIPOGRAFIA > Galano Grotesque`). Sem ela o PowerPoint troca a fonte e o layout desalinha. Os arquivos de fonte não ficam neste repositório porque são licenciados.
2. Abrir o PPTX e conferir os slides 01, 02 e 11 com as prévias JPG. Se o texto estiver diferente da prévia, a fonte não foi instalada.
3. Salvar uma cópia com fontes incorporadas: **Arquivo > Opções > Salvar > Incorporar fontes no arquivo > Incorporar todos os caracteres** (Windows).
4. Projetar em tela cheia na saída do LED com resolução 4032 x 1344, sem escala.

## Mesa de corte (vMix, Resolume, ProPresenter)

- Slides prontos: usar os JPG de `FEA-previas/` ou exportar do PowerPoint em **Arquivo > Exportar > PNG** (sai em 4032 x 1344).
- Slides 16:9 dos palestrantes ou câmera: usar `FEA-elite-moldura-16x9-centro-transparente.png` como sobreposição e posicionar a entrada 16:9 na janela central (x 821, y 0, 2390 x 1344).

## Decisões de identidade

- Paleta oficial do KV: preto `#050C0F` (Pantone Black 6 C), azul `#7FB3C6` (Pantone 550 C), cinza claro `#EBF2F5` (Cool Gray 1 C), tom claro do gradiente `#D3EAF2`. Vermelho `#BB3838` só no layout de alerta.
- Logo, monograma T e gradiente vieram dos arquivos oficiais (SVG) da pasta do KV, renderizados em alta resolução.
- **Canela Deck não foi usada no texto editável**: a versão no Drive é *Trial*, com 74 caracteres e **sem acentos** (ã, ç, é, ô). Qualquer título em português quebraria no telão. Para usar Canela, é preciso a licença completa (Commercial Type).
- Fundos gerados por código a partir do KV (luz fria de palco, contorno do monograma, brilho de piso). Nenhuma imagem de IA generativa.

## Regras de conteúdo mantidas

Aviso fixo "Resultados variam de acordo com cada paciente." nos layouts de antes e depois · sem marca de produto sem aprovação · QR code com UTM único por slide (`utm_source=palco`, `utm_medium=led`, `utm_campaign=elite-injectors-2026`, `utm_content=nome-do-slide`).

## Regerar

```bash
cd FEA-elite-template-palco-LED/FEA-fonte-scripts
python3 fea_fundos_elite.py <pasta_assets>          # precisa de T-mask.png (logo7.svg renderizado)
PPTX_SKILL=<skill pptx> NODE_PATH=<node_modules> node fea_gerar_template_palco_elite.js <pasta_assets> saida.pptx
python3 fea_pos_processar.py saida.pptx FEA-elite-template-palco-LED-4032x1344.pptx
```

O pós-processamento corrige dois defeitos do pptxgenjs: espaços de foto sem o tipo "imagem" e nomes de mídia com ":" e acentos (que impedem o arquivo de abrir em alguns leitores).
