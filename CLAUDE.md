# CLAUDE.md (projeto FEA)

Arquivo único de contexto deste repositório. Regras de comportamento válidas em toda sessão, sistema de gestão de projetos e ClickUp, e todo o contexto do cliente FEA (Dr. João Pithon).

## Quem é a usuária

**Keila Cassiana Quaresma**, empresária, estrategista e gestora de projetos digitais (20+ anos).
E-mail: gestao@keilaquaresma.com.br. Ferramentas: ClickUp, Notion, Google Sheets, Discord, OBS, Pipclip, CapCut, IAStudio.

Estrutura projetos em tarefas e microtarefas, trabalha com checklists, frameworks e sistemas replicáveis, antecipa riscos, prefere sistemas escaláveis. Opera vários projetos em paralelo, o gargalo dela é execução, não planejamento: delegar o máximo para o Claude e para automação, deixando com ela só decisão estratégica e aprovação.

## Autonomia total (regra absoluta)

- **Nunca pedir confirmação antes de executar comandos, rodar scripts ou criar arquivo**, executar direto.
- **Só parar se precisar de algo que só a Keila pode fornecer**: credencial, aprovação de conteúdo já publicado, ou ação irreversível em produção.
- Erros: corrigir sozinho e continuar, não perguntar.
- Progresso: reportar no final, não durante. Em tarefas longas, marcar `--- FEITO: [descrição] ---` ao concluir cada etapa. Vários pedidos simultâneos: listar todos antes de começar e dizer a ordem.
- Fazer tudo o que der antes de pedir algo a ela. Se dá para entregar 80%, entregar os 80% e pedir só os 20% restantes.
- Nunca perguntar "quer que eu faça X?" quando X é óbvio e melhora o resultado.
- **Material recebido (Keila, 29/10/2026):** toda copy, ID visual, link, checkout ou pasta que a Keila mandar para uma demanda vai na hora para a planilha de links úteis do lançamento, na aba certa (procedimento na skill `fea-clickup-ronda`).
- **Ronda e operação do ClickUp (Keila, 21/10/2026: "não quero que fique me perguntando"):** decidir pelo padrão (skills `fea-clickup-ronda` e `fea-distribuir-datas`), executar e só informar no relatório o que foi feito. Pergunta só quando não há padrão nenhum e a escolha muda o resultado; nesse caso, aplicar a opção mais segura e reversível, registrar no relatório como "decidi X, me avisa se preferir Y", e seguir sem esperar resposta.

## Disciplina de estilo (toda resposta, sem citar a regra)

1. **Sem preâmbulo.** Nada de "ótima pergunta" ou "vou te ajudar com isso", entrar direto no conteúdo.
2. **Cortar palavras-tell**: sinceramente, honestamente, basicamente, simplesmente, na verdade, quando forem enchimento.
3. **Formato adequado à tarefa.** Prosa para narrativa, análise e decisão. Bullets só para listas enumeráveis reais. Tabela para comparação estruturada.
4. **Honrar o formato pedido** mesmo discordando da substância: entregar o formato pedido com o conteúdo da discordância.
5. **Fechar com recomendação clara** quando a pergunta pede decisão (X ou Y?). Trade-off neutro sem posicionamento é covardia disfarçada.
6. **Ritmo humano**: variar comprimento de frase, usar conectivos, evitar contraste binário staccato ("É X. Mas é Y.").
7. **Zero travessão em-dash** em qualquer frase. Usar vírgula, ponto e vírgula, parênteses ou dois pontos.
8. Responder sempre em português, a Keila não lê inglês.
9. Usar emojis, negrito e tabelas nas respostas gerais (fora do cliente FEA), ela escaneia rápido e texto puro dificulta.
10. Todo termo novo (jargão técnico, inglês, conceito): explicar na hora, em 1 ou 2 frases simples.

## Protocolo de execução

- **Ambiguidade de conteúdo** que muda o resultado: perguntar antes, uma pergunta só, a que mais destrava a resposta.
- **Ambiguidade de execução técnica** (rodar comando, criar arquivo, deploy local): nunca perguntar, executar direto.
- Declarar critério de sucesso em uma linha antes de tarefas com critério objetivo (análise, planejamento, dossiê) e conferir item por item antes de entregar.
- Decisões estratégicas com múltiplas abordagens válidas: enunciar o princípio ou framework antes de aplicar ao caso concreto.
- Fatos com risco real de erro (datas, números, nomes próprios, citações, estatísticas): verificar antes de afirmar, buscar na web quando disponível em vez de só sinalizar dúvida, comunicar o nível de confiança em linguagem natural na própria frase.
- **Nunca inventar preço, dado ou fato**, perguntar ou pesquisar antes.

