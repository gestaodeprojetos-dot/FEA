# Anexo 4 — Por que o PDF não pode ser traduzido «no lugar»

Testado no arquivo real, não estimado. Três bloqueios independentes; o primeiro
é definitivo.

## Bloqueio 1 — A fonte do corpo de texto não tem os glifos do espanhol

O corpo de texto usa **GuardianTextEgyp-Regular, 11 pt**, embutida no PDF como
**subconjunto CFF de 8,4 KB com apenas 89 glifos** — só o que o português usa.

Inspeção do charset:

```
WDSKFF+GuardianTextEgyp-Regular — 89 glifos
   TEM:   á é í ó ú ã õ ç
   FALTA: ñ Ñ ¿ ¡ ü « » —
WDSKFF+GuardianTextEgyp-Bold — 82 glifos
   FALTA: ñ Ñ ¿ ¡ ü « » —
```

Faltam exatamente os caracteres que o espanhol exige. `¿Qué es la SOOF?` não
pode ser escrito nessa fonte: o `¿` não existe no arquivo. O resultado seria
caractere vazio ou tofu.

Contornar exige **embutir outra fonte**. Guardian Text Egyptian é licenciada
(Commercial Type) e o arquivo completo não está no PDF — só o subconjunto. Trocar
por uma fonte parecida altera a tipografia de forma visível em 59 páginas.

*Observação:* as HelveticaNeue do material **têm** todos os glifos espanhóis
(2.000+ cada). O problema é a serifada do corpo de texto, que é a que carrega
quase todo o conteúdo.

## Bloqueio 2 — O espanhol é 15 % a 20 % mais longo

Medido: 8.056 palavras em espanhol contra o português original. Cada caixa de
texto justificada precisa de nova quebra de linha e nova hifenização. Isso é
trabalho de diagramação, não de substituição automática — e substituir sem
rediagramar produz texto transbordando ou linhas frouxas.

## Bloqueio 3 — 194 linhas de texto estão dentro das imagens

Levantadas por OCR em 29 páginas. Incluem **o título na capa e na contracapa**,
os rótulos dos infográficos das páginas 22, 36 e 57, e as pranchas de atlas.
Nenhuma pode ser alterada sem editar a arte. Nenhuma ferramenta de PDF resolve
isso, porque não é texto — é pixel.

## O caminho correto

O arquivo de origem da diagramação (InDesign, `.indd` ou `.idml`) com a fonte
licenciada instalada. O designer substitui o texto, reflui as caixas, reaplica os
rótulos de arte, troca os QR e reexporta. O resultado é um PDF de qualidade
igual à do original.

**O entregável que alimenta esse processo já está pronto:**

| Arquivo | Serve para |
|---|---|
| `Relleno_Ojeras_ES_manuscrito_bilingue.docx` | O texto ES, página por página, lado a lado com o PT |
| `anexo-1-texto-en-arte.md` | Os rótulos de arte, com página e tradução |
| `anexo-3-inventario-videos-qr.md` + planilha | Os QR a regerar e os vídeos a traduzir |
| `anexo-2-correcoes-original.md` | Correções e pontos que pedem decisão do autor |

## Alternativa, se não houver o arquivo de origem

É possível gerar um PDF **de conferência**: substituindo a serifada por uma fonte
aberta de desenho semelhante, com o texto espanhol refluido. Serve para validar
conteúdo e leitura, **não para publicar** — a tipografia não será a do original.
Sob demanda.
