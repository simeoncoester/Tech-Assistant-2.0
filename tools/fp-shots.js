const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const issues = []; const dir = process.argv[2];
 const p = await (await b.newContext({ viewport:{width:1440,height:900}, serviceWorkers:'block' })).newPage(); p.on('pageerror',e=>issues.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const gears = (process.argv[3] || 'API 560,API 550B,Chandler Curve Bender,GML 8200,Maag EQ4').split(',');
 for (const [i, g] of gears.entries()) {
  await p.evaluate(g => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); const a={id:'A',name:'Band',productions:[]}; const pr=newProduction('studio'); pr.id='P'; const st=newStage('EQ'); st.gear=g; pr.chain.channels=[{id:'c1',name:'Vox',source:'',stages:[st],notes:''}]; a.productions.push(pr); S.artists=[a]; normalize(); prAutoAttach(st);
    nav('chain',{artistId:'A',mode:'studio',prodId:'P',inst:'drums',chainOwner:'prod'}); showPhotoRecall(st, S.devTpls.find(t=>t.id===st.photo.tplId), false); }, g);
  await p.waitForTimeout(500); await p.screenshot({ path: `${dir}/new${i}.png` });
 }
 // slider: drag the 1 kHz band and read the value
 await p.evaluate(() => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); const st = P().chain.channels[0].stages[0]; st.gear = 'API 560'; delete st.photo; prAutoAttach(st); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); });
 await p.waitForTimeout(400); await p.click('.pr-seg button:has-text("Einstellen")'); await p.waitForTimeout(150);
 const sl = p.locator('.pr-ctrl.t-slider').nth(4); const bb = await sl.boundingBox();
 await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down(); await p.mouse.move(bb.x + bb.width / 2 + bb.width * .2, bb.y + bb.height / 2, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(200);
 const r = await p.evaluate(() => { const st = P().chain.channels[0].stages[0], t = S.devTpls.find(x => x.id === st.photo.tplId), c = t.ctrls[4]; return [c.name, c.type, prVal(c, st.photo.vals[c.id]), prVal(t.ctrls[0], st.photo.vals[t.ctrls[0].id] || {})]; });
 console.log('slider', r); if (r[1] !== 'slider' || !/^\+\d/.test(r[2]) || r[3] !== '0 dB') issues.push('slider ' + r);
 await p.screenshot({ path: `${dir}/slider.png` });
 await b.close(); console.log(issues.join('\n') || 'NO ISSUES'); })();
