// Renderização paralela: node render_par.js FPS SAIDA.mp4 WORKERS
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { execFileSync, spawn } = require('child_process');
const fs = require('fs');
const DIR = __dirname, HTML = process.env.HTML || 'FEA-teaser-reology-map.html';
async function worker(fps, k, W) {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: +(process.env.VW || 1920), height: +(process.env.VH || 1080) } });
  await p.goto('file://' + DIR + '/' + HTML);
  await p.evaluate(() => window.ready); await p.evaluate(() => document.fonts.ready);
  const n = Math.round(await p.evaluate(() => window.DURATION) * fps);
  for (let i = k; i < n; i += W) {
    await p.evaluate(t => window.seek(t), i / fps);
    await p.screenshot({ path: `${DIR}/frames/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (k === 0 && i % (W * 150) === 0) console.log('quadro', i, '/', n);
  }
  await b.close();
}
(async () => {
  const [a1, a2, a3, a4] = process.argv.slice(2);
  if (a1 === 'worker') return worker(+a2, +a3, +a4);
  const fps = +a1, out = a2, W = +a3 || 4;
  fs.rmSync(DIR + '/frames', { recursive: true, force: true }); fs.mkdirSync(DIR + '/frames');
  await Promise.all([...Array(W).keys()].map(k => new Promise((res, rej) => {
    const c = spawn('node', [__filename, 'worker', fps, k, W], { stdio: 'inherit', env: process.env });
    c.on('exit', code => code ? rej(new Error('worker ' + k)) : res());
  })));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(fps), '-i', DIR + '/frames/f%05d.jpg', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  console.log('ok', out);
})().catch(e => { console.error(e); process.exit(1); });
