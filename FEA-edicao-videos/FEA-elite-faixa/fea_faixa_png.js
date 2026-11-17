const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:200}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(500);await (await p.$('#f')).screenshot({path:process.argv[3],omitBackground:true});await b.close()})();
