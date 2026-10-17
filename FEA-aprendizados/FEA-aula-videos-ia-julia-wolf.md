# FEA: aprendizados da aula "Como começar a fazer vídeos com IA do zero" (Júlia Wolf Cruz)

- **Fonte:** live da Júlia Wolf Cruz (agência Prospe, programa Amplia), YouTube `MiCFi_lGY-Q`, 65 min. Cópia do vídeo na pasta do Drive `1EyY4BwcSQcfLwsmFFHTU3_3wamY-swuS`.
- **Assistido por:** Claude, em 17/10/2026, com transcrição completa (Whisper) e leitura dos quadros de tela do mapa mental da aula.
- **Skill que aplica este conteúdo:** `.claude/skills/fea-videos-ia/SKILL.md`.

A aula mostra três fluxos de vídeo com IA usados na operação dela: **edição** de vídeo gravado, **criação 100% IA** (sem gravar nada) e **clone** de especialista. Cerca de 45 minutos são de conteúdo; o restante é venda do desafio dela e conversa com o chat.

## 1. Edição de vídeo gravado (6 etapas)

**Ferramentas, todas plugadas no Claude ou no ChatGPT (sem custo extra além da assinatura da IA):**

| Ferramenta | Função |
|---|---|
| Claude (Opus) ou ChatGPT | Lê o bruto, decide cortes, legenda e monta a estratégia geral da edição |
| Remotion | Coloca texto, imagem, B-roll e tela dividida por cima do vídeo (biblioteca gratuita que gera vídeo a partir de código) |
| FFmpeg | Corta e junta os trechos |
| Whisper | Transcreve palavra por palavra, com tempo de cada palavra |
| yt-dlp | Baixa o vídeo de referência do YouTube |

**Etapas:**

1. **Ferramenta:** configurar o conjunto acima uma vez.
2. **Referência:** a IA assiste a um vídeo que serve de modelo e extrai ritmo, velocidade, respiro entre falas, se corta a palavra até o fim ou antes, presença de texto e imagem sobre a tela, trilha sonora e filtro de cor. Isso vira um **arquivo salvo** que a IA relê em toda edição, sem precisar explicar de novo.
3. **Bruto:** transcrever e mapear o que entra. Não é só tirar palavra repetida: a IA precisa perceber quando um raciocínio foi abandonado no meio e recomeçado (descartar a primeira tentativa inteira) e quando a ordem das falas pode ser trocada para ficar mais clara.
4. **Emoção de cada trecho:** para cada parte, o que está sendo feito com a pessoa, o que ela precisa sentir para o próximo trecho funcionar e que tipo de elemento entrega isso (texto, imagem, matéria de jornal, dado de mercado). Vídeo de rede social pode não ter elemento nenhum; VSL (vídeo de vendas da página) pede muito mais B-roll e prova.
5. **Montagem:** cortar, legendar e inserir os elementos escolhidos.
6. **Revisão humana:** legenda certa? tempo dos cortes nas falas certo?

Ela organiza isso em um "funcionário de IA" chamado Tarantino, com mais de 30 skills, e nomeia os agentes por função (Clarice para texto, outro para clone).

## 2. Criação 100% IA (7 etapas)

Princípio central da aula: **o dinheiro se perde na geração, não na ideação.** Ideia mal amarrada gasta créditos à toa e gera vídeo bonito que não conta história. A diferença entre a versão feita sem ideação e a refeita com o processo completo foi, nas palavras dela, "muito grande".

1. **Ideia (checklist antes de gerar qualquer coisa):** com quem vou falar? para qual mídia? sensação desejada? o que vai quebrar o padrão do feed? sobre o que a história realmente é? quem é o protagonista? há outros personagens? quais ambientes? há objetos de destaque? qual a jornada, o arco narrativo? há referências visuais? Sites de referência citados: FrameSet, Film Grab e um terceiro de busca por imagem semelhante (o nome não ficou claro no áudio).
2. **Roteiro:**
   - Especificações: onde publica, pessoa real ou criada por IA, tem narração? **Se tem narração, gravar o áudio antes**, porque ele define o tempo de cada cena (evita gerar 10 s quando a cena precisa de 5). Sem narração, o tempo se resolve na edição.
   - Quebrar em cenas: corta quando muda o lugar, o momento, quem está no quadro ou a ação principal.
   - Definir cada cena: lugar, dia ou noite, quem está, o que faz, roupa, estado, quem está ao redor.
3. **Visual:** luz (frontal, natural de janela, lado), cor (dominantes, de apoio, temperatura, contraste), lente e profundidade de campo, composição, movimento de câmera (tripé, mão, acompanhando), energia, textura (granulado, nitidez), cenário, pessoa. A IA extrai tudo isso da referência.
4. **Assets (elementos gerados antes do vídeo):** ambiente vazio, character sheet (ficha do personagem em vários ângulos), objetos que se repetem (sacola, abajur, bloco de notas) e, por fim, a base composta (personagem dentro do ambiente com os objetos). Tudo salvo como arquivos soltos numa pasta que a IA lê a cada geração, com subpasta de aprovados. É isso que mantém a consistência.
5. **Plano por cena:** imagem de começo, imagem de fim e movimento de câmera de cada cena.
6. **Prompts:** a IA escreve os prompts de animação a partir da ideia, das imagens e do plano. Ferramenta usada: **Higgsfield** (tem um "Super Computer" que ajuda a montar prompts, gasta mais crédito).
7. **Iteração:** analisar o que foi gerado, corrigir o que perdeu continuidade (mão trocada, esmalte que some, cadarço errado), juntar. **Trilha sonora só no final**; na geração, pedir apenas efeitos sonoros.

