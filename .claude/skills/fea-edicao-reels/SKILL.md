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

**Títulos inventados (quando não há imagem de títulos):** nunca colocar nome de produto na headline (ex.: "mento feminino com Volumax" errado; "mento feminino" certo). Exceção: se a headline já veio pronta na imagem de títulos, manter como está (pedido da Keila, 02/10/2026).

**Atenção à ordem (pedido da Keila, 26/09/2026):** a imagem de títulos às vezes está na **ordem de postagem**, e não na ordem dos arquivos. Nunca casar título e vídeo só pela posição. Para cada vídeo, ler a transcrição (o que o Dr. fala e faz) e escolher o título que descreve aquele conteúdo. Montar uma tabela `arquivo -> título -> motivo (frase do Dr. que confirma)` e conferir que cada título foi usado uma vez só. A numeração da saída (`1-`, `2-`...) segue a ordem da imagem, a de postagem. Vídeos sem título correspondente, ou títulos sem vídeo, vão para a Keila decidir antes de renderizar.

## Padrão visual (não mudar sem pedido)

| Item | Valor |
|---|---|
| Formato | 1080x1920, 30 fps, H.264, áudio original (sem trilha, sem normalizar) |
| Título | Montserrat **ExtraBold 116** (tamanho ASS), branco, contorno preto sólido 4 px + sombra 1 px, centro exato do quadro, **2 linhas equilibradas** sempre que passar de 14 caracteres (até ~22 por linha; 3 linhas só se não couber), **entrelinha 0,78** (linhas bem próximas). Medido em pixels na referência da Keila em 24/09/2026: a linha mais longa ocupa ~2/3 da largura. Nos **3 primeiros segundos** |
| Legenda | Montserrat **Bold 56 px**, branca, contorno preto 3,5 px, centralizada a ~80% da altura, 1 a 2 linhas de até 22 caracteres (cada linha ocupa ~1/3 da largura), entrelinha 0,80 (medida na referência da Keila), começa minúscula, sem ponto final, **sem a interjeição "ó"**. **Só entra depois que o título sai**. Ajustada em 24/09/2026: a de 36 px ficou pequena demais. **Legendar toda fala audível, incluindo a do paciente** quando o Dr. pergunta e o paciente responde (ex.: "como ficou a anestesia?", paciente: "não senti nada"). Não pular a resposta do paciente (Keila, 02/10/2026) |
| Sem CTA autoral | não colocar chamada de imersão criada pela edição (padrão desde 16/09). Quando houver CTA de campanha (ex.: `blackfriday_cta.mp4`), ele é concatenado ao final pelo `fea_render_com_cta.py` |
| **Limite de 3 min inclui CTA** | a duração total do vídeo final (conteúdo + CTA concatenado) **não pode passar de 3 minutos** (180 s). Como o CTA tem ~60 s, o conteúdo editado deve caber em ~120 s. Se não couber, dividir em Parte 1/Parte 2 (pedido da Keila, 02/10/2026) |
| Parte 1/2 | se, depois de cortar, o conteúdo + CTA passar de 3 min: dividir; título igual com "Parte 1"/"Parte 2" embaixo; nos 3 s finais da Parte 1, cartela "Parte 2 no perfil" no estilo do título (`parte` e `cartela_final` no projeto.json). Cada parte + CTA ≤ 3 min |

## Regras de corte (critério da editora da equipe)

