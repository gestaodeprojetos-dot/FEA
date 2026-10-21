// Renderiza as artes da contagem regressiva (PNG + MP4) a partir de FEA-contagem.html.
// Uso: node fea_render.js [--tpl contagem|palestrantes] [--still-only] [--days 11,10] [--fmt feed,story] [--workers 3]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const STILL_ONLY = args.includes('--still-only');
const DAYS = opt('--days', '11,10,9,8,7,6,5,4,3,2,1,0').split(',').map(Number);
const FMTS = opt('--fmt', 'feed,story').split(',');
const WORKERS = parseInt(opt('--workers', '3'), 10);
const TPL = opt('--tpl', 'contagem'); // contagem | palestrantes
const BASE = opt('--base', `http://127.0.0.1:8765/FEA-${TPL === 'palestrantes' ? 'contagem-palestrantes' : 'contagem'}.html`);
const OUT = path.resolve(__dirname, '..', TPL === 'palestrantes' ? 'output-palestrantes' : 'output');
const AUDIO = path.resolve(__dirname, '..', 'output', 'FEA-elite-trilha.wav');
const FPS = 30, DUR = 10;

// data de postagem: hoje (21/10) = faltam 11 dias
const postDate = n => { const d = new Date(Date.UTC(2026, 9, 21 + (11 - n))); return `${String(d.getUTCDate()).padStart(2, '0')}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`; };
const label = n => n === 0 ? 'e-hoje' : `faltam-${String(n).padStart(2, '0')}`;
const fname = (n, fmt) => `FEA-elite-${TPL === 'palestrantes' ? 'palestrantes-' : ''}${postDate(n)}-${label(n)}-${fmt === 'story' ? 'stories' : 'feed'}`;

async function job(browser, n, fmt) {
  const H = fmt === 'story' ? 1920 : 1350;
  const page = await browser.newPage({ viewport: { width: 1080, height: H }, deviceScaleFactor: 1 });
  await page.goto(`${BASE}?n=${n}&fmt=${fmt}`);
  await page.evaluate(() => window.__ready);
  await page.waitForTimeout(150);
  const dir = path.join(OUT, fmt === 'story' ? 'stories' : 'feed');
  fs.mkdirSync(dir, { recursive: true });
  const base = path.join(dir, fname(n, fmt));

  await page.evaluate(() => window.__render(9.9, 297));
  await page.screenshot({ path: base + '.png', clip: { x: 0, y: 0, width: 1080, height: H } });
  if (STILL_ONLY) { await page.close(); return; }

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', AUDIO,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
    '-movflags', '+faststart', '-shortest', base + '.mp4']);
  const done = new Promise((res, rej) => ff.on('close', c => c ? rej(new Error('ffmpeg ' + c)) : res()));
  for (let f = 0; f < FPS * DUR; f++) {
    await page.evaluate(([t, f]) => window.__render(t, f), [f / FPS, f]);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95, clip: { x: 0, y: 0, width: 1080, height: H } });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await done;
  await page.close();
  console.log('ok', path.basename(base));
}

(async () => {
  const browser = await chromium.launch({ args: ['--disable-web-security', '--force-color-profile=srgb'] });
  const queue = [];
  for (const n of DAYS) for (const fmt of FMTS) queue.push([n, fmt]);
  await Promise.all(Array.from({ length: WORKERS }, async () => {
    while (queue.length) { const [n, fmt] = queue.shift(); await job(browser, n, fmt); }
  }));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
