# FEA · Inventário das páginas WordPress/Elementor fora do repositório lp-joaopithon (25/11/2026)

Levantamento só de leitura. Nada foi alterado em WordPress, repositório, ClickUp ou planilhas.

**Critério de sucesso:** todos os subdomínios web de joaopithon.com.br identificados, todas as páginas publicadas listadas, cada uma comparada com `src/pages` e `public` do repositório, e as ativas que só existem no WordPress com o que a transferência exige.

## 1. Método

- Subdomínios: certificados públicos (crt.sh) + links nas notas FEA e no repositório. Web encontrados: joaopithon.com.br (raiz), bf, bio, ctx, eb, el, fea, feb, fef, fep, iff, pg, pl e lp. Os demais (api, dify, n8n, evolution, minio, s3, pixel, webhook, painel, reology, cpanel, mail etc.) são sistemas, não páginas. Não existem subdomínios plx, latam ou elite próprios (elite. responde pelo coringa, sem WordPress).
- WordPress confirmado pelo meta generator em todos os 13 subdomínios (WordPress 7.1.5 + Elementor 3.30 a 4.2). O lp. é o Astro do repositório.
- Lista de páginas: API REST de cada WordPress (`/wp-json/wp/v2/pages`), que traz todas as páginas publicadas, inclusive as com noindex que o sitemap omite. Sitemaps conferidos (`sitemap_index.xml` Yoast em 11 deles; `wp-sitemap.xml` em ctx e eb). Os únicos tipos de conteúdo públicos são páginas e posts (sem landing pages do tipo e-landing-page).
- Cada página foi aberta (curl, só HTML, sem baixar imagens) para status, redirecionamento, formulário, checkout, pixels, vídeo e imagens. Uma imagem de cada página ativa foi testada com HEAD (todas 200, servidas pelo Cloudflare, sem bloqueio por Referer).
- Repositório: `src/pages`, `public`, `public/_redirects`, `docs/GUIA-NOVA-PAGINA.md` e `CLAUDE.md` (branch main; só existe a main no remoto).

**Status usado:** *Ativa* = produto vigente e página em uso ou citada nos Links úteis · *Ativa (já tem versão no código)* = existe equivalente em lp. · *Migrada* = o WordPress já redireciona para lp. · *Recente* = evento de 2026 já encerrado, serve de base para a próxima edição · *Antiga* = 2024/2025, variações de teste A/B encerradas, clones, rascunhos e "Sample Page".

## 2. Total por subdomínio

| Subdomínio | Páginas | Ativas só no WP | Ativas já no código / migradas | Recentes | Antigas |
|---|---|---|---|---|---|
| joaopithon.com.br | 94 | 11 | 0 | 1 | 82 |
| bf.joaopithon.com.br | 46 | 5 | 5 | 0 | 36 |
| bio.joaopithon.com.br | 14 | 13 | 0 | 0 | 1 |
| ctx.joaopithon.com.br | 5 | 4 | 0 | 0 | 1 |
| eb.joaopithon.com.br | 16 | 15 | 0 | 0 | 1 |
| el.joaopithon.com.br | 5 | 0 | 2 | 1 | 2 |
| fea.joaopithon.com.br | 6 | 0 | 0 | 5 | 1 |
| feb.joaopithon.com.br | 22 | 11 | 1 | 0 | 10 |
| fef.joaopithon.com.br | 7 | 0 | 0 | 0 | 7 |
| fep.joaopithon.com.br | 45 | 10 | 0 | 20 | 15 |
| iff.joaopithon.com.br | 85 | 4 | 1 | 58 | 22 |
| pg.joaopithon.com.br | 5 | 0 | 0 | 1 | 4 |
| pl.joaopithon.com.br | 8 | 2 | 1 | 3 | 2 |
| **Total** | **358** | **75** | **10** | **89** | **184** |

lp.joaopithon.com.br (repositório): 26 páginas em `src/pages` + 1 export em `public/iff/latam-c` (Black Brasil e Latam, Elite, Elite Experience, Elite Mentoring, FEB Masterclass Toxina, MPL, IFF).

## 3. O que já está no código (não precisa transferir)