## 3. Clone de especialista (6 etapas)

Ferramentas: **HeyGen** para o avatar em vídeo, **ElevenLabs** para a voz (ela prefere o clone de voz do ElevenLabs ao do próprio HeyGen, por naturalidade). O Claude opera o ElevenLabs direto.

1. Character sheet da pessoa (frente, lado, ângulos).
2. Fotos da pessoa em vários ambientes que viram cenário dos vídeos (aeroporto, cozinha, sala, carro).
3. Áudio: juntar material bruto com a voz real e clonar.
4. Criação do personagem no HeyGen (sobe áudio, vídeos e assets).
5. Roteiro com regras de fala para voz sintética:
   - pedir para a IA ler a documentação atualizada da plataforma antes de escrever;
   - cada sinal de pontuação muda a fala;
   - números sempre por extenso;
   - quebra de linha onde a pessoa respira;
   - palavra em inglês e sigla: corrigir a pronúncia na escrita;
   - direção de voz: uma instrução por bloco.
6. Geração: ouvir o áudio antes de gerar o vídeo, depois ajustar.

**Limitação atual, segundo ela:** boca e dentes ficam estranhos em fala longa (criativos de 40 s ou mais). Ela mesma quase não usa clone hoje; "dá para quebrar um galho".

## 4. Princípios transversais

- **Cérebro do negócio portátil:** pastas com instruções, agentes e skills que funcionam no Claude e no ChatGPT, com backup no Drive. Não ficar refém de uma ferramenta. (É exatamente o modelo deste repositório: `CLAUDE.md` + skills `fea-`.)
- **Design System por projeto e por lançamento:** logo, cores, tipografia, comportamento da marca em um arquivo `.md` e um `.html` que a IA lê antes de criar qualquer peça visual. Pode haver um por lançamento e um para orgânico e outro para pago. O mesmo vale para vídeo (padrão de edição de VSL, de Reels).
- **Margem para refação:** ao orçar vídeo com IA, embutir no preço as gerações que dão errado.
- **Custo declarado por ela:** Claude e ChatGPT no plano Max 20x, Higgsfield em torno de R$ 800 por mês para uso próprio (número dito por ela na live, não verificado).

## 5. Triagem para a FEA

| Item da aula | Situação na FEA | Decisão |
|---|---|---|
| Edição com Claude + FFmpeg + Whisper | **Já existe**: `fea-edicao-reels` faz transcrição em 3 passadas, cortes e legenda no padrão aprovado | Manter. Ganhos possíveis listados abaixo |
| Ficha de referência salva | Padrão visual já salvo em `FEA-padrao-edicao-videos.md`, mas não há ficha de **ritmo** extraída de vídeo de referência | **Adotar** para novos formatos (VSL, aula de masterclass, depoimento) |
| Detectar raciocínio abandonado e reordenar falas | Cortes hoje removem pausas e trechos sem fala | **Adotar como checagem** nos brutos longos do Dr. João; reordenar só com aprovação, porque mexe no conteúdo clínico |
| Emoção de cada trecho e B-roll | Reels de procedimento não usam B-roll | **Adotar em VSL e vídeo de lançamento**, sempre com material real (aula, cadáver com disclaimer, depoimento autorizado) |
| Remotion | Não usado; FFmpeg + legenda ASS resolvem o Reels | Avaliar só se surgir demanda de VSL com muitos elementos sobre a tela |
| Criação 100% IA (Higgsfield) | **Linha vermelha nº 7**: imagem e vídeo médico ou clínico gerado por IA não vão para entregável final | Usar **só para storyboard e mockup interno**. O checklist de ideia, roteiro e visual vale integralmente para briefing de gravação real com Gabriel Napoli e Weslei Sousa |
| Clone do Dr. João (HeyGen + ElevenLabs) | Não existe. HeyGen já é usado para **dublagem** em espanhol | **Não criar sem aprovação expressa da Keila e do Dr. João**: autoridade clínica, compliance CFM/CFO e risco de reputação. As regras de roteiro para voz sintética valem já para qualquer texto enviado ao HeyGen |
| Design System em `.md` + `.html` | Identidade FEP Experience está no `CLAUDE.md`, sem arquivo próprio | **Recomendado**: criar `FEA-design-system.md` e `.html` (paleta, tipografia, componentes, um bloco por produto), resolvendo antes o conflito com a vertente institucional |

Rastreamento de funil: nenhum dos fluxos da aula mede resultado do vídeo. Para VSL e criativos FEA, cada versão precisa de UTM próprio e leitura de retenção por trecho, ligando a "emoção de cada trecho" a dado real de queda de audiência. Sem métrica, otimização é palpite.
