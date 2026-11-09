// Foto-Recall auf iPhone-Größe: Lupe, Doppeltipp, Zwei-Finger-Zoom, Verschieben, automatische Seiten
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const ctx = await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const open = async (g, kind) => { await p.evaluate(([g, kind]) => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); for (const k in prPage) delete prPage[k]; const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage(kind); st.gear = g; pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize(); prAutoAttach(st); window._st = st;
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, [g, kind]); await p.waitForTimeout(600); };
 const W = () => p.evaluate(() => { const v = document.querySelector('.pr-view').getBoundingClientRect(), w = document.querySelector('.pr-photo').getBoundingClientRect(); return [Math.round(v.width), Math.round(v.height), Math.round(w.width), Math.round(w.left)]; });
 const fail = []; const ok = (c, m) => { if (!c) fail.push(m); };
 await open('Universal Audio 1176LN', 'Kompressor');
 const pages = await p.locator('.pr-pages button').allTextContents(); ok(pages.join('|') === 'Alles|Links|Rechts', 'auto pages ' + pages);
 const w0 = await W();
 await p.click('.pr-zoom'); await p.waitForTimeout(150); const w1 = await W(); ok(w1[2] > w0[2] * 1.9 && w1[1] > w0[1] * 1.9, 'lupe ' + w0 + ' -> ' + w1);
 ok(await p.getAttribute('.pr-zoom', 'aria-pressed') === 'true', 'aria-pressed');
 // drag pans, no page change while zoomed
 const m = await p.locator('.pr-main').boundingBox(); const cx = m.x + m.width / 2, cy = m.y + m.height / 2;
 await p.mouse.move(cx + 100, cy); await p.mouse.down(); await p.mouse.move(cx - 100, cy, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(150);
 const w2 = await W(); ok(w2[3] < w1[3] - 150, 'pan ' + w1 + ' -> ' + w2); ok(await p.locator('.pr-pages button[aria-pressed=true]').textContent() === 'Alles', 'page changed while zoomed');
 await p.screenshot({ path: 'out/zoom1.png' });
 await p.click('.pr-zoom'); await p.waitForTimeout(150); const w3 = await W(); ok(w3[2] === w0[2], 'zoom out ' + w3);
 // double tap zooms in and out
 await p.mouse.click(cx, cy); await p.mouse.click(cx, cy); await p.waitForTimeout(150); const w4 = await W(); ok(w4[2] > w0[2] * 1.9, 'double tap in ' + w4);
 await p.waitForTimeout(400); await p.mouse.click(cx, cy); await p.mouse.click(cx, cy); await p.waitForTimeout(150); ok((await W())[2] === w0[2], 'double tap out');
 // swipe still changes the page when not zoomed
 await p.waitForTimeout(400); await p.mouse.move(cx + 100, cy); await p.mouse.down(); await p.mouse.move(cx - 100, cy, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(300);
 ok(await p.locator('.pr-pages button[aria-pressed=true]').textContent() === 'Links', 'swipe page');
 // pinch with two touch points (CDP)
 const cdp = await ctx.newCDPSession(p); const tp = (x, id) => ({ x, y: cy, id });
 await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [tp(cx - 30, 0), tp(cx + 30, 1)] });
 for (let i = 1; i <= 5; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [tp(cx - 30 - i * 15, 0), tp(cx + 30 + i * 15, 1)] });
 await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(200);
 const w5 = await W(); ok(await p.getAttribute('.pr-zoom', 'aria-pressed') === 'true' && w5[2] > 1000, 'pinch ' + w5);
 // set mode: a knob still turns while zoomed, value is kept
 await p.click('.pr-seg button:has-text("Einstellen")'); await p.waitForTimeout(150);
 const kb = await p.evaluate(() => { const v = document.querySelector('.pr-view').getBoundingClientRect(); const el = [...document.querySelectorAll('.pr-layer .pr-ctrl.t-knob')].find(e => { const r = e.getBoundingClientRect(); const x = r.left + r.width / 2, y = r.top + r.height / 2; return x > v.left + 30 && x < v.right - 30 && y > v.top + 70 && y < v.bottom - 10; }); const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
 await p.mouse.move(kb[0], kb[1]); await p.mouse.down(); await p.mouse.move(kb[0], kb[1] - 60, { steps: 5 }); await p.mouse.up(); await p.waitForTimeout(150);
 ok(await p.evaluate(() => Object.values(window._st.photo.vals).some(v => v.pos > .1)), 'knob turn while zoomed');
 await p.screenshot({ path: 'out/zoom2.png' });
 console.log(fail.join('\n') || 'ZOOM OK', errs.join('|') || 'noerr'); await b.close(); })();