| Página WordPress | Equivalente no repositório |
|---|---|
| bf./off-black-vitalicia-abertura/ · ativa | lp/black-friday/live/ e vitalicio-i/ |
| bf./black-vitalicia/ · ativa | lp/black-friday/vitalicia/ e vitalicio-i/ |
| bf./black-vitalicia-cupom/ · ativa | lp/black-friday/cupom-a/ |
| bf./black-vitalicia-d/ · ativa | lp/black-friday/combo/ e combo-parcelado/ |
| bf./lista-de-espera/ · migrada | redireciona para bf./black-vitalicia/ |
| el./elite-injectors-congress-a/ · recente | lp/elite/pre-venda/ (edição 2027) |
| el./elite-injectors-congress/ · recente | lp/elite/pre-venda/ e lista-de-espera/ (edição 2027) |
| feb./mtb/ · migrada | lp/feb/masterclass-toxina/ (redireciona) |
| iff./ · recente | lp/iff/latam-c/ (export do canvas) e lp/iff/ |
| pl./mpl/ · migrada | lp/preenchimento-labial/masterclass/ (redireciona) |
| (sem página WP) Elite Mentoring, Elite Mentoring Diagnóstico, Elite Experience | lp/elite-mentoring/*, lp/elite-experience/* |
| (sem página WP) Black Friday Latam | lp/black-friday-latam/* |

O repositório ainda aponta para 3 páginas WordPress como destino: `bf./black-vitalicia-obrigado/`, `feb./pesquisa/` e `pl./pesquisa-mpl/` (obrigado/pesquisa depois do formulário). Se forem transferidas, esses destinos mudam junto.

## 4. Páginas ATIVAS que só existem no WordPress

Pontos comuns a todas: o GTM é o mesmo do repositório (`GTM-PFCMG8V3`), então Meta, Google e demais tags vêm dele; o pixel da VK aparece nas capturas e vendas marcadas; formulários Elementor Pro usam telefone com intl-tel-input e as ações (webhook, lista do ActiveCampaign, redirecionamento) ficam no servidor, não no HTML, então precisam ser copiadas do editor do Elementor antes de migrar; nenhuma página ativa tem noindex; todas as imagens testadas são públicas.

### Masterclass em Bioestimulador / FBio · Brasil (6)

- **bio./fbio/** · Formação Especialista em Bioestimuladores · vendas · alterada 17/06/2026  
  Formulário: não · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3 · Imagens: 108 (públicas, 200)
- **bio./live-zoom/** · Live Zoom · zoom · alterada 11/06/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Zoom: https://us06web.zoom.us/j/81204025790 · Imagens: 4 (públicas, 200)
- **bio./masterclass-bio/** · Masterclass em Bioestimuladores de Colágeno · captura · alterada 10/06/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Após o envio vai para: bio./masterclass-bio-obrigado/? · Imagens: 7 (públicas, 200)
- **bio./masterclass-bio-a/** · Masterclass em Bioestimuladores de Colágeno · a · captura · alterada 10/06/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Após o envio vai para: bio./masterclass-bio-obrigado/? · Imagens: 7 (públicas, 200)
- **bio./masterclass-bio-obrigado/** · Obrigado · Masterclass em Bioestimuladores de Colágeno · obrigado · alterada 09/06/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)
- **bio./onboarding/** · Onboarding · Formação Especialista em Bioestimuladores · onboarding · alterada 13/06/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)

### Masterclass em Bioestimulador / FBio · Latam (7)

- **bio./fbio-latam/** · Formação Especialista em Bioestimuladores · LATAM · vendas · alterada 17/08/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/I106759959E?off=n2gnxcep · Rastreio: GTM-PFCMG8V3 · Imagens: 108 (públicas, 200)
- **bio./live-zoom-latam/** · Live Zoom · LATAM · zoom · alterada 04/08/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)
- **bio./masterclass-bio-latam/** · Masterclass em Bioestimuladores de Colágeno · LATAM · captura · alterada 17/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, VK · Após o envio vai para: bio./masterclass-bio-obrigado-latam/? · Imagens: 7 (públicas, 200)
- **bio./masterclass-bio-latam-a/** · Masterclass em Bioestimuladores de Colágeno · LATAM · A · captura · alterada 10/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, VK · Após o envio vai para: bio./masterclass-bio-obrigado-latam/? · Imagens: 5 (públicas, 200)
- **bio./masterclass-bio-latam-b/** · Masterclass em Bioestimuladores de Colágeno · LATAM · B · captura · alterada 10/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, VK · Após o envio vai para: bio./masterclass-bio-obrigado-latam/? · Imagens: 5 (públicas, 200)
- **bio./masterclass-bio-obrigado-latam/** · Obrigado · Masterclass em Bioestimuladores de Colágeno · LATAM · obrigado · alterada 14/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)
- **bio./onboarding-latam/** · Onboarding · Formação Especialista em Bioestimuladores · LATAM · onboarding · alterada 10/08/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)

### Ebook Intercorrências (2)

- **eb./intercorrencias/** · Intercorrências no Preenchimento Facial · Ebook · vendas · alterada 19/12/2025  
  Formulário: não · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)
- **eb./intercorrencias-l/** · Intercorrências no Preenchimento Facial · l · vendas · alterada 19/12/2025  
  Formulário: não · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3 · Imagens: 44 (públicas, 200)

### Ebook Olheiras (PTO) (11)

- **eb./ebook-pto/** · Preenchimento Tridimensional de Olheiras · Ebook · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)
- **eb./ebook-pto-a/** · Preenchimento Tridimensional de Olheiras · A · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-b/** · Preenchimento Tridimensional de Olheiras · b · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-c/** · Preenchimento Tridimensional de Olheiras · C · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-d/** · Preenchimento Tridimensional de Olheiras · D · vendas · alterada 21/05/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-e/** · Preenchimento Tridimensional de Olheiras · E · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-f/** · Preenchimento Tridimensional de Olheiras · F · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-g/** · Preenchimento Tridimensional de Olheiras · G · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 52 (públicas, 200)
- **eb./ebook-pto-h/** · Preenchimento Tridimensional de Olheiras · H · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3, VK · Imagens: 54 (públicas, 200)
- **eb./ebook-pto-l/** · Preenchimento Tridimensional de Olheiras · l · vendas · alterada 23/06/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/S97800165C?off=1lg7jeno · Rastreio: GTM-PFCMG8V3 · Imagens: 44 (públicas, 200)
- **eb./ebook-pto-obrigado/** · Preenchimento Tridimensional de Olheiras · Obrigado · obrigado · alterada 01/09/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)

### Upsell de ebook (CPX/CAC) (2)

- **eb./upsell-cac/** · Upssell · CAC · vendas (upsell) · alterada 13/01/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/D95593160T · Rastreio: GTM-PFCMG8V3 · Vídeo: YouTube · Imagens: 2 (públicas, 200)
- **eb./upsell-cpx/** · Upsell · CPX · vendas (upsell) · alterada 15/01/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/O89651368W?off=ugzaamhx · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)

### CTX · Brasil (2)

- **ctx./curso-de-toxina-express/** · Curso de Toxina Express · vendas · alterada 14/09/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/X105748129H?off=zzgv77dj · Rastreio: GTM-PFCMG8V3, VK · Imagens: 57 (públicas, 200)
- **ctx./obrigado-ctx/** · Obrigado · ctx · obrigado · alterada 01/09/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)

### CTX · Latam (2)

- **ctx./curso-de-toxina-express-latam/** · Curso de Toxina Express · LATAM · vendas · alterada 14/09/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/E107212688I?off=bfsu34ha · Rastreio: GTM-PFCMG8V3 · Imagens: 58 (públicas, 200)
- **ctx./obrigado-ctx-latam/** · Obrigado · ctx · latam · obrigado · alterada 21/09/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 4 (públicas, 200)

### FEB / MTB · Brasil (6)

- **feb./feb/** · Formação Especialista em Botox · vendas · alterada 11/08/2026  
  Formulário: Elementor Form · Checkout: https://pay.hotmart.com/H62237207S · Rastreio: GTM-PFCMG8V3, VK · Imagens: 27 (públicas, 200)
- **feb./live-zoom/** · Live zoom · zoom · alterada 31/07/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 7 (públicas, 200)
- **feb./mtb-b/** · Masterclass em Toxina Botulínica · b · captura · alterada 01/11/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, VK · Imagens: 8 (públicas, 200)
- **feb./onboarding/** · Onboarding · onboarding · alterada 08/01/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 8 (públicas, 200)
- **feb./pesquisa/** · Pesquisa · MTB · check-in/pesquisa · alterada 03/11/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 10 (públicas, 200)
- **feb./vk/** · Formação Especialista em Botox · vk · vendas · alterada 11/08/2026  
  Formulário: Elementor Form · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, VK · Imagens: 24 (públicas, 200)

### FEB / MTB · Latam (5)

- **feb./feb-latam/** · Formação Especialista em Botox · LATAM · vendas · alterada 10/07/2026  
  Formulário: Elementor Form · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3 · Vídeo: YouTube · Imagens: 27 (públicas, 200)
- **feb./feb-latam-a/** · Formação Especialista em Botox · LATAM · a · vendas · alterada 07/07/2026  
  Formulário: Elementor Form · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3 · Imagens: 27 (públicas, 200)
- **feb./mtb-latam/** · Masterclass em Toxina Botulínica · latam · captura · alterada 14/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, VK · Imagens: 8 (públicas, 200)
- **feb./onboarding-latam/** · Onboarding · LATAM · onboarding · alterada 03/07/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 7 (públicas, 200)
- **feb./pesquisa-latam/** · Pesquisa · LATAM · check-in/pesquisa · alterada 13/08/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 10 (públicas, 200)

### Masterclass em Preenchimento Labial (MPL) (2)

- **pl./live-zoom-mpl/** · Live zoom · mpl · zoom · alterada 13/11/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 2 (públicas, 200)
- **pl./pesquisa-mpl/** · Masterclass em Preenchimento Labial · Pesquisa · check-in/pesquisa · alterada 11/11/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: nenhuma do WP

### Black Vitalícia (5)

- **bf./black-vitalicia-obrigado/** · black-vitalicia-obrigado · obrigado · alterada 19/10/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Vídeo: YouTube · Imagens: 44 (públicas, 200)
- **bf./black-vitalicia-obrigado-alunos/** · black-vitalicia-obrigado · cupom · obrigado · alterada 19/10/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 44 (públicas, 200)
- **bf./lista-de-espera-bf/** · Black Vitalícia · Lista de Espera · captura (lista de espera) · alterada 08/10/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 5 (públicas, 200)
- **bf./onboarding-bfv/** · Onboarding Black Friday Vitalício · onboarding · alterada 19/10/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3 · Imagens: 6 (públicas, 200)
- **bf./verificacao-numeros/** · Verificação números · outro (verificação de número) · alterada 01/10/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3 · Imagens: 7 (públicas, 200)

### FEP · Brasil (6)

- **fep./carta-fep/** · Carta · fep · vendas (carta) · alterada 16/09/2026  
  Formulário: não · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 62 (públicas, 200)
- **fep./fep/** · Formação Especialista em Preenchimento · vendas · alterada 06/11/2026  
  Formulário: Elementor Form · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, Clarity · Vídeo: YouTube · Imagens: 151 (públicas, 200)
- **fep./lista-de-espera/** · Formação Especialista em Preenchimento · Lista de espera · captura (lista de espera) · alterada 03/09/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 71 (públicas, 200)
- **joaopithon.com.br/lista-de-espera-fep/** · Lista de espera · FEP · captura (lista de espera) · alterada 07/04/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, Clarity · Vídeo: YouTube · Imagens: 149 (públicas, 200)
- **fep./onboarding-fep/** · Onboarding · fep · onboarding · alterada 06/04/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 7 (públicas, 200)
- **fep./redirect-2/** · Redirect · 2 · outro (redirecionamento) · alterada 18/02/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Após o envio vai para: api.whatsapp.com/send?phone=551151040781&text=Ol%C3%A1!%20Gostaria%20de%20mais%20informa%C · Imagens: 5 (públicas, 200)

### FEP · Latam (4)

- **fep./carta-fep-latam/** · Carta FEP / LATAM · vendas (carta) · alterada 14/10/2026  
  Formulário: não · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 86 (públicas, 200)
- **fep./fep-latam/** · Formação Especialista em Preenchimento / LATAM · vendas · alterada 14/10/2026  
  Formulário: Elementor Form · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 149 (públicas, 200)
- **fep./lista-de-espera-latam/** · Formação Especialista em Preenchimento · Lista de espera / LATAM · captura (lista de espera) · alterada 13/10/2026  
  Formulário: Elementor Form · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 154 (públicas, 200)
- **fep./onboarding-fep-latam/** · Onboarding · FEP / LATAM · onboarding · alterada 13/10/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 7 (públicas, 200)

### FEP Experience (5)

- **joaopithon.com.br/fep-exp-obrigado/** · FEP EXP · Obrigado · obrigado · alterada 18/09/2026  
  Formulário: não · Checkout: https://pay.hotmart.com/P93831788Q?off=5qywtk6m · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 6 (públicas, 200)
- **joaopithon.com.br/fep-experience/** · FEP EXPERIENCE · vendas · alterada 28/08/2026  
  Formulário: Respondi · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, VK, Clarity · Vídeo: YouTube · Imagens: 90 (públicas, 200)
- **joaopithon.com.br/fep-experience-a/** · FEP EXPERIENCE · A · vendas · alterada 28/08/2026  
  Formulário: Respondi · Checkout: não aparece no HTML (botão interno, popup ou âncora; pegar no editor) · Rastreio: GTM-PFCMG8V3, VK, Clarity · Vídeo: YouTube · Imagens: 90 (públicas, 200)
- **fep./onboarding-fep-exp/** · Onboarding · Fep Exp · onboarding · alterada 19/06/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 16 (públicas, 200)
- **joaopithon.com.br/onboarding-fep-exp/** · Onboarding · FEP EXP · onboarding · alterada 13/03/2026  
  Formulário: webhook/automação · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 7 (públicas, 200)

### Masterclass em Intercorrências (MTI) (4)

- **iff./mti/** · Masterclass em Intercorrências · captura · alterada 12/11/2026  
  Formulário: Elementor Form, ActiveCampaign · Rastreio: GTM-PFCMG8V3, VK, Clarity · Após o envio vai para: iff./mti-checkin/? · Imagens: 8 (públicas, 200)
- **iff./mti-a/** · Masterclass em Intercorrências · A · captura · alterada 09/09/2026  
  Formulário: Elementor Form, ActiveCampaign · Rastreio: GTM-PFCMG8V3, VK, Clarity · Após o envio vai para: iff./mti-checkin/? · Imagens: 7 (públicas, 200)
- **iff./mti-checkin/** · MTI · obrigado · check-in/pesquisa · alterada 12/11/2026  
  Formulário: Elementor Form, ActiveCampaign · Rastreio: GTM-PFCMG8V3, VK, Clarity · Imagens: 5 (públicas, 200)
- **iff./mti-zoom/** · Masterclass Intercorrências · Zoom · zoom · alterada 10/09/2026  
  Formulário: ActiveCampaign · Rastreio: GTM-PFCMG8V3, VK, Clarity · Imagens: 6 (públicas, 200)

### Institucional / outros (6)

- **joaopithon.com.br/** · Acessos úteis · outro (hub de links) · alterada 16/10/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 37 (públicas, 200)
- **joaopithon.com.br/elementor-28131/** · Redirect · outro (redirecionamento) · alterada 02/06/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Zoom: https://us06web.zoom.us/j/82657687599 · Após o envio vai para: us06web.zoom.us/j/82657687599 · Imagens: 4 (públicas, 200)
- **joaopithon.com.br/links-joao-pithon/** · Links · João Pithon · outro (hub de links) · alterada 05/08/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 7 (públicas, 200)
- **joaopithon.com.br/politica-de-privacidade/** · Política de Privacidade · institucional · alterada 12/01/2024  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 11 (públicas, 200)
- **joaopithon.com.br/redirecionar-whatsapp/** · redirecionar-whatsapp · outro (redirecionamento) · alterada 10/06/2026  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Após o envio vai para: wa.me/551151960668?text=Ol%C3%A1%20gostaria%20de%20ser%20paciente%20modelo · Imagens: 4 (públicas, 200)
- **joaopithon.com.br/termos-de-uso/** · Termos de uso · institucional · alterada 12/01/2024  
  Formulário: não · Rastreio: GTM-PFCMG8V3, Clarity · Imagens: 11 (públicas, 200)

### Produtos vigentes sem nenhuma página no WordPress

- **PLX Brasil e PLX Latam:** nenhuma página publicada em nenhum subdomínio e as abas WEB DESIGNER dos Links úteis estão vazias. Checkout Brasil já existe (pay.hotmart.com/P107410854L?off=whzgr6uz). As páginas serão criadas do zero, direto no código (o André disse que faz depois da Masterclass).
- **Combo 2 em 1: FEB + FEBio Vitalício e Masterclass em Bioestimulador 12/26:** os Links úteis apontam para lp/febio/masterclass/, /obrigado/, /combo/, /combo/obrigado/ e /onboarding/, todas **404 hoje** e ausentes do repositório (nenhuma branch remota além da main). A única página do evento em uso no WordPress é bio./live-zoom/ (ainda com o Zoom de junho, 81204025790). As páginas de junho em bio. servem de fonte de copy, imagens e formulário.
- **Ebook Intercorrências Latam:** sem página no WordPress.
- **Elite Mentoring e Elite Experience:** já estão só no código.

### Achados que merecem atenção

1. **eb./intercorrencias/ e /intercorrencias-l/:** os botões de compra têm `href="#"` e não há link de checkout no HTML; o botão de WhatsApp aponta para `http://Quero%20falar%20com%20a%20equipe!` (link quebrado). Na transferência, pedir o checkout ao Luca e corrigir o WhatsApp.
2. **bio./fbio/ (vendas FBio Brasil):** os 5 botões levam a `#top` e não há checkout no HTML. A versão Latam tem checkout direto (pay.hotmart.com/I106759959E?off=n2gnxcep).
3. **fep./fep/, fep./carta-fep/ e as Latam:** checkout dentro de popup do Elementor ou formulário, sem link visível; o botão principal da fep./fep/ leva a bf./verificacao-numeros/ (fluxo de verificação de aluno da Black).
4. **feb./mtb/ e pl./mpl/** já redirecionam para lp.; as variações mtb-a, mtb-letybo, mpl-a/b/c continuam publicadas no WordPress e podem receber tráfego antigo.
5. **iff. (raiz)** é a vendas do IFF5 Latam; já existe a versão C em `public/iff/latam-c/`, mas a raiz do WordPress segue no ar com ActiveCampaign próprio.

## 5. O que a transferência exige, por página ativa

| Tipo | O que levar | Componente pronto no repositório |
|---|---|---|
| Captura (Elementor Form) | Campos, ação de envio (webhook ou lista AC, copiar do editor), redirecionamento para obrigado com parâmetros, VK de captura | `FormularioAC.astro` (AC), `VK.astro tipo=captura`, sala com GTM e Clarity |
| Captura (ActiveCampaign embed, MTI) | formId do Active | `FormularioAC.astro` |
| Vendas | Links Hotmart com `off`, repasse de UTMs e `xcod`, VK de vendas, vídeos YouTube | seção 7 do guia (checkout e repasse), `VK.astro tipo=vendas` |
| Obrigado/pesquisa | Formulário de pesquisa e para onde as respostas vão (Clint, planilha, webhook) | precisa de webhook da automação |
| Onboarding e Zoom | Links de grupo, área de membros, sala do Zoom | só conteúdo |
| FEP Experience | Formulário Respondi (embed) | mesmo padrão da Elite Experience (`elite-experience.ts`) |

## 6. Ordem sugerida de transferência

1. **Masterclass em Bioestimulador 12/26 + Combo 2 em 1: FEB + FEBio Vitalício** (captação começa 30/11): finalizar lp/febio/masterclass, obrigado, combo, combo/obrigado e onboarding usando bio./masterclass-bio, bio./masterclass-bio-obrigado, bio./fbio e bio./onboarding como fonte; criar a página do Zoom no código ou atualizar bio./live-zoom/ com a sala de 08/12. Versão Latam em seguida, a partir de bio./masterclass-bio-latam, fbio-latam, onboarding-latam e live-zoom-latam.
2. **PLX Brasil e PLX Latam:** vendas e obrigado/pesquisa (Brasil) e vendas, onboarding e check-in (Latam), novas no código; nada a migrar.
3. **Ebooks:** eb./intercorrencias (corrigir checkout e WhatsApp), eb./ebook-pto (página principal e só as variações em uso no tráfego) e eb./ebook-pto-obrigado; depois upsell-cpx e upsell-cac.
4. **Elite Mentoring:** nada a transferir (vendas e diagnóstico já estão no código, nada dele existe no WordPress). Falta criar a página de obrigado/agendamento e o formulário com webhook; a de onboarding consta nos Links úteis, mas a regra da Adri de 24/11 diz que perpétuo não tem onboarding, então confirmar antes.
5. Depois, por calendário: FEB/MTB (feb./feb, pesquisa, live-zoom, onboarding e Latam; a captura já está no código), CTX Brasil e Latam, MTI, Black Vitalícia (obrigado, onboarding, lista de espera e verificação), FEP e FEP Experience, Masterclass em Anatomia para dezembro (fea.), institucionais (raiz, links, política e termos).

## 7. Rastreamento de funil

1. **Limitação atual:** as ações dos formulários Elementor ficam no servidor e não aparecem no HTML; sem exportar do editor não há como conferir de fora para onde cada lead vai, e nenhuma linha "Link de webhook" dos Links úteis está preenchida.
2. **Leitura via plataforma:** os ebooks (Intercorrências e Olheiras) podem ganhar tracking de leitura via Heyzine, FlippingBook ou Issuu no lugar do PDF solto.
3. **UTM único por QR code:** ao migrar, padronizar o repasse de UTMs e `xcod` para o checkout (o componente do repositório já faz isso), inclusive nos QR codes dos ebooks.
4. **Frente no plano de ação:** rastreamento de funil fim a fim (anúncio, página, formulário, Clint/Active, checkout) como etapa obrigatória de cada página transferida.

Sem métrica, otimização é palpite.

## Apêndice A · Páginas recentes (eventos de 2026 encerrados)

- **Black da FEP 12/25** (1): fep./abertura-black/
- **Elite Injectors Congress 2026** (3): el./checkin/, el./elite-injectors-congress/, el./elite-injectors-congress-a/
- **FEP / PSP (versão antiga)** (1): joaopithon.com.br/psp-a/
- **FEP · Brasil** (1): fep./carta-fep-21-07-2026/
- **IFF10** (32): iff./checkout-iff10/, iff./checkout-iff10-67/, iff./iff10/, iff./iff10-a/, iff./iff10-aa/, iff./iff10-ab/, iff./iff10-ac/, iff./iff10-ad/, iff./iff10-ae/, iff./iff10-af/, iff./iff10-ag/, iff./iff10-ah/, iff./iff10-ai/, iff./iff10-aj/, iff./iff10-ak/, iff./iff10-al/, iff./iff10-am/, iff./iff10-an/, iff./iff10-ao/, iff./iff10-ap/, iff./iff10-b/, iff./iff10-r/, iff./iff10-s/, iff./iff10-t/, iff./iff10-u/, iff./iff10-v/, iff./iff10-w/, iff./iff10-x/, iff./iff10-y/, iff./iff10-z/, iff./iff10-zoom/, iff./iff10ml-obrigado/
- **IFF5 · Brasil** (22): iff./checkout-iff5/, iff./iff/, iff./iff-a/, iff./iff-b/, iff./iff-c/, iff./iff-d/, iff./iff-e/, iff./iff-f/, iff./iff-g/, iff./iff-h/, iff./iff-i/, iff./iff-j/, iff./iff-k/, iff./iff-l/, iff./iff-m/, iff./iff-n/, iff./iff-o/, iff./iff-p/, iff./iff-q/, iff./iff-r/, iff./iff-s/, iff./iff5ml-obrigado/
- **IFF5 · Latam** (5): iff./, iff./iff5-b/, iff./iff5-latam-a/, iff./iff5-latam-obrigado/, iff./iff5-latam-zoom/
- **Masterclass em Anatomia / FEA** (5): fea./fea/, fea./mea/, fea./mea-a/, fea./mea-obrigado/, fea./onboarding/
- **Masterclass em Preenchimento Labial (MPL)** (3): pl./mpl-a/, pl./mpl-b/, pl./mpl-c/
- **PSP (captação FEP)** (18): fep./off-psp-obrigado-2/, fep./psp/, fep./psp-a/, fep./psp-aa/, fep./psp-ab/, fep./psp-ac/, fep./psp-ad/, fep./psp-ae/, fep./psp-af/, fep./psp-ag/, fep./psp-ah/, fep./psp-ai/, fep./psp-obrigado/, fep./psp-v/, fep./psp-w/, fep./psp-x/, fep./psp-y/, fep./psp-z/
- **Pós-Graduação** (1): pg./upsell-fep/

## Apêndice B · Páginas antigas

- **joaopithon.com.br** (82): /atsd, /cac, /cpx, /cpx-a, /cpx-b, /cpx-c, /cpx-d, /cpx-e, /fec, /fep-experience-inscricoes-encerradas, /imersao-avancada-em-rinomodelacao, /imersao-avancada-em-rinomodelacao-b, /imersao-avancada-em-rinomodelacao-c, /ipl, /ipo, /ipo-a, /ipo-b, /ipo-c, /lista-de-espera-fec, /lista-espera-fep, /master-class-em-fios, /masterclass-em-fios-de-pdo, /masterclass-em-toxina-botulinica-cloned-16530, /masterclass-em-toxina-butolinica-a, /mep, /mep-a, /obrigado-cpx, /off-carta-fep, /off-carta-fep-25-06-25, /off-dowload-3-psp, /off-fep, /off-material-didatico-aula-1-psp, /off-material-didatico-aula-2-psp, /off-material-didatico-aula-3-psp, /off-material-didatico-aula-4-psp, /off-onboarding-fep, /off-psp, /onboarding-cac, /onboarding-fec, /onboarding-imersao-avancada-em-rinomodelacao, /onboarding-ipl, /onboarding-ipo, /psp-aa, /psp-b, /psp-bb, /psp-c, /psp-cc, /psp-d, /psp-dd, /psp-e, /psp-f, /psp-g, /psp-h, /psp-i, /psp-j, /psp-obrigado, /teste-form-active, /teste-vitalicio, /upsell-cpx, /upsell-fec, /upsell-fep-exp, /verificacao-de-numero, /verificacao-de-numero-falso, /verificacao-de-numero-seguro, /verificacao-ipo, /vitalicio, /workshop-em-preenchimento, /workshop-em-preenchimento-a, /workshop-em-preenchimento-b, /workshop-em-preenchimento-c, /workshop-em-preenchimento-d, /workshop-em-preenchimento-e, /workshop-em-preenchimento-f, /workshop-em-preenchimento-g, /workshop-em-preenchimento-h, /workshop-em-preenchimento-i, /workshop-em-preenchimento-j, /workshop-em-preenchimento-k, /workshop-em-preenchimento-l, /workshop-em-preenchimento-m, /workshop-em-preenchimento-n, /workshop-em-preenchimento-o
- **bf.** (36): /black-da-fep, /black-da-fep-a, /black-da-fep-b, /black-da-fep-c, /black-da-fep-d, /black-da-fep-e, /black-da-fep-f, /black-da-fep-g, /black-da-fep-h, /black-vitalicia-abertura-cloned, /black-vitalicia-c, /black-vitalicia-e, /black-vitalicia-f, /black-vitalicia-verificacao, /captura-aluno, /download-3-psp, /lista-de-espera-obrigado, /material-didatico-aula-3-psp, /mem, /mem-a, /mem-b, /mer, /mer-a, /mer-b, /mer-c, /off-black-vitalicia, /off-verificacao-aluno, /off-vitalicio-abertura, /onboarding-black-friday-vitalicio-cloned-283, /privacy-policy, /redirect, /sample-page, /teste, /teste-captura-bf, /teste-form, /verificacao-aluno-2
- **bio.** (1): /sample-page
- **ctx.** (1): /sample-page
- **eb.** (1): /sample-page
- **el.** (2): /esboco, /sample-page
- **fea.** (1): /sample-page
- **feb.** (10): /mtb-a, /mtb-letybo, /mtb-letybo-a, /mtb-letybo-b, /mtb-letybo-c, /redirect, /sample-page, /teste-formulario, /teste-formulario-2, /teste-formulario-3
- **fef.** (7): /fef, /master-class-em-fios-a, /master-class-em-fios-teste, /masterclass-em-fios, /onboarding-fef, /sample-page, /teste-form-active
- **fep.** (15): /formacao-especialista-em-preenchimento-cloned-363, /off-psp-obrigado, /psp-k, /psp-l, /psp-m, /psp-n, /psp-o, /psp-p, /psp-q, /psp-r, /psp-s, /psp-t, /psp-u, /redirect, /sample-page
- **iff.** (22): /area-de-membros-iff, /iff10-c, /iff10-d, /iff10-e, /iff10-f, /iff10-g, /iff10-h, /iff10-i, /iff10-j, /iff10-k, /iff10-l, /iff10-m, /iff10-n, /iff10-o, /iff10-p, /iff10-q, /iff5-teste, /login, /masterclass-em-intercorrencias-cloned-4677, /sample-page, /t, /teste
- **pg.** (4): /, /carta, /onboarding-pos-graduacao, /sample-page
- **pl.** (2): /sample-page, /teste

## Apêndice C · Lista completa

| URL | Título | Produto | Tipo | Status | Alterada |
|---|---|---|---|---|---|
| joaopithon.com.br/atsd/ | ATSD | Institucional / outros | vendas | Antiga | 2024-04-04 |
| joaopithon.com.br/cac/ | Curso Avançado de Complicações | CAC | vendas | Antiga | 2026-01-13 |
| joaopithon.com.br/cpx/ | CPX | CPX | captura | Antiga | 2025-09-01 |
| joaopithon.com.br/cpx-a/ | CPX · a | CPX | captura | Antiga | 2024-12-11 |
| joaopithon.com.br/cpx-b/ | CPX · b | CPX | captura | Antiga | 2024-12-11 |
| joaopithon.com.br/cpx-c/ | CPX · c | CPX | captura | Antiga | 2025-02-24 |
| joaopithon.com.br/cpx-d/ | CPX · d | CPX | captura | Antiga | 2025-06-09 |
| joaopithon.com.br/cpx-e/ | CPX · e | CPX | captura | Antiga | 2025-09-18 |
| joaopithon.com.br/fec/ | FEC | FEC | vendas | Antiga | 2024-05-22 |
| joaopithon.com.br/fep-experience-inscricoes-encerradas/ | Fep experience inscrições encerradas | FEP Experience | outro (inscrições encerradas) | Antiga | 2024-07-05 |
| joaopithon.com.br/imersao-avancada-em-rinomodelacao/ | Imersão Avançada em Rinomodelação | IAR | vendas | Antiga | 2024-06-24 |
| joaopithon.com.br/imersao-avancada-em-rinomodelacao-b/ | Imersão Avançada em Rinomodelação · b | IAR | vendas | Antiga | 2024-06-12 |
| joaopithon.com.br/imersao-avancada-em-rinomodelacao-c/ | Imersão Avançada em Rinomodelação · c | IAR | vendas | Antiga | 2024-06-17 |
| joaopithon.com.br/ipl/ | Imersão Avançada em Preenchimento Labial | IPL | vendas | Antiga | 2025-01-25 |
| joaopithon.com.br/ipo/ | Imersão Avançada em Preenchimento de Olheiras | IPO | vendas | Antiga | 2025-02-18 |
| joaopithon.com.br/ipo-a/ | Imersão Avançada em Preenchimento de Olheiras · A | IPO | vendas | Antiga | 2025-02-13 |
| joaopithon.com.br/ipo-b/ | Imersão Avançada em Preenchimento de Olheiras · B | IPO | vendas | Antiga | 2025-02-13 |
| joaopithon.com.br/ipo-c/ | Imersão Avançada em Preenchimento de Olheiras · C | IPO | vendas | Antiga | 2025-02-13 |
| joaopithon.com.br/lista-de-espera-fec/ | Lista de espera · fec | FEC | captura (lista de espera) | Antiga | 2024-05-23 |
| joaopithon.com.br/lista-espera-fep/ | Lista de espera | FEP / PSP (versão antiga) | captura (lista de espera) | Antiga | 2025-09-22 |
| joaopithon.com.br/master-class-em-fios/ | Master Class em Fios | Fios de PDO | captura | Antiga | 2025-07-05 |
| joaopithon.com.br/masterclass-em-fios-de-pdo/ | Masterclass em Fios de PDO | Fios de PDO | captura | Antiga | 2025-07-01 |
| joaopithon.com.br/masterclass-em-toxina-botulinica-cloned-16530/ | Masterclass em Toxina Botulínica · [Cloned #16530] | MTB (versão antiga) | teste/rascunho | Antiga | 2024-12-03 |
| joaopithon.com.br/masterclass-em-toxina-butolinica-a/ | Masterclass em Toxina Butolínica · A | MTB (versão antiga) | captura | Antiga | 2025-05-26 |
| joaopithon.com.br/mep/ | Masterclass em Preenchimento | MEP | captura | Antiga | 2025-07-30 |
| joaopithon.com.br/mep-a/ | Masterclass em Preenchimento · A | MEP | captura | Antiga | 2025-07-29 |
| joaopithon.com.br/obrigado-cpx/ | Onboarding · CPX | CPX | obrigado | Antiga | 2024-04-08 |
| joaopithon.com.br/off-carta-fep/ | Carta · fep | FEP / PSP (versão antiga) | vendas (carta) | Antiga | 2025-09-23 |
| joaopithon.com.br/off-carta-fep-25-06-25/ | off · Carta · fep | FEP / PSP (versão antiga) | vendas (carta) | Antiga | 2025-06-25 |
| joaopithon.com.br/off-dowload-3-psp/ | off · dowload 3 · psp | FEP / PSP (versão antiga) | outro (material) | Antiga | 2025-04-02 |
| joaopithon.com.br/off-fep/ | FEP psp | FEP / PSP (versão antiga) | vendas | Antiga | 2025-09-23 |
| joaopithon.com.br/off-material-didatico-aula-1-psp/ | Material Didático · Aula 1 psp | FEP / PSP (versão antiga) | outro (material) | Antiga | 2025-09-20 |
| joaopithon.com.br/off-material-didatico-aula-2-psp/ | Material Didático · Aula 2 psp | FEP / PSP (versão antiga) | outro (material) | Antiga | 2025-09-20 |
| joaopithon.com.br/off-material-didatico-aula-3-psp/ | off · Material Didático · Aula 3 psp | FEP / PSP (versão antiga) | outro (material) | Antiga | 2025-04-02 |
| joaopithon.com.br/off-material-didatico-aula-4-psp/ | Material Didático · Aula 4 psp | FEP / PSP (versão antiga) | outro (material) | Antiga | 2025-09-20 |
| joaopithon.com.br/off-onboarding-fep/ | Onboarding · FEP | FEP / PSP (versão antiga) | onboarding | Antiga | 2025-09-23 |
| joaopithon.com.br/off-psp/ | Protocolo de Segurança no Preenchimento | FEP / PSP (versão antiga) | vendas | Antiga | 2025-09-09 |
| joaopithon.com.br/onboarding-cac/ | Onboarding · CAC | CAC | onboarding | Antiga | 2024-09-19 |
| joaopithon.com.br/onboarding-fec/ | Onboarding · FEC | FEC | onboarding | Antiga | 2024-05-21 |
| joaopithon.com.br/onboarding-imersao-avancada-em-rinomodelacao/ | Onboarding · Imersão Avançada em Rinomodelação | IAR | onboarding | Antiga | 2024-06-11 |
| joaopithon.com.br/onboarding-ipl/ | Onboarding · IPL | IPL | onboarding | Antiga | 2025-01-20 |
| joaopithon.com.br/onboarding-ipo/ | Onboarding · IPO | IPO | onboarding | Antiga | 2025-01-30 |
| joaopithon.com.br/psp-aa/ | Protocolo de Segurança no Preenchimento · aa | FEP / PSP (versão antiga) | captura | Antiga | 2025-03-12 |
| joaopithon.com.br/psp-b/ | Protocolo de Segurança no Preenchimento · b | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-08 |
| joaopithon.com.br/psp-bb/ | Protocolo de Segurança no Preenchimento · bb | FEP / PSP (versão antiga) | captura | Antiga | 2025-03-27 |
| joaopithon.com.br/psp-c/ | Protocolo de Segurança no Preenchimento · c | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-08 |
| joaopithon.com.br/psp-cc/ | Protocolo de Segurança no Preenchimento · c | FEP / PSP (versão antiga) | captura | Antiga | 2025-03-25 |
| joaopithon.com.br/psp-d/ | Protocolo de Segurança no Preenchimento · d | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-08 |
| joaopithon.com.br/psp-dd/ | Protocolo de Segurança no Preenchimento · dd | FEP / PSP (versão antiga) | captura | Antiga | 2025-03-25 |
| joaopithon.com.br/psp-e/ | Protocolo de Segurança no Preenchimento · e | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-f/ | Protocolo de Segurança no Preenchimento · f | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-g/ | Protocolo de Segurança no Preenchimento · g | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-h/ | Protocolo de Segurança no Preenchimento · h | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-i/ | Protocolo de Segurança no Preenchimento · i | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-j/ | Protocolo de Segurança no Preenchimento · j | FEP / PSP (versão antiga) | captura | Antiga | 2025-09-03 |
| joaopithon.com.br/psp-obrigado/ | Protocolo de segurança no Preenchimento · pesquisa | FEP / PSP (versão antiga) | obrigado | Antiga | 2025-09-03 |
| joaopithon.com.br/teste-form-active/ | teste form active | Institucional / outros | teste/rascunho | Antiga | 2025-07-30 |
| joaopithon.com.br/teste-vitalicio/ | Teste vitalício | Institucional / outros | teste/rascunho | Antiga | 2025-06-13 |
| joaopithon.com.br/upsell-cpx/ | Upsell CPX | Institucional / outros | vendas (upsell) | Antiga | 2024-03-26 |
| joaopithon.com.br/upsell-fec/ | Upsell FEC | FEC | vendas (upsell) | Antiga | 2024-05-22 |
| joaopithon.com.br/upsell-fep-exp/ | Upsell FEP EXP | FEP Experience | vendas (upsell) | Antiga | 2024-08-16 |
| joaopithon.com.br/verificacao-de-numero/ | Verificação de Número | CAC | outro (verificação de número) | Antiga | 2024-08-13 |
| joaopithon.com.br/verificacao-de-numero-falso/ | Verificação de Número · Falso | CAC | outro (verificação de número) | Antiga | 2024-08-13 |
| joaopithon.com.br/verificacao-de-numero-seguro/ | Verificação de Número · Seguro | CAC | outro (verificação de número) | Antiga | 2024-08-13 |
| joaopithon.com.br/verificacao-ipo/ | Verificação IPO | IPO | outro (verificação de número) | Antiga | 2025-02-18 |
| joaopithon.com.br/vitalicio/ | vitalício | Institucional / outros | vendas | Antiga | 2025-09-25 |
| joaopithon.com.br/workshop-em-preenchimento/ | Workshop em Preenchimento | Workshop em Preenchimento | captura | Antiga | 2025-07-01 |
| joaopithon.com.br/workshop-em-preenchimento-a/ | Workshop em Preenchimento · A | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-b/ | Workshop em Preenchimento · B | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-c/ | Workshop em Preenchimento · C | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-d/ | Workshop em Preenchimento · D | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-e/ | Workshop em Preenchimento · E | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-f/ | Workshop em Preenchimento · F | Workshop em Preenchimento | captura | Antiga | 2025-06-13 |
| joaopithon.com.br/workshop-em-preenchimento-g/ | Workshop em Preenchimento · g | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-h/ | Workshop em Preenchimento · h | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-i/ | Workshop em Preenchimento · i | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-j/ | Workshop em Preenchimento · j | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-k/ | Workshop em Preenchimento · k | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-l/ | Workshop em Preenchimento · l | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-m/ | Workshop em Preenchimento · m | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-n/ | Workshop em Preenchimento · n | Workshop em Preenchimento | captura | Antiga | 2025-06-25 |
| joaopithon.com.br/workshop-em-preenchimento-o/ | Workshop em Preenchimento · o | Workshop em Preenchimento | captura | Antiga | 2025-07-01 |
| joaopithon.com.br/ | Acessos úteis | Institucional / outros | outro (hub de links) | Ativa | 2026-10-16 |
| joaopithon.com.br/elementor-28131/ | Redirect | Institucional / outros | outro (redirecionamento) | Ativa | 2026-06-02 |
| joaopithon.com.br/fep-exp-obrigado/ | FEP EXP · Obrigado | FEP Experience | obrigado | Ativa | 2026-09-18 |
| joaopithon.com.br/fep-experience/ | FEP EXPERIENCE | FEP Experience | vendas | Ativa | 2026-08-28 |
| joaopithon.com.br/fep-experience-a/ | FEP EXPERIENCE · A | FEP Experience | vendas | Ativa | 2026-08-28 |
| joaopithon.com.br/links-joao-pithon/ | Links · João Pithon | Institucional / outros | outro (hub de links) | Ativa | 2026-08-05 |
| joaopithon.com.br/lista-de-espera-fep/ | Lista de espera · FEP | FEP · Brasil | captura (lista de espera) | Ativa | 2026-04-07 |
| joaopithon.com.br/onboarding-fep-exp/ | Onboarding · FEP EXP | FEP Experience | onboarding | Ativa | 2026-03-13 |
| joaopithon.com.br/politica-de-privacidade/ | Política de Privacidade | Institucional / outros | institucional | Ativa | 2024-01-12 |
| joaopithon.com.br/redirecionar-whatsapp/ | redirecionar-whatsapp | Institucional / outros | outro (redirecionamento) | Ativa | 2026-06-10 |
| joaopithon.com.br/termos-de-uso/ | Termos de uso | Institucional / outros | institucional | Ativa | 2024-01-12 |
| joaopithon.com.br/psp-a/ | Protocolo de Segurança no Preenchimento · a | FEP / PSP (versão antiga) | captura | Recente | 2026-04-14 |
| bf./black-da-fep/ | Black da Fep | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-a/ | Black da Fep · a | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-b/ | Black da Fep · b | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-c/ | Black da Fep · c | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-d/ | Black da Fep · d | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-e/ | Black da Fep · e | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-f/ | Black da Fep · f | Black da FEP 12/25 | vendas | Antiga | 2025-12-09 |
| bf./black-da-fep-g/ | Black da Fep · g | Black da FEP 12/25 | vendas | Antiga | 2025-12-12 |
| bf./black-da-fep-h/ | Black da Fep · h | Black da FEP 12/25 | vendas | Antiga | 2025-12-12 |
| bf./black-vitalicia-abertura-cloned/ | Black Vitalícia · Abertura · [Cloned #2069] | Black Vitalícia | teste/rascunho | Antiga | 2026-03-06 |
| bf./black-vitalicia-c/ | Black Vitalícia · C | Black Vitalícia | vendas | Antiga | 2025-10-15 |
| bf./black-vitalicia-e/ | Black Vitalícia · E | Black Vitalícia | vendas | Antiga | 2025-10-15 |
| bf./black-vitalicia-f/ | Black Vitalícia · F | Black Vitalícia | vendas | Antiga | 2025-10-15 |
| bf./black-vitalicia-verificacao/ | Black Vitalícia · Verificação Aluno | Black Vitalícia | outro (verificação de número) | Antiga | 2025-10-27 |
| bf./captura-aluno/ | Captura Aluno | Black Vitalícia | captura | Antiga | 2024-11-01 |
| bf./download-3-psp/ | Download 3 psp | ? | outro (material) | Antiga | 2025-04-02 |
| bf./lista-de-espera-obrigado/ | Lista de Espera · obrigado | Black Vitalícia | obrigado | Antiga | 2025-11-27 |
| bf./material-didatico-aula-3-psp/ | Material Didático Aula 3 psp | ? | outro (material) | Antiga | 2025-04-02 |
| bf./mem/ | Masterclass em Mandíbula | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-12-15 |
| bf./mem-a/ | Masterclass em Mandíbula · a | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-14 |
| bf./mem-b/ | Masterclass em Mandíbula · b | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-14 |
| bf./mer/ | MasterClass em Rinomodelação | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-07 |
| bf./mer-a/ | MasterClass em Rinomodelação · a | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-07 |
| bf./mer-b/ | MasterClass em Rinomodelação · b | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-07 |
| bf./mer-c/ | MasterClass em Rinomodelação · c | Masterclasses Rino/Mandíbula 11/25 | captura | Antiga | 2025-11-08 |
| bf./off-black-vitalicia/ | Black Vitalícia | Black Vitalícia | vendas | Antiga | 2025-11-06 |
| bf./off-verificacao-aluno/ | Verificação Aluno | Black Vitalícia | outro (verificação de número) | Antiga | 2024-12-03 |
| bf./off-vitalicio-abertura/ | Vitalício Abertura | Black Vitalícia | vendas | Antiga | 2024-12-03 |
| bf./onboarding-black-friday-vitalicio-cloned-283/ | Onboarding Black Friday Vitalício · [Cloned #283] | Black Vitalícia | onboarding | Antiga | 2024-10-30 |
| bf./privacy-policy/ | Privacy Policy | ? | institucional | Antiga | 2024-10-24 |
| bf./redirect/ | redirect | ? | outro (redirecionamento) | Antiga | 2025-06-03 |
| bf./sample-page/ | Sample Page | ? | teste/rascunho | Antiga | 2024-10-23 |
| bf./teste/ | Teste | ? | teste/rascunho | Antiga | 2025-11-07 |
| bf./teste-captura-bf/ | teste captura bf | ? | teste/rascunho | Antiga | 2025-10-14 |
| bf./teste-form/ | teste form | ? | teste/rascunho | Antiga | 2024-11-12 |
| bf./verificacao-aluno-2/ | Verificação Aluno 2 | Black Vitalícia | outro (verificação de número) | Antiga | 2024-10-25 |
| bf./black-vitalicia-obrigado/ | black-vitalicia-obrigado | Black Vitalícia | obrigado | Ativa | 2026-10-19 |
| bf./black-vitalicia-obrigado-alunos/ | black-vitalicia-obrigado · cupom | Black Vitalícia | obrigado | Ativa | 2026-10-19 |
| bf./lista-de-espera-bf/ | Black Vitalícia · Lista de Espera | Black Vitalícia | captura (lista de espera) | Ativa | 2026-10-08 |
| bf./onboarding-bfv/ | Onboarding Black Friday Vitalício | Black Vitalícia | onboarding | Ativa | 2026-10-19 |
| bf./verificacao-numeros/ | Verificação números | Black Vitalícia | outro (verificação de número) | Ativa | 2026-10-01 |
| bf./black-vitalicia/ | Black Vitalícia · B | Black Vitalícia | vendas | Ativa (já tem versão no código) | 2026-09-30 |
| bf./black-vitalicia-cupom/ | Black Vitalícia · Cupom | Black Vitalícia | vendas | Ativa (já tem versão no código) | 2026-09-29 |
| bf./black-vitalicia-d/ | Black Vitalícia · D | Black Vitalícia | vendas | Ativa (já tem versão no código) | 2026-09-30 |
| bf./off-black-vitalicia-abertura/ | Black Vitalícia · Abertura | Black Vitalícia | vendas | Ativa (já tem versão no código) | 2026-10-20 |
| bf./lista-de-espera/ | Lista de Espera | Black Vitalícia | captura (lista de espera) | Migrada | 2024-11-28 |
| bio./sample-page/ | Sample Page | Masterclass em Bioestimulador / FBio · Brasil | teste/rascunho | Antiga | 2026-06-04 |
| bio./fbio/ | Formação Especialista em Bioestimuladores | Masterclass em Bioestimulador / FBio · Brasil | vendas | Ativa | 2026-06-17 |
| bio./fbio-latam/ | Formação Especialista em Bioestimuladores · LATAM | Masterclass em Bioestimulador / FBio · Latam | vendas | Ativa | 2026-08-17 |
| bio./live-zoom/ | Live Zoom | Masterclass em Bioestimulador / FBio · Brasil | zoom | Ativa | 2026-06-11 |
| bio./live-zoom-latam/ | Live Zoom · LATAM | Masterclass em Bioestimulador / FBio · Latam | zoom | Ativa | 2026-08-04 |
| bio./masterclass-bio/ | Masterclass em Bioestimuladores de Colágeno | Masterclass em Bioestimulador / FBio · Brasil | captura | Ativa | 2026-06-10 |
| bio./masterclass-bio-a/ | Masterclass em Bioestimuladores de Colágeno · a | Masterclass em Bioestimulador / FBio · Brasil | captura | Ativa | 2026-06-10 |
| bio./masterclass-bio-latam/ | Masterclass em Bioestimuladores de Colágeno · LATAM | Masterclass em Bioestimulador / FBio · Latam | captura | Ativa | 2026-08-17 |
| bio./masterclass-bio-latam-a/ | Masterclass em Bioestimuladores de Colágeno · LATAM · A | Masterclass em Bioestimulador / FBio · Latam | captura | Ativa | 2026-08-10 |
| bio./masterclass-bio-latam-b/ | Masterclass em Bioestimuladores de Colágeno · LATAM · B | Masterclass em Bioestimulador / FBio · Latam | captura | Ativa | 2026-08-10 |
| bio./masterclass-bio-obrigado/ | Obrigado · Masterclass em Bioestimuladores de Colágeno | Masterclass em Bioestimulador / FBio · Brasil | obrigado | Ativa | 2026-06-09 |
| bio./masterclass-bio-obrigado-latam/ | Obrigado · Masterclass em Bioestimuladores de Colágeno · LATAM | Masterclass em Bioestimulador / FBio · Latam | obrigado | Ativa | 2026-08-14 |
| bio./onboarding/ | Onboarding · Formação Especialista em Bioestimuladores | Masterclass em Bioestimulador / FBio · Brasil | onboarding | Ativa | 2026-06-13 |
| bio./onboarding-latam/ | Onboarding · Formação Especialista em Bioestimuladores · LATAM | Masterclass em Bioestimulador / FBio · Latam | onboarding | Ativa | 2026-08-10 |
| ctx./sample-page/ | Sample Page | CTX · Brasil | teste/rascunho | Antiga | 2026-06-16 |
| ctx./curso-de-toxina-express/ | Curso de Toxina Express | CTX · Brasil | vendas | Ativa | 2026-09-14 |
| ctx./curso-de-toxina-express-latam/ | Curso de Toxina Express · LATAM | CTX · Latam | vendas | Ativa | 2026-09-14 |
| ctx./obrigado-ctx/ | Obrigado · ctx | CTX · Brasil | obrigado | Ativa | 2026-09-01 |
| ctx./obrigado-ctx-latam/ | Obrigado · ctx · latam | CTX · Latam | obrigado | Ativa | 2026-09-21 |
| eb./sample-page/ | Sample Page | ? | teste/rascunho | Antiga | 2025-10-31 |
| eb./ebook-pto/ | Preenchimento Tridimensional de Olheiras · Ebook | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-a/ | Preenchimento Tridimensional de Olheiras · A | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-b/ | Preenchimento Tridimensional de Olheiras · b | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-c/ | Preenchimento Tridimensional de Olheiras · C | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-d/ | Preenchimento Tridimensional de Olheiras · D | Ebook Olheiras (PTO) | vendas | Ativa | 2026-05-21 |
| eb./ebook-pto-e/ | Preenchimento Tridimensional de Olheiras · E | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-f/ | Preenchimento Tridimensional de Olheiras · F | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-g/ | Preenchimento Tridimensional de Olheiras · G | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-h/ | Preenchimento Tridimensional de Olheiras · H | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-l/ | Preenchimento Tridimensional de Olheiras · l | Ebook Olheiras (PTO) | vendas | Ativa | 2026-06-23 |
| eb./ebook-pto-obrigado/ | Preenchimento Tridimensional de Olheiras · Obrigado | Ebook Olheiras (PTO) | obrigado | Ativa | 2026-09-01 |
| eb./intercorrencias/ | Intercorrências no Preenchimento Facial · Ebook | Ebook Intercorrências | vendas | Ativa | 2025-12-19 |
| eb./intercorrencias-l/ | Intercorrências no Preenchimento Facial · l | Ebook Intercorrências | vendas | Ativa | 2025-12-19 |
| eb./upsell-cac/ | Upssell · CAC | Upsell de ebook (CPX/CAC) | vendas (upsell) | Ativa | 2026-01-13 |
| eb./upsell-cpx/ | Upsell · CPX | Upsell de ebook (CPX/CAC) | vendas (upsell) | Ativa | 2026-01-15 |
| el./esboco/ | esboço | Elite Injectors Congress 2026 | teste/rascunho | Antiga | 2026-09-15 |
| el./sample-page/ | Sample Page | Elite Injectors Congress 2026 | teste/rascunho | Antiga | 2026-07-02 |
| el./checkin/ | ELITE INJECTORS CONGRESS · Checkin | Elite Injectors Congress 2026 | check-in/pesquisa | Recente | 2026-08-28 |
| el./elite-injectors-congress/ | ELITE INJECTORS CONGRESS | Elite Injectors Congress 2026 | vendas | Recente (já tem versão no código) | 2026-10-15 |
| el./elite-injectors-congress-a/ | ELITE INJECTORS CONGRESS · A | Elite Injectors Congress 2026 | vendas | Recente (já tem versão no código) | 2026-10-15 |
| fea./sample-page/ | Sample Page | Masterclass em Anatomia / FEA | teste/rascunho | Antiga | 2026-05-21 |
| fea./fea/ | Formação Especialista em Anatomia | Masterclass em Anatomia / FEA | vendas | Recente | 2026-06-02 |
| fea./mea/ | Masterclass em Anatomia | Masterclass em Anatomia / FEA | captura | Recente | 2026-06-03 |
| fea./mea-a/ | Masterclass em Anatomia · A | Masterclass em Anatomia / FEA | captura | Recente | 2026-05-26 |
| fea./mea-obrigado/ | Masterclass em  Anatomia · Obrigado | Masterclass em Anatomia / FEA | obrigado | Recente | 2026-05-26 |
| fea./onboarding/ | Onboarding FEA | Masterclass em Anatomia / FEA | onboarding | Recente | 2026-06-02 |
| feb./mtb-a/ | Masterclass em Toxina Botulínica · a | FEB / MTB · Brasil | captura | Antiga | 2025-10-06 |
| feb./mtb-letybo/ | Masterclass em Toxina Botulínica · Letybo | FEB / MTB · Brasil | captura | Antiga | 2025-10-07 |
| feb./mtb-letybo-a/ | Masterclass em Toxina Botulínica · Letybo · A | FEB / MTB · Brasil | captura | Antiga | 2025-10-07 |
| feb./mtb-letybo-b/ | Masterclass em Toxina Botulínica · Letybo · B | FEB / MTB · Brasil | captura | Antiga | 2025-10-07 |
| feb./mtb-letybo-c/ | Masterclass em Toxina Botulínica · Letybo · c | FEB / MTB · Brasil | captura | Antiga | 2025-10-07 |
| feb./redirect/ | Redirect | FEB / MTB · Brasil | outro (redirecionamento) | Antiga | 2025-06-04 |
| feb./sample-page/ | Sample Page | FEB / MTB · Brasil | teste/rascunho | Antiga | 2025-05-26 |
| feb./teste-formulario/ | teste formulário | FEB / MTB · Brasil | teste/rascunho | Antiga | 2025-06-06 |
| feb./teste-formulario-2/ | teste formulário 2 | FEB / MTB · Brasil | teste/rascunho | Antiga | 2025-06-06 |
| feb./teste-formulario-3/ | teste formulário 3 | FEB / MTB · Brasil | teste/rascunho | Antiga | 2025-06-06 |
| feb./feb/ | Formação Especialista em Botox | FEB / MTB · Brasil | vendas | Ativa | 2026-08-11 |
| feb./feb-latam/ | Formação Especialista em Botox · LATAM | FEB / MTB · Latam | vendas | Ativa | 2026-07-10 |
| feb./feb-latam-a/ | Formação Especialista em Botox · LATAM · a | FEB / MTB · Latam | vendas | Ativa | 2026-07-07 |
| feb./live-zoom/ | Live zoom | FEB / MTB · Brasil | zoom | Ativa | 2026-07-31 |
| feb./mtb-b/ | Masterclass em Toxina Botulínica · b | FEB / MTB · Brasil | captura | Ativa | 2026-11-01 |
| feb./mtb-latam/ | Masterclass em Toxina Botulínica · latam | FEB / MTB · Latam | captura | Ativa | 2026-08-14 |
| feb./onboarding/ | Onboarding | FEB / MTB · Brasil | onboarding | Ativa | 2026-01-08 |
| feb./onboarding-latam/ | Onboarding · LATAM | FEB / MTB · Latam | onboarding | Ativa | 2026-07-03 |
| feb./pesquisa/ | Pesquisa · MTB | FEB / MTB · Brasil | check-in/pesquisa | Ativa | 2026-11-03 |
| feb./pesquisa-latam/ | Pesquisa · LATAM | FEB / MTB · Latam | check-in/pesquisa | Ativa | 2026-08-13 |
| feb./vk/ | Formação Especialista em Botox · vk | FEB / MTB · Brasil | vendas | Ativa | 2026-08-11 |
| feb./mtb/ | Masterclass em Toxina Botulínica | FEB / MTB · Brasil | captura | Migrada | 2026-11-03 |
| fef./fef/ | Formação Especialista em Fios | FEF / Masterclass em Fios | vendas | Antiga | 2025-07-31 |
| fef./master-class-em-fios-a/ | Master Class em Fios · A | FEF / Masterclass em Fios | captura | Antiga | 2025-07-10 |
| fef./master-class-em-fios-teste/ | Master Class em Fios · teste | FEF / Masterclass em Fios | teste/rascunho | Antiga | 2025-07-10 |
| fef./masterclass-em-fios/ | Master Class em Fios | FEF / Masterclass em Fios | captura | Antiga | 2025-07-30 |
| fef./onboarding-fef/ | Onboarding | FEF / Masterclass em Fios | onboarding | Antiga | 2025-07-12 |
| fef./sample-page/ | Sample Page | FEF / Masterclass em Fios | teste/rascunho | Antiga | 2025-07-05 |
| fef./teste-form-active/ | teste form active | FEF / Masterclass em Fios | teste/rascunho | Antiga | 2025-07-10 |
| fep./formacao-especialista-em-preenchimento-cloned-363/ | Formação Especialista em Preenchimento · [Cloned #363] | FEP · Brasil | teste/rascunho | Antiga | 2026-04-16 |
| fep./off-psp-obrigado/ | Protocolo de Segurança do Preenchimento · pesquisa | PSP (captação FEP) | obrigado | Antiga | 2025-09-11 |
| fep./psp-k/ | Protocolo de Segurança no Preenchimento · k | PSP (captação FEP) | captura | Antiga | 2025-09-09 |
| fep./psp-l/ | Protocolo de Segurança no Preenchimento · l | PSP (captação FEP) | captura | Antiga | 2025-09-09 |
| fep./psp-m/ | Protocolo de Segurança no Preenchimento · m | PSP (captação FEP) | captura | Antiga | 2025-09-09 |
| fep./psp-n/ | Protocolo de Segurança no Preenchimento · n | PSP (captação FEP) | captura | Antiga | 2025-09-09 |
| fep./psp-o/ | Protocolo de Segurança no Preenchimento · o | PSP (captação FEP) | captura | Antiga | 2025-09-09 |
| fep./psp-p/ | Protocolo de Segurança no Preenchimento · p | PSP (captação FEP) | captura | Antiga | 2025-09-13 |
| fep./psp-q/ | Protocolo de Segurança no Preenchimento · Q | PSP (captação FEP) | captura | Antiga | 2025-09-17 |
| fep./psp-r/ | Protocolo de Segurança no Preenchimento · R | PSP (captação FEP) | captura | Antiga | 2025-09-17 |
| fep./psp-s/ | Protocolo de Segurança no Preenchimento · S | PSP (captação FEP) | captura | Antiga | 2025-09-17 |
| fep./psp-t/ | Protocolo de Segurança no Preenchimento · T | PSP (captação FEP) | captura | Antiga | 2025-09-17 |
| fep./psp-u/ | Protocolo de Segurança no Preenchimento · U | PSP (captação FEP) | captura | Antiga | 2025-09-17 |
| fep./redirect/ | Redirect | FEP · Brasil | outro (redirecionamento) | Antiga | 2025-10-02 |
| fep./sample-page/ | Sample Page | FEP · Brasil | teste/rascunho | Antiga | 2025-09-05 |
| fep./carta-fep/ | Carta · fep | FEP · Brasil | vendas (carta) | Ativa | 2026-09-16 |
| fep./carta-fep-latam/ | Carta FEP / LATAM | FEP · Latam | vendas (carta) | Ativa | 2026-10-14 |
| fep./fep/ | Formação Especialista em Preenchimento | FEP · Brasil | vendas | Ativa | 2026-11-06 |
| fep./fep-latam/ | Formação Especialista em Preenchimento / LATAM | FEP · Latam | vendas | Ativa | 2026-10-14 |
| fep./lista-de-espera/ | Formação Especialista em Preenchimento · Lista de espera | FEP · Brasil | captura (lista de espera) | Ativa | 2026-09-03 |
| fep./lista-de-espera-latam/ | Formação Especialista em Preenchimento · Lista de espera / LATAM | FEP · Latam | captura (lista de espera) | Ativa | 2026-10-13 |
| fep./onboarding-fep/ | Onboarding · fep | FEP · Brasil | onboarding | Ativa | 2026-04-06 |
| fep./onboarding-fep-exp/ | Onboarding · Fep Exp | FEP Experience | onboarding | Ativa | 2026-06-19 |
| fep./onboarding-fep-latam/ | Onboarding · FEP / LATAM | FEP · Latam | onboarding | Ativa | 2026-10-13 |
| fep./redirect-2/ | Redirect · 2 | FEP · Brasil | outro (redirecionamento) | Ativa | 2026-02-18 |
| fep./abertura-black/ | Abertura Black da Fep | Black da FEP 12/25 | vendas | Recente | 2026-03-25 |
| fep./carta-fep-21-07-2026/ | Carta · fep · 21.07.2026 | FEP · Brasil | vendas (carta) | Recente | 2026-07-21 |
| fep./off-psp-obrigado-2/ | Protocolo de Segurança do Preenchimento · pesquisa 2 | PSP (captação FEP) | obrigado | Recente | 2026-04-14 |
| fep./psp/ | Protocolo de Segurança no Preenchimento | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-a/ | Protocolo de Segurança no Preenchimento · a | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-aa/ | Protocolo de Segurança no Preenchimento · aa | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| fep./psp-ab/ | Protocolo de Segurança no Preenchimento · ab | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| fep./psp-ac/ | Protocolo de Segurança no Preenchimento · ac | PSP (captação FEP) | captura | Recente | 2026-04-29 |
| fep./psp-ad/ | Protocolo de Segurança no Preenchimento · ad | PSP (captação FEP) | captura | Recente | 2026-04-29 |
| fep./psp-ae/ | Protocolo de Segurança no Preenchimento · ae | PSP (captação FEP) | captura | Recente | 2026-04-29 |
| fep./psp-af/ | Protocolo de Segurança no Preenchimento · af | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-ag/ | Protocolo de Segurança no Preenchimento · ag | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-ah/ | Protocolo de Segurança no Preenchimento · ah | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-ai/ | Protocolo de Segurança no Preenchimento · ai | PSP (captação FEP) | captura | Recente | 2026-05-05 |
| fep./psp-obrigado/ | Protocolo de Segurança do Preenchimento · obrigado | PSP (captação FEP) | obrigado | Recente | 2026-04-15 |
| fep./psp-v/ | Protocolo de Segurança no Preenchimento · V | PSP (captação FEP) | captura | Recente | 2026-04-16 |
| fep./psp-w/ | Protocolo de Segurança no Preenchimento · w | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| fep./psp-x/ | Protocolo de Segurança no Preenchimento · x | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| fep./psp-y/ | Protocolo de Segurança no Preenchimento · y | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| fep./psp-z/ | Protocolo de Segurança no Preenchimento · z | PSP (captação FEP) | captura | Recente | 2026-04-22 |
| iff./area-de-membros-iff/ | Área de Membros IFF | IFF5 · Brasil | outro (área de membros) | Antiga | 2025-05-22 |
| iff./iff10-c/ | Imersão Avançada em Full Face com mais de 10 ml · C | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-d/ | Imersão Avançada em Full Face com mais de 10 ml · D | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-e/ | Imersão Avançada em Full Face com mais de 10 ml · E | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-f/ | Imersão Avançada em Full Face com mais de 10 ml · F | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-g/ | Imersão Avançada em Full Face com mais de 10 ml · G | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-h/ | Imersão Avançada em Full Face com mais de 10 ml · H | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-i/ | Imersão Avançada em Full Face com mais de 10 ml · i | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-j/ | Imersão Avançada em Full Face com mais de 10 ml · j | IFF10 | vendas | Antiga | 2025-08-01 |
| iff./iff10-k/ | Imersão Avançada em Full Face com mais de 10 ml · K | IFF10 | vendas | Antiga | 2025-08-11 |
| iff./iff10-l/ | Imersão Avançada em Full Face com mais de 10 ml · L | IFF10 | vendas | Antiga | 2025-08-13 |
| iff./iff10-m/ | Imersão Avançada em Full Face com mais de 10 ml · M | IFF10 | vendas | Antiga | 2025-08-13 |
| iff./iff10-n/ | Imersão Avançada em Full Face com mais de 10 ml · N | IFF10 | vendas | Antiga | 2025-08-20 |
| iff./iff10-o/ | Imersão Avançada em Full Face com mais de 10 ml · O | IFF10 | vendas | Antiga | 2025-08-20 |
| iff./iff10-p/ | Imersão Avançada em Full Face com mais de 10 ml · P | IFF10 | vendas | Antiga | 2025-08-13 |
| iff./iff10-q/ | Imersão Avançada em Full Face com mais de 10 ml · Q | IFF10 | vendas | Antiga | 2025-08-13 |
| iff./iff5-teste/ | iff5 teste | IFF5 · Brasil | teste/rascunho | Antiga | 2026-01-19 |
| iff./login/ | Login | IFF5 · Brasil | outro (login) | Antiga | 2025-05-17 |
| iff./masterclass-em-intercorrencias-cloned-4677/ | Masterclass em Intercorrências · [Cloned #4677] | Masterclass em Intercorrências (MTI) | teste/rascunho | Antiga | 2026-11-11 |
| iff./sample-page/ | Sample Page | IFF5 · Brasil | teste/rascunho | Antiga | 2025-04-24 |
| iff./t/ | teste pop up | IFF5 · Brasil | teste/rascunho | Antiga | 2026-03-23 |
| iff./teste/ | teste | IFF5 · Brasil | teste/rascunho | Antiga | 2025-07-29 |
| iff./mti/ | Masterclass em Intercorrências | Masterclass em Intercorrências (MTI) | captura | Ativa | 2026-11-12 |
| iff./mti-a/ | Masterclass em Intercorrências · A | Masterclass em Intercorrências (MTI) | captura | Ativa | 2026-09-09 |
| iff./mti-checkin/ | MTI · obrigado | Masterclass em Intercorrências (MTI) | check-in/pesquisa | Ativa | 2026-11-12 |
| iff./mti-zoom/ | Masterclass Intercorrências · Zoom | Masterclass em Intercorrências (MTI) | zoom | Ativa | 2026-09-10 |
| iff./checkout-iff10/ | checkout-iff10 | IFF10 | outro (checkout) | Recente | 2026-08-18 |
| iff./checkout-iff10-67/ | checkout-iff10 · valor 67 | IFF10 | outro (checkout) | Recente | 2026-08-31 |
| iff./checkout-iff5/ | checkout-iff5 | IFF5 · Brasil | outro (checkout) | Recente | 2026-09-18 |
| iff./iff/ | Imersão Avançada em Full Face com menos de 5 ml | IFF5 · Brasil | vendas | Recente | 2026-07-21 |
| iff./iff-a/ | Imersão Avançada em Full Face com menos de 5 ml · a | IFF5 · Brasil | vendas | Recente | 2026-06-25 |
| iff./iff-b/ | Imersão Avançada em Full Face com menos de 5 ml · b | IFF5 · Brasil | vendas | Recente | 2026-06-25 |
| iff./iff-c/ | Imersão Avançada em Full Face com menos de 5 ml · c | IFF5 · Brasil | vendas | Recente | 2026-06-25 |
| iff./iff-d/ | Imersão Avançada em Full Face com menos de 5 ml · d | IFF5 · Brasil | vendas | Recente | 2026-06-24 |
| iff./iff-e/ | Imersão Avançada em Full Face com menos de 5 ml · e | IFF5 · Brasil | vendas | Recente | 2026-06-25 |
| iff./iff-f/ | Imersão Avançada em Full Face com menos de 5 ml · F | IFF5 · Brasil | vendas | Recente | 2026-07-21 |
| iff./iff-g/ | Imersão Avançada em Full Face com menos de 5 ml · g | IFF5 · Brasil | vendas | Recente | 2026-07-21 |
| iff./iff-h/ | Imersão Avançada em Full Face com menos de 5 ml · h | IFF5 · Brasil | vendas | Recente | 2026-07-17 |
| iff./iff-i/ | Imersão Avançada em Full Face com menos de 5 ml · i | IFF5 · Brasil | vendas | Recente | 2026-07-06 |
| iff./iff-j/ | Imersão Avançada em Full Face com menos de 5 ml · j | IFF5 · Brasil | vendas | Recente | 2026-07-13 |
| iff./iff-k/ | Imersão Avançada em Full Face com menos de 5 ml · k | IFF5 · Brasil | vendas | Recente | 2026-07-06 |
| iff./iff-l/ | Imersão Avançada em Full Face com menos de 5 ml · l | IFF5 · Brasil | vendas | Recente | 2026-07-13 |
| iff./iff-m/ | Imersão Avançada em Full Face com menos de 5 ml · m | IFF5 · Brasil | vendas | Recente | 2026-07-06 |
| iff./iff-n/ | Imersão Avançada em Full Face com menos de 5 ml · n | IFF5 · Brasil | vendas | Recente | 2026-07-16 |
| iff./iff-o/ | Imersão Avançada em Full Face com menos de 5 ml · o | IFF5 · Brasil | vendas | Recente | 2026-07-07 |
| iff./iff-p/ | Imersão Avançada em Full Face com menos de 5 ml · p | IFF5 · Brasil | vendas | Recente | 2026-07-17 |
| iff./iff-q/ | Imersão Avançada em Full Face com menos de 5 ml · q | IFF5 · Brasil | vendas | Recente | 2026-07-21 |
| iff./iff-r/ | Imersão Avançada em Full Face com menos de 5 ml · r | IFF5 · Brasil | vendas | Recente | 2026-07-21 |
| iff./iff-s/ | Imersão Avançada em Full Face com menos de 5 ml · s | IFF5 · Brasil | vendas | Recente | 2026-07-16 |
| iff./iff10/ | Imersão Avançada em Full Face com mais de 10 ml · AB | IFF10 | vendas | Recente | 2026-09-15 |
| iff./iff10-a/ | Imersão Avançada em Full Face com mais de 10 ml · A | IFF10 | vendas | Recente | 2026-04-07 |
| iff./iff10-aa/ | Imersão Avançada em Full Face com mais de 10 ml · AA | IFF10 | vendas | Recente | 2026-04-04 |
| iff./iff10-ab/ | Imersão Avançada em Full Face com mais de 10 ml | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ac/ | Imersão Avançada em Full Face com mais de 10 ml · AC | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ad/ | Imersão Avançada em Full Face com mais de 10 ml · AD | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ae/ | Imersão Avançada em Full Face com mais de 10 ml · AE | IFF10 | vendas | Recente | 2026-09-15 |
| iff./iff10-af/ | Imersão Avançada em Full Face com mais de 10 ml · AF | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ag/ | Imersão Avançada em Full Face com mais de 10 ml · AG | IFF10 | vendas | Recente | 2026-09-08 |
| iff./iff10-ah/ | Imersão Avançada em Full Face com mais de 10 ml · AH | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ai/ | Imersão Avançada em Full Face com mais de 10 ml · AI | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-aj/ | Imersão Avançada em Full Face com mais de 10 ml · AJ | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-ak/ | Imersão Avançada em Full Face com mais de 10 ml · AK | IFF10 | vendas | Recente | 2026-08-27 |
| iff./iff10-al/ | Imersão Avançada em Full Face com mais de 10 ml · AL | IFF10 | vendas | Recente | 2026-08-28 |
| iff./iff10-am/ | Imersão Avançada em Full Face com mais de 10 ml · AM | IFF10 | vendas | Recente | 2026-08-28 |
| iff./iff10-an/ | Imersão Avançada em Full Face com mais de 10 ml · AN | IFF10 | vendas | Recente | 2026-09-03 |
| iff./iff10-ao/ | Imersão Avançada em Full Face com mais de 10 ml · AO | IFF10 | vendas | Recente | 2026-09-15 |
| iff./iff10-ap/ | Imersão Avançada em Full Face com mais de 10 ml · AP | IFF10 | vendas | Recente | 2026-09-08 |
| iff./iff10-b/ | Imersão Avançada em Full Face com mais de 10 ml · B | IFF10 | vendas | Recente | 2026-04-07 |
| iff./iff10-r/ | Imersão Avançada em Full Face com mais de 10 ml · R | IFF10 | vendas | Recente | 2026-03-13 |
| iff./iff10-s/ | Imersão Avançada em Full Face com mais de 10 ml · S | IFF10 | vendas | Recente | 2026-08-25 |
| iff./iff10-t/ | Imersão Avançada em Full Face com mais de 10 ml · T | IFF10 | vendas | Recente | 2026-03-18 |
| iff./iff10-u/ | Imersão Avançada em Full Face com mais de 10 ml · U | IFF10 | vendas | Recente | 2026-03-18 |
| iff./iff10-v/ | Imersão Avançada em Full Face com mais de 10 ml · V | IFF10 | vendas | Recente | 2026-04-07 |
| iff./iff10-w/ | Imersão Avançada em Full Face com mais de 10 ml · W | IFF10 | vendas | Recente | 2026-04-07 |
| iff./iff10-x/ | Imersão Avançada em Full Face com mais de 10 ml · X | IFF10 | vendas | Recente | 2026-03-20 |
| iff./iff10-y/ | Imersão Avançada em Full Face com mais de 10 ml · Y | IFF10 | vendas | Recente | 2026-03-23 |
| iff./iff10-z/ | Imersão Avançada em Full Face com mais de 10 ml · Z | IFF10 | vendas | Recente | 2026-04-07 |
| iff./iff10-zoom/ | Imersão Avançada em Full Face com mais de 10 ml · Zoom | IFF10 | zoom | Recente | 2026-08-04 |
| iff./iff10ml-obrigado/ | Iff 10ml · obrigado | IFF10 | obrigado | Recente | 2026-08-14 |
| iff./iff5-b/ | Imersão Avançada em Full Face com mais de 5 ml · LATAM · B | IFF5 · Latam | vendas | Recente | 2026-10-07 |
| iff./iff5-latam-a/ | Imersão Avançada em Full Face com mais de 5 ml · LATAM · A | IFF5 · Latam | vendas | Recente | 2026-10-07 |
| iff./iff5-latam-obrigado/ | Iff 5ml · obrigado · latam | IFF5 · Latam | obrigado | Recente | 2026-09-21 |
| iff./iff5-latam-zoom/ | Imersão Avançada em Full Face com menos de 5ml · Zoom · LATAM | IFF5 · Latam | zoom | Recente | 2026-10-12 |
| iff./iff5ml-obrigado/ | Iff 5ml · obrigado | IFF5 · Brasil | obrigado | Recente | 2026-06-19 |
| iff./ | Imersão Avançada em Full Face com mais de 5 ml · LATAM | IFF5 · Latam | vendas | Recente (já tem versão no código) | 2026-10-07 |
| pg./ | pós graduação | Pós-Graduação | vendas | Antiga | 2026-02-09 |
| pg./carta/ | Carta | Pós-Graduação | vendas (carta) | Antiga | 2026-02-09 |
| pg./onboarding-pos-graduacao/ | Onboarding · Pós Graduação | Pós-Graduação | onboarding | Antiga | 2026-02-10 |
| pg./sample-page/ | Sample Page | Pós-Graduação | teste/rascunho | Antiga | 2025-01-20 |
| pg./upsell-fep/ | Upsell · FEP | Pós-Graduação | vendas (upsell) | Recente | 2026-05-04 |
| pl./sample-page/ | Sample Page | Masterclass em Preenchimento Labial (MPL) | teste/rascunho | Antiga | 2026-03-03 |
| pl./teste/ | teste | Masterclass em Preenchimento Labial (MPL) | teste/rascunho | Antiga | 2026-07-09 |
| pl./live-zoom-mpl/ | Live zoom · mpl | Masterclass em Preenchimento Labial (MPL) | zoom | Ativa | 2026-11-13 |
| pl./pesquisa-mpl/ | Masterclass em Preenchimento Labial · Pesquisa | Masterclass em Preenchimento Labial (MPL) | check-in/pesquisa | Ativa | 2026-11-11 |
| pl./mpl/ | Masterclass em Preenchimento Labial · 4 | Masterclass em Preenchimento Labial (MPL) | captura | Migrada | 2026-07-13 |
| pl./mpl-a/ | Masterclass em Preenchimento Labial · 3 | Masterclass em Preenchimento Labial (MPL) | captura | Recente | 2026-07-13 |
| pl./mpl-b/ | Masterclass em Preenchimento Labial · b | Masterclass em Preenchimento Labial (MPL) | captura | Recente | 2026-07-09 |
| pl./mpl-c/ | Masterclass em Preenchimento Labial · c | Masterclass em Preenchimento Labial (MPL) | captura | Recente | 2026-07-13 |
