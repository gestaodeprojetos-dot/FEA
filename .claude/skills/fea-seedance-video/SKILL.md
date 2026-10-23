---
name: fea-seedance-video
description: Gera prompts em inglês para o Seedance 2.5 (Higgsfield, Magnific ou outro wrapper) que animam cenas com os personagens recorrentes do usuário a partir do ambiente vazio + fotos de rosto + foto de roupa, com o rosto idêntico às fotos, atuação natural sem exagero, sem música e com falas em PT-BR. Use sempre que o usuário pedir prompt de vídeo, take, cena, fala de personagem, animar uma imagem, Seedance, vídeo no Higgsfield, image-to-video, reference, start frame, extend ou video edit — e também quando ele voltar com um vídeo que deu errado (rosto mudou, ficou robótico ou exagerado, apareceu música, objeto duplicado, câmera errada) ou disser que um vídeo ficou bom.
---

# fea-seedance-video

Transforma **o pedido de uma cena** (ambiente, personagens, movimentos, falas, duração) num prompt
de vídeo em inglês para o Seedance 2.5, em que a identidade dos personagens é inegociável e cada
geração tem a melhor chance de sair certa de primeira.

Os nomes que aparecem nos exemplos (Ana, Luna, Pedro, Lucas, Clara) são fictícios: servem só para
mostrar como cada regra foi aprendida.

## Como esta skill está organizada

| O quê | Onde | Para quê |
|---|---|---|
| **Elenco** (fotos, Identity Card, figurinos, ambientes, props) | `personagens/` (como montar: `personagens/README.md`) | O rosto de cada personagem fica escrito num lugar só. **Leia de lá a cada pedido**, não de memória — muda |
| **Projetos de vídeo** | `projetos/<projeto>.md` (modelo em `projetos/README.md`) | Convenções de câmera, formato, anexos, como cada personagem atua, onde a cena parou, histórico |
| **Prompts aprovados** | `prompts-aprovados/` (índice no `README.md`) | O texto exato do que o usuário aprovou. É de onde se reaproveitam palavras |
| **Como planejar o clipe** | `references/estrategia.md` | Custo, duração, modo (Reference/Start Frame/Extend/Edit), riscos, quando parar de corrigir texto |
| **Como montar o prompt** | `references/prompt-template.md` | Os blocos, na ordem, e o modo compacto |
| **Frases testadas** | `references/frases.md` | O que escrever e o que evitar. Checklist antes de entregar |
| **Atuação** | `references/atuacao-natural.md` | Nem robótico, nem exagerado |
| **Áudio e falas** | `references/audio-dialogo.md` + `vozes.md` | Bloco AUDIO, áudio de referência, vozes |
| **Modelo e plataformas** | `references/seedance-2-5.md` | Como o Seedance e o Higgsfield se comportam |
| **Diagnóstico** | `references/troubleshooting.md` | Quando o vídeo volta errado |
| **Antes e depois do prompt** | `references/FEA-pre-producao.md` | Roteiro em cenas, kit de imagens (cenário, folha de rosto, figurino, objeto, pose), voz, edição, tempo e custo |
| **Exemplos da aula** | `references/FEA-exemplos-aula.md` | Dois prompts completos que a autora da skill aprovou, com o pedido que gerou cada um |

As pastas `personagens/`, `projetos/` e `prompts-aprovados/` começam vazias. Elas se enchem com o uso.

## Contexto do usuário

- Conversa em **português do Brasil**, simples e sem jargão. Quem usa esta skill nem sempre é
  técnico e muitas vezes dita mensagens longas por voz. **Explique o porquê** em uma linha quando
  pedir algo.
- Prompt final **sempre em inglês**; falas **em PT-BR**, entre aspas, exatamente como o usuário mandou.
- Plataforma principal: **Higgsfield** (prompt completo, testa em Draft e finaliza o que ficou
  bom). No **Magnific** o limite é de 1000 caracteres → modo compacto.
- **Não copie anexos para pastas sem necessidade.** Se as imagens já estão na plataforma, liste os
  anexos pelo nome do arquivo original, na ordem. Só crie arquivo quando for imagem nova (quadro
  extraído, recorte) e avise onde salvou.
- **Cada geração custa crédito.** Nunca sugira "gere 2 ou 3 versões e veja". Entregue a versão mais
  segura, não a mais ambiciosa, e avise antes os riscos que o texto não resolve.
- **Nenhuma música, trilha ou narração, nunca.** Nenhuma legenda ou texto na tela (salvo texto
  diegético pedido). Som ambiente sim.
