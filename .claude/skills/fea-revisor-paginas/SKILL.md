---
name: fea-revisor-paginas
description: Revisor criterioso de páginas da FEA com o olhar do Luca (estrategista dono do projeto). Usar SEMPRE antes de entregar, mostrar, pedir aprovação ou dizer "pronto" sobre qualquer página, landing page, captura, vendas, obrigado, onboarding, Zoom, migração do WordPress, prévia de branch, artefato de design de página ou código de página da FEA (lp.joaopithon.com.br, subdomínios fep, feb, bio, eb, ctx, pl, bf, joaopithon.com.br). Também ao revisar página feita pelo André ou por outra IA. Dá nota de 0 a 100 com checklist de pesos e veredito.
---

# FEA · Revisor de páginas (olhar do Luca)

Objetivo: nenhuma página da FEA sai feia, ruim, quebrada ou fora do padrão. O revisor olha a página como o Luca olharia no celular dele, antes que ele precise pedir o ajuste. Ele aprende com três fontes: os pedidos do Luca às páginas, o que o André mudou em resposta e os padrões da empresa (CLAUDE.md do projeto FEA e do repositório `lp-joaopithon`).

Base de aprendizado (ler antes da primeira revisão da sessão): `referencias/FEA-aprendizado-luca-andre.md` (31 pedidos e 12 princípios).

## Quando usar

- Antes de dizer "pronto", "no ar", "ok" ou de mandar link de página ou prévia a qualquer pessoa (Gestão FEA, André, Luca, time).
- Depois de cada rodada de ajuste: a página volta ao revisor inteira, não só o trecho alterado.
- Em migração do WordPress para o código, em página nova, em teste A/B e em ajuste pontual (troca de link, data, texto, foto).

## Princípio número 1 (André, 25/11/2026)

**Migração de página é cópia fiel do original do WordPress**: estrutura, ordem das seções, CSS, espaçamentos, fontes, cores, imagens, textos e links do original, medidos lado a lado. Nunca visual reinterpretado, "melhorado" ou redesenhado (a FEB de vendas migrada assim ficou "extremamente ruim"; a FEP feita como cópia fiel ficou certa). Correções de conteúdo (número de alunos, link quebrado, data vencida) entram por cima da cópia fiel e são listadas à parte.

**Página nova segue a referência visual do Luca** (artefato de briefing, print com marcações, site modelo como o NDZ ou docustoaolucro.com/sessao), com ajuste fino do André. Toda página nova sai em branch + artefato no Claude Design idêntico ao branch, para o André lapidar (regra do André, 25/11).

## Processo de revisão

1. **Reunir a referência.** Briefing ou artefato do Luca, print com marcações, página original do WordPress (se for migração), planilha de Links úteis do evento (aba WEB DESIGNER e GERAL), briefing do lançamento. Sem referência, a nota de fidelidade vale no máximo metade e isso é dito no relatório.
2. **Varredura automática.** Rodar o script:
   ```
   node .claude/skills/fea-revisor-paginas/referencias/fea_revisar_pagina.js <URL> <pasta-no-scratchpad> [--latam]
   ```
   Ele abre em 390 px (celular, tela 2x) e 1440 px, rola até o fim, tira print de página inteira e da primeira dobra, lista rolagem lateral, imagens quebradas, erros de console, pedidos que falharam, todos os links e botões com status HTTP, checkout sem `off=`, âncora morta, travessão, "pra", marcas proibidas, números antigos, "Dr. João" sem "Pithon", "R$" separado do número, SEO, GTM, VK e Clarity. Gera `relatorio.md` e `relatorio.json`. Não clica em checkout nem envia formulário (bloqueia GTM, Clarity, pixels e `proc.php`).
