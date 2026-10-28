// Captura das telas do Reology Map para o teaser (tema escuro, alta resolução).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const ROOT = '/tmp/claude-0/-home-user-FEA/570307b6-bb2f-5ff2-b02a-3f6fff2d3202/scratchpad';
const OUT = ROOT + '/cap';
const BASE = 'https://reology.joaopithon.com.br/';
const BRANDS = ['Belotero','Biogelis','Cutegel','e.p.t.q','Evofill','Finahfil','Hyafilia','Juvéderm','Milimetric PRO','Neauvia','Neuramis','Perfectha','Rennova','Restylane','Revanesse','Saypha','Singderm','Sofiderm','Stylage','Up','Yvoire'];
const BLUR = process.env.BLUR !== '0';

async function tidy(p) {
  await p.addStyleTag({ content: `
    a[href*="administracao"], [href*="/administracao"] { display:none !important; }
    nextjs-portal { display:none !important; }
    ${BLUR ? 'main img:not([src*="mapa-equipe"]):not([src*="reology"]) { filter: blur(9px) !important; }' : ''}
    *, *::before, *::after { scroll-behavior:auto !important; }
  ` });
  await p.evaluate(({ brands, blur }) => {
    // remove a faixa "Modo revisão interna" (só aparece para conta de equipe)
    for (const el of document.querySelectorAll('body *')) {
      if (el.children.length < 6 && /MODO REVISÃO INTERNA/i.test(el.innerText || '') && el.getBoundingClientRect().top < 60 && el.getBoundingClientRect().height < 80) {
        el.style.display = 'none';
      }
    }
    if (!blur) return;
    const set = new Set(brands.map(b => b.toLowerCase()));
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const hits = [];
    while (walker.nextNode()) {
      const t = walker.currentNode.nodeValue.trim().toLowerCase();
      if (!t) continue;
      const clean = t.replace(/^\d+\s*/, '');
      if (set.has(clean) || [...set].some(b => t === b + ' ·' || t.startsWith(b + ' · lote'))) hits.push(walker.currentNode.parentElement);
    }
    for (const el of hits) { el.style.filter = 'blur(5px)'; }
    // marca em imagens de caixa de produto
  }, { brands: BRANDS, blur: BLUR });
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const desk = await b.newContext({ storageState: ROOT + '/browser/state.json', viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2 });
  await desk.addInitScript(() => { try { localStorage.setItem('reology-theme', 'dark'); } catch (e) {} });
  const p = await desk.newPage();
  const go = async (u) => { await p.goto(BASE + u, { waitUntil: 'networkidle', timeout: 90000 }); await p.waitForTimeout(1800); await tidy(p); await p.waitForTimeout(400); };
  const shot = async (n, full) => { await p.screenshot({ path: `${OUT}/${n}.png`, fullPage: !!full }); console.log('ok', n); };

  // Login (tagline do app)
  const anon = await b.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2 });
  await anon.addInitScript(() => { try { localStorage.setItem('reology-theme', 'dark'); } catch (e) {} });
  const pa = await anon.newPage();
  await pa.goto(BASE + 'login', { waitUntil: 'networkidle' }); await pa.waitForTimeout(1500);
  await pa.screenshot({ path: `${OUT}/00-login.png` }); console.log('ok 00-login');

  // Regiões (mapa facial)
  await go('');
  await shot('01-regioes');
  await shot('01-regioes-full', true);
  const face = await p.locator('button[aria-label="Mapa: 1. Lábio"]').boundingBox();
  console.log('labio', JSON.stringify(face));
  for (const [i, r] of [['a', '1. Lábio'], ['b', '8. Arco zigomático'], ['c', '16. Nariz']]) {
    await p.locator(`button[aria-label="Mapa: ${r}"]`).click(); await p.waitForTimeout(900); await tidy(p);
    await shot('02-regiao-click-' + i);
  }
  await go('regioes/labios');
  await shot('03-regiao-labios-full', true);

  // Produtos
  await go('produtos');
  await shot('04-produtos');
  await shot('04-produtos-full', true);
  await p.locator('input[type=search], input[placeholder*="Termo"], main input').first().fill('lábio').catch(() => {});
  await p.waitForTimeout(1500); await tidy(p);
  await shot('05-produtos-busca');

  // Ficha
  await go('produtos/juvederm-volbella-lido');
  await shot('06-ficha');
  await shot('06-ficha-full', true);
  for (const f of ['0,1 Hz', '5 Hz']) {
    await p.getByRole('button', { name: f, exact: true }).first().click().catch(e => console.log('freq', f, e.message.split('\n')[0]));
    await p.waitForTimeout(900); await tidy(p);
    await shot('07-ficha-' + f.replace(/[ ,]/g, ''), true);
  }

  // Mapa da Reologia
  await go('mapa-da-reologia');
  await shot('08-mapa');
  await shot('08-mapa-full', true);

  // Comparador
  await go('comparador?produto=juvederm-volbella-lido&produto=juvederm-voluma-lido&produto=restylane-kysse-lido');
  await shot('09-comparador');
  await shot('09-comparador-full', true);

  // Biblioteca
  await go('biblioteca');
  await shot('10-biblioteca');
  await shot('10-biblioteca-full', true);

  // Mobile
  const mob = await b.newContext({ storageState: ROOT + '/browser/state.json', viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  await mob.addInitScript(() => { try { localStorage.setItem('reology-theme', 'dark'); } catch (e) {} });
  const m = await mob.newPage();
  for (const [n, u] of [['11-mob-regioes', ''], ['12-mob-produtos', 'produtos'], ['13-mob-ficha', 'produtos/juvederm-volbella-lido'], ['14-mob-comparador', 'comparador?produto=juvederm-volbella-lido&produto=juvederm-voluma-lido']]) {
    await m.goto(BASE + u, { waitUntil: 'networkidle', timeout: 90000 }); await m.waitForTimeout(1800); await tidy(m);
    await m.screenshot({ path: `${OUT}/${n}.png` }); await m.screenshot({ path: `${OUT}/${n}-full.png`, fullPage: true }); console.log('ok', n);
  }

  // Logo
  const logo = await p.$$eval('img', is => is.map(i => i.currentSrc || i.src).filter(s => /reology/i.test(s)));
  console.log('logo', JSON.stringify(logo));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