- **Proporção e convenção de câmera mudam por projeto.** Confirme no primeiro prompt de um projeto
  novo e registre em `projetos/`.
- O usuário **lê o prompt antes de gerar** e pega erros de lógica. Escreva para ele conseguir conferir.

## Quatro coisas que o Seedance faz

Todas as regras desta skill saem destes quatro comportamentos (detalhes em
`references/seedance-2-5.md`):

1. **Mostra tudo o que está escrito.** Gesto citado acontece, objeto citado aparece, negativa traz
   o que nega, adjetivo de intensidade vira exagero. → Escreva só o que deve aparecer, de forma
   afirmativa, uma vez. Não invente gesto que não foi pedido.
2. **Imagem vence texto.** → Quando algo tem que sair exato (rosto, roupa, pose, estado de um
   objeto, tamanho, ângulo), resolva com a imagem certa, não com mais palavras.
3. **Cada geração é um sorteio novo.** → Clipes simples; não mexa no que funcionou; quando a sorte
   pesa mais que o texto, mude de estratégia (`estrategia.md`).
4. **Prompt que cresce, piora.** → Alvo até ~12 mil caracteres, teto de 15 mil. Correção
   substitui frase, não acrescenta.

## Fluxo

### 1. Projeto e pessoas
Descubra o projeto e quem está na cena. Leia `projetos/<projeto>.md` e o `card.md` de cada
personagem em `personagens/`. Personagem novo: monte a pasta dele como explica
`personagens/README.md`. Projeto novo: crie `projetos/<projeto>.md` com formato, plataforma, câmera
e elenco, e pergunte a proporção.
Se ainda falta o kit da cena (roteiro em cenas, cenário vazio, fotos ou folha de rosto, figurino,
objeto com texto, pose difícil), ajude a montar antes do prompt: `references/FEA-pre-producao.md`.

### 2. O que já funcionou
Abra `prompts-aprovados/README.md`. Se houver um aprovado do mesmo projeto ou da mesma situação
(diálogo de duas pessoas, take solo com fala, trajeto em volta de móvel, Extend…), parta das palavras dele.

### 3. O pedido
Movimentos, takes, falas, duração. Pergunte **numa rodada só** o que for determinante e caro de
adivinhar: duração ou áudio, texto exato da fala, quem fala, em que momento, de que lado fica a
câmera, quem abre a porta, se a pessoa está sentada ou em pé, qual de dois objetos é o certo.
Suposição errada custa gerações. Detalhes secundários (lente, som ambiente) você escolhe e diz o
que escolheu.

### 4. Planejar o clipe
`references/estrategia.md`: duração (com áudio, áudio + ~2 s), quantos takes cabem (uma ação
principal por take), qual modo, quais anexos e em que ordem. Se o pedido cai num risco conhecido
(texto na tela, objeto que some, grupo grande, aperto de mão, marca registrada), diga em uma linha,
com a alternativa segura, antes do prompt.

### 5. Compor
`references/prompt-template.md`, com `atuacao-natural.md` e `audio-dialogo.md` abertos. Identity
Card copiado literal do `card.md`.

### 6. Revisar antes de entregar
- Passe o prompt por `references/frases.md` e troque o que estiver na coluna "Evite".
- Releia o pedido do usuário item por item e confira se cada um está no prompt — e se nada que ele
  não pediu entrou (gesto, objeto, expressão).
- Conte os caracteres (`wc -m` num arquivo temporário).
- Confira: numeração dos anexos (com Start Frame tudo sobe uma posição), menções `@ImageN`
  separadas, proporção no LOOK, tempos somando a duração, continuidade com a cena anterior (lado,
  posição, para onde olha).
- **Todo detalhe visível escrito no prompt tem que estar numa referência anexada e bater com ela.**
  Abra a imagem e confira antes de descrever (cor, textura, pele, acessório). Não invente detalhe
  que você não viu ("pele bronzeada", "unhas curtas", "veias"): escreva "exactly as in @ImageN".
- **Antes de tirar um anexo** (roupa, relógio, acessório) porque "não vai aparecer", desenhe a
  geometria do plano: de onde a câmera olha, por qual borda o corpo entra. Se puder entrar no
  quadro, o anexo fica e o prompt descreve como aparece. Continuidade com os outros planos (manga,
  relógio, aliança) vale até em close.
- **Quando o usuário voltar com um vídeo**, baixe e olhe os quadros antes de responder, e confira a
  ordem dos anexos que ele usou contra os `@ImageN` do prompt.

### 7. Entregar
Nesta ordem, sem parágrafos explicando o prompt:

1. **Prompt** num único bloco de código, pronto para colar. Em correção, o título diz a versão:
   "Versão 3 (substitui a 2)".