3. **Olhar os prints, seção por seção.** Abrir com Read os prints `celular-390-primeira-dobra.png`, `celular-390-inteira.png` (se for muito alta, recortar em fatias de ~1600 px com Python/PIL antes de abrir) e `computador-1440-*.png`. Para cada seção: hierarquia, alinhamento, espaçamento, quebra de linha, foto, contraste, botão. Anotar o que o Luca pediria.
4. **Larguras extras quando houver risco.** Topo, selos e títulos de 1 linha: conferir também 320, 360, 430 e 768 px e no WebKit (`require('playwright').webkit`), porque o Safari desenha a fonte cerca de 8% mais larga (pedido 23).
5. **Comparar com a referência.** Migração: abrir o original do WordPress nas mesmas larguras e comparar print a print (mesma ordem, mesmo espaçamento, mesmo texto). Página nova: comparar com o artefato do Luca bloco a bloco.
6. **Testar CTAs de verdade, sem comprar.** Abrir a página com `?utm_source=teste&utm_medium=teste&utm_campaign=teste&xcod=AB12` e conferir o href final de cada botão (checkout com `off=` certo, utm e sck repassados, sem `sck` fixo). Checkout da Hotmart: abrir no navegador e ver o produto e a oferta (o curl leva desafio anti-robô). WhatsApp: número e mensagem pronta. Grupo: abrir a campanha Sendflow e ver o nome do grupo atual. Formulário: nunca enviar (cria lead real); interceptar o envio.
7. **Pontuar o checklist abaixo**, aplicar os bloqueios automáticos e dar o veredito.
8. **Corrigir e reavaliar** até chegar a 95 ou mais. Só então entregar, com a nota e o resumo do revisor.

## Checklist com pesos (100 pontos)

Cada critério: o que verificar · como verificar · o que o Luca pediria. Critério parcialmente atendido leva nota proporcional.

### A. Fidelidade ao briefing ou à referência (20)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| A1 Estrutura | 8 | Todas as seções do briefing, na ordem; migração com a mesma estrutura do original | Lista de blocos do briefing x print inteiro; original WordPress lado a lado | "Faltou o bloco X", "não era essa ordem" |
| A2 Textos e números do briefing | 6 | Headline, subtítulo, botões, preços e provas exatamente como aprovados | Comparar texto a texto com o briefing ou doc de copy | "Esse não é o texto que eu mandei" |
| A3 Referência visual | 6 | Página nova reproduz a solução da referência (chips de data, rótulo com fios, slider de antes e depois); migração sem reinterpretação | Print da referência x print da página na mesma largura | "Fica igual à referência", "por que mudou o visual?" |

### B. Visual e hierarquia (20)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| B1 Primeira dobra | 5 | Logo discreta (não compete com a headline), foto, data e local em chips com ícone, informação que remove a objeção ("presencial e gratuito"), promessa e botão visíveis cedo no celular | Print `celular-390-primeira-dobra` | "Logo menor", "subir o botão", "faltou o PRESENCIAL E GRATUITO" |
| B2 Fotos e rostos | 4 | Rosto do Dr. João Pithon e de paciente inteiro, fora do degradê, sem colar no texto, fiel (sem acessório exagerado, sem IA deformando); foto nítida, sem ampliação visível | Prints de 320 a 430 px; abrir a imagem original | "Está cortando o rosto da paciente", "diminui o relógio", "o rosto não ficou fidedigno" |
| B3 Identidade do produto | 3 | Cores, fontes e componentes da sala do produto (Elite, Black, PLX, CTX, FEP...); elementos de campanha com a identidade da campanha ativa; nome da marca escrito junto do símbolo | Comparar com a página mais recente da mesma marca no repositório | "Precisa estar escrito Elite ali" |
| B4 Tipografia e quebra de linha | 4 | Título no número de linhas desenhado; selo sem terceira linha; sem palavra solta (viúva); "R$" colado ao número; texto mínimo de 11 px no celular | Prints em 320, 360, 390, 430 e WebKit; achado "R$" do script | Print circulando o selo quebrado |
| B5 Espaçamento, alinhamento e contraste | 2 | Respiro regular entre seções, centralização e margens iguais, texto do botão no centro, contraste legível | Print inteiro; medir com `getBoundingClientRect` quando houver dúvida | "Está desalinhado", "ficou apertado" |
| B6 Nada quebrado no celular | 2 | Sem rolagem lateral, sem sobreposição, botão flutuante de WhatsApp não cobre o botão de compra, carrosséis funcionam | Achados do script; print inteiro; rolar no 390 | "No meu celular está quebrado" |