- **Limite: 3 minutos no total (conteúdo + CTA).** Cortar o máximo necessário para caber. Como o CTA de campanha tem ~60 s, o conteúdo editado deve ter no máximo ~120 s. Se não couber, dividir em Parte 1/Parte 2 (Keila, 02/10/2026).
- Manter: explicação clínica, técnica, dosagens, planejamento, falas de autoridade do Dr. João, e trechos **sem fala** mostrando o procedimento.
- Tirar: conversa fora do tema (agenda, assuntos pessoais), trechos parados sem ação ("deixa eu segurar"), repetições, final arrastado.
- Tirar falas que atacam colegas ou concorrentes (ex.: "é tudo marketing, todo mundo finge"). Linha vermelha FEA: atacar o sistema, nunca pessoas.
- **Deixar o Dr. mostrar a técnica (regra principal, Keila 26/09/2026):** só cortar quando o Dr. **não está fazendo nada** (parado, esperando, limpando longamente, conversando fora do tema). Procedimento acontecendo, com cânula ou agulha trabalhando, marcação sendo feita ou resultado sendo mostrado, **fica, mesmo sem fala**. Silêncio não é motivo de corte: olhar os quadros antes de cortar qualquer pausa. Vídeo picotado ou curto demais foi reprovado nos casos "4mL e bio" (olheiras, labial, bioestimulador, bigode chinês).
- **Outro lado do rosto**: se o Dr. repete o procedimento do outro lado, a repetição mostra técnica e fica. Só encurtar se passar de 3 min e o trecho for idêntico ao primeiro lado.
- **Início do vídeo**: começa assim que o Dr. começa a falar (cerca de 0,25 s antes da voz). Medir o início da voz no áudio (volume acima de ~42 dB por 0,5 s), não pelo Whisper, que erra o tempo da primeira palavra depois de silêncio (pedido de 24/09/2026).
- **Ponto de corte exato**: o script encaixa cada corte no respiro entre palavras medido no áudio (`encaixar_cortes`; o tempo das palavras da transcrição erra até 0,3 s e não é usado), para não pegar o início de outra palavra ("básico bem feito" do vídeo 10).
- **Final do vídeo**: nunca terminar com frase ou palavra cortada, nem com cara de que falta algo ("vamos lá", "agora a gente vai para..." sem concluir). Se ele não conclui a frase, o vídeo acaba na última frase completa antes dela.
- **Espelho**: cortar quando o Dr. pede o espelho ("espelhinho para ela ver") e a paciente se olha, a não ser que ele esteja explicando algo técnico.
- **"Fecha o olho/olhinho"**: cortar o pedido para a paciente fechar os olhos.
- **Conversa de fundo** (outras pessoas, não o Dr.): cortar; se estiver no meio do procedimento e não der para cortar, silenciar o áudio daquele trecho.
- **Conversa pessoal ou histórico da paciente** (ex.: "fez cirurgia há pouco tempo? não"), queixa de dor fora de contexto técnico, "sou ruim de agulha": cortar.
- **Nunca cortar no meio de uma frase do Dr.**, nem para tirar sangue: o corte espera a frase terminar.
- **Tudo que dá "errado" sai** (pedido de 24/09/2026): sangramento visível (gota escorrendo, gaze ou cotonete com sangue), agulha que estoura, intercorrência, cara ou gemido de dor, fala ao fundo. Revisar com folha de contato (`fea_folha.sh`: 1 quadro a cada 3 s) e depois 1 quadro por segundo nos trechos suspeitos para achar início e fim. Gotinha ou pequeno filete no ponto da picada **fica**; só sai o sangue que escorre de verdade (pinga, desce pelo lábio ou queixo). Detecção automática de vermelho não funciona (embalagens vermelhas, gota pequena).
- **Procurando o pertuito**: o tempo em que o Dr. tenta achar o ponto de entrada sai; o vídeo vai direto para o procedimento.
- **Gemido ou expressão de dor da paciente**: cortar ou silenciar (`silenciar` no projeto.json). Se a cara de dor aparecer no meio do procedimento e não der para cortar, dar zoom no ponto tratado para tirar a expressão do quadro (`zoom`: `[inicio, fim, fator, cx, cy]`, cx/cy em fração do quadro). Procurar: interjeições na transcrição (ai, ui, hum), trechos com voz no áudio sem fala transcrita, e conferir o rosto nesses quadros (pedido de 24/09/2026).
- Vídeo que já cabe e é todo clínico fica **inteiro** (respeitando as duas regras acima).
- Se existir edição anterior **do mesmo material**, reproduzir os cortes dela por alinhamento de quadros (ver abaixo). Sempre conferir que é o mesmo paciente antes.

## Fluxo

