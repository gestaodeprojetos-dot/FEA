# Montar uma página do briefing à prévia · respostas para a Gestão FEA

Nov 24, 2026 · @Someone

## Resumo

A parte técnica (estrutura, URL, imagens, checkout e rastreamento) já está documentada no próprio repositório, e vai ganhar um guia único para página nova: `docs/GUIA-NOVA-PAGINA.md`, escrito a partir do código real. Este documento responde cada pergunta em linhas gerais, cobre o que não está no repositório (testes, prévia, design e acessos) e propõe a pauta da call.

Onde ler no repositório, depois de conectada:

- `CLAUDE.md`: no topo, as regras para a gestão e outras IAs; depois, uma seção por projeto (Black Friday, Elite Mentoring, Elite Experience e outros), com páginas, links, eventos e testes de cada um.
- `docs/DESFAZER-PUBLICACAO.md`: como voltar atrás se algo der errado.
- `docs/GUIA-NOVA-PAGINA.md` (em preparação): o passo a passo técnico para página nova.

## 1. Estrutura do repositório

Um site só, em Astro, publicado em lp.joaopithon.com.br. Este repositório não publica outros subdomínios: endereços como bf.joaopithon.com.br são de outros sistemas.

| Pasta | O que guarda |
| --- | --- |
| `src/pages/<caminho>/index.astro` | Cada página é uma pasta; o caminho da pasta é o endereço |
| `src/components/<projeto>/` | As seções de cada página (topo, prova, perguntas, rodapé…) |
| `src/layouts/` | A "sala" de cada marca ou campanha: GTM, pixel da VK, Clarity, fontes e imagem de compartilhamento |
| `src/styles/` | O CSS de cada projeto |
| `src/assets/<projeto>/` | As imagens originais de cada projeto |
| `src/config/` | Links, datas, WhatsApp, lotes e checkouts que mudam com frequência |
| `public/_redirects` e `worker/` | Redirecionamentos (o Worker é só o do encerramento da Black) |

**Modelo base para página nova:** a página mais recente da mesma marca, porque ela já tem a sala, as fontes, o rastreamento e as correções que vieram depois. Exemplos: Elite Mentoring, o diagnóstico; Elite Experience, o teste D; Black Friday, a página de vendas da Vitalícia. O guia vai indicar o modelo de cada marca.

## 2. Padrão de URL

- Formato: `/<marca ou campanha>/<página>/`, como `/black-friday/vitalicia/`, `/elite-mentoring/diagnostico/` e `/elite-experience/d/`.
- Minúsculas, palavras separadas por hífen, sem acento.
- Versões de teste de uma mesma página ficam por letra (`/elite-experience/b/`, `/c/`, `/d/`), e cada anúncio aponta para a sua.
- Páginas de obrigado ficam dentro da página principal (`/elite-mentoring/diagnostico/aprovado/`).
- Páginas de captura e vendas ficam fora do Google (noindex), a não ser que a gestão peça para indexar.

## 3. Imagens

- **Antes de entrar no design ou no código, toda imagem passa pelo Photoshop**, inclusive as criadas com IA: é redimensionada para o tamanho que a página precisa, tratada ou montada quando a seção pede (recorte, enquadramento, composição) e salva em WebP. Só depois vai para o Claude Design ou para o Claude Code.
- Essa imagem tratada é o original que entra em `src/assets/<projeto>/`, com nome que diz o que é (`hero-v2-mobile-dr-joao-pithon-paciente.webp`).
- O Astro gera a partir dela as versões leves (AVIF e WebP) em vários tamanhos; a página escolhe a certa para cada tela.
- A foto do topo carrega primeiro (prioridade alta); as demais carregam conforme a pessoa rola.
- Quando o celular e o computador usam fotos diferentes, cada aparelho baixa só a sua.
- Para a gestão: num ajuste pontual que troca uma imagem, mandar a imagem já tratada e em WebP, no mesmo tamanho da que está sendo substituída; se ela precisar de tratamento, o pedido vai para o André.

## 4. Checkout e repasse de parâmetros

