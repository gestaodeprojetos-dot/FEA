// Gera criativos estaticos Black Friday Vitalicia (feed 1:1 e stories 9:16)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ASSETS = process.argv[2];
const OUT = process.argv[3];
const ONLY = process.argv[4];
fs.mkdirSync(OUT, { recursive: true });

const GOLD = '#E5AD6A';
const ph = (n) => `file://${ASSETS}/phs/${n}.jpg`;
const logo = `file://${ASSETS}/bfv-logo.svg`;

const ADS = [
  { id: 162, foto: '15', pre: 'Vem aí...',
    head: 'Pela primeira vez, uma oferta de acesso a todos os meus cursos, formações e imersões <b>VITALÍCIA.</b>',
    sub: 'A formação que evolui junto com você. Um marco na sua carreira em harmonização facial.' },
  { id: 163, foto: '22', pre: 'Vem aí...',
    head: 'Pela primeira vez, uma oferta com os meus <b>20 cursos, formações e imersões</b>, liberados de uma vez, <b>VITALÍCIA.</b>',
    sub: 'Os cursos que evoluem junto com você, inclusive os que eu ainda vou lançar.' },
  { id: 164, foto: '39',
    head: 'Pela primeira vez, uma oferta com <b>o menor valor de toda a Black Friday</b>, reservada a quem estiver ao vivo, <b>VITALÍCIA.</b>',
    sub: 'A formação que evolui junto com você. O Lote Especial é só para quem estiver comigo na live de abertura.' },
  { id: 165, foto: '25', big: true,
    head: 'Da insegurança ao <b>domínio da harmonização facial.</b>',
    sub: 'A formação, baseada em casos reais, que evolui junto com você.' },
  { id: 166, foto: '21', big: true,
    head: 'Do medo da intercorrência ao <b>domínio que te deixa pronto para qualquer paciente.</b>',
    sub: 'Os cursos que evoluem junto com você, para sempre, num pagamento só.' },
  { id: 167, foto: '08', big: true,
    head: 'Do primeiro preenchimento ao <b>domínio completo da harmonização facial.</b>',
    sub: 'A formação, construída a partir da prática clínica, que evolui junto com você.' },
  { id: 168, foto: '07', big: true,
    head: 'Do medo de intercorrência ao <b>domínio completo, até nas áreas mais desafiadoras.</b>',
    sub: 'A formação, construída a partir da prática clínica, que evolui junto com você.' },
  { id: 169, foto: '40', big: true,
    head: 'Da insegurança que paralisa ao <b>domínio que te torna referência.</b>',
    sub: 'A formação, construída a partir da prática clínica, que evolui junto com você.' },
  { id: 170, foto: '25', lista: true },
];

const CURSOS = [
  'Formação Especialista em Preenchimento', 'Formação Especialista em Botox',
  'Formação Especialista em Fios', 'Formação Especialista em Corporal',
  'Formação Especialista em Anatomia', 'Formação Especialista em Bioestimuladores',
  'Pós-Graduação em Técnicas Injetáveis', 'Elite Injectors Congress',
  'Curso Avançado de Complicações', 'Atenda Todo Santo Dia',
  'Curso de Preenchimento Express', 'Curso de Toxina Express', 'FEP Direct',
  'Imersão Avançada em Rinomodelação', 'Imersão Avançada em Olheiras',
  'Imersão Avançada em Lábios', 'Imersão Avançada em Full Face com menos de 5 ml',
  'Imersão Avançada em Full Face com mais de 10 ml',
  'Livro Digital: A Ciência e Arte do Preenchimento Tridimensional de Olheiras',
  'Livro Digital: Intercorrências no Preenchimento com Ácido Hialurônico',
];

