#!/usr/bin/env node
/*
 * fea_revisar_pagina.js · varredura automática de uma página da FEA (parte técnica do revisor)
 *
 * Uso:
 *   node fea_revisar_pagina.js <URL> [pasta-de-saida] [--latam] [--sem-links]
 *
 *   <URL>             página a revisar (prévia de branch, workers.dev, localhost ou no ar)
 *   [pasta-de-saida]  onde salvar prints e relatório (padrão: $FEA_SCRATCH ou /tmp/fea-revisor/<data>)
 *   --latam           página em espanhol: procura termos de boleto/pix e português esquecido
 *   --sem-links       não testa o status HTTP dos links (mais rápido)
 *
 * O que faz (só leitura, não clica em checkout nem envia formulário):
 *   1. Abre a página em 390 px (celular, tela 2x) e 1440 px (computador), rola até o fim para
 *      carregar o lazy e tira print de página inteira e da primeira dobra em cada largura.
 *   2. Detecta rolagem lateral no celular e lista os elementos que passam da borda.
 *   3. Lista imagens quebradas, sem alt, sem width/height e pesadas (> 300 KB).
 *   4. Registra erros de console, erros de página e pedidos que falharam.
 *   5. Lista todos os links e botões com destino e status HTTP (Hotmart, WhatsApp, Sendflow, Zoom...),
 *      href vazio ou "#", âncora sem alvo, target=_blank sem rel=noopener, checkout sem off=.
 *   6. Varre o texto visível: travessão (— e –), "pra ", marcas de toxina/AH/bioestimulador,
 *      palavras-tell, "Dr. João" sem "Pithon", números antigos de alunos, "R$" separado do número,
 *      promessa de resultado e urgência suspeita.
 *   7. Confere SEO e rastreamento: title, description, og:image, canonical, robots, lang, h1,
 *      GTM, VK e Clarity.
 *
 * Saída: <pasta>/relatorio.json, <pasta>/relatorio.md e os PNG. Código de saída 0 sempre;
 * o resumo final diz quantos BLOQUEIOS, ALERTAS e AVISOS foram encontrados.
 *
 * Requer Node + Playwright (require('playwright') já funciona no ambiente do agente).
 */

const fs = require('fs');
const path = require('path');
const { chromium, request } = require('playwright');

