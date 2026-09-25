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

Os títulos são **exatamente** os da imagem (ler com `read_file_content` do Drive, que faz OCR). Às vezes o nome de cada arquivo já é o título. Numerar `1- Título`, `2- Título`... na ordem da imagem, contínuo mesmo se a imagem reiniciar a numeração.

## Padrão visual (não mudar sem pedido)

| Item | Valor |
|---|---|
| Formato | 1080x1920, 30 fps, H.264, áudio original (sem trilha, sem normalizar) |
| Título | Montserrat **ExtraBold 116** (tamanho ASS), branco, contorno preto sólido 4 px + sombra 1 px, centro exato do quadro, **2 linhas equilibradas** sempre que passar de 14 caracteres (até ~22 por linha; 3 linhas só se não couber), **entrelinha 0,78** (linhas bem próximas). Medido em pixels na referência da Keila em 24/09/2026: a linha mais longa ocupa ~2/3 da largura. Nos **3 primeiros segundos** |
| Legenda | Montserrat **Bold 56 px**, branca, contorno preto 3,5 px, centralizada a ~80% da altura, 1 a 2 linhas de até 22 caracteres (cada linha ocupa ~1/3 da largura), entrelinha 0,80 (medida na referência da Keila), começa minúscula, sem ponto final, **sem a interjeição "ó"**. **Só entra depois que o título sai**. Ajustada em 24/09/2026: a de 36 px ficou pequena demais |
| Sem CTA | não colocar chamada de imersão no final (padrão desde 16/09) |
| Parte 1/2 | se, depois de cortar, passar de 3 min: dividir; título igual com "Parte 1"/"Parte 2" embaixo; nos 3 s finais da Parte 1, cartela "Parte 2 no perfil" no estilo do título (`parte` e `cartela_final` no projeto.json) |

## Regras de corte (critério da editora da equipe)

- **Limite: 3 minutos.** Cortar o máximo necessário para caber.
- Manter: explicação clínica, técnica, dosagens, planejamento, falas de autoridade do Dr. João, e trechos **sem fala** mostrando o procedimento.
- Tirar: conversa fora do tema (agenda, assuntos pessoais), trechos parados sem ação ("deixa eu segurar"), repetições, final arrastado.
- Tirar falas que atacam colegas ou concorrentes (ex.: "é tudo marketing, todo mundo finge"). Linha vermelha FEA: atacar o sistema, nunca pessoas.
- **Outro lado do rosto**: quando o Dr. João repete o procedimento do outro lado sem falar nada, cortar esse trecho e ir direto para a próxima fala (pedido de 24/09/2026). Vale para qualquer pausa longa sem fala durante a repetição.
- **Início do vídeo**: começa assim que o Dr. começa a falar (cerca de 0,25 s antes da voz). Medir o início da voz no áudio (volume acima de ~42 dB por 0,5 s), não pelo Whisper, que erra o tempo da primeira palavra depois de silêncio (pedido de 24/09/2026).
- **Ponto de corte exato**: o script encaixa cada corte no respiro entre palavras medido no áudio (`encaixar_cortes`; o tempo das palavras da transcrição erra até 0,3 s e não é usado), para não pegar o início de outra palavra ("básico bem feito" do vídeo 10).
- **Final do vídeo**: nunca terminar com frase ou palavra cortada, nem com cara de que falta algo ("vamos lá", "agora a gente vai para..." sem concluir). Se ele não conclui a frase, o vídeo acaba na última frase completa antes dela.
- **Espelho**: cortar quando o Dr. pede o espelho ("espelhinho para ela ver") e a paciente se olha, a não ser que ele esteja explicando algo técnico.
- **"Fecha o olho/olhinho"**: cortar o pedido para a paciente fechar os olhos.
- **Conversa de fundo** (outras pessoas, não o Dr.): cortar; se estiver no meio do procedimento e não der para cortar, silenciar o áudio daquele trecho.
- **Conversa pessoal ou histórico da paciente** (ex.: "fez cirurgia há pouco tempo? não"), queixa de dor fora de contexto técnico, "sou ruim de agulha": cortar.
- **Tudo que dá "errado" sai** (pedido de 24/09/2026): sangramento visível (gota escorrendo, gaze ou cotonete com sangue), agulha que estoura, intercorrência, cara ou gemido de dor, fala ao fundo. Revisar com folha de contato (`fea_folha.sh`: 1 quadro a cada 3 s) e depois 1 quadro por segundo nos trechos suspeitos para achar início e fim. Detecção automática de vermelho não funciona (embalagens vermelhas, gota pequena).
- **Procurando o pertuito**: o tempo em que o Dr. tenta achar o ponto de entrada sai; o vídeo vai direto para o procedimento.
- **Gemido ou expressão de dor da paciente**: cortar ou silenciar (`silenciar` no projeto.json). Se a cara de dor aparecer no meio do procedimento e não der para cortar, dar zoom no ponto tratado para tirar a expressão do quadro (`zoom`: `[inicio, fim, fator, cx, cy]`, cx/cy em fração do quadro). Procurar: interjeições na transcrição (ai, ui, hum), trechos com voz no áudio sem fala transcrita, e conferir o rosto nesses quadros (pedido de 24/09/2026).
- Vídeo que já cabe e é todo clínico fica **inteiro** (respeitando as duas regras acima).
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
9. **Revisão obrigatória**: rodar a skill `fea-revisao-reels` (`python3 FEA-edicao-videos/fea_revisar.py projeto.json --folhas PASTA`) e olhar as folhas de contato. Só entrega com 0 ERRO e cada ATENÇÃO resolvida.
10. **Final**: aplicar as correções, rodar sem `--previa` (qualidade total) e subir para a pasta de destino.

