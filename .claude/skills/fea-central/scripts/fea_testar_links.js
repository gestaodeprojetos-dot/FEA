// Testa páginas e links rastreados como um lead real (segue redirecionamento, lê título, texto e links).
// Uso: node fea_testar_links.js URL1 URL2 ...   (ou um arquivo .txt com uma URL por linha)
// Mostra: status | URL final | título | data/hora que aparecem no texto | links e botões sem destino.
const {chromium}=require('playwright');const fs=require('fs');
let urls=process.argv.slice(2);
if(urls.length===1&&fs.existsSync(urls[0]))urls=fs.readFileSync(urls[0],'utf8').split('\n').map(s=>s.trim()).filter(Boolean);
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const u of urls){try{const r=await p.goto(u,{waitUntil:'networkidle',timeout:45000});
 const txt=await p.evaluate(()=>document.body.innerText);
 const datas=[...new Set(txt.match(/\b\d{1,2}(\/\d{1,2}| de [a-zç]+)\b[^\n]{0,30}/gi)||[])].slice(0,4);
 const vazios=await p.evaluate(()=>[...document.querySelectorAll('a,button')].filter(e=>/quero|garantir|entrar|acessar|grupo|inscrev/i.test(e.innerText)&&(!e.getAttribute('href')||e.getAttribute('href').startsWith('#'))&&e.tagName==='A').map(e=>e.innerText.trim().slice(0,40)));
 const utm=(p.url().match(/utm_campaign=([^&]+)/)||[])[1]||'';
 console.log([r&&r.status(),u,'->',p.url().slice(0,140),'|',await p.title(),utm?'| campanha '+utm:'','| datas:',datas.join(' ; '),vazios.length?'| BOTÃO SEM LINK: '+vazios.join(', '):''].join(' '));
}catch(e){console.log('ERRO',u,e.message.split('\n')[0])}}
await b.close();})();
