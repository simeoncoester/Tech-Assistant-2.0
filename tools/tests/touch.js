const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const ctx = await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 await p.evaluate(() => { const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage('Channel Strip'); st.gear = 'TL Audio VTC';
   pr.chain.channels = Array.from({ length: 12 }, (_, i) => ({ id: 'c' + i, name: 'K' + i, source: '', stages: [i ? newStage('Preamp') : st], notes: '' })); a.productions.push(pr); S.artists = [a]; normalize(); prAutoAttach(st);
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); window.scrollTo(0, 200); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); });
 await p.waitForTimeout(600);
 const cdp = await ctx.newCDPSession(p);
 const drag = async (x0, y0, x1, y1) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] });
   for (let k = 1; k <= 10; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * k / 10, y: y0 + (y1 - y0) * k / 10 }] }); await p.waitForTimeout(16); }
   await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(400); };
 const state = () => p.evaluate(() => [window.scrollY, [...document.querySelectorAll('.pr-pages button')].findIndex(b => b.getAttribute('aria-pressed') === 'true')]);
 await p.evaluate(() => { window._ev = []; ['pointerdown','pointerup','pointercancel'].forEach(t => window.addEventListener(t, e => window._ev.push(t + ':' + (e.target.className && e.target.className.baseVal === undefined ? e.target.className : e.target.tagName)), true)); }); const s0 = await state();
 await drag(300, 500, 120, 440);   // diagonal swipe on the panel
 const s1 = await state();
 console.log(await p.evaluate(() => { const r = document.querySelector('.pr-main').getBoundingClientRect(), v = document.querySelector('.pr-view').getBoundingClientRect(); return [r.left, r.right, r.top, r.bottom, v.left, v.right]; })); await drag(30, 560, 220, 600);   // diagonal swipe on the black area beside the panel
 const s2 = await state(); console.log(await p.evaluate(() => window._ev.join(' ')));
 await drag(200, 620, 210, 250);   // vertical drag: page behind must not scroll
 const s3 = await state();
 console.log(s0, s1, s2, s3, errs.join('|') || 'noerr'); await b.close(); })();
