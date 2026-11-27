---
name: fea-wordpress
description: Opera os 7 WordPress da FEA (joaopithon.com.br e subdomínios feb, iff, fef, pl, eb, fep) pela API REST. Testa credenciais, lê e altera configurações com segurança (foto do estado antes, verificação pública depois, limpeza de cache e plano de volta). Usar sempre que pedirem para testar, conferir ou mexer em WordPress, site, LP, título, Yoast, WP Rocket ou Elementor da FEA ou do Dr. João Pithon.
---

# FEA: operação dos WordPress via API REST

Skill do projeto FEA (Dr. João Pithon). Responder em português, sem em-dash, sempre "para" e nunca "pra".

## 1. Mapa dos sites

| Site | Nome no WordPress (nov/2026) | Usuário | Variável da senha |
|------|------------------------------|---------|-------------------|
| joaopithon.com.br | João Pithon | `WP_USER` (Pithon) | `WP_PASS_MAIN` (o script também aceita `WP_PASS_SITE`) |
| feb.joaopithon.com.br | Formação Especialista em Botox | `WP_USER` | `WP_PASS_FEB` |
| iff.joaopithon.com.br | IFF5 \| Dr. João Pithon | `WP_USER` | `WP_PASS_IFF` |
| fef.joaopithon.com.br | Formação Especialista em Fios | `WP_USER` | `WP_PASS_FEF` |
| pl.joaopithon.com.br | Joao Pithon | `WP_USER` | `WP_PASS_PL` |
| eb.joaopithon.com.br | Ebook - João Pithon | `WP_USER` | `WP_PASS_EB` |
| fep.joaopithon.com.br | João Pithon | **`WP_USER_FEP` (admin)** | `WP_PASS_FEP` |

Regras de credencial:
- As senhas são **senhas de aplicativo** do WordPress (geradas em Usuários > Perfil > Senhas de aplicativo). Elas só funcionam na API, não no login da tela `wp-login.php`.
- Senhas ficam só em variáveis de ambiente. Nunca gravar em arquivo, commit, log ou resposta. Nunca pedir que colem senha no chat: indicar o cadastro em variável de ambiente.
- Usuário por site: se existir `WP_USER_<SITE>` (exemplo `WP_USER_FEP`), ele substitui o `WP_USER`. Hoje só o fep usa usuário diferente.
- Se faltar variável, avisar qual falta e seguir com os outros sites.
- Quem gera senha nova e mexe na hospedagem: André Vivas (webdesigner).

## 2. Particularidades técnicas (aprendidas na prática)

- **WAF**: o servidor devolve 406 para User-Agent genérico. Sempre mandar UA de navegador:
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36`
- **Cloudflare** na frente, mas não guarda HTML (`cf-cache-status: DYNAMIC`). Quem guarda a página pronta é o **WP Rocket**.
- **WP Rocket não tem rota de limpar cache na API.** O caminho que funciona: `DELETE /wp-json/elementor/v1/cache`. Isso limpa o cache do Elementor e, por integração, o cache inteiro do WP Rocket. O CSS do Elementor é regerado no próximo acesso (conferir se responde 200).
- **Yoast SEO** monta o título da aba e do Google como "título da página - nome do site". Trocar o nome do site (Configurações > Geral) muda o título de toda página que não tem título de SEO próprio. Página com título próprio fica intacta.
- Plugins do iff (nov/2026): Elementor e Elementor Pro, PRO Elements, Happy Addons, Yoast SEO, WP Rocket, PrettyLinks, Header Footer Code Manager, All-in-One WP Migration.
- O iff tem páginas para os dois públicos, BR (português) e LATAM (espanhol). Título do site neutro: "IFF5 | Dr. João Pithon".

## 3. Teste de credenciais (somente leitura)

Rodar `scripts/fea_teste_wp.sh` (está nesta pasta da skill; no repositório FEA também existe em `FEA-scripts/fea_teste_wp.sh`). Ele faz só GET em `/wp-json/wp/v2/users/me` e devolve tabela:

| HTTP | Significado |
|------|-------------|
| 200 | logado, mostra nome e papel |
| 401 | usuário ou senha de aplicativo errados |
| 403 | bloqueado por WAF ou plugin de segurança |
| 406 | WAF recusou o User-Agent |

Resultado de referência (26/11/2026): os 7 sites deram 200 com papel administrator.

## 4. Protocolo para qualquer alteração (serviço em produção)

Alterar WordPress é mexer em site no ar. Só alterar com pedido explícito da Keila (ou do André repassado por ela). Seguir as etapas na ordem:

1. **Foto do estado atual.** Salvar em arquivo local o que vai mudar. Exemplo para configurações:
   `GET /wp-json/wp/v2/settings` (campos `title`, `description`, `url`, `language`).
   Listar as páginas afetadas: `GET /wp-json/wp/v2/pages?per_page=100&status=publish&context=edit&_fields=id,link,yoast_head_json.title` (paginar se houver mais de 100).
   Guardar o `<title>` público de cada página antes.
2. **Medir o impacto.** Contar quantas páginas mudam (por exemplo, quantas têm o nome do site no título do Yoast) e quantas têm título próprio e ficam iguais.
3. **Aplicar só o que foi pedido.** Exemplo de troca do título do site:
   `POST /wp-json/wp/v2/settings` com JSON `{"title":"IFF5 | Dr. João Pithon"}`.
   Não tocar em páginas, menus ou plugins sem pedido.
4. **Conferir na API.** Ler de novo `/wp-json/wp/v2/settings` e `/wp-json/` (campo `name`, público).
5. **Limpar cache.** `DELETE /wp-json/elementor/v1/cache`. Sem isso, as páginas continuam mostrando o valor antigo para o público.
6. **Conferir no público, página por página.** Baixar o `<title>` de todas as URLs (dá para rodar 10 em paralelo) e contar: quantas com valor antigo (meta: 0), quantas com valor novo, quais com título próprio. Conferir também se os CSS do Elementor (`/wp-content/uploads/elementor/css/post-*.css`) respondem 200, para garantir que o layout não quebrou.
7. **Relatar** valor antigo, valor novo, número de páginas afetadas e intactas, o que foi feito com o cache e o plano de volta.

**Plano de volta:** reenviar o valor salvo na etapa 1 com o mesmo `POST` e repetir as etapas 5 e 6.

Nunca: desativar plugin, mudar tema, apagar conteúdo, mexer em usuário ou senha, ou mudar URL do site sem confirmação explícita. Essas ações podem derrubar a página de vendas.

## 5. Histórico de alterações

| Data | Site | O que mudou | Antes | Depois | Pedido por |
|------|------|-------------|-------|--------|-----------|
| 26/11/2026 | iff | Título do site | Inmersión Avanzada en Full Face con menos de 5 ml | IFF5 \| Dr. João Pithon | André Vivas, via Keila |

Detalhe da alteração de 26/11/2026: 85 páginas publicadas. 83 passaram a terminar em "IFF5 | Dr. João Pithon". 2 têm título de SEO próprio e ficaram iguais ("Masterclass em Intercorrências · 17 de novembro, 20h", em `/mti/` e na cópia dela). Depois da limpeza de cache, 0 páginas com o título antigo.

Acrescentar uma linha nesta tabela a cada nova alteração.

## 6. Pendências conhecidas

- Cadastrar `WP_USER_FEP` e `WP_PASS_FEP` no ambiente de cada Claude que for usar esta skill.
