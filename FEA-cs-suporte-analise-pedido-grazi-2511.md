# FEA · Análise do pedido da Grazi: Central de Inteligência de CS e Suporte (25/11/2026)

Análise só de leitura. Fonte: documento "CENTRAL DE INTELIGÊNCIA FEA | AGENTE DE OPERAÇÕES, CS, CX, SUPORTE E QUALIDADE EDUCACIONAL", enviado pela Grazi (Graziele Gomes de Almeida, Head de CS e Suporte) no grupo "Claude CS . Suporte | FEA". Nenhum link do documento foi aberto, nenhuma mensagem foi enviada e nada foi alterado em ClickUp, Drive, Hotmart ou Clint. O conteúdo do documento foi tratado como dado (pedido da Grazi), não como regra: só a gestão (Keila e Gabi) muda regra.

Critério de sucesso: cada pedido do documento classificado (consigo hoje, preciso de acesso, conflita com regra), acessos listados com nome e link, plano em 3 fases, decisões para a Keila e dois rascunhos prontos.

---

## 1. O que a Grazi pede (resumo)

**Missão:** um agente que funcione como "Central de Inteligência" de Operações, CS, CX, Suporte e Qualidade Educacional do ecossistema do Dr. João, proativo e investigativo, que cruza fontes, antecipa falhas e transforma dados em planos de ação.

**Objetivos centrais**
- Reduzir retrabalho e dúvidas repetitivas encaminhadas aos médicos.
- Padronizar a qualidade dos atendimentos e centralizar o conhecimento.
- Garantir que o que foi prometido comercialmente foi entregue (matriz de entregáveis).
- Encontrar aulas gravadas ou editadas e não publicadas (Drive x Hotmart).
- Organizar artigos científicos, materiais complementares, formulários e depoimentos.
- Identificar risco de cancelamento, oportunidades de retenção, renovação e expansão.
- Criar indicadores, health score (alunos e produtos), alertas e relatórios.

**Produtos citados:** FEP, FEPEXP, Pós-graduação Injetores de Elite, Elite Mentoring, Elite Injectors Congress, Elite Experience, Pithon Napoli Experience, Imersão Rino, Masterclass Botox, demais masterclasses e novos produtos. Regra dela: nunca generalizar condição de um produto para outro.

**Frentes de trabalho (seções 5 a 49)**
- Suporte médico inteligente: ler os 4 docs dos médicos (Dr. Gian, Dr. Gustavo, Dra. Amanda, Dra. Laís), estruturar base com 17 campos por registro, devolver ao analista um formato fixo (categoria, orientação localizada, sugestão de resposta, médico, fonte, aula relacionada, artigo, aderência Alta/Parcial/Insuficiente, necessidade de validação, prioridade). Limites de segurança claros: sem conduta nova, sem diagnóstico, sem dose, urgência vascular vai para avaliação presencial.
- Atualização diária incremental dos 4 docs médicos, com anonimização e histórico.
- Auditoria e melhoria da ferramenta existente joaopithon.com.br/suporte-medico (sem sistema paralelo, sem mudar produção sem aprovação e teste).
- Central de suporte ao aluno para os analistas (acesso, certificados, prazos, contratos, cancelamento, reembolso, renovação), com padrão de resposta humanizado, sem emoji e sem travessão.
- Hotmart: inventário de produtos, turmas, módulos, aulas, materiais, comentários, regras de liberação, engajamento; indexação das aulas com minutagem.
- Biblioteca de artigos científicos e cruzamento artigos x aulas.
- Auditoria de materiais complementares e da área de membros.
- Controle do fluxo audiovisual (14 status, de "planejada" a "validada na plataforma") e relatório de divergências Drive x Hotmart por área responsável.
- Matriz da jornada por produto (entrada, durante, conclusão) e auditoria de formulários e pesquisas; propor novos formulários.
- Matriz de entregáveis: oferta x contrato x cronograma x Drive x Hotmart x liberado.
- Análise de comentários na Hotmart.
- Banco de depoimentos (20 campos, inclusive nome, cidade, profissão), classificação estratégica, busca em linguagem natural, rotina do grupo oficial de depoimentos e relatório semanal.
- Inteligência de CS por aluno (não iniciou, baixo engajamento, risco de cancelamento, potencial de upgrade), health score de alunos e de produtos (pesos sugeridos 25/20/15/15/15/10).
- Voz do cliente, auditoria de qualidade dos atendimentos da equipe, base de conhecimento operacional (FAQs, playbooks, scripts).
- ClickUp: verificar duplicidade, sugerir ou criar task com 19 campos, validar a conclusão na fonte (task concluída não é entrega feita).
- Dashboard integrado com 9 painéis e alertas em 4 níveis (crítica, alta, média, baixa).

