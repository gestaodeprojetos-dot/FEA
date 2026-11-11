// uso: node make.js saida_dir JSON_tapes   -> gera tape_<id>.png + period, e botao.png
const { chromium } = require('playwright'); const fs=require('fs');
const out=process.argv[2]; const tapes=JSON.parse(process.argv[3]);
const FONT=`<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=block" rel="stylesheet">`;
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:6000,height:300}});
 const per={};
 for(const [id,[w,y]] of Object.entries(tapes)){
  await p.setContent(`<html><head>${FONT}<style>html,body{margin:0;background:transparent}
  .u{display:inline-flex;align-items:center;white-space:nowrap;font-family:Montserrat;padding:0 0 0 60px;gap:60px}
  .w{font-weight:900;font-size:64px;color:#fff}.y{font-weight:800;font-size:48px;color:#ffe9a8;letter-spacing:2px}.s{font-size:30px;color:#111}
  </style></head><body><span class="u" id="u"><span class="w">${w}</span><span class="s">▲</span><span class="y">${y}</span><span class="s">▲</span></span></body></html>`);
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
  const W=Math.ceil(await p.evaluate(()=>document.getElementById('u').getBoundingClientRect().width));
  const n=Math.ceil(3200/W)+1;
  await p.setContent(`<html><head>${FONT}<style>html,body{margin:0;background:transparent}
  .t{width:${W*n}px;height:150px;display:flex;align-items:center;overflow:hidden;background:linear-gradient(180deg,#e0222a 0%,#c4141c 55%,#a50f16 100%);border-top:10px solid #111;border-bottom:10px solid #111;box-sizing:border-box;font-family:Montserrat}
  .u{flex:0 0 ${W}px;width:${W}px;display:inline-flex;align-items:center;white-space:nowrap;padding-left:60px;gap:60px;box-sizing:border-box}
  .w{font-weight:900;font-size:64px;color:#fff}.y{font-weight:800;font-size:48px;color:#ffe9a8;letter-spacing:2px}.s{font-size:30px;color:#111}
  </style></head><body><div class="t">${`<span class="u"><span class="w">${w}</span><span class="s">▲</span><span class="y">${y}</span><span class="s">▲</span></span>`.repeat(n)}</div></body></html>`);
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({path:`${out}/tape_${id}.png`,omitBackground:true,clip:{x:0,y:0,width:W*n,height:150}});
  per[id]=W;
 }
 await p.setContent(`<html><head>${FONT}<style>html,body{margin:0;background:transparent}
 .c{display:inline-flex;flex-direction:column;align-items:center;padding:20px 30px}
 .a{font-size:0;margin-bottom:8px}
 .btn{padding:22px 64px;border-radius:18px;background:linear-gradient(180deg,#f7e3a1 0%,#e2bd5f 45%,#c9993c 100%);box-shadow:0 8px 24px rgba(0,0,0,.45),inset 0 2px 0 rgba(255,255,255,.6);font-family:Montserrat;font-weight:900;font-size:48px;color:#1a1308;letter-spacing:1px}
 </style></head><body><div class="c" id="c"><svg class="a" width="60" height="64" viewBox="0 0 60 64"><path d="M22 2h16v30h16L30 62 6 32h16z" fill="#f1cf74" stroke="#5a4214" stroke-width="3" stroke-linejoin="round"/></svg><div class="btn">SAIBA MAIS</div></div></body></html>`);
 await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
 await p.locator('#c').screenshot({path:`${out}/botao.png`,omitBackground:true});
 fs.writeFileSync(`${out}/periodos.json`,JSON.stringify(per)); await b.close();
})();
