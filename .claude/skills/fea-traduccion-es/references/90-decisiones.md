# Registro de decisões terminológicas

Cada decisão aqui é definitiva até que o autor a mude. O objetivo é não
rediscutir a mesma escolha a cada material traduzido.

## Variante e registro
- **Espanhol LatAm neutro.** Tratamento formal (usted) ao leitor profissional.
  Definido por João Pithon em 20/08/2026.

## Termos de autor conservados
| Termo | Decisão | Por quê |
|---|---|---|
| `pertuito` | Conservado, glosado na 1ª aparição | Termo de autor; o próprio artigo em inglês do autor usa *pertuit* |
| `metodologia ARTI` | Conservado | Sigla fecha em ES: Anatomía, Reología, Técnica, Intercurrencias |
| `método 3TC` | Conservado | Marca metodológica do autor |
| `anestesia SANPE` | Conservado | Marca metodológica do autor |
| `Protocolo PDRR` | Traduzido, sigla mantida | Protocolo de Diagnóstico y Reperfusión Rápida — sigla fecha em ES |
| `Protocolo de Segurança PithonNapoli` | Traduzido, nome mantido | Protocolo de Seguridad PithonNapoli |

## Escolhas com alternativa descartada
| PT | Escolhido | Descartado | Por quê |
|---|---|---|---|
| intercorrências | **intercurrencias** | complicaciones | Preserva a sigla ARTI; e "complicaciones" já traduz *complicações*, que o autor usa como termo distinto |
| Swelling Factor | **Swelling Factor** (inglês) | factor de hinchazón | A literatura de reologia em espanhol conserva o inglês; glosado na 1ª aparição |
| G' | **módulo elástico (G')** | módulo de almacenamiento | Uso mais frequente na literatura estética em ES |
| goteira lacrimal | **gotera lagrimal** | canal lagrimal | "Gotera" é uso anatômico legítimo em ES (cf. gotera bicipital) |
| fios de tração | **hilos tensores** | hilos de tracción | "Tensores" é o termo consolidado no mercado hispano-americano |

## Pendências que precisam de decisão do autor
| Item | Situação |
|---|---|
| `ligamento de retenção orbicular` vs. `orbitária` | O ebook de olheiras usa as duas formas para a mesma estrutura (pág. 12 e 34). Espelhei o original na tradução. **Recomendo uniformizar para *orbitario* nos dois idiomas.** |
| `ultrassom microfocado` | Traduzido como *ultrasonido microenfocado*, marcado `[a confirmar]` — inferido de título de aula, sem o conteúdo do módulo à vista |
| Destino dos QR Codes | Apontam para material em PT/EN. Decidir se troca para versão ES ou se a legenda avisa o idioma |

## Critério de aceitação da entrega

Definido por João Pithon em 20/08/2026: **a entrega não fica atrelada a 100 % de
perfeição.**

Implementado em dois níveis separados, porque um percentual único misturaria
coisas incomensuráveis:

| Nível | Escopo | Critério |
|---|---|---|
| **Classe A — barreira clínica** | dose, via, fármaco, plano, lado, negação, omissão, sigla de autor, tratamento | Tolerância zero. Fora do percentual. Um achado retém. |
| **Classe B — índice editorial** | terminologia, lusismo, ortotipografia, registro | `LIBERADO` ≥ 95 % · `COM RESSALVAS` 80–95 % · `RETIDO` < 80 % |

**Por que 80 % ficou como piso e não como linha de liberação:** medido no ebook
de olheiras (308 segmentos, 8.056 palavras), um índice de 80 % toleraria 61
segmentos com achado — um parágrafo problemático a cada cinco. O índice
observado com glossário travado e auditor rodando foi de 100 %. Logo, 95 % já
é folga real, e a faixa 80–95 % cumpre o objetivo de não travar entrega por
imperfeição: nela o material **sai**, com os pontos para análise anexos.

Limiares em `scripts/auditar.py`: `LIMIAR_LIBERA = 95.0`, `LIMIAR_MINIMO = 80.0`.

Em todos os vereditos — inclusive `LIBERADO` — o relatório traz o bloco
**PONTOS PARA ANÁLISE**, ordenado por custo de não corrigir.

## Fonte e tipografia dos PDFs

**Completar a fonte, nunca substituí-la.** O corpo dos PDFs da FEA usa
GuardianTextEgyp embutida como subconjunto de 82 a 89 glifos — só o que o
português usa. Faltam `ñ Ñ Ó Í Ú ü • —`. Trocar a fonte alteraria a tipografia
de 49 páginas de texto; por isso `scripts/completar_fonte.py` **monta os glifos
faltantes a partir dos que a própria fonte já tem**:

| Glifo | Como é montado |
|---|---|
| `ñ Ñ` | base `n`/`N` + til isolado de `ã` |
| `Ó Í Ú Á É` | maiúscula + acento isolado de `ó`/`í`/`ú`, escalado a 0,92 |
| `ü` | `u` + dois pontos derivados de `period` |
| `—` | `endash` ou `hyphen` alongado até 1 em |
| `•` | copiado do peso irmão que já o tem |
| `D J , ; “ ” k 7` no negrito | doados do Regular e engrossados sinteticamente |

Detalhe que custou depuração: para o `Í`, a referência de altura é `n`, não `i` —
o pingo do `i` falseia a detecção do acento.

**Aspas `“ ”`, não `« »`.** Decisão técnica: a fonte tem as curvas nativas e não
tem guillemets. Sintetizar guillemets a partir do sinal de maior gera glifo
pequeno e desalinhado — testado e descartado. Aspas curvas são igualmente
corretas em espanhol latino-americano.

**Apóstrofo curvo `G’`.** `quoteright` existe na fonte; o apóstrofo reto não.
Aplicado às 25 ocorrências de notação reológica da tradução.

**Resultado verificado:** cobertura completa do texto ES no corpo e no negrito
inline. O único glifo não sintetizável, o dígito `6`, aparece apenas em títulos
em HelveticaNeue-Bold, que tem 2.080 glifos e cobre tudo.