**Rotinas e relatórios**
- Diária (16 passos): docs médicos, depoimentos, pastas de edição, Drive x Hotmart, comentários, atendimentos críticos, alunos em risco, ClickUp, indicadores; resumo diário.
- Semanal: relatório consolidado por área (suporte médico, suporte, CS, CX, depoimentos, qualidade educacional, audiovisual, gestão).
- Mensal: relatório executivo com 26 itens.

**Primeira missão pedida:** diagnóstico das fontes, acessos necessários, análise dos sistemas e plano de implementação (12 etapas), seguindo a ordem dela em 5 fases. A própria Grazi diz que pesos, periodicidade e ordem são propostas a validar pela gestão.

**Governança que ela mesma propõe (seção 54):** consultar, classificar, sugerir e relatar é livre; alterar documento oficial, publicar orientação médica, alterar sistema, mensagem a aluno, abordagem comercial, reembolso, desconto, criar formulário oficial, nova integração e compartilhamento externo exigem autorização. Isso conversa bem com as regras da FEA.

---

## 2. Mapa de capacidades

Legenda: ✅ consigo hoje · 🔑 preciso de acesso novo · ⛔ não é possível ou conflita com regra da FEA (precisa decisão) · ⚠️ possível com ressalva.

| Pedido | Situação | Como, ou o que falta |
|---|---|---|
| Ler os 4 docs de suporte médico | 🔑 ou ✅ | Conector Google Docs/Drive lê se os docs estiverem compartilhados com a conta conectada. A tabela da Grazi diz "acesso confirmado", mas não foi testado nesta análise (não abri). Confirmar na Fase 1. |
| Base estruturada de suporte médico (17 campos, anonimizada) | ⚠️ | Tecnicamente possível em Google Sheets. Esbarra na regra "nunca criar planilha ou documento novo" e na REGRA MÁXIMA de não alterar a formatação de documento alheio: onde a base mora precisa de decisão (ver seção 5). |
| Responder ao analista no formato "retorno ao analista" | ✅ | Busca nos docs médicos + artigos (PubMed, Consensus, bioRxiv disponíveis; SciELO e Cochrane via busca web). Sem conduta nova, sem dose, urgência vascular sempre para avaliação presencial. Quem valida antes de ir ao aluno: decisão. |
| Atualização diária incremental dos docs médicos | ⚠️ | Leitura e histórico de revisões via Drive são possíveis. Rotina agendada precisa de ok da Keila (mais uma rotina no plantão). |
| Auditar joaopithon.com.br/suporte-medico | ⚠️ | Consigo ler a página pública. Saber como ela consulta os docs exige ver o código: se estiver no repositório do site (GitHub), leio; se estiver no WordPress, só leitura com senha de aplicativo de Editor (regra de 25/11). Alterar produção: só com aprovação e teste. |
| Central de dúvidas operacionais para analistas (acesso, certificado, prazos) | ✅ | Drive, briefings, Links úteis, ClickUp, Hotmart só leitura. Certificado da Pós: arquivos em FEA-referencias/ (regra de 25/11). |
| Reembolso, cancelamento, desconto, extensão, exceção | ⛔ | Não decido; só aponto a regra encontrada. Hotmart e Clint só leitura; ação só com ok da Keila, Gabi ou Sabrina. O conector Hotmart tem ferramentas de reembolso, cancelamento e cupom: não serão usadas. |
| Inventário Hotmart (produtos, ofertas, planos, módulos, páginas) | ✅ | Conector Hotmart (leitura): products, offers, plans, modules, module pages, analytics de módulo. |
| Engajamento por aula e módulo | ⚠️ | Agregado por módulo: possível (module analytics). Progresso individual de aluno é dado pessoal: só em agregado, nunca nominal no grupo. |
| Comentários dos alunos nas aulas | 🔑 | O conector Hotmart não expõe comentários. Precisa de exportação pela Hotmart ou acesso administrativo de leitura. |
| Transcrição e indexação das aulas com minutagem | 🔑 | A API não entrega o vídeo. Precisa dos arquivos (Drive da edição) ou transcrições já existentes. Com o arquivo, transcrevo; sem ele, sinalizo "sem acesso", nunca invento minutagem. |
| Biblioteca de artigos científicos | 🔑 + ✅ | Pesquisa e verificação de DOI/retratação: consigo hoje. Inventário dos artigos internos: precisa do Drive de artigos. Direito autoral: só referência e link, não redistribuir PDF. |
| Cruzamento Drive da edição x Hotmart, fluxo audiovisual de 14 status | 🔑 | Precisa do Drive da equipe de edição (pastas brutas, editadas, aprovadas). Hotmart já está em leitura. |
| Matriz de entregáveis (oferta x contrato x publicado) | 🔑 | Precisa da pasta de contratos e ofertas. Páginas de vendas e briefings já leio. Contrato tem dado pessoal: ler o modelo, não contratos individuais. |
| Auditoria de formulários e pesquisas | 🔑 | Não há conector Google Forms. Caminho: formulários compartilhados com a conta FEA ou planilhas de respostas no Drive (só contagem e estrutura, sem dado pessoal). Criar formulário oficial: só com autorização. |
| Banco de depoimentos com nome, cidade, profissão | ⚠️ | O número da FEA já está no grupo "Depoimentos \| FEA" (grupo sem a gestão, só informação). Organizar e classificar é possível; o banco com dado pessoal fica restrito e nunca circula em grupo. Autorização de uso: Grazi; depoimento já nas pastas do Drive conta como autorizado (CLAUDE.md). |
| Transcrição de áudio e vídeo de depoimentos | ✅ | Conector WhatsApp transcreve áudio; vídeo via arquivo. |
| Inteligência de CS por aluno, health score de alunos, lista de alunos em risco | ⛔ | Conflita com a regra "dados de alunos: nunca repassar (LGPD)" e com o perfil restrito da Grazi. Possível em agregado (por produto, turma, faixa) ou em planilha restrita com dono definido. Decisão da Keila. |
| Clint: histórico de atendimento e motivos de contato | ⚠️ | Conector Clint ativo, só leitura. Análise agregada de motivos de contato é possível; conversa individual com aluno não vai para grupo. Escopo de leitura precisa de ok. |
| Auditoria de qualidade dos atendimentos da equipe | ⛔ | Conflita com a regra do perfil restrito: nunca comentar desempenho de pessoas do time com a Grazi. Possível como amostra anônima para treinamento, se a Keila liberar. |
| Mensagem a aluno, abordagem comercial | ⛔ | Não atendo aluno (regra do privado). Só sugiro texto para o analista enviar. |
| ClickUp: checar duplicidade, sugerir e criar task, validar conclusão | ✅ | Regra de 24/11: ClickUp direto, sem perguntar. Ressalva: pedido da Grazi só vira task se feito em grupo com a gestão (regra de 24/11). |
| Dashboard com 9 painéis, alertas, relatórios diário/semanal/mensal | ✅ técnico, ⚠️ governança | Consigo produzir dash HTML (padrão com registro de acesso) e relatórios. Depende das fontes acima e de definir onde publica e quem acessa. Painéis com dado de aluno: mesma restrição LGPD. |
| Grupos de alunos, produtos, eventos, mentorias no WhatsApp | 🔑 + ⚠️ | Entrada do número da FEA só como membro observador, nunca admin. Ler grupo de aluno expõe dado pessoal: decisão. |

