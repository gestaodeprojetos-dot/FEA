---
name: fea-paginas
description: Criar, ajustar, publicar e conferir páginas de captura e de vendas do ecossistema FEA / Dr. João Pithon (feb, fep, iff, fef e lp.joaopithon.com.br). Use quando pedirem para mexer numa página existente a partir de um briefing (ex. briefing do Luca), criar página nova de lançamento, publicar no WordPress/Elementor ou no Cloudflare Pages, ou conferir se uma página está no ar e funcionando.
---

# FEA: páginas (ajuste, criação, publicação e conferência)

Playbook validado na prática em 03/11/2026, no ajuste da página da Masterclass em Toxina (feb.joaopithon.com.br/mtb) para a live de 9/11. Escreva sempre em português, sem travessão (em-dash), sempre "para" e nunca "pra", e explique qualquer termo técnico em 1 ou 2 frases simples: quem pede não é técnico.

## 1. Mapa técnico do ecossistema (auditado em 03/11/2026, reconfirmar se mudar)

| Endereço | O que é |
|---|---|
| `joaopithon.com.br` | WordPress principal (separado dos subdomínios) |
| `feb.`, `fep.`, `iff.`, `fef.joaopithon.com.br` | Cada um é um WordPress próprio: Elementor + PRO Elements, tema Hello Elementor, cache WP Rocket, PHP 8.2, hospedagem LiteSpeed (Núcleo Brasil Servidores) |
| `lp.joaopithon.com.br` | Site estático no Cloudflare, mantido pelo André Vivas (webdesigner) |
| Cloudflare | Fica na frente de tudo: DNS, segurança, CDN e SSL. O HTML das páginas WordPress NÃO fica em cache nele (`cf-cache-status: DYNAMIC`), então não precisa purgar depois de editar |

Fatos que mudam a estratégia:
- **Página se edita no WordPress, nunca no Cloudflare.** O Cloudflare só entra para DNS (subdomínio novo), segurança, ou purga de cache de arquivo estático.
- **O login do WordPress tem captcha da hospedagem (recaptcha.cloud) + desafio do Cloudflare.** Automação a partir de servidor/nuvem NÃO passa. Não tente contornar e não peça para afrouxar segurança. Use a extensão Claude no Chrome, que roda no navegador já logado da pessoa (seção 4).
- Formulários das páginas: widget Form do Elementor integrado ao ActiveCampaign, com campos ocultos de UTM (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `vk_source`, `vk_ad_id`), máscara de telefone e redirecionamento pós-envio para `/pesquisa` (que leva ao grupo de WhatsApp). Esses scripts ficam em widgets HTML no fim da página.

## 2. Antes de mexer: diagnóstico (sem pedir nada a ninguém)

1. Ler o briefing inteiro. Se vier como link de artifact do Claude, ler pelo próprio artifact. Se vier como Google Doc público: `curl -sL "https://docs.google.com/document/d/{ID}/export?format=txt"`.
2. Baixar a página no ar (`curl -sL -D headers.txt URL -o page.html`) e mapear os widgets do Elementor pelos atributos `data-id` e `data-widget_type`. Isso mostra exatamente o que existe, em que ordem, e o que já foi alterado (no caso MTB, a data do cartão e o alvo da contagem já estavam atualizados: o briefing pedia 4 ajustes, só 3 faltavam).
3. Medir a primeira tela no celular com Playwright (script em `referencias/FEA-teste-primeira-tela.js`): posição do fim do botão principal contra a altura visível em iPhone 13/14 (664px), iPhone SE (568), Galaxy S9+ (658), Galaxy S24 (780), Pixel 7 (839) e desktop. **Não confie na premissa do briefing**: no caso MTB o briefing dizia que o botão estava na primeira tela, mas nos iPhones comuns ele já estava abaixo.
4. Separar: o que o briefing manda mudar, o que manda manter, o que proíbe.

## 3. Construir os ajustes como blocos HTML prontos

Para cada elemento novo, gerar um bloco para colar num widget **HTML** do Elementor (exemplos reais em `referencias/`). Regras aprendidas:

- Classes com prefixo próprio (`mtb-...`) para não colidir com o tema.
- Fazer o widget ocupar a largura toda sem depender de configuração manual: `.elementor-element:has(> .elementor-widget-container > .minha-classe){width:100%;max-width:100%}`.
- Script que precisa rodar já no carregamento (ex.: contagem regressiva) usa `<script nowprocket>`. Sem isso o WP Rocket atrasa o script até a primeira interação do visitante.
- Contagem regressiva com horário absoluto em UTC (`Date.UTC(ano, mês-1, dia, hora+3, 0, 0)` para horário de Brasília), para funcionar igual em qualquer fuso. Reservar a altura da linha (`&nbsp;`) para a página não "pular" quando o número aparecer.
- Fonte da página (Inter) nos textos de apoio; cores e fontes exatamente as do briefing.
- `text-wrap:balance` em títulos de 2 linhas, para não sobrar palavra sozinha.
- Testar ANTES de entregar: injetar os blocos na página real via Playwright (substituindo os widgets no DOM), medir de novo a primeira tela em todos os aparelhos, conferir que a linha pequena cabe em 320px de largura e tirar prints.
- Se a mudança empurrar o botão para fora da primeira tela, dizer com números (antes x depois por aparelho) e recomendar, sem esconder o trade-off.