### C. Copy e tom (12)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| C1 Escrita FEA | 4 | Sempre "para", nunca "pra"; zero travessão (U+2014) e meia-risca usada como travessão; sem palavra-tell; "Dr. João Pithon" por extenso | Achados do script + leitura | "Sem travessão", "Dr. João Pithon, sempre" |
| C2 Tom médico-científico | 3 | Linguagem de par profissional, foco em segurança e técnica, nada de tom popular ou motivacional; público técnico ("profissionais habilitados") | Leitura seção a seção | "Isso parece curso raso" |
| C3 Compliance (linha vermelha) | 3 | Sem marca de toxina, ácido hialurônico ou bioestimulador sem aprovação; sem promessa de resultado estético; sem minimizar risco; aviso de profissional habilitado quando o briefing pede | Achados do script + leitura | (reprova automática, ver abaixo) |
| C4 Urgência e escassez reais | 2 | Lote, vagas, prazo e percentual batem com o briefing e com a planilha; nada fabricado | Conferir briefing e `src/config/` | "Esse percentual está certo?" |

### D. Prova social (8)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| D1 Números oficiais | 4 | 52.754 alunos é o total geral do Dr. João Pithon; 44 países; mililitros conforme o briefing (+7.000 ml ou +12.000 ml); nenhum número antigo (35 mil, 30.000, 20.000, 10.000, 19 países, "quase 100%") | Achados do script + briefing | "Troca para 52.754 em tudo" |
| D2 Depoimentos | 4 | Prints originais, na ordem do briefing, com grifo na frase principal, autorizados (pastas do Drive ou ok da Grazi); alcance separado de resultado; legenda curta com número em negrito; antes e depois só com imagem autorizada, nunca IA | Print das seções de prova; origem das imagens | "Separa os prints de alcance dos depoimentos" |

### E. CTAs e links (15)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| E1 Checkout | 6 | Todo botão de compra leva ao checkout certo do produto e do lote, com `off=` correto, utm e sck repassados, sem `sck` fixo; abre na Hotmart sem erro | Tabela de links do script; abrir no navegador | (checkout errado reprova automaticamente) |
| E2 Botões sem destino | 3 | Nenhum `href="#"`, vazio, âncora sem alvo, link com texto no lugar da URL, link de prévia (`workers.dev`) | Achados do script | "Esse botão não faz nada" |
| E3 WhatsApp, grupos, Zoom, área de membros | 4 | Número oficial do momento; mensagem pronta com "para"; grupo Sendflow do evento certo (não de outro lançamento); Zoom da edição atual; área de membros do produto certo | Abrir cada link; conferir na planilha de Links úteis | "O botão de suporte é este link" |
| E4 Coerência | 2 | Mesmo objetivo, mesmo destino e mesma frase de botão em toda a página; no modelo low ticket do Luca, sem botão de compra na primeira dobra | Tabela de links | "Todos os botões para o mesmo formulário" |

### F. Rastreamento (8)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| F1 Tags da sala | 3 | GTM `GTM-PFCMG8V3` no head e noscript no body; VK do tipo certo (captura ou vendas); Clarity do projeto | SEO e rastreamento do script; HTML gerado | "O Saar precisa trackear" |
| F2 UTMs e eventos | 3 | Parâmetros repassados nos botões; evento no dataLayer por botão, com `utm_source` e `utm_campaign`, sem dado pessoal | Abrir com UTMs de teste; `window.dataLayer` no console | "Consigo saber de onde veio a venda?" |
| F3 Formulário e webhook | 2 | Formulário com webhook ou destino definido (planilha de Links úteis), leads chegando, sem lead de teste real | Conferir planilha e código; interceptar envio | "O lead está chegando?" |