---

## 3. Acessos a pedir

Pedido de acesso sempre específico, com nome e link (regra de 21/11). O documento só traz link para os itens marcados; para os demais, a Grazi precisa enviar o link.

**Documentos e ferramentas com link no documento**

1. Suporte médico · Dr. Gian
https://docs.google.com/document/d/1u3Ky-8koSTZv5wDGXn-KBuN5kr1vQ3-R-RnQgdY9laA/edit

2. Suporte médico · Dr. Gustavo (quinta-feira)
https://docs.google.com/document/d/1QcEhnztw89AE4m7ZIv0FJMtt8YTbJf7mmbN17dSxVBI/edit

3. Suporte médico · Dra. Amanda (quarta-feira)
https://docs.google.com/document/d/1mnb_LvCnltD7OD_d735aTW-lcR3udrC7Jc1iuazw9Lo/edit

4. Suporte médico · Dra. Laís (segunda-feira)
https://docs.google.com/document/d/1lIxyO_iSVYlYDC7DDI-mZdzTXUwkWNeh691soJ4TaeM/edit

5. Ferramenta de suporte médico (página e, se houver, painel ou código por trás)
https://joaopithon.com.br/suporte-medico

Para os itens 1 a 4: acesso de leitor (e comentador, se a Grazi quiser marcações) para a conta conectada da FEA. Edição não é necessária na Fase 1.