const args = process.argv.slice(2);
const URL_ALVO = args.find((a) => /^https?:\/\//.test(a));
const LATAM = args.includes('--latam');
const SEM_LINKS = args.includes('--sem-links');
const pastaArg = args.find((a) => a !== URL_ALVO && !a.startsWith('--'));

if (!URL_ALVO) {
  console.error('Uso: node fea_revisar_pagina.js <URL> [pasta-de-saida] [--latam] [--sem-links]');
  process.exit(1);
}

const carimbo = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const PASTA =
  pastaArg ||
  path.join(process.env.FEA_SCRATCH || '/tmp/fea-revisor', `${carimbo}-${new URL(URL_ALVO).pathname.replace(/\W+/g, '_') || 'raiz'}`);
fs.mkdirSync(PASTA, { recursive: true });

// ---------------------------------------------------------------- regras de texto
// Marcas que a linha vermelha 3 proíbe sem aprovação (toxina, ácido hialurônico, bioestimulador).
const MARCAS = [
  'Botox', 'Xeomin', 'Dysport', 'Letybo', 'Botulift', 'Prosigne', 'Nabota', 'Relatox', 'Daxxify', 'Jeuveau',
  'Juvederm', 'Juvéderm', 'Restylane', 'Belotero', 'Rennova', 'Perfectha', 'Stylage', 'Teosyal', 'Saypha',
  'Yvoire', 'Neuramis', 'Revanesse', 'Sculptra', 'Radiesse', 'Ellansé', 'Ellanse', 'Elleva', 'Harmonyca', 'Profhilo',
];
// Uso aprovado: o nome do produto FEB contém "Botox".
const MARCAS_PERMITIDAS = [/Especialista em Botox/i, /Especialista en Botox/i];

const PALAVRAS_TELL = ['sinceramente', 'honestamente', 'basicamente', 'simplesmente', 'na verdade'];
const PROMESSA = [/resultado garantido/i, /garantimos (o )?resultado/i, /sem nenhum risco/i, /é fácil/i, /qualquer um (faz|consegue)/i, /100% seguro/i, /risco zero/i];
const URGENCIA = [/últimas? vagas?/i, /só hoje/i, /corra/i, /última chance/i, /acaba (hoje|em)/i, /vagas? limitadas?/i];
const NUMEROS_ANTIGOS = [/\b35 mil\b/i, /\+?\s?35\.000\b/, /\b30\.000 alunos/i, /\b20\.000 alunos/i, /\b10\.000 alunos/i, /\b19 países/i, /\b9 países/i, /quase 100%/i];
const BOLETO_PIX = [/boleto/i, /\bpix\b/i, /pago pendiente/i, /pago vencido/i];
const PT_EM_PAGINA_ES = [/\bvocê\b/i, /\bpara você\b/i, /\bnão\b/i, /\bInscreva/i, /\bQuero\b/];

// ---------------------------------------------------------------- achados
const achados = [];
// nivel: BLOQUEIO (reprova sozinho) · ALERTA (corrigir antes de entregar) · AVISO (conferir)
function achado(nivel, categoria, mensagem, detalhe) {
  achados.push({ nivel, categoria, mensagem, detalhe: detalhe || null });
}

function contexto(texto, indice, raio = 50) {
  return texto.slice(Math.max(0, indice - raio), indice + raio).replace(/\s+/g, ' ').trim();
}

async function rolarAteOFim(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let y = 0;
      const passo = Math.max(300, Math.floor(window.innerHeight * 0.8));
      const t = setInterval(() => {
        window.scrollBy(0, passo);
        y += passo;
        if (y >= document.documentElement.scrollHeight + passo) {
          clearInterval(t);
          window.scrollTo(0, 0);
          resolve();
        }
      }, 120);
    });
  });
  await page.waitForTimeout(1200);
}

// Domínios de terceiros bloqueados na varredura (não gera evento, lead nem visita falsa).
const BLOQUEAR = [/googletagmanager\.com/, /google-analytics\.com/, /clarity\.ms/, /facebook\.net/, /connect\.facebook/, /vk\.com|vkontakte|pixel\.vk/, /activehosted\.com\/proc\.php/, /doubleclick/];

async function abrir(browser, largura, altura, escala, rotulo) {
  const context = await browser.newContext({
    viewport: { width: largura, height: altura },
    deviceScaleFactor: escala,
    isMobile: largura < 800,
    hasTouch: largura < 800,
    userAgent:
      largura < 800
        ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
        : undefined,
    locale: LATAM ? 'es-CO' : 'pt-BR',
  });
  const page = await context.newPage();
  const consoleErros = [];
  const pedidosFalhos = [];
  page.on('console', (m) => {
    if (m.type() === 'error') consoleErros.push(m.text().slice(0, 300));
  });
  page.on('pageerror', (e) => consoleErros.push('pageerror: ' + String(e.message || e).slice(0, 300)));
  page.on('requestfailed', (r) => {
    const u = r.url();
    if (BLOQUEAR.some((rx) => rx.test(u))) return;
    pedidosFalhos.push(`${r.failure() ? r.failure().errorText : 'falha'} ${u.slice(0, 200)}`);
  });
  page.on('response', (r) => {
    const s = r.status();
    if (s >= 400 && !BLOQUEAR.some((rx) => rx.test(r.url()))) pedidosFalhos.push(`HTTP ${s} ${r.url().slice(0, 200)}`);
  });
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (BLOQUEAR.some((rx) => rx.test(u))) return route.abort();
    return route.continue();
  });
  const resp = await page.goto(URL_ALVO, { waitUntil: 'domcontentloaded', timeout: 60000 });
  try {
    await page.waitForLoadState('networkidle', { timeout: 15000 });
  } catch (_) {}
  await rolarAteOFim(page);
  await page.screenshot({ path: path.join(PASTA, `${rotulo}-primeira-dobra.png`) });
  await page.screenshot({ path: path.join(PASTA, `${rotulo}-inteira.png`), fullPage: true });
  return { context, page, status: resp ? resp.status() : null, consoleErros, pedidosFalhos };
}