2. **Anexos, na ordem exata**, com o nome de arquivo de cada um — a numeração tem que bater com o
   `@ImageN` / `@AudioN` do prompt.
3. **Na ferramenta:** modo (Reference/Omni, Start Frame, Extend ou Edit), duração em segundos
   inteiros, proporção, áudio ligado.
4. **Uma ou duas linhas em PT-BR:** o que ficou travado, o que você escolheu por conta própria e
   o risco que sobrou. Em correção, a lista das frases trocadas, uma por problema.

### 8. Iterar
Resultado ruim → `references/troubleshooting.md`, começando pela configuração. Olhe o vídeo em
vez de supor: peça o arquivo ou um print, ou procure na pasta de vídeos do projeto (o caminho fica
em `projetos/<projeto>.md`) e extraia quadros com `ffmpeg`. Correção pontual: parta do prompt
**exato** daquele vídeo e troque só as frases dos problemas apontados. Sempre o prompt inteiro,
nunca um trecho.

### 9. Registrar o que aprendeu
A skill só melhora se o aprendizado for para o lugar certo, **integrado ao que já existe** (uma
linha na tabela certa, uma regra corrigida), e não colado no fim de um arquivo como diário.

| Descobriu | Onde registrar |
|---|---|
| O usuário aprovou com palavras claras | `prompts-aprovados/` + linha no índice (`README.md` explica como) |
| Uma frase que deu problema, ou a frase que resolveu | `references/frases.md`, na tabela da categoria |
| Um sintoma novo e sua correção | `references/troubleshooting.md`, na seção certa |
| Comportamento do modelo ou da plataforma (limite, custo, modo, sintaxe) | `references/seedance-2-5.md` |
| Gosto do usuário, convenção do projeto, estado da cena, como um personagem atua | `projetos/<projeto>.md` |
| Traço físico errado ou novo do personagem | `personagens/<nome>/card.md` — e avise o usuário em uma linha |
| Voz | `vozes.md` |

Só chame de "aprovado" o que o usuário aprovou ("ficou ótimo", "perfeito", "deu certo"). Ir para a
cena seguinte sem comentar não é aprovação. Não afirme o que não viu no vídeo.

Não salve outros prompts em disco: eles saem como texto na conversa.

## Regras que não se negociam

- **O rosto vem só das fotos reais do personagem.** Imagem gerada (folha de rosto, frame de vídeo,
  recorte pequeno) nunca é fonte de rosto: deixa a pessoa "muito estranha". Única exceção: folha de
  rosto feita no ChatGPT a partir de fotos boas em vários ângulos, conferida contra as fotos e
  aprovada pelo usuário (`references/FEA-pre-producao.md`). Na dúvida, fotos reais.
- **Identity Card copiado literal** do `card.md`. Encurtar é escolher campos inteiros. As exceções
  (frase de sorriso em cena sem sorriso, altura, comentários) estão em `prompt-template.md`.
- **Ambiente vazio como `@Image1`, nunca frame inicial** (salvo quando o modo escolhido é Start
  Frame). Imagem de cena com pessoas faz o modelo copiar os dublês.
- **Uma função por anexo**, dita por escrito, com o que ignorar nele. Personagem vinculado às fotos
  por traço visível.
- **Roupa só da foto de roupa.** As roupas das fotos de rosto são nomeadas uma vez e excluídas.
- **Nenhuma música; nenhuma legenda.** Bloco AUDIO sempre presente, com o fecho fixo.
- **Atuação por comportamento observável, pequena.** Nada de gesto, expressão ou objeto que o
  usuário não pediu.
- **Continuidade de ação entre os takes.** O movimento não reinicia no corte: a partir do 2º take,
  `Continuing from the previous shot:` e o estado de cada pessoa, **inclusive a expressão**. Se
  terminou sorrindo, começa o take seguinte com o mesmo sorriso. Entre clipes, descreva o estado
  (posição, o que segura, para onde olha), não a ação passada.
- **Correção = prompt inteiro, mudando só o necessário.** E rotulado com a versão.
- **Um prompt, um bloco.** Sem negative prompt separado.

## Guarda-corpo

Fluxo de vídeo com pessoas reais, com uso autorizado por elas. Recuse montar prompts que coloquem
alguém em contexto sexual, em situação difamatória, ou fabriquem cena enganosa apresentada como
real (pessoa identificável em evento político, crime, endosso comercial que não aconteceu, ou
dizendo algo que ela não diria em contexto que possa ser tomado como verdadeiro). Diga em uma
frase e ofereça a alternativa mais próxima que funcione.
