# Backlog Black Friday — unificação e deduplicação

Migração das demandas da pasta **Black Friday Vitalícia 10/26** (Space
`Marketing`, workspace `9013080622`) para as listas de Backlog Brasil e Latam.

> **✅ CONCLUÍDO — 112/112 tarefas.** Brasil 56/56, Latam 56/56.
> Verificado por `filter_tasks` nas duas listas após a criação.

## Origem

| Lista | ID | Pais | Folhas |
|---|---|---|---|
| Sprint 1 (17/8 - 23/8) | `901328170220` | 9 | 40 |
| Sprint 2 (24/8 - 30/8) | `901328179817` | 4 | 10 |
| Sprint 3 (31/8 - 6/9) | `901328225835` | 1 | 2 |
| **Total** | | **14** | **52** |

66 tarefas na origem. As tarefas-pai são disciplinas que se repetem entre
sprints (Design ×2, Copy ×2, Webdesigner ×2, Gestão ×3).

**As 66 tarefas originais permanecem intactas nas sprints** — o backlog
recebeu cópias, não houve movimentação.

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

- **Status:** preservado no Brasil (fiel à origem — 6 tarefas em `feito`/`fazendo`); resetado para `a fazer` em todo o Latam (mercado novo)
- **Responsáveis:** preservados nas duas listas
- **Due dates:** descartados — eram específicos das sprints de ago/2026, não pertencem a um backlog
- **Correção de digitação:** `Atualiza copy Carta de Vendas` → `Atualizar copy Carta de Vendas`

## Estrutura final — idêntica nas duas listas

| Disciplina | Pai (Brasil) | Pai (Latam) | Folhas |
|---|---|---|---|
| Gestão | `86ak4bea5` | `86ak4jzkn` | 13 |
| Copy | `86ak4beaj` | `86ak4jzn6` | 15 |
| Webdesigner | `86ak4beb0` | `86ak4jzpw` | 8 |
| Design | `86ak4bebf` | `86ak4jztb` | 5 |
| Gestão de Tráfego | `86ak4bebw` | `86ak4jzuv` | 2 |
| Suporte / CS | `86ak4bec7` | `86ak4jzwc` | 2 |
| Automação | `86ak4becr` | `86ak4jzy4` | 2 |
| Comercial | `86ak4bed4` | `86ak4jzzr` | 0 |
| Edição de vídeo | `86ak4bedn` | `86ak4k017` | 0 |
| **Total** | | | **9 + 47 = 56** |

- Brasil: https://app.clickup.com/9013080622/v/l/li/901328245846
- Latam: https://app.clickup.com/9013080622/v/l/li/901328249233

## Histórico de execução

A migração foi interrompida duas vezes pelo rate limit do conector ClickUp:

| Tentativa | Criadas | Bloqueio |
|---|---|---|
| 1 | 30 | `wait 331 minutes` (~5h30) |
| 2 | +50 (80) | `wait 1436 minutes` (~24h) |
| 3 | +32 (112) | — concluído |

O intervalo de ~24h da segunda janela indica **cota diária de chamadas de API
no workspace**, não limite de burst — reduzir o ritmo das chamadas não contorna
o bloqueio, só a virada do dia. O mesmo workspace exibe o aviso *"Você
ultrapassou seu limite de armazenamento"* na interface, o que sugere limites
ligados ao plano.

Para migrações futuras desse tamanho: contar com ~2 dias de janela, ou criar
pela interface do ClickUp (que não passa pela API e não consome a cota).
