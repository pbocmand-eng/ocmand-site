// Automated check of the built site: every page at seven screen widths (overflow, broken images, clipped text,
// overlaps, one h1), plus menus, the photo viewer, forms, redirects and the 404 page.
// Run through:  bash _source/check.sh   (it rebuilds, starts the local server and runs this).
const { chromium } = require('playwright');
const B='http://127.0.0.1:8812';
const fs=require('fs'),path=require('path');
// every page listed in sitemap.xml is checked, so a new page is covered as soon as build.py adds it there
const pages=[...fs.readFileSync(path.join(__dirname,'..','sitemap.xml'),'utf8').matchAll(/<loc>https?:\/\/[^\/<]+([^<]*)<\/loc>/g)].map(m=>m[1]||'/');
const widths=[360,390,768,1024,1280,1440,1920];
(async()=>{
  const br=await chromium.launch(); const issues=[]; let checks=0;
  for(const w of widths){
    const ctx=await br.newContext({viewport:{width:w,height:900}});
    await ctx.route(/googletagmanager|google-analytics/,r=>r.abort());
    const pg=await ctx.newPage();
    pg.on('console',m=>{ if(m.type()==='error' && !/ERR_FAILED|googletagmanager/.test(m.text())) issues.push(`[${w}] console: ${m.text().slice(0,140)}`); });
    pg.on('pageerror',e=>issues.push(`[${w}] pageerror: ${e.message.slice(0,140)}`));
    pg.on('response',r=>{ if(r.status()>=400) issues.push(`[${w}] ${r.status()} ${r.url()}`); });
    for(const p of pages){
      await pg.goto(B+p,{waitUntil:'load'});
      const h=await pg.evaluate(()=>document.documentElement.scrollHeight);
      for(let y=0;y<h;y+=500){ await pg.evaluate(y=>window.scrollTo(0,y),y); await pg.waitForTimeout(60); }
      await pg.waitForTimeout(900);
      const r=await pg.evaluate(()=>{
        const out=[]; const vw=document.documentElement.clientWidth;
        if(document.documentElement.scrollWidth>vw+1) out.push('horizontal scroll: '+document.documentElement.scrollWidth+' > '+vw);
        document.querySelectorAll('img').forEach(i=>{ if(i.getAttribute('src') && i.complete && i.naturalWidth===0) out.push('broken img '+i.getAttribute('src')); });
        const unre=[...document.querySelectorAll('[data-reveal]')].filter(e=>getComputedStyle(e).opacity<0.99).length; if(unre) out.push('unrevealed '+unre);
        document.querySelectorAll('.h-xl,.h-lg,.h-md,.h-sm,.tb dd,.markets .name,.lede,.btn,.creds dt,.facts dd,.ledger td,.site-footer a,.nav a,.kicker').forEach(e=>{
          const r=e.getBoundingClientRect(); if(!r.width) return;
          if(e.scrollWidth>e.clientWidth+2 && getComputedStyle(e).display!=='inline') out.push('text overflows its box: '+e.className+' "'+e.textContent.trim().slice(0,40)+'"');
          if(r.right>vw+1||r.left<-1){ let hid=false; for(let a=e.parentElement;a;a=a.parentElement){ const cs=getComputedStyle(a); if(cs.visibility==='hidden'||cs.opacity==='0'){hid=true;break;} } if(!hid) out.push('outside viewport: '+e.className+' "'+e.textContent.trim().slice(0,40)+'" right='+Math.round(r.right)); }
        });
        // sibling overlap in grids
        document.querySelectorAll('.phase,.intro,.split,.sec-head,.cta .wrap,.contact-grid,.markets a,.people,.cols3').forEach(g=>{
          const k=[...g.children].filter(c=>c.getBoundingClientRect().width>0);
          for(let i=0;i<k.length;i++)for(let j=i+1;j<k.length;j++){ const a=k[i].getBoundingClientRect(),b=k[j].getBoundingClientRect();
            const inner=el=>{ let m=el.getBoundingClientRect().right; el.querySelectorAll('*').forEach(c=>{ const cr=c.getBoundingClientRect(); if(cr.width&&cr.right>m) m=cr.right; }); return m; };
            if(Math.abs(a.top-b.top)<a.height && b.left>=a.left && inner(k[i])>b.left+2 && a.bottom>b.top+2 && b.bottom>a.top+2) out.push('overlap in .'+g.className.split(' ')[0]+': "'+k[i].textContent.trim().slice(0,30)+'"'); }
        });
        const h1=document.querySelectorAll('h1').length; if(h1!==1) out.push('h1 count '+h1);
        return out;
      });
      checks++; r.forEach(x=>issues.push(`[${w}] ${p} ${x}`));
    }
    await ctx.close();
  }
  // interactions
  const log=[];
  { const ctx=await br.newContext({viewport:{width:1440,height:900}}); await ctx.route(/googletagmanager/,r=>r.abort());
    await ctx.route(/api\.web3forms\.com/,r=>r.fulfill({status:200,contentType:'application/json',body:'{"success":true}'}));
    const pg=await ctx.newPage(); await pg.goto(B+'/');
    await pg.hover('.has-menu > a'); await pg.waitForTimeout(400);
    log.push('dropdown visible: '+await pg.evaluate(()=>getComputedStyle(document.querySelector('.menu')).visibility));
    await pg.click('.menu a[href="/public-works"]'); await pg.waitForURL('**/public-works');
    log.push('dropdown nav -> '+new URL(pg.url()).pathname+' | h1: '+await pg.textContent('h1'));
    log.push('aria-current on Markets: '+await pg.evaluate(()=>!!document.querySelector('.nav a[aria-current="page"]')));
    await pg.click('.nav > a[href="/projects"]'); await pg.waitForURL('**/projects');
    await pg.click('button.shot >> nth=1'); await pg.waitForTimeout(400);
    log.push('lightbox open: '+await pg.evaluate(()=>document.querySelector('dialog.lb').open)+' | '+await pg.textContent('[data-count]')+' | '+await pg.textContent('dialog [data-name]'));
    await pg.keyboard.press('ArrowRight'); await pg.waitForTimeout(200); log.push('next: '+await pg.textContent('[data-count]')+' img ok: '+await pg.evaluate(()=>document.querySelector('dialog.lb img').naturalWidth>0));
    await pg.keyboard.press('Escape'); await pg.waitForTimeout(200); log.push('lightbox closed: '+await pg.evaluate(()=>!document.querySelector('dialog.lb').open));
    await pg.goto(B+'/contact#subs'); await pg.waitForTimeout(600);
    log.push('#subs anchor in view: '+await pg.evaluate(()=>{const r=document.querySelector('#subs').getBoundingClientRect(); return r.top>=0&&r.top<400;}));
    await pg.goto(B+'/contact'); await pg.click('#bid button[type=submit]'); await pg.waitForTimeout(200);
    log.push('empty form: '+await pg.textContent('#bid .form-status'));
    await pg.fill('#f-name','QA'); await pg.fill('#f-email','qa@example.com'); await pg.click('#bid button[type=submit]'); await pg.waitForTimeout(500);
    log.push('valid form: '+await pg.textContent('#bid .form-status'));
    let r=await pg.goto(B+'/residential'); log.push('/residential -> '+new URL(pg.url()).pathname);
    r=await pg.goto(B+'/no/such/page'); log.push('deep 404: status '+r.status()+' | h1: '+await pg.textContent('h1')+' | styled: '+await pg.evaluate(()=>getComputedStyle(document.querySelector('.site-header')).backgroundColor)+' | logo: '+await pg.evaluate(()=>document.querySelector('.brand svg').getBoundingClientRect().width>50));
    log.push('footer year: '+await pg.textContent('[data-year]'));
    await ctx.close(); }
  { const ctx=await br.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}); await ctx.route(/googletagmanager/,r=>r.abort());
    const pg=await ctx.newPage(); await pg.goto(B+'/about'); await pg.click('.burger'); await pg.waitForTimeout(450);
    log.push('mobile menu: '+await pg.evaluate(()=>{const n=document.querySelector('.nav'),r=n.getBoundingClientRect(); return getComputedStyle(n).visibility+' covers='+(r.width>=389&&r.bottom>=840)+' scrollLocked='+(getComputedStyle(document.body).overflow==='hidden');}));
    await pg.click('.nav > a[href="/contact"]'); await pg.waitForURL('**/contact'); log.push('mobile nav -> '+new URL(pg.url()).pathname+' menuClosed='+await pg.evaluate(()=>!document.body.classList.contains('nav-open')));
    await ctx.close(); }
  await br.close();
  console.log('page/width checks:',checks); console.log('ISSUES ('+issues.length+'):'); [...new Set(issues)].forEach(i=>console.log(' -',i)); console.log('INTERACTIONS:'); log.forEach(l=>console.log(' -',l));
  process.exit(issues.length?1:0);
})();
