# REVISÃO — *Relleno Tridimensional de Ojeras* (ES-LatAm) · 23/09/2026

Revisor: leitura de par especialista, persona médico hispano-hablante.
Arquivo revisado: `Relleno_Tridimensional_de_Ojeras_ES.pdf`, 74 páginas,
9.896 palavras, 1.221 segmentos.

## Cobertura — leia antes do veredito

**O PDF original em português não está no repositório.** Isso não é detalhe:

| Camada | Estado | Por quê |
|---|---|---|
| 1 — Mecânica (`auditar.py`) | ✅ completa | não depende do original |
| 2 — Segurança clínica | ⚠️ **parcial** | dose, via, plano e lado foram conferidos quanto a coerência interna e plausibilidade clínica, **não contra a origem** |
| 3 — Back-translation | ❌ **não executada** | exige o original |
| 3b — Mídia e QR | ✅ completa | 33 QR lidos e conferidos um a um |
| 4 — Voz nativa | ✅ completa | não depende do original |

A camada 3 é justamente a que pega **o número certo na estrutura errada, o
ligamento trocado, a ordem dos passos invertida e o «não» perdido** — erros que
o espanhol não denuncia, porque o texto fica perfeitamente legível dizendo outra
coisa. Nenhum desses foi procurado como deveria.

**Consequência prática:** o veredito abaixo cobre a qualidade editorial e a
coerência interna. Não substitui a conferência contra o original. Se você me
der o PDF em português, fecho as camadas 2 e 3 em cerca de uma hora.

---

## SITUAÇÃO EM 23/09/2026 — achados aplicados

Os achados [1] a [7] e a questão [Q1] **foram aplicados no PDF entregue**
(`produccion/correcciones_revision.py`, onze trocas). O que segue abaixo é o
registro da revisão como ela foi feita; a coluna de estado diz o que já
está resolvido no arquivo.

| # | Achado | Estado |
|---|---|---|
| [1] | pág. 12, falta `al` | ✅ aplicado |
| [2] | cinco nomes para o rebordo orbitário (p17, 21, 22, 52) | ✅ uniformizado em `reborde orbitario` |
| [3] | pág. 30, `craneal`/`distal` | ✅ `en sentido caudal` |
| [4] | caixa de `metodología ARTI` | ✅ maiúscula nas 7 |
| [5] | pág. 52, `ligamento LCC` | ✅ `soporte al LCC` |
| [6] | pág. 20, hífen no lugar do travessão | ✅ travessão desenhado |
| [7] | pág. 44, `mg/mL` partido entre linhas | ✅ unidade inteira |
| [Q1] | `orbicular (ORL)` contra `orbitario (LRO)` | ✅ `orbitario (LRO)` nas duas ocorrências da p34 |
| [Q2] | pág. 34, lista prometida que não aparece | ⏳ depende do original PT |
| [Q4] | pág. 40, «la fuerza G» | ⏳ decisão do autor |
| [Q5] | 2 QR para material que não está em espanhol | ⏳ decisão do autor |
| camadas 2 e 3 | conferência contra a origem | ⏳ depende do original PT |

Conferido depois de aplicar: `auditar.py` **LIBERADO, 100 %**, zero classe A;
`conferir_fontes.py` zero glifo de recurso; camada de texto idêntica nas 64
páginas não tocadas; zero sobreposição nova nas 10 tocadas; 74 páginas, 136
imagens, 33 links, 8 marcadores, `/Lang` es-419 — tudo preservado. As três
correções de parágrafo e as sete de linha foram vistas em renderização a 200
e 300 dpi, uma por uma.

O travessão da p20 é **desenho, não caractere**: a Helvetica Neue Bold
embutida no PDF do cliente tem 82 glifos e nenhum U+2014. A barra sai da
barra do próprio hífen do arquivo — mesma altura, mesma espessura, largura
de um em —, o que mantém o tipo do título.

---

## VEREDITO DA REVISÃO (registro de 23/09/2026, antes das correções)

```
Classe A (barreira clínica):  0 achados confirmados
Classe B (índice editorial):  99,2 %   (1.211 de 1.221 segmentos limpos)
                              1,01 achados por mil palavras
                              3 GRAVE · 4 MENOR
Questões ao autor:            5  (não afetam o veredito)
```

O `auditar.py` devolveu 100 % e zero classe A. **Os 0,8 % de diferença são
achados que o script não vê** — estão listados abaixo, com a regra proposta
para que ele passe a ver.

---

## GRAVE

### [1] pág. 12 · gramática — frase sem preposição

```
Tradução ES:  «Haga clic en el botón o apunte el celular el código QR
               para descargar el e-book de Allergan»
Correção:     «Haga clic en el botón o apunte el celular AL código QR
               para descargar el e-book de Allergan»
```

Falta o `al`. A frase fica agramatical e está **na arte**, em corpo grande,
numa página de conteúdo. É o primeiro erro que um leitor hispano-hablante vê.