### G. Brasil e Latam (7)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| G1 Versão espanhol completa | 4 | Toda página Brasil tem a versão Latam equivalente, 100% em espanhol (popup, rodapé, botões, mensagem do WhatsApp, `lang="es"`), sem português esquecido | Rodar o script com `--latam` | "Cadê a Latam?" |
| G2 Pagamento Latam | 3 | Sem boleto, pix, "pago pendiente" ou "pago vencido"; preço em US$ quando for o caso; checkout Latam | Achados do script com `--latam` | (boleto/pix no Latam reprova a página) |

Página só Brasil por decisão registrada: G vale integral, com a decisão citada.

### H. Técnico (10)

| Critério | Pts | O que verificar | Como verificar | O que o Luca pediria |
|---|---|---|---|---|
| H1 Sem erro | 3 | Status 200; zero erro de console e pedido falho (imagem 404, fonte, script) | Achados do script | "Tem imagem quebrada" |
| H2 Imagens otimizadas | 2 | WebP/AVIF, menos de 300 KB, width e height, lazy abaixo da dobra, foto do topo com prioridade, cada largura baixa só a sua | Achados do script; aba de rede | "Está demorando para abrir" |
| H3 Desempenho | 2 | Lighthouse mobile sem GTM 90 ou mais (padrão do site 96 a 100); CLS 0 carregando e rolando | Lighthouse 3 rodadas | "A página está pesada" |
| H4 SEO básico | 2 | title de 2 a 4 palavras com o produto, description, og:image 1200x630 (link no WhatsApp com imagem), canonical do domínio final, um h1, noindex em captura, obrigado e teste | Achados do script | "O link no WhatsApp saiu sem imagem" |
| H5 Repositório | 1 | `npm run build` sem erro, só a página nova mudou no `dist/`, regra `no-cache` no `public/_headers`, trabalho em branch | Checklist da seção 9 do `docs/GUIA-NOVA-PAGINA.md` | (o André confere) |

Soma: A 20 + B 20 + C 12 + D 8 + E 15 + F 8 + G 7 + H 10 = 100.

## Reprova automática (nota não importa)

- Qualquer item da linha vermelha: marca de toxina, ácido hialurônico ou bioestimulador sem aprovação; promessa de resultado estético garantido; risco minimizado; conteúdo técnico para leigo; imagem de IA como antes e depois ou como foto clínica.
- Link de checkout errado: produto, lote ou `off=` diferente do briefing, checkout de outro produto, checkout com erro na Hotmart, botão de compra sem destino.
- Grupo, Zoom ou WhatsApp levando a outro evento.
- Boleto ou pix em página Latam.
- Migração com visual reinterpretado (princípio 1).
- Imagem quebrada ou rolagem lateral na primeira dobra do celular.

## Veredito

| Nota | Veredito |
|---|---|
| 95 a 100 | Entrega. Mandar com a nota e a lista do que foi conferido |
| 85 a 94 | Corrige os itens apontados e reavalia a página inteira |
| abaixo de 85 | Refaz (estrutura, referência ou método errados) |

## Formato do relatório do revisor

Curto, em português, sem travessão:

```
Revisor de páginas · <página> · <URL>
Nota: NN/100 · Veredito: entrega | corrige e reavalia | refaz
Reprova automática: nenhuma | <qual>
A Fidelidade NN/20 · B Visual NN/20 · C Copy NN/12 · D Prova NN/8 · E CTAs NN/15 · F Rastreamento NN/8 · G Latam NN/7 · H Técnico NN/10
O que o Luca pediria (em ordem de impacto):
1. ...
Conferido: larguras, navegadores, links testados, prints (caminhos)
```

## Aprender com cada nova rodada

Todo pedido novo do Luca a uma página e toda correção ou direcionamento do André viram uma linha nova em `referencias/FEA-aprendizado-luca-andre.md` (data, página, pedido, o que mudou, princípio). Se o princípio for novo, entra também no checklist acima, no critério certo, com o "o que o Luca pediria" na voz dele. Erro apontado pelo André ou pela gestão depois de uma página aprovada pelo revisor: registrar por que o revisor deixou passar e qual verificação passa a pegar.