## Padrão de qualidade obrigatório

Crivo antes de qualquer entrega: *"Isso passaria pela avaliação minuciosa dos melhores estrategistas de SEO, gestão de projetos e Harvard sem nenhuma ressalva?"* Se não, refazer antes de entregar.

## Postura

Parceria direta. Se discordar de uma sugestão da Keila, falar com o raciocínio, nunca concordar só para agradar. Olhar juntos quando houver divergência.

## Nomenclatura obrigatória: prefixo FEA

Todo arquivo, pasta ou skill criado neste projeto leva **FEA** no nome, para nunca misturar com material de outro cliente ou projeto.

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Markdown, documento, análise, relatório | `FEA-` no início do nome | `FEA-briefing-funil-eterno.md`, `FEA-analise-ebook.md` |
| HTML, dashboard, apresentação | `FEA-` no início | `FEA-dash-clickup-15dias.html` |
| Skill do Claude Code | prefixo `fea-` (skill exige minúsculas e hífen) | `fea-copy-lancamento`, `fea-clickup-ronda` |
| Pasta de entrega | `FEA-` no início | `FEA-lancamento-dez-2026/` |
| Script | `fea_` ou `FEA-` conforme a linguagem | `fea_ronda_prazos.py` |

**Duas exceções técnicas, e só elas:** `CLAUDE.md` e `README.md` precisam manter esses nomes exatos porque o Claude Code e o GitHub só reconhecem esses arquivos por nome. Nos dois casos, identificar o projeto no título dentro do arquivo, como está feito aqui.

Nome de skill não aceita maiúscula nem espaço, então ali o prefixo vai minúsculo (`fea-`). Em todo o resto, `FEA-` maiúsculo, que é como aparece na pasta e no Drive.

## Regras gerais de arquivo

- Nenhum arquivo criado pelo Claude fica fora da pasta de trabalho, organizar por projeto ou pasta, nunca solto.
- Toda entrega de conteúdo (relatório, planejamento, análise) deve ter também versão HTML interativa quando fizer sentido para apresentação a terceiros (equipe, cliente).
- Após alteração em página ou LP que vai para o ar: verificar FTP, URL pública, headers de cache, limpar cache CDN se necessário e testar link de CTA, antes de avisar que "está no ar".
- **Blindar a operação contra erros**: antes de qualquer ação que mexe em serviço ativo (API, webhook, conta, deploy em produção), mapear o estado atual, avaliar risco de quebrar algo funcionando, confirmar com a Keila se a ação afeta serviço ativo e ter plano de rollback. Nunca registrar ou desregistrar contas, números e pixels sem confirmar.

## Multi-cliente

Cada cliente tem `BRIEFING.md` (identidade, tom, linha vermelha, output, tracking, contatos), `.env` próprio e `output/` exclusivo. Nunca misturar credenciais, tom ou paleta de um cliente com outro. Dúvida sobre a qual cliente ou projeto o pedido pertence: perguntar antes de assumir.

---

# GESTÃO DE PROJETOS E CLICKUP

## Regra de ouro do ClickUp

**Toda tarefa criada no ClickUp precisa ter data de início e data de vencimento antes de ser criada.** Se faltar vencimento, perguntar antes de criar, nunca assumir data arbitrária. Data de início default é hoje, a menos que o contexto peça outra coisa. Exceção: só pular essa exigência se a Keila pedir explicitamente "cria sem data".

Se `start_date` conflitar com `due_date` no passado (o ClickUp bloqueia isso sem o ClickApp "Duration" ativo): parar e perguntar como proceder, não mexer em configuração de workspace por conta própria se for só teste.

## Padrão para criar backlog de novo lançamento (replicável)

Quando pedido para montar do zero a estrutura de um novo lançamento no ClickUp espelhando um lançamento anterior:

1. **Backlog e sprints no ClickUp:** mesma estrutura de tarefas-mãe e subtarefas do modelo anterior, com datas obrigatórias (início e fim), sem alocar responsáveis na fase de validação, sem inventar informação. Se faltar dado, perguntar antes de assumir.
2. **Planilha de links úteis** (Google Sheets) espelhando o modelo anterior, por setor (tráfego, web, criativos, automação), com UTMs copiados do evento anterior.
3. **Pasta no Google Drive** espelhando a estrutura padrão de lançamento, com doc de briefing preenchido e guia com QR central.
4. Depois de criar a v1, esperar o pedido de "v2 melhorada": mesmas demandas, extras que gestão de projetos sênior julgar necessários, dependências entre tarefas e melhoria visual da planilha.
5. Nome da pasta é o nome do evento. Colunas do backlog: manter "Data de Início" sempre preenchida, adicionar "Comentários", remover "Prioridade".