1. **Ambiente**: `bash FEA-edicao-videos/fea_preparar_ambiente.sh <scratchpad>`. Se faltar rede, pedir à Keila para liberar os domínios listados no topo do script (menu do ambiente > Edit > Network access).
2. **Acesso aos vídeos**: `python3 FEA-edicao-videos/fea_drive.py baixar PASTA_ID destino/` baixa a pasta inteira pela API (acesso das variáveis do ambiente, sem abrir link público), retomando se a conexão cair e conferindo o tamanho (a conexão às vezes fechava sem erro e o .MOV vinha truncado, "moov atom not found"). `fea_drive.py listar PASTA_ID` mostra id, nome, tamanho e duração.
3. **Áudio e transcrição**: extrair WAV mono 16 kHz com o FFmpeg de `env.sh` e rodar `python3 FEA-edicao-videos/fea_transcrever.py tr/ wav/*.wav` (roda em segundo plano). O script faz 3 passadas (02/10/2026): (a) Whisper com VAD; (b) **refino**: segmento longo (> 15 s) é retranscrito em pedaços cortados nos silêncios, porque o tempo das palavras vinha esticado e a legenda saía até 9 s atrasada em vídeo de toxina com fala esparsa; (c) **complemento**: cada buraco entre palavras em que o áudio tem voz é transcrito de novo sem VAD, porque o VAD pulava fala baixa (o "4, 5, 6" de "pertuito 1, 2, 3, 4, 5, 6" e o "Ótimo" baixinho da paciente). Para refazer só (b) e (c) num JSON existente: `--complementar`.
4. **Mesmo material já editado?** Comparar quadros (miniaturas 27x48 em cinza a 5 fps, correlação normalizada). Correlação ~0,99 = mesmo material: mapear offset quadro a quadro a 30 fps e extrair os trechos `manter`. Zero correspondência = outro paciente, decidir os cortes pela transcrição.
5. **Cortes**: ler a transcrição com tempos, escolher `manter` (segundos do bruto) cortando em pausas entre palavras. Marcar em `remover_legenda` trechos em que a transcrição inventou fala sobre silêncio (ou palavra repetida pelo complemento). Para recuperar os cortes de uma edição já entregue: `python3 FEA-edicao-videos/fea_alinhar.py FFMPEG editado.mp4 brutos... --cta 59.55`.
   - **Começo**: o vídeo começa na primeira fala do bruto, mesmo que a frase repita o título (a fala dos 3 s do título fica sem legenda, padrão). Começar no meio de frase ("...na lista de preenchedores") é erro.
   - **Para caber em ~120 s de conteúdo** (sem picotar a técnica), o que sai primeiro: conversa comercial (preço, "presente", "vale por duas seringas"), comparação com outra marca, propaganda de curso no meio do caso, repetição/resumo final do que já foi explicado, chamada final ("agora a gente vai para...", "vocês vão acompanhar..."), conversa pessoal. Se ainda passar, Parte 1/Parte 2.
   - **Parte 1/Parte 2**: mesmo número no nome (`6- Título Parte 1.mp4`, `6- Título Parte 2.mp4`), para não renumerar o resto da pasta nem descasar da imagem de títulos. A legenda continua por baixo da cartela "Parte 2 no perfil".
6. **projeto.json** (ver o docstring de `fea_editar_video.py`): `entrada`, `transcricao`, `saida`, `titulo`, `titulo_origem` (`"imagem"` = veio da imagem de títulos e sai exato; `"inventado"` = sem imagem, nunca com nome de produto), `parte`, `cartela_final`, `manter`, `remover_legenda`, `correcoes` (regex extras do lote). Antes do render, `python3 fea_editar_video.py projeto.json --so-legenda` gera só o .ass para ler todas as legendas (rápido).
   - **Título da imagem sai exato**, inclusive com "?" e ":" (nunca "Técn." ou "Result."); se não couber em 3 linhas de ~22 caracteres, vai em 4 linhas com fonte 100.
   - **Headline longa demais** (mais de ~45 caracteres, 4 linhas na tela) incomoda a Keila (03/10/2026: "a headline está muito grande"). Não abreviar por conta própria: levar a ela uma versão curta para aprovar. Exemplo aprovado: "Como fica o resultado da toxina para não deixar a ruga do Wi-Fi sem perder arqueamento?" virou "Toxina para ruga do Wi-Fi sem perder o arqueamento".
