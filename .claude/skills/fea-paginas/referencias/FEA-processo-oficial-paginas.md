# FEA: processo oficial de criação de páginas (mapa do André, 23/11/2026)

Resumo do documento "Processo de criação de páginas · Mapa para a gestão". Quando houver conflito entre este arquivo e o SKILL.md, vale este arquivo, e acima dele o CLAUDE.md/AGENTS.md do próprio repositório.

## Onde ficam as páginas

- Repositório: `andrevivas/lp-joaopithon` (GitHub, privado, conta pessoal do André). Projeto em **Astro**.
- Publicação: GitHub conectado ao Cloudflare. **Todo envio para a branch principal vai ao ar sozinho em 4 a 7 min, sem revisão.**
- Prévia: cada branch ou pull request ganha um endereço de prévia no Cloudflare.
- Acesso da gestão (desde 23/11/2026): conta `gestaodeprojetos-dot` com escrita no repositório; app do Claude instalado pelo André só nesse repositório. Cada pessoa liga a própria conta do Claude ao GitHub.
- Alarme: envio à branch principal feito por alguém que não é o André abre um aviso no GitHub e manda e-mail para ele.
- Manual de desfazer: `docs/DESFAZER-PUBLICACAO.md` no repositório.
- Regras para IAs no topo do CLAUDE.md e AGENTS.md do repositório: **nunca publicar pelo terminal (sempre pelo GitHub)**; a pasta `referencias/` é material de versões antigas; há uma tabela de onde ficam links, datas e contatos. Ler esses arquivos antes de qualquer alteração.
- Ferramentas ligadas às páginas: Hotmart (checkout), formulários (Respondi, Google Apps Script), WhatsApp, Zoom, GTM, pixel da VK, Clarity.

## As 11 etapas

| Etapa | O que acontece | Quem faz / aprova |
|---|---|---|
| 1. Pedido e briefing | Objetivo, público, oferta, preços, datas e horários, links (checkout, formulário, WhatsApp, Zoom), pixels e eventos | Gestão e cliente |
| 2. Copy | Textos por seção; números e promessas com fonte | Copy escreve, cliente aprova |
| 3. Pesquisa de design | Referências e moodboard por seção, inventário de materiais reais | André + Claude (chat) |
| 4. Design | Página em 1920 px e 390 px, cada rodada salva como versão (V1, V2...). Etapa mais longa | Claude Design + André |
| 5. Aprovação do estrategista | Luca aprova o protótipo ou pede ajustes (volta à 4) | Luca |
| 6. Pacote para o código | Zip com a página, arquivos-fonte e MUDANCAS.md / AJUSTES.md | André pede ao Claude Design |
| 7. Construção | Componentes, imagens otimizadas, botões, formulários, UTMs, eventos e pixels; em revisões, só o que mudou | Claude Code |
| 8. Testes | Comparação com o design em 7 a 11 larguras (diferença máxima 1 px), sem rolagem lateral, sem a página "pular", botões e UTMs, eventos, velocidade, resto do site inalterado | Claude Code |
| 9. Revisão | André confere prints e relatório: publica, corrige no código ou volta ao design | André |
| 10. Publicação | Envio ao GitHub, publicação automática, conferência no ar | Claude Code, com ordem do André |
| 11. Pós-publicação | Gatilhos no GTM, anúncios por URL, Clarity, viradas de lote, encerramento | Gestão, tráfego e André |

Retornos: Luca pede ajuste (volta à 4); teste falhou (volta à 7); ajuste de design depois do código (volta à 4). Só publica com aprovação do André.

Onde vai o tempo (estimativa do André, só etapas dele): pesquisa 15%, primeira versão 10%, **rodadas de ajuste 40%**, pacote 3%, subir 22%, revisão 5%, pós 5%. O que mais encurta: briefing e copy completos e aprovação rápida.

## Pesquisa (etapa 3) e moodboard

1. Entender o pedido (objetivo, público, etapa do funil, oferta, tom, o que já existe, como o padrão do Elite Mentoring).
2. Partir das seções da copy e do papel de cada uma.
3. Buscar 2 a 4 referências por seção (Awwwards, Land-book, Dribbble, Behance, Mobbin; concorrentes; páginas nossas que converteram).
4. Anotar o que aproveitar e por quê (não copiar).
5. Montar o moodboard com print de celular e computador e o trecho da copy de cada seção.
6. Conferir materiais reais (fotos, depoimentos, números, vídeos que existem de verdade).
7. Escrever o pedido de design por seção: objetivo, conteúdo, referências, regras (celular primeiro, onde ficam os botões, o que não pode faltar).

Papel por seção: Topo (entender a oferta e clicar; foto, título e botão na primeira tela do celular) · Dor (identificação) · Prova (cartões de números, prints legíveis) · Depoimentos (print legível, legenda curta, filtros) · Quem é (autoridade) · Para quem é · Como funciona (passos, datas, local) · Preço/oferta (riscado, lotes, parcelas, contador) · Perguntas (abre e fecha) · Chamada final (botão repetido, motivo para agir sem exagero).

