// Renderiza uma página de animação (contrato: window.DURATION, window.seek(t), window.ready).
//   HTML=pagina.html VW=1920 VH=1080 [DPR=1] node fea_render.js preview 1,3.5,6
//   HTML=pagina.html VW=1920 VH=1080 [DPR=1] [FPS=30] node fea_render.js video saida.mp4 [processos=4]
// O HTML é procurado a partir da pasta atual. Os quadros ficam em ./frames (apagada a cada vídeo).
let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const { chromium } = playwright;
const { execFileSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const CWD = process.cwd();
const HTML = process.env.HTML || 'index.html';
const VW = +(process.env.VW || 1920), VH = +(process.env.VH || 1080), DPR = +(process.env.DPR || 1);
const FRAMES = path.join(CWD, 'frames');

async function open() {
  const opts = { args: ['--allow-file-access-from-files'] };
  if (process.env.CHROME_PATH) opts.executablePath = process.env.CHROME_PATH;
  const b = await chromium.launch(opts);
  const p = await b.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: DPR });
  await p.goto('file://' + path.resolve(CWD, HTML));
  await p.evaluate(() => window.ready); await p.evaluate(() => document.fonts.ready);
  return { b, p };
}

async function worker(fps, k, W) {
  const { b, p } = await open();
  const n = Math.round(await p.evaluate(() => window.DURATION) * fps);
  for (let i = k; i < n; i += W) {
    await p.evaluate(t => window.seek(t), i / fps);
    await p.screenshot({ path: `${FRAMES}/f${String(i).padStart(5, '0')}.png` });
    if (k === 0 && i % (W * 60) === 0) console.log('quadro', i, '/', n);
  }
  await b.close();
}

(async () => {
  const [mode, a, c] = process.argv.slice(2);
  if (mode === 'worker') return worker(+a, +c, +process.argv[5]);
  if (mode === 'preview') {
    const { b, p } = await open();
    for (const t of a.split(',').map(Number)) {
      await p.evaluate(t => window.seek(t), t);
      await p.screenshot({ path: path.join(CWD, `prev-${t}.jpg`), type: 'jpeg', quality: 88 });
    }
    await b.close(); return;
  }
  const fps = +(process.env.FPS || 30), out = a, W = +c || 4;
  fs.rmSync(FRAMES, { recursive: true, force: true }); fs.mkdirSync(FRAMES);
  await Promise.all([...Array(W).keys()].map(k => new Promise((res, rej) => {
    const ch = spawn('node', [__filename, 'worker', fps, k, W], { stdio: 'inherit', env: process.env });
    ch.on('exit', code => code ? rej(new Error('processo ' + k)) : res());
  })));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(fps), '-i', FRAMES + '/f%05d.png',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  console.log('ok', out);
})().catch(e => { console.error(e); process.exit(1); });