7. **Render final**: `python3 fea_render_com_cta.py projeto.json CTA.mp4` (H.264 1080p qualidade total + CTA). Conferir visualmente um mosaico de quadros (título aos 1,5 s e legenda aos ~12 s de cada vídeo) antes de subir.
8. **Revisão da Keila**: ela revisa direto na pasta de destino do Drive. Pontos para ela decidir vão no resumo final da conversa, sem travar a entrega.
9. **Revisão obrigatória**: rodar a skill `fea-revisao-reels` (`python3 FEA-edicao-videos/fea_revisar.py projeto.json --folhas PASTA`) e olhar as folhas de contato. Só entrega com 0 ERRO e cada ATENÇÃO resolvida.
10. **Final**: aplicar as correções, rodar `fea_render_com_cta.py` (qualidade total) e subir com `fea_drive.py upload` para a pasta de destino.
11. **Planilha de controle de edições** (obrigatório, Keila 02/10/2026): atualizar a planilha `1RYzwrbbCFZCTVZ-pJosMhDpwNdSDLoFEZVHpIQjWzNQ` na aba EDIÇÕES com:
    - **Link da pasta de brutos** (não só o nome, o link clicável `https://drive.google.com/drive/folders/ID`)
    - **Link da pasta do vídeo editado** (link clicável da pasta de destino)
    - Quantidade de vídeos e nome da pasta
    - A planilha vai para quem posta nas redes sociais: sem link, a pessoa não acha os vídeos
    - Se a numeração de pastas ficou com buraco (ex.: 1, 2, 4 sem o 3), renomear para ficar sequencial ao criar a próxima pasta, ou criar a pasta com o número faltante

## Pontos para sempre levar à Keila antes de finalizar

- Marcas faladas (ácido hialurônico, toxina, bioestimulador, distribuidoras). Ela aprovou manter nos lotes de setembro, mas confirmar grafia. Confirmadas: Neuramis Volume, Revanesse Kiss, Neauvia Stimulate, Yvoire Contour, Letybo, Seryntox, Vietri.
- Afirmações absolutas de resultado ou segurança ("zero intercorrência, zero necrose"): recomendar cortar por compliance CFM/CFO; a decisão é dela.
- Recomendação comercial (ex.: distribuidora): perguntar se é parceria.
- Nome de paciente falado ou legendado: confirmar grafia.
- Quantidade de vídeos diferente da quantidade de títulos na imagem.

## Correções de texto

**Nome de produto: sempre pesquisar a grafia oficial** (site do fabricante ou distribuidor) antes de legendar, e adicionar em `CORRECOES`. Confirmados: Biofils (fios), Kirialys (Pharmaesthetics), Restylane Volyme (Galderma), Perfectha Subskin, Neauvia Intense e Stimulate, Yvoire Contour, Neuramis, Revanesse, Letybo, Seryntox. Termos: ácido hialurônico, bolus.

Grafias fixas (Keila, 26/09/2026): **Neauvia** (nunca Nuvia), **tear trough**, **1%** e **0,2** (número inteiro na legenda, o script junta "0" + ",2"). Legenda nunca tira palavra no meio da fala (só a palavra solta inventada no silêncio), para ficar sincronizada com o áudio.

Grafias fixas (Keila, 02/10/2026): **pertuito** (nunca "hipertuito"), **picadinha** (nunca "picadinho"/"ficadinha"), **anestesia** (nunca "parestesia" quando o contexto é a anestesia em si: "como foi a parestesia?"; Whisper confunde), **desse mento** (duas palavras, nunca "descimento" junto). Quando o Dr. enumera algo (ex.: "pertuito 1, 2, 3, 4, 5, 6"), legendar **todos os números**, não parar na metade; número por extenso no meio de lista com algarismo vira algarismo ("1, 2, 3, 4, 5, 6").

**Atenção, parestesia:** "sem nenhum paciente com parestesia" é o termo médico certo (complicação neural). A troca automática para "anestesia" deixava a frase sem sentido, então ela só vale no contexto "como foi/ficou a parestesia"; nos outros casos, conferir no áudio e levar para a Keila.

