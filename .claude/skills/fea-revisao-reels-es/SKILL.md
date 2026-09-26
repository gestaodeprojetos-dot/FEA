---
name: fea-revisao-reels-es
description: Revisora rigorosa dos Reels da FEA (Dr. João Pithon) com legenda e headline em espanhol, antes da entrega. Roda a revisão técnica da skill fea-revisao-reels (formato, tempo, cortes, sincronia) e acrescenta a revisão do espanhol como par especialista, feita às cegas: resíduo de português, glossário clínico, falsos amigos, número, negação e marca iguais ao PT bloco a bloco, ¿? e ¡!, tamanho e velocidade de leitura, headline e back-translation dos trechos técnicos. Usar sempre depois de editar com fea-edicao-reels-es e quando pedirem para revisar, conferir ou auditar vídeos, legendas ou headlines em espanhol.
---

# FEA: revisão rigorosa de Reels em espanhol

Nenhum vídeo em espanhol vai para a Keila sem passar pelas 4 partes abaixo, nesta ordem. Qualquer ERRO devolve o vídeo para a edição; cada ATENÇÃO é corrigida ou justificada por escrito.

1. **Técnica** (skill `fea-revisao-reels`): formato, título, tempo da legenda, sincronia com a voz, cortes, começo e fim, sangue, dor, conversa. O script entende `"idioma": "es"` e pula só as regras de texto em português.
2. **Espanhol automático**: `fea_revisar_es.py`.
3. **Espanhol às cegas**: um revisor que não traduziu lê PT e ES lado a lado.
4. **Visual**: quadros com a legenda em espanhol na tela.

## Como rodar

```
python3 FEA-edicao-videos/fea_revisar.py FEA-projeto-<lote>-es.json --folhas folhas/
python3 FEA-edicao-videos/fea_revisar_es.py FEA-projeto-<lote>-es.json
```

`fea_revisar_es.py` recalcula as legendas PT a partir do áudio para garantir que a tradução é do corte atual. Sem os brutos na máquina, `--sem-audio` confere só o arquivo de tradução e o `.ass`.

## Checklist do espanhol (o que cada regra exige)

| # | Regra | Como é conferida | Nível |
|---|---|---|---|
| E1 | Todo bloco traduzido, e traduzido do corte atual | arquivo `legendas_es` contra as legendas PT recalculadas | ERRO |
| E2 | Número igual ao PT (dose, volume, calibre, unidade) | algarismos de cada bloco PT e ES | ERRO (Classe A) |
| E3 | Negação do PT presente no ES ("não", "nunca", "sem") | palavras de negação por bloco | ERRO (Classe A) |
| E4 | Marca, sigla e protocolo iguais ao PT | lista de marcas e siglas por bloco | ERRO (Classe A) |
| E5 | "-" (bloco fora da tela) só em muleta pura | bloco "-" com número, marca ou mais de 3 palavras | ERRO |
| E6 | Nada de português: letra (ã, õ, ç, â, ê, ô, à) ou palavra ("você", "não", "com", "região"...) | texto da tela | ERRO |
| E7 | Armadilhas do glossário (zigomático, camada, tecido, sulco, pálpebra, têmpora, harmonización, hialurônico, vitalícia, canula sem acento...) | texto da tela e título | ERRO |
| E8 | ¿...? e ¡...! com par, inclusive entre dois blocos | sequência de blocos e título | ERRO |
| E9 | Sem travessão/raya (regra FEA) | texto | ERRO |
| E10 | "70 %", decimal com vírgula, "mL", "G’" | texto | ERRO |
| E11 | Máximo 2 linhas, linha até 26 caracteres (24 ideal) | `.ass` | ERRO (26) / ATENÇÃO (24) |
| E12 | Leitura: até 17 caracteres/s (21 é o limite duro) | texto / duração do bloco | ERRO (21) / ATENÇÃO (17) |
| E13 | Mesmo padrão visual: sem ponto final, começa minúscula | texto | ERRO / ATENÇÃO |
| E14 | Usted (decisão de João Pithon, 20/08/2026) | formas de tú e vos | ATENÇÃO |
| E15 | Falsos amigos (señal, encaminar, acompañamiento, largo, descartar, complicación, filo, bigote chino...) | texto | ATENÇÃO |
| E16 | Headline: maiúscula só na 1ª palavra e em nome próprio, gancho preservado, até 3 linhas | título do projeto; revisão cega | ATENÇÃO / revisão manual |
| E17 | Cartela "Parte 2 en el perfil" | projeto | ERRO |
| E18 | Back-translation dos blocos técnicos | lista impressa pelo script; revisão cega | revisão manual |
| E19 | Sentido clínico idêntico ao PT (plano, camada, lado, estrutura) | revisão cega | revisão manual |
| E20 | Registro médico-científico, sem ênfase oral traduzida ao pé da letra | revisão cega | revisão manual |

