# Diagnóstico — quando o clipe não saiu como devia

Peça o vídeo ou um print do quadro problemático sempre que puder: comparar com as referências
diagnostica muito mais rápido que a descrição. E não afirme o que não viu ("acertou o terno em
todos" quando não acertou custou confiança).

## 1. Antes de mexer no texto: confira a configuração

Metade dos problemas não é de texto. Pergunte em uma linha só o que não souber:

1. **Modo:** Reference/Omni, Start Frame ou Extend? Era o modo certo para o que a cena pedia
   (`estrategia.md`)?
2. **Anexos:** quais, em que ordem. Com Start Frame no Higgsfield, o frame vira `@Image1` e
   empurra os outros.
3. **Menções `@ImageN` intactas:** no Higgsfield, a menção é um vínculo com o anexo. **Trocar um
   anexo apaga a menção dele no texto** (já rodou um prompt com "exactly as in ,") e acrescentar
   um Start Frame renumera tudo. Depois de trocar qualquer anexo, cole o prompt inteiro de novo.
   Menções coladas uma na outra (`@Image6 and @Image7`) já chegaram quebradas: escreva cada uma
   separada por vírgula e peça para conferir depois de colar.
4. **Duração na ferramenta** igual à do prompt (um prompt de 14 s já rodou com 12 s e ninguém
   viu).
5. **Proporção** na ferramenta igual à escrita no LOOK.
6. **Qual versão rodou.** Se você entregou várias versões, confirme qual foi gerada (já rodou uma
   v1 superada).

## 2. Sintomas

### Rosto e identidade

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "ficou muito diferente" / "estranha" | Imagem **gerada** como fonte de rosto (folha de rosto gerada, frame de vídeo, recorte pequeno de baixa resolução) | Só fotos reais, todas as que o card lista. Imagem gerada nunca é fonte de rosto |
| "o rosto é o da imagem da cena" / "imitou a foto" | Imagem de cena com pessoas (dublês): o modelo copia enquadramento, ângulo, gesto e rostos | Ambiente **vazio** como `@Image1` (esquema atual). Se só houver imagem com pessoas, recorte a pessoa fora (`sips`/`ffmpeg` numa cópia) e entregue o recorte |
| "começa parecido e vai mudando" | Rosto pequeno, cabeça girando muito, clipe longo | Plano mais fechado; cabeça de frente com só os olhos se movendo; clipe mais curto |
| "trocou/misturou os rostos" | Vínculo por ordem, traço citado em um só | Vincular cada grupo de fotos por traço visível; afirmar cada traço nos dois; TELLING THEM APART (bloco TELLING THEM APART, em `prompt-template.md`) |
| "apareceu uma pinta / marca que ela não tem" | Traço falso no card, repetido no prompt | Conferir o card contra as fotos e corrigir **o card** (todos os prompts herdam dele). Avise o usuário em uma linha |
| "ele ficou estufado / um armário" | Sem foto de corpo, ou `stocky`/`broad` no card | Anexar foto de corpo; `slim… never bulky` quando for o caso |
| "rosto deformado" num close | Cabeça girando com fotos só frontais | Cabeça de frente, só os olhos se movem |
| "apareceu tatuagem/aliança/marca no braço" | A foto vence o texto, ou o modelo inventa quando o antebraço fica em evidência | Bloco ARMS AND HANDS do projeto, uma vez; manga comprida ou braço fora do quadro; objeto entra e sai do quadro (`lifts the phone into frame`) |

### Roupa e acessórios

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "veio com a roupa da foto de rosto" (uma ou duas pessoas) | Foto de rosto vazando roupa | Nomear **por escrito, uma vez**, as roupas que aparecem nas fotos de rosto daquela cena e dizer que não fazem parte do clipe; WARDROBE `exactly as in @ImageN` peça por peça |
| "saíram todos com a roupa das fotos" (grupo) | Com muitas pessoas, cada uma puxa a roupa da própria foto; repetir no texto falhou ~6 vezes | Uma foto de cada pessoa **já vestida** com a roupa da cena (montada pelo usuário). Sem isso, avise antes que o texto não segura |
| "apareceu um brinco / mudou o esmalte" | Acessório ou cor que varia entre as fotos | Brinco que está nas fotos não sai por texto (o usuário liberou o da Ana). Cor que varia: fixar com as mesmas palavras em todo prompt (esmalte vinho) |
| "a roupa mudou entre os takes" | WARDROBE vago | Peça por peça, `unchanged for the whole clip, including across cuts` |

### Atuação e ritmo

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "robótico" / "parece avatar" | Ação sem comportamento, só uma mão coreografada, olhar fixo, simultaneidade | `atuacao-natural.md`: as duas mãos com ações próprias, ações encadeadas que ocupem o take, quem escuta com ação concreta |
| "andou como um robô" | Palavras de rigidez (`upright, chin level, square shoulders, even stride`) | Andar descrito por comportamento solto (`frases.md`) |
| "exagerado" / "careta" / "boca muito aberta" | Adjetivos de intensidade, reação empilhada, negativas de expressão | `frases.md` → Rosto. Reaproveitar as palavras de um aprovado |
| "sério demais" / "sorriu demais" | Dose do sorriso | Um sorriso pequeno e breve num só momento |
| "mordendo o lábio" | `pensive`, `lips pressed`, regra do sorriso em cena sem sorriso | `frases.md` → Rosto |
| "esperou e só depois reagiu" | Reação em beats espaçados | Reação no mesmo movimento; a pessoa já no quadro no 1º frame |
| "ficou parada / congelada" | `holding`, foto de pose, "fica em pé ao lado" | Ação em andamento desde o 1º quadro |
| "sobrou tempo dela respirando" / "tempo morto" | `breath` como beat; take longo demais para a ação | Ação concreta para quem escuta; take mais curto |
| "fez um gesto que eu não pedi" (aceno, mão no queixo) | O próprio prompt inventou o gesto | Tirar o gesto. Fim de fala neutro escrito (`settles back to neutral… no punctuating gesture`) |
| "a IA tá correndo pra dar tempo" | Clipe do tamanho do áudio, ou ação demais | Áudio + ~2 s; menos ação |
| "falou olhando pra câmera" | Close centralizado sem direção de olhar | Olhar afirmativo + referência de enquadramento e olhar (still de cena aprovada) |
| "a expressão da imagem de referência vazou" | Still de posição com uma expressão marcada | No REFERENCES, só as posições são tiradas do still; rosto descrito de forma afirmativa |

### Câmera e enquadramento

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "começou igualzinho à imagem" | Ferramenta em Start Frame, ou clipe de 1 take com a pessoa na imagem | Modo Reference; ambiente vazio; take com ângulo e escala diferentes da imagem (`new angle, unlike @Image1`) |
| "continuou contra-plongée" | A altura da câmera vem da imagem | Trocar a imagem por uma na altura dos olhos. Texto (`eye level`, altura em metros) não resolveu |
| "close muito apertado" / "não queria close na cara" | Palavra "close" lida como close extremo | Tamanho do plano por partes do corpo (`head-and-shoulders, headroom above her hair…`); no Instagram, rosto no terço de cima e terço de baixo livre para legenda |
| "a câmera girou" (queria panorâmica) | `arc`, `orbit`, "giro" | Travelling lateral (`frases.md`) |
| "câmera parada em tudo" | Regra de câmera generalizada | Regra por take |
| "focou pelo lado errado" | Lado da câmera não escrito | Escrever o lado |
| "transição estranha" (swish pan) | Movimento no começo do take lido como transição | Movimento dentro do take; `Hard cut.` entre takes |
| "o giro saiu pela metade" | Arco de 180° em menos de ~5 s | Dar ≥5 s ao arco, ou trocar por plano zenital/travelling |
| "apareceu uma porta/parede que não existe" | Câmera de lado ou em arco mostrando área sem referência: o modelo inventa | Manter a câmera vendo o que a referência mostra; recorte de parede lisa como referência de fundo |
| "a porta/letreiro que está atrás da câmera apareceu" | A imagem do ambiente tem esse elemento | Recorte da parede lisa como referência do fundo daquele take |

### Objetos, espaço e direção

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "criou um objeto extra" (tapete, caixa vazia) | Posição descrita em relação a um objeto, ou palavra que vira objeto | Contar e amarrar ao que existe (`exactly one rug — the one under the coffee table`) |
| "o objeto que tinha sumido voltou" | Imagem com o objeto + texto repetindo o nome | Imagem já no estado final; não nomear o que sumiu |
| "o objeto ficou gigante" | Imagem de referência em close passa a escala; variação do modelo | Imagem de referência já no tamanho certo, em plano aberto; `the size in the sheet's close-ups is not used`; âncora no corpo da pessoa |
| "atravessou a mesa" | Trajeto vago | Caminho em 3 pontos com tempo + `solid object… never through/across/over/under` + faixa de chão livre |
| "foi na direção contrária" / "lados trocados" | Esquerda/direita não são respeitadas; em plano reverso o modelo copia o lado da imagem | Câmera à frente recuando; destino pelo que se vê; imagem de referência do próprio ângulo |
| "abriu o envelope ao contrário" / "virou o objeto errado" | Câmera de frente: o modelo vira a face importante para a lente | Câmera atrás do ombro ou Start Frame no estado certo |
| "a porta abriu sozinha" / "não é assim que abre" | Ninguém foi dito para abrir | Quem abre, mão, tipo de maçaneta, distância em que para |
| "o texto/letreiro saiu errado" | Modelo não soletra | Na edição; ou câmera frontal + recorte do letreiro como referência |
| "a pata mexe sem segurar" | Pata não manipula ferramenta pequena | Objeto só segurado, que já está na foto |
| "o efeito apareceu antes da hora" (brilho antes do pó) | Efeito descrito sem amarrar no tempo | Tempo exato do efeito e o que existe antes dele |

### Grupo (3 ou mais pessoas)

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "saíram seis, eu quero sete" | Contagem sem lista | Lista da esquerda para a direita por traço + "N mulheres e M homens" |
| "estão numa roda" / "de costas" / "flertando" | `facing each other`, cabeça virada para o par | Corpos de frente para a câmera, cabeça gira 15–25° |
| "tem gente que não aparece" | Planos demais no tempo (9 planos em 13–15 s) | Menos planos, ou dividir em dois clipes |
| "a altura não ficou certa" | Altura em metros ignorada | Sem solução por texto confirmada; foto de corpo; still do grupo |
| "estão falando chinês" | Murmúrio sem idioma | `in Brazilian Portuguese` |
| "brinco/acessório num que não usa" | Acessório migra entre pessoas | Afirmar o que cada um usa (bloco TELLING THEM APART, em `prompt-template.md`) |

### Áudio

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "tem música" / "trilha" | Fecho do AUDIO ausente; ambiente de evento/festa | Fecho literal; ambiente sem "event", "party", "stage"; `No studio audience and no laugh track` em sitcom |
| "apareceu legenda" | Fala sem o fecho; vozes de fundo compreensíveis | Fecho literal; vozes de fundo `too distant to understand` |
| "o nome saiu errado" | Voz sintetizada | Pronúncia ancorada num áudio de referência com essa função |
| "a fala ficou diferente do áudio" / "tom triste" | Pedido de cópia exata do áudio | `audio-dialogo.md` → função do áudio |
| "cortou o fim da fala" | Clipe curto para o áudio | Áudio + ~2 s |
| "a voz não parece a dele" / "cada clipe uma voz" | Descritor mudou | Descritor literal de `vozes.md`; propor áudio de referência |

### Plataforma

| O usuário diz | Causa provável | Correção |
|---|---|---|
| "Rejected due to copyright restrictions" | Marca no texto, foto de produto com logo, foto com rosto de pessoa famosa | Tirar a marca do texto; objeto genérico; foto de roupa sem pessoa (`estrategia.md`) |
| "perde qualidade quando coloco o frame" | Frame de vídeo gerado como referência, ou rascunho 480p | Frame bom como **Start Frame** (com as referências de rosto/corpo/roupa); upscale antes se for de rascunho |
| "escureceu no começo / não ficou contínuo" | Start Frame do último quadro para alongar | Extend só com o vídeo |

## 3. Como corrigir

- **Correção pontual = troca só das frases do problema.** Quando o usuário aponta N problemas num
  vídeo que no resto está bom, parta do prompt **exato** daquele vídeo e troque só as frases
  ligadas a cada problema, mantendo tudo o mais palavra por palavra. Na entrega, liste as frases
  trocadas, uma por problema. Reescrever "para melhorar" já gerou "pontuei 3 coisas e você mudou
  tudo" e o "pior de todos".
- **A correção substitui, não acrescenta.** Cada correção que só soma frases faz o prompt crescer
  e diluir o resto. Nenhum vídeo com prompt de 15 mil caracteres ou mais foi aprovado. Se a
  correção nova pede uma frase, tire a antiga que ela substitui.
- **Rotule as versões.** "Versão 3 (substitui a 2) — rode esta". Se o usuário rodar uma versão
  antiga, diga.
- **Interprete o pedido pelo mínimo.** "Ele mal aparece" não é pedido para cortá-lo do quadro.
  Na dúvida entre duas leituras com custo de geração, pergunte.
- **O prompt inteiro sempre**, num bloco só, mesmo quando muda uma frase.

Quando a correção de texto deixa de funcionar, veja "Quando parar de corrigir o texto" em
`estrategia.md`.

## 4. O que não adianta

- "SAME FACE", "100% identical" em maiúsculas ou repetido. Âncora concreta rende mais.
- "8k, masterpiece, ultra realistic". Ruído.
- Negativa para tirar um traço que está nas fotos ("no earrings", "no tattoo"). A foto vence.
- Altura e distância em metros entre pessoas.
- Repetir a roupa em todo take para vencer a roupa das fotos num grupo grande.
- Corrigir ângulo de câmera herdado da imagem só com texto.
- Regerar o mesmo prompt várias vezes quando a causa é o modo, os anexos ou uma frase do prompt.
  (Regerar o mesmo prompt **faz sentido** quando o defeito é claramente sorte: o mesmo texto já
  deu um gato pequeno e um gato gigante.)
