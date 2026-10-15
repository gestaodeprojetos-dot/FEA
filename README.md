# FEA

Contexto operacional do projeto FEA (Formação Especialista em Anatomia, Dr. João Pithon) em arquivo único: `CLAUDE.md` na raiz.

Cobre as regras de comportamento da Keila (autonomia, disciplina de estilo, protocolo de execução, padrão de qualidade, regras de arquivo, multi-cliente), a nomenclatura obrigatória com prefixo FEA em tudo que for criado, o sistema de gestão de projetos e ClickUp (regra de datas, backlog de lançamento, ronda de prazos), todo o contexto do cliente FEA (identidade, tom médico-científico, linha vermelha, identidade visual, produtos, calendário, equipe, copy, Funil Eterno, acessos) e o template de SOP.

## Skill `fea-central`

O mesmo contexto está empacotado como skill em `.claude/skills/fea-central/`, para poder ser carregado sob demanda e levado para outros logins ou repositórios.

```
.claude/skills/fea-central/
├── SKILL.md                            # regras de comportamento + índice
└── references/
    ├── FEA-cliente.md                  # cliente FEA: tom, linha vermelha, identidade visual, produtos, calendário, equipe, copy, Funil Eterno
    ├── FEA-clickup-gestao.md           # ClickUp: regra de datas, backlog de lançamento, ronda de prazos
    └── FEA-template-sop.md             # template de SOP e checklist
```

Ativa automaticamente pelo campo `description` (FEA, João Pithon, ClickUp, SOP, copy de lançamento, ActiveCampaign) ou manualmente com `/fea-central`.

**Instalar em outro login ou máquina**, para valer em qualquer pasta:

```bash
mkdir -p ~/.claude/skills && cp -r .claude/skills/fea-central ~/.claude/skills/
```

Dentro deste repositório não precisa copiar nada, o Claude Code lê `.claude/skills/` do próprio projeto.