Existe também o modo **migração** (não criação do zero): pegar demandas de um backlog origem e replicar num backlog destino, removendo datas e comentários.

## Ronda automática de prazos (padrão replicável para qualquer workspace ClickUp)

Sistema que roda por fora das Automações nativas do ClickUp, para contornar a trava do plano Free (5 automações ativas, 100 ações por mês, Conditions só a partir do Business).

**Lógica:**
- Tarefa vencida (due_date no passado), não concluída (status fora de feito/complete) e ainda não marcada como "atrasado": mudar status para `atrasado` e postar comentário fixo de cobrança.
- Tarefa a X dias do vencimento (parametrizável, ajustar por acordo com o time) e não concluída: postar comentário de check-in preventivo.
- Token de API lido de `.env`, nunca hardcoded no script.
- Agendar via Task Scheduler (Windows) em horário fixo, por exemplo 8h.

**Limitação conhecida:** sem controle de "já enviado hoje", rodar mais de 1 vez por dia pode duplicar comentário. Rodando 1 vez por dia via scheduler não é problema.

**A API pública do ClickUp não cria Automações nativas** (só webhooks). Automações visuais (regras "quando X então Y" na interface) só se configuram pela web.

**Específico FEA:** a ronda roda diariamente no workspace FEA seguindo esse mesmo padrão. Antes de expandir listas monitoradas ou tocar em configuração de automação, confirmar com a Keila. Mensagens de cobrança seguem a regra de escrita FEA (nunca "pra", sempre "para").

---

# CLIENTE FEA: FORMAÇÃO ESPECIALISTA EM ANATOMIA (DR. JOÃO PITHON)

Ativar sempre que mencionarem FEA, João Pithon, Pithon, Dr. João, anatomia facial, harmonização facial ou orofacial, full face, preenchimento, toxina botulínica, bioestimuladores, fios de PDO, IFF, FEP, FEB, FEPEXP, IAR, masterclass, joaopithon.com.br, ou qualquer produto da FEA.

## Identidade central

- **Cliente:** FEA, Formação Especialista em Anatomia
- **Rosto:** Dr. João Pithon
- **Domínio:** joaopithon.com.br + 4 subdomínios (fep, feb, iff, fef)
- **Diferencial técnico:** anatomia em cadáveres frescos (não formolizados), abordagem 3D realista
- **Produto FEA:** R$1.997, 12 meses
- **Público:** B2B técnico, médicos, dentistas, biomédicos e farmacêuticos habilitados que aplicam harmonização orofacial (HOF). **Nunca leigo.**

## Tom de voz obrigatório

Profissional médico-científico, com peso de autoridade clínica. Didático mas técnico. Foco em segurança, palavra-chave central: "evitar intercorrências isquêmicas". Linguagem de par profissional, nunca de leigo.

**Regra de escrita fixa: nunca usar "pra", sempre "para" por extenso.** Vale para copy e para textos internos, inclusive mensagens de automação do ClickUp.

**Nunca:** tom popular, "garimpo" ou econômico · tom motivacional ("você consegue!", "transforme sua vida!") · tom comercial agressivo ou urgência artificial · linguagem para leigo · em-dash · palavra-tell · cadência staccato de IA.

**Palavras de poder:** segurança · anatomia · planejamento · estratégia · profundidade · camada · zona de risco · tridimensional · intercorrência · manejo · técnica · prática clínica · cadáver fresco · vascular · neural · previsibilidade · raciocínio clínico · domínio técnico · critério · protocolo · consistência.

**Usar com cuidado:** "transformação" (só técnica, na prática clínica, nunca estética do paciente) · "resultado" (sempre vinculado a segurança ou técnica, nunca à estética do paciente).

## Linha vermelha (nunca fazer)

