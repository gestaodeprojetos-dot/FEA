---
name: fea-criativos
description: Esteira de criativos de anúncio da FEA (Dr. João Pithon), adaptada do DNA TSA (ACE Criativos, antiga Fábrica de Criativos). Gera ideias com 5 headlines cada, passa por avaliação, aprovação em HTML, produz os três modelos (M4 narrado, M4 sem narração, encenação) em 9:16 e 1:1, confere o arquivo final e entrega pacote aprovado para o tráfego. Usar quando a Keila pedir anúncios novos, criativos, headlines, ideias de anúncio, lote de criativos, M4, encenação, ou ativar a esteira.
---

# FEA: Criativos de anúncio

Missão: produzir propostas e peças aprovadas no método TSA com a identidade FEA (FEP Experience). Fonte integral (DNA TSA, commit 220328a60b, e Inteligência Agêntica, commit a921288064): `references/FEA-fonte-dna-criativos.md`. Ler a seção da etapa antes de executar. Em conflito, a regra mais restritiva vence, e **a linha vermelha FEA vence o DNA TSA**.

## Adaptação obrigatória à FEA (ler antes de tudo)

| Ponto do DNA TSA | Na FEA |
|---|---|
| Foto do M4 e planos da encenação gerados por IA (Antigravity, Higgsfield) | **Proibido em entregável final** (linha vermelha 7). Foto do M4 = foto real do Dr. João (pasta do Drive) ou material gravado pela equipe; peça gráfica com designer (Gabriela Costa ou André Vivas). IA só para mockup interno de planejamento, marcado como tal |
| Encenação com personagem fictício animado | Só como mockup interno. Versão final da encenação usa três planos **gravados** (Gabriel Napoli, Weslei Sousa) ou cortes reais de aula, procedimento autorizado ou bastidor, com movimento contínuo |
| Voz VoiceStudio / ElevenLabs / clone | Narração = voz real do Dr. João ou da equipe médica, gravada. Clone de voz do Dr. João em anúncio só com autorização escrita registrada (DNA-AV-03). Dublagem para espanhol segue a regra HeyGen do CLAUDE.md |
| Trilha ACE Music | Banco com direito comercial comprovado. "Gratuito" não é licença |
| ACE Simulator (gate ≥ 8,0) | Não existe aqui: headlines ficam `SEM_VALIDACAO_SIMULATOR`. Rodar o framework de 10 critérios do CLAUDE.md como avaliação do Claude (nunca chamar de "Simulator"). Veredito FEA: 90+ publica, 80 a 89 com variação B, 60 a 79 reescreve, abaixo de 60 descarta. Aprovação da Keila vem depois dessa avaliação, nunca no lugar dela |
| ACE COPY | Adriane Möbbs. Posso propor headlines; ela revisa quando a Keila pedir. Eu continuo dono do registro do gate |
| Cadu (exceção ao gate) | Keila |
| Entrega para Tráfego | Matheus Saar (The Trinity), via skill `fea-gestor-trafego` |

Material de paciente: vídeos e imagens que a Keila envia já têm autorização. Cadáver fresco em peça pública só com disclaimer. Nunca citar marca de AH ou toxina sem aprovação.

## Entrada

Briefing aprovado, produto, fase do funil, estágio de consciência dominante, público (persona FEA), oferta, objetivo da peça, CTA e destino, quantidade de ideias, referências, histórico de desempenho com período e atribuição, orçamento. Pedir só o que faltar, numa pergunta.

## Etapas

1. **Ler desempenho**: ranking com período, fonte, atribuição. Volume não é eficiência. Correlação não prova causa. Sem transcrição, escrever "incerto".
2. **Propor fichas**: por ideia, 5 headlines, mais virada, apoio, CTA, legenda, narração em frases curtas, destino e hipótese. Um estágio de consciência por peça. Mecanismo único citado (cadáver fresco, Dr. João ao vivo, dupla certificação, comunidade, suporte clínico, trilha). Prova antes do pedido.
3. **Avaliar**: framework de 10 critérios em cada headline. Preservar as aprovadas; refazer as reprovadas **uma única vez**, registrando v1, nota, justificativa, v2. Não mudar público nem critério para subir a nota. Persistindo reprovação, mostrar aprovadas e reprovadas separadas e pedir informação específica.
4. **Primeira aprovação (HTML)**: ideias, headlines com estado, foto piloto, amostra de narração, objetivo, referências, avaliação e limitações. Keila aprova headline a headline. Silêncio, visualização ou download não são aprovação.
5. **Produzir** (sem perguntar quais modelos), para cada headline aprovada:

| Ordem | Código | Modelo |
|---|---|---|
| 1 | M4 | Foto com zoom lento, texto entrando em etapas (manchete, virada, apoio, CTA) no tempo da narração, narração e trilha |
| 2 | M4SN | Mesmo movimento e texto do M4, só trilha |
| 3 | ENC | Três planos com movimento contínuo, um por frase da narração, texto em etapas, narração e trilha |

Cada um em 9:16 (1080x1920) e 1:1 (1080x1080): **seis arquivos por headline**. Recompor, nunca esticar nem usar faixas. Até 15 s é referência; nunca cortar palavra nem acelerar a fala para caber. Montagem com ffmpeg e o pipeline de `FEA-edicao-videos/`.

6. **Conferir o arquivo final**, não o pedido:
   - dimensões, duração, codec H.264, áudio presente;
   - transcrever o áudio final e comparar com o texto aprovado;
   - texto da tela chama para o mesmo destino da narração e da legenda;
   - regras de tela: até 5 palavras visíveis por vez; número só se for falado; logo só o arquivo oficial; nenhum quadro congelado para completar duração (cartela parada intencional registrada como exceção);
   - grafia técnica correta, nunca "pra", sem em-dash; aproveitar os checks da skill `fea-revisao-reels` no que se aplica.
7. **Segunda aprovação (HTML)**: aprovar ou rejeitar cada peça e formato. Rejeitar a encenação não invalida o M4 aprovado. Ajuste que muda a base volta à Keila.
8. **Fechar pacote**: Drive com pastas separadas `FEA-rascunhos/` e `FEA-aprovados/`, HTML e PDF com nomes, headlines, texto principal, legendas, CTA, arquivos, formatos, versões e estados. Só aprovados seguem para o tráfego. Nada é publicado automaticamente.

Estados de cada saída: conceito, texto, prompt, job, arquivo, conferido, aprovado. Prompt não satisfaz gate de mídia; job aceito não prova arquivo; HTML exibido não prova aprovação.

## Gasto

Higgsfield (só para mockup interno) apenas pelo CLI, nunca pela API: `higgsfield account status` e `higgsfield generate cost` antes, prestação de contas no fim por `higgsfield account transactions`. Nunca rodar `higgsfield auth token`. Timeout depois de pedido pago: consultar o job, nunca gerar de novo. Compra, assinatura ou recarga: aprovação item a item da Keila.

## Identidade e nomes

Identidade FEP Experience (roxo `#5B4599`, azul-violeta `#3846BB`, lavanda `#D0D1E9`, Sora + Montserrat). Arquivos `FEA-<produto>-<ideia>-H<n>-<M4|M4SN|ENC>-<9x16|1x1>-v<n>.mp4`.

## Receipt

Tarefa, estado, entrada e versão, ações, ferramentas e modelos efetivos (ou VERSION_UNVERIFIED), artefatos, conferências com resultado, aprovações, custo, pendências, próxima ação e responsável.
