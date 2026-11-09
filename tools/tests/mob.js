const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 for (const [i, g] of ['API 312', 'Neve 1073LB (500er)'].entries()) {
 await p.evaluate(g => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); const a={id:'A',name:'Band',productions:[]}; const pr=newProduction('studio'); pr.id='P'; const st=newStage('Preamp'); st.gear=g; pr.chain.channels=[{id:'c1',name:'Vox',source:'',stages:[st],notes:''}]; a.productions.push(pr); S.artists=[a]; normalize(); prAutoAttach(st);
    nav('chain',{artistId:'A',mode:'studio',prodId:'P',inst:'drums',chainOwner:'prod'}); showPhotoRecall(st, S.devTpls.find(t=>t.id===st.photo.tplId), false); }, g);
 await p.waitForTimeout(600);
 if (i === 0) { await p.click('.pr-seg button:has-text("Einstellen")'); await p.waitForTimeout(150); await p.locator('.pr-ctrl.t-push').first().click(); await p.waitForTimeout(200); }
 await p.screenshot({ path: `out/mob${i}.png` }); }
 console.log(errs.join('|') || 'noerr'); await b.close(); })();
