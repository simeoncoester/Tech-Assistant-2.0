const { chromium } = require('playwright');
const VPS = [[375,667],[390,844],[768,1024],[1024,1366],[1440,900]];
(async () => {
  const b = await chromium.launch({ args: ['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream'] });
  const issues = [];
  for (const [w,hh] of VPS) {
    for (const lang of ['de','en']) for (const theme of ['dark','ice']) {
    if (lang==='en' && w!==375) continue; if (theme==='ice' && w!==390) continue;
    const ctx = await b.newContext({ viewport: { width: w, height: hh }, permissions: ['microphone'] });
    const page = await ctx.newPage();
    const tag = `${w}x${hh}/${lang}/${theme}`;
    let cur = 'load';
    page.on('pageerror', e => issues.push(`[${tag}] ${cur} PAGEERROR ${e.message}`));
    page.on('console', m => { if (m.type()==='error' && !/fonts\.g|Failed to load resource/.test(m.text())) issues.push(`[${tag}] ${cur} CONSOLE ${m.text()}`); });
    await page.addInitScript(([lang,theme]) => { try { localStorage.setItem('drumtech-onboarded','1'); localStorage.setItem('drumtech-nosplash','1'); sessionStorage.setItem('drumtech-nosplash','1'); localStorage.setItem('drumtech-dev','1'); localStorage.setItem('drumtech-lang',lang); localStorage.setItem('drumtech-theme',theme);} catch(e){} }, [lang,theme]);
    await page.goto('http://localhost:8765/index.html'); await page.waitForTimeout(800);
    // seed
    await page.evaluate(() => {
      const a = { id: newId(), name: 'Testband', productions: [] };
      ['live','studio'].forEach(m => { const p = newProduction(m); p.name = m==='live'?'Sommertour 2026':'Album'; p.drums = [newDrum('Snare','14'), newDrum('Tom','10'), newDrum('Tom','12'), newDrum('Tom','16'), newDrum('Bassdrum','22')];
        p.setlists = [{ id: newId(), mode: m, name: 'Set A', date: '2026-07-01', venue: 'Halle', songs: [1,2,3].map(i => ({ id: newId(), title: 'Song mit sehr langem Titel Nummer ' + i, key: ['C','Am','F#'][i-1], bpm: 90+i*20, sig: '4/4', note: 'Intro leise / Capo 2 / Ende fade', gt: {}, bs: {} })) }];
        a.productions.push(p); });
      S.artists.push(a); normalize(); touch();
      window.__a = a;
    });
    const a = await page.evaluate(() => ({ id: __a.id, live: __a.productions[0], studio: __a.productions[1] }));
    const routes = [
      ['artists',{}],['mode',{artistId:a.id}],['projects',{artistId:a.id,mode:'live'}],
      ...['live','studio'].flatMap(m => { const p = a[m]; const base = {artistId:a.id, mode:m, prodId:p.id};
        return [['home',base],['inst',base],['kits',{...base,inst:'drums'}],['kit',{...base,inst:'drums'}],['kitlist',{...base,inst:'drums'}],['chains',{...base,inst:'drums'}],['console',{...base,inst:'drums'}],
        ...(m === 'live' ? [['setlists',base],['setlist',{...base,setId:p.setlists[0].id}]] : []),['tuner',{...base,inst:'drums',target:p.drums[1].id,tTab:'lugs'}],
        ['ghome',{...base,inst:'guitar'}],['ghome',{...base,inst:'bass'}],['tunings',{...base,inst:'guitar'}],['ginsts',{...base,inst:'guitar'}],['gtuner',{...base,inst:'bass'}],['backups',{...base,inst:'drums'}],['backups',{...base,inst:'guitar'}]]; }),
      ['tuner',{tunerFrom:'free',tTab:'lugs',target:null}],['gtuner',{tunerFrom:'free',inst:'guitar'}],['click',{}]];
    for (const [v,p] of routes) {
      cur = v + (p.mode?'/'+p.mode:'') + (p.inst?'/'+p.inst:'');
      await page.evaluate(([v,p]) => nav(v,p), [v,p]); await page.waitForTimeout(250);
      const got = await page.evaluate(() => route.view);
      if (got !== v) issues.push(`[${tag}] ${cur} REDIRECTED to ${got}`);
      const r = await page.evaluate(() => {
        const out = []; const W = document.documentElement.clientWidth;
        if (document.documentElement.scrollWidth > W + 1) out.push('HSCROLL ' + document.documentElement.scrollWidth + '>' + W);
        const desc = el => el.tagName.toLowerCase() + (el.className && typeof el.className==='string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') + ' "' + (el.textContent||'').trim().slice(0,30) + '"';
        const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.visibility!=='hidden' && s.display!=='none' && r.width>0 && r.height>0; };
        document.querySelectorAll('#app *, #bar *').forEach(el => { if (!vis(el)) return; const r = el.getBoundingClientRect(); if (r.right > W + 1 && getComputedStyle(el).position!=='fixed') { let p=el.parentElement, clipped=false; while(p){const o=getComputedStyle(p).overflowX; if(o!=='visible'){clipped=true;break;} p=p.parentElement;} if(!clipped) out.push('OFFSCREEN ' + desc(el) + ' right=' + Math.round(r.right)); } });
        document.querySelectorAll('.grid, .row, .chips').forEach(c => { const kids=[...c.children].filter(vis); const cr=c.getBoundingClientRect();
          kids.forEach(k => { const r=k.getBoundingClientRect(); if (r.right>cr.right+1.5 || r.left<cr.left-1.5) out.push('OVERFLOW-IN ' + desc(c) + ' child ' + desc(k)); });
          for (let i=0;i<kids.length;i++) for (let j=i+1;j<kids.length;j++){const A=kids[i].getBoundingClientRect(),B=kids[j].getBoundingClientRect(); const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left), oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top); if(ox>2&&oy>2&&getComputedStyle(kids[i]).position!=='absolute'&&getComputedStyle(kids[j]).position!=='absolute') out.push('OVERLAP in '+desc(c)+': '+desc(kids[i])+' / '+desc(kids[j]));} });
        document.querySelectorAll('.card button, .card .btn').forEach(bt => { if(!vis(bt)) return; const card = bt.closest('.card'); const cr=card.getBoundingClientRect(), r=bt.getBoundingClientRect(); if (r.right>cr.right+1.5||r.left<cr.left-1.5||r.bottom>cr.bottom+1.5) out.push('BTN-OUTSIDE-CARD ' + desc(bt)); });
        return [...new Set(out)].slice(0,8);
      });
      r.forEach(x => issues.push(`[${tag}] ${cur} ${x}`));
      if (w===390 && lang==='de' && theme==='dark') await page.screenshot({ path: `${process.env.S}/shot-${cur.replace(/\//g,'_')}.png`, fullPage: true });
    }
    await ctx.close();
  }}
  await b.close();
  console.log([...new Set(issues)].join('\n') || 'NO ISSUES');
})();