Grafias do lote de outubro (02/10/2026): Letybo (nunca Letibol/Letibô/Letipo/Letibon; "letibona" = "Letybo na"), corrugador, pré-jowl e jowl (nunca "pre-joy", "jaw"), buldoguinho, Perfectha Subskin (nunca "Afecta"), Yvoire (nunca "Ivoar"), Biogelis Volumax (Pharmaesthetics), alto G' (nunca "autogelinha"), ácido hialurônico (nunca "acilurônico"/"acelerônico"), 20 mg (com espaço), Wi-Fi, Nefertiti, ptose (nunca "hiptose"/"pitose"), Dysport (nunca "dispor"), DAO (nunca "dow"), médio-pupilar (nunca "M-pupilar"), "fica arqueado" (o Whisper ouve "hackeado").

Marca de fios (Keila, 03/10/2026): **Biofils** (nunca "biofios", "bio fios" ou "biofil"; o Whisper ouve "biofios").

**Legenda e diálogo** (02/10/2026): pergunta do Dr. e resposta do paciente nunca no mesmo bloco ("doeu?" / "não, nem um pouquinho"); fala de uma palavra que é a frase inteira ("Não.", "Ótimo.") fica sozinha na tela. Começo de frase no meio de um bloco ganha vírgula e minúscula. Vírgula antes de "tá"/"viu" só no fim da frase ("a minha agulha tá de cima" não leva vírgula), e nunca depois de palavra de ligação ("acho que aí eu vou").

Notação técnica (pedido da Keila, 24/09/2026): cânula se escreve **calibre x comprimento** ("2270", "22 70" ou "24-70" viram `22x70`, `24x70`); "G linha" vira `G'` e "G duas linhas" vira `G''`. Quando o Dr. fala "prédio" (a transcrição ouve assim), é **pré-jowl** (pedido de 25/09/2026). "Entre os prés" nas anestesias é pré-molar e fica como está.

`CORRECOES` em `fea_editar_video.py` aplica a regra FEA (nunca "pra", sempre "para") e termos técnicos (carpule, têmpora, interfascial, hidroxiapatita, tecidual, sulco nasolabial, tan delta, mL...). Toda grafia nova confirmada pela Keila entra ali e, se for nome próprio, em `NOMES_PROPRIOS`. Conferir na tela do vídeo (caixa do produto) quando houver dúvida de marca.

## Entrega e limites conhecidos

- **Qualidade total, sem limite de tamanho** (Keila, 02/10/2026: "não é para limitar, quero qualidade"). `--entrega` gera H.264 CRF 18, áudio AAC 192k 48 kHz, e o CTA entra por stream copy, sem recompressão. Nunca voltar a mirar 30 MB nem 2 passadas por bitrate. **Nunca HEVC/H.265**: no computador dela o vídeo abre com tela preta e só áudio (24/09/2026).
- **Nunca entregar vídeo pelo chat** (`SendUserFile`): a entrega é sempre direto na pasta de destino do Drive.
- **CTA Black Friday** (válido até 09/10/2026): todo vídeo editado termina com o CTA (`1FKH9yu_5Dyz31hmeSKIgyu-WzHcR2Nn8` no Drive, ~60 s). Renderizar com `python3 FEA-edicao-videos/fea_render_com_cta.py projeto.json CTA.mp4`.
- **Limite de 3 min é do vídeo final, com o CTA** (Keila, 02/10/2026). Com CTA de ~60 s, o conteúdo fica em até ~120 s. O script acusa ERRO se passar.
- **Upload, pasta e renomear**: `python3 FEA-edicao-videos/fea_drive.py upload PASTA_ID arquivos... [--substituir]`, `pasta PAI_ID "nome"`, `renomear ID "OK. nome"`, `testar`. Chaves só nas variáveis do ambiente (`FEA_GDRIVE_CLIENT_ID`, `FEA_GDRIVE_CLIENT_SECRET`, `FEA_GDRIVE_REFRESH_TOKEN`), nunca no código nem no git. Se `testar` falhar ou não mostrar Drive inteiro e Sheets, rodar `bash FEA-edicao-videos/fea_setup_google_oauth.sh` (link para a Keila autorizar uma vez).
- Permissões do Drive e dos scripts ficam em `.claude/settings.json` (no git), então valem em toda conversa nova sem pedir confirmação.
- A máquina é temporária: vídeos só na nuvem se perdem se a sessão ficar parada. Scripts e projeto.json ficam no git.

