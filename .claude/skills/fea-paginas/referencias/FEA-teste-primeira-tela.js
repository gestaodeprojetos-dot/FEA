// Mede se o botão principal aparece na primeira tela em vários aparelhos e tira prints.
// Uso: node FEA-teste-primeira-tela.js "https://feb.joaopithon.com.br/mtb/" "CONFIRMAR"
// (2º argumento: trecho do texto do botão principal)
const { chromium, devices } = require('playwright');
const url = process.argv[2];
const textoBotao = new RegExp(process.argv[3] || 'CONFIRMAR', 'i');
const aparelhos = [
  ['iPhone 13', devices['iPhone 13']], ['iPhone SE', devices['iPhone SE']],
  ['Galaxy S9+', devices['Galaxy S9+']], ['Galaxy S24', devices['Galaxy S24'] || devices['Galaxy S9+']],
  ['Pixel 7', devices['Pixel 7']], ['Desktop', { viewport: { width: 1366, height: 768 } }],
];
(async () => {
  const b = await chromium.launch();
  for (const [nome, dev] of aparelhos) {
    const ctx = await b.newContext({ ...dev }); const p = await ctx.newPage();
    await p.goto(url + (url.includes('?') ? '&' : '?') + 'utm_source=teste&nc=' + Date.now(), { waitUntil: 'load', timeout: 60000 });
    await p.waitForTimeout(2500);
    await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
    const r = await p.evaluate((src) => {
      const re = new RegExp(src, 'i');
      const btn = [...document.querySelectorAll('button, a')].find(x => re.test(x.textContent) && x.offsetParent);
      const rb = btn && btn.getBoundingClientRect();
      return { alturaVisivel: innerHeight, fimDoBotao: rb && Math.round(rb.bottom + scrollY), botaoNaPrimeiraTela: rb ? rb.bottom + scrollY <= innerHeight : null,
        utmCapturada: document.querySelector('[name="form_fields[utm_source]"]')?.value || null };
    }, textoBotao.source);
    console.log(nome.padEnd(12), JSON.stringify(r));
    await p.screenshot({ path: `FEA-print-${nome.replace(/\W+/g, '-')}.png` });
    await ctx.close();
  }
  await b.close();
})();