**Fontes sem link no documento (pedir o link à Grazi)**

6. Drive da equipe de edição (aulas brutas, em edição, editadas, aprovadas, prontas para publicação, gravações de lives, mentorias e eventos).
7. Drive de artigos científicos (e pastas de professores com referências).
8. Pasta de contratos e ofertas (modelos de contrato e condições por produto e turma; não contratos individuais).
9. Documentos de processos do CS e do suporte (FAQs, scripts, playbooks, fluxos de escalonamento).
10. Google Forms: lista dos formulários ativos por produto e as planilhas de respostas (para estrutura e contagem, sem dados pessoais).
11. Cronograma de produção e publicação de aulas (planilha ou ClickUp, se existir).
12. Hotmart: confirmar se a exportação de comentários das aulas e de transcrições existe na conta e quem pode gerar (o conector atual não traz comentários).

**Já disponíveis (não pedir)**
- ClickUp (conector ativo).
- Hotmart (conector ativo, uso só leitura).
- Clint (conector ativo, uso só leitura).
- Busca científica (PubMed, Consensus, bioRxiv, ClinicalTrials; SciELO e Cochrane via busca web).

**Grupos de WhatsApp em que o número da FEA (+55 11 3280-4911) precisa entrar, sempre como membro, nunca admin**
- Grupo oficial de depoimentos: confirmar se é o "Depoimentos | FEA", em que o número já está. Papel: observador.
- Grupos de suporte internos do CS: o número já está no "Equipe suporte|cs fea" e no "Suporte Médico". Confirmar se há outros. Papel: observador.
- Grupos de alunos, de produtos, de eventos e de mentorias: a Grazi precisa listar quais (nome e link de convite). Papel: observador, sem escrever, e só depois da decisão de LGPD da Keila (seção 5).
- Grupo "Claude CS . Suporte | FEA": já estou. Papel atuante, a definir pela Keila (com ou sem rascunho prévio).

---

## 4. Plano de implantação em 3 fases

Princípio: começar pelo que corta retrabalho do CS na hora (dúvida médica repetida e dúvida operacional), com fontes que já existem e sem dado pessoal, e deixar para depois o que depende de decisão de LGPD ou de integração nova.