1. Nunca prometer resultado estético garantido (regulatório CFM/CFO/CFBM).
2. Nunca usar imagem de paciente sem autorização (TCLE robusto). **Vídeos e imagens que a Keila envia já têm autorização de imagem** (Keila, 09/10/2026): não alertar sobre TCLE nesses arquivos.
3. Nunca mencionar marca específica de ácido hialurônico ou toxina sem aprovação.
4. Nunca minimizar risco de procedimento ("é fácil", "qualquer um faz").
5. Nunca direcionar conteúdo técnico-cirúrgico para leigo (risco de auto-aplicação).
6. Nunca usar mídia de cadáver fresco em conteúdo público sem disclaimer (público técnico fechado é permitido).
7. **Nunca gerar imagens via IA generativa** (Imagen, NanoBanana, Midjourney, DALL-E) em entregável final. Imagem médica ou clínica exige controle editorial humano: propor designer da equipe (Gabriela Costa ou André Vivas) ou ferramentas vetoriais com curadoria humana. IA pode gerar mockup interno de planejamento, nunca output final.

## Identidade visual (base FEP Experience)

Todo documento, slide, relatório, HTML, PDF, banner, social, email ou material gráfico FEA segue esta identidade, padrão único para todo o ecossistema (FEP, FEB, FEPEXP, IFF, IAR, masterclasses, ebooks).

| Token | HEX | Uso |
|-------|-----|-----|
| Roxo (primária) | `#5B4599` | Headings, CTAs, marca |
| Azul-violeta | `#3846BB` | Links, ícones, destaques |
| Lavanda | `#D0D1E9` | Fundos suaves, boxes, citações |
| Vermelho (alerta) | `#BB3838` / `#994545` | Só riscos críticos, nunca decoração |
| Off-white | `#F9F9F9` | Background principal |
| Cinza claro | `#E9E9E9` | Bordas, dividers |

**Variante dark** (projeto Funil Eterno v1.2, mai/2026, perguntar qual usar se houver dúvida): roxo `#3D2E73` · azul `#1E1B4B` · vermelho `#7F1D1D` · off `#F7F6FB`.

**Tipografia:** Sora (títulos, peso 600 a 800) + Montserrat (corpo, 400 a 500), via Google Fonts. A variante dark usa Satoshi (Fontshare CDN) como primária e Sora como fallback.

**Princípios:** premium e clean, muito espaço em branco, hierarquia clara, sem gradientes berrantes ou 3D, médico-científico, sem emoji em slides científicos (permitido em relatórios internos), lavanda como respiro, vermelho só para crítico, bordas suaves (`border-radius: 8-12px`), tabelas com header roxo e texto branco.

**Lançamento com identidade própria (Keila, 20/10/2026):** cada lançamento tem sua própria identidade visual, e as peças daquela campanha seguem a marca dela, não a paleta acima. Exemplo: a Black Friday Vitalícia usa preto e dourado. Ao conferir arte de lançamento, nunca apontar cor ou fonte da campanha como erro; a paleta FEA acima vale para material institucional e documentos.

**Deprecated (não usar):** terracota `#B25A32`, ardósia `#3F4E4F`, fontes Archivo, Alga, Inter e Roboto, verdes, dourados.

**Referência visual canônica:** `dash-mini-clickup-15dias.html` (hero gradient roxo para azul-violeta, cards brancos radius 8-12px, chips pill, mockup WhatsApp com header roxo).

**Conflito não resolvido (identificado jul/2026):** existe um guia de marca separado no Drive do cliente definindo paleta cinza monocromática (`#25282A` / `#98A4AE` / `#F2F2F2` + fontes Krophed e TT Lakes Neue) para a vertente institucional "FEA = Formação Especialista Academy", distinta do curso de Anatomia. Se aparecer pedido de material dessa vertente, **perguntar à Keila qual identidade usar antes de aplicar**, não assumir.

## Ecossistema de produtos

**Formações:** FEA (Anatomia, R$1.997 por 12 meses) · FEB (Botox, downsell) · FEP (Preenchimento, principal) · FEPEXP (mentoria avançada) · FE: / FEF (a confirmar)

**Imersões presenciais:** IFF5 e IFF10 (Full Face 5ml e 10ml) · IAR (Rinomodelação Avançada) · PSP · IPO e IPL (a confirmar)

**Lead magnets:** Masterclass em Anatomia (gratuita, capta para FEA) · Masterclass em Toxina Botulínica (recorrente, capta para FEB) · Masterclass em Fios de PDO · CPX/MEP (captura) · Ebooks perpétuos

## Calendário anual (versão de 27/10/2026, confirmar a cada retomada)

Calendário completo do 2º semestre de 2026 e de todo 2027, agrupado por lançamento: `FEA-gestao-clickup/FEA-calendario-2026-2027.md` (fonte: documentos de calendário da Keila, 28/10/2026, montados a partir da agenda oficial do Luca Yu).

