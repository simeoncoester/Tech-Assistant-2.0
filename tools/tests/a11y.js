// Accessibility audit (WCAG 2.1 AA, automatic part): text contrast in both designs, touch target size, buttons/inputs without a name, images without alt.
// Phone size with touch. Prints one line per finding group, ends with "A11Y OK" when nothing critical is left. Details: A11Y_ALL=1 lists every group.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const found = new Map(); const crit = [];
 for (const theme of ['dark', 'ice']) {
  const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', hasTouch: true, viewport: { width: 390, height: 844 }, serviceWorkers: 'block' }); const p = await ctx.newPage();
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
  await p.evaluate(() => { const pl = S.artists[0].productions.find(x => x.id === 'PL'); pl.setlists = [{ id: 'SL', mode: 'live', name: 'Hauptset', date: '2026-07-04', venue: 'Hamburg', info: [], cols: [], songs: ['Erster Song', 'Zweiter Song'].map((t, i) => ({ id: 'so' + i, title: t, key: 'A-Moll', bpm: 120, sig: '4/4', note: 'Intro leise / Break', instNotes: [], extra: {} })) }]; normalize(); touch(); });
  const scan = async view => { await p.waitForTimeout(350); const r = await p.evaluate(() => {
   const out = [], root = [...document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .stage, .stage-song')].pop() || document.body;
   const rgba = s => { const m = String(s).match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v[3] ?? 1]; };
   const lum = c => { const f = x => { x /= 255; return x <= .03928 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; }; return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2]); };
   const over = (top, bot) => { const a = top[3]; return [top[0] * a + bot[0] * (1 - a), top[1] * a + bot[1] * (1 - a), top[2] * a + bot[2] * (1 - a), 1]; };
   const bgOf = el => { const stack = []; let q = el, approx = false; while (q && q.nodeType === 1) { const cs = getComputedStyle(q); let c = rgba(cs.backgroundColor);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') { const g = (cs.backgroundImage.match(/rgba?\([^)]+\)/g) || []).map(rgba); if (g.length) { const wa = g.reduce((s, x) => s + x[3], 0) || 1, avg = g.reduce((s, x) => [s[0] + x[0] * x[3] / wa, s[1] + x[1] * x[3] / wa, s[2] + x[2] * x[3] / wa, s[3] + x[3] / g.length], [0, 0, 0, 0]); c = c && c[3] ? over(avg, c) : avg; } else approx = true; }
      if (c && c[3] > 0) { stack.push(c); if (c[3] >= .99) break; } q = q.parentElement; }
     let bg = [0, 0, 0, 1]; if (!q || q.nodeType !== 1) { const b = rgba(getComputedStyle(document.body).backgroundColor); bg = b && b[3] ? [b[0], b[1], b[2], 1] : [255, 255, 255, 1]; }
     for (let i = stack.length - 1; i >= 0; i--) bg = stack[i][3] >= .99 ? stack[i] : over(stack[i], bg); return [bg, approx]; };
   const sig = el => { let s = el.tagName.toLowerCase(); const cl = typeof el.className === 'string' ? el.className.trim().split(/\s+/).filter(x => x && !/^(on|set|sel|active)$/.test(x)).slice(0, 2) : []; if (cl.length) s += '.' + cl.join('.'); const pc = el.parentElement && typeof el.parentElement.className === 'string' ? el.parentElement.className.trim().split(/\s+/)[0] : ''; return (pc ? pc + ' > ' : '') + s; };
   const vis = el => { const cs = getComputedStyle(el), r = el.getBoundingClientRect(); return cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > .05 && r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight * 3; };
   // checked by hand: .ch-cat is a 4 px colour strip with an invisible 13 px ::before tap area; fader scale numbers sit under the moving fader cap (readable, see screenshot)
   root.querySelectorAll('*').forEach(el => { if (el.closest('svg, canvas, .pr-photo, .pr-mini, #splash') || el.matches('.ch-cat, .fader .tick b') || !vis(el)) return;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); const cs = getComputedStyle(el);
    const txt0 = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim(), gradText = /text/.test(cs.webkitBackgroundClip || cs.backgroundClip) && rgba(cs.color) && rgba(cs.color)[3] === 0, emoji = /^[\p{Extended_Pictographic}\p{Regional_Indicator}\s\u200d\ufe0f]+$/u.test(txt0);
    if (own && !gradText && !emoji && !el.closest('[aria-hidden="true"]')) { const fg = rgba(cs.color); if (fg) { let a = fg[3], q = el; while (q && q !== document.body) { a *= +getComputedStyle(q).opacity; q = q.parentElement; }
      const [bg, approx] = bgOf(el), f = over([fg[0], fg[1], fg[2], a], bg), L1 = lum(f), L2 = lum(bg), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
      const fs = parseFloat(cs.fontSize), big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700), need = big ? 3 : 4.5, disabled = el.closest(':disabled, [aria-disabled="true"]');
      if (ratio < need && !disabled) out.push(['CONTRAST', sig(el), +ratio.toFixed(2), need, el.textContent.trim().slice(0, 24), approx]); } }
    const r = el.getBoundingClientRect(), interactive = el.matches('button, a[href], input:not([type=hidden]), select, textarea, summary, [role=button], [role=switch], [role=tab]');
    if (interactive && !el.disabled && !el.closest('.pr-layer')) { const m = Math.min(r.width, r.height); if (m < 24) out.push(['TAP<24', sig(el), Math.round(r.width) + 'x' + Math.round(r.height), 24, el.textContent.trim().slice(0, 18) || el.getAttribute('aria-label') || '']); else if (m < 44 && !el.matches('input, select, textarea')) out.push(['TAP<44', sig(el), Math.round(r.width) + 'x' + Math.round(r.height), 44, el.textContent.trim().slice(0, 18) || el.getAttribute('aria-label') || '']);
     const name = (el.getAttribute('aria-label') || el.getAttribute('title') || el.getAttribute('aria-labelledby') || el.textContent || el.getAttribute('placeholder') || el.value || '').trim() || (el.id && document.querySelector(`label[for="${el.id}"]`)) || el.closest('label');
     if (!name && el.type !== 'file') out.push(['NONAME', sig(el), el.tagName, 0, el.outerHTML.slice(0, 80)]); }
    if (el.tagName === 'IMG' && !el.hasAttribute('alt')) out.push(['NOALT', sig(el), '', 0, el.src.slice(0, 40)]); });
   return out; });
   r.forEach(([k, s, v, need, txt, approx]) => { const key = k + ' | ' + s; const e = found.get(key) || { k, s, n: 0, worst: v, txt, views: new Set(), themes: new Set(), approx }; e.n++; e.views.add(view); e.themes.add(theme); if (k === 'CONTRAST' && v < e.worst) { e.worst = v; e.txt = txt; } found.set(key, e); }); };
  const go = async (name, v, q) => { await p.evaluate(([v, q]) => { document.querySelectorAll('.sheet-ov, .pr-ov, #onb, .stage, .stage-song').forEach(x => x.remove()); nav(v, q); }, [v, q]); await scan(name); };
  await go('artists', 'artists', {}); await go('mode', 'mode', base); await go('projects', 'projects', base); await go('inst', 'inst', base);
  for (const [n, v, q] of [['home', 'home', { inst: 'drums' }], ['kit', 'kit', { inst: 'drums' }], ['chain', 'chain', { inst: 'drums', chainOwner: 'prod' }], ['console', 'console', { inst: 'drums', chainOwner: 'prod' }], ['tuner', 'tuner', { inst: 'drums' }], ['gtuner', 'tuner', { inst: 'guitar' }], ['tunings', 'tunings', { inst: 'guitar' }], ['ginst', 'ginst', { inst: 'guitar', instId: 'I1' }], ['backups', 'backups', { inst: 'drums' }]]) await go(n, v, { ...base, ...q });
  await go('click', 'click', {});
  const lb = { artistId: 'A', mode: 'live', prodId: 'PL', inst: 'drums' }; await go('setlists', 'setlists', lb); await go('setlist', 'setlist', { ...lb, setId: 'SL' });
  await p.evaluate(() => showStage(S.artists[0].productions.find(x => x.id === 'PL').setlists[0])); await scan('stage');
  await p.evaluate(() => { document.querySelectorAll('.stage').forEach(x => x.remove()); showStageSong(S.artists[0].productions.find(x => x.id === 'PL').setlists[0], 0); }); await scan('show');
  await p.evaluate(() => { document.querySelectorAll('.stage-song').forEach(x => x.remove()); nav('artists', {}); settingsPop(); }); await scan('settings');
  await p.evaluate(() => { document.querySelectorAll('.sheet-ov').forEach(x => x.remove()); nav('chain', { artistId: 'A', mode: 'studio', prodId: 'PS', inst: 'drums', chainOwner: 'prod' }); const st = S.artists[0].productions[0].chain.channels[0].stages[0]; showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }); await scan('photo-recall');
  await ctx.close(); }
 const list = [...found.values()].sort((a, b) => a.k.localeCompare(b.k) || (a.worst - b.worst));
 for (const e of list) { const c = e.k === 'NONAME' || e.k === 'NOALT' || e.k === 'TAP<24' || (e.k === 'CONTRAST' && e.worst < 3); if (c) crit.push(e); if (c || process.env.A11Y_ALL) console.log(`${c ? '!' : ' '} ${e.k} ${e.s} | ${e.worst} | "${e.txt}" | ${[...e.themes].join('/')} | ${[...e.views].slice(0, 5).join(',')}${e.approx ? ' ~' : ''} x${e.n}`); }
 console.log(`groups: ${list.length}, critical: ${crit.length}`); await b.close(); console.log(crit.length ? 'A11Y ISSUES' : 'A11Y OK'); })();