O alvo registrado em `anexo-1-texto-en-arte.md` já era o correto, com `al` — a
preposição se perdeu na reaplicação sobre a arte. A frase equivalente da pág. 6
está certa, o que confirma que é lapso isolado e não decisão.

**Custo de não corrigir: alto.** Erro visível, em página de conteúdo, sem
atenuante.

### [2] páginas 17, 21, 22, 52 · inconsistência interna — o rebordo orbitário tem cinco nomes

| Pág. | Forma usada |
|---|---|
| 14, 15, 33 (×2), 34 | `reborde orbitario` ← forma do glossário |
| 17 | `borde superior del hueso orbitario` |
| 21 | `borde inferior de la órbita` |
| 22 | `reborde óseo de la órbita` |
| 52 | `reborde óseo orbitario` |

O aluno vê cinco nomes para o mesmo acidente ósseo — e este é o ponto de
referência de toda a técnica: os quatro pertuitos se localizam em relação a ele.

**Ressalva honesta:** parte da variação pode estar no original, e o revisor não
uniformiza o que o original varia sem sinalizar. As formas da p17 (*borde
superior*) e da p21 (*borde inferior*) podem inclusive designar bordas
diferentes. **Sem o PDF português não dá para separar o que é variação do autor
do que é variação do tradutor.** Por isso entra como GRAVE a conferir, não como
erro fechado.

**Custo de não corrigir: alto** — termo estrutural, repetido, em material de
ensino.

### [3] pág. 30 · eixo anatômico — `craneal` emparelhado com `distal`

```
Tradução ES:  «demarca la protrusión de la grasa orbitaria en sentido craneal
               y la región malar […] en sentido distal»
Proposta:     «…en sentido craneal y […] en sentido caudal»
```

`craneal` emparelha com `caudal`. `distal` pertence ao eixo proximal/distal, que
na face não se usa para essa relação. O livro usa `craneal`/`caudal`
corretamente em todas as outras passagens (págs. 12, 33, 34).

**Por que NÃO estou classificando como classe A:** a rubrica põe «lado e
sentido» na barreira clínica, e com razão — inversão de sentido é erro de
procedimento. Aqui **não há inversão**: o sentido descrito está correto, o que
está errado é o *nome do eixo*. Chamar isso de classe A reteria a entrega por um
problema que não põe paciente em risco, e esvaziaria a classe A. Fica como
GRAVE, com a observação de que só o original resolve se o lapso é da tradução
ou do autor.

---

## MENOR

### [4] `metodología ARTI` com caixa oscilante
Pág. 6 em minúscula (`la metodología ARTI`); págs. 8 (×2), 9 (×2) e 72 em
maiúscula (`La Metodología ARTI`). Seis contra um. Uniformizar — a norma
espanhola pede minúscula para o substantivo comum, mas por ser nome de
metodologia de autor a maiúscula é defensável. **O defeito é oscilar**, não a
escolha.

### [5] pág. 52 · redundância — `el soporte al ligamento LCC`
`LCC` já é *ligamento cigomático-cutáneo*; o texto diz «ligamento ligamento».
Corrigir para `el soporte al LCC` ou `al ligamento cigomático-cutáneo`.

### [6] pág. 20 · travessão virou hífen
`ANATOMÍA EN CADÁVER - REVISIÓN COMPLETA`. O alvo registrado no
`anexo-1-texto-en-arte.md` traz travessão (`—`). As demais aberturas do livro
usam travessão.

### [7] pág. 44 · unidade partida entre linhas
`aproximadamente 20 mg/` / `mL` — a unidade quebra na mudança de linha. Não se
parte unidade de medida. Pode ter sido introduzido pelo refluxo, já que o
espanhol corre mais longo que o português.

---

## QUESTÃO AO AUTOR — não afetam o veredito

### [Q1] pág. 34 · `ligamento retenedor orbicular (ORL)` contra quatro `orbitario`
Já registrado em `90-decisiones.md` como pendência. Acrescento o argumento que
fecha a questão: **a sigla contradiz o adjetivo.** `ORL` é *Orbital Retaining
Ligament*. «Ligamento retenedor **orbicular** (ORL)» diz orbicular e sigla
orbital na mesma linha. Recomendo `orbitario` nos dois idiomas.

### [Q2] pág. 34 · lista prometida que não aparece
«…es la manifestación clínica resultante de la suma de **los siguientes
elementos anatómicos**.» O parágrafo seguinte abre com «Así pues, puede
concluirse…». A lista anunciada não existe. Ou ela se perdeu, ou a frase deveria
apontar para uma figura. Confirme contra o original.