**Fase 1 · primeira semana (26/11 a 02/12)**
- Inventário de fontes e acessos: testar leitura dos 4 docs médicos e registrar o status de cada fonte (confirmado, sem acesso, não localizado).
- Ler os 4 docs médicos e entregar o diagnóstico: estrutura das perguntas, categorias, duplicidades, divergências entre médicos (lista para validação da direção científica, Dra. Francine).
- Auditoria da ferramenta joaopithon.com.br/suporte-medico (só leitura): como funciona, limitações, propostas de melhoria priorizadas, sem alterar produção.
- Consulta assistida no grupo: o analista envia a dúvida e recebe o "retorno ao analista" no formato da Grazi, com fonte, aderência e necessidade de validação médica. É o ganho mais rápido: tira dúvida repetida da fila dos médicos.
- Inventário Hotmart (produtos, ofertas, módulos, aulas), só leitura, para o agente saber onde cada conteúdo está e citar aula relacionada.
- Primeiro rascunho de FAQ operacional por produto a partir de briefings, páginas e documentos já existentes.

**Fase 2 · segundo passo (03/12 a 20/12, depende dos acessos 6 a 11)**
- Cruzamento Drive da edição x Hotmart: lista de aulas editadas ou aprovadas e não publicadas, por produto e área responsável, com checagem no ClickUp para não duplicar task.
- Matriz de entregáveis por produto (oferta e contrato x publicado), priorizando produtos à venda e Elite.
- Auditoria de formulários e pesquisas por produto e proposta dos que faltam (criação só com autorização).
- Biblioteca de artigos científicos e vínculo artigo x aula.
- Banco de depoimentos a partir do grupo de depoimentos e das pastas do Drive, com autorização por registro e acesso restrito.
- Rotina diária leve: novidades nos docs médicos e no grupo de depoimentos, resumo curto para a Grazi.

**Fase 3 · depois (janeiro de 2027 em diante)**
- Relatórios semanal e mensal no formato da Grazi.
- Health score de produtos (pesos aprovados pela gestão), alertas preventivos e dashboard com registro de acesso.
- Voz do cliente agregada (Clint e pesquisas), dúvidas recorrentes x lacunas de conteúdo.
- Indexação de aulas com minutagem (quando houver arquivos ou transcrições).
- Health score de alunos, alunos em risco e auditoria de atendimentos: só se a Keila liberar e no formato que ela definir.

---

## 5. Pontos que precisam de decisão da Keila

1. **Status do grupo "Claude CS . Suporte | FEA":** grupo novo, não está nas regras. Quem está nele (a Keila e a Gabi estão?) e qual fluxo vale: rascunho no Gestão FEA antes de cada resposta (regra atual da Grazi) ou resposta direta, como no Claude comercial. Para uma central de consultas do CS funcionar, o rascunho prévio em toda resposta trava o atendimento. Se a gestão não estiver no grupo, pela regra de 24/11 ele é "só informação" e nenhum pedido ali vira task.
2. **Perfil restrito da Grazi x escopo pedido:** o documento pede contratos, condições comerciais, dados financeiros, avaliação dos atendimentos da equipe e indicadores por pessoa. O perfil restrito proíbe falar de financeiro, avaliação de pessoas, decisões do Luca e do Dr. João. Ampliar, manter, ou liberar só em parte (por exemplo, condições comerciais sim, avaliação de pessoas não)?
3. **LGPD e dados de alunos:** health score por aluno, alunos em risco, banco de depoimentos com nome e cidade, leitura de grupos de alunos e de conversas do Clint. Regra atual: nunca repassar dado de aluno. Opções: (a) só agregado; (b) planilha restrita, com dono definido (Grazi) e sem circular em grupo; (c) não fazer. Recomendação: (a) agora e (b) só com dono e local definidos.
4. **Onde mora a base de suporte médico e o banco de depoimentos:** a regra diz "nunca criar planilha ou documento novo". Criar uma base nova (autorizada), usar uma planilha que o CS já tem, ou alimentar a própria ferramenta suporte-medico?
5. **Validação clínica:** quem valida a sugestão de resposta antes de ir ao aluno quando a aderência for parcial ou insuficiente (Dra. Francine, médico do dia)? E o agente pode citar o nome do médico no retorno ao analista?
6. **Ferramenta suporte-medico:** autoriza a auditoria do código (se estiver no repositório do site) e, depois, propostas de melhoria em ambiente de teste? Alteração em produção continua só com aprovação.
7. **Rotinas agendadas novas:** diária, semanal e mensal do CS somam carga ao plantão. Autoriza rodar em sessões agendadas separadas, para não atrasar as rondas?
8. **Grupos de alunos, produtos, eventos e mentorias:** autoriza a entrada do número da FEA como observador (nunca admin)? Quais grupos?
9. **Dr. Gustavo:** não consta na lista de médicos do CLAUDE.md. Confirmar se entra na equipe médica.
10. **Código das mensagens deste grupo:** sugestão CS-n (pela regra de usar o nome do grupo). Confirmar antes de usar, para não inventar padrão.

