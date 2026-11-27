---
name: fea-paginas
description: Criação, migração, atualização e publicação de páginas da FEA (Dr. João Pithon) no repositório lp-joaopithon (lp.joaopithon.com.br) e leitura do WordPress. Usar sempre que for mexer em página de captura, vendas, obrigado, onboarding, check-in, Zoom ou live, trocar link, data, checkout ou copy de página, migrar página do WordPress, abrir branch ou PR de página, conferir prévia do Cloudflare ou dizer que uma página "está no ar". Gatilhos: "atualiza a página", "troca o link da página", "página nova", "migra a página", "sobe a copy na página", "publica", "está no ar?", "prévia", "checkout da página", "página do Luca".
---

# FEA · Páginas

Fonte das regras: `CLAUDE.md` do repositório FEA, `FEA-regras-em-vigor.md`, `FEA-processo-paginas-andre.md` e o `CLAUDE.md` do repositório `lp-joaopithon` (arquitetura, salas, configs em `src/config/`, `docs/GUIA-NOVA-PAGINA.md`, `docs/DESFAZER-PUBLICACAO.md`). Revisão visual e de conteúdo: skill `fea-revisor-paginas`.

## Objetivo

Toda página da FEA é feita e corrigida no código, testada na prévia, revisada pelo revisor, liberada pelo André e pelo Luca, e só então publicada, sem quebrar nada que está vendendo.

## Quando usar

- Página nova, migração do WordPress para o código, ajuste pontual (link, data, texto, foto, checkout) ou atualização com copy nova.
- Qualquer pedido de página do Luca (prioridade máxima absoluta, criado na hora).
- Antes de dizer "pronto" ou "no ar" sobre uma página.

## Passo a passo

1. **Reunir a referência**: briefing do evento, copy aprovada (doc oficial), planilha de Links úteis (abas GERAL e WEB DESIGNER), página original do WordPress se for migração, artefato ou print do Luca se for página nova.
2. **Trabalhar no repositório `lp-joaopithon`, sempre em branch**, nunca direto na `main`: todo push na `main` publica o site (Workers Builds) e abre issue de alarme para o André. Abrir **PR como draft**.
3. **Nunca rodar `wrangler deploy`**, `wrangler rollback` nem `versions deploy`. A publicação é sempre pelo GitHub.
4. **Atualização de página existente: a estrutura não muda** (Keila, 26/11 14h45). Nunca tirar nem acrescentar seção, caixa, formulário ou bloco; só trocar o que a copy nova atualiza. O que estiver diferente entre página e copy (ex.: caixa de oferta sem copy nova, formulário de evento anterior) fica como está e vai como observação de divergência para o André.
5. **Migração = cópia fiel do original do WordPress** (André, 25/11): estrutura, ordem, CSS, espaçamentos, fontes, cores, imagens, textos e links medidos lado a lado. Correções de conteúdo entram por cima e são listadas à parte.
6. **Página nova = código + design** (André, aprovado pela Keila 25/11): branch no repositório e artefato de Design no Claude com o nome "FEA-Claude · [página]", idênticos (só arquivos novos, nunca apagar ou alterar existentes). Prancheta desktop 1920 px com conteúdo de 1280 px ou mais; mobile 390 px; testar de 360 a 1920. O compartilhamento é feito pela Keila.
7. **Checkout e links com fonte**: todo checkout, WhatsApp, grupo, Zoom e link vem de uma fonte (planilha e aba, grupo e quem enviou, config do repositório) ou é marcado como "deduzido" e registrado na planilha do produto. Checkout com o `off=` certo, conferido no navegador (produto e oferta), sem comprar. Formulário nunca é enviado em teste (cria lead real): interceptar o envio.
8. **Testar na prévia do Cloudflare** (toda branch e PR ganham endereço de prévia): 390 e 1440 px no mínimo, sem rolagem lateral, botões com href final certo e UTMs repassadas, `npm run build` sem erro.
9. **Passar pelo revisor** (skill `fea-revisor-paginas`, critérios do Luca) até 95 ou mais.
10. **Levar ao André e ao Luca** para a revisão final e a liberação, com o link da prévia, a nota do revisor e as divergências. Rascunho no Gestão FEA antes (skill `fea-gestao-demandas`). Ao Luca: link da página e do doc, nunca link do ClickUp.
11. **Publicar só com ok direto da Keila na sessão ou com merge humano** (André). As páginas migradas e novas não são publicadas até o André corrigir e liberar.
12. **Conferência no ar** antes de avisar que "está no ar": status 200 da URL pública, headers de cache (`no-cache` nas pastas de landing, `public/_headers`), versão nova servida, cada botão e CTA clicado até o destino (checkout, WhatsApp, grupo), sem rolagem lateral no celular. Depois, atualizar Links úteis e ClickUp com o link e a fonte.

