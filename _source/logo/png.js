// Renders apple-touch-icon.png (repository root) and the brand PNGs (_source/logo/brand) from the SVGs.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.join(__dirname,'..','..'),BRAND=path.join(__dirname,'brand');
(async()=>{const b=await chromium.launch();
for(const [svg,out,w,h] of [[path.join(ROOT,'favicon.svg'),path.join(ROOT,'apple-touch-icon.png'),180,180],[path.join(BRAND,'brand-square-white-on-navy.svg'),path.join(BRAND,'ocmand-logo-square-navy.png'),1200,1200],[path.join(BRAND,'brand-stacked-navy.svg'),path.join(BRAND,'ocmand-logo-stacked-navy.png'),1923,1060],[path.join(BRAND,'brand-stacked-white-on-navy.svg'),path.join(BRAND,'ocmand-logo-stacked-white-on-navy.png'),1923,1060],[path.join(BRAND,'brand-horizontal-navy.svg'),path.join(BRAND,'ocmand-logo-horizontal-navy.png'),2015,344]]){
 const p=await b.newPage({viewport:{width:w,height:h}});const transparent=!svg.includes('white')&&!svg.includes('favicon');
 await p.setContent(`<html><body style="margin:0;background:transparent"><img src="data:image/svg+xml;base64,${fs.readFileSync(svg).toString('base64')}" style="width:${w}px;height:${h}px;display:block"></body></html>`);
 await p.screenshot({path:out,omitBackground:transparent});await p.close();}
await b.close();})();
