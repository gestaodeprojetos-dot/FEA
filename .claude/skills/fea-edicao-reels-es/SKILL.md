---
name: fea-edicao-reels-es
description: Edita Reels de procedimento da FEA (Dr. João Pithon) com legendas e headlines em espanhol latino-americano, no mesmo padrão visual e de cortes da skill fea-edicao-reels, com tradução bloco a bloco sincronizada com a fala, glossário clínico travado e revisão bilíngue para a Keila. Usar quando pedirem vídeos, Reels ou cortes em espanhol, legenda em espanhol, headline ou título em espanhol, versão ES, LATAM, mercado hispano, ou vídeos dublados em espanhol.
---

# FEA: Reels com legenda e headline em espanhol

Tudo o que a skill `fea-edicao-reels` define continua valendo aqui: entrada, cortes, padrão visual, início e fim na fala, sangue, dor, conversa, Parte 1/Parte 2, entrega em H.264 abaixo de 30 MB. **Ler aquela skill antes desta.** Esta acrescenta só a camada de espanhol: tradução da legenda, headline em espanhol e a revisão bilíngue.

Público do vídeo em espanhol: médico e dentista hispano-falante que aplica harmonização. Um termo anatômico trocado, um número diferente ou uma negação perdida na legenda é risco clínico, não erro de estilo.

## Os dois casos

| Caso | Como reconhecer | Legenda |
|---|---|---|
| **A. Áudio em português** (o Dr. fala PT) | brutos normais da FEA | tradução PT → ES bloco a bloco, no tempo exato da fala PT |
| **B. Áudio em espanhol** (vídeo dublado, ou o Dr. falando espanhol) | pasta de dublados, vídeos do YouTube ES | transcrição direto em espanhol (`fea_transcrever.py --idioma es`) |

Na dúvida, ouvir 5 segundos de um bruto antes de transcrever.

## Glossários (carregar antes de traduzir qualquer bloco)

Em `references/`, nesta ordem:
1. `FEA-00-nucleo-es.md` e `FEA-01-voz-y-estilo-es.md`: obrigatórios, sempre.
2. `FEA-11-rellenos-ah-ojeras-es.md` (preenchimento, olheiras, reologia) ou `FEA-15-intercurrencias-es.md` (intercorrência, dose, via), conforme o tema.
3. `FEA-glossario-video-es.md`: fala oral do Dr., termos dos Reels, headlines, campanha e decisões de vídeo.

Termo que não está em nenhum: pesquisar o uso em literatura médica em espanhol, marcar como proposta no doc de revisão e, aprovado, registrar na seção 2 do glossário de vídeo.

## Fluxo (caso A, áudio em português)

1. **Editar normalmente** até os cortes aprovados, como na skill PT (ambiente, download, transcrição PT, `manter`, `silenciar`, `zoom`). O `projeto.json` do lote ES é uma cópia do PT com:
   - `"idioma": "es"` no topo;
   - em cada vídeo: `"titulo"` = headline em espanhol, `"titulo_pt"` = headline original, `"saida"` = `out/N- <headline ES>.mp4`, `"legendas_es"` = `es/N- <headline ES>.json`;
   - `"cartela_final": "Parte 2 en el perfil"` quando houver Parte 1;
   - `"cta"` só se existir CTA gravado em espanhol (nunca colar CTA em português sem a Keila pedir).
   Nome do arquivo: `FEA-edicao-videos/FEA-projeto-<lote>-es.json`.
2. **Exportar as legendas PT** com tempo, já com os cortes finais:
   ```
   python3 FEA-edicao-videos/fea_editar_video.py FEA-projeto-<lote>-es.json --exportar-legendas es/
   ```
   Cada vídeo vira `es/<nome>.json` com os blocos `{id, s, e, seg, pt, es}`. Se o arquivo já existia, a tradução dos blocos que não mudaram é reaproveitada.
3. **Traduzir** preenchendo `"es"` de cada bloco, seguindo as regras abaixo. Ler o vídeo inteiro (todos os `pt`) antes de traduzir o primeiro bloco: o sentido de uma frase costuma atravessar dois blocos.
4. **Headlines**: traduzir cada `titulo_pt` (regras abaixo), gravar no `titulo` do projeto e no `titulo_es` do arquivo.
5. **Prévia**: `python3 FEA-edicao-videos/fea_editar_video.py FEA-projeto-<lote>-es.json --previa` (ou `--entrega`). O render **para** se um bloco estiver sem tradução ou se o PT mudou depois da exportação (cortes mexidos): exportar de novo e traduzir só os blocos novos.
6. **Revisão**: skill `fea-revisao-reels-es` (obrigatória, nunca entregar sem ela).
7. **Doc bilíngue para a Keila** (ver abaixo) e prévias pelo `SendUserFile`.
8. **Final** com as correções dela, revisão de novo, e subida para a pasta de destino.

## Fluxo (caso B, áudio em espanhol)

1. `python3 FEA-edicao-videos/fea_transcrever.py --idioma es tr/ wav/*.wav`
2. `projeto.json` com `"idioma": "es"` e **sem** `legendas_es`: a legenda sai da própria transcrição, com as correções de espanhol (`CORRECCIONES_ES` em `fea_editar_video.py`).
3. Cortes, prévia, revisão e doc como no caso A (no doc, a coluna PT fica vazia ou com a fala original, se houver o vídeo em português).

## Regras de tradução da legenda

