// Lesbarkeit auf dem iPhone: kleinste Schrift- und Reglergröße jedes Faceplates im Foto-Recall (beste Seite, ohne Zoom). Aufruf: node tools/fp-legible.js ["Gerät A,Gerät B"]
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const names = await p.evaluate(() => Object.keys(FACEPLATES)); const out = [];
 const only = process.argv[2] ? process.argv[2].split(',') : null;
 for (const g of names) { if (only && !only.includes(g)) continue;
  await p.evaluate(g => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); for (const k in prPage) delete prPage[k]; const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage(FACEPLATES[g].kind || 'EQ'); st.gear = g; pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize(); prAutoAttach(st); window._st = st;
   nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, g);
  await p.waitForTimeout(350);
  const n = await p.locator('.pr-pages button').count(); const best = {}; let ctrlMin = {};
  for (let i = 0; i < Math.max(1, n); i++) { if (n) { await p.locator('.pr-pages button').nth(i).click(); await p.waitForTimeout(120); }
    const r = await p.evaluate(() => { const v = document.querySelector('.pr-view').getBoundingClientRect(); const sc = document.querySelector('.pr-txt svg').getBoundingClientRect().width / 1000;
      const T = [...document.querySelectorAll('.pr-txt svg text')].map((t, k) => { const bb = t.getBoundingClientRect(); const fs = parseFloat(t.getAttribute('font-size') || getComputedStyle(t).fontSize) ; const vis = bb.left >= v.left - 1 && bb.right <= v.right + 1 && bb.top >= v.top - 1 && bb.bottom <= v.bottom + 1; return [k, t.textContent, vis ? fs * sc : 0]; }).filter(t => t[1].trim());
      const C = [...document.querySelectorAll('.pr-layer .pr-ctrl')].map((c, k) => { const bb = c.getBoundingClientRect(); const vis = bb.left + bb.width / 2 >= v.left && bb.left + bb.width / 2 <= v.right && bb.top + bb.height / 2 >= v.top && bb.top + bb.height / 2 <= v.bottom; return [k, vis ? Math.min(bb.width, bb.height) : 0]; });
      return { T, C, vw: v.width, vh: v.height }; });
    r.T.forEach(([k, t, s]) => { if (!best[k] || s > best[k][1]) best[k] = [t, s]; }); r.C.forEach(([k, s]) => { ctrlMin[k] = Math.max(ctrlMin[k] || 0, s); });
  }
  const arr = Object.values(best), sizes = arr.map(a => a[1]); const small = arr.filter(a => a[1] < 5);
  out.push({ g, pages: n, minTxt: Math.min(...sizes).toFixed(1), n: arr.length, lt5: small.length, never: arr.filter(a => a[1] === 0).map(a => a[0]).slice(0, 6), minCtrl: Math.min(...Object.values(ctrlMin)).toFixed(0), ex: small.slice(0, 3).map(a => a[0]) });
 }
 out.sort((a, b) => a.minTxt - b.minTxt); out.forEach(o => console.log(`${o.minTxt}px txt | ctrl ${o.minCtrl}px | pages ${o.pages} | <5px ${o.lt5}/${o.n} | ${o.g}` + (o.never.length ? ' | NEVER VISIBLE: ' + o.never.join(',') : '')));
 console.log(errs.join('|') || 'noerr'); await b.close(); })();
