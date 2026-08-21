# Backlog Black Friday — unificação e deduplicação

Estado da migração das demandas da pasta **Black Friday Vitalícia 10/26**
(Space `Marketing`, workspace `9013080622`) para as listas de Backlog.

> **Interrompido por rate limit da API do ClickUp** (resposta: *"Rate limit
> exceeded. Please wait 331 minutes"*). Este documento existe para permitir
> retomar exatamente de onde parou.

## Origem

| Lista | ID | Pais | Folhas |
|---|---|---|---|
| Sprint 1 (17/8 - 23/8) | `901328170220` | 9 | 40 |
| Sprint 2 (24/8 - 30/8) | `901328179817` | 4 | 10 |
| Sprint 3 (31/8 - 6/9) | `901328225835` | 1 | 2 |
| **Total** | | **14** | **52** |

66 tarefas na origem. As tarefas-pai são disciplinas que se repetem entre
sprints (Design ×2, Copy ×2, Webdesigner ×2, Gestão ×3).

## Resultado da deduplicação: 66 → 56

**5 pais colapsados** (Design ×2→1, Copy ×2→1, Webdesigner ×2→1, Gestão ×3→1).

**5 folhas eliminadas:**

| # | Tarefa mantida | Duplicata removida | Tipo |
|---|---|---|---|
| 1 | Atualizar página de obrigado + pesquisa | `86ak2k2md` (S2) == `86ak0fte4` (S1) | exata |
| 2 | Conferir se os links de todas as páginas do evento estão na planilha | `86ak2k2z0` (S2) == `86ak0ft7h` (S1) | exata |
| 3 | Atualizar página de Captação | `86ak0ftft` "página de Captura" | semântica |
| 4 | Atualizar copy de criativos de Captação (lotes) | `86ak0fmvw` sem "(lotes)" | semântica |
| 5 | Criar copy das imagens de API (acrescentar todos os bônus de escassez) | `86ak2jwtf` "Copy de imagens de API para bônus" | semântica |

**Mantidas separadas** (avaliadas e descartadas como duplicata):

- `Conferir UTMs de captação e vendas` vs `Atualizar links de UTMs` — etapas sequenciais
- `Reservar Hugo` vs `Confirmar com Luca se o Hugo fará a live` — sequenciais
- `Atualizar página de vendas` (Webdesigner) vs `Atualizar copy Página de Vendas` (Copy) — disciplinas distintas
- `Atualizar criativos de captação` (Design) vs `Atualizar copy de criativos` (Copy) — arte vs texto

## Decisões aplicadas

- **Status:** preservado no Brasil (fiel à origem); resetar para `a fazer` no Latam
- **Responsáveis:** preservados
- **Due dates:** descartados — eram específicos das sprints de ago/2026, não pertencem a um backlog
- **Correção de digitação:** `Atualiza copy Carta de Vendas` → `Atualizar copy Carta de Vendas`

## Estrutura final (9 disciplinas / 47 folhas)

| Disciplina | Folhas |
|---|---|
| Gestão | 13 |
| Copy | 15 |
| Webdesigner | 8 |
| Design | 5 |
| Gestão de Tráfego | 2 |
| Suporte / CS | 2 |
| Automação | 2 |
| Comercial | 0 |
| Edição de vídeo | 0 |

---

## ✅ JÁ CRIADO — Backlog Black Friday Brasil (`901328245846`)

### Pais (9/9 completos)

| Disciplina | ID | Status | Responsáveis |
|---|---|---|---|
| Gestão | `86ak4bea5` | fazendo | Keila, Gabriela |
| Copy | `86ak4beaj` | fazendo | Adriane, Matheus |
| Webdesigner | `86ak4beb0` | a fazer | André |
| Design | `86ak4bebf` | a fazer | — |
| Gestão de Tráfego | `86ak4bebw` | a fazer | — |
| Suporte / CS | `86ak4bec7` | a fazer | — |
| Automação | `86ak4becr` | a fazer | — |
| Comercial | `86ak4bed4` | a fazer | — |
| Edição de vídeo | `86ak4bedn` | a fazer | — |

### Gestão — 13/13 completo (pai `86ak4bea5`)

`86ak4bemw` Estruturar o drive do lançamento (fazendo, Gabriela)
`86ak4benr` Pedir os melhores ads e páginas para o tráfego do lançamento anterior (fazendo, Gabriela)
`86ak4bep7` Atualizar backlog Clickup (fazendo, Gabriela)
`86ak4bepw` Atualizar planilha de Ads do tráfego (Gabriela)
`86ak4beqb` Organizar Ads nas pastas (Gabriela)
`86ak4beqw` Brifar os ajustes nos criativos e materiais para Designer (Gabriela)
`86ak4berc` Confirmar com Luca se a live será na Dermadream (reserva 15 dias de antecedência) (feito, Keila)
`86ak4berw` Confirmar com Luca se o Hugo fará a live
`86ak4betd` Reservar Hugo
`86ak4betu` Inserir pasta de depoimentos na pasta SLIDES
`86ak4beu8` Atualizar pasta de logo
`86ak4beuu` Compartilhar com Luca os links de Captação
`86ak4bevg` Conferir se os leads estão caindo no CRM na lista certa

### Copy — 8/15 (pai `86ak4beaj`, todas com Adriane + Matheus)

`86ak4bez3` Atualizar copy de criativos de Captação (lotes) (feito)
`86ak4bezu` Atualizar legendas de criativos
`86ak4bf04` Copy de onboarding + grupo cheio + descrição grupo VIP (fazendo)
`86ak4bf0m` Atualizar copy Página de Vendas
`86ak4bf1e` Atualizar copy Página Lista de espera
`86ak4bf2k` Atualizar copy Carta de Vendas
`86ak4bf3j` Copy 3 mensagens de API (MKT para o comercial disparar)
`86ak4bf3y` Atualizar copy página de obrigado/pesquisa

---

## ⏳ FALTA CRIAR

### Brasil (`901328245846`) — 26 folhas

**Copy** (pai `86ak4beaj`, todas com assignees `55090440`, `82063965`) — 7 restantes:
1. Atualizar copy criativos de lembrete — status `feito`
2. Atualizar copy criativos de Remarketing — status `feito`
3. Atualizar copy criativos de Vendas
4. Criar copy das imagens de API (acrescentar todos os bônus de escassez)
5. Copy motion
6. Copy do ingresso
7. Criar descrição aula do youtube

**Webdesigner** (pai `86ak4beb0`) — 8:
1. Conferir se os links de todas as páginas do evento estão na planilha
2. Atualizar lista no formulário + grupo whatsapp
3. Atualizar página de obrigado + pesquisa
4. Atualizar página de Captação
5. Página de não aluno/aluno
6. Redirecionamento: https://joaopithon.com.br/evento-grupo
7. Criar página link pra Zoom
8. Atualizar página de vendas

**Design** (pai `86ak4bebf`) — 5:
1. Atualizar arte do ingresso
2. Criar thumb da Aula
3. Capa grupo whatsapp
4. Capa de forms de não compradores
5. Atualizar criativos de captação

**Gestão de Tráfego** (pai `86ak4bebw`) — 2:
1. Conferir UTMs de captação e vendas
2. Atualizar links de UTMs (captação e vendas)

**Suporte / CS** (pai `86ak4bec7`) — 2:
1. Criar link da aula no YouTube
2. Atualizar pesquisa NPS - O que faltou para ser meu aluno

**Automação** (pai `86ak4becr`) — 2:
1. Criar comunidade normal + vip
2. Link de webhook

### Latam (`901328249233`) — 56 tarefas (9 pais + 47 folhas)

Cópia integral da estrutura acima, com **todos os status resetados para
`a fazer`** (mercado novo, nada executado). Responsáveis preservados.

## Total

| | Tarefas |
|---|---|
| Criadas | 30 |
| Faltando (Brasil) | 26 |
| Faltando (Latam) | 56 |
| **Total do plano** | **112** |
