# FEA · Comando para o Claude Design assumir as páginas

Cole o texto abaixo, inteiro, na conversa do Claude da outra conta (o que executa as tasks com a etiqueta `claude-design`).

---

A partir de agora (27/11) você assume as páginas da FEA: as do código (repositório `oandrevivas/lp-joaopithon`, site lp.joaopithon.com.br) e as do WordPress (joaopithon.com.br e subdomínios). A sessão principal deixa de executar páginas e só faz a ponte com a gestão e a publicação.

**Antes de começar**
1. Clone `gestaodeprojetos-dot/FEA` (branch `claude/brave-maxwell-hkkfbf`) e leia inteiro: `CLAUDE.md`, `.claude/skills/fea-paginas/SKILL.md`, `.claude/skills/fea-revisor-paginas/SKILL.md`, `.claude/skills/fea-revisor-luca/SKILL.md` e `FEA-comando-claude-design-regras-2711.md` (as 9 regras de hoje).
2. Clone `oandrevivas/lp-joaopithon` e leia o `CLAUDE.md` dele (arquitetura escola, sala e página; nunca `wrangler deploy`; todo push na `main` publica o site).
3. WordPress: para a skill de WordPress, faça `git fetch origin claude/epic-fermat-0r0nw0 && git checkout FETCH_HEAD -- .claude/skills/fea-wordpress FEA-scripts/fea_teste_wp.sh` no repositório FEA e leia `.claude/skills/fea-wordpress/SKILL.md` (User-Agent de navegador, limpar o cache do Elementor depois de cada alteração, foto do estado antes, plano de volta). O acesso está na task https://app.clickup.com/t/17th71zb9ha (descrição e comentário). Nunca repita senha em comentário, PR, mensagem ou arquivo. O fep.joaopithon.com.br ainda não tem acesso.

**Como trabalhar**
- Toda página é feita e corrigida no código. Página que ainda está no WordPress e precisa de correção: migrar para o código já corrigida (cópia fiel: estrutura, textos, cores, fontes, imagens e links medidos lado a lado com o original). No WordPress, só redirecionamentos e o que a task pedir.
- Sempre em branch e PR **draft**, com o título começando por `PR-PRODUTO-PÁGINA-n` e o link da prévia (`https://<branch-com-hifens>-lp-joaopithon.suporte-ca6.workers.dev/<rota>/`) junto do link do GitHub.
- Página existente: a estrutura não muda (não tirar nem acrescentar seções, caixas ou formulários); só o que a copy nova atualiza.
- Antes de devolver: `npm run build` sem erro; nenhum arquivo existente do `dist/` muda além do previsto; prévia testada em 390 e 1440 px; sem rolagem lateral; botões com o destino certo e as UTMs; noindex quando for captura ou página interna; nenhum `[ ]`, `A CONFIRMAR`, `tbd`, "pra" ou travessão no HTML; formulário nunca enviado em teste (cria lead real).
- **Você não publica.** Nunca faz merge na `main` nem marca PR como pronta. Devolve a task em "em revisão" com o comentário "🤖 Claude:" dizendo o que fez, o próximo passo e para quem vai, com o código da PR e os links das prévias. A sessão principal leva à Keila ou à Gabi, e com o ok "pode publicar a PR-XXX-n" ela publica e confere no ar.
- Nunca deduzir link, data, preço, sala de Zoom ou formulário: faltou dado, escreva na task o que falta e de quem.

**O que já está em andamento (assuma a partir daqui)**
1. **PR-ZOOM-32** (FEB, IFF10, MTI e Preenchimento Labial, páginas de Zoom migradas do WordPress): publicada às 10h59 de 27/11; aguardando o Cloudflare colocar no ar. Depois disso, falta redirecionar no WordPress os endereços antigos para as rotas novas: feb.joaopithon.com.br/live-zoom/ → /feb/live-zoom/, iff.joaopithon.com.br/iff10-zoom/ → /iff/iff10-zoom/, iff.joaopithon.com.br/mti-zoom/ → /iff/mti-zoom/, pl.joaopithon.com.br/live-zoom-mpl/ → /preenchimento-labial/live-zoom/ (todas em lp.joaopithon.com.br, 302, mantendo a query string). Só depois de a sessão principal confirmar as 4 no ar.
2. **PR-ZOOM-MASTERBIO-33** (Master Bio, sala 88201058257): ok de publicação da Keila já dado; publicação pela sessão principal assim que a prévia confirmar. Depois: redirecionar bio.joaopithon.com.br/live-zoom/ → https://lp.joaopithon.com.br/febio/live-zoom/.
3. **Redirecionamentos da Master Bio 12/26** (task https://app.clickup.com/t/17th71zb9ha, prazo hoje 18h): atalhos do bio. e páginas antigas do Elementor para a captura e o check-in novos agora; `masterclass-grupo` e `aula-zoom` só depois do link do grupo e da sala confirmados.
4. **Formulários novos das capturas MTB 01/27 e MPL 01/27** (hoje com os formulários 58 e 62 do evento anterior): tasks do André https://app.clickup.com/t/17th71zb99c e https://app.clickup.com/t/17th71zb99d. O fluxo (Vivi cria o formulário e o André integra, ou só o André) está em confirmação com a Gabi: não mexa até a task dizer quem faz.
5. **PRs abertas esperando revisão do André ou ok da gestão** (não refaça; atualize só se a task pedir): 1 PLX Brasil e Latam, 3 Ebook Intercorrências Brasil, 4 Ebook Olheiras, 5 CTX versão B, 6 FEB migração, 7 FEP migração, 8 CTX e upsells, 9 migração lote 3, 10 FEBIO link do grupo (falta o link do Grupo Exclusivo), 13 e 25 patrocínio Elite Injectors 2027 (a 25 espera o número de parcelas do Luca), 14 Elite Mentoring perpétuo, 16 e 19 link na bio (a 2 é versão antiga), 18 PLX Latam onboarding. Ao mexer em qualquer uma, renomeie o título para o padrão `PR-PRODUTO-PÁGINA-n`.

**Confirme** respondendo "Páginas assumidas", com a lista dos 5 itens acima e o que vai fazer primeiro.
