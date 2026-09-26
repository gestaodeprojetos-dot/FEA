---
name: fea-edicao-reels
description: Edita vídeos verticais de procedimento da FEA (Dr. João Pithon) no padrão da equipe - cortes, título Montserrat grande e centralizado, legenda automática em Montserrat Bold com contorno preto, limite de 3 minutos com divisão em Parte 1/Parte 2. Usar quando a Keila pedir para editar vídeos, Reels, cortes de procedimento, legendar vídeos ou "editar a pasta" de brutos do Drive (full face, toxina, preenchimento, anestesia etc.).
---

# FEA: edição de Reels de procedimento

Padrão aprovado pela Keila em 23/09/2026 ("é assim mesmo que quero"). Detalhes visuais e histórico em `FEA-edicao-videos/FEA-padrao-edicao-videos.md`. Scripts em `FEA-edicao-videos/`.

## Entrada que a Keila manda

1. **Link da pasta de brutos** no Drive (vídeos .MOV do iPhone + uma **imagem com os títulos**).
2. **Pasta de destino** e o **nome da subpasta** a criar (ex.: dentro de "Setembro", `20- Full face 6mL e toxina`). Criar com o MCP do Drive (`create_file`, mimeType de pasta).
3. Às vezes, pastas de referência.

Sem imagem de títulos, a headline é o ponto-chave falado no vídeo (ex.: o Dr. diz "faltam 7 dias", headline "Faltam 7 dias"). Os títulos são **exatamente** os da imagem (ler com `read_file_content` do Drive, que faz OCR). Às vezes o nome de cada arquivo já é o título. Numerar `1- Título`, `2- Título`... na ordem da imagem, contínuo mesmo se a imagem reiniciar a numeração.

## Padrão visual (não mudar sem pedido)

| Item | Valor |
|---|---|
| Formato | 1080x1920, 30 fps, H.264, áudio original (sem trilha, sem normalizar) |
| Título | Montserrat ExtraBold 140 px, branco, contorno preto 5 px, centro exato do quadro, até 3 linhas de ~16 caracteres, **linhas juntas** (entrelinha 0,8 do tamanho da fonte, `TITULO_ENTRELINHA`; ajuste de 26/09/2026, a entrelinha padrão da Montserrat ficou aberta demais), nos **3 primeiros segundos** |
| Legenda | Montserrat **Bold 56 px**, branca, contorno preto 3,5 px, centralizada a ~80% da altura, 1 a 2 linhas de até 22 caracteres (cada linha ocupa ~1/3 da largura), começa minúscula, sem ponto final. **Só entra depois que o título sai**. Ajustada em 24/09/2026: a de 36 px ficou pequena demais |
| CTA | padrão desde 16/09: sem CTA. Quando a pasta trouxer um vídeo "CTA" e a Keila pedir (lote Black Amazonia, 26/09/2026), colar esse vídeo no final de cada edição com o campo `cta` do projeto.json (sem título nem legenda sobre ele; o limite de 3 min conta o CTA) |
| Parte 1/2 | se, depois de cortar, passar de 3 min: dividir; título igual com "Parte 1"/"Parte 2" embaixo; nos 3 s finais da Parte 1, cartela "Parte 2 no perfil" no estilo do título (`parte` e `cartela_final` no projeto.json) |

## Regras de corte (critério da editora da equipe)

- **Limite: 3 minutos.** Cortar o máximo necessário para caber.
- Manter: explicação clínica, técnica, dosagens, planejamento, falas de autoridade do Dr. João, e trechos **sem fala** mostrando o procedimento.
- **Começo sem silêncio**: o vídeo começa com o Dr. já falando. Rodar `python3 FEA-edicao-videos/fea_inicio_fala.py wav/*.wav` e iniciar o primeiro trecho de `manter` 0,08 s antes do valor (a transcrição marca 0,0 s mesmo com silêncio antes). Pedido de 26/09/2026.
- Tirar: conversa fora do tema (agenda, assuntos pessoais), trechos parados sem ação ("deixa eu segurar"), repetições, final arrastado.
- Tirar falas que atacam colegas ou concorrentes (ex.: "é tudo marketing, todo mundo finge"). Linha vermelha FEA: atacar o sistema, nunca pessoas.
- Vídeo que já cabe e é todo clínico fica **inteiro**.
- Se existir edição anterior **do mesmo material**, reproduzir os cortes dela por alinhamento de quadros (ver abaixo). Sempre conferir que é o mesmo paciente antes.

