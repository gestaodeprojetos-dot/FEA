const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport:{width:390,height:844}, deviceScaleFactor:2, isMobile:true, hasTouch:true,
    userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'});
  const p = await ctx.newPage();
  await p.goto('https://el.joaopithon.com.br/elite-injectors-congress/', {waitUntil:'networkidle', timeout:60000});
  const H = await p.evaluate(()=>document.body.scrollHeight);
  for (let y=0; y<H; y+=300){ await p.evaluate(v=>window.scrollTo(0,v), y); await p.waitForTimeout(120); }
  await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(1500);
  const info = await p.evaluate(()=>{
    const all=[...document.querySelectorAll('body *')].filter(e=>['fixed','sticky'].includes(getComputedStyle(e).position) && e.getBoundingClientRect().height>20);
    return all.map(e=>({tag:e.tagName,cls:e.className.toString().slice(0,60),r:e.getBoundingClientRect().toJSON()}));
  });
  console.log(JSON.stringify(info));
  await p.screenshot({path: dir+'/viewport.png'});
  // esconde barra fixa para o full page
  await p.evaluate(()=>{[...document.querySelectorAll('body *')].forEach(e=>{const s=getComputedStyle(e).position; if((s==='fixed'||s==='sticky') && e.getBoundingClientRect().height>20 && e.getBoundingClientRect().height<200) e.style.display='none';});});
  await p.waitForTimeout(500);
  await p.screenshot({path: dir+'/full.png', fullPage:true});
  const marks = await p.evaluate(()=>{const f=t=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.textContent.includes(t)){return n.parentElement.getBoundingClientRect().top+scrollY}}return -1};
    return {data:f('01 e 02 de Novembro'), botao:f('GARANTIR A MINHA VAGA'), lote:f('PRIMEIRO LOTE'), passaporte:f('Passaporte Elite'), H:document.body.scrollHeight}});
  console.log(JSON.stringify(marks));
  await b.close();
})();
