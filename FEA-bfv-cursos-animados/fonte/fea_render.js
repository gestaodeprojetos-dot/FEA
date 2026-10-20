// node render.js preview 1,5,10   -> PNGs nos tempos dados
// node render.js video 30 saida.mp4 -> quadros + MP4
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const DIR = __dirname;
(async () => {
  const [mode, a, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + DIR + '/' + (process.env.HTML || 'teaser.html'));
  await p.evaluate(() => window.ready);
  await p.evaluate(() => document.fonts.ready);
  if (mode === 'preview') {
    for (const t of a.split(',').map(Number)) {
      await p.evaluate(t => window.seek(t), t);
      await p.screenshot({ path: `${DIR}/prev-${t}.jpg`, quality: 80, type: 'jpeg' });
    }
  } else {
    const fps = +a || 30, dur = await p.evaluate(() => window.DURATION), n = Math.round(dur * fps);
    const fdir = DIR + '/frames'; fs.rmSync(fdir, { recursive: true, force: true }); fs.mkdirSync(fdir);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => window.seek(t), i / fps);
      await p.screenshot({ path: `${fdir}/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 95 });
      if (i % 150 === 0) console.log('quadro', i, '/', n);
    }
    execSync(`ffmpeg -v error -y -framerate ${fps} -i ${fdir}/f%05d.jpg -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart "${out}"`);
    console.log('ok', out);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
