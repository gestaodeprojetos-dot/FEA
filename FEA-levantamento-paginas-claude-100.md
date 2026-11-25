# FEA: levantamento para o Claude criar páginas de ponta a ponta

Versão de 24/11/2026. Base: "Processo de criação de páginas · Mapa para a gestão" (André, 23/11) e "Montar uma página do briefing à prévia" (André, 24/11). Testes de acesso feitos nesta data.

Objetivo: o Luca manda o briefing no grupo e o Claude entrega a página pronta para aprovação, sem passar pelo Claude Design.

## 1. Já funciona (testado em 24/11)

| Item | Situação |
|---|---|
| Hotmart | Conector ativo: lista produtos e ofertas (códigos para os botões de compra) |
| WhatsApp (número Atendimento FEA) | Conector ativo; o número está em 25 grupos, inclusive "Web \| FEA", "Copy \| FEA", "Artes \| FEA" e "Elite Experience \| 04 e 05/12": dá para ler o briefing direto do grupo |
| Google Drive | Conector ativo: lê copy, fotos e pastas compartilhadas |
| Ferramentas de construção | Node 22 e Astro instaláveis; tratamento técnico de imagem (recorte, redimensionamento, WebP e AVIF) |
| Testes visuais | Navegador automático: prints em 360, 390, 430, 1440 e 1920 px e mais larguras, captura de páginas de referência |
| GitHub | Conector ativo para branch, pull request e publicação, assim que o repositório abrir |

## 2. Bloqueia (sem isso não sai página)

| # | Falta | Detalhe |
|---|---|---|
| 1 | Acesso ao repositório `oandrevivas/lp-joaopithon` | Liberado em 25/11 (leitura e escrita, registrado no WEB-439). O nome certo do dono é `oandrevivas`; os testes anteriores falhavam por usar `andrevivas`. Ligar o repositório na sessão só quando houver demanda de página |
| 2 | Combinado com o André: páginas criadas pelo Claude nascem no código, sem projeto no Claude Design | O próprio documento do André recomenda que o Claude Design fique só com ele. Sem projeto de design, não há o que sincronizar: o código é a única versão. Se um dia ele quiser redesenhar, traz a página do ar para o Claude Design, como já faz |
| 3 | Quem dá a ordem de publicar as páginas criadas pelo Claude | Hoje o processo exige ordem do André. Proposta: aprovação do Luca na prévia + "pode publicar" da Keila; o André acompanha pelo alarme |
| 4 | Qual grupo é o canal oficial de briefing | Provável "Web \| FEA". Confirmar, e combinar que o briefing chega em uma mensagem ou documento único |
| 5 | Quem entrega a copy | O briefing do Luca traz a copy pronta, ou o Claude escreve e o Luca aprova |

## 3. Necessário para a página funcionar completa (rastreamento e formulário)

| # | Falta | Por quê |
|---|---|---|
| 6 | Acesso ao GTM (contêiner das páginas) | Botão ou página nova cria evento novo, que só aparece nos relatórios depois que o gatilho é criado. Pela nuvem, o caminho é uma conta de serviço do Google com permissão de edição no contêiner, guardada nos segredos do ambiente; publicar no GTM só combinado com o tráfego. Alternativa: o Claude entrega a lista de eventos e o tráfego cria os gatilhos |
| 7 | Acesso ao ActiveCampaign (endereço da conta + chave de API nos segredos do ambiente) | O conector está instalado mas sem configuração. Necessário para criar ou conferir formulário, lista e tags de cada evento |
| 8 | Regra dos formulários | Quando usar ActiveCampaign, Respondi ou Google Apps Script em página nova |
| 9 | Cloudflare | Conectado em 24/11 (conector oficial, uso só de leitura). Prévias virão pelo GitHub; chave de publicação só se alguma página ficar fora do repositório |

| 10 | WordPress (6 sites) | API responde da nuvem sem captcha (testado 25/11). Usuário `claude-fea` e Senha de aplicativo criados em 5 sites em 25/11 (site, feb, iff, fef, pl); fep pendente. Falta guardar `WP_USER` e `WP_PASS_<SITE>` nas variáveis do ambiente da nuvem |

## 4. Materiais (uma vez, depois só atualizar)

| # | Falta | Por quê |
|---|---|---|
| 10 | Banco de imagens já tratadas: fotos do Dr. João em alta, recortes sem fundo, fotos de eventos e de cadáver fresco liberadas | O Claude recorta, redimensiona e converte. Retoque e montagem de Photoshop ficam fora. Imagem gerada por IA não entra em página (regra FEA) |
| 11 | Pasta de depoimentos aprovados para página, com autorização | Há o grupo "Depoimentos \| FEA" com pasta no Drive: confirmar quais podem ir para página |
| 12 | Números oficiais com fonte | Alunos formados, anos, turmas: só entram com fonte |
| 13 | Links de visualização dos projetos do Claude Design do André | Para o Claude aprender o padrão visual de cada marca, junto com as páginas que já estão no repositório |
| 14 | Biblioteca de referências aprovadas por tipo de seção | Proposta do próprio André; o Claude monta e mantém a partir das páginas que forem ao ar |

## 5. Etapas que continuam humanas

| Etapa | Quem |
|---|---|
| Aprovar o visual na prévia (substitui a etapa 5) | Luca |
| Abrir a prévia num iPhone de verdade (o navegador automático simula, não substitui) | Quem aprova |
| Autorizar publicar | Conforme combinado do item 3 |
| Tratamento de imagem que exige Photoshop | Designer |

## 6. Como fica o fluxo

1. Luca manda o briefing no grupo.
2. Claude confere o briefing contra o checklist e devolve o que faltar.
3. Claude consulta as ofertas na Hotmart e os materiais no Drive.
4. Claude monta a pesquisa de referências (com prints) a partir do modelo mais recente da mesma marca.
5. Claude cria a página numa branch, já no código.
6. Claude roda o checklist de testes do André e manda prévia, prints e relatório.
7. Luca aprova ou pede ajuste; os ajustes voltam para o passo 5.
8. Com o "pode publicar", Claude publica pelo GitHub, confere no ar e testa o botão principal sem enviar formulário.
9. Claude entrega a lista de eventos novos para o GTM.

Sugestão de início: uma página Expressa ou Essencial (modelo de marca já existente). Depois, uma Bem trabalhada como piloto, comparada com o padrão do André.