Número, negação e marca são **Classe A** (barreira clínica, como no catálogo de tradução): tolerância zero. Nos vídeos todo ERRO bloqueia a entrega, porque o texto de legenda é curto e a correção é barata.

## Revisão cega (obrigatória)

Quem traduz acumula razões para as próprias escolhas, e essas razões cegam para o erro. Por isso a revisão de sentido é feita por um **subagente** (ferramenta Agent) que recebe só:
- o arquivo `es/<vídeo>.json` (PT e ES bloco a bloco) e as headlines PT e ES;
- os glossários de `.claude/skills/fea-edicao-reels-es/references/`;
- esta tabela de checklist.

Nada de justificativa de tradução. Pedir ao subagente, por vídeo:
1. back-translation dos blocos técnicos (lista do script) e divergência de sentido com o PT;
2. termo fora do glossário ou em desacordo com ele;
3. frase que soa traduzida (lusismo sintático, gerúndio de posterioridade, "el mismo" como pronome, "a nivel de");
4. headline: o gancho em espanhol promete o mesmo que o PT? tom médico-científico? cabe em 3 linhas?
5. veredito: LIBERADO ou lista de correções.

Escolha que só se sustenta com justificativa vai para o glossário de vídeo (seção 5, decisões), não para uma explicação avulsa.

## Revisão visual

Na folha de contato (`--folhas`) e em 3 quadros por vídeo (começo, meio e fim, no início de uma legenda):
- acento, ñ, ¿ e ¡ desenhados certo (Montserrat cobre todos; se aparecer quadrado, a fonte não carregou);
- legenda inteira na tela, sem linha cortada, no máximo 2 linhas;
- o texto do quadro corresponde ao que o Dr. fala naquele segundo (sincronia herdada do PT);
- headline em 3 linhas ou menos, centralizada.

## Como resolver cada achado

- **Leitura rápida demais ou linha longa:** condensar tirando muleta e redundância; conteúdo clínico nunca sai. Se ainda não couber, juntar o sentido com o bloco vizinho mantendo número, marca e negação no bloco original.
- **Número diferente:** voltar ao PT e ao áudio; o ES espelha o que o Dr. disse, sem arredondar nem converter.
- **Negação sumiu:** reescrever o bloco; nunca liberar.
- **Tradução velha:** `--exportar-legendas` de novo; a tradução dos blocos que não mudaram volta sozinha, traduzir só os novos.
- **Falso amigo ou tú:** ler o contexto; "descartar un diagnóstico" está certo, "descartar la aguja" é "desechar".
- **Title Case na headline:** passar para maiúscula só na primeira palavra, a não ser que a Keila tenha escrito assim.

## Antes de entregar

- [ ] `fea_revisar.py` com 0 ERRO em todos os vídeos.
- [ ] `fea_revisar_es.py` com 0 ERRO em todos os vídeos.
- [ ] Cada ATENÇÃO resolvida ou justificada.
- [ ] Revisão cega feita por subagente, com back-translation dos blocos técnicos, e correções aplicadas.
- [ ] Quadros com legenda ES olhados (acentos, ñ, ¿¡, 2 linhas).
- [ ] Doc bilíngue `FEA-revision-legendas-es-<lote>` pronto, com os pontos para decidir no topo.
- [ ] Termos e decisões novos registrados no glossário de vídeo.
- [ ] Relato para a Keila: o que a revisão corrigiu, vídeo por vídeo.

## Quando a Keila pedir uma regra nova

Registrar nos 3 lugares: na skill `fea-edicao-reels-es` (ou no glossário de vídeo, se for termo), em `fea_revisar_es.py` e na tabela acima.
