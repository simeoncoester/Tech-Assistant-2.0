// Tablet audit: opens every main view in tablet sizes, turns the tablet (viewport swap) and back, checks for sideways scrolling,
// off-screen/overlapping elements and compares the rotated layout with a fresh render. One size: VP='[768,1024,"dark"]' node tablet.js
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const issues = [];
 for (const [w, hh, theme] of (process.env.VP ? [JSON.parse(process.env.VP)] : [[768, 1024, 'dark'], [1024, 1366, 'ice'], [1180, 820, 'dark']])) {
  const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', hasTouch: true, viewport: { width: w, height: hh }, deviceScaleFactor: 1, serviceWorkers: 'block' }); const p = await ctx.newPage(); const tag = `${w}x${hh}/${theme}`; let cur = '';
  p.on('pageerror', e => issues.push(`[${tag}] ${cur} PAGEERROR ${e.message}`)); p.on('console', m => { if (m.type() === 'error' && !/fonts\.g|Failed to load resource/.test(m.text())) issues.push(`[${tag}] ${cur} CONSOLE ${m.text()}`); });
  await p.addInitScript(th => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); localStorage.setItem('drumtech-nosplash','1'); localStorage.setItem('drumtech-dev','1'); localStorage.setItem('drumtech-theme', th); }, theme);
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
  await p.evaluate(() => { const a = { id: 'A', name: 'Die Testband mit langem Namen', productions: [] };
   const st = (k, g) => { const s = newStage(k); s.gear = g || ''; return s; };
   const pr = newProduction('studio'); pr.id = 'PS'; pr.name = 'Album 2026 Hansa Studio'; pr.drums = [newDrum('Bassdrum', '22'), newDrum('Snare', '14'), newDrum('Tom', '12'), newDrum('Tom', '16')]; pr.drums[0].mic = 'Shure Beta 52A'; pr.drums[0].mics2 = ['Neumann U 47 fet'];
   pr.instruments = [{ id: 'I1', inst: 'guitar', name: 'Fender Stratocaster', amp: 'Fender Twin Reverb', ampMic: 'Shure SM57', ampMics2: ['Royer R-121'] }, { id: 'I2', inst: 'bass', name: 'Fender Precision Bass', amp: 'Ampeg SVT' }];
   pr.chain.channels = [{ id: 'c1', name: 'Bassdrum innen', source: 'Shure Beta 52A', stages: [st('Preamp', 'Neve 1073'), st('Kompressor', 'Universal Audio 1176LN'), st('EQ', 'Pultec EQP-1A')], notes: 'Notiz zum Kanal' },
     { id: 'c2', name: 'Overheads', width: 'stereo', source: '', stages: [st('Preamp', 'API 512c'), st('EQ', 'API 550A')], notes: '' },
     { id: 'c3', name: 'Raum', width: 'dual', source: '', stages: [st('Preamp', 'Telefunken V76'), st('Kompressor', 'Fairchild 670')], notes: '' },
     { id: 'c4', name: 'Snare oben mit sehr langem Kanalnamen', source: '', stages: [st('Channel Strip', 'TL Audio VTC')], notes: '' }];
   pr.chain.busses = [{ id: 'b1', name: 'Drum-Bus', source: '', srcIds: ['c1', 'c2', 'c4'], stages: [st('Kompressor', 'SSL G-Series Bus Compressor')], notes: '' }, { id: 'b2', name: 'Hall', source: '', srcIds: ['c4'], stages: [st('Hall', 'Bricasti M7')], notes: '' }];
   pr.chain.masters = [st('Master Section', 'TL Audio VTC Master Section')];
   pr.totalChain = JSON.parse(JSON.stringify(pr.chain)); pr.instChains.guitar.channels = [{ id: 'g1', name: 'Strat Twin', instId: 'I1', source: '', stages: [st('Preamp', 'Neve 1073')], notes: '' }];
   const pl = newProduction('live'); pl.id = 'PL'; pl.name = 'Tour'; pl.drums = [newDrum('Snare', '14')]; a.productions.push(pr, pl); S.artists = [a]; normalize(); fpAttachAll(); [pr.chain, pr.totalChain].forEach(C => { [...C.channels, ...C.busses].forEach(c => openSet.add(c.id)); }); dualOpen.c3 = 'L'; touch(); });
  const base = { artistId: 'A', mode: 'studio', prodId: 'PS' };
  const check = async name => { cur = name; await p.waitForTimeout(350);
   const r = await p.evaluate(() => { const out = []; const W = document.documentElement.clientWidth;
    const top = document.querySelector('.sheet-ov:last-of-type, .pr-ov, #onb') ; const root = [...document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .pr-pop-ov')].pop() || document.body;
    if (document.documentElement.scrollWidth > W + 1) out.push('HSCROLL ' + document.documentElement.scrollWidth);
    const desc = el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') + ' "' + (el.textContent || '').trim().slice(0, 28) + '"';
    const vis = el => { const s = getComputedStyle(el), r = el.getBoundingClientRect(); return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0; };
    const clippedBy = el => { let q = el.parentElement; while (q) { const o = getComputedStyle(q); if (o.overflowX !== 'visible') return true; q = q.parentElement; } return false; };
    root.querySelectorAll('*').forEach(el => { if (!vis(el) || el.closest('svg') || el.closest('.pr-photo')) return; const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
     if ((r.right > W + 1 || r.left < -1) && cs.position !== 'fixed' && !clippedBy(el)) out.push('OFFSCREEN ' + desc(el) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
     if (/^(BUTTON|LABEL|H1|H2|H3|B|SPAN|SMALL|A|SUMMARY)$/.test(el.tagName) && el.childElementCount === 0 && el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible' && cs.textOverflow !== 'ellipsis' && el.clientWidth > 0) out.push('CLIPPED ' + desc(el) + ' ' + el.scrollWidth + '>' + el.clientWidth);
     if ((el.tagName === 'BUTTON' || el.getAttribute('role') === 'button') && (r.width < 28 || r.height < 28) && !el.closest('.pr-layer') && !el.disabled) out.push('SMALL-TAP ' + desc(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
    root.querySelectorAll('.grid, .row, .chips, .pop-btns, .seg').forEach(c => { const kids = [...c.children].filter(vis); const cr = c.getBoundingClientRect();
     kids.forEach(k => { const r = k.getBoundingClientRect(); if (r.right > cr.right + 1.5 || r.left < cr.left - 1.5) out.push('OVERFLOW-IN ' + desc(c) + ' child ' + desc(k)); });
     for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) { const A = kids[i].getBoundingClientRect(), B = kids[j].getBoundingClientRect(); const ox = Math.min(A.right, B.right) - Math.max(A.left, B.left), oy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top); if (ox > 2 && oy > 2 && getComputedStyle(kids[i]).position !== 'absolute' && getComputedStyle(kids[j]).position !== 'absolute') out.push('OVERLAP ' + desc(kids[i]) + ' / ' + desc(kids[j])); } });
    return [...new Set(out)].slice(0, 12); });
   r.forEach(x => issues.push(`[${tag}] ${name} ${x}`)); await p.screenshot({ path: `${process.env.S || 'out'}/tablet-${w}x${hh}-${name}.png`, fullPage: !(await p.evaluate(() => !!document.querySelector('.sheet-ov, .pr-ov, #onb'))) }); };

  const sig = () => p.evaluate(() => { const root = [...document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .pr-pop-ov, .stage, .stage-song')].pop() || document.body; const o = [];
    root.querySelectorAll('*').forEach(el => { if (el.closest('svg') || el.closest('canvas')) return; const r = el.getBoundingClientRect(); if (!r.width || !r.height) return; o.push([el.tagName.toLowerCase() + '.' + String(el.className && el.className.baseVal === undefined ? el.className : '').trim().split(/\s+/).slice(0, 2).join('.'), Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]); }); return o; });
  const rot = async (name, reopen) => { await p.setViewportSize({ width: hh, height: w }); await p.waitForTimeout(450); const W0 = w; 
   { const t = tag; cur = name + '-rot'; }
   await check(name + '-rot');
   const tabOk = await p.evaluate(() => { const tb = document.getElementById('tabbar'); if (!tb || !tb.offsetHeight || document.querySelector('.sheet-ov, .pr-ov, #onb, .stage, .stage-song')) return ''; scrollTo(0, 0); const r = tb.getBoundingClientRect(); return (r.bottom > innerHeight + 1 || r.bottom < innerHeight - 40) ? 'TABBAR bottom ' + Math.round(r.bottom) + ' vs ' + innerHeight : ''; }); if (tabOk) issues.push(`[${tag}] ${name}-rot ${tabOk}`);
   if (reopen) { const a = await sig(); await p.evaluate(() => scrollTo(0, 0)); await reopen(); await p.waitForTimeout(450); const bb = await sig();
     if (a.length !== bb.length) issues.push(`[${tag}] ${name}-rot ROTDIFF count ${a.length} vs fresh ${bb.length}`);
     else { const d = a.map((x, i) => [x, bb[i]]).filter(([x, y]) => x[0] !== y[0] || [1, 2, 3, 4].some(k => Math.abs(x[k] - y[k]) > 3)); if (d.length) issues.push(`[${tag}] ${name}-rot ROTDIFF ${d.length}/${a.length} first ${JSON.stringify(d[0])}`); } }
   await p.setViewportSize({ width: w, height: hh }); await p.waitForTimeout(450); const hs = await p.evaluate(() => { const o = []; if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 1) o.push('HSCROLL ' + document.documentElement.scrollWidth); const root = [...document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .stage, .stage-song')].pop() || document.body; root.querySelectorAll('button, .card, .tile, .pop').forEach(el => { const r = el.getBoundingClientRect(); if (r.width && (r.right > innerWidth + 1 || r.left < -1)) { let q = el.parentElement, cl = false; while (q) { if (getComputedStyle(q).overflowX !== 'visible') cl = true; q = q.parentElement; } if (!cl) o.push('OFF ' + el.className); } }); return o.slice(0, 4).join(', '); }); if (hs) issues.push(`[${tag}] ${name}-back ${hs}`); };
  const rr = () => p.evaluate(() => render(true));
  const go = async (name, v, extra) => { await p.evaluate(([v, q]) => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb').forEach(x => x.remove()); nav(v, q); }, [v, { ...base, ...extra }]); await check(name); await rot(name, rr); };
  await go('inst', 'inst', {});
  await go('home-drums', 'home', { inst: 'drums' });
  await go('chain', 'chain', { inst: 'drums', chainOwner: 'prod' });
  await go('chain-total', 'chain', { chainOwner: 'total' });
  await go('chain-git', 'chain', { inst: 'guitar', chainOwner: 'inst' });
  await go('console', 'console', { inst: 'drums', chainOwner: 'prod' });
  await go('kit', 'kit', { inst: 'drums' });
  await go('ginsts', 'ginsts', { inst: 'guitar' });
  await go('ginst', 'ginst', { inst: 'guitar', instId: 'I1' });
  await go('ghome', 'ghome', { inst: 'guitar' });
  await go('backups', 'backups', { inst: 'drums' });
  await go('tuner', 'tuner', { inst: 'drums' }); await go('gtuner', 'tuner', { inst: 'guitar' }); await go('tunings', 'tunings', { inst: 'guitar' }); await go('artists', 'artists', {}); await go('mode', 'mode', {});
  await p.evaluate(() => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb').forEach(x => x.remove()); nav('click', {}); }); await check('click'); await rot('click', rr);
  // live: setlists, editor, large view, show mode
  await p.evaluate(() => { const pl = S.artists[0].productions.find(x => x.id === 'PL'); const song = (t, i) => ({ id: 'so' + i, title: t, key: 'A-Moll', bpm: 120 + i, sig: '4/4', note: 'Intro leise / Break nach dem Solo, dann wieder voll rein', instNotes: [{ instId: '', name: 'Gitarre', inst: 'guitar', tuning: 'Drop D', capo: 2, note: 'Chorus an' }], extra: { Licht: 'Blau', 'Backline-Notizen': 'Gitarrenwechsel · Kapo 2' } });
    pl.setlists = [{ id: 'SL', mode: 'live', name: 'Hauptset Sommer', date: '2026-07-04', venue: 'Hamburg', info: [{ k: 'Curfew', v: '23:00' }], cols: [{ name: 'Licht', type: 'text' }, { name: 'Backline-Notizen', type: 'text' }], songs: ['Erster Song', 'Ein Song mit sehr langem Titel der umbrechen muss', 'Dritter', 'Vierter', 'Fünfter', 'Sechster'].map(song) }]; normalize(); touch(); });
  const lb = { artistId: 'A', mode: 'live', prodId: 'PL' }; const goL = async (name, v, extra) => { await p.evaluate(([v, q]) => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .stage, .stage-song').forEach(x => x.remove()); nav(v, q); }, [v, { ...lb, ...extra }]); await check(name); await rot(name, rr); };
  await goL('live-inst', 'inst', {}); await goL('live-home', 'home', { inst: 'drums' }); await goL('setlists', 'setlists', { inst: 'drums' }); await goL('setlist', 'setlist', { inst: 'drums', setId: 'SL' });
  await p.evaluate(() => showStage(S.artists[0].productions.find(x => x.id === 'PL').setlists[0])); await check('stage'); await rot('stage', () => p.evaluate(() => { document.querySelectorAll('.stage').forEach(x => x.remove()); showStage(S.artists[0].productions.find(x => x.id === 'PL').setlists[0]); }));
  { const vb = p.locator('.stage button:has-text("Ansicht"), .stage button[aria-label*="Ansicht"]').first(); if (await vb.count()) { await vb.click(); await check('stage-panel'); await rot('stage-panel'); const t2 = p.locator('.st-pov button:has-text("Anpassen")').first(); if (await t2.count()) { await t2.click(); await check('stage-panel2'); await rot('stage-panel2'); } await p.evaluate(() => document.querySelectorAll('.st-pov').forEach(x => x.remove())); } else issues.push('no Ansicht button'); }
  await p.evaluate(() => { document.querySelectorAll('.stage').forEach(x => x.remove()); const sl = S.artists[0].productions.find(x => x.id === 'PL').setlists[0]; showStageSong(sl, 0); }).catch(e => issues.push(`[${tag}] showStageSong ${e.message.slice(0, 80)}`)); await check('show'); await rot('show', () => p.evaluate(() => { document.querySelectorAll('.stage-song').forEach(x => x.remove()); showStageSong(S.artists[0].productions.find(x => x.id === 'PL').setlists[0], 0); }));
  await p.evaluate(() => document.querySelectorAll('.stage, .stage-song').forEach(x => x.remove()));
  // photo recall of a wide rack device, a 500 module and the channel strip
  for (const [nm, ci, si] of [['pr-1073', 0, 0], ['pr-550a', 1, 1], ['pr-vtc', 3, 0]]) { await p.evaluate(([ci, si]) => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb').forEach(x => x.remove()); nav('chain', { artistId: 'A', mode: 'studio', prodId: 'PS', inst: 'drums', chainOwner: 'prod' }); const st = S.artists[0].productions[0].chain.channels[ci].stages[si]; showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, [ci, si]); await check(nm); await rot(nm, () => p.evaluate(([ci, si]) => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); const st = S.artists[0].productions[0].chain.channels[ci].stages[si]; showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, [ci, si])); }
  // pop-ups
  await go('inst2', 'inst', {}); await p.click('.gear-btn'); await check('pop-settings'); await rot('pop-settings');
  for (const v of [['artists', {}], ['inst', {}], ['chain', { inst: 'drums', chainOwner: 'prod' }], ['console', { inst: 'drums', chainOwner: 'prod' }], ['ghome', { inst: 'guitar' }], ['kit', { inst: 'drums' }], ['tuner', { inst: 'drums' }]]) {
   await p.evaluate(([v, q]) => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb').forEach(x => x.remove()); nav(v, q); }, [v[0], { ...base, ...v[1] }]); await p.waitForTimeout(200);
   const hb = p.locator('header button[aria-label*="Hilfe"], header .help-btn').first(); if (await hb.count()) { await hb.click(); await check('help-' + v[0]); await rot('help-' + v[0]);
     const n = await p.locator('#onb .onb-dots > *, #onb .dots > *').count(); for (let i = 1; i < Math.min(n, 8); i++) { const nx = p.locator('#onb button:has-text("Weiter")').first(); if (!(await nx.count())) break; await nx.click(); await check('help-' + v[0] + '-' + i); } } else issues.push(`[${tag}] no help button on ${v[0]}`); }
  // console dual insert pop, photo recall from stage
  await go('console2', 'console', { inst: 'drums', chainOwner: 'prod' }); const ins = p.locator('button.ins').first(); if (await ins.count()) { await ins.click(); await check('console-ins'); await rot('console-ins'); }
  await ctx.close(); }
 await b.close(); const real = [...new Set(issues)].filter(x => !/SMALL-TAP|no help button on artists/.test(x)); console.log(real.join('\n') || 'TABLET OK'); })();