- Os links de checkout da Hotmart ficam em `src/config/` ou no topo da página, nunca espalhados pelos botões: trocar o lote é mudar um lugar só.
- Um script da página copia os parâmetros da URL (UTMs e outros combinados por página) para o link do botão no clique, para a venda ou o cadastro ser atribuído à campanha certa.
- Nas páginas de vendas, o pixel da VK também participa da atribuição da venda na Hotmart.
- Quais parâmetros cada página repassa (incluindo sck e xcod) muda de página para página: o guia vai trazer a regra padrão e as exceções, conferidas no código.

## 5. Rastreamento

- Cada sala carrega o GTM, o pixel da VK (de captura ou de vendas, conforme a página) e o Clarity.
- Cada botão importante dispara um evento no dataLayer com o nome do projeto e a ação (ex.: `elite_diagnostico_aplicacao`, com `cta: topo`, `depoimentos`…), as UTMs e nunca dados pessoais.
- Página ou botão novo cria evento novo: ele só aparece nos relatórios depois que o gatilho correspondente for criado no GTM.
- A lista de eventos de cada página fica na seção dela no `CLAUDE.md`.

## 6. Checklist de testes antes de pedir aprovação

- [ ] Build sem erro
- [ ] Celular (360, 390 e 430 px) e computador (1440 e 1920 px): nada cortado, sem rolagem lateral
- [ ] Textos iguais aos da copy aprovada; números com fonte; sem travessão; "R$" junto do número
- [ ] Todos os botões com o destino certo (checkout, formulário, WhatsApp), na aba certa, com as UTMs repassadas
- [ ] Eventos disparando no dataLayer com o nome e o `cta` certos
- [ ] A página não "pula" ao carregar; imagens leves; foto do topo nítida
- [ ] noindex conferido (ou indexação, se pedida)
- [ ] Nenhuma outra página mudou (comparar o build com o anterior)
- [ ] Prévia aberta no celular de verdade, de preferência num iPhone
- [ ] Prints do celular e do computador anexados ao pedido de aprovação

## 7. Prévia

- Toda branch e todo pull request ganham um endereço de prévia no Cloudflare automaticamente.
- Onde ver: painel do Cloudflare, Workers e Pages, projeto lp-joaopithon, aba Implantações (lista de versões e prévias). Para isso a gestão precisa de acesso ao Cloudflare (item 9).
- No primeiro teste combinado (a correção no manual de desfazer), vamos confirmar se o link também aparece no próprio pull request, o que dispensaria o painel.

## 8. Design no Claude Design

- Os projetos ficam na conta webdesign@joaopithon.com.br, uma conta da empresa usada pelo André (não é pessoal).
- Cada página é um projeto no Claude Design. O primeiro pedido (o prompt de criação, montado a partir da copy e do moodboard) gera a primeira versão; as rodadas de ajuste acontecem no mesmo projeto, e cada projeto tem o seu artefato de design, que pode ser compartilhado por link.
- Para ver e comentar: o André compartilha o link do projeto.

**Por que não recomendamos a gestão editar os mesmos projetos:** depois que a página vai para o código, o design e a página no ar seguem caminhos que o André precisa manter em sincronia, e esse controle é feito no tato:

1. **Ajuste rápido:** vai direto no Claude Code, sem passar pelo Claude Design. A página no ar muda e o design fica para trás.
2. **Ajuste que pede direção visual:** antes de redesenhar, o André traz a página como está no ar de volta para o Claude Design, para ele entender o momento atual, com cuidado para não substituir nem perder as versões que já existem no projeto.
3. **Rodadas de redesenho:** vários pedidos e testes até chegar a um resultado adequado; raramente o primeiro pedido já resolve.
4. **Volta para o código:** só os ajustes aprovados seguem para o Claude Code, num pacote com o que mudou.

Com mais de uma pessoa mexendo nos mesmos projetos, fica fácil alguém redesenhar em cima de uma versão desatualizada, ou um ajuste feito só no código ser desfeito na próxima versão.

**O que funciona melhor:**

- **O Claude Design fica com o André.** Depois que um projeto está no Claude Design, os ajustes ali dependem de olhar e de tato, e de manter o design em sincronia com a página no ar. A gestão vê e comenta pelo link e manda os pedidos; quem ajusta é o André.
- **Página no ar, ajuste pontual na ausência do André:** o caminho é direto no código, pelo repositório, sem passar pelo Claude Design. Exemplos: trocar o link de um botão, um WhatsApp, uma data ou um texto curto. Na volta, o André vê pelo alarme o que mudou e, se for preciso, leva a mudança para o design.
- **Na call:** mostrar esse vai e vem num projeto real (o diagnóstico do Elite Mentoring).