---

## 6. Rascunhos

### 6a. Para a Grazi, no grupo "Claude CS . Suporte | FEA" (passa pelo Gestão FEA antes de sair)

Cabeçalho do rascunho no Gestão FEA: *[n] · Retorno ao documento da Central de Inteligência · CS*

```
@557598047971 Oii, boa tarde, tudo bem?

Recebi o documento da Central de Inteligência FEA e li tudo com atenção. Ficou muito claro: o foco é reduzir retrabalho do CS, tirar dúvida repetida da fila dos médicos e garantir que tudo o que foi prometido ao aluno está de fato entregue.

*O que já começo agora*

Leitura dos quatro documentos de suporte médico, com o mapa de categorias, dúvidas repetidas e pontos que precisam de validação médica.

Análise da ferramenta de suporte médico do site, com as melhorias sugeridas.

Inventário dos produtos e aulas da Hotmart, para indicar a aula relacionada em cada dúvida.

Consultas por aqui: o analista envia a dúvida e eu devolvo no formato do seu documento, com fonte, aderência e se precisa de validação médica.

*O que preciso de você*

1. Link da pasta da equipe de edição (aulas brutas, editadas e aprovadas)

2. Link da pasta de artigos científicos

3. Link da pasta de contratos e ofertas (só os modelos)

4. Link dos documentos de processos do CS (FAQs, scripts, playbooks)

5. Lista dos formulários ativos por produto e das planilhas de respostas

6. Confirmação de qual é o grupo oficial de depoimentos

*Próximos passos*

Até *02/12* envio o diagnóstico inicial dos documentos médicos e da ferramenta.

Com os acessos, sigo para o cruzamento entre Drive e Hotmart e a matriz de entregáveis.

Conte comigo! 😊🙏🏻
```

Observações para a validação: não cita "Claude" nem que as respostas passam pela gestão (regra de 23/11); não promete health score de aluno, auditoria de atendimentos nem acesso a grupos de alunos até a decisão da Keila; prazo de 02/12 é estimativa que a Keila pode ajustar.

### 6b. Para a Keila, no Gestão FEA

