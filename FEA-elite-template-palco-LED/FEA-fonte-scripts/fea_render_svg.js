const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage();
  const jobs=[['logo3.svg','FEA-elite-logo-claro.png',3200,null],['logo7.svg','T-mask.png',null,2600],['logo10.svg','FEA-elite-monograma.png',null,1200]];
  for(const [src,out,w,h] of jobs){
    const svg=fs.readFileSync(src,'utf8'); const vb=svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const W=w||Math.round(h*vb[2]/vb[3]), H=h||Math.round(w*vb[3]/vb[2]);
    await p.setViewportSize({width:W,height:H});
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg','<svg width="'+W+'" height="'+H+'"')}</body></html>`);
    await p.screenshot({path:out,omitBackground:true,clip:{x:0,y:0,width:W,height:H}}); console.log(out,W,H);
  }
  await b.close();
})();
