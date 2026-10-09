const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs');
(async()=>{
  const [,,dir,outdir,mode]=process.argv; // mode: "stills:1,2,3" or "all:DUR"
  const html=fs.readFileSync(dir+'/FEA-composicao-virada-lote.html','utf8').replace('__LEGENDAS__',fs.readFileSync(dir+'/legendas.json','utf8'));
  fs.writeFileSync(dir+'/_comp_run.html',html);
  const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1080,height:1920}});
  await pg.goto('file://'+dir+'/_comp_run.html'); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(500);
  fs.mkdirSync(outdir,{recursive:true});
  let times=[];
  if(mode.startsWith('stills:')) times=mode.slice(7).split(',').map(Number);
  else { const dur=Number(mode.slice(4)); for(let i=0;i<Math.round(dur*30);i++) times.push(i/30); }
  let i=0;
  for(const t of times){ await pg.evaluate(t=>window.render(t),t);
    const name=mode.startsWith('stills:')?`s_${t.toFixed(2)}.png`:`f_${String(i).padStart(5,'0')}.png`;
    await pg.screenshot({path:outdir+'/'+name, omitBackground:true}); i++; }
  await b.close();
})();