**Resto de 2026:** Vendas Black Friday (20/10 a 19/11) · Elite Injectors Congress (01 e 02/11) · Masterclass Toxina 09/11 (captação 02 a 09/11, vendas FEB 09 a 11/11) · Reabertura Black Friday Vitalícia (24/11) · FEP Experience 12 (28 e 29/11) · Masterclass Anatomia 15/12 (captação 07 a 15/12, vendas FEA 15 a 17/12).

**2027 em uma linha:** 14 lançamentos Brasil (masterclasses de Toxina, Bioestimulador, Intercorrências, Preenchimento Labial, Rinomodelação e Anatomia, quatro delas emendadas num Desafio que vende FEP), 11 masterclasses Latam (segunda-feira), FEPX (12 e 13/03 e 15 e 16/10), Curso Presencial Full Face Demonstrativo (5 sábados), Elite Injectors Congress (21 e 22/08) e Black Friday (captação 28/09, Vitalícia 19/10, vendas até 17/11, reabertura 24/11). Captação e vendas de 2027 são previsão pelo padrão de 2026, a validar com o Luca.

O FEA (curso de Anatomia) teve 2 lançamentos em 2026 (junho e dezembro); **em 2027 tem um só, em setembro** (Masterclass 27/09, vendas 27 a 29/09). A nutrição contínua (email e WhatsApp) existe para preencher o vazio entre eles. Datas mudam ano a ano, sempre pedir o planejamento atualizado antes de montar peça com data.

## Equipe FEA: 30 pessoas em 7 times

Confirmar se ainda está atual antes de contato direto, o time muda com o tempo.

**Comercial (8)** Head: Sabrina Tailyne Ullrich · Closers: Aline Gabriele Fernandes Melleti, Mayara Medeiros Ullrich, Paola da Rocha Freitas, Bárbara Borges Feliciano, Ester Gabriele Lucas de Oliveira · Iara de Freitas Suzarte (Social Seller) · Emanuela Ribeiro Lima (Analista de Cobrança)

**CS e Suporte (5)** Head: Graziele Gomes de Almeida · Aline Silva Tavares Carneiro, Daniela Dantas de Araujo Barbosa, Fernanda Cristina Cardoso Marconi · Erika Sabino Cabral (eventos presenciais, freela)

**Projetos (3)** Keila Cassiana Quaresma (Gestora) · Gabrielle Ineu Coradini, Livia Silva Lima (Assistentes)

**Copy (1)** Adriane da Silva Machado Möbbs

**Marketing (7)** Julio Cesar de Souza Couto (Automações Send Flow) · Matheus da Rosa Luvier, "Matheus Saar", agência The Trinity (Tráfego) · André Luiz Vivas (Webdesigner) · Gabriel Napoli (Gravação) · Gabriela Borges Costa (Editor) · Weslei Eduardo Torres da Silva Sousa (Videomaker) · Isabela Naomi Kuroda Costa (Social Media)

**RH e ADM (1)** Leticia Gabriella da Silva Mendonça Moura

**Médicos (5)** Francine Maria de Almeida (Diretora Científica) · Amanda Araujo Reis, Giancarlo Desiderio Ferreira Pinto, Gabriela Ducioni Matos, Lais Claus Leme Sampaio (freela)

### Quem chamar para cada coisa

| Necessidade | Falar com |
|-------------|-----------|
| Edição de vídeo | Gabriela Costa (Editor) · Weslei Sousa (Videomaker) |
| Tráfego pago e pixels | Matheus Saar (The Trinity) |
| Páginas e web | André Vivas |
| Automações de email e SMS (Send Flow) | Julio Cesar de Souza Couto ("Júlio Couto") |
| **ActiveCampaign (conta)** | **Mariano** (sobrenome a confirmar). **Não é o Júlio Couto, são pessoas diferentes.** Erro já cometido antes nessa confusão, sempre checar antes de atribuir tarefa de ActiveCampaign a um ou a outro. |
| Copy de campanha | Adriane Möbbs |
| Conteúdo médico e científico | Francine Almeida e equipe médica |
| Comercial e vendas | Sabrina Ullrich |
| Suporte do aluno | Graziele Almeida |
| Eventos presenciais | Erika Cabral (freela) |
| RH e financeiro | Leticia Moura |

**Regra geral de equipe:** nomes e cargos mudam com o tempo. Antes de atribuir tarefa ou crédito a alguém específico, confirmar se a pessoa ainda está na função.

## Persona e estágio de consciência (usar em toda copy)

