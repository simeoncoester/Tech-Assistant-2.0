const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ viewport: { width: 1200, height: 900 }, serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 await p.evaluate(() => { const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage('EQ'); st.gear = 'Link Audio SLQ';
   const own = { id: 'own', name: 'Link Audio SLQ', gear: 'Link Audio SLQ', kind: 'EQ', ar: .29, ctrls: [
     { id: 'a', name: 'HF', type: 'knob', x: .25, y: .11, r: .3 }, { id: 'b', name: 'Khz', type: 'knob', x: .72, y: .2, r: .3 }, { id: 'c', name: 'HMF', type: 'knob', x: .25, y: .27, r: .3 }, { id: 'd', name: 'LMF', type: 'knob', x: .3, y: .62, r: .3 }, { id: 'e', name: '', type: 'push', x: .75, y: .52, r: .1 }] };
   S.devTpls = [own]; st.photo = { tplId: 'own', vals: { a: { pos: .8 }, b: { pos: .3 }, c: { pos: .6 }, d: { pos: .2 }, e: { in: true } } };
   pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize();
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); showPhotoRecall(st, own, false); window._st = st; });
 await p.waitForTimeout(400); await p.click('.pr-eye'); await p.waitForTimeout(600);
 const r = await p.evaluate(() => { const st = window._st, t = S.devTpls.find(x => x.id === st.photo.tplId); return [t.builtin, Object.entries(st.photo.vals).map(([k, v]) => t.ctrls.find(c => c.id === k).name + '=' + JSON.stringify(v)).join('; '), !!document.querySelector('.pr-photo.fpreal')]; });
 console.log(r); await p.screenshot({ path: 'out/eye.png' });
 await p.click('.pr-eye'); await p.waitForTimeout(500);
 console.log(await p.evaluate(() => { const st = window._st; return [st.photo.tplId, JSON.stringify(st.photo.vals)]; }), errs.join('|') || 'noerr'); await b.close(); })();