Fontes para atualizar: grupo "Web | FEA" (`120363176440560812@g.us`), Daily FEA, Gestão FEA, artefatos de briefing do Luca e o `CLAUDE.md` do repositório `lp-joaopithon` (cada seção registra os ajustes "a pedido do cliente" com data, antes e depois). O histórico de commits da `origin/main` foi achatado em 25/11; os commits novos do André voltam a ser fonte (`git -C /home/user/lp-joaopithon log origin/main -p --author="André"`).

## Fonte pendente: histórico de revisões do WordPress

O WordPress (subdomínios fep, feb, bio, eb, ctx e joaopithon.com.br, Elementor) ainda não tem acesso do agente. Quando o acesso sair (usuário do agente com senha de aplicativo e a linha de `HTTP_AUTHORIZATION` no `.htaccess`, pedidos no Gestão FEA, WEB-386):

1. Credenciais só pelo ambiente (variáveis como `WP_USER` e `WP_APP_PASSWORD`, cadastradas em Network secrets), nunca no código, no chat ou no WhatsApp.
2. Listar as páginas com conteúdo de edição:
   ```
   curl -s -u "$WP_USER:$WP_APP_PASSWORD" "https://<subdominio>.joaopithon.com.br/wp-json/wp/v2/pages?context=edit&per_page=100&status=publish"
   ```
3. Para cada página ativa (inventário em `FEA-inventario-paginas-wordpress-2511.md`), baixar as revisões:
   ```
   curl -s -u "$WP_USER:$WP_APP_PASSWORD" "https://<subdominio>.joaopithon.com.br/wp-json/wp/v2/pages/<ID>/revisions?context=edit&per_page=100"
   ```
   O Elementor guarda o layout no meta `_elementor_data` (JSON); se a revisão não trouxer o meta, comparar o `content.raw` e o HTML renderizado de cada versão.
4. Comparar revisão a revisão (data, autor, o que mudou: texto, imagem, espaçamento, botão, link) e cruzar a data com os pedidos do Luca no grupo Web e no ClickUp.
5. Registrar cada par "pedido do Luca, mudança do André" na tabela do aprendizado e atualizar o checklist.
6. Só leitura: nunca salvar, publicar ou restaurar revisão pelo agente.

Até lá, a cópia fiel de uma migração é medida contra a página pública do WordPress (HTML e prints), como no método da FEP.

## Regra do André para artefatos de design (Daily FEA, 25/11 17h18)

- Prancheta desktop de **1920 px**, com largura útil de conteúdo de **1280 px ou mais** quando a seção pedir.
- Mobile em **390 px**, mas **responsivo de verdade**: conferir em várias larguras (360, 390, 414, 768, 1024, 1280, 1440, 1920), nunca só numa tela fixa. Reprova se quebrar em qualquer largura intermediária.
- Ao finalizar o artefato, avisar a Keila no Gestão FEA para ela compartilhar o link com o webdesign@joaopithon.com.br.

## Links de páginas futuras (regra de 25/11, André + Keila)

Quando alguém pedir o link de uma página ainda não criada: definir o caminho seguindo o guia de links do André (pasta do produto, minúsculas, hífen, barra no fim, `-latam` para a versão Latam, mesmo padrão das páginas irmãs), responder com o endereço avisando que só abre depois da publicação e marcar o André para revisar. Exemplo aprovado: `lp.joaopithon.com.br/plx-latam/obrigado/` e `/plx-latam/onboarding/`.

## Critérios confirmados pelo Luca (26/11/2026, 9h39, privado)

Ao receber os 6 critérios (primeira dobra com foto, data e local, frase que tira a objeção, promessa e botão; celular sem quebra feia e sem rosto do Dr. João Pithon cortado; prova em print original com grifo antes do botão de compra; números oficiais 52.754 alunos e 44 países), o Luca respondeu "isso mesmo". Os pesos acima continuam valendo. Itens 5 (página de referência) e 6 (o que mais incomoda) ficaram sem resposta: perguntar de novo só quando houver página nova para ele revisar.
