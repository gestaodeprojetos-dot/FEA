# FEA · Comando para o Claude Design aprender as regras de 27/11

Cole o texto abaixo, inteiro, na conversa do Claude da outra conta (o que executa as tasks com a etiqueta `claude-design`).

---

Regras novas da FEA, passadas pela Keila hoje (27/11). Valem a partir de agora em toda task `claude-design` (artes, páginas no lp.joaopithon e WordPress). Guarde na sua memória e nas suas skills e confirme com "Regras de 27/11 anotadas", listando os 9 itens em uma linha cada.

1. **Nome da PR diz qual página.** Toda PR de página tem, no começo do título, o código `PR-PRODUTO-PÁGINA-n`, em que n é o número da PR (ex.: `PR-PLX-LATAM-18`, `PR-MASTERBIO-20`, `PR-AULAZERO-15`, `PR-ZOOM-32`). Use o mesmo código em todo comentário e retorno. Só o número não basta.

2. **Publicação.** Você nunca faz merge na `main` (todo push na main publica o site). Abra a PR sempre como draft, com o link da prévia (`https://<branch-com-hifens>-lp-joaopithon.suporte-ca6.workers.dev/<rota>/`) junto do link do GitHub. Quem publica é a sessão principal, com o ok da Keila ou da Gabi no formato "pode publicar a PR-XXX-n".

3. **Retorno completo.** Todo retorno na task, ao voltar para "em revisão", diz: (a) o que você fez, (b) qual é o próximo passo, (c) para quem vai. Comentário no ClickUp começa com "🤖 Claude:".

4. **Nunca deduzir.** Só afirme com a informação na mão (arquivo aberto, link testado, página conferida). Faltou dado: escreva na task o que falta e de quem, nunca invente link, data, preço ou sala de Zoom.

5. **Antes de atribuir uma entrega a um setor, confira quem faz.** Exemplo do erro de 26/11: escrevemos que o formulário da captura vinha da Automação sem ninguém ter definido. Regra: o formulário do ActiveCampaign das páginas de captura é do André; a Automação cria listas, tags e webhooks.

6. **Escrita FEA em toda página, arte e texto.** Nunca "pra" (sempre "para"), zero travessão (—), sem palavras de enchimento. Vale também para texto que veio do WordPress ao migrar uma página: corrija e liste a correção.

7. **Mensagens de grupo de evento (se a task envolver copy de grupo).** O doc fica em ordem cronológica de envio; tom caloroso e próximo, sem exagero, modelado nos lembretes de grupo de eventos anteriores; emoji de mão 🏽 nessas mensagens; nenhuma mensagem duplicada; dúvida de copy vai ao Matheus van der Ham.

8. **WordPress.** Usuário e senha vêm só da descrição da task (ou das variáveis do ambiente). Nunca repita a senha em comentário, PR, mensagem, arquivo ou print. Antes de mexer em redirecionamento ou página no ar, anote o estado atual (para poder voltar atrás) e, depois, teste cada link com o destino final e as UTMs.

9. **Não mexer no que está no ar sem o dado confirmado.** Exemplo: os atalhos `masterclass-grupo` e `aula-zoom` da Master Bio só mudam depois que a gestão confirmar o link do grupo e a sala do Zoom; até lá, só o que a task marca como "agora".

Task em andamento para aplicar já: https://app.clickup.com/t/17th71zb9ha (Redirecionamentos da Master Bio 12/26 no WordPress).