## Fluxo

1. **Ambiente**: `bash FEA-edicao-videos/fea_preparar_ambiente.sh <scratchpad>`. Se faltar rede, pedir à Keila para liberar os domínios listados no topo do script (menu do ambiente > Edit > Network access).
2. **Acesso aos vídeos**: os arquivos do Drive da FEA são privados. Pedir à Keila para colocar a pasta de brutos (e as referências) em **"Qualquer pessoa com o link: Leitor"** e depois voltar para Restrito. Baixar em paralelo com
   `curl -sSL -o arq.MOV "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`
   e conferir com `file` (se vier HTML "Sign-in", o link não está aberto). IDs pelo `search_files` do Drive com `parentId = 'ID_DA_PASTA'`.
3. **Áudio e transcrição**: extrair WAV mono 16 kHz com o FFmpeg de `env.sh` e rodar `python3 FEA-edicao-videos/fea_transcrever.py tr/ wav/*.wav` (roda em segundo plano; com VAD fica rápido).
4. **Mesmo material já editado?** Comparar quadros (miniaturas 27x48 em cinza a 5 fps, correlação normalizada). Correlação ~0,99 = mesmo material: mapear offset quadro a quadro a 30 fps e extrair os trechos `manter`. Zero correspondência = outro paciente, decidir os cortes pela transcrição.
5. **Cortes**: ler a transcrição com tempos, escolher `manter` (segundos do bruto) cortando em pausas entre palavras. Marcar em `remover_legenda` trechos em que a transcrição inventou fala sobre silêncio.
6. **projeto.json** (ver o docstring de `fea_editar_video.py`): `entrada`, `transcricao`, `saida`, `titulo`, `parte`, `cartela_final`, `manter`, `remover_legenda`, `correcoes` (regex extras do lote).
7. **Prévia primeiro**: `python3 fea_editar_video.py projeto.json --previa` gera versão 720p abaixo de 30 MB. Com pressa, `--entrega` gera direto o final em H.264 1080p abaixo de 30 MB (dividir o lote em 2 projetos e rodar em paralelo). Conferir visualmente um mosaico de quadros (título aos 1,5 s e legenda aos ~12 s de cada vídeo) antes de mandar.
8. **Revisão da Keila**: criar no Drive, dentro da pasta de destino, um Google Doc `FEA-revisao-legendas-<lote>` com as legendas de cada vídeo (`[mm:ss] texto`, extraídas dos .ass) e, no topo, os pontos para decidir. Enviar as prévias pelo `SendUserFile`.
9. **Final**: aplicar as correções, rodar sem `--previa` (qualidade total) e subir para a pasta de destino.

## Pontos para sempre levar à Keila antes de finalizar

- Marcas faladas (ácido hialurônico, toxina, bioestimulador, distribuidoras). Ela aprovou manter nos lotes de setembro, mas confirmar grafia. Confirmadas: Neuramis Volume, Revanesse Kiss, Neauvia Stimulate, Yvoire Contour, Letybo, Seryntox, Vietri.
- Afirmações absolutas de resultado ou segurança ("zero intercorrência, zero necrose"): recomendar cortar por compliance CFM/CFO; a decisão é dela.
- Recomendação comercial (ex.: distribuidora): perguntar se é parceria.
- Nome de paciente falado ou legendado: confirmar grafia.
- Quantidade de vídeos diferente da quantidade de títulos na imagem.

Decisões já tomadas pela Keila (lote Black Amazonia, 26/09/2026), não perguntar de novo:
- "Harmonização facial" na fala do Dr. João está correto: ele é médico, não dentista. Manter.
- Campanha Black Friday Vitalícia: "o último curso que você vai comprar", "nunca mais compre um curso", "a maior Black Friday da harmonização facial" e "não vai ter outra chance" (último dia) estão aprovados pelo comercial.
- Série de contagem regressiva: headline no formato "Faltam N dias" / "Falta 1 dia", mesmo quando a fala é "Em N dias começa".
- Linguagem falada na legenda: "tamo junto" vira "estamos juntos", "tá" vira "está".

