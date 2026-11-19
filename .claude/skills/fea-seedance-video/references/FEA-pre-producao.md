# Pré-produção e pós-produção: o que vem antes e depois do prompt

Fonte: aula "Como criar vídeos realistas e cinematográficos com IA", da Ana Alice (editora da
Craft, autora original desta skill), gravada no Zoom em 23/10/2026, com o PDF da aula. A skill já
cobria a geração do vídeo; esta página cobre os passos 1, 2 e 5 do método dela.

## O método em 5 passos

| Passo | O quê | Onde está nesta skill |
|---|---|---|
| 1. Roteiro | Texto ou áudio dividido em cenas | Esta página |
| 2. Geração de imagens | O kit de cada cena: cenário, personagem, figurino, objetos, pose | Esta página |
| 3. Direção e prompt | Plano, ângulo, lente, movimento; o Claude escreve o prompt | `prompt-template.md`, `frases.md` |
| 4. Geração do vídeo | Testar em Draft, corrigir, aprovar | `estrategia.md`, `troubleshooting.md` |
| 5. Edição | Juntar takes, trilha, legenda, cor | Esta página |

## 1. Roteiro

- Todo vídeo parte de um roteiro ou de um áudio. Pode ser simples (quem entra, o que cada um fala)
  ou já trazer câmera e movimento.
- **Partindo de áudio** (trecho de vídeo do YouTube, narração): transcreva, cole num doc e
  separe por cena antes de pedir prompt. Assim se sabe quantas cenas gerar e o que entra em cada
  uma. Se o usuário mandar o áudio, faça você a transcrição e a divisão e mostre para ele aprovar.
- **Do roteiro à cena:** antes de escrever, pergunte o que torna a fala visível. "Meus olhos!"
  pedia algo que doesse nos olhos: a cachorra de costas alongando. "Essa é a próxima missão"
  pedia sofisticação: escritório de mafioso e só "Próxima missão" escrito no envelope.
- **IA só quando ela resolve algo.** Use quando não há pessoa, cenário ou verba para gravar. Se o
  vídeo real já existe, muitas vezes uma boa edição resolve melhor.
- **A ideia tem que ter a ver com a pessoa.** Referência de trend só funciona se encaixa na
  narrativa do perfil (a cachorra que já aparece no perfil, o formato que combina com a
  personalidade). Se a resposta a "isso tem a ver com ela?" balança, não tem.
- Referência de filme ajuda, mas personagem com direito autoral (Vingadores, por exemplo) não
  pode ser copiado. Sugira o clima, não o personagem.
- O Claude entra como parceiro de ideia (sugerir personagens de filme que combinam com a pessoa),
  não para escrever o roteiro sozinho. O lado humano do roteiro é o que diferencia o vídeo.

## 2. O kit de cada cena (imagens antes do vídeo)

Tudo o que vai aparecer no vídeo vira imagem antes. Cada cena tem um kit: **cenário vazio,
personagem, figurino** e, quando precisa sair exato, **objeto** e **pose**.

### Ferramenta

- Ana usa o **ChatGPT** para imagem. O **Nano Banana** funciona bem para cenário e objeto, mas
  muda o rosto: na comparação da aula, a folha do Nano Banana deixou a pessoa "quase outra" e a
  do ChatGPT saiu "surpreendentemente igual".
- Peça com todos os detalhes desde a primeira mensagem (fundo, luz, idade, estilo). Quando a
  imagem começa a ficar falsa depois de várias correções, **recomece a conversa** com o pedido
  completo em vez de seguir corrigindo: na aula, o recomeço deu certo de primeira.

### Cenário

- Parta de uma referência (Pinterest, print de outro vídeo) e peça a versão própria: ampliar o
  enquadramento, tirar o móvel que não serve, acrescentar o que a cena precisa, de frente e **sem
  ninguém**.
- Peça o formato certo já na imagem (9:16 vertical ou 16:9 horizontal) e luz de cinema.

### Personagem (rosto)

- **Fotos reais, em vários ângulos, bem iluminadas**, de perto e de longe, e uma de corpo
  inteiro. Do jeito que a pessoa quer aparecer nos vídeos: se vai aparecer maquiada, a foto é
  maquiada.
- **Com fotos boas em vários ângulos**, a folha de rosto do ChatGPT funcionou (personagem fixo,
  vários vídeos). Pedido usado na aula, para adaptar:

  > Preciso de uma folha de rosto desse personagem, mantendo todos os detalhes e características
  > físicas dele, o mais semelhante ao real possível, fundo de estúdio cinza, super realista.
  > A roupa que ele vai usar é o último anexo, mas quero o rosto idêntico, bem detalhado.
  > Formato 16:9, 6 poses; a sexta é um close-up bem detalhado do rosto.

- **Com poucas fotos ou fotos ruins**, a folha sai diferente. Aí use as **fotos reais direto no
  vídeo** e escreva no prompt que delas só vem o rosto (roupas, acessórios e fundos ignorados).
  É a regra padrão desta skill (`seedance-2-5.md`). Na dúvida, fotos reais.
