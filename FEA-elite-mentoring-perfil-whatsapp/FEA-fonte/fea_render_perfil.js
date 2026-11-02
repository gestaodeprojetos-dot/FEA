// Renderiza a foto de perfil do Elite Mentoring (1080x1080) a partir do HTML.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'FEA-perfil-whatsapp-elite-mentoring.html'));
  await p.waitForTimeout(400);
  await p.locator('.arte').screenshot({ path: path.join(__dirname, '_render-2x.png') });
  await b.close();
})();
