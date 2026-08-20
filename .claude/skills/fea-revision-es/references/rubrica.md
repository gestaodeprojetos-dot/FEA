# Rubrica de revisão — critérios de aceitação

Referência para classificar achados sem hesitar. Em dúvida entre duas
severidades, escolha a mais alta.

## BLOQUEANTE — não publica

- Dose, concentração, unidade ou posologia divergente do original.
- Via de administração trocada (`EV` mantido em vez de `IV`; `IM` por `IV`).
- Nome de fármaco incorreto (`triancinolona`, `clavulanato`).
- Plano anatômico, camada ou profundidade trocada.
- Lado ou sentido invertido: medial/lateral, craneal/caudal, superior/inferior.
- Ordem dos passos de uma técnica alterada.
- Negação perdida ou acrescentada («no aplicar» → «aplicar»).
- Contraindicação, alerta ou critério de emergência omitido ou suavizado.
- Falso amigo que muda o sentido clínico: `señal` por `signo`,
  `descartar la aguja` por `desechar la aguja`.
- Sigla de autor quebrada (ARTI, PDRR, ETIP, HPI, NOIA deixando de fechar).
- Tuteo ou voseo em material de registro formal.
- Ênclise em verbo finito (`aplicase`), mesóclise, futuro do subjuntivo.
- Trecho do original simplesmente ausente na tradução.

## GRAVE — corrige antes de publicar

- Termo divergente do glossário sem decisão registrada em `90-decisiones.md`.
- **Inconsistência interna:** o mesmo termo traduzido de duas formas no mesmo
  material. Registre todas as ocorrências, não só a primeira.
- Lusismo sintático: `el mismo` como pronome, `a nivel de` por `en`,
  `en base a`, `casos donde`, `hubieron`.
- Falta o «a» de objeto direto de pessoa (`evaluar el paciente`).
- Citação bibliográfica, abstract ou legenda de figura de terceiros traduzida
  quando deveria permanecer em inglês.
- Marca ou princípio ativo traduzido ou com grafia alterada.
- Unidade sem espaço (`20mg`), pluralizada (`20 mgs`), decimal com ponto.
- Registro oscilante dentro do mesmo material.
- Texto embutido em arte não inventariado (exige OCR para afirmar).

## MENOR — corrige se houver tempo

- Falta `¿` ou `¡` de abertura.
- Aspas retas em vez de `«…»`; hífen em vez de raya em prosa.
- Percentual sem espaço (`70%`).
- Título de seção em Title Case à moda portuguesa.
- Conector repetitivo; gerúndio de posterioridade isolado.
- Intensificador redundante herdado do português (`totalmente seguro`).
- `Ud.` em vez de `usted` na prosa.

## QUESTÃO AO AUTOR — não é erro de tradução

- O original é ambíguo e qualquer leitura muda o sentido clínico.
- O original se contradiz entre duas passagens.
- O original tem erro próprio (dose improvável, termo trocado, texto perdido
  entre páginas).
- Um dado técnico está incompleto no original (valor faltando em série).
- Há tensão lógica entre dois trechos que o leitor atento vai notar.
- Decisão editorial: traduzir ou não rótulo em arte de terceiros; destino de
  QR Code; uniformizar denominação que o original varia.

## Como calcular o veredito

Duas perguntas, nesta ordem. A primeira tem precedência absoluta.

**1. Há achado de classe A (BLOQUEANTE)?**
Se sim → `RETIDO`. Fim. Não calcule índice, não pondere, não relativize.
Segurança clínica não entra em média.

**2. Qual o índice de classe B?**

```
índice = segmentos sem achado GRAVE/MENOR / segmentos totais × 100
```

| Classe A | Índice classe B | Veredito |
|---|---|---|
| ≥ 1 | qualquer | **RETIDO** |
| 0 | ≥ 95 % | **LIBERADO** |
| 0 | 80 % a 95 % | **LIBERADO COM RESSALVAS** — a entrega segue |
| 0 | < 80 % | **RETIDO** |

Limiares configurados em `fea-traduccion-es/scripts/auditar.py`
(`LIMIAR_LIBERA = 95.0`, `LIMIAR_MINIMO = 80.0`). Alterá-los é decisão do autor
e vai para `90-decisiones.md`.

### Regras de contagem

- **Segmento** = parágrafo ou rótulo com mais de dois caracteres. Bloco marcado
  «SE CONSERVA EN INGLÉS» não conta, nem no numerador nem no denominador.
- **Segmento com mais de um achado conta uma vez** no índice — o índice mede
  quantos parágrafos o leitor encontraria com problema, não quantos problemas
  existem. A densidade por mil palavras é que mede volume; reporte as duas.
- **Inconsistência interna conta por ocorrência, não por termo.** Se o mesmo
  termo aparece traduzido de duas formas em 40 lugares, são 40 segmentos
  sujos. É o achado que o aluno mais percebe e o que menos aparece se contado
  como «um problema».
- **Falso positivo do auditor não conta.** Mas precisa ser nomeado no relatório
  com a regra proposta, senão o auditor perde credibilidade e passa a ser
  ignorado.

### O que o índice não mede

O índice é editorial. Ele **não** cobre: fidelidade de sentido em trecho longo,
ordem dos passos de uma técnica, tensão lógica do original, adequação cultural.
Isso é a camada 3 (back-translation) e a camada 4 (voz nativa), que são
julgamento — e cujo resultado, quando encontra defeito, entra como classe A
(se muda o sentido clínico) ou classe B (se é só estilo).

Nunca reporte índice alto como se fosse aprovação de conteúdo. O índice diz
«o texto está limpo», não «o texto diz a mesma coisa que o original».