## Pontos para sempre levar à Keila antes de finalizar

- Marcas faladas (ácido hialurônico, toxina, bioestimulador, distribuidoras). Ela aprovou manter nos lotes de setembro, mas confirmar grafia. Confirmadas: Neuramis Volume, Revanesse Kiss, Neauvia Stimulate, Yvoire Contour, Letybo, Seryntox, Vietri.
- Afirmações absolutas de resultado ou segurança ("zero intercorrência, zero necrose"): recomendar cortar por compliance CFM/CFO; a decisão é dela.
- Recomendação comercial (ex.: distribuidora): perguntar se é parceria.
- Nome de paciente falado ou legendado: confirmar grafia.
- Quantidade de vídeos diferente da quantidade de títulos na imagem.

## Correções de texto

Notação técnica (pedido da Keila, 24/09/2026): cânula se escreve **calibre x comprimento** ("2270", "22 70" ou "24-70" viram `22x70`, `24x70`); "G linha" vira `G'` e "G duas linhas" vira `G''`. Quando o Dr. fala "prédio" (a transcrição ouve assim), é **pré-jowl** (pedido de 25/09/2026). "Entre os prés" nas anestesias é pré-molar e fica como está.

`CORRECOES` em `fea_editar_video.py` aplica a regra FEA (nunca "pra", sempre "para") e termos técnicos (carpule, têmpora, interfascial, hidroxiapatita, tecidual, sulco nasolabial, tan delta, mL...). Toda grafia nova confirmada pela Keila entra ali e, se for nome próprio, em `NOMES_PROPRIOS`. Conferir na tela do vídeo (caixa do produto) quando houver dúvida de marca.

## Entrega e limites conhecidos

- `SendUserFile` aceita no máximo **30 MB** por arquivo. Para a Keila guardar no computador: **H.264** 1080p abaixo de 30 MB, em 2 passadas (`libx264 -preset medium -pass 1/2`, bitrate de vídeo = 27,5 MB x 8 / duração, menos 96 kbps do áudio AAC). **Nunca HEVC/H.265**: no computador dela o vídeo abre com tela preta e só áudio (aconteceu em 24/09/2026).
- A conexão do Drive não sobe vídeos grandes. Caminho definitivo: conta de serviço `fea-upload-69@fea-edicao-videos.iam.gserviceaccount.com` (projeto Google Cloud FEA-edicao-videos), com Editor na pasta Setembro. **Bloqueio em 24/09/2026**: política `iam.disableServiceAccountKeyCreation` impede gerar a chave JSON; o administrador do Workspace precisa criar exceção só para o projeto. Com a chave, subir pela API do Drive (`supportsAllDrives=true`, upload resumable), guardando a chave em `.env` fora do git.
- A máquina é temporária: vídeos só na nuvem se perdem se a sessão ficar parada. Scripts e projeto.json ficam no git.

## Armadilhas

- Nunca `pkill -f fea_editar_video.py`: mata o próprio shell que contém o texto. Usar o PID do processo.
- **Palavra solta na legenda sem o Dr. falar** (pedido de 24/09/2026): o script confere cada palavra no áudio (`ancorar_na_voz`): sem voz no tempo da palavra, ela sai; palavra esticada fica só no trecho com voz; palavra de ligação sozinha na tela ("e", "o", "para") não aparece. Conferir depois medindo a voz durante cada legenda (meta: nenhuma com menos de 35% de voz).
- Transcrição sem VAD inventa "tchau"/"obrigado" em trechos silenciosos. Com VAD, palavras podem ficar "esticadas"; o script já limita a 1,2 s e quebra a legenda no início de cada frase.
- Renderizar leva cerca de 1 min por minuto de vídeo nesta máquina (4 CPUs). Avisar a Keila do tempo estimado e usar tarefas em segundo plano.
- Os 8 vídeos do lote "20- Full face 4mL" estão encerrados: não editar mais (pedido da Keila em 23/09/2026).
