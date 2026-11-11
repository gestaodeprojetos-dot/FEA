// FEA: captura recortes da página de vendas (contorna o desafio do Cloudflare buscando cada recurso via curl).
// Uso (na pasta lp/): REG='{"bonus":[3660,4725]}' node fea_ads_capturar_pagina.js  -> sec_*.png (juntar em ins_<nome>.png)
const { chromium } = require('playwright'); const { execFileSync } = require('child_process'); const fs=require('fs');
const UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)';
(async()=>{
 const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:430,height:932},deviceScaleFactor:3,userAgent:UA});
 await ctx.route(/joaopithon\.com\.br/, async r=>{
   const url=r.request().url();
   try{ const hdr=execFileSync('curl',['-sL','-A',UA,'-D','-','-o','body.bin',url]).toString();
     const ct=(hdr.match(/content-type:\s*([^\r\n]+)/ig)||[]).pop()||'';
     await r.fulfill({status:200,body:fs.readFileSync('body.bin'),headers:{'content-type':ct.split(':').slice(1).join(':').trim()||'application/octet-stream'}});
   }catch(e){ await r.abort(); }
 });
 const p=await ctx.newPage();
 await p.goto('https://lp.joaopithon.com.br/black-friday/vitalicia/',{waitUntil:'load',timeout:120000});
 for(let y=0;y<40000;y+=500){await p.evaluate(v=>window.scrollTo(0,v),y);await p.waitForTimeout(150);}
 const pos=await p.evaluate(()=>{const f=(re)=>{const e=[...document.querySelectorAll('h1,h2,h3,p,span,div')].find(e=>re.test(e.innerText||'')&&e.children.length<6);if(!e)return null;const r=e.getBoundingClientRect();return Math.round(r.top+scrollY)};
   return {bonus:f(/^E ainda por cima/),incluso:f(/^O que está incluso/),emais:f(/^E mais/),novos:f(/^Novos cursos a caminho/),forte:f(/^Literalmente, essa é a/),prof:f(/^Professor/),lotes:f(/^Esta oferta será dividida/),atencao:f(/^ATENÇÃO/),comp:f(/^Comparativo/),mas:f(/^Mas na Black Friday/)}});
 console.log(JSON.stringify(pos)); fs.writeFileSync('pos.json',JSON.stringify(pos));
 await p.evaluate(()=>{for(const e of document.querySelectorAll('*')){const c=getComputedStyle(e);if(c.position==='fixed'||c.position==='sticky'){e.style.setProperty('display','none','important')}}});
 const shotRange=async(name,y0,y1)=>{ const parts=[]; for(let y=y0;y<y1;y+=900){ await p.evaluate(v=>window.scrollTo(0,v),y); await p.waitForTimeout(900); const top=await p.evaluate(()=>scrollY); const h=Math.min(900,y1-y); await p.screenshot({path:`sec_${name}_${parts.length}.png`,clip:{x:0,y:y-top,width:430,height:h}}); parts.push(1);} console.log(name,parts.length); };
 const R=JSON.parse(process.env.REG); for(const [n,[a,z]] of Object.entries(R)){ await shotRange(n,a,z); }
 await b.close();
})();
