# FEA: padrão de edição de vídeos verticais (Reels de procedimento)

Versão 1.0 · criado em 23/09/2026 · responsável: Keila Quaresma (aprovação) · execução: Claude

## De onde veio o padrão

As referências analisadas foram as pastas de setembro "2- Full face 3ml", "4- Full face 4ml", "17- 4mL e toxina" e "19- Full face e toxina". A pasta "4- Full face 4ml" é a edição anterior do mesmo material bruto da pasta de julho (IMG_5481 a IMG_5489). O alinhamento quadro a quadro deu entre 97% e 100% de correspondência, então os cortes da editora foram reproduzidos exatamente.

## O que a editora faz (e o script replica)

| Item | Padrão |
|------|--------|
| Formato | vertical 1080x1920, 30 fps, sem zoom nem reenquadramento, áudio original sem trilha nem normalização |
| Cortes | remove conversa fora do tema (agenda, assuntos pessoais) e trechos repetidos; mantém fala clínica e também trechos sem fala em que o procedimento aparece |
| Título | nos primeiros 3 segundos, branco, centralizado; a legenda só entra depois que o título sai |
| Legenda | frases curtas (1 a 2 linhas), brancas, centralizadas no terço inferior, começando com minúscula, sem ponto final |
| Encerramento | as edições de agosto e começo de setembro tinham CTA da Imersão Full Face 10 mL; as de 16/09 em diante não têm mais. **Padrão atual: sem CTA** |

## Ajustes pedidos pela Keila (23/09/2026)

| Item | Referência | Novo padrão |
|------|-----------|-------------|
| Fonte | sans-serif padrão do app | **Montserrat** (título ExtraBold, legenda Bold) |
| Título | cerca de 95 px | **ExtraBold 116 (ASS), entrelinha 0,78**, centralizado, 2 linhas equilibradas acima de 14 caracteres (até ~22 por linha), contorno preto sólido 4 px; medido na referência de 24/09 |
| Legenda | cerca de 40 px, a 78% da altura | **Montserrat Bold 56 px, contorno preto, a ~80% da altura** (ajuste de 24/09: a versão de 36 px ficou pequena) |
| Duração máxima | sem regra | **3 minutos**. Corta o máximo possível; se ainda passar, divide em Parte 1 e Parte 2 |
| Divisão | não havia | Título igual com "Parte 1" (ou "Parte 2") embaixo; nos 3 s finais da Parte 1 entra "Parte 2 no perfil" no estilo do título |
| Títulos | editora | exatamente os da imagem enviada na pasta de brutos |

## Regras de texto nas legendas

- Nunca "pra": sempre "para" (também "pro" vira "para o").
- Correções técnicas fixas no script: carpule, têmpora, interfascial, bolus, mL, nomes de produto com grafia oficial.
- Trechos em que a transcrição automática "inventa" fala sobre silêncio (por exemplo, "tchau" repetido) são removidos da legenda.
- A interjeição "ó" não entra na legenda.
- Cânula em calibre x comprimento (22x70); G linha = G', G duas linhas = G''.
- Entrelinha 0,78 no título e 0,80 na legenda, medidas em pixels nas referências da Keila.
- Vídeo começa assim que o Dr. começa a falar (sem silêncio no início) e nunca termina com frase cortada; trecho silencioso repetindo o procedimento do outro lado é cortado.
- Cortar: espelho para a paciente se ver, pedido de "fecha o olho", conversa de fundo (ou silenciar) e conversa pessoal ou de histórico da paciente.
- Cortar tudo que dá errado: sangramento visível, agulha estourando, intercorrência, dor, fala ao fundo, e o tempo procurando o pertuito.
- Corte sempre no respiro entre palavras, nunca com o começo da palavra seguinte.
- Legenda só aparece quando há voz no áudio: nada de palavra solta no silêncio.
- Gemido ou expressão de dor da paciente: cortar ou silenciar; no meio do procedimento, zoom no ponto tratado.
- A Keila revisa as legendas antes de finalizar.

## Pontos de atenção de compliance

- Menção falada a marcas de ácido hialurônico (Neuramis Volume, Revanesse Kiss) nos vídeos de bigode chinês, pré-jowl, têmporas e preenchimento labial: mantida com aprovação da Keila em 23/09/2026.
- Nome da paciente é falado no vídeo 1 (mantido na edição anterior).

## Fluxo técnico

1. Baixar brutos e referências (pastas com "qualquer pessoa com o link"; voltar para Restrito depois).
2. Transcrever com Whisper large-v3-turbo (palavras com tempo).
3. Definir trechos mantidos (`manter`) por vídeo no `projeto.json`.
4. `python3 fea_editar_video.py projeto.json --previa` para revisão (720p, abaixo de 30 MB); sem `--previa` para o final em qualidade total.
5. Revisão da Keila, correções, render final e envio para a pasta de destino no Drive.