- Confira a folha gerada contra as fotos antes de usar: se um ângulo (o três quartos, por
  exemplo) mudou a pessoa, o vídeo vai puxar esse rosto toda vez que ela virar de lado.
- **Tatuagem pequena** vira texto inventado no braço. Saídas: manga comprida, apagar a tatuagem,
  ou uma foto bem de perto dela se precisar aparecer.

### Figurino

- **Só a roupa, sem rosto.** Rosto pequeno numa foto de corpo inteiro sai pouco detalhado, e o
  vídeo puxa esse rosto quando a pessoa está longe da câmera.
- Pedido que sempre funcionou: a roupa **"como um fantasma vestido"**, usando a proporção
  corporal das fotos reais (anexadas), em vários ângulos. Assim o corpo não engorda nem afina.
- Se as mãos importam (unhas pintadas, anel), mantenha as mãos na folha da roupa.
- **Cena com muita gente:** gere cada pessoa **já vestida** com a roupa da cena. Só a foto da
  roupa ao lado da foto do rosto vazou nas gerações com 7 pessoas.

### Objetos e texto escrito

- Objeto que tem que sair exato (envelope com "Próxima missão", o papel de dentro) vira imagem
  antes, com o texto já escrito. Sem a imagem, a IA inventa.

### Pose difícil

- Pose que a IA inventaria (cachorra alongando, duas pessoas sentadas de um jeito específico):
  gere a pose como imagem de estúdio, ou tire um print de um vídeo aprovado, e anexe como
  **referência de pose**, não como Start Frame. Nos clipes seguintes a posição se mantém.

## 3 e 4. Pontos da aula que reforçam a skill

Já estão nas outras páginas; ficam aqui para quem lê só esta:

- Cenário sozinho, personagem e roupa em anexos separados foi a virada da qualidade (antes, a
  cena com as pessoas já dentro mudava os rostos).
- Gerar trechos de ~10 s com 2 ou 3 takes dentro mantém a continuidade melhor que clipes soltos.
- Corte por mudança de ângulo esconde a emenda. Start Frame tirado de um vídeo perde um pouco de
  qualidade (leve borrão na emenda); só use em take contínuo, e disfarce na edição com cor e um
  fade leve.
- Várias folhas de idade no mesmo clipe confundem a IA: divida o clipe por idade.
- Vídeo quase perfeito com um detalhe errado: **Video Edit**. Peça para tirar só aquele item e
  confira o resto, porque já tirou junto um crachá que devia ficar.
- Descreva como a pessoa fala ("contido, não mostra muito os dentes"; "super alegre"), senão a
  IA exagera a boca.
- Higgsfield tem outros modos: trocar a pessoa de um vídeo real (motion) e trocar um objeto.

## Voz

- **Melhor caminho: a pessoa grava o áudio** e ele entra como `@AudioN`. O vídeo já sai dublado,
  com a entonação e o ritmo dela. Fala longa ou com muita emoção: sempre gravada.
- Para quem grava, mande a direção de cada fala: o sentimento (reflexivo, chateado, empolgado,
  indignado) e, se tiver, um vídeo de referência do tom.
- **Voz de personagem que não existe** (a cachorra): grave você mesmo a fala e troque a voz no
  ElevenLabs. Corte cada fala num arquivo separado (fala 1, fala 2...).
- **Sem áudio nenhum:** gere com a IA falando e depois use o **Change Voice** do Higgsfield com o
  clone da voz da pessoa (aceita amostra de até 3 minutos, por exemplo um trecho de vídeo dela).
  Fica parecido, não perfeito; só para fala curta.

## 5. Edição

1. Juntar os takes na ordem do roteiro; cortar atraso de reação se precisar.
2. **Trilha e efeitos sonoros depois**, por isso o prompt sempre pede sem música: dá controle e
  não quebra a continuidade entre clipes. Os efeitos que o Higgsfield já coloca podem ficar.
  Banco de trilha usado: Envato (Artlist também serve).
3. Legenda e textos (nome de pessoa, diálogo, narração).
4. Cor: contraste e um filtro leve dão o "look de cinema" e escondem emenda de Start Frame.

Depois de pronto, assista inteiro procurando objeto que apareceu do nada (na aula, uma lapela
surgiu e só foi vista no fim).

## Tempo e custo de referência (Ana, out/2026)

- Um vídeo de ~1 minuto: **1 dia a 1 dia e meio** de trabalho focado, mais a edição. Um
  cenário e dois personagens é rápido; muitos personagens demora bem mais.
- Higgsfield, plano Creator: 12 mil créditos por mês, que dão mais ou menos **5 vídeos de 1
  minuto** (~2 mil créditos por vídeo, mais quando tem muito personagem). Para 3 vídeos por
  semana, ela gasta ~22 mil por mês e compra crédito extra.
- Magnific saiu bem mais caro (~4 mil créditos por clipe de 10 s) e limita o prompt a 1000
  caracteres; por isso ela ficou no Higgsfield.
- Esses números são da conta dela. Antes de planejar volume, confirme plano e preço atuais.