## 9. Pesquisa e referências: até onde a IA vai sozinha

A IA da gestão consegue preparar quase toda a pesquisa e o prompt inicial; o que ela não substitui é a escolha das referências e o julgamento visual, que são o que separa uma página genérica de uma página no padrão da marca. Por isso a proposta é dividir o trabalho, e não tirar o André dessa etapa.

Hoje o André faz à mão: lê a copy, define o papel de cada seção, procura referências visuais, escolhe as que combinam com a marca, anota o que aproveitar de cada uma e transforma tudo no prompt que gera a primeira versão.

| Parte da pesquisa | A IA consegue? | Observação |
| --- | --- | --- |
| Dividir a copy em seções e dizer o papel de cada uma | Sim | Trabalho de leitura e estrutura, que ela faz bem |
| Listar os materiais disponíveis (fotos, depoimentos, números) | Sim, se tiver acesso às pastas | Inclui apontar o que falta ou está em baixa qualidade |
| Achar referências candidatas na web | Em parte | Encontra páginas e sites de referência, mas só "vê" o visual se receber prints ou tiver navegador com captura de tela |
| Escolher as referências certas para a marca | Não sozinha | Depende de gosto, do que é atual, do que combina com a marca e do que já converteu: é a parte humana |
| Anotar o que aproveitar de cada referência | Sim, com os prints escolhidos | Analisa bem uma imagem quando alguém já escolheu o que vale olhar |
| Escrever o prompt de criação para o Claude Design | Sim | Fica bom quando parte de um moodboard curado |

**Proposta de divisão:**

1. **A IA da gestão monta um dossiê da página:** copy dividida em seções, o papel de cada uma, materiais disponíveis e o que falta, 3 a 5 referências candidatas por seção (com link e print, quando der) e um rascunho do prompt.
2. **O André faz a curadoria:** tira, troca e acrescenta referências, anota o que aproveitar e ajusta o prompt. Essa parte fica bem mais curta, porque o trabalho braçal já vem feito.
3. **O prompt vai para o Claude Design** e o processo segue igual: primeira versão, rodadas de ajuste e aprovação do Luca.

**Por nível de entrega:** nas páginas Expressa e Essencial, que partem de um modelo nosso, a IA pode levar o trabalho do briefing até o prompt pronto, com o André só revisando. Nas páginas Bem trabalhada e Excelente, a curadoria do André continua necessária. Em todos os níveis, as rodadas de ajuste no Claude Design ficam com o André.

**Para a IA aprender o padrão com o tempo:** guardar uma biblioteca de referências aprovadas por tipo de seção (topo, prova, depoimentos, preço…), com os moodboards das páginas que já foram ao ar. Cada página nova parte dessa biblioteca, e ela fica mais rica a cada projeto.

## 10. Acessos que faltam

| Acesso | Para quê | Nível sugerido |
| --- | --- | --- |
| Cloudflare (conta Suporte@joaopithon.com.br) | Ver as prévias e, se combinado, voltar uma versão pelo manual de desfazer | Membro com acesso aos Workers; permissão de implantar só se a gestão for fazer o rollback |
| GTM (contêiner das páginas) | Criar e conferir os gatilhos dos eventos novos | Editar; publicar só se combinado com quem cuida do tráfego |
| Claude Design | Ver ou desenhar no mesmo fluxo | Links dos projetos do André, para ver e comentar; os ajustes no Claude Design ficam com o André |

## 11. Pauta da call (40 a 50 min)

1. Tour pelo repositório: estrutura, `src/config/` e a seção de um projeto no `CLAUDE.md` (10 min).
2. Um caso real do início ao fim: o diagnóstico do Elite Mentoring, do Claude Design à página no ar (10 min).
3. Pesquisa e referências: o que entra no dossiê da IA e como fica a curadoria do André (10 min).
4. Prévia e testes: abrir uma prévia e passar o checklist (5 min).
5. Acessos: Cloudflare, GTM e Claude Design (5 min).
6. Combinados: quem mexe em quê, quando avisar o André e o primeiro teste (5 min).
