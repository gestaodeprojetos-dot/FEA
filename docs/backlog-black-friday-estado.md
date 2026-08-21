# Backlog Black Friday — unificação e deduplicação

Estado da migração das demandas da pasta **Black Friday Vitalícia 10/26**
(Space `Marketing`, workspace `9013080622`) para as listas de Backlog.

> **Status: Brasil concluído (56/56). Latam parcial (24/56).**
>
> A execução foi interrompida duas vezes pelo rate limit do conector ClickUp:
> primeiro com *"wait 331 minutes"* (~5h30), depois com *"wait 1436 minutes"*
> (~24h). O intervalo de ~24h indica **cota diária**, não limite de burst —
> reduzir o ritmo das chamadas não resolve; só esperar o dia virar.

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

## ✅ CONCLUÍDO — Backlog Black Friday Brasil (`901328245846`)

**56/56 tarefas.** 9 disciplinas + 47 folhas, exatamente conforme o plano acima.
Status preservados da origem (6 tarefas em `feito`/`fazendo`), responsáveis
preservados, due dates descartados.

| Disciplina | ID do pai | Folhas |
|---|---|---|
| Gestão | `86ak4bea5` | 13/13 |
| Copy | `86ak4beaj` | 15/15 |
| Webdesigner | `86ak4beb0` | 8/8 |
| Design | `86ak4bebf` | 5/5 |
| Gestão de Tráfego | `86ak4bebw` | 2/2 |
| Suporte / CS | `86ak4bec7` | 2/2 |
| Automação | `86ak4becr` | 2/2 |
| Comercial | `86ak4bed4` | 0 |
| Edição de vídeo | `86ak4bedn` | 0 |

---

## ⚠️ PARCIAL — Backlog Black Friday Latam (`901328249233`)

**24/56 tarefas.** Todos os status em `a fazer` (mercado novo), responsáveis
preservados.

### Pais (9/9 completos)

| Disciplina | ID | Responsáveis |
|---|---|---|
| Gestão | `86ak4jzkn` | Keila, Gabriela |
| Copy | `86ak4jzn6` | Adriane, Matheus |
| Webdesigner | `86ak4jzpw` | André |
| Design | `86ak4jztb` | — |
| Gestão de Tráfego | `86ak4jzuv` | — |
| Suporte / CS | `86ak4jzwc` | — |
| Automação | `86ak4jzy4` | — |
| Comercial | `86ak4jzzr` | — |
| Edição de vídeo | `86ak4k017` | — |

### Gestão — 13/13 completo (pai `86ak4jzkn`)

Todas criadas: Estruturar o drive do lançamento · Pedir os melhores ads e
páginas · Atualizar backlog Clickup · Atualizar planilha de Ads do tráfego ·
Organizar Ads nas pastas · Brifar os ajustes para Designer · Confirmar com
Luca se a live será na Dermadream · Confirmar com Luca se o Hugo fará a live ·
Reservar Hugo · Inserir pasta de depoimentos na pasta SLIDES · Atualizar pasta
de logo · Compartilhar com Luca os links de Captação · Conferir se os leads
estão caindo no CRM na lista certa

### Copy — 2/15 (pai `86ak4jzn6`)

`86ak4k0p1` Atualizar copy de criativos de Captação (lotes)
`86ak4k0qv` Atualizar legendas de criativos

---

## ⏳ FALTA CRIAR — 32 folhas, todas no Latam (`901328249233`)

Todas com status default (`a fazer`).

**Copy** (pai `86ak4jzn6`, assignees `55090440` + `82063965`) — 13:
1. Copy de onboarding + grupo cheio + descrição grupo VIP
2. Atualizar copy Página de Vendas
3. Atualizar copy Página Lista de espera
4. Atualizar copy Carta de Vendas
5. Copy 3 mensagens de API (MKT para o comercial disparar)
6. Atualizar copy página de obrigado/pesquisa
7. Atualizar copy criativos de lembrete
8. Atualizar copy criativos de Remarketing
9. Atualizar copy criativos de Vendas
10. Criar copy das imagens de API (acrescentar todos os bônus de escassez)
11. Copy motion
12. Copy do ingresso
13. Criar descrição aula do youtube

**Webdesigner** (pai `86ak4jzpw`) — 8:
1. Conferir se os links de todas as páginas do evento estão na planilha
2. Atualizar lista no formulário + grupo whatsapp
3. Atualizar página de obrigado + pesquisa
4. Atualizar página de Captação
5. Página de não aluno/aluno
6. Redirecionamento: https://joaopithon.com.br/evento-grupo
7. Criar página link pra Zoom
8. Atualizar página de vendas

**Design** (pai `86ak4jztb`) — 5:
1. Atualizar arte do ingresso
2. Criar thumb da Aula
3. Capa grupo whatsapp
4. Capa de forms de não compradores
5. Atualizar criativos de captação

**Gestão de Tráfego** (pai `86ak4jzuv`) — 2:
1. Conferir UTMs de captação e vendas
2. Atualizar links de UTMs (captação e vendas)

**Suporte / CS** (pai `86ak4jzwc`) — 2:
1. Criar link da aula no YouTube
2. Atualizar pesquisa NPS - O que faltou para ser meu aluno

**Automação** (pai `86ak4jzy4`) — 2:
1. Criar comunidade normal + vip
2. Link de webhook

## Total

| | Tarefas |
|---|---|
| Brasil — concluído | 56 / 56 |
| Latam — criadas | 24 / 56 |
| Latam — faltando | 32 |
| **Total criado** | **80 / 112** |

## Observação sobre a cota do ClickUp

O conector devolveu duas janelas de espera muito diferentes (~5h30 e ~24h)
para a mesma operação. O padrão indica **cota diária de chamadas de API no
workspace**, provavelmente ligada ao plano — o mesmo workspace exibe o aviso
*"Você ultrapassou seu limite de armazenamento"* na interface. Reduzir o ritmo
das chamadas não contorna isso: as 32 folhas restantes precisam de uma nova
janela diária, ou de criação manual na interface (que não passa pela API).