const baseCss = `
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#000}
.c{position:relative;overflow:hidden;background:#050403;font-family:'Montserrat',sans-serif;color:#fff}
.glow{position:absolute;inset:0;pointer-events:none}
.photo{position:absolute;background-repeat:no-repeat;background-size:cover}
.logo{position:absolute;display:block}
.pre{color:${GOLD};font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.head{font-weight:500;line-height:1.22;letter-spacing:-.005em}
.head b{font-weight:800;color:${GOLD}}
.sub{font-weight:400;line-height:1.4;color:rgba(255,255,255,.82)}
.pill{display:inline-block;border:3px solid ${GOLD};border-radius:999px;font-weight:800;letter-spacing:.02em;color:#fff;white-space:nowrap}
.cta{display:inline-block;background:linear-gradient(180deg,#F2C58C 0%,${GOLD} 55%,#C98E4C 100%);color:#140d05;font-weight:800;text-transform:uppercase;border-radius:12px;letter-spacing:.03em;white-space:nowrap;box-shadow:0 0 40px rgba(229,173,106,.35)}
.ig{color:rgba(255,255,255,.7);font-weight:500;letter-spacing:.02em}
.flare{position:absolute;height:3px;background:linear-gradient(90deg,transparent,rgba(255,214,160,.0) 10%,#FFD9A6 50%,rgba(255,214,160,0) 90%,transparent);box-shadow:0 0 24px 6px rgba(229,173,106,.45);border-radius:3px}
.lista{list-style:none;columns:2;column-gap:28px}
.lista li{break-inside:avoid;position:relative;padding-left:22px;font-weight:500;line-height:1.25;color:rgba(255,255,255,.92)}
.lista li:before{content:'';position:absolute;left:0;width:9px;height:9px;border-radius:50%;background:${GOLD};top:.42em}
`;

function glow(w, h, fx, fy) {
  return `<div class="glow" style="background:
    radial-gradient(ellipse ${w * 0.9}px ${h * 0.55}px at ${fx}% ${fy}%, rgba(229,173,106,.28), rgba(229,173,106,0) 70%),
    radial-gradient(ellipse ${w}px ${h * 0.35}px at 50% 105%, rgba(229,173,106,.22), rgba(0,0,0,0) 70%)"></div>`;
}

function feed(ad) {
  const S = 1080;
  if (ad.lista) {
    return `<div class="c" style="width:${S}px;height:${S}px">
      ${glow(S, S, 80, 30)}
      <div class="photo" style="right:-60px;top:0;width:520px;height:620px;background-image:url(${ph(ad.foto)});background-position:50% 12%;
        -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 40%),linear-gradient(0deg,transparent 0,#000 35%);-webkit-mask-composite:source-in"></div>
      <img class="logo" src="${logo}" style="left:64px;top:56px;width:330px">
      <div style="position:absolute;left:64px;top:228px;width:580px">
        <div style="font-weight:900;font-size:76px;letter-spacing:.01em;line-height:1;color:${GOLD}">ABSURDO <span style="font-size:62px">😳</span></div>
        <div class="head" style="font-size:30px;margin-top:20px">O valor que você vai pagar para ter <b>todos os cursos do Dr. João Pithon para sempre.</b></div>
      </div>
      <ul class="lista" style="position:absolute;left:64px;right:64px;top:520px;font-size:19.5px">
        ${CURSOS.map((c) => `<li style="margin-bottom:11px">${c}</li>`).join('')}
      </ul>
      <div style="position:absolute;left:64px;right:64px;bottom:52px;display:flex;align-items:center;justify-content:space-between">
        <span class="cta" style="font-size:28px;padding:22px 40px">Toque em saiba mais</span>
        <span class="ig" style="font-size:24px">@drjoaopithon</span>
      </div>
    </div>`;
  }
  const hs = ad.big ? 50 : 39;
  return `<div class="c" style="width:${S}px;height:${S}px">
    ${glow(S, S, 78, 40)}
    <div class="photo" style="right:-40px;top:40px;width:600px;height:${S - 40}px;background-image:url(${ph(ad.foto)});background-position:50% 8%;
      -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 38%),linear-gradient(0deg,transparent 0,#000 30%);-webkit-mask-composite:source-in"></div>
    <div class="flare" style="left:40px;width:520px;top:${ad.pre ? 300 : 262}px"></div>
    <img class="logo" src="${logo}" style="left:64px;top:60px;width:380px">
    <div style="position:absolute;left:64px;top:${ad.pre ? 330 : 300}px;width:${ad.big ? 600 : 545}px">
      ${ad.pre ? `<div class="pre" style="font-size:30px;margin-bottom:16px">${ad.pre}</div>` : ''}
      <div class="head" style="font-size:${hs}px">${ad.head}</div>
      <div class="sub" style="font-size:24px;margin-top:22px;width:520px">${ad.sub}</div>
    </div>
    <div style="position:absolute;left:64px;bottom:58px">
      <div class="pill" style="font-size:34px;padding:14px 38px">20 DE OUTUBRO | 20H</div>
      <div style="display:flex;align-items:center;gap:28px;margin-top:22px">
        <span class="cta" style="font-size:26px;padding:20px 34px">Inscreva-se gratuitamente</span>
      </div>
    </div>
    <div class="ig" style="position:absolute;right:56px;bottom:62px;font-size:22px">@drjoaopithon</div>
  </div>`;
}

