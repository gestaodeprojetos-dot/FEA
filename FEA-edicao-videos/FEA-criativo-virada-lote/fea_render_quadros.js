// FEA: renderiza a composição quadro a quadro (PNG com transparência, 30 fps).
// Uso: node fea_render_quadros.js PASTA_COMP CFG.json PASTA_SAIDA "all" | "stills:1.5,8,12"
// PASTA_COMP precisa de FEA-composicao-virada-lote.html, logo.png, pagina.jpg, card-*.png e ../fonts.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [, , dir, cfgPath, outdir, mode] = process.argv;
  const cfg = fs.readFileSync(cfgPath, 'utf8');
  const nome = JSON.parse(cfg).nome, dur = JSON.parse(cfg).dur;
  const html = fs.readFileSync(dir + '/FEA-composicao-virada-lote.html', 'utf8').replace('__CFG__', cfg);
  const run = `${dir}/_run_${nome}.html`; fs.writeFileSync(run, html);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await pg.goto('file://' + run); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
  fs.mkdirSync(outdir, { recursive: true });
  const stills = mode.startsWith('stills:');
  const times = stills ? mode.slice(7).split(',').map(Number) : [...Array(Math.round(dur * 30)).keys()].map(i => i / 30);
  let i = 0;
  for (const t of times) {
    await pg.evaluate(t => window.render(t), t);
    const name = stills ? `${nome}_${t.toFixed(2)}.png` : `f_${String(i).padStart(5, '0')}.png`;
    await pg.screenshot({ path: outdir + '/' + name, omitBackground: true }); i++;
  }
  await b.close();
})();