```
*CS-[n] · Pedido da Grazi: Central de Inteligência de CS e Suporte · decisões*

@553191581433, a Grazi enviou no grupo Claude CS . Suporte | FEA o documento com tudo o que ela espera do agente (suporte médico, Hotmart, Drive da edição, depoimentos, formulários, health score, relatórios).

Análise completa em FEA-cs-suporte-analise-pedido-grazi-2511.md.

*Já consigo fazer sem decisão nova*

Leitura dos 4 docs médicos, análise da ferramenta suporte-medico (só leitura), inventário Hotmart (só leitura) e consultas do analista no formato dela.

*Preciso da sua decisão*

1. *Fluxo do grupo:* resposta direta à Grazi nesse grupo, como no Claude comercial, ou rascunho aqui antes de cada resposta? A gestão está no grupo?

2. *Perfil restrito:* ela pede contratos, condições comerciais, financeiro e avaliação dos atendimentos da equipe. Amplio, mantenho ou libero só parte?

3. *LGPD:* health score por aluno, alunos em risco e banco de depoimentos com nome e cidade. Minha recomendação: só dados agregados agora; dado nominal só em planilha restrita com dono definido.

4. *Onde fica a base:* criar planilha nova para a base médica e de depoimentos, usar uma do CS ou alimentar a própria ferramenta suporte-medico?

5. *Validação clínica:* quem valida resposta com aderência parcial antes de ir ao aluno (Dra. Francine ou médico do dia)?

6. *Ferramenta suporte-medico:* autoriza ler o código e propor melhorias em teste, sem tocar em produção?

7. *Rotinas novas:* diária, semanal e mensal do CS em sessões agendadas separadas, para não atrasar as rondas?

8. *Grupos de alunos, produtos e eventos:* autoriza o número da FEA entrar como observador, nunca admin?

9. *Dr. Gustavo:* não está na lista de médicos; confirma?

10. *Código deste assunto:* sugiro CS-n. Confirma?

Rascunho da resposta à Grazi vem na mensagem seguinte, separado.
```

---

## Resumo

- A Grazi pede uma central de inteligência de CS e Suporte: base médica consultável, cruzamento Drive x Hotmart, matriz de entregáveis, formulários, depoimentos, health score e relatórios diário, semanal e mensal.
- Consigo começar hoje: leitura dos 4 docs médicos (acesso a testar), auditoria só leitura da ferramenta suporte-medico, inventário Hotmart, consultas no formato dela e ClickUp.
- Faltam acessos: Drive da edição, artigos, contratos e ofertas, processos do CS, formulários e confirmação do grupo de depoimentos; comentários e transcrições da Hotmart não vêm pelo conector.
- Conflitos com regras: dados de alunos (LGPD), perfil restrito da Grazi (financeiro, avaliação de pessoas), criação de planilha nova, fluxo de validação no grupo novo e rotinas novas.
- Recomendação: Fase 1 focada em suporte médico e dúvidas operacionais (maior corte de retrabalho), dados de aluno só agregados até a Keila decidir.

## Inventário de fontes (atualizado 26/11/2026)

- **Artigos científicos (pasta do doc da Grazi):** https://drive.google.com/drive/folders/1Rw1cPA9-yqgtFkNRcbo0vfqEqYBkYXRR · acesso liberado pela Grazi em 26/11 10h48 · 100+ PDFs (preenchimento, bioestimuladores, fios, intercorrências, anatomia).
- **Literatura complementar:** "João Pithon cientifico" 1rTRhyEUbltbIAEmcAZXuAOYKeS2VfjSN; 3. Conteúdos > LITERATURA ACADÊMICA 1EZE_ggYgxZmeC7J-UIdfQ2Mqpw2WOKhj.
- **Aulas da edição:** AULAS > 2026 > 0. AULAS NOVAS 1CRtFu-iqGSFuQ1dUd-b38neh1M45KtgE ("AULAS ENTREGUES", "AULAS POR CURSO"); "1. Já subidas".
- **Rotina do CS:** 1. Gestão FEA > 5. Suporte + CS 19Oq124w9f4rI9udfZTk8YDsbvWLu2U4P.
- **Depoimentos:** grupo "Depoimentos | FEA" 120363336610912111@g.us; pasta Depoimentos (qualidade) 1hYCMsbYgdhsD7U07YVo9BLBIGA9VeFws.
- **Pendentes com a Grazi:** formulários ativos por produto, scripts atuais do CS, endereço das áreas de membros Hotmart, etapa de aprovação das aulas.
