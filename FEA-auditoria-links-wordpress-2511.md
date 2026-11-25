# FEA · Auditoria de links das 75 páginas WordPress ativas (25/11/2026)

Auditoria só de leitura das 75 páginas marcadas como *Ativa* em `FEA-inventario-paginas-wordpress-2511.md`. Nada foi alterado em WordPress, ClickUp, Drive ou repositório.

**Critério de sucesso:** as 75 páginas baixadas, todo link de ação (checkout, WhatsApp, Sendflow, Zoom, páginas internas, formulários, vídeos) testado com status final, e toda data visível vencida registrada.

**Método:** HTML de cada página baixado com curl (sem imagens, User-Agent de Chrome); as 75 responderam 200 sem redirecionamento. Links extraídos de `href`, popups do Elementor e containers com link (data-settings). 199 URLs únicas testadas com GET seguindo redirecionamento, uma requisição a cada 0,5 s. Os 9 checkouts Hotmart foram abertos num navegador real (o curl recebe desafio anti-robô 202 do AWS WAF), com nome do produto conferido; o preço aparece em US$ porque o teste saiu de IP dos EUA. Vídeos do YouTube conferidos pelo oEmbed (todos 200, nenhum removido ou privado). Grupos de WhatsApp: todos os 10 convites `chat.whatsapp.com` estão válidos (mostram nome do grupo). Formulários Elementor mandam o lead para o destino configurado no servidor, que não aparece no HTML; esses destinos não puderam ser testados de fora. Salas do Zoom respondem 200 sempre (a página de entrada não diz se a reunião expirou), então o critério foi o número da sala versus o evento.

## Resumo: só os problemas, por urgência

### 1. Masterclass em Bioestimulador 12/26 e Combo 2 em 1: FEB + FEBio Vitalício (captação começa 30/11)

