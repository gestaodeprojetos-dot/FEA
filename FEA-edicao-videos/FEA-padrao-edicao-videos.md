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
| Fonte | sans-serif padrão do app | **Montserrat** (título ExtraBold, legenda SemiBold) |
| Título | cerca de 95 px | **140 px**, centralizado, até 3 linhas equilibradas, contorno preto grosso (5 px) |
| Legenda | cerca de 40 px, a 78% da altura | **Montserrat Bold 56 px, contorno preto, a ~80% da altura** (ajuste de 24/09: a versão de 36 px ficou pequena) |
| Duração máxima | sem regra | **3 minutos**. Corta o máximo possível; se ainda passar, divide em Parte 1 e Parte 2 |
| Divisão | não havia | Título igual com "Parte 1" (ou "Parte 2") embaixo; nos 3 s finais da Parte 1 entra "Parte 2 no perfil" no estilo do título |
| Títulos | editora | exatamente os da imagem enviada na pasta de brutos |

## Regras de texto nas legendas

- Nunca "pra": sempre "para" (também "pro" vira "para o").
- Correções técnicas fixas no script: carpule, têmpora, interfascial, bolus, mL, nomes de produto com grafia oficial.
- Trechos em que a transcrição automática "inventa" fala sobre silêncio (por exemplo, "tchau" repetido) são removidos da legenda.
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
