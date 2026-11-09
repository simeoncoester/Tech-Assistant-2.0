const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const open = async (g, kind) => { await p.evaluate(([g, kind]) => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage(kind); st.gear = g; pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize(); prAutoAttach(st); window._st = st;
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, [g, kind]); await p.waitForTimeout(700); };
 await open('TL Audio VTC Master Section', 'Master Section');
 for (let i = 0; i < 5; i++) { await p.locator('.pr-pages button').nth(i).click(); await p.waitForTimeout(300); await p.screenshot({ path: `out/pg${i}.png` }); }
 await p.locator('.pr-pages button').nth(3).click(); await p.waitForTimeout(200);
 await p.click('.pr-seg button:has-text("Einstellen")'); await p.waitForTimeout(200);
 const mf = await p.evaluate(() => { const t = S.devTpls.find(x => x.id === window._st.photo.tplId); const i = t.ctrls.findIndex(c => c.name === 'Master Fader'); return i; });
 const el = p.locator('.pr-layer .pr-ctrl').nth(mf); const bb = await el.boundingBox();
 await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height * .2); await p.mouse.down(); await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height * .4, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(200);
 const v = await p.evaluate(() => { const st = window._st, t = S.devTpls.find(x => x.id === st.photo.tplId), c = t.ctrls.find(c => c.name === 'Master Fader'); return prVal(c, st.photo.vals[c.id]); });
 await open('Klark Teknik 2A-KT', 'Kompressor'); await p.screenshot({ path: 'out/kt.png' });
 const txt = await p.evaluate(() => !!document.querySelector('.pr-txt svg text'));
 console.log('master fader', v, 'txt', txt, errs.join('|') || 'noerr'); await b.close(); })();