1. **bio./masterclass-bio-obrigado/**: o botão "ENTRE PARA O GRUPO DO WHATSAPP" vai para `joaopithon.com.br/masterclass-grupo`, que hoje redireciona para a campanha Sendflow `masterclass-em-intercorrencias-nov-26`, cujo grupo atual é "⚡ BLACK VITALÍCIA: REABERTURA RELÂMPAGO". Lead de Bioestimulador cai no grupo da Black.
2. **bio./masterclass-bio-obrigado-latam/**: o botão do grupo vai para `joaopithon.com.br/masterclass-grupo-latam`, que redireciona para `sndflw.com/i/iff5ml-latam-1026` (Imersão Full Face menos de 5 ml Latam).
3. **bio./live-zoom/**: o botão "ACESSAR SALA DE AULA" abre a sala de junho `us06web.zoom.us/j/81204025790`; a live de 08/12 precisa da sala nova (a versão Latam usa a máscara `aula-zoom-latam`, sala 84558582144).
4. **bio./fbio/** (vendas FBio Brasil): sem checkout. O botão "QUERO APROVEITAR" da oferta está sem link e os outros 3 botões levam a `#top`, que é a própria oferta. A versão Latam tem checkout funcionando (Formación Especialista en Bioestimuladores).
5. **Datas vencidas no Bio:** contador "15 de junho, às 20h" em bio./masterclass-bio/ e bio./masterclass-bio-a/; "Lunes, 17 de agosto" nas 3 capturas Latam; bônus "até 15 de junho" em bio./fbio/ e bio./fbio-latam/.
6. **bio./onboarding/**: botão "Como acessar a FEBio" com `href="#"` (na Latam o botão equivalente leva à ajuda da Hotmart).
7. **Combo e Masterclass Bio 12/26 no código:** as 5 páginas citadas nos Links úteis (`lp.joaopithon.com.br/febio/masterclass/`, `/obrigado/`, `/combo/`, `/combo/obrigado/`, `/onboarding/`) seguem 404 nesta conferência (25/11, 16h).

### 2. Ebook Intercorrências

8. **eb./intercorrencias/** e **eb./intercorrencias-l/**: os 4 botões de compra têm `href="#"`; não existe checkout em nenhuma das duas páginas.
9. Nas duas, o botão de WhatsApp aponta para `http://Quero%20falar%20com%20a%20equipe!` (texto no lugar da URL, link quebrado).

### 3. Ebook Olheiras (PTO)

10. **eb./ebook-pto-h/**: dois botões ("QUERO TRANSFORMAR A OLHEIRA NO MEU DIFERENCIAL" e "QUERO ME TORNAR REFERÊNCIA EM OLHEIRAs") apontam para `#oferta`, âncora que não existe na página; o clique não faz nada. Os outros botões levam ao checkout correto.
11. **eb./ebook-pto-l/**: botão de WhatsApp com o mesmo link quebrado `http://Quero%20falar%20com%20a%20equipe!`.
Checkout das 10 variações conferido: "[Ebook] A Ciência e Arte do Preenchimento Tridimensional das Olheiras", ativo.

### 4. CTX (Curso de Toxina Express)

12. **ctx./curso-de-toxina-express/**: botão "Quero aprender com o Dr. João Pithon" com `href="#"`.
13. **ctx./curso-de-toxina-express-latam/**: botão "QUIERO APRENDER CON EL DR. JOÃO PITHON" com `href="#"` e botão "QUIERO APROVECHAR" que só volta ao topo (`#top` sem alvo; na versão Brasil o mesmo botão vai ao WhatsApp).
Checkouts Brasil (CTX Protocolo Glabela) e Latam (Curso de Toxina Express, Protocolo Glabela) ativos.

### 5. FEB / MTB

14. **feb./pesquisa/** (destino pós-cadastro da MTB, e o repositório lp aponta para ela): o botão do grupo vai à campanha Sendflow `masterclass-em-toxina-botulinica-nov-26`, que hoje abre "⚡ BLACK VITALÍCIA: REABERTURA RELÂMPAGO". Se a Masterclass Toxina 12/26 reaproveitar essa página, o lead cai no grupo da Black.
15. **feb./mtb-b/**: contador "9 de novembro, às 20h" (vencido) e lista de marcas de toxina (Botox, Xeomin, Dysport, Letybo etc.), que pela linha vermelha 3 precisa de aprovação.
16. **feb./feb/** e **feb./vk/**: bônus "até 23h59 do dia 11 de agosto" (vencido). A feb./vk/ não mostra checkout no HTML (só `#oferta` e formulário).
17. **feb./feb-latam/** e **feb./feb-latam-a/**: o popup do botão principal está em português ("Preencha o formulário e se torne uma especialista em Botox"). Na feb-latam-a, o vídeo embutido é "As 7 marcas de toxinas existentes no Brasil hoje" (em português, cita marcas).
18. **feb./mtb-latam/**: data sem dia ("Martes, a las 7PM"), copyright 2025 e lista de marcas.
19. **feb./onboarding-latam/**: rodapé com CNPJ 50.200.444/0001-00; o padrão das outras 71 páginas é 50.297.444/0001-09.
Checkout FEB (Formação Especialista em Botox) ativo.

### 6. FEP

20. **fep./carta-fep/**: "as inscrições abrem na quarta-feira, 16 de setembro" (vencido).
21. **fep./carta-fep-latam/**: o botão "QUIERO APROVECHAR" vai a `joaopithon.com.br/evento-vip-latam`, que redireciona para o Grupo VIP da Imersão Full Face 5 ml Latam (`vip-iff5ml-latam-1026`), não da FEP Latam. Confirmar se é intencional.
22. **fep./fep-latam/**: popup do botão principal em português ("Preencha seus dados para continuar").
23. **fep./fep/** e **fep./fep-latam/**: o checkout depende do formulário do popup (redirecionamento configurado no servidor); não dá para conferir de fora, testar manualmente.

### 7. FEP Experience (próxima edição 28 e 29/11)

24. **joaopithon.com.br/fep-experience/** e **/fep-experience-a/**: anunciam "ÚLTIMOS INGRESSOS 11ª EDIÇÃO, 17 e 18 de Outubro" (vencido).
25. **joaopithon.com.br/fep-exp-obrigado/**: o checkout de pré-matrícula (pay.hotmart.com/P93831788Q) mostra o evento de 16 e 17/08/2025 no WTC.
26. **joaopithon.com.br/onboarding-fep-exp/**: "16 e 17 de Maio" no topo e "16 E 18 DE MAIO" mais abaixo (vencido e inconsistente).
27. **fep./onboarding-fep-exp/**: o formulário Google "Preencher o formulário" devolve 401 (exige login da organização); o botão "Contatar equipe" tem `href="#"`; o site da hospedagem parceira (admilhasconsultoria.com.br) está com certificado SSL expirado.

### 8. Institucional

28. **joaopithon.com.br/** (hub "Acessos úteis"): os ícones de Instagram, TikTok e YouTube levam ao perfil `drajessica.cardiopediatra`, que não é do Dr. João. Grave, corrigir primeiro neste bloco.
29. **joaopithon.com.br/** também leva a destinos encerrados: iff./iff10/ (Imersão de 15 e 16/09, ainda com "COMEÇA HOJE"), el./elite-injectors-congress/ (edição de 01 e 02/11; a 2027 está em lp/elite), fep-experience (datas de outubro) e pg. (bônus de 10/02 e 20/08).
30. **joaopithon.com.br/links-joao-pithon/** (link da bio): leva a feb./feb (bônus de 11/08), fep-exp-bio (fep-experience de outubro, UTM FEPEXP2025) e pos-bio (pg. com bônus vencidos).
31. **joaopithon.com.br/lista-espera-fep/** (destino do hub e da bio, página diferente de /lista-de-espera-fep/): rodapé com CNPJ 42.342.917/0001-14.

### 9. Eventos encerrados (MTI, MPL, Black Vitalícia): conferir se o redirecionamento é intencional

32. **iff./mti-checkin/** e **pl./pesquisa-mpl/**: os grupos Sendflow das masterclasses de novembro hoje abrem os grupos "BLACK VITALÍCIA: REABERTURA RELÂMPAGO" (o da MPL cai no grupo #12). Provável reaproveitamento dos grupos para a reabertura; confirmar.
33. **iff./mti/** ("Terça, 17 de novembro") e **iff./mti-a/** ("14 de setembro"): datas passadas em páginas ativas.
34. **bf./black-vitalicia-obrigado/** e **/black-vitalicia-obrigado-alunos/**: "liberada apenas no dia 19/20 de Outubro" e "27 de Outubro" (passado). Na versão não aluno, o botão "ENTRE PARA O GRUPO DO WHATSAPP" abre conversa com o número 551151940346, não um grupo.
35. **joaopithon.com.br/elementor-28131/**: redireciona para a sala Zoom 82657687599 (junho); conferir se ainda é usada.

36. **Mensagem pronta do WhatsApp de ajuda do Zoom** (bio./live-zoom/, bio./live-zoom-latam/, feb./live-zoom/, iff./mti-zoom/, pl./live-zoom-mpl/): o texto pré-preenchido diz "preciso de ajuda pra acessar a Sala do Zoom" (regra FEA: "para"), e na Latam vai em português.

**O que está ok:** os 9 checkouts Hotmart abrem com o produto certo; os 10 convites `chat.whatsapp.com` são válidos; todos os números de WhatsApp estão bem formados (DDI 55 + DDD + número); as máscaras aula-zoom (81923431173), aula-zoom-2 (85866693966) e aula-zoom-latam (84558582144) redirecionam para salas do Zoom; os 30 vídeos do YouTube estão públicos; nenhuma página ou link interno deu 404, 410 ou 5xx.

## Rastreamento de funil

1. **Limitação técnica atual:** o destino dos formulários Elementor (redirecionamento para checkout ou obrigado, webhook, lista do ActiveCampaign) fica no servidor; sem exportar do editor, a ponta formulário → grupo/checkout não pode ser auditada de fora, e é justamente nela que apareceram os grupos trocados (itens 1, 2 e 14).
2. **Tracking de leitura:** os ebooks Intercorrências e Olheiras podem medir leitura via Heyzine, FlippingBook ou Issuu.
3. **UTM único por QR code e por máscara:** as máscaras `joaopithon.com.br/masterclass-grupo`, `grupovip`, `evento-vip-latam` são reaproveitadas entre eventos; uma máscara por evento (com UTM) evita lead em grupo errado.
4. **Frente no plano de ação:** rastreamento de funil fim a fim, incluindo teste do caminho do lead (Gabi) em cada página antes de cada captação.

Sem métrica, otimização é palpite.

## Tabelas por produto

Legenda do status: código HTTP final (→ destino quando houve redirecionamento); "200 (navegador)" para checkout Hotmart aberto em navegador real com o nome do produto; "âncora" para link interno da própria página.

### Masterclass em Bioestimulador / FBio · Brasil

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| bio./fbio/ | botão sem link "QUERO APROVEITAR" | (vazio) | sem href | PROBLEMA: botão "QUERO APROVEITAR" da oferta sem link (sem checkout na página) |
| bio./fbio/ | âncora/botão "QUERO APROVEITAR" | #top | âncora | PROBLEMA: leva à seção de oferta, cujo botão não tem link; página sem checkout |
| bio./fbio/ | texto da página | (data visível) | n/a | PROBLEMA: bônus "até 23h59 do dia 15 de junho" (vencido) |
| bio./live-zoom/ | Zoom "ACESSAR SALA DE AULA" | https://us06web.zoom.us/j/81204025790 | 200 | PROBLEMA: sala do Zoom de junho (81204025790); live da Masterclass Bio 12/26 precisa da sala nova |
| bio./live-zoom/ | WhatsApp "Preciso de ajuda para entrar" | https://wa.me/551151940346?text=Dr%20Jo%C3%A3o%20preciso%20de%20ajuda%20pra%20acessar%20a%20Sala%20do%20Zoom | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Dr+Jo%C3%A3o+preciso+de+ajuda+pra+acessar+a+Sala+do+Zoo | ok |
| bio./masterclass-bio-a/ | âncora/botão "Quero participar" | #oferta | âncora | ok |
| bio./masterclass-bio-a/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "15 de junho, às 20h" (vencido) |
| bio./masterclass-bio-obrigado/ | página interna "ENTRE PARA O GRUPO DO WHATSAPP" | https://joaopithon.com.br/masterclass-grupo | 200 → https://sndflw.com/i/masterclass-em-intercorrencias-nov-26 | PROBLEMA: redireciona para Sendflow masterclass-em-intercorrencias-nov-26, que hoje abre o grupo da Black Vitalícia Reabertura; não é grupo de Bioestimulador |
| bio./masterclass-bio/ | âncora/botão "Quero participar" | #oferta | âncora | ok |
| bio./masterclass-bio/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "15 de junho, às 20h" (vencido) |
| bio./onboarding/ | âncora/botão "Como acessar a FEBio" | # | âncora | PROBLEMA: botão "Como acessar a FEBio" com href="#" |
| bio./onboarding/ | WhatsApp "Preciso de ajuda" | https://api.whatsapp.com/send/?phone=5511939408518 | 200 | ok |
| bio./onboarding/ | grupo WhatsApp "Entrar no Canal de Alunos FEBio" | https://chat.whatsapp.com/C1taW6B3anLFzLQS8tSwj7 | 200 | ok |
| bio./onboarding/ | área de membros "Acessar a Área de Membros" | https://hotmart.com/pt-br/club/formacao-especialista/products/7646849?from=EditProductPage | 200 | ok |

### Masterclass em Bioestimulador / FBio · Latam

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| bio./fbio-latam/ | âncora/botão "QUIERO APROVECHAR" | #top | âncora | ok (leva à oferta, que tem checkout) |
| bio./fbio-latam/ | checkout Hotmart "QUIERO APROVECHAR" | https://pay.hotmart.com/I106759959E?off=n2gnxcep&checkoutMode=10&bid=1785251390626 | 200 (navegador): Formación Especialista en Bioestimuladores | ok |
| bio./fbio-latam/ | texto da página | (data visível) | n/a | PROBLEMA: bônus "hasta las 23:59 del día 15 de junio" (vencido) |
| bio./live-zoom-latam/ | Zoom "ACCEDER A LA SALA DE CLASE" | https://joaopithon.com.br/aula-zoom-latam | 200 → https://us06web.zoom.us/j/84558582144 | ok |
| bio./live-zoom-latam/ | WhatsApp "Necesito ayuda para entrar" | https://wa.me/551151940346?text=Dr%20Jo%C3%A3o%20preciso%20de%20ajuda%20pra%20acessar%20a%20Sala%20do%20Zoom | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Dr+Jo%C3%A3o+preciso+de+ajuda+pra+acessar+a+Sala+do+Zoo | ok |
| bio./masterclass-bio-latam-a/ | âncora/botão "Quiero participar" | #oferta | âncora | ok |
| bio./masterclass-bio-latam-a/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "Lunes, 17 de agosto" (vencido) |
| bio./masterclass-bio-latam-b/ | âncora/botão "Quiero participar" | #oferta | âncora | ok |
| bio./masterclass-bio-latam-b/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "Lunes, 17 de agosto" (vencido) |
| bio./masterclass-bio-latam/ | âncora/botão "Quiero participar" | #oferta | âncora | ok |
| bio./masterclass-bio-latam/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "Lunes, 17 de agosto" (vencido) |
| bio./masterclass-bio-obrigado-latam/ | página interna "RETIRAR REGALO" | https://bio.joaopithon.com.br/wp-content/uploads/2026/08/Ficha-de-anamnesis-LATAM.docx | 200 | ok |
| bio./masterclass-bio-obrigado-latam/ | página interna "ENTRAR AL GRUPO DE WHATSAPP" | https://joaopithon.com.br/masterclass-grupo-latam | 200 → https://sndflw.com/i/iff5ml-latam-1026 | PROBLEMA: redireciona para Sendflow iff5ml-latam-1026 (grupo da Imersão Full Face Latam), não para grupo de Bioestimulador |
| bio./onboarding-latam/ | WhatsApp "Necesito ayuda" | https://api.whatsapp.com/send/?phone=5511939408518 | 200 | ok |
| bio./onboarding-latam/ | grupo WhatsApp "Entrar al Canal de Alumnos FEBio" | https://chat.whatsapp.com/JXfqDvzSIdIAJZKCdDoICy | 200 | ok |
| bio./onboarding-latam/ | ajuda Hotmart "Cómo acceder a FEBio" | https://help.hotmart.com/pt-br/article/215827338/como-acessar-o-produto-que-comprei-?_hi=eyJjaWQiOiIxNzcwNjc3NzE5OTE2Nzc2MzE3OTI2MTY1NDU0MzA | 200 | ok |
| bio./onboarding-latam/ | área de membros "Acceder al Área de Miembros" | https://hotmart.com/pt-br/club/formacao-especialista/products/8134919?from=EditProductPage | 200 | ok |

### Ebook Intercorrências

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| eb./intercorrencias-l/ | âncora/botão "Quero aprender com o Dr. João Pitho" | # | âncora | PROBLEMA: os 4 botões de compra com href="#", sem checkout |
| eb./intercorrencias-l/ | WhatsApp "Quero aprender com o Dr. João Pitho" | http://Quero%20falar%20com%20a%20equipe! | não testado | PROBLEMA: link quebrado (texto no lugar da URL do WhatsApp) |
| eb./intercorrencias/ | âncora/botão "Quero aprender com o Dr. João Pitho" | # | âncora | PROBLEMA: os 4 botões de compra com href="#", sem checkout |
| eb./intercorrencias/ | WhatsApp "Quero aprender com o Dr. João Pitho" | http://Quero%20falar%20com%20a%20equipe! | não testado | PROBLEMA: link quebrado (texto no lugar da URL do WhatsApp) |

### Ebook Olheiras (PTO)

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| eb./ebook-pto-a/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-a/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-a/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-b/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-b/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-b/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-c/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-c/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-c/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-d/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-d/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-d/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&bid=1776262796244 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-e/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-e/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-e/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-f/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-f/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-f/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-g/ | âncora/botão "QUERO DOMINAR A TÉCNICA TRIDIMENSIO" | #oferta | âncora | ok |
| eb./ebook-pto-g/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-g/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-h/ | âncora/botão "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | #oferta | âncora | PROBLEMA: âncora #oferta não existe na página (2 botões não fazem nada) |
| eb./ebook-pto-h/ | WhatsApp "Quero aprender com o Dr. João Pitho" | https://api.whatsapp.com/send/?phone=5511966256272 | 200 | ok |
| eb./ebook-pto-h/ | checkout Hotmart "QUERO DOMINAR A TÉCNICA DE OLHEIRAS" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&bid=1776262796244 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-h/ | checkout Hotmart "QUERO ME TORNAR REFERÊNCIA EM OLHEI" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-l/ | WhatsApp "Quero aprender com o Dr. João Pitho" | http://Quero%20falar%20com%20a%20equipe! | não testado | PROBLEMA: link quebrado (texto no lugar da URL do WhatsApp) |
| eb./ebook-pto-l/ | checkout Hotmart "Quero aprender com o Dr. João Pitho" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |
| eb./ebook-pto-obrigado/ | grupo WhatsApp "ENTRE PARA O GRUPO DO WHATSAPP" | https://chat.whatsapp.com/KKra8iK6Yz41B40mR8qKJZ | 200 | ok |
| eb./ebook-pto/ | página interna "Quero aprender com o Dr. João Pitho" | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| eb./ebook-pto/ | checkout Hotmart "Quero aprender com o Dr. João Pitho" | https://pay.hotmart.com/S97800165C?off=1lg7jeno&checkoutMode=10 | 200 (navegador): [Ebook] Preenchimento Tridimensional das Olheiras | ok |

### Upsell de ebook (CPX/CAC)

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| eb./upsell-cac/ | âncora/botão "QUERO TER SEGURANÇA" | #oferta | âncora | ok |
| eb./upsell-cac/ | página interna "QUERO FALAR COM A EQUIPE" | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| eb./upsell-cac/ | checkout Hotmart "QUERO TER SEGURANÇA" | https://pay.hotmart.com/D95593160T | 200 (navegador): Assinatura Curso Avançado de Complicações | ok |
| eb./upsell-cac/ | vídeo YouTube | https://youtu.be/YtHJGg8nXDA | 200 (oEmbed): Curso Avançado de Complicações | ok |
| eb./upsell-cpx/ | âncora/botão "QUERO TER SEGURANÇA" | #oferta | âncora | ok |
| eb./upsell-cpx/ | página interna "QUERO FALAR COM A EQUIPE" | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| eb./upsell-cpx/ | checkout Hotmart "QUERO TER SEGURANÇA" | https://pay.hotmart.com/O89651368W?off=ugzaamhx&checkoutMode=10 | 200 (navegador): Curso de Preenchimento Express | ok |
| eb./upsell-cpx/ | vídeo YouTube | https://www.youtube.com/watch?v=wH-GERygMCc | 200 (oEmbed): Curso de Preenchimento Express | ok |

### CTX · Brasil

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| ctx./curso-de-toxina-express/ | âncora/botão "Quero aprender com o Dr. João Pitho" | # | âncora | PROBLEMA: botão "Quero aprender com o Dr. João Pithon" com href="#" |
| ctx./curso-de-toxina-express/ | âncora/botão "GARANTIR PROTOCOLO GLABELA POR R$ 6" | #oferta | âncora | ok |
| ctx./curso-de-toxina-express/ | checkout Hotmart "QUERO MEU PROTOCOLO GLABELA" | https://pay.hotmart.com/X105748129H?off=zzgv77dj | 200 (navegador): CTX Protocolo Glabela | ok |
| ctx./curso-de-toxina-express/ | WhatsApp "QUERO APROVEITAR" | https://wa.me/5511966256272?text=Oi%2C%20tenho%20interesse%20no%20CTX%20-%20Protocolo%20Glabela | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text=Oi%2C+tenho+interesse+no+CTX+-+Protocolo+Glabela&type= | ok |
| ctx./obrigado-ctx/ | grupo WhatsApp "ENTRE PARA O GRUPO DO WHATSAPP" | https://chat.whatsapp.com/DlnjMYMUVwcDQX5hQKwM8n | 200 | ok |

### CTX · Latam

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| ctx./curso-de-toxina-express-latam/ | âncora/botão "QUIERO APRENDER CON EL DR. JOÃO PIT" | # | âncora | PROBLEMA: botão "QUIERO APRENDER CON EL DR. JOÃO PITHON" com href="#" |
| ctx./curso-de-toxina-express-latam/ | âncora/botão "ASEGURAR PROTOCOLO GLABELA POR $29," | #oferta | âncora | ok |
| ctx./curso-de-toxina-express-latam/ | âncora/botão "QUIERO APROVECHAR" | #top | âncora | PROBLEMA: botão "QUIERO APROVECHAR" só volta ao topo (na versão Brasil vai ao WhatsApp) |
| ctx./curso-de-toxina-express-latam/ | checkout Hotmart "QUIERO MI PROTOCOLO GLABELA" | https://pay.hotmart.com/E107212688I?off=bfsu34ha | 200 (navegador): Curso de Toxina Express (Protocolo Glabela) Latam | ok |
| ctx./obrigado-ctx-latam/ | Sendflow (grupo) "ÚNETE AL GRUPO DE WHATSAPP" | https://sndflw.com/i/giJkMm2j9OxkcIV8LZlZ | 200 | ok |

### FEB / MTB · Brasil

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| feb./feb/ | âncora/botão "Assista a aula de introdução gratui" | #aula | âncora | ok |
| feb./feb/ | âncora/botão "QUERO SER UM ESPECIALISTA" | #elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjIxNSIsInRvZ2dsZSI6ZmFsc2V9 | âncora | ok |
| feb./feb/ | âncora/botão "QUERO SER UM ESPECIALISTA" | #oferta | âncora | ok |
| feb./feb/ | WhatsApp "SUPORTE FEB" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./feb/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./feb/ | checkout Hotmart | https://pay.hotmart.com/H62237207S | 200 (navegador): Formação Especialista em Botox | ok |
| feb./feb/ | vídeo YouTube | https://www.youtube.com/watch?v=Ff58AB74ym8 | 200 (oEmbed): A Toxina Botulínica - Formação Especialista em Bot | ok |
| feb./feb/ | texto da página | (data visível) | n/a | PROBLEMA: bônus "até 23h59 do dia 11 de agosto" (vencido) |
| feb./live-zoom/ | Zoom "ACESSAR SALA DE AULA" | https://joaopithon.com.br/aula-zoom | 200 → https://us06web.zoom.us/j/81923431173?pwd=iCwfQ58b7LoeHFijIHiGYVujz4ZkyG.1 | ok |
| feb./live-zoom/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./live-zoom/ | WhatsApp "Preciso de ajuda para entrar" | https://wa.me/551151940346?text=Dr%20Jo%C3%A3o%20preciso%20de%20ajuda%20pra%20acessar%20a%20Sala%20do%20Zoom | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Dr+Jo%C3%A3o+preciso+de+ajuda+pra+acessar+a+Sala+do+Zoo | ok |
| feb./mtb-b/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./mtb-b/ | texto da página | (data visível) | n/a | PROBLEMA: contador para "9 de novembro, às 20h" (vencido); lista marcas de toxina (Xeomin, Dysport etc.), confirmar aprovação |
| feb./onboarding/ | WhatsApp "Preciso de ajuda" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./onboarding/ | grupo WhatsApp "Entrar no Canal dos Alunos FEB" | https://chat.whatsapp.com/H4pyNGrwmoX1wZjGnXS9I7?mode=r_t | 200 | ok |
| feb./onboarding/ | ajuda Hotmart "Como acessar o FEB" | https://help.hotmart.com/pt-br/article/215827338/como-acessar-o-produto-que-comprei- | 200 | ok |
| feb./onboarding/ | área de membros "Área de membros" | https://hotmart.com/pt-br/club/formacao-especialista | 200 | ok |
| feb./onboarding/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./pesquisa/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./pesquisa/ | Sendflow (grupo) "ENTRAR NO GRUPO DO WHATSAPP" | https://sndflw.com/i/masterclass-em-toxina-botulinica-nov-26 | 200 | PROBLEMA: grupo pós-pesquisa da MTB hoje abre "BLACK VITALÍCIA: REABERTURA RELÂMPAGO"; o repositório lp aponta para esta página, então a Masterclass Toxina 12/26 cairia nesse grupo se reaproveitar |
| feb./vk/ | âncora/botão "Assista a aula de introdução gratui" | #aula | âncora | ok |
| feb./vk/ | âncora/botão "QUERO SER UM ESPECIALISTA" | #oferta | âncora | ok |
| feb./vk/ | WhatsApp "SUPORTE FEB" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./vk/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./vk/ | vídeo YouTube | https://www.youtube.com/watch?v=Ff58AB74ym8 | 200 (oEmbed): A Toxina Botulínica - Formação Especialista em Bot | ok |
| feb./vk/ | texto da página | (data visível) | n/a | PROBLEMA: bônus "até 23h59 do dia 11 de agosto" (vencido); página sem checkout visível (só #oferta e formulário) |

### FEB / MTB · Latam

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| feb./feb-latam-a/ | âncora/botão "Mira la clase de introducción gratu" | #aula | âncora | ok |
| feb./feb-latam-a/ | âncora/botão "QUIERO SER UN ESPECIALISTA" | #elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjEwNjIiLCJ0b2dnbGUiOmZhbHNlfQ%3D%3D | âncora | ATENÇÃO: popup do botão em português em página Latam |
| feb./feb-latam-a/ | âncora/botão "QUIERO SER UN ESPECIALISTA" | #oferta | âncora | ok |
| feb./feb-latam-a/ | WhatsApp "SOPORTE FEB" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./feb-latam-a/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./feb-latam-a/ | vídeo YouTube | https://www.youtube.com/watch?v=jK-hLjD0GF4 | 200 (oEmbed): As 7 marcas de toxinas existentes no Brasil hoje | Atenção: vídeo "As 7 marcas de toxinas" em página Latam, título em português e cita marcas (linha vermelha 3: confirmar aprovação) |
| feb./feb-latam/ | âncora/botão "Mira la clase de introducción gratu" | #aula | âncora | ok |
| feb./feb-latam/ | âncora/botão "QUIERO SER UN ESPECIALISTA" | #elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjEwODIiLCJ0b2dnbGUiOmZhbHNlfQ%3D%3D | âncora | ATENÇÃO: popup do botão em português ("Preencha o formulário e se torne uma especialista em Botox") em página Latam |
| feb./feb-latam/ | âncora/botão "QUIERO SER UN ESPECIALISTA" | #oferta | âncora | ok |
| feb./feb-latam/ | WhatsApp "SOPORTE FEB" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./feb-latam/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./feb-latam/ | vídeo YouTube | https://youtu.be/pGBoJC6ZH14 | 200 (oEmbed): Vídeo onboarding Spanish | ok |
| feb./mtb-latam/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./mtb-latam/ | texto da página | (data visível) | n/a | ATENÇÃO: data sem dia ("Martes, a las 7PM"), copyright 2025, lista marcas de toxina |
| feb./onboarding-latam/ | WhatsApp "Pedir ayuda" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| feb./onboarding-latam/ | grupo WhatsApp "Entrar al Canal de Alumnos FEB" | https://chat.whatsapp.com/HkH8sbOgE1ABRXe0m8hgJf | 200 | ok |
| feb./onboarding-latam/ | ajuda Hotmart "Cómo acceder a FEB" | https://help.hotmart.com/pt-br/article/215827338/como-acessar-o-produto-que-comprei- | 200 | ok |
| feb./onboarding-latam/ | área de membros "Área de miembros" | https://hotmart.com/pt-br/club/formacao-especialista | 200 | ok |
| feb./onboarding-latam/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./onboarding-latam/ | texto da página | (data visível) | n/a | ATENÇÃO: rodapé com CNPJ 50.200.444/0001-00 (padrão é 50.297.444/0001-09) |
| feb./pesquisa-latam/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| feb./pesquisa-latam/ | Sendflow (grupo) "ENTRAR AL GRUPO DE WHATSAPP" | https://sndflw.com/i/masterclass-en-toxina-botulinica | 200 | ok |

### FEP · Brasil

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| fep./carta-fep/ | âncora/botão "QUERO APROVEITAR" | #oferta | âncora | ok |
| fep./carta-fep/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./carta-fep/ | página interna "QUERO APROVEITAR" | https://joaopithon.com.br/grupovip | 200 → https://sndflw.com/i/aJWn3xzzi2By6coFm4OE | ok (Sendflow com título genérico "João Pithon"; conferir campanha) |
| fep./carta-fep/ | Sendflow (grupo) "QUERO APROVEITAR!" | https://sndflw.com/i/grupo-vip-fep-0925 | 200 | ok |
| fep./carta-fep/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./carta-fep/ | texto da página | (data visível) | n/a | PROBLEMA: "inscrições abrem na quarta-feira, 16 de setembro" (vencido) |
| fep./fep/ | âncora/botão "QUERO APROVEITAR" | #elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjU4MCIsInRvZ2dsZSI6ZmFsc2V9 | âncora | ATENÇÃO: checkout depende do formulário do popup (ação no servidor, não verificável de fora) |
| fep./fep/ | âncora/botão "Quero aproveitar todos os presentes" | #oferta | âncora | ok |
| fep./fep/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./fep/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./fep/ | vídeo YouTube | https://youtu.be/sAjL9yJK4vI | 200 (oEmbed): AulaFEP venda2 | ok |
| fep./lista-de-espera/ | âncora/botão "ENTRAR NA LISTA DE ESPERA" | #hero | âncora | ok |
| fep./lista-de-espera/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./lista-de-espera/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./onboarding-fep/ | WhatsApp "Preciso de ajuda" | https://api.whatsapp.com/send?phone=5511978511985 | 200 | ok |
| fep./onboarding-fep/ | grupo WhatsApp "Entrar no Canal dos Alunos FEP" | https://chat.whatsapp.com/DbxsHTxXe3oHFWKChAn1As | 200 | ok |
| fep./onboarding-fep/ | formulário "Preencher o formulário" | https://forms.gle/MmMVTZ8PcYk345gf7 | 200 → https://docs.google.com/forms/d/e/1FAIpQLSf_pZPjQFrCSmg-B_NlsGucYtVI7GwyDrJgYoSFYdibOA9NpQ/viewform?usp=send_f | ok |
| fep./onboarding-fep/ | ajuda Hotmart "Como acessar o FEP" | https://help.hotmart.com/pt-br/article/como-acessar-o-produto-que-comprei-/215827338 | 200 | ok |
| fep./onboarding-fep/ | área de membros "Acessar área de membros" | https://hotmart.com/pt-br/club/formacao-especialista | 200 | ok |
| fep./onboarding-fep/ | área de membros "Área de membros" | https://hotmart.com/pt-br/club/formacao-especialista/products/3977383?from=EditProductPage | 200 | ok |
| fep./redirect-2/ | WhatsApp | https://api.whatsapp.com/send?phone=551151040781&text=Ol%C3%A1!%20Gostaria%20de%20mais%20informa%C3%A7%C3%B5es%20sobre%20a%20Imers%C3%A3o%20 | 200 | ok |
| joaopithon.com.br/lista-de-espera-fep/ | botão sem link "A FEP é destinada a qual público?" | (vazio) | sem href | ok |
| joaopithon.com.br/lista-de-espera-fep/ | âncora/botão "QUERO SER UM INJETOR FULL FACE" | #oferta | âncora | ok |
| joaopithon.com.br/lista-de-espera-fep/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/lista-de-espera-fep/ | página interna "suporte@joaopithon.com.br" | mailto:suporte@joaopithon.com.br | não testado | ok |
| joaopithon.com.br/lista-de-espera-fep/ | vídeo YouTube | https://www.youtube.com/watch?v=jdKqqIsDBhE&list=PLKUDo0w3i0KBepIlvouYBVJb9uo26tzRa&index=10&t=7s | 200 (oEmbed): História dos alunos FEP | ok |
| joaopithon.com.br/lista-de-espera-fep/ | vídeo YouTube | https://youtu.be/SXGUPNret7w | 200 (oEmbed): Gabrieli Dortt | ok |
| joaopithon.com.br/lista-de-espera-fep/ | vídeo YouTube | https://youtu.be/pyV7qBTbSBw | 200 (oEmbed): Jéssica Latorre | ok |
| joaopithon.com.br/lista-de-espera-fep/ | vídeo YouTube | https://youtu.be/r347PcxFt7k | 200 (oEmbed): Ana Luiza Simões | ok |

### FEP · Latam

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| fep./carta-fep-latam/ | âncora/botão "QUIERO APROVECHAR" | #oferta | âncora | ok |
| fep./carta-fep-latam/ | página interna | http://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| fep./carta-fep-latam/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./carta-fep-latam/ | página interna "QUIERO APROVECHAR" | https://joaopithon.com.br/evento-vip-latam | 200 → https://sndflw.com/i/vip-iff5ml-latam-1026 | ATENÇÃO: carta FEP Latam leva ao Grupo VIP da Imersão Full Face 5ml Latam (vip-iff5ml-latam-1026); confirmar |
| fep./carta-fep-latam/ | Sendflow (grupo) "QUIERO APROVECHAR!" | https://sndflw.com/i/grupo-vip-fep-0925 | 200 | ok |
| fep./carta-fep-latam/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./fep-latam/ | âncora/botão "QUIERO APROVECHAR" | #elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjIwOTkiLCJ0b2dnbGUiOmZhbHNlfQ%3D%3D | âncora | ATENÇÃO: popup em português ("Preencha seus dados para continuar") em página Latam; checkout depende do formulário |
| fep./fep-latam/ | âncora/botão "Quiero aprovechar todos los regalos" | #oferta | âncora | ok |
| fep./fep-latam/ | página interna | http://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| fep./fep-latam/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./fep-latam/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./lista-de-espera-latam/ | âncora/botão "ENTRAR EN LA LISTA DE ESPERA" | #hero | âncora | ok |
| fep./lista-de-espera-latam/ | página interna | http://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| fep./lista-de-espera-latam/ | página interna "VALIDADOR DE NÚMEROS" | https://bf.joaopithon.com.br/verificacao-numeros/ | 200 | ok |
| fep./lista-de-espera-latam/ | vídeo YouTube | https://www.youtube.com/watch?v=krDoV8ur4L4 | 200 (oEmbed): White Waves - Background | ok |
| fep./onboarding-fep-latam/ | WhatsApp "Necesito ayuda" | https://api.whatsapp.com/send?phone=5511978511985 | 200 | ok |
| fep./onboarding-fep-latam/ | grupo WhatsApp "Entrar al Canal de Alumnos FEP" | https://chat.whatsapp.com/JoD8o5KqqZLLChp8T2tJop | 200 | ok |
| fep./onboarding-fep-latam/ | formulário "Completar el formulário" | https://docs.google.com/forms/d/e/1FAIpQLSe0X6_wno55C6kToA5PzzkG15ZZVxaGGKPpr-ZAODXSb8LImg/viewform | 200 | ok |
| fep./onboarding-fep-latam/ | ajuda Hotmart "Cómo acceder a la FEP" | https://help.hotmart.com/pt-br/article/como-acessar-o-produto-que-comprei-/215827338 | 200 | ok |
| fep./onboarding-fep-latam/ | área de membros "Acessar área de membros" | https://hotmart.com/pt-br/club/formacao-especialista | 200 | ok |
| fep./onboarding-fep-latam/ | área de membros "Área de miembros" | https://hotmart.com/pt-br/club/formacao-especialista/products/3977383?from=EditProductPage | 200 | ok |

### FEP Experience

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| fep./onboarding-fep-exp/ | âncora/botão "Contatar equipe" | # | âncora | PROBLEMA: botão "Contatar equipe" com href="#" (os outros dois "#" têm versão com link) |
| fep./onboarding-fep-exp/ | WhatsApp "Preciso de ajuda" | https://api.whatsapp.com/send?phone=5511939408518 | 200 | ok |
| fep./onboarding-fep-exp/ | grupo WhatsApp "Entrar no canal de alunos" | https://chat.whatsapp.com/LlfatQyDLvl3ivCfjAfQPh?mode=gi_t | 200 | ok |
| fep./onboarding-fep-exp/ | formulário "Preencher o formulário" | https://docs.google.com/forms/d/e/1FAIpQLScQxZMdCkwjv5imVRVRh4tTYElVyHtjRKRr3E1acRdRJiLNdA/viewform | 401 | PROBLEMA: formulário Google exige login (401), aluno sem conta da organização não consegue abrir |
| fep./onboarding-fep-exp/ | Drive "Procure aqui sua foto" | https://drive.google.com/drive/u/2/folders/1ojQnyTvG7DQPR58PMnmtuyHcBrzeWCqh | 200 → https://drive.google.com/drive/folders/1ojQnyTvG7DQPR58PMnmtuyHcBrzeWCqh | ok |
| fep./onboarding-fep-exp/ | área de membros "Acessar área de membros" | https://hotmart.com/pt-br/club/formacao-especialista | 200 | ok |
| fep./onboarding-fep-exp/ | externo "Hospedagem parceira" | https://www.admilhasconsultoria.com.br/ | falha SSL (certificado expirado) | PROBLEMA: site parceiro com certificado SSL expirado (navegador mostra alerta) |
| fep./onboarding-fep-exp/ | vídeo YouTube | https://www.youtube.com/shorts/h2ytKMjqwXo | 200 (oEmbed): Onboarding FEPEXP | ok |
| joaopithon.com.br/fep-exp-obrigado/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/fep-exp-obrigado/ | checkout Hotmart "Acessar o link de Pré-Matrícula" | https://pay.hotmart.com/P93831788Q?off=5qywtk6m | 200 (navegador): FEP Experience [Pré-Matrícula], evento de 16 e 17/08/2025 no checkout | PROBLEMA: checkout de pré-matrícula ainda mostra evento de 16 e 17/08/2025 (WTC) |
| joaopithon.com.br/fep-experience-a/ | âncora/botão "GARANTA O SEU INGRESSO" | #ing | âncora | ok |
| joaopithon.com.br/fep-experience-a/ | formulário "GARANTA O SEU INGRESSO AQUI" | https://form.respondi.app/yhmbxvJI | 200 | ok |
| joaopithon.com.br/fep-experience-a/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=0IG6d41t3Xk | 200 (oEmbed): Dra. Livia | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=3gwQV_OQxbk&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=5 | 200 (oEmbed): Dra. Thais Viana | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=6Q9d6F3YRZA | 200 (oEmbed): Dra. Tatiana | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=EO6MR70GzRE | 200 (oEmbed): FEP EXPERIENCE 1 | PREENCHIMENTO FULL FACE - JULHO | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=KjGF-BjW4ng | 200 (oEmbed): Dra. Talita | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=LrRjAr50NoM&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=1&t=95s | 200 (oEmbed): Dra. Daniela Rosa | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=WrP5e8wyKT4&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=2 | 200 (oEmbed): Dra. Andrea Mitsugui | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=YaBZ_FUWqj0&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=4 | 200 (oEmbed): Dra. Fernanda Corsi | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=d_XAuz_yTqY | 200 (oEmbed): Dra. Layse Xavier | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=klb3TtL91TQ&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=3 | 200 (oEmbed): Dra. Rafaela Drummond | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=ms6NYDEFTdA | 200 (oEmbed): Dra. Duda | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=nkvB_XothXA | 200 (oEmbed): Dr. José Felipe | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=qcm7p3FKNcU | 200 (oEmbed): Dra. Isabela | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=tTh6IT03DCg | 200 (oEmbed): Dra. Michele | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://www.youtube.com/watch?v=woq15qLyTMs&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=6 | 200 (oEmbed): Dra. Laura Mazzini | FEP Experience | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://youtu.be/-OcOTkEfS34 | 200 (oEmbed): FEP EXPERIENCE 2 | PREENCHIMENTO FULL FACE - SETEM | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://youtube.com/shorts/8kolyT5vIMQ | 200 (oEmbed): Fep Exp | ok |
| joaopithon.com.br/fep-experience-a/ | vídeo YouTube | https://youtube.com/shorts/CajfchqCtz8 | 200 (oEmbed): Depoimento FEPEXP | ok |
| joaopithon.com.br/fep-experience-a/ | texto da página | (data visível) | n/a | PROBLEMA: anuncia "ÚLTIMOS INGRESSOS 11ª EDIÇÃO 17 e 18 de Outubro" (vencido; próxima é 28 e 29/11) |
| joaopithon.com.br/fep-experience/ | âncora/botão "GARANTA O SEU INGRESSO" | #ing | âncora | ok |
| joaopithon.com.br/fep-experience/ | formulário "GARANTA O SEU INGRESSO AQUI" | https://form.respondi.app/yhmbxvJI | 200 | ok |
| joaopithon.com.br/fep-experience/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=0IG6d41t3Xk | 200 (oEmbed): Dra. Livia | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=3gwQV_OQxbk&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=5 | 200 (oEmbed): Dra. Thais Viana | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=6Q9d6F3YRZA | 200 (oEmbed): Dra. Tatiana | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=EO6MR70GzRE | 200 (oEmbed): FEP EXPERIENCE 1 | PREENCHIMENTO FULL FACE - JULHO | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=KjGF-BjW4ng | 200 (oEmbed): Dra. Talita | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=LrRjAr50NoM&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=1&t=95s | 200 (oEmbed): Dra. Daniela Rosa | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=WrP5e8wyKT4&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=2 | 200 (oEmbed): Dra. Andrea Mitsugui | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=YaBZ_FUWqj0&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=4 | 200 (oEmbed): Dra. Fernanda Corsi | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=d_XAuz_yTqY | 200 (oEmbed): Dra. Layse Xavier | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=klb3TtL91TQ&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=3 | 200 (oEmbed): Dra. Rafaela Drummond | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=ms6NYDEFTdA | 200 (oEmbed): Dra. Duda | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=nkvB_XothXA | 200 (oEmbed): Dr. José Felipe | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=qcm7p3FKNcU | 200 (oEmbed): Dra. Isabela | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=tTh6IT03DCg | 200 (oEmbed): Dra. Michele | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://www.youtube.com/watch?v=woq15qLyTMs&list=PLKUDo0w3i0KBjDJ4YeMprqPlGbD20Kyq-&index=6 | 200 (oEmbed): Dra. Laura Mazzini | FEP Experience | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://youtu.be/-OcOTkEfS34 | 200 (oEmbed): FEP EXPERIENCE 2 | PREENCHIMENTO FULL FACE - SETEM | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://youtube.com/shorts/8kolyT5vIMQ | 200 (oEmbed): Fep Exp | ok |
| joaopithon.com.br/fep-experience/ | vídeo YouTube | https://youtube.com/shorts/CajfchqCtz8 | 200 (oEmbed): Depoimento FEPEXP | ok |
| joaopithon.com.br/fep-experience/ | texto da página | (data visível) | n/a | PROBLEMA: anuncia "ÚLTIMOS INGRESSOS 11ª EDIÇÃO 17 e 18 de Outubro" (vencido; próxima é 28 e 29/11) |
| joaopithon.com.br/onboarding-fep-exp/ | âncora/botão | #elementor-action%3Aaction%3Dlightbox%26settings%3DeyJ0eXBlIjoidmlkZW8iLCJ2aWRlb1R5cGUiOiJ5b3V0dWJlIiwidXJsIjoiaHR0cHM6XC9cL3d3dy55b3V0dWJlL | âncora | ok |
| joaopithon.com.br/onboarding-fep-exp/ | Drive "baixar o Manual" | https://drive.google.com/file/d/1r5WnHexafcqC0Cnlz85KD-NswjUjTybo/view | 200 | ok |
| joaopithon.com.br/onboarding-fep-exp/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/onboarding-fep-exp/ | Sendflow (grupo) "Entrar agora no Grupo" | https://sendflow.pro/i/fepexp | 200 → https://i.sendflow.pro/invite/fepexp | ok |
| joaopithon.com.br/onboarding-fep-exp/ | texto da página | (data visível) | n/a | PROBLEMA: "16 e 17 de Maio" e "16 E 18 DE MAIO" (vencido e inconsistente) |

### Masterclass em Intercorrências (MTI)

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| iff./mti-a/ | âncora/botão "QUERO MINHA VAGA NA AULA" | #oferta | âncora | ok |
| iff./mti-a/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| iff./mti-a/ | formulário | https://lucayhi.activehosted.com/f/embed.php?id=40 | 200 | ok |
| iff./mti-a/ | texto da página | (data visível) | n/a | ATENÇÃO: "14 DE SETEMBRO, ÀS 20H" (já passou) |
| iff./mti-checkin/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| iff./mti-checkin/ | Sendflow (grupo) "ENTRE PARA O GRUPO DO WHATSAPP" | https://sndflw.com/i/masterclass-em-intercorrencias-nov-26 | 200 | ATENÇÃO: campanha Sendflow hoje abre grupo "BLACK VITALÍCIA: REABERTURA RELÂMPAGO"; confirmar se é intencional |
| iff./mti-checkin/ | formulário | https://lucayhi.activehosted.com/f/embed.php?id=40 | 200 | ok |
| iff./mti-zoom/ | Zoom "ACESSAR SALA DE AULA" | https://joaopithon.com.br/aula-zoom | 200 → https://us06web.zoom.us/j/81923431173?pwd=iCwfQ58b7LoeHFijIHiGYVujz4ZkyG.1 | ok |
| iff./mti-zoom/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| iff./mti-zoom/ | WhatsApp "Preciso de ajuda para entrar" | https://wa.me/551151940346?text=Dr%20Jo%C3%A3o%20preciso%20de%20ajuda%20pra%20acessar%20a%20Sala%20do%20Zoom | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Dr+Jo%C3%A3o+preciso+de+ajuda+pra+acessar+a+Sala+do+Zoo | ok |
| iff./mti-zoom/ | formulário | https://lucayhi.activehosted.com/f/embed.php?id=40 | 200 | ok |
| iff./mti/ | âncora/botão "QUERO MINHA VAGA NA AULA" | #oferta | âncora | ok |
| iff./mti/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| iff./mti/ | formulário | https://lucayhi.activehosted.com/f/embed.php?id=40 | 200 | ok |
| iff./mti/ | texto da página | (data visível) | n/a | ATENÇÃO: "Terça, 17 de novembro, às 20h" (já passou) |

### Masterclass em Preenchimento Labial (MPL)

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| pl./live-zoom-mpl/ | Zoom "ACESSAR SALA DE AULA" | https://joaopithon.com.br/aula-zoom-2 | 200 → https://us06web.zoom.us/j/85866693966?pwd=oF0ZocPs9LUiE1NC9g3ZTQ32EG6zvO.1 | ok |
| pl./live-zoom-mpl/ | WhatsApp "Preciso de ajuda para entrar" | https://wa.me/551151940346?text=Dr%20Jo%C3%A3o%20preciso%20de%20ajuda%20pra%20acessar%20a%20Sala%20do%20Zoom | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Dr+Jo%C3%A3o+preciso+de+ajuda+pra+acessar+a+Sala+do+Zoo | ok |
| pl./pesquisa-mpl/ | Sendflow (grupo) "ENTRE PARA O GRUPO DO WHATSAPP" | https://sndflw.com/i/masterclass-em-preenchimento-labial-nov-26 | 200 → https://chat.whatsapp.com/DgnM0O9cgiwJ0ICrokJQlK | ATENÇÃO: leva ao grupo "BLACK VITALÍCIA: REABERTURA RELÂMPAGO #12"; confirmar se é intencional |

### Black Vitalícia

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| bf./black-vitalicia-obrigado-alunos/ | Sendflow (grupo) "ENTRE PARA O GRUPO DO WHATSAPP" | https://sndflw.com/i/bfv-26-alunos-fep | 200 → https://chat.whatsapp.com/HZZGjfexIpV2tCvp0VF3Bs | ok |
| bf./black-vitalicia-obrigado-alunos/ | Sendflow (grupo) "Resgatar meus presentes" | https://sndflw.com/i/drjoaopithon-blackfriday2025 | 200 | ok |
| bf./black-vitalicia-obrigado-alunos/ | texto da página | (data visível) | n/a | ATENÇÃO: "liberada apenas no dia 19 de Outubro" e "27 de Outubro" (já passou) |
| bf./black-vitalicia-obrigado/ | Sendflow (grupo) "Resgatar meus presentes" | https://sndflw.com/i/drjoaopithon-blackfriday2025 | 200 | ok |
| bf./black-vitalicia-obrigado/ | WhatsApp "ENTRE PARA O GRUPO DO WHATSAPP" | https://wa.me/551151940346?text=Quero%20acesso%20ao%20grupo%20da%20Black%20Friday%20Vital%C3%ADcia | 200 → https://api.whatsapp.com/send/?phone=551151940346&text=Quero+acesso+ao+grupo+da+Black+Friday+Vital%C3%ADcia&ty | ATENÇÃO: botão "ENTRE PARA O GRUPO" abre conversa com número, não grupo (a versão alunos usa Sendflow) |
| bf./black-vitalicia-obrigado/ | vídeo YouTube | https://youtu.be/dnQfv3SBqBA | 200 (oEmbed): live de abertura 20 de outubro | ok |
| bf./black-vitalicia-obrigado/ | texto da página | (data visível) | n/a | ATENÇÃO: "liberada apenas no dia 20 de Outubro" e "27 de Outubro" (já passou) |
| bf./lista-de-espera-bf/ | (nenhum link de ação) | n/a | página 200 | ok |
| bf./onboarding-bfv/ | WhatsApp "Preciso de ajuda" | https://api.whatsapp.com/send?phone=5511978511985 | 200 | ok |
| bf./onboarding-bfv/ | grupo WhatsApp "Entrar no Grupo VIP" | https://chat.whatsapp.com/LR0SRx8j38o4128Avs566k | 200 | ok |
| bf./onboarding-bfv/ | ajuda Hotmart "Como acessar a Área de Membros" | https://help.hotmart.com/pt-br/article/215827338/como-acessar-o-produto-que-comprei- | 200 | ok |
| bf./onboarding-bfv/ | área de membros "Área de Membros" | https://hotmart.com/pt-br/club/combo-vitalicio | 200 | ok |
| bf./verificacao-numeros/ | (nenhum link de ação) | n/a | página 200 | ok |

### Institucional / outros

| Página | Tipo de link | URL | Status | Problema |
|---|---|---|---|---|
| joaopithon.com.br/ | âncora/botão "Eventos presenciais" | #eve | âncora | ok |
| joaopithon.com.br/ | âncora/botão "Pós-Graduação" | #pos | âncora | ok |
| joaopithon.com.br/ | âncora/botão "Falar com o time" | #sup | âncora | ok |
| joaopithon.com.br/ | âncora/botão "Técnicas e protocolos" | #tec | âncora | ok |
| joaopithon.com.br/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/ | externo | https://www.instagram.com/drajessica.cardiopediatra/ | 429 → https://www.instagram.com/accounts/login/?next=https%3A%2F%2Fwww.instagram.com%2Fdrajessica.cardiopediatra%2F& | PROBLEMA GRAVE: rede social de outro perfil (não é do Dr. João) |
| joaopithon.com.br/ | externo | https://www.tiktok.com/@drajessicacardiopediatra | 200 | PROBLEMA GRAVE: rede social de outro perfil (não é do Dr. João) |
| joaopithon.com.br/ | vídeo YouTube | https://www.youtube.com/@drajessica.cardiopediatra | 404 (oEmbed):  | PROBLEMA GRAVE: rede social de outro perfil (não é do Dr. João) |
| joaopithon.com.br/ | página interna | https://ctx.joaopithon.com.br/curso-de-toxina-express/ | 200 | ok |
| joaopithon.com.br/ | página interna | https://eb.joaopithon.com.br/ebook-pto-h/ | 200 | ok |
| joaopithon.com.br/ | página interna | https://el.joaopithon.com.br/elite-injectors-congress/ | 200 | PROBLEMA: destino com edição encerrada (01 e 02/11, lote até 14/10); Elite 2027 está em lp/elite |
| joaopithon.com.br/ | página interna | https://iff.joaopithon.com.br/iff10/ | 200 | PROBLEMA: destino com evento encerrado (Imersão IFF10 de 15 e 16/09, ainda "COMEÇA HOJE") |
| joaopithon.com.br/ | página interna | https://joaopithon.com.br/fep-experience/ | 200 | ATENÇÃO: destino anuncia edição de 17 e 18/10 (já passou) |
| joaopithon.com.br/ | página interna | https://joaopithon.com.br/lista-espera-fep/ | 200 | ATENÇÃO: página de destino com CNPJ 42.342.917/0001-14, diferente do padrão 50.297.444/0001-09 |
| joaopithon.com.br/elementor-28131/ | âncora/botão "Ir para o conteúdo" | #content | âncora | ok |
| joaopithon.com.br/elementor-28131/ | página interna "João Pithon" | https://joaopithon.com.br/ | 200 | ok |
| joaopithon.com.br/elementor-28131/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/elementor-28131/ | Zoom "Entrar na reunião" | zoommtg://zoom.us/join?confno=82657687599 | protocolo app | ATENÇÃO: sala Zoom de junho/2026; conferir se ainda é usada |
| joaopithon.com.br/elementor-28131/ | Zoom | https://us06web.zoom.us/j/82657687599 | 200 | ATENÇÃO: sala Zoom de junho/2026; conferir se ainda é usada |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://feb.joaopithon.com.br/feb | 200 | ATENÇÃO: destino com bônus vencido (11/08) |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://joaopithon.com.br/cpx-bio | 200 → https://joaopithon.com.br/cpx/?utm_campaign=CPX&utm_source=IG_organico&utm_medium=ORG&utm_term=IG_organicos&ut | ok |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://joaopithon.com.br/fep-exp-bio | 200 → https://joaopithon.com.br/fep-experience/?utm_campaign=FEPEXP2025&utm_source=IG_organico&utm_medium=ORG_aplica | ATENÇÃO: leva à fep-experience com datas de 17 e 18/10 (UTM FEPEXP2025) |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://joaopithon.com.br/lista-espera-fep/ | 200 | ATENÇÃO: página de destino com CNPJ 42.342.917/0001-14, diferente do padrão 50.297.444/0001-09 |
| joaopithon.com.br/links-joao-pithon/ | página interna | https://joaopithon.com.br/pos-bio | 200 → https://pg.joaopithon.com.br/?utm_campaign=POS_MAI25&utm_source=IG_organico&utm_medium=ORG&utm_term=IG_organic | ATENÇÃO: leva à pg. com bônus vencidos (10/02 e 20/08) |
| joaopithon.com.br/politica-de-privacidade/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/redirecionar-whatsapp/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
| joaopithon.com.br/redirecionar-whatsapp/ | WhatsApp | https://wa.me/551151960668?text=Ol%C3%A1%20gostaria%20de%20ser%20paciente%20modelo | 200 → https://api.whatsapp.com/send/?phone=551151960668&text=Ol%C3%A1+gostaria+de+ser+paciente+modelo&type=phone_num | ok |
| joaopithon.com.br/termos-de-uso/ | página interna | https://joaopithon.com.br/comercial | 200 → https://api.whatsapp.com/send/?phone=5511966256272&text&type=phone_number&app_absent=0 | ok |