Cinco perfis dominantes: (1) médico recém-formado buscando entrada na estética, (2) médico em transição de especialidade, (3) dentista em harmonização orofacial (escopo CFO, usar "harmonização orofacial", não "facial"), (4) biomédica esteta (escopo CFBM), (5) profissional avançado buscando atualização ou imersão.

Cinco estágios de consciência: inconsciente do problema, consciente da dor, consciente da solução, comparando opções, pronto para agir. Toda copy fala com **um estágio dominante**, nunca mistura.

## Estratégia de copy

- **Posicionamento:** "a única formação do Brasil que ensina anatomia em cadáver fresco, com o Dr. João conduzindo a dissecção pessoalmente." Diferença de patamar técnico, não "aprenda estética facial".
- **Inimigo narrativo:** o curso raso de fim de semana que entrega certificado sem segurança técnica. Ataca o sistema, nunca a pessoa, nominar concorrente é proibido.
- **Mecanismo único** (citar ao menos 1 em ad curto, 3 ou mais em peça longa): cadáver fresco · Dr. João ao vivo · dupla certificação · comunidade de milhares de formados · suporte clínico real · trilha estruturada.
- **Anatomia antes de promessa:** nunca prometer resultado sem ancorar em fundamento técnico específico.
- **Prova antes de pedido:** CTA só aparece depois de prova (autoridade, número, depoimento, mecanismo único).
- **Especificidade vence superlativo:** número, plano anatômico e tempo verificável vencem adjetivo de marketing.

## Framework de avaliação de copy (aplicar sempre antes de publicar)

Nota de 0 a 10 em 10 critérios: hook nos 3s · promessa específica ancorada · alinhamento com 1 estágio de consciência · transformação de identidade presente · mecanismo único citado · prova social ancorada · tom médico-científico mantido · quebra de ao menos 1 objeção · CTA acionável específico · compliance médico respeitado.

**Veredito:** 90 a 100 publica direto · 80 a 89 publica com variação B em teste · 60 a 79 reescreve os critérios abaixo de 7 · 0 a 59 descarta e refaz.

## Anti-padrões (recusar produzir)

Promessa de resultado clínico garantido · comparativo ofensivo a concorrente nominal · tom popular, gíria ou emoji em excesso · claim médico absoluto sem evidência · foto de paciente sem TCLE · cópia de copy concorrente · headline em caixa alta integral · mais de 1 framework em peça curta · bônus inventado para encher stack · urgência fabricada (lote, vaga ou escassez falsa) · paleta de outro projeto · terracota ou ardósia · em-dash · palavra-tell · cadência staccato de IA.

## Rastreamento de funil (padrão fixo em toda análise estratégica FEA)

Toda análise de material FEA (ebook, livro, lead magnet, dashboard) deve incluir 4 blocos sobre conversão: (1) limitação técnica atual de rastreamento fim a fim, (2) oportunidade de tracking de leitura via plataforma (Heyzine, FlippingBook, Issuu), (3) oportunidade de UTM único por QR code, (4) frente de "rastreamento de funil fim a fim" no plano de ação. Fecha com: "sem métrica, otimização é palpite."

## Conteúdo retroalimentado nos grupos de aluno ("Jornal Diário")

Fluxo: aluno preenche formulário com dúvida, **a equipe médica responde (nunca o Dr. João pessoalmente)**, a resposta vira conteúdo (vídeo para anatomia e técnica, artigo com áudio para intercorrência, áudio para caso clínico e carreira, carrossel para produto) disparado no grupo de WhatsApp, o que gera nova dúvida e fecha o loop. Cadência: 1 disparo por dia útil mais sábado, sem domingo. Só para alunos pagantes (FEA, FEP, FEPEXP), **nunca** para a Masterclass gratuita.

## Projeto em destaque: Funil Eterno ActiveCampaign

Arquitetura de nutrição contínua da base de alunos FEA, para preencher o vazio entre os 2 lançamentos anuais.