(async () => {
  const browser = await chromium.launch();
  const relatorio = { url: URL_ALVO, quando: new Date().toISOString(), latam: LATAM, pasta: PASTA };

  // ------------------------------------------------------------ celular 390
  const cel = await abrir(browser, 390, 844, 2, 'celular-390');
  relatorio.status = cel.status;
  if (cel.status !== 200) achado('BLOQUEIO', 'técnico', `A página respondeu ${cel.status}, não 200`);

  const medidaCel = await cel.page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const sw = document.documentElement.scrollWidth;
    const fora = [];
    document.querySelectorAll('body *').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed' && r.right > vw + 1) return fora.push({ el: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''), direita: Math.round(r.right) });
      if (r.right > vw + 1 || r.left < -1) {
        // ignora quem está dentro de um contêiner que corta (carrossel com overflow hidden/auto)
        let p = el.parentElement;
        let cortado = false;
        while (p && p !== document.body) {
          const pc = getComputedStyle(p);
          if (/(hidden|auto|scroll|clip)/.test(pc.overflowX)) { cortado = true; break; }
          p = p.parentElement;
        }
        if (!cortado) fora.push({ el: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''), esquerda: Math.round(r.left), direita: Math.round(r.right) });
      }
    });
    // textos pequenos demais no celular
    const pequenos = [];
    document.querySelectorAll('p, li, span, a, button, label, small').forEach((el) => {
      if (!el.childNodes.length || !el.innerText || !el.innerText.trim()) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0) return;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs < 11) pequenos.push(`${fs}px: ${el.innerText.trim().slice(0, 60)}`);
    });
    // botões com área de toque pequena
    const toque = [];
    document.querySelectorAll('a[href], button').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      const t = (el.innerText || el.getAttribute('aria-label') || '').trim();
      if (t && r.height < 40 && /quero|garant|compr|inscre|aplic|acessar|entrar|baixar|participar|agendar|liberar/i.test(t)) toque.push(`${Math.round(r.width)}x${Math.round(r.height)}: ${t.slice(0, 50)}`);
    });
    return { vw, sw, fora: fora.slice(0, 25), pequenos: [...new Set(pequenos)].slice(0, 20), toque: toque.slice(0, 20), altura: document.documentElement.scrollHeight };
  });
  relatorio.celular = medidaCel;
  if (medidaCel.sw > medidaCel.vw + 1) achado('ALERTA', 'visual', `Rolagem lateral no celular: página com ${medidaCel.sw}px numa tela de ${medidaCel.vw}px`, medidaCel.fora);
  else if (medidaCel.fora.length) achado('AVISO', 'visual', 'Elementos passam da borda no celular (sem gerar rolagem, conferir no print)', medidaCel.fora);
  if (medidaCel.pequenos.length) achado('AVISO', 'visual', 'Textos com menos de 11px no celular', medidaCel.pequenos);
  if (medidaCel.toque.length) achado('ALERTA', 'visual', 'Botões de ação com menos de 40px de altura no celular', medidaCel.toque);

  // ------------------------------------------------------------ computador 1440
  const desk = await abrir(browser, 1440, 900, 1, 'computador-1440');
  const medidaDesk = await desk.page.evaluate(() => ({ vw: document.documentElement.clientWidth, sw: document.documentElement.scrollWidth, altura: document.documentElement.scrollHeight }));
  relatorio.computador = medidaDesk;
  if (medidaDesk.sw > medidaDesk.vw + 1) achado('ALERTA', 'visual', `Rolagem lateral no computador: ${medidaDesk.sw}px em ${medidaDesk.vw}px`);

  // ------------------------------------------------------------ erros de console e rede
  const erros = [...new Set([...cel.consoleErros, ...desk.consoleErros])];
  const falhas = [...new Set([...cel.pedidosFalhos, ...desk.pedidosFalhos])];
  relatorio.console = erros;
  relatorio.pedidosFalhos = falhas;
  if (erros.length) achado('ALERTA', 'técnico', `${erros.length} erro(s) de console`, erros.slice(0, 15));
  if (falhas.length) achado('ALERTA', 'técnico', `${falhas.length} pedido(s) que falharam (imagem, fonte, script)`, falhas.slice(0, 15));

  // ------------------------------------------------------------ dados da página (celular)
  const dados = await cel.page.evaluate(() => {
    const meta = (sel) => (document.querySelector(sel) ? document.querySelector(sel).getAttribute('content') : null);
    const html = document.documentElement.outerHTML;
    const imgs = [...document.images].map((i) => ({
      src: i.currentSrc || i.src,
      alt: i.getAttribute('alt'),
      larguraNatural: i.naturalWidth,
      completa: i.complete,
      temDimensao: i.hasAttribute('width') && i.hasAttribute('height'),
      visivel: i.getBoundingClientRect().width > 0,
    }));
    const links = [...document.querySelectorAll('a, button, [role=button], [data-href]')].map((el) => ({
      tag: el.tagName.toLowerCase(),
      texto: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').replace(/\s+/g, ' ').trim().slice(0, 80),
      href: el.getAttribute('href') || el.getAttribute('data-href'),
      hrefAbs: el.href || null,
      target: el.getAttribute('target'),
      rel: el.getAttribute('rel'),
      visivel: el.getBoundingClientRect().width > 0 && getComputedStyle(el).visibility !== 'hidden',
    }));
    const ids = new Set([...document.querySelectorAll('[id]')].map((e) => e.id));
    return {
      titulo: document.title,
      descricao: meta('meta[name="description"]'),
      ogImage: meta('meta[property="og:image"]'),
      ogTitulo: meta('meta[property="og:title"]'),
      canonical: document.querySelector('link[rel=canonical]') ? document.querySelector('link[rel=canonical]').href : null,
      robots: meta('meta[name="robots"]'),
      lang: document.documentElement.lang,
      h1: [...document.querySelectorAll('h1')].map((h) => h.innerText.trim().slice(0, 120)),
      gtm: /GTM-[A-Z0-9]+/.exec(html) ? /GTM-[A-Z0-9]+/.exec(html)[0] : null,
      vk: /pixel\.js|sales_pixel\.js|event_pageview\.js/.test(html),
      clarity: /clarity/.test(html),
      textoVisivel: document.body.innerText,
      imgs,
      links,
      ids: [...ids],
    };
  });
  relatorio.seo = {
    titulo: dados.titulo, descricao: dados.descricao, ogImage: dados.ogImage, ogTitulo: dados.ogTitulo,
    canonical: dados.canonical, robots: dados.robots, lang: dados.lang, h1: dados.h1,
    gtm: dados.gtm, vk: dados.vk, clarity: dados.clarity,
  };

  // SEO básico
  if (!dados.titulo) achado('ALERTA', 'técnico', 'Página sem <title>');
  if (dados.titulo && /[—–]/.test(dados.titulo)) achado('ALERTA', 'copy', 'Travessão no <title>', dados.titulo);
  if (!dados.descricao) achado('AVISO', 'técnico', 'Sem meta description');
  if (!dados.ogImage) achado('ALERTA', 'técnico', 'Sem og:image (link compartilhado no WhatsApp sai sem imagem)');
  if (!dados.canonical) achado('AVISO', 'técnico', 'Sem canonical');
  if (dados.h1.length !== 1) achado('AVISO', 'técnico', `A página tem ${dados.h1.length} h1 (o ideal é 1)`, dados.h1);
  if (LATAM && dados.lang && !/^es/i.test(dados.lang)) achado('ALERTA', 'latam', `Página Latam com lang="${dados.lang}" (esperado es)`);
  if (!LATAM && dados.lang && !/^pt/i.test(dados.lang)) achado('AVISO', 'técnico', `lang="${dados.lang}"`);
  if (!dados.gtm) achado('ALERTA', 'rastreamento', 'GTM não encontrado no HTML');
  if (!dados.vk) achado('AVISO', 'rastreamento', 'Pixel da VK não encontrado (confirmar se a sala usa)');
  if (!dados.clarity) achado('AVISO', 'rastreamento', 'Clarity não encontrado (confirmar se a sala usa)');
  if (/workers\.dev|localhost/.test(dados.canonical || '')) achado('AVISO', 'técnico', 'Canonical aponta para a prévia, não para o domínio final', dados.canonical);

  // imagens
  const quebradas = dados.imgs.filter((i) => i.completa && i.larguraNatural === 0 && i.src);
  const semAlt = dados.imgs.filter((i) => i.alt === null);
  const semDim = dados.imgs.filter((i) => !i.temDimensao && i.visivel);
  if (quebradas.length) achado('BLOQUEIO', 'visual', `${quebradas.length} imagem(ns) quebrada(s)`, quebradas.map((i) => i.src));
  if (semAlt.length) achado('AVISO', 'técnico', `${semAlt.length} imagem(ns) sem atributo alt`, semAlt.map((i) => i.src).slice(0, 10));
  if (semDim.length) achado('AVISO', 'técnico', `${semDim.length} imagem(ns) sem width/height (risco de a página pular ao carregar)`, semDim.map((i) => i.src).slice(0, 10));

  // peso das imagens
  const api = await request.newContext({ ignoreHTTPSErrors: false });
  const pesadas = [];
  for (const src of [...new Set(dados.imgs.map((i) => i.src).filter((s) => /^https?:/.test(s)))].slice(0, 60)) {
    try {
      const r = await api.fetch(src, { method: 'GET', timeout: 20000 });
      const b = (await r.body()).length;
      if (b > 300 * 1024) pesadas.push(`${Math.round(b / 1024)} KB ${src}`);
    } catch (_) {}
  }
  if (pesadas.length) achado('AVISO', 'técnico', 'Imagens com mais de 300 KB', pesadas);

  // ------------------------------------------------------------ texto visível
  const texto = dados.textoVisivel;
  const ocorrencias = (rx, nivel, categoria, msg) => {
    const lista = [];
    let m;
    const g = new RegExp(rx.source, rx.flags.includes('g') ? rx.flags : rx.flags + 'g');
    while ((m = g.exec(texto)) && lista.length < 12) lista.push(contexto(texto, m.index));
    if (lista.length) achado(nivel, categoria, msg, lista);
  };
  ocorrencias(/—/, 'ALERTA', 'copy', 'Travessão (—) no texto visível');
  ocorrencias(/ – /, 'ALERTA', 'copy', 'Meia-risca usada como travessão ( – ) no texto visível');
  ocorrencias(/\bpra\b/i, 'ALERTA', 'copy', '"pra" no texto (sempre "para")');
  ocorrencias(/R\$ (?=\d)/, 'AVISO', 'visual', '"R$" com espaço comum antes do número (pode quebrar a linha: usar espaço que não quebra)');
  ocorrencias(/Dr\.? João(?! Pithon)/, 'AVISO', 'copy', '"Dr. João" sem "Pithon" (pedido do Luca: sempre "Dr. João Pithon")');
  PALAVRAS_TELL.forEach((p) => ocorrencias(new RegExp(`\\b${p}\\b`, 'i'), 'AVISO', 'copy', `Palavra-tell: "${p}"`));
  NUMEROS_ANTIGOS.forEach((rx) => ocorrencias(rx, 'ALERTA', 'prova social', `Número antigo de prova social (${rx.source}); padrão atual: 52.754 alunos, 44 países`));
  PROMESSA.forEach((rx) => ocorrencias(rx, 'BLOQUEIO', 'linha vermelha', `Possível promessa de resultado ou risco minimizado (${rx.source})`));
  URGENCIA.forEach((rx) => ocorrencias(rx, 'AVISO', 'copy', `Urgência: confirmar se é real (${rx.source})`));
  MARCAS.forEach((marca) => {
    const g = new RegExp(`\\b${marca}\\b`, 'gi');
    const lista = [];
    let m;
    while ((m = g.exec(texto)) && lista.length < 8) {
      const ctx = contexto(texto, m.index, 40);
      if (!MARCAS_PERMITIDAS.some((rx) => rx.test(ctx))) lista.push(ctx);
    }
    if (lista.length) achado('BLOQUEIO', 'linha vermelha', `Marca comercial "${marca}" no texto (linha vermelha 3: só com aprovação)`, lista);
  });
  if (/52[.\s]?754/.test(texto)) relatorio.numeroAlunos = '52.754 presente';
  const datas = texto.match(/\b\d{1,2} de (janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b/gi);
  if (datas) achado('AVISO', 'copy', 'Datas no texto: conferir se nenhuma já passou e se batem com o briefing', [...new Set(datas)]);
  if (LATAM) {
    BOLETO_PIX.forEach((rx) => ocorrencias(rx, 'BLOQUEIO', 'latam', `Página Latam com termo de pagamento brasileiro (${rx.source})`));
    PT_EM_PAGINA_ES.forEach((rx) => ocorrencias(rx, 'ALERTA', 'latam', `Possível português na página em espanhol (${rx.source})`));
  }

  // ------------------------------------------------------------ links e botões
  const vistos = new Map();
  const linhasLinks = [];
  for (const l of dados.links) {
    const href = l.href;
    const rotulo = l.texto || '(sem texto)';
    if (l.tag !== 'a' && !href) continue; // botão de interface (play, acordeão, carrossel)
    if (href === null || href === '' || href === '#') {
      if (l.visivel) achado('BLOQUEIO', 'cta', `Botão/link sem destino (href ${href === null ? 'ausente' : '"' + href + '"'}): "${rotulo}"`);
      continue;
    }
    if (href.startsWith('#')) {
      if (!dados.ids.includes(href.slice(1))) achado('ALERTA', 'cta', `Âncora sem alvo na página: ${href} ("${rotulo}"). Se abre popup por script, clicar e conferir; se não, o botão não faz nada`);
      continue;
    }
    if (/^(mailto|tel):/.test(href)) continue;
    if (/^javascript:/i.test(href)) { achado('ALERTA', 'cta', `Link javascript: "${rotulo}"`); continue; }
    const abs = l.hrefAbs;
    if (!abs || !/^https?:/.test(abs)) { achado('ALERTA', 'cta', `Link inválido: ${href} ("${rotulo}")`); continue; }
    if (l.target === '_blank' && !/noopener|noreferrer/.test(l.rel || '')) achado('AVISO', 'técnico', `target=_blank sem rel=noopener: ${abs.slice(0, 120)}`);
    if (/%20|Quero%20falar/i.test(new URL(abs).hostname)) achado('BLOQUEIO', 'cta', `Link quebrado (texto no lugar da URL): "${rotulo}"`, abs);
    if (/pay\.hotmart\.com/.test(abs) && !/[?&]off=/.test(abs)) achado('ALERTA', 'cta', `Checkout Hotmart sem off= (oferta não definida): "${rotulo}"`, abs);
    if (/(wa\.me|api\.whatsapp\.com)/.test(abs)) {
      const msg = decodeURIComponent((abs.split('text=')[1] || '').replace(/\+/g, ' '));
      if (/\bpra\b/i.test(msg)) achado('ALERTA', 'copy', `Mensagem pronta do WhatsApp com "pra": "${msg.slice(0, 100)}"`);
    }
    if (/workers\.dev|localhost/.test(abs) && !abs.startsWith(new URL(URL_ALVO).origin)) achado('ALERTA', 'cta', `Link aponta para uma prévia: ${abs}`);
    linhasLinks.push({ texto: rotulo, url: abs, visivel: l.visivel });
    if (!vistos.has(abs)) vistos.set(abs, null);
  }

  if (!SEM_LINKS) {
    for (const u of vistos.keys()) {
      if (/googletagmanager|clarity|facebook\.net/.test(u)) continue;
      try {
        const opcoes = { method: 'GET', maxRedirects: 8, timeout: 25000, headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36' } };
        let r = await api.fetch(u, opcoes);
        if (r.status() >= 500) { await new Promise((ok) => setTimeout(ok, 3000)); r = await api.fetch(u, opcoes); } // 5xx pode ser instabilidade: 2ª tentativa
        let final = r.url();
        let obs = '';
        if (/pay\.hotmart\.com\/error/.test(final)) obs = 'checkout com erro na Hotmart (vendas encerradas ou oferta inválida)';
        if (/hotmart/.test(u) && r.status() === 403) obs = 'Hotmart bloqueia robôs: abrir no navegador para conferir';
        vistos.set(u, { status: r.status(), final, obs });
        if (r.status() >= 400 && !(r.status() === 403 && /hotmart|instagram|facebook/.test(u))) achado('BLOQUEIO', 'cta', `Link com status ${r.status()}: ${u}`);
        if (obs.startsWith('checkout com erro')) achado('BLOQUEIO', 'cta', `Checkout abre erro na Hotmart: ${u}`, final);
      } catch (e) {
        vistos.set(u, { status: 'erro', final: null, obs: String(e.message).slice(0, 120) });
        achado('ALERTA', 'cta', `Link não respondeu: ${u}`, String(e.message).slice(0, 120));
      }
    }
  }
  relatorio.links = linhasLinks.map((l) => ({ ...l, ...(vistos.get(l.url) || {}) }));

  // Coerência de CTA: botões de compra com destinos diferentes
  const checkouts = [...new Set(linhasLinks.filter((l) => /pay\.hotmart\.com/.test(l.url)).map((l) => l.url.replace(/([?&])(utm_[^&]+|sck=[^&]+|src=[^&]+|xcod=[^&]+)/g, '$1').replace(/[?&]+$/, '')))];
  relatorio.checkouts = checkouts;
  if (checkouts.length > 1) achado('AVISO', 'cta', 'Mais de um checkout na página: conferir se é intencional (perfis, lotes, Brasil e Latam)', checkouts);

  await browser.close();
  await api.dispose();

  // ------------------------------------------------------------ saída
  const conta = (n) => achados.filter((a) => a.nivel === n).length;
  relatorio.resumo = { bloqueios: conta('BLOQUEIO'), alertas: conta('ALERTA'), avisos: conta('AVISO') };
  relatorio.achados = achados;
  fs.writeFileSync(path.join(PASTA, 'relatorio.json'), JSON.stringify(relatorio, null, 2));

  const md = [];
  md.push(`# Varredura FEA · ${URL_ALVO}`, '', `Quando: ${relatorio.quando} · status ${relatorio.status} · ${LATAM ? 'Latam' : 'Brasil'}`, '');
  md.push(`**Resumo:** ${relatorio.resumo.bloqueios} bloqueio(s) · ${relatorio.resumo.alertas} alerta(s) · ${relatorio.resumo.avisos} aviso(s)`, '');
  md.push(`Celular 390: largura ${medidaCel.sw}/${medidaCel.vw}px, altura ${medidaCel.altura}px · Computador 1440: largura ${medidaDesk.sw}/${medidaDesk.vw}px, altura ${medidaDesk.altura}px`, '');
  md.push('## Achados', '');
  for (const n of ['BLOQUEIO', 'ALERTA', 'AVISO']) {
    for (const a of achados.filter((x) => x.nivel === n)) {
      md.push(`- **${a.nivel}** [${a.categoria}] ${a.mensagem}`);
      if (a.detalhe) (Array.isArray(a.detalhe) ? a.detalhe : [a.detalhe]).slice(0, 8).forEach((d) => md.push(`  - ${typeof d === 'string' ? d : JSON.stringify(d)}`));
    }
  }
  md.push('', '## SEO e rastreamento', '', '```', JSON.stringify(relatorio.seo, null, 2), '```', '');
  md.push('## Links e botões', '', '| Texto | Destino | Status | Obs. |', '|---|---|---|---|');
  for (const l of relatorio.links) md.push(`| ${l.texto.replace(/\|/g, '/')} | ${l.url.slice(0, 110)} | ${l.status ?? ''} | ${l.obs || ''} |`);
  md.push('', '## Prints', '', ...fs.readdirSync(PASTA).filter((f) => f.endsWith('.png')).map((f) => `- ${path.join(PASTA, f)}`));
  fs.writeFileSync(path.join(PASTA, 'relatorio.md'), md.join('\n'));

  console.log(md.slice(0, 6).join('\n'));
  for (const a of achados) console.log(`${a.nivel.padEnd(8)} [${a.categoria}] ${a.mensagem}`);
  console.log(`\nRelatório: ${path.join(PASTA, 'relatorio.md')}`);
})().catch((e) => {
  console.error('Falha na varredura:', e);
  process.exit(2);
});