## Critérios de UI e UX (rodadas da etapa 4)

UI: hierarquia (título, apoio, botão) · espaçamento e ritmo · contraste e leitura (também no sol, no celular) · fotos em cada largura (ex.: título sobre o rosto em celulares largos) · consistência de botões, selos e cartões · quebras de linha ("R$" nunca sozinho).
UX: primeira tela do celular mostra oferta e botão · ordem dor, solução, prova, quem ensina, para quem é, como funciona, preço, dúvidas, ação · botões nos momentos de decisão, barra fixa no celular depois de rolar · formulários curtos · perguntas frequentes com objeções reais · acessibilidade e velocidade no 4G · testes A/B em endereços diferentes (como os topos A, B, C e D do Elite Experience).

## Ajustes depois do design aprovado

| Tipo | Onde se resolve |
|---|---|
| Bug ou funcionamento | Direto no código, testes de novo |
| Texto, número, link ou data sem mudar o visual | Direto no código |
| Visual ou experiência (layout, foto, espaçamento, ordem, bloco novo) | Volta ao design, aprovação, pacote só com as mudanças, código aplica e testa |
| Detalhe visual mínimo decidido na hora | No código, registrado como diferença intencional em relação ao design |

O design é a referência: mudança visual feita só no código é desfeita na próxima versão.

## Risco por tipo de alteração (regra para a IA da gestão)

| Alteração | Risco | Como fazer |
|---|---|---|
| Link, data, WhatsApp, Zoom, texto curto | Baixo | Pode publicar; conferir a prévia e depois o botão principal no ar |
| Trocar imagem, reescrever trecho maior | Médio | Branch e prévia conferida no celular e no computador antes de publicar |
| Bloco novo ou mudança de layout | Alto | Branch e prévia mostrada ao André e ao Luca antes de publicar |
| Checkout, ofertas, eventos, redirecionamentos | Alto | Combinar com o André antes |

Combinados: trabalhar sempre em branch e conferir a prévia (publicar direto só em troca simples) · avisar o André antes de mexer numa página que ele está editando · depois de publicar, testar o botão principal **sem enviar formulário com dados de teste** (cria lead real) · definir quem responde se algo quebrar em lançamento.

Primeiro teste combinado: corrigir o nome da conta do Cloudflare em `docs/DESFAZER-PUBLICACAO.md` numa branch, abrir pull request, o André confere e publica.

## Pontos de atenção

Publicação automática sem etapa intermediária · cada botão de compra aponta para uma oferta da Hotmart (código errado vende no preço errado; ofertas antigas desativadas pelo time) · viradas de lote, contadores e encerramentos usam o horário do servidor e são testados com relógio simulado; mudança de data por escrito e com fuso · botão ou página nova cria eventos novos e precisa de gatilho no GTM · números, depoimentos e imagens geradas por IA só vão ao ar aprovados pelo cliente · formulários: testes nunca enviam lead real · páginas antigas continuam no ar até alguém pedir para tirar ou redirecionar.

## Briefing completo (checklist antes de começar)

Objetivo e como medir · público e etapa do funil · oferta com preço por lote e código de cada oferta na Hotmart · datas e horários com fuso (abertura, viradas, encerramento, reabertura) · links finais (checkout, formulário, WhatsApp com mensagem pronta, Zoom) · textos aprovados e números com fonte · fotos e vídeos na melhor qualidade, com autorização · eventos e UTMs do tráfego · quem aprova e até quando · o que acontece depois (encerramento, reabertura, obrigado).

## Níveis de entrega (página nova)

| | Expressa | Essencial | Bem trabalhada | Excelente |
|---|---|---|---|---|
| Prazo | 1 dia útil ou uma tarde | 2 dias úteis | 3 a 5 dias úteis | 6 a 10 dias úteis |
| Pesquisa | Nenhuma | Referências gerais | Moodboard por seção | Moodboard + concorrentes + inventário |
| Design | Perto do primeiro pedido | Uma passada seção por seção | Bem detalhado, imagens tratadas | Refinamento total, microinterações |
| Testes | Celular, computador, botão e links | Essenciais + eventos, sem rolagem lateral | Completos em várias larguras, velocidade | Completos + acessibilidade + A/B |

Expressa fica abaixo do mínimo seguro e é entregue com aviso por escrito do que ficou sem ajuste e sem teste. Prazo conta a partir da copy aprovada com briefing completo; aprovação do Luca soma à parte; mudança de copy depois do design aprovado é nova rodada.

Alterações em páginas existentes: link/data/texto curto no mesmo dia (mínimo 2 h) · ajuste visual meio dia a 1 dia útil · nova versão 1 a 3 dias úteis · projeto grande por etapas com cronograma.