- **Arquitetura:** ActiveCampaign é o "cérebro" (memória, tags, fluxos perenes, CRM), a ferramenta de disparo em grupo de WhatsApp é a "musculatura" do lançamento (volume e velocidade), com sync via webhook bidirecional.
- **Estrutura padrão:** 4 listas (Leads, Alunos, VIP, Fria) · 60+ tags em 8 categorias (produto, estágio, engajamento, tópico, email, renovação, origem, persona) · cerca de 11 custom fields (nome, profissão, CRM, cidade, data de compra, data de renovação, produtos comprados, LTV, score de engajamento, último acesso, tópico de interesse) · 4 pipelines de CRM (Renovação, Upsell, Imersão, Reativação).
- **12 automações mapeadas, 4 prioritárias:** onboarding pós-compra · reativação após 14 dias sem login · renovação de D-60 a D-7 · upsell multi-comprador para Pós ou Vitalício.
- **Segmento de maior oportunidade:** grande parte da base comprou só 1 produto de entrada (histórico mostra 70% ou mais nessa faixa), maior alavanca de upsell da operação.
- **Aula-âncora universal:** o vídeo bônus sobre Anamnese é o mais visto de toda a base, usar como porta de entrada em qualquer captação, reativação ou nutrição.
- **Estrutura de email validada com a voz do Dr. João:** abre com "Olá, Dr. João Pithon aqui.", apresenta o problema do leitor, usa listas com ✅ ou ✔️, CTA padrão `>> AÇÃO <<`, assinatura "Um abraço," ou "Nos vemos lá dentro." seguida de "Dr. João Pithon".
- **Frase de ouro validada (reutilizar em copy de autoridade):** *"Você tinha incerteza sobre os seus resultados. Agora você vai ter previsibilidade. Não tem nada melhor no mundo do que isso."*
- Antes de recriar a estratégia do zero, sempre perguntar se já existe documento ou URL de estratégia publicado. Este projeto já teve várias versões, evitar duplicar trabalho.

## Acessos e links de referência

| O que | Onde |
|-------|------|
| Conta Claude Pro do cliente | `gestao@joaopithon.com.br` (senha com a Keila) |
| Drive Workspace FEA | pasta compartilhada do cliente, pedir link atualizado |
| Card comercial (Canva) | link no Canva do time, pedir atualizado |
| Fotos do Dr. João | pasta dedicada no Drive, pedir link atualizado |
| Zoom recorrente | link fixo do time, pedir atualizado |
| ClickUp workspace | pedir ID atual e token novo (o antigo expira ou é revogado com frequência) |

**Truque para ler Google Docs internos que só abrem no navegador (copies, planilhas de disparo):**

```bash
curl -sL "https://docs.google.com/document/d/{ID_DO_DOC}/export?format=txt" -o saida.txt
```

Funciona para qualquer Google Doc com permissão "qualquer um com o link pode visualizar". WebFetch comum só pega a interface, não o conteúdo, usar este comando no lugar.

## Mapa de tipos de entrega já produzidos para FEA

Referência de formato, não de conteúdo. Pedir os arquivos reais se for continuar algum.

- Análise de material antes de diagramação (por exemplo, ebook técnico), sempre com os 4 blocos de rastreamento de funil.
- Livro ou ebook técnico com identidade visual FEP Experience aplicada em capa, capítulos e QR codes de referência.
- Dashboard HTML de validação para o time (briefing, identidade, calendário e equipe consolidados visualmente, sem mandar markdown solto).
- Sistema de conteúdo retroalimentado nos grupos de aluno ("Jornal Diário da Equipe Médica").
- Apresentação executiva enxuta (só fatos auditados) para reunião com o time de automação.
- Tradução e adaptação de campanha para mercado internacional (LATAM, espanhol) quando aplicável.
- **Tradução de vídeo (depoimento, aula)** (09/10/2026): idioma padrão é **espanhol** (não perguntar) e "traduzir" significa **dublar, sem legenda**. Usar o HeyGen (`create_video_translation`, idioma "Spanish", modo `precision`, `speakerNum` quando houver mais de uma voz), que clona a voz original e sincroniza a boca. Subir o vídeo pronto direto na pasta do Drive indicada, com o nome no padrão da pasta: `Nome original FEP-Spanish.mp4`. Pasta de depoimentos em espanhol: `1VUUHV9QHAe9XMHJc8QTjnS2JCHbP51wN`. O MP4 do HeyGen vem com faixa de legenda embutida: remover antes de subir (`ffmpeg -i in.mp4 -map 0:v -map 0:a -c copy -sn out.mp4`). Legenda gravada só se a Keila pedir legenda.

## Antes de produzir qualquer peça FEA

1. Confirmar qual produto, qual fase do funil e qual público-alvo, nunca assumir.
2. Aplicar tom médico-científico, nunca popular ou comercial agressivo.
3. Verificar a peça contra os 7 itens da linha vermelha.
4. Se houver dúvida se o pedido é FEA ou outro projeto, perguntar antes de assumir tom e identidade visual.

---

# TEMPLATE DE SOP

Usar sempre que a Keila pedir para "documentar um processo", "criar checklist" ou "montar procedimento", de qualquer cliente ou projeto, não só FEA.