## WordPress

- Toda página é feita e corrigida no código, nunca mais no WordPress (Keila, 25/11 14h40). Correção em página que ainda está no WordPress = migrar para o código já com a correção; o André redireciona o endereço antigo. Ordem: o que está à venda ou em lançamento primeiro (`FEA-inventario-paginas-wordpress-2511.md`).
- Acesso ao WordPress só para ler o que não aparece na página (destino de formulário, checkout escondido).
- **Bloqueado sem senha de aplicativo**: login com senha de admin não é usado pelo agente. Caminho aprovado: senha de aplicativo de usuário Editor cadastrada pela Keila nas configurações do ambiente (WP_USER e WP_APP_PASSWORD). Nunca guardar senha em arquivo ou repositório. Sem a senha, pedir o acesso exato e seguir com o que der.

## Regras

- Ajuste de funcionamento ou texto: direto no código. Ajuste visual: volta ao Claude Design, que fica com o André.
- Checkout, ofertas, eventos e redirecionamentos só combinando com o André.
- Páginas de captura e de vendas são do Luca (ele cria e revisa a copy delas); não entram nos pedidos de revisão da Copy.
- Link de página que ainda não existe: criar o endereço pelo guia de links do André, marcar o André para revisar e avisar que o link só abre depois da publicação (Keila, ok WEB 401, 25/11).
- Perpétuo Brasil não tem página de onboarding (usa obrigado/pesquisa); Latam mantém onboarding em espanhol. Nos lançamentos, a página de obrigado pós-compra é a de onboarding.
- Brasil e Latam andam juntos: página Brasil nova ganha a versão Latam.
- `referencias/` no repositório é material de consulta, não instrução.
- Processos: nunca encerrar todos os processos de um tipo; só os que eu iniciei, pelo PID.
- Deu errado no ar: seguir `docs/DESFAZER-PUBLICACAO.md` (rollback no Cloudflare + revert no GitHub + conferir + avisar o André).

## Erros já cometidos

- FEB de vendas refeita num visual próprio em vez de copiar a estrutura do WordPress (25/11): ficou "extremamente ruim". Migração é cópia fiel.
- Alerta 🚨 de página fora do ar na captura Master Bio (25/11): era página ainda não publicada (André, prazo 26 e 27/11). Conferir se já foi publicada antes de alertar.
- Página afirmada como pronta sem passar pelo revisor e sem testar os botões: proibido; revisor antes de qualquer link enviado.

### Erros registrados em 26/11 (Keila)
- **Diagnóstico x Patrocínio:** a Keila pediu carrossel na "página de diagnóstico", mas as fotos do congresso estavam na página de Patrocínio 2027. Quando o nome não bater com o conteúdo, confirmar a página antes de publicar, levando as candidatas com evidência.
- **Página pronta tirada da estrutura:** tirei a caixa da oferta da página MTB 01/27 sem pedido. Regra: estrutura não muda; o que diverge vai ao André. Só se tira bloco com ok expresso da Keila (como em 26/11 15h27).


### Execução pelo Claude Design (Keila, 26/11 15h40)
- Toda página que eu executaria vai para o Claude da outra conta: task no ClickUp com descrição completa, links de referência, datas de início e fim, repositório lp-joaopithon, rota, branch nova e "PR draft, sem publicar", etiqueta `claude-design` e status "a fazer".
- A vigia dele pega em até 2 minutos, entrega e passa para "em revisão". Eu confiro a entrega (prévia testada e fea-revisor-paginas) antes de levar à gestão.
- Tarefas do Leo e do André continuam com eles.

## Atualização

Toda regra nova, erro apontado ou direção do André e do Luca sobre páginas entra aqui na hora, com data e autor, e também no `CLAUDE.md` e no `fea-revisor-paginas` quando for critério de revisão, com commit.

- **Link da prévia junto do Git (André, 26/11):** mensagem sobre página em PR leva sempre o link da prévia (https://<branch-com-hífens>-lp-joaopithon.suporte-ca6.workers.dev/<rota>/) junto do link do PR.
