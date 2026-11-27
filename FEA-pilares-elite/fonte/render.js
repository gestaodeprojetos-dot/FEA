// node render.js preview HTML 1,2,3   |   node render.js video HTML FPS saida.mp4
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const DIR = __dirname;
(async () => {
  const [mode, html, a, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + DIR + '/' + html);
  await p.evaluate(() => window.ready); await p.evaluate(() => document.fonts.ready);
  if (mode === 'preview') {
    for (const t of a.split(',').map(Number)) {
      await p.evaluate(t => window.seek(t), t);
      await p.screenshot({ path: `${DIR}/prev-${t}.jpg`, type: 'jpeg', quality: 85 });
    }
  } else {
    const fps = +a, n = Math.round(await p.evaluate(() => window.DURATION) * fps), fdir = DIR + '/frames';
    fs.rmSync(fdir, { recursive: true, force: true }); fs.mkdirSync(fdir);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => window.seek(t), i / fps);
      await p.screenshot({ path: `${fdir}/f${String(i).padStart(5, '0')}.png` });
    }
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(fps), '-i', fdir + '/f%05d.png', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
    console.log('ok', out);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