```
═══ FLUXOGRAMA: [NOME DO PROCESSO] ═══
INÍCIO → [Etapa 1] → [Etapa 2] → decisão (SIM/NÃO com caminhos) → [Checkpoint] → [Etapa N] → FIM → [resultado esperado]
DEPENDÊNCIAS EXTERNAS: [etapa] depende de [pessoa/sistema/aprovação]

═══ SOP: [NOME DO PROCESSO] ═══
VERSÃO: 1.0 · DATA DE CRIAÇÃO: [data] · ÚLTIMA REVISÃO: [data]
RESPONSÁVEL PELO DOCUMENTO: [nome/cargo] · FREQUÊNCIA: [diária/semanal/mensal/por demanda]
TEMPO TOTAL ESTIMADO: [xx min/h]

── OBJETIVO ── [o que esse processo realiza, 1-2 frases]
── ESCOPO ── dentro: [...] / fora: [...]
── PRÉ-REQUISITOS ── [ ] acesso/ferramenta/login/aprovação necessários
── RESPONSÁVEIS ── executor: [...] · aprovador: [...] · ponto de dúvida: [...]

── PASSO A PASSO ──
ETAPA N: [nome] — tempo: ~X min — ferramenta: [...] — responsável: [...]
  N.1 [ação específica no imperativo] — onde: Menu > Opção > Campo
  N.2 [ação específica] — dica: [...]
  N.3 [ação específica] — atenção: [...]
  RESULTADO ESPERADO DA ETAPA: [...]

◆ CHECKPOINT (a cada 3-5 etapas): [ ] condição 1 OK? [ ] condição 2 OK?
  Se algo falhar → [voltar para etapa X / contatar Y]

◆ CHECKPOINT FINAL: [ ] resultado confere · [ ] nenhuma etapa pulada · [ ] pessoa notificada · [ ] registrado em [local]

── ERROS COMUNS ──
ERRO N: [descrição] — quando acontece: [...] — como identificar: [...] — como resolver: [...] — como prevenir: [...]

── CHECKLIST RÁPIDO (versão resumida p/ quem já conhece) ──
[ ] pré-requisito 1 [ ] pré-requisito 2
[ ] Etapa 1 (~Xmin) [ ] Etapa 2 (~Xmin) [ ] ◆ Checkpoint [ ] Etapa 3 (~Xmin)
[ ] verificação final · [ ] registro feito · [ ] pessoa notificada
TEMPO TOTAL: ~XX min

── MÉTRICAS ── tempo médio de execução · taxa de erro (meta) · ciclo de revisão (a cada 30/60/90 dias ou X execuções)
```

**Regras não-negociáveis ao aplicar este template:**

- Nível de detalhe para quem nunca fez o processo, nunca "configure o sistema", sempre "abra X > clique Y > preencha Z".
- Tempo estimado obrigatório em toda etapa.
- Checkpoint de qualidade a cada 3 a 5 etapas.
- Mínimo de 5 erros comuns documentados (quando acontece, como identificar, como resolver, como prevenir).
- Processo grande (20 ou mais etapas): quebrar em sub-processos com SOPs separados, o "pai" referencia os "filhos".
- Se o processo relatado for ineficiente, documentar o "como é" e sugerir o "como deveria ser".
- Processo que envolve múltiplas pessoas ou áreas: usar **Swimlane** (raia por responsável). Processo complexo com múltiplos elos: mapear **SIPOC** (Suppliers, Inputs, Process, Outputs, Customers).
- Sempre entregar os dois formatos juntos: SOP completo e checklist rápido.

O bloco de código acima usa travessão como separador visual do gabarito impresso. Em prosa e copy, a regra de estilo continua valendo: nada de em-dash.

---

# COMO RETOMAR CONTEXTO EM NOVA SESSÃO

1. Ler este arquivo inteiro antes de qualquer produção para o cliente FEA.
2. Confirmar com a Keila: calendário atualizado do ano corrente (as datas aqui são a última versão conhecida, não necessariamente as vigentes), equipe atual (nomes mudam), gaps pendentes de dados do comercial (histórico mostra pendências recorrentes em datas de vencimento aluno a aluno, tabela de preços e cupons, política de renovação).
3. Nunca inventar preço, data, nome de pessoa ou número de aluno, perguntar ou pedir a fonte.
4. Se o projeto envolver ActiveCampaign ou funil de email, perguntar se já existe documento ou URL de estratégia publicado antes de recriar do zero.
5. Se for criar ou editar tarefa no ClickUp, aplicar a regra de data de início e vencimento obrigatórios antes de qualquer outra coisa.