function story(ad) {
  const W = 1080, H = 1920;
  if (ad.lista) {
    return `<div class="c" style="width:${W}px;height:${H}px">
      ${glow(W, H, 75, 20)}
      <div class="photo" style="right:-90px;top:60px;width:560px;height:700px;background-image:url(${ph(ad.foto)});background-position:50% 0%;
        -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 45%),linear-gradient(180deg,transparent 0,#000 22%,#000 55%,transparent 100%);-webkit-mask-composite:source-in"></div>
      <img class="logo" src="${logo}" style="left:72px;top:200px;width:400px">
      <div style="position:absolute;left:72px;top:400px;width:640px">
        <div style="font-weight:900;font-size:92px;line-height:1;color:${GOLD};white-space:nowrap">ABSURDO <span style="font-size:76px">😳</span></div>
        <div class="head" style="font-size:36px;margin-top:22px">O valor que você vai pagar para ter <b>todos os cursos do Dr. João Pithon para sempre.</b></div>
      </div>
      <ul class="lista" style="position:absolute;left:72px;right:72px;top:690px;font-size:25px;columns:1">
        ${CURSOS.map((c) => `<li style="margin-bottom:7px;padding-left:28px">${c}</li>`).join('')}
      </ul>
      <div style="position:absolute;left:0;right:0;bottom:190px;text-align:center">
        <span class="cta" style="font-size:36px;padding:28px 56px">Toque em saiba mais</span>
        <div class="ig" style="font-size:28px;margin-top:22px">@drjoaopithon</div>
      </div>
    </div>`;
  }
  const hs = ad.big ? 64 : 48;
  return `<div class="c" style="width:${W}px;height:${H}px">
    ${glow(W, H, 50, 35)}
    <div class="photo" style="left:0;right:0;top:300px;height:820px;background-image:url(${ph(ad.foto)});background-position:50% 4%;
      -webkit-mask-image:linear-gradient(0deg,transparent 0,transparent 8%,#000 55%),linear-gradient(180deg,transparent 0,#000 16%);-webkit-mask-composite:source-in"></div>
    <img class="logo" src="${logo}" style="left:50%;transform:translateX(-50%);top:170px;width:500px">
    <div style="position:absolute;left:80px;right:80px;bottom:250px;text-align:center;display:flex;flex-direction:column;align-items:center">
      <div class="flare" style="position:relative;width:760px;margin-bottom:34px"></div>
      ${ad.pre ? `<div class="pre" style="font-size:36px;margin-bottom:16px">${ad.pre}</div>` : ''}
      <div class="head" style="font-size:${hs}px">${ad.head}</div>
      <div class="sub" style="font-size:31px;margin-top:24px;padding:0 20px">${ad.sub}</div>
      <div class="pill" style="font-size:44px;padding:16px 48px;margin-top:46px">20 DE OUTUBRO | 20H</div>
      <div style="margin-top:28px"><span class="cta" style="font-size:34px;padding:26px 50px">Inscreva-se gratuitamente</span></div>
      <div class="ig" style="font-size:28px;margin-top:24px">@drjoaopithon</div>
    </div>
  </div>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const ad of ADS) {
    if (ONLY && String(ad.id) !== ONLY) continue;
    for (const [fmt, fn, w, h] of [['feed-1x1', feed, 1080, 1080], ['stories-9x16', story, 1080, 1920]]) {
      await page.setViewportSize({ width: w, height: h });
      const html = `<!doctype html><html><head><meta charset="utf-8"><style>${baseCss}</style></head><body>${fn(ad)}</body></html>`;
      const tmp = path.join(OUT, '.tmp.html');
      fs.writeFileSync(tmp, html);
      await page.goto('file://' + tmp, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      // garante que o texto nao estoura a arte
      const overflow = await page.evaluate(() => {
        const c = document.querySelector('.c').getBoundingClientRect();
        return [...document.querySelectorAll('.head,.sub,.pill,.cta,.lista,.ig')].some((e) => {
          const r = e.getBoundingClientRect();
          return r.right > c.right + 1 || r.bottom > c.bottom + 1;
        });
      });
      const file = path.join(OUT, `FEA-BFV-ADS${ad.id}-${fmt}.png`);
      await page.locator('.c').screenshot({ path: file });
      console.log(file, overflow ? 'OVERFLOW' : 'ok');
      fs.unlinkSync(tmp);
    }
  }
  await browser.close();
})();