**Tempo e bloco**
- Um bloco PT vira um bloco ES, no mesmo tempo. Não mover conteúdo entre blocos, a não ser o mínimo que a sintaxe do espanhol exige; **número, marca e negação ficam no mesmo bloco do PT** (a revisora confere bloco a bloco).
- `"es": "-"` tira o bloco da tela, e só serve para muleta pura ("né?", "tá bom?"). Bloco com número, marca ou mais de 3 palavras nunca pode ser "-".

**Tamanho (legenda precisa dar tempo de ler)**
- Até **2 linhas de 24 caracteres** (26 no limite). O script quebra as linhas, sem separar número e unidade, "Dr. João" ou marca de duas palavras.
- Até **17 caracteres por segundo** (21 é o limite duro). O espanhol corre 10% a 20% mais longo que o português: condensar é obrigatório, e se faz tirando muleta e redundância, **nunca conteúdo clínico** (dose, volume, número, plano, camada, lado, produto, instrumento, negação, advertência de segurança).

**Registro e voz** (detalhes em `FEA-01-voz-y-estilo-es.md` e na seção 1 do glossário de vídeo)
- Usted, nunca tú, vos ou vosotros. "Observe", "fíjese", nunca "mira".
- A técnica do Dr. em 1ª pessoa do plural ("aquí hacemos un bolo"); instrução ao colega no imperativo formal ("evalúe", "aspire").
- Tom médico-científico: a ênfase oral brasileira traduzida ao pé da letra soa infantil em espanhol técnico. "Isso é muito, muito importante" vira "este punto es determinante".
- Não corrigir a clínica do Dr., não acrescentar nem tirar ressalva, não converter unidade. Fala ambígua: traduzir mantendo a ambiguidade e levar à Keila.

**Ortotipografia** (o script corrige parte sozinho, a revisora confere tudo)
- ¿...? e ¡...! abrem e fecham (a pergunta pode abrir num bloco e fechar no seguinte).
- Decimal com vírgula ("0,2 mL"), milhar com ponto, porcentagem com espaço ("70 %"), "mL", "G’" e "G’’" com apóstrofo curvo, "cánula 22x70".
- Sem travessão (regra FEA vale acima da raya do espanhol): vírgula, dois-pontos ou parênteses.
- Mesmo padrão visual do PT: começa minúscula (salvo nome próprio ou sigla), sem ponto final.
- Marca, sigla e protocolo de autor nunca traduzem.

## Regras da headline em espanhol

- Mesmo visual do PT. Maiúscula só na primeira palavra e em nome próprio, marca ou sigla (o espanhol não usa Title Case).
- Traduzir o **gancho**: mesma promessa técnica, mesmo tom médico-científico, sem urgência nem promessa de resultado estético. Exemplos na seção 3 do glossário de vídeo.
- Até 3 linhas. Se não couber, encurtar a frase, não a fonte.
- Headline que a Keila escrever em espanhol vale exatamente como ela escreveu.
- Contagem regressiva: "Faltan N días" / "Falta 1 día". Cartela da Parte 1: "Parte 2 en el perfil".

## Doc de revisão bilíngue para a Keila

A Keila lê português; o doc precisa deixar ela aprovar o espanhol sem depender de ler espanhol fluente. Google Doc `FEA-revision-legendas-es-<lote>` na pasta de destino, com:

1. **No topo, os pontos para decidir**: headlines adaptadas (não literais), termos novos fora do glossário, falas com afirmação absoluta, CTA e campanha.
2. **Headlines**: tabela PT | ES | por que essa escolha (1 linha).
3. **Legendas por vídeo**: tabela `[mm:ss] | PT | ES`.
4. **Back-translation** dos blocos técnicos (os que a revisora lista): o ES traduzido de volta para o português, ao lado do PT original, para ela ver que o sentido clínico não mudou.

## Pontos para sempre levar à Keila (além dos da skill PT)

- Headline que precisou de adaptação (não é tradução literal).
- Termo técnico sem entrada nos glossários.
- CTA e frases de campanha (seção 4 do glossário de vídeo, todas "a confirmar").
- Vídeo com CTA em português colado no final: pedir o CTA em espanhol ou tirar.
- Afirmação absoluta de resultado ou segurança: a mesma regra de compliance do PT vale em espanhol; o público hispano também é regulado no país de cada profissional, e não inventamos regra de país nenhum.

## Armadilhas

- Traduzir antes de fechar os cortes: cada corte novo muda os blocos. O render trava (é de propósito); reexportar e traduzir só o que mudou.
- Traduzir bloco a bloco sem ler o vídeo inteiro: frase partida entre dois blocos sai com a sintaxe do português.
- Confiar na legenda PT como fonte da verdade: ela passou por correções (ex.: "prédio" virou pré-jowl). Na dúvida sobre o que o Dr. disse, ouvir o trecho.
- Espelhar a muleta ("entonces", "¿sí?") em todo bloco: some com ela, a legenda fica mais curta e mais técnica.
- `fea_revisar.py` sozinho não basta no vídeo em espanhol: ele confere formato, tempo e cortes; o texto ES é da `fea_revisar_es.py` e da revisão cega.

## Quando a Keila pedir uma regra nova de espanhol

Registrar nos 3 lugares: nesta skill (ou no glossário de vídeo, se for termo), em `fea_revisar_es.py` (`ARMADILHAS`, `FALSOS_AMIGOS` ou teste novo) e na tabela da skill `fea-revisao-reels-es`.