## Autonomia total no Drive (Keila, 02/10/2026)

Autorização total para mexer no Drive sem perguntar: criar pasta, baixar vídeo, subir vídeo, renomear pasta. Não perguntar nada. Executar direto. A Keila não vai aceitar perguntas sobre permissão de Drive.

## Planilha de controle de edições

Planilha `1RYzwrbbCFZCTVZ-pJosMhDpwNdSDLoFEZVHpIQjWzNQ`, aba EDIÇÕES. Atualizar após cada caso clínico com:
- **Link da pasta de brutos** (clicável: `https://drive.google.com/drive/folders/ID_DA_PASTA`)
- **Link da pasta do vídeo editado** (clicável)
- Quantidade de vídeos e nome da pasta
- Se uma pasta de destino for excluída e deixar buraco na numeração (ex.: 1, 2, 4), renumerar ao criar a próxima pasta para ficar sequencial

Atualizar com `python3 FEA-edicao-videos/fea_atualizar_planilha.py append ...` (mesmas chaves do Drive, escopo `spreadsheets`). Links sempre clicáveis: a planilha vai para quem posta nas redes.

## Anúncio LATAM em espanhol (Keila, 05/10/2026)

Pasta de criativos MTB LATAM: `19tGHEnoBC9-8DGSbvjE7GJTFCBiRHCsn`, nome `Ads NN - MTB LATAM` (próximo número livre).
1. Traduzir o bruto no HeyGen (upload do arquivo como asset; link do YouTube com restrição de idade falha) em **Spanish (Latin America)**, o mesmo dos criativos LATAM anteriores. O resultado sai a 25 fps em `https://resource2.heygen.ai/video_translate/{id}/original.mp4`.
2. Transcrever com `fea_transcrever.py --idioma es` e pôr `"idioma": "es"` no projeto.json (desliga as correções do português, que estragam o espanhol).
3. Cortar a chamada final em português para a FEB/comentário: o CTA do anúncio é o vídeo da Masterclass (ex.: `Ads 76 - MTB LATAM`, 26 s), convertido para H.264 30 fps AAC 48 kHz antes do `fea_render_com_cta.py`.
4. Headline em espanhol, sem nome de produto. A HeyGen às vezes inventa palavra (ex.: "Relájate, Capi"): tirar da legenda em `correcoes` e silenciar no `silenciar` (a revisora acusa "voz falhando" nesse ponto, é esperado).

## Armadilhas

- Nunca `pkill -f`/`pgrep -f` com o nome do script dentro do mesmo comando: casa com o próprio shell e mata a sessão. Pegar o PID com `ps -eo pid,args` e dar `kill PID`.
- **Voz falhando/picotando** (pasta 7 de outubro, vídeo 1): a edição entregue era um trecho único do bruto, sem corte nem silenciar, e a medição (janelas de 5 ms) não achou queda de volume, silêncio digital nem clipping em relação ao bruto. O vídeo foi refeito do bruto, em 1 trecho, e a revisora ganhou a checagem "voz falhando" (volume do final x bruto, com alinhamento fino de ±4 quadros, para não confundir deslocamento de 50 ms com falha). Se a Keila ainda ouvir a falha, pedir o segundo exato.
- **Palavra solta na legenda sem o Dr. falar** (pedido de 24/09/2026): o script confere cada palavra no áudio (`ancorar_na_voz`): sem voz no tempo da palavra, ela sai; palavra esticada fica só no trecho com voz; palavra de ligação sozinha na tela ("e", "o", "para") não aparece. Conferir depois medindo a voz durante cada legenda (meta: nenhuma com menos de 35% de voz).
- Transcrição sem VAD inventa "tchau"/"obrigado" em trechos silenciosos. Com VAD, palavras podem ficar "esticadas"; o script já limita a 1,2 s e quebra a legenda no início de cada frase.
- Renderizar leva cerca de 1 min por minuto de vídeo nesta máquina (4 CPUs). Avisar a Keila do tempo estimado e usar tarefas em segundo plano.
- Os 8 vídeos do lote "20- Full face 4mL" estão encerrados: não editar mais (pedido da Keila em 23/09/2026).