## 4. Aplicar no WordPress via extensão Claude no Chrome

A pessoa abre o WordPress logado no Chrome e cola na extensão um prompt autossuficiente, neste formato:

```
Tarefa: aplicar N ajustes na página X do WordPress Y (Elementor). Página no ar com tráfego pago: siga as regras de segurança.
REGRAS DE SEGURANÇA
- NUNCA apague, mova ou altere: formulário, botão principal, título, subheadline, [lista do briefing], e os widgets HTML do fim da página (UTM e redirecionamento).
- Se apagar algo errado, Ctrl+Z na hora. Em dúvida, PARE e pergunte. Só clique em "Atualizar" depois da conferência.
PASSO 0: abrir wp-admin > Páginas > [página] (ID n) > Editar com Elementor.
PASSO 1..N: [ação exata, com o texto ou o código EXATO para colar e a posição exata, citando os textos vizinhos]
PASSO de conferência: modo celular, checklist do que deve aparecer. (A contagem pode ficar vazia dentro do editor, é normal.)
PASSO: Atualizar. Depois WP Rocket > Limpar cache.
PASSO final: responder com resumo por passo e qualquer diferença.
```

Tranquilizar quem pede: editar no Elementor não tira a página do ar. O público vê a versão antiga até clicar em **Atualizar**, e a troca é instantânea. Rollback: Elementor > Histórico > Revisões.

## 5. Conferência depois de publicado (obrigatória antes de dizer "está no ar")

1. Baixar de novo a página e confirmar, widget por widget, que o que devia mudar mudou e o que não devia está idêntico (comparar os `form_fields` e o código dos scripts de UTM/redirecionamento com a versão anterior).
2. Abrir com `?utm_source=teste` e confirmar que o campo oculto `utm_source` foi preenchido.
3. Rodar a medição de primeira tela e tirar prints em vários celulares; conferir que a contagem aparece sem interação e a tarja fixa continua fixa ao rolar.
4. Conferir a página pós-envio (`/pesquisa`) e para onde vai o link do grupo.
5. Não fazer inscrição de teste real (cria lead falso no ActiveCampaign) sem combinar.

## 6. Página nova (lançamento sem referência)

Princípio: aprovar no protótipo, construir depois. Fluxo: briefing → estrutura e copy → protótipo HTML num link privado para aprovação → construção → ligações (formulário, lista e tags no ActiveCampaign, UTMs, pixel, redirecionamento, grupo) → conferência da seção 5.

Checklist do briefing (perguntar o que faltar, nunca inventar): produto e evento (nome, data, hora, formato, replay), público e estágio de consciência, promessa central, oferta e o que pode/não pode ser revelado, ação esperada, identidade visual (FEA, do produto ou outra), pós-inscrição (obrigado, pesquisa, grupo), campos do formulário + lista e tags do ActiveCampaign, UTMs e pixel, prazo e aprovador.

Página duplicada de outra (Elementor > Salvar como modelo > Inserir na página nova) tem 3 armadilhas: o formulário continua mandando para a lista e as tags do evento antigo; o redirecionamento continua indo para o grupo antigo; datas e contagem vêm junto. Corrigir as três.

Sugestão estrutural: manter uma página modelo vazia (`FEA-modelo-base-captura`) com o esqueleto técnico testado (formulário, UTMs, redirecionamento, pixel, tarja com contagem).

## 7. Caminho mais rápido: Cloudflare Pages

Página estática em código, publicada direto pelo Claude, sem Elementor nem captcha. Mais rápida de entregar e de carregar; a contrapartida é que o time não edita sozinho.
- Precisa de um API token do Cloudflare criado pela pessoa: `Account > Cloudflare Pages > Edit`, `Account > Account Settings > Read`, `Zone > DNS > Edit` restrito à zona `joaopithon.com.br`, mais o Account ID.
- **Nunca publicar dentro do projeto do André (`lp.joaopithon.com.br`)**: cada publicação substitui o projeto inteiro e apagaria as páginas dele. Criar um projeto separado num subdomínio próprio (ex.: `paginas.joaopithon.com.br`). Adicionar um subdomínio novo não afeta registros existentes; nunca alterar ou apagar registros de DNS existentes sem mapear antes (risco de derrubar site e e-mail).
- Não migrar páginas que já convertem; usar no próximo lançamento novo como piloto e comparar.

## 8. Copy e compliance (resumo; o tom completo está no CLAUDE.md do projeto FEA)

Público B2B técnico (médicos, dentistas, biomédicos, farmacêuticos), nunca leigo. Tom médico-científico, foco em segurança. Nunca: prometer resultado estético, citar preço/lote/parcelas quando o briefing proíbe, revelar bônus "mistério", urgência falsa, nomear marca sem aprovação, travessão, "pra". Frases como "só para quem estiver ao vivo" só entram se confirmadas.

## 9. Segurança operacional

- Credenciais: preferir usuário temporário com função Editor, apagado no fim; lembrar de trocar senha que tenha sido escrita em conversa.
- Repositórios com contexto de cliente devem ser privados.
- Em página com tráfego pago: mapear o estado atual, ter rollback (Revisões), aplicar, conferir. Nunca mexer em formulário, pixel, DNS ou automação sem confirmar com quem é responsável (automação de e-mail: Júlio Couto; conta ActiveCampaign: Mariano; tráfego e pixel: Matheus Saar; páginas: André Vivas).
