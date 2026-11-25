const {chromium}=require('playwright');
(async()=>{const [,,url,out,w,h,mode,arg]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w||1440,height:+h||900}});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(String(e)));
await p.goto(url);await p.waitForTimeout(1500);
if(mode==='full'){await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,160));}});await p.waitForTimeout(1200);
 const miss=await p.evaluate(()=>[...document.querySelectorAll('[data-reveal]:not(.is-in)')].length);console.log('unrevealed after scroll:',miss);
 await p.evaluate(()=>{window.scrollTo(0,0);document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')});await p.waitForTimeout(900);}
if(mode==='scroll'){await p.evaluate(y=>window.scrollTo(0,+y),arg);await p.waitForTimeout(1300);}
if(mode==='click'){await p.click(arg);await p.waitForTimeout(900);}
if(mode==='hover'){await p.hover(arg);await p.waitForTimeout(700);}
await p.screenshot({path:out,fullPage:mode==='full'});if(errs.length)console.log('ERRORS',errs);await b.close();})();
