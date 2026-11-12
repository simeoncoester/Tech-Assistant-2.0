// tab bar stays at the bottom of the screen while the page scrolls (iPhone size, both themes)
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [], out = [];
 for (const theme of ['glass', 'ice']) { const p = await (await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(th => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); localStorage.setItem('drumtech-dev','1'); localStorage.setItem('drumtech-theme', th); }, theme);
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(400);
  await p.evaluate(() => { const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('live'); pr.id = 'P'; pr.name = 'Tour'; pr.drums = [newDrum('Snare', '14'), newDrum('Tom', '12')];
    pr.instruments = Array.from({ length: 9 }, (_, i) => ({ id: 'g' + i, inst: 'guitar', name: 'Gitarre ' + (i + 1), tuningId: '', amp: '', ampMic: '' })); a.productions.push(pr); S.artists = [a]; normalize(); });
  const views = [['home', { inst: 'drums' }], ['ghome', { inst: 'guitar' }], ['ginsts', { inst: 'guitar' }], ['ginst', { inst: 'guitar', instId: 'g0' }], ['tuner', { inst: 'drums' }], ['kit', { inst: 'drums' }], ['setlists', { inst: 'drums' }]];
  for (const [v, patch] of views) { const ok = await p.evaluate(([v, patch]) => { try { nav(v, { artistId: 'A', mode: 'live', prodId: 'P', ...patch }); return route.view; } catch (e) { return 'ERR ' + e.message; } }, [v, patch]); await p.waitForTimeout(250);
   if (v === 'tuner') { const s = p.locator('.dt-set').first(); if (await s.count()) { await s.click(); await p.waitForTimeout(200); } }
   const m = async () => p.evaluate(() => { const tb = document.getElementById('tabbar'); if (!tb || tb.hidden) return null; const r = tb.getBoundingClientRect(); return { bottomGap: Math.round(innerHeight - r.bottom), top: Math.round(r.top), sh: document.documentElement.scrollHeight, ih: innerHeight, y: Math.round(scrollY), pos: getComputedStyle(tb).position }; });
   const a0 = await m(); if (!a0) { out.push(`${theme} ${v}->${ok}: no tabbar`); continue; }
   await p.evaluate(() => window.scrollTo(0, 150)); await p.waitForTimeout(80); const a1 = await m(); await p.evaluate(() => window.scrollTo(0, 99999)); await p.waitForTimeout(80); const a2 = await m();
   const good = a0.bottomGap === a1.bottomGap && a1.bottomGap === a2.bottomGap && a0.bottomGap >= 0 && a0.bottomGap < 60;
   out.push(`${good ? 'OK ' : 'BAD'} ${theme} ${ok}: gap ${a0.bottomGap}/${a1.bottomGap}/${a2.bottomGap} scrollH ${a0.sh} vs ${a0.ih} maxY ${a2.y} ${a0.pos}`);
   if (theme === 'glass' && ['ginsts', 'tuner', 'home'].includes(v)) await p.screenshot({ path: `out/tab-${v}.png` }); }
 }
 console.log(out.join("\n")); console.log((out.every(l => l.startsWith("OK")) ? "TAB OK " : "TAB BAD ") + (errs.join("|") || "noerr")); await b.close(); })();
