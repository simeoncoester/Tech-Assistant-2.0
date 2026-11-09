const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ viewport: { width: 900, height: 1400 }, serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 await p.evaluate(() => { const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage('EQ'); st.gear = 'Link Audio SLQ';
   S.devTpls = [{ id: 'own', name: 'Link Audio SLQ', gear: 'Link Audio SLQ', kind: 'EQ', ar: .29, ctrls: [{ id: 'a', name: 'HF', type: 'knob', x: .25, y: .11, r: .3 }] }]; st.photo = { tplId: 'own', vals: { a: { pos: .8 } } };
   pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize(); openSet.add('c1'); window._st = st;
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); });
 await p.waitForTimeout(400);
 const n = await p.locator('.pr-choice button').count();
 await p.locator('.pr-choice button').nth(1).click(); await p.waitForTimeout(300);
 const r = await p.evaluate(() => [S.devTpls.find(t => t.id === window._st.photo.tplId).builtin, document.querySelector('.pr-choice button[aria-pressed=true]').textContent]);
 // dev manager hides builtins
 await p.evaluate(() => devManager()); await p.waitForTimeout(200);
 const items = await p.evaluate(() => [...document.querySelectorAll('.dev-item b')].map(x => x.textContent));
 await p.evaluate(() => document.querySelectorAll('.sheet-ov').forEach(x => x.remove()));
 // guitar extra amp
 await p.evaluate(() => { const i = { id: 'g1', inst: 'guitar', name: 'Strat', model: '', amp: 'Fender Twin Reverb', ampMic: 'Shure SM57', di: '', notes: '' }; P().instruments = [i]; nav('ginst', { ginstId: 'g1', inst: 'guitar', mode: 'studio' }); });
 await p.waitForTimeout(400);
 const before = await p.locator('.mic-add').count();
 await p.locator('.mic-row .mic-add').first().click(); await p.waitForTimeout(300);
 const labels = await p.evaluate(() => [...document.querySelectorAll('.field label, .field > span, label')].map(x => x.textContent.trim()).filter(t => /Amp|Mikrofon am Amp/.test(t)));
 await p.screenshot({ path: 'out/amps.png' });
 console.log(n, r, items, before, labels, errs.join('|') || 'noerr'); await b.close(); })();