## Headlines sem imagem de títulos

Antes de renderizar, mandar à Keila um Google Doc `FEA-revisao-headlines-<lote>` com, para cada vídeo: a fala dos 3 primeiros segundos, a headline atual e 2 ou 3 opções tiradas da fala (recomendação marcada). A contagem regressiva "Faltam N dias" já está aprovada; as demais ela escolhe (em 26/09/2026 ela recusou headlines de resumo, quer o gancho do vídeo).

## Selfie espelhada e ruído de fundo (pedido de 26/09/2026)

- **Fundo ao contrário** (texto do banner invertido, câmera frontal): `"espelhar": true` no vídeo. Conferir no mosaico de quadros quais estão invertidos.
- **Ruído ao fundo** (ar-condicionado, clínica): `"limpar_audio": "rnn/sh.rnnn"` no projeto (RNNoise via `arnndn` + `afftdn` leve). O `fea_preparar_ambiente.sh` baixa o modelo. Conferir que a fala continua intacta transcrevendo o áudio limpo de um vídeo.
- Arquivos "v_daa....mp4" exportados de app costumam ser cópia de um .mov da mesma pasta: comparar transcrição e duração e editar só o original.

## Legenda logo depois do título

A fala dos 3 primeiros segundos fica só sob o título. O script descarta o pedaço de frase dito sob o título até a última pontuação (evita legenda começando em "vitalícia, para você...") e nunca quebra "Saiba Mais" ou "Black Friday Vitalícia" entre duas legendas (`TERMOS_JUNTOS`). Se ainda sobrar fragmento, usar `remover_legenda` no trecho.

## Correções de texto

`CORRECOES` em `fea_editar_video.py` aplica a regra FEA (nunca "pra", sempre "para") e termos técnicos (carpule, têmpora, interfascial, hidroxiapatita, tecidual, sulco nasolabial, tan delta, mL...). Toda grafia nova confirmada pela Keila entra ali e, se for nome próprio, em `NOMES_PROPRIOS`. Conferir na tela do vídeo (caixa do produto) quando houver dúvida de marca.

## Entrega e limites conhecidos

- `SendUserFile` aceita no máximo **30 MB** por arquivo. Para a Keila guardar no computador: **H.264** 1080p abaixo de 30 MB, em 2 passadas (`libx264 -preset medium -pass 1/2`, bitrate de vídeo = 27,5 MB x 8 / duração, menos 96 kbps do áudio AAC). **Nunca HEVC/H.265**: no computador dela o vídeo abre com tela preta e só áudio (aconteceu em 24/09/2026).
- A conexão do Drive não sobe vídeos grandes. Caminho definitivo: conta de serviço `fea-upload-69@fea-edicao-videos.iam.gserviceaccount.com` (projeto Google Cloud FEA-edicao-videos), com Editor na pasta Setembro. **Bloqueio em 24/09/2026**: política `iam.disableServiceAccountKeyCreation` impede gerar a chave JSON; o administrador do Workspace precisa criar exceção só para o projeto. Com a chave, subir pela API do Drive (`supportsAllDrives=true`, upload resumable), guardando a chave em `.env` fora do git.
- A máquina é temporária: vídeos só na nuvem se perdem se a sessão ficar parada. Scripts e projeto.json ficam no git.

## Armadilhas

- Nunca `pkill -f fea_editar_video.py`: mata o próprio shell que contém o texto. Usar o PID do processo.
- Transcrição sem VAD inventa "tchau"/"obrigado" em trechos silenciosos. Com VAD, palavras podem ficar "esticadas"; o script já limita a 1,2 s e quebra a legenda no início de cada frase.
- Renderizar leva cerca de 1 min por minuto de vídeo nesta máquina (4 CPUs). Avisar a Keila do tempo estimado e usar tarefas em segundo plano.
- Os 8 vídeos do lote "20- Full face 4mL" estão encerrados: não editar mais (pedido da Keila em 23/09/2026).
