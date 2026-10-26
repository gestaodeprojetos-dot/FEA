# Estratégia do clipe — decidir antes de escrever

Quase todo crédito perdido até hoje veio de decisões tomadas antes da primeira palavra do prompt:
clipe com coisa demais, modo errado na ferramenta, duração curta para a fala, ou insistir em
corrigir texto quando o problema era a sorte da geração. Esta página é para pensar nisso **antes**
de compor.

## O que cada geração custa (Higgsfield, valores que o usuário passou em 2026-10-08)

| Operação | Custo aproximado | Observação |
|---|---|---|
| Seedance 2.5 **Draft** (480p), clipe de ~10 s | ~33 créditos | É como o usuário testa. Rascunho fica disponível para finalizar por 7 dias |
| Finalizar o draft em 1080p | ~132 | Só o que ficou bom |
| **Video Edit** do Seedance (edita um vídeo pronto) | ~132, mais o vídeo já finalizado | Cobra pela duração do vídeo de entrada |
| FLUX Video Edit | 1 crédito/s (até 15 s) | Barato, mas o usuário prefere não arriscar ("não quero arriscar") |
| Duração mínima por geração | 4 s | No Higgsfield e no Magnific. Só número inteiro de segundos |

Consequência prática — o tamanho certo de clipe fica **entre ~8 e ~13 s**:
- Clipe longo (20–25 s) é arriscado: se uma parte falha, paga tudo de novo. O usuário recusou
  clipe de 25 s e pediu para dividir em dois ("não quero gerar vídeos tão longos por conta de
  crédito", sitcom ep. 1).
- Picotar demais também é caro: quatro clipes de 4 s custam mais que um de 10 s ("teria que gerar
  4 vídeos de 4 segundos, o que sairia mais caro", sitcom ep. 2).
- Então: uma cena de 20 s vira **dois** clipes, cortados num ponto natural (troca de quem fala,
  alguém senta). Um clipe que falhou por variação não vira quatro clipes de 4 s; ver "Quando
  parar de corrigir o texto".
- Um take que falhou dentro de uma cena boa pode ser regerado sozinho **se** a cena aceitar o
  corte ali (ex.: só o take solo da Ana, 8 s, sitcom ep. 1). Se o take depende de continuidade
  fina com os vizinhos, regere a cena.

## Duração

- **Com áudio real (`@AudioN`): a duração sai do áudio, não da contagem de palavras.** Meça
  (`ffprobe` ou `silencedetect`, ver `audio-dialogo.md`) e some **~2 s de folga** depois da
  última palavra. Folga de 1 s às vezes basta (8 s para ~7 s de áudio, aprovado no ep. 1), às
  vezes não (11 s para 9,9 s cortou o fim da fala no ep. 2). Vídeo do mesmo tamanho do áudio faz
  a personagem "correr pra dar tempo". O usuário também quer essa sobra para encaixar o próximo
  áudio na edição.
- **Sem áudio real:** ~2,5 palavras por segundo (Lucas e Pedro falam devagar: ~2/s) + ~1–2 s.
  A contagem por palavra superestima quando a pessoa fala rápido: confirme com o usuário se ele
  tiver o áudio.
- O texto da fala no prompt tem que ser **idêntico** ao áudio, palavra por palavra. Peça a
  transcrição se tiver dúvida.
- Take com menos de ~2,5 s mal cabe uma ação. Take com mais de ~8 s sem ação nova "flutua".
- Duração sempre em segundos inteiros. Se o cálculo der 11,5, use 12 e diga por quê.

## Reference, Start Frame ou Video Edit?

| Situação | Modo | Por quê |
|---|---|---|
| Cena nova a partir do ambiente vazio + fotos dos personagens | **Reference / Omni-reference** | Composição livre, identidade vem das fotos |
| Já existe um frame aprovado e a pose, a luz ou o enquadramento têm que sair **iguais** | **Start Frame**, com as fotos de rosto/corpo/roupa ainda anexadas | Reference não trava pose: recompõe a cena (insert da Luna, 2026-10-08). Texto também não copia um frame bom (clipe da ligação do Pedro, 2026-10-05) |
| Mesma pose, porém mais de perto | Recortar o frame já no enquadramento novo (`ffmpeg ... crop`) e usar o recorte como **Start Frame** | Start Frame mantém o enquadramento do frame |
| Vídeo quase bom, falta tirar/trocar **um objeto** | **Video Edit** com prompt curto só da mudança | Tirou o tapete duplicado e preservou o resto (cena 2 do ep. 2, "ficou perfeito") |
| Vídeo quase bom, problema de **atuação ou timing** | Regerar em Draft partindo do prompt exato daquele vídeo, mudando só as frases do problema | Edição de atuação não foi confirmada como confiável |
| Alongar o fim de um clipe aprovado (mais tempo da pessoa parada, respirando) | **Extend** (`video_extension`) com o vídeo anexado e prompt curto só de continuação | Start Frame tirado do último quadro "escurece e não fica contínuo"; o Extend ficou "incrível" (sitcom ep. 1) |
| Texto escrito na tela, logo, letreiro com mais de ~3 palavras | Gerar sem o texto; aplicar na edição | Modelo de vídeo não soletra texto longo |

**Último quadro da cena anterior como Start Frame da próxima: não.** O usuário prefere que cada cena
comece num ângulo diferente do fim da anterior ("não roda liso", animação dos anos 80, 19/10). A
continuidade vai no texto (o estado de cada um) e o corte é por mudança de ângulo. Se precisar de
Start Frame, faça uma imagem nova, de outro ângulo.

Com Start Frame no Higgsfield, **o frame ocupa `@Image1`** e empurra os outros anexos uma
posição. Numere já com esse deslocamento e mostre a lista na ordem real.

## Antes de escrever, procure o que já funcionou

1. Abra `prompts-aprovados/README.md`. Se houver um aprovado do mesmo projeto, com o mesmo tipo
   de plano ou situação, **parta das palavras dele** e mude só o que a cena nova exige.
2. Abra `projetos/<projeto>.md`: convenção de câmera, esquema de anexos, estado da cena anterior
   (quem está onde, de frente para quem) e regras de cada personagem.

## Quando parar de corrigir o texto

Sinal: **duas gerações seguidas variando muito com mudanças pequenas de texto**, ou uma correção
que mudou só 3 frases e mesmo assim tudo saiu diferente. A variação do modelo passou a pesar mais
que o texto. A partir daí, cada nova versão de texto é aposta. Opções, da mais barata para a mais
cara — apresente ao usuário em uma ou duas linhas e deixe ele escolher:

1. **Rodar de novo o prompt da melhor geração**, sem mudar nada (em Draft é barato e às vezes é o
   que resolve).
2. **Video Edit** sobre a melhor geração, se o defeito for um objeto ou detalhe isolado.
3. **Travar a composição com uma imagem** (still aprovado como Start Frame, recorte do ambiente
   sem o elemento que não pode aparecer, referência de pose com o objeto já no tamanho certo).
   Imagem é mais barata que vídeo e vence o texto.
4. Simplificar o clipe: menos takes, menos ações, menos anexos.
5. Resolver na edição (overlay de texto, troca de áudio, corte de atraso).

Nunca proponha a opção mais cara sem dizer o custo dela.

## Riscos que se resolvem antes de gerar

Se o pedido cai num destes, avise **em uma linha**, com a alternativa segura, antes do prompt:

- Texto legível na tela, carta, logo → na edição.
- Objeto que precisa sumir ou mudar de estado → imagem de referência já no estado final.
- Tamanho exato de bicho/objeto ao lado de pessoa → imagem de referência já no tamanho certo.
- Aperto de mão, abraço, entregar objeto em close → plano aberto ou mão fora do quadro.
- Pose antropomórfica sem foto (cachorro alongando, sentado como gente) → gerar a foto de pose
  antes, como imagem (ela entra como referência de pose).
- Fala que não cabe no tempo → encurtar a fala ou alongar o clipe.
- Produto ou marca real (iPhone, logo de empresa, roupa com rosto de pessoa famosa) → o
  Higgsfield rejeita com "copyright restrictions". Objeto genérico sem marca no texto e na
  imagem; logo real entra na edição.
- Pata de bicho manipulando ferramenta pequena (lixa, caneta) → não sai; trocar por objeto que
  ele só segura e que já aparece na foto de referência (a caneca da Luna).
- Mais de ~5 pessoas com rosto reconhecível no mesmo clipe → um corte curto por pessoa (singles)
  e só um plano aberto, sem rostos grandes.

## O que nunca decidir sozinho

Quando o pedido é ambíguo e a escolha errada custa uma geração, pergunte em uma linha:
qual de dois objetos tirar, se a personagem levanta ou continua sentada, de que lado a câmera
fica, em que segundo a fala começa, **quem é um personagem que o roteiro não nomeia** (menino ou
menina, se é parente de alguém, se é a mesma pessoa que aparece em outra cena). Suposição errada já
custou gerações (o tapete errado, a Luna "levantando", a fala marcada em 4 s quando o usuário
queria mais tarde) e um retrabalho inteiro de folhas: em "O relógio" a "criança" da sala virou
"menina que representa a Clara" por suposição minha, e era um menino sem relação com ela.