### [Q3] pág. 29 → 30 · **o texto perdido não existe**
O `relatorio-producao-es.md` registra que «a frase da p29 termina em *aplicando
siempre el*» e que pareceria haver texto perdido. **Reli a página no PDF
entregue: não é o caso.** A p29 fecha com período completo — «…y evitando
irregularidades como bolsas o hinchazones.» — e a p30 abre uma seção nova. O
alarme veio do DOCX incompleto ou de uma extração que quebrou a linha.
**Um item a menos na sua lista de decisões.**

### [Q4] pág. 40 · «la fuerza G que se le aplica»
`G'` é módulo elástico; não existe «fuerza G» em reologia — em espanhol o termo
remete a força de aceleração. Provável frouxidão do original. Se quiser, troco
por «la fuerza de deformación que se le aplica».

### [Q5] 4 QR levam a material que não está em espanhol
Págs. 12 (e-book Allergan) e 18, 25, 30 (livro AFE, o mesmo destino nas três).
Já consta como pendência em `90-decisiones.md`. Os outros QR estão corretos: os
de artigo científico apontam para o artigo em inglês, como manda o glossário, e
os 20 de vídeo já foram trocados para os ativos em espanhol.

**Decisão do autor em 22/09/2026:** o que está em inglês pode ficar. Isso
resolve os QR de artigo. Os dois acima (Allergan, AFE) continuam pendentes se o
material for português.

---

## O que a revisão confirmou que está certo

Não é enchimento: é o que dispensa nova conferência.

- **Terminologia travada, sem exceção.** `cigomático` com C nas 10 ocorrências;
  `surco nasoyugal` nas 10; `efecto Tyndall` com T maiúscula nas 10.
  Zero ocorrência das armadilhas listadas no glossário.
- **Tratamento formal uniforme.** `usted` em todo o material, inclusive nos
  imperativos da conclusão («oriente», «recomiende», «sugiera»). Nenhum tuteo.
- **Posologia íntegra** onde é verificável: `prednisona 40 mg/día`,
  `Arnica montana D2`, `3 veces al día`, `compresas frías durante las primeras
  24 horas`, `al menos 48 horas`, `de 15 a 30 días`, `de 0,3 a 0,5 mm`,
  `de 0,5 a 1 cm`, `20 mg/mL` e `25 mg/mL`. Decimais com vírgula, espaço entre
  cifra e unidade, `mL` com L maiúsculo.
- **Marcas intactas:** Yvoire Contour, Restylane Lift, Voluma, Subskin,
  Biogelis Volume, Traumeel S, Motix, Thrombophob, Allergan.
- **Espanhol nativo.** Não encontrei lusismo sintático, conector repetido nem
  ênfase comercial brasileira traduzida ao pé da letra. A prosa dos capítulos de
  técnica e intercorrências lê como escrita em espanhol, não como traduzida.

---

## AJUSTES NO AUDITOR

O `auditar.py` deu **100 % num texto que tem um erro de gramática visível na
página 12**. Isso não é ruído: é um furo de cobertura, e furo não reportado vira
falsa confiança.

| Regra proposta | Pega |
|---|---|
| `apunte\s+\w+\s+(el\|la)\s+código` sem `al` | achado [1] e a família «verbo de direção + objeto sem preposição» |
| Contagem de variantes por acidente anatômico: se `(re)?borde.{0,30}(orbitari\|órbita)` aparece em 3+ formas distintas, avisar | achado [2] |
| `craneal` e `distal` no mesmo período | achado [3] |
| Nome de metodologia de autor com caixa oscilante no mesmo documento | achado [4] |
| Sigla precedida do substantivo que ela já contém (`ligamento LCC`, `ligamento LRO`) | achado [5] |
| Unidade de medida partida por quebra de linha (`mg/$`) | achado [7] |

Os achados [2] e [3] pedem heurística, não casamento de padrão: valem como aviso
para conferência humana, nunca como bloqueio.

---

## PONTOS PARA ANÁLISE — ordenados por custo de não corrigir

| # | Ponto | Custo se ficar como está |
|---|---|---|
| 1 | **Camadas 2 e 3 não executadas** (falta o original PT) | Desconhecido, e é o único item cujo risco não sei dimensionar. Dose ou plano trocado contra a origem passaria por toda esta revisão sem ser visto. |
| 2 | [1] pág. 12, falta `al` | Erro de gramática visível, em conteúdo, para todo comprador |
| 3 | [2] cinco nomes para o rebordo orbitário | Termo estrutural, base da técnica, repetido |
| 4 | [3] `craneal`/`distal` na pág. 30 | Eixo anatômico inconsistente em material de ensino |
| 5 | [Q1] `orbicular` vs `orbitario` | Contradiz a própria sigla; some se uniformizar |
| 6 | [4] a [7] menores | Acabamento |
| 7 | [Q5] 2 QR para material em português | Experiência do aluno hispano-hablante |

**Os itens 2 a 6 foram aplicados em 23/09/2026.** O item 1 — as camadas 2 e
3 da revisão — continua dependendo do PDF em português; é o único item cujo
risco não sei dimensionar, e a única ressalva que resta nesta entrega.
