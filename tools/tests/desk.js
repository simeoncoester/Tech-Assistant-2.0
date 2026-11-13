// Computer handling: mouse, wheel/trackpad and keyboard. Expects "DESK OK".
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const bad = []; const ok = (c, m) => { if (!c) bad.push(m); };
for (const [w, hh] of [[1440, 900], [1280, 720]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: hh }, serviceWorkers: 'block' }); const p = await ctx.newPage(); const T = `[${w}x${hh}] `;
  p.on('pageerror', e => bad.push(T + 'PAGEERROR ' + e.message));
  await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded', '1'); sessionStorage.setItem('drumtech-nosplash', '1'); localStorage.setItem('drumtech-nosplash', '1'); localStorage.setItem('drumtech-dev', '1'); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(400);
  await p.evaluate(() => { const a = { id: 'A', name: 'Band', productions: [] }; const st = (k, g) => { const s = newStage(k); s.gear = g; return s; };
    const pr = newProduction('studio'); pr.id = 'PS'; pr.name = 'Album'; pr.drums = [newDrum('Bassdrum', '22'), newDrum('Snare', '14')];
    pr.chain.channels = Array.from({ length: 5 }, (_, i) => ({ id: 'c' + i, name: 'Kanal ' + (i + 1), source: '', stages: [st('Preamp', 'Neve 1073'), st('Kompressor', 'Universal Audio 1176LN')] }));
    const pl = newProduction('live'); pl.id = 'PL'; pl.name = 'Tour'; const song = (t, i) => ({ id: 'so' + i, title: t, key: 'A-Moll', bpm: 120, sig: '4/4', note: '', instNotes: [], extra: {} });
    pl.setlists = [{ id: 'SL', mode: 'live', name: 'Set', songs: ['Eins', 'Zwei', 'Drei', 'Vier', 'Fünf', 'Sechs', 'Sieben', 'Acht', 'Neun', 'Zehn', 'Elf', 'Zwölf', 'Dreizehn', 'Vierzehn'].map(song) }];
    a.productions.push(pr, pl); S.artists = [a]; normalize(); fpAttachAll(); touch(); });
  const clean = () => p.evaluate(() => document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .stage, .stage-song, .st-pov').forEach(x => x.remove()));
  const cnt = sel => p.locator(sel).count();
  // 1 photo recall: wheel zoom, pan, keys
  await p.evaluate(() => { nav('chain', { artistId: 'A', mode: 'studio', prodId: 'PS', inst: 'drums', chainOwner: 'prod' }); const s = S.artists[0].productions[0].chain.channels[0].stages[0]; showPhotoRecall(s, S.devTpls.find(t => t.id === s.photo.tplId), false); });
  await p.waitForTimeout(500);
  const pw = () => p.evaluate(() => { const r = document.querySelector('.pr-photo').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.left), Math.round(r.top)]; });
  const page0 = () => p.evaluate(() => [...document.querySelectorAll('.pr-ov [aria-pressed="true"]')].map(x => x.textContent.trim()).join('|'));
  const m = await p.evaluate(() => { const r = document.querySelector('.pr-main').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
  const w0 = await pw(); await p.mouse.move(m[0], m[1]); await p.keyboard.down('Control'); await p.mouse.wheel(0, -300); await p.keyboard.up('Control'); await p.waitForTimeout(200);
  const w1 = await pw(); ok(w1[0] > w0[0] * 1.3, T + `ctrl+wheel does not zoom (${w0[0]} -> ${w1[0]})`);
  await p.mouse.wheel(120, 0); await p.waitForTimeout(150); const w2 = await pw(); ok(w2[1] < w1[1] - 20, T + `wheel does not pan the zoomed photo (${w1[1]} -> ${w2[1]})`);
  await p.keyboard.press('0'); await p.waitForTimeout(150); const w3 = await pw(); ok(Math.abs(w3[0] - w0[0]) < 3, T + 'key 0 does not reset zoom');
  await p.keyboard.press('+'); await p.waitForTimeout(150); ok((await pw())[0] > w0[0] * 1.3, T + 'key + does not zoom'); await p.keyboard.press('-'); await p.waitForTimeout(150);
  const pa = await page0(); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(350); const pb = await page0(); ok(pa !== pb, T + `arrow key does not change the page (${pa})`);
  // mouse drag across the photo changes the page too
  await p.mouse.move(m[0] + 150, m[1]); await p.mouse.down(); await p.mouse.move(m[0] - 150, m[1], { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(400); ok((await page0()) !== pb, T + 'mouse drag does not change the page');
  // set a knob with the mouse
  await p.locator('.pr-ov button:has-text("Einstellen")').first().click(); await p.waitForTimeout(200); await p.evaluate(() => { const all = document.querySelector('.pr-ov [role="tablist"] button, .pr-pages button'); });
  const kb = await p.evaluate(() => { const k = [...document.querySelectorAll('.pr-ctrl')].find(x => { const r = x.getBoundingClientRect(); return /knob/.test(x.className) && r.width > 8 && r.left > 0 && r.right < innerWidth && r.top > 60 && r.bottom < innerHeight; }); if (!k) return null; const r = k.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
  if (kb) { const v0 = await p.evaluate(() => JSON.stringify(S.artists[0].productions[0].chain.channels[0].stages[0].photo.vals)); await p.mouse.move(kb[0], kb[1]); await p.mouse.down(); await p.mouse.move(kb[0], kb[1] - 60, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(200);
    ok(v0 !== await p.evaluate(() => JSON.stringify(S.artists[0].productions[0].chain.channels[0].stages[0].photo.vals)), T + 'mouse drag does not turn a knob'); } else bad.push(T + 'no knob found in photo recall');
  await p.evaluate(() => document.querySelectorAll('.sheet-ov').forEach(x => x.remove())); await p.keyboard.press('Escape'); await p.waitForTimeout(200); ok(!(await cnt('.pr-ov')), T + 'Escape does not close the photo recall');
  // 2 Escape closes pop-ups and overlays
  await clean(); await p.click('.gear-btn'); await p.waitForTimeout(200); ok(await cnt('.sheet-ov'), T + 'settings did not open'); await p.keyboard.press('Escape'); await p.waitForTimeout(200); ok(!(await cnt('.sheet-ov')), T + 'Escape does not close settings');
  const hb = p.locator('header button[aria-label*="Hilfe"], header .help-btn').first(); if (await hb.count()) { await hb.click(); await p.waitForTimeout(300); ok(await cnt('#onb'), T + 'help did not open'); const t0 = await p.evaluate(() => document.querySelector('#onb').textContent.slice(0, 60)); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(300); ok(t0 !== await p.evaluate(() => (document.querySelector('#onb') || {}).textContent?.slice(0, 60)), T + 'arrow key does not turn help slides'); await p.keyboard.press('Escape'); await p.waitForTimeout(300); ok(!(await cnt('#onb')), T + 'Escape does not close help'); }
  await clean(); await p.evaluate(() => { nav('setlists', { artistId: 'A', mode: 'live', prodId: 'PL', inst: 'drums' }); showStage(S.artists[0].productions[1].setlists[0]); }); await p.waitForTimeout(400);
  await p.mouse.move(w / 2, hh / 2); await p.mouse.wheel(0, 400); await p.waitForTimeout(250); ok(await p.evaluate(() => { const s = document.querySelector('.stage'); return [s, ...s.querySelectorAll('*')].some(x => x.scrollTop > 0) || scrollY > 0; }), T + 'mouse wheel does not scroll the large view');
  { const vb = p.locator('.stage button:has-text("Ansicht"), .stage button[aria-label*="Ansicht"]').first(); await vb.click(); await p.waitForTimeout(250); ok(await cnt('.st-pov'), T + 'view panel did not open'); await p.keyboard.press('Escape'); await p.waitForTimeout(250); ok(!(await cnt('.st-pov')) && await cnt('.stage'), T + 'Escape with the view panel open must close only the panel'); }
  await p.keyboard.press('Escape'); await p.waitForTimeout(250); ok(!(await cnt('.stage')), T + 'Escape does not close the large view');
  await p.evaluate(() => showStageSong(S.artists[0].productions[1].setlists[0], 0)); await p.waitForTimeout(300); const s0 = await p.evaluate(() => document.querySelector('.stage-song').textContent.slice(0, 40)); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(350);
  ok(s0 !== await p.evaluate(() => document.querySelector('.stage-song').textContent.slice(0, 40)), T + 'arrow key does not change the song in show mode'); await p.keyboard.press('Escape'); await p.waitForTimeout(250); ok(!(await cnt('.stage-song')), T + 'Escape does not close show mode');
  // 3 setlist editor: wheel scroll and reorder with the mouse
  await clean(); await p.evaluate(() => nav('setlist', { artistId: 'A', mode: 'live', prodId: 'PL', inst: 'drums', setId: 'SL' })); await p.waitForTimeout(400);
  await p.mouse.move(w / 2, hh / 2); await p.mouse.wheel(0, 300); await p.waitForTimeout(200); ok(await p.evaluate(() => scrollY > 50), T + 'mouse wheel does not scroll the page'); await p.evaluate(() => scrollTo(0, 0));
  const rows = await p.evaluate(() => [...document.querySelectorAll('.song .s-head')].slice(0, 3).map(x => { const r = x.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }));
  if (rows.length >= 3) { await p.mouse.move(rows[0][0], rows[0][1]); await p.mouse.down(); await p.mouse.move(rows[0][0], rows[0][1] + 10, { steps: 2 }); await p.mouse.move(rows[2][0], rows[2][1] + 12, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(300);
    ok(await p.evaluate(() => S.artists[0].productions[1].setlists[0].songs[0].title !== 'Eins'), T + 'mouse drag does not reorder songs'); } else bad.push(T + 'song rows not found: ' + rows.length);
  // 4 mixer: fader with mouse, double click resets, arrow keys
  await clean(); await p.evaluate(() => nav('console', { artistId: 'A', mode: 'studio', prodId: 'PS', inst: 'drums', chainOwner: 'prod' })); await p.waitForTimeout(500);
  const fv = () => p.evaluate(() => S.artists[0].productions[0].chain.channels[0].mix.fader); const fb = await p.locator('.fader').first().boundingBox();
  await p.mouse.move(fb.x + fb.width / 2, fb.y + fb.height * .5); await p.mouse.down(); await p.mouse.move(fb.x + fb.width / 2, fb.y + fb.height * .8, { steps: 5 }); await p.mouse.up(); const f1 = await fv(); ok(f1 < 0, T + 'mouse drag does not move the fader ' + f1);
  await p.mouse.dblclick(fb.x + fb.width / 2, fb.y + fb.height * .5); await p.waitForTimeout(200); ok((await fv()) === 0, T + 'double click does not reset the fader ' + await fv());
  ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), T + 'sideways scroll in the mixer');
  await ctx.close(); }
await b.close(); console.log(bad.join('\n') || 'DESK OK'); })();