Passo a passo completo na skill `.claude/skills/fea-edicao-reels/SKILL.md`.

## Criativos de anúncio Elite Mentoring (Dr. João falando para a câmera), v2 de 06/11/2026

Script: `fea_criativo.py` (projeto: `FEA-projeto-criativos-diagnostico-nov.json`). A v1 (cartões roxos, legenda em blocos curtos, jump cut agressivo) foi reprovada pela Keila: "legenda feia, cortes estranhos, o Dr. comendo palavra".

| Item | Padrão v2 |
|------|-----------|
| Identidade | Elite Mentoring (Drive: pasta ELITE MENTORING; página do diagnóstico): fundo `#011A24`, superfície `#072B38`, turquesa `#62B9B4`, água `#86F9F8` |
| Fontes | títulos em Gloock (a Canela Deck do Drive é trial e não tem acento; a página usa Gloock como substituta), textos em Galano Grotesque (Drive), legenda em Montserrat |
| Logo | EM_Asset 15 (símbolo em degradê, ELITE branco, MENTORING turquesa) no topo, o vídeo inteiro |
| Gancho | cartão escuro no topo, selo "DIAGNÓSTICO GRATUITO" em turquesa espaçado e headline em Gloock branca, 4 s |
| Legenda | padrão dos conteúdos FEA: Montserrat Bold 56, branca, contorno preto, ~80% da altura, até 2 linhas de 22 caracteres |
| Inserts | cartão escuro com borda água e texto em Galano caixa alta, 3 por vídeo, com whoosh |
| Saiba Mais | pílula água com texto escuro (o botão da página) e seta água abaixo da legenda |
| Cortes | só sai silêncio real (ruído de fundo + 6 dB por 0,55 s ou mais) com 0,2 s de respiro; erros de fala (frase abandonada, gaguejada) saem pelo `manter`. Nunca usar o limiar de voz do Reels (ruído + 12 dB): ele corta sílaba fraca |
| Zoom | alterna 100%/110% só depois de trecho de 2 s ou mais |
| Trilha | uma por vídeo, voz em -15 LUFS e trilha em -28 LUFS, abaixando quando ele fala |

### Ajustes de 07/11/2026 (v3)

| Item | Padrão |
|------|--------|
| Enquadramento | rosto detectado a cada 0,5 s (OpenCV); zoom até deixar o rosto em ~27% da altura (busto), entre 1x e 1,8x, centrado no rosto. Com o Dr. sentado longe, as pernas saem do quadro. Quando ele se mexe ou a câmera ajusta, o zoom acompanha (zoompan com curva) |
| Cortes | a cada corte entra um punch-in leve (7%) alternado, para o pulo não ficar estranho; pontos conferidos no áudio em janelas de 10 ms podem ir como `[a, b, "exato"]` |
| Abertura | quando o começo do bruto não presta (o Dr. ainda sentando), cartão de tela cheia da marca (logo, selo, gancho) por cima da fala (`abertura` em segundos) |
| Ilustrações | `fea_ilustracoes.py`, no estilo dos slides do pitch: `crescimento` (barras + linha com seta), `pilares`, `passos` numerados, `plano` (itens que se somam) e `relogio` (2 minutos). Entram na frase-gatilho, por 3,6 s, no centro da tela, com whoosh; se cair no botão Saiba Mais, entram logo depois |

### Ajustes de 07/11/2026 (v4): cortes

Reprovado: "o Dr. dá uma errada e você deixa". Causa: a transcrição padrão (Whisper) LIMPA a fala, então tropeço, repetição e frase recomeçada não apareciam.

- Transcrição LITERAL em todo criativo (prompt com hesitações, sem VAD, sem contexto anterior), salva em `trv/`, e revisão vídeo a vídeo com o mapa de tropeços (repetição, palavra cortada, pausa com voz sem palavra).
- Ponto ambíguo: transcrever o trecho de 2 a 3 s isolado. A transcrição longa às vezes "inventa" repetição (vídeos 2, 5, 6 e 10 estavam limpos).
- Erro confirmado vai em `remover` com pontos medidos no áudio em janelas de 10 ms (respiro entre palavras).
- Pausa e hesitação: sai todo trecho abaixo de ruído + 10 dB por 0,40 s ou mais sem palavra da transcrição literal, com 0,12 s de respiro.
- Sem cartão de abertura em tela cheia (a Keila não gostou).

