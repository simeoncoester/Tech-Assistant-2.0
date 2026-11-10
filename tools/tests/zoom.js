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
 // one layer: picture, lettering and controls keep exactly the same place on the plate at every zoom, in every mode
 const geo = () => p.evaluate(() => { const ph = document.querySelector('.pr-photo'), w = ph.getBoundingClientRect(); const rel = r => [(r.left - w.left) / w.width, (r.top - w.top) / w.height, r.width / w.width, r.height / w.height].map(v => v.toFixed(3)).join(',');
   return { lay: ph.offsetWidth, parts: [ph.querySelector('img'), ph.querySelector('.pr-txt svg'), ph.querySelector('.pr-layer')].map(e => rel(e.getBoundingClientRect())).join(' '), ctrls: [...ph.querySelectorAll('.pr-layer .pr-ctrl')].map(c => rel(c.getBoundingClientRect())).join(' '), vals: JSON.stringify(window._st.photo.vals) }; });
 for (const [g, kind] of [['Universal Audio 1176LN', 'Kompressor'], ['TL Audio VTC', 'Channel Strip'], ['API 560', 'EQ']]) for (const md of ['Einstellen', 'Regler setzen']) {
  await open(g, kind); await p.click(`.pr-seg button:has-text("${md}")`); await p.waitForTimeout(200); const g0 = await geo();
  // pinch that starts on a control: zooms, but changes no value and moves no control
  const kc = await p.evaluate(() => { const r = document.querySelector('.pr-layer .pr-ctrl').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: kc[0], y: kc[1], id: 0 }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: kc[0] - 12, y: kc[1] - 12, id: 0 }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: kc[0] - 12, y: kc[1] - 12, id: 0 }, { x: kc[0] + 60, y: kc[1] + 40, id: 1 }] });
  for (let i = 1; i <= 6; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: kc[0] - 12 - i * 10, y: kc[1] - 12 - i * 6, id: 0 }, { x: kc[0] + 60 + i * 12, y: kc[1] + 40 + i * 8, id: 1 }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(250);
  // then a one-finger drag beside the controls moves the detail
  const free = await p.evaluate(() => { const v = document.querySelector('.pr-view').getBoundingClientRect(), rs = [...document.querySelectorAll('.pr-layer .pr-ctrl')].map(c => c.getBoundingClientRect());
    for (let y = v.top + 14; y < v.bottom - 14; y += 9) for (let x = v.left + 14; x < v.right - 14; x += 9) if (document.elementFromPoint(x, y)?.classList.contains('pr-layer') && rs.every(r => x < r.left - 16 || x > r.right + 16 || y < r.top - 16 || y > r.bottom + 16)) return [x, y]; return null; });
  if (free) { const before = await p.evaluate(() => document.querySelector('.pr-photo').getBoundingClientRect().left); await p.mouse.move(free[0], free[1]); await p.mouse.down(); await p.mouse.move(free[0] + 70, free[1] + 50, { steps: 5 }); await p.mouse.up(); await p.waitForTimeout(200);
    const after = await p.evaluate(() => document.querySelector('.pr-photo').getBoundingClientRect().left); ok(Math.abs(after - before) > 20, `${g}/${md} pan did not move the plate`); } else fail.push(`${g}/${md} no free spot found`);
  const g1 = await geo(), tag = `${g}/${md}`;
  ok(await p.getAttribute('.pr-zoom', 'aria-pressed') === 'true', tag + ' no zoom');
  ok(g1.parts === '0.000,0.000,1.000,1.000 0.000,0.000,1.000,1.000 0.000,0.000,1.000,1.000', tag + ' layers apart ' + g1.parts);
  const near = (a, b) => { const A = a.split(/[ ,]/).map(Number), B = b.split(/[ ,]/).map(Number); return A.length === B.length && A.every((v, i) => Math.abs(v - B[i]) <= .0025); }; ok(near(g1.ctrls, g0.ctrls), tag + ' controls moved'); ok(g1.vals === g0.vals, `${tag} values changed ${g0.vals} -> ${g1.vals}`);
  ok(await p.locator('.pr-pop-ov, .sheet-ov').count() === 0, tag + ' pop-up opened by the gesture'); }
 // drawn faceplates: "Regler setzen" stays, but no rename and the menu only resets the values or takes the faceplate off the stage
 await open('TL Audio VTC Master Section', 'Master Section');
 ok(await p.locator('.pr-seg button:has-text("Regler setzen")').isVisible(), 'faceplate: Regler setzen missing');
 await p.click('.pr-title'); await p.waitForTimeout(200); ok(await p.locator('.sheet-ov').count() === 0, 'faceplate: rename opened');
 await p.click('.pr-menu[aria-label="Weitere Aktionen"]'); await p.waitForTimeout(250);
 const items = await p.locator('.sheet-ov button').allTextContents(); ok(items.join('|') === 'Werte zurücksetzen|Von Stufe entfernen|Abbrechen', 'faceplate menu: ' + items.join('|'));
 // an own photo keeps every option
 await p.evaluate(async () => { document.querySelectorAll('.sheet-ov, .pr-ov').forEach(x => x.remove()); const c = document.createElement('canvas'); c.width = 300; c.height = 150; c.getContext('2d').fillRect(0, 0, 300, 150); const t = { id: 'own1', name: 'Mein Gerät', kind: 'EQ', ar: 2, ctrls: [{ id: 'k', name: 'Gain', type: 'knob', x: .5, y: .5, r: .1 }] }; S.devTpls.push(t); await FileStore.put('dev-own1', { data: c.toDataURL('image/png') }); const st = P().chain.channels[0].stages[0]; st.gear = 'Mein Gerät'; st.photo = { tplId: 'own1', vals: {} }; showPhotoRecall(st, t, false); });
 await p.waitForTimeout(500); ok(await p.locator('.pr-seg button:has-text("Regler setzen")').isVisible(), 'own photo: Regler setzen missing');
 await p.click('.pr-menu[aria-label="Weitere Aktionen"]'); await p.waitForTimeout(250);
 const own = await p.locator('.sheet-ov button').allTextContents(); ok(['Gerät umbenennen', 'Zuschneiden', 'Foto ersetzen', 'Werte zurücksetzen', 'Foto löschen', 'Von Stufe entfernen'].every(x => own.includes(x)), 'own photo menu: ' + own.join('|'));
 console.log(fail.join('\n') || 'ZOOM OK', errs.join('|') || 'noerr'); await b.close(); })();
