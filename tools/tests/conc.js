// Doppelknöpfe (API 550A, Neve 1084): Ring und Innenknopf drehen sich getrennt, der Zeiger läuft über den gedruckten Bogen
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [], fail = []; const ok = (c, m) => { if (!c) fail.push(m); };
 const p = await (await b.newContext({ ...devices['iPhone 13'], serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 for (const [g, kind, outer, inner] of [['API 550A', 'EQ', 'High Freq', 'High Gain'], ['Neve 1084', 'Preamp', 'Mid kHz', 'Mid Gain'], ['Neve 1073', 'Preamp', 'Low Freq', 'Low Gain']]) {
  await p.evaluate(([g, kind]) => { document.querySelectorAll('.pr-ov').forEach(x => x.remove()); for (const k in prPage) delete prPage[k]; const a = { id: 'A', name: 'Band', productions: [] }; const pr = newProduction('studio'); pr.id = 'P'; const st = newStage(kind); st.gear = g; pr.chain.channels = [{ id: 'c1', name: 'Vox', source: '', stages: [st], notes: '' }]; a.productions.push(pr); S.artists = [a]; normalize(); prAutoAttach(st); window._st = st;
    nav('chain', { artistId: 'A', mode: 'studio', prodId: 'P', inst: 'drums', chainOwner: 'prod' }); showPhotoRecall(st, S.devTpls.find(t => t.id === st.photo.tplId), false); }, [g, kind]);
  await p.waitForTimeout(600); await p.click('.pr-seg button:has-text("Einstellen")'); await p.waitForTimeout(200);
  const geo = await p.evaluate(([outer, inner]) => { const t = S.devTpls.find(x => x.id === window._st.photo.tplId), els = [...document.querySelectorAll('.pr-layer .pr-ctrl')], io = t.ctrls.findIndex(c => c.name === outer), ii = t.ctrls.findIndex(c => c.name === inner);
    els[io].scrollIntoView?.(); const ro = els[io].getBoundingClientRect(), ri = els[ii].getBoundingClientRect(); return { cx: ro.left + ro.width / 2, cy: ro.top + ro.height / 2, Ro: ro.width / 2, Ri: ri.width / 2, conc: els[ii].classList.contains('conc'), ido: t.ctrls[io].id, idi: t.ctrls[ii].id, sweep: t.ctrls[io].sweep }; }, [outer, inner]);
  ok(geo.conc, g + ': inner knob not marked as concentric'); ok(Array.isArray(geo.sweep), g + ': ring has no sweep');
  const val = id => p.evaluate(id => (window._st.photo.vals[id] || {}).pos, id);
  const drag = async (x, y) => { await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.move(x + 40, y - 40, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(150); };
  await drag(geo.cx, geo.cy); const i1 = await val(geo.idi), o1 = await val(geo.ido); ok(i1 > 0 && o1 === undefined, `${g}: drag on the inner knob -> inner ${i1}, ring ${o1}`);
  const rr = (geo.Ro + geo.Ri) / 2; await drag(geo.cx - rr * .7, geo.cy + rr * .7); const i2 = await val(geo.idi), o2 = await val(geo.ido); ok(o2 > 0 && i2 === i1, `${g}: drag on the ring -> ring ${o2}, inner ${i1} -> ${i2}`);
  const ang = await p.evaluate(([ido]) => { const t = S.devTpls.find(x => x.id === window._st.photo.tplId), c = t.ctrls.find(c => c.id === ido); return [prAng(c, 0), prAng(c, 1), prAng({}, 0), prAng({}, 1)]; }, [geo.ido]);
  ok(ang[0] === geo.sweep[0] && ang[1] === geo.sweep[1] && ang[2] === -135 && ang[3] === 135, g + ': angles ' + ang);
  // every knob can be turned a full circle, also when its values are printed on a short arc
  const full = await p.evaluate(() => S.devTpls.find(x => x.id === window._st.photo.tplId).ctrls.filter(c => c.type === 'knob').map(c => { const l = prPLim(c); return Math.round(Math.abs(prAng(c, l[1]) - prAng(c, l[0]))); }));
  ok(full.every(a => a === 360), g + ': turn range ' + full.join(','));
  for (let k = 0; k < 6; k++) await drag(geo.cx - rr * .7, geo.cy + rr * .7); const top = await val(geo.ido), lim = await p.evaluate(id => prPLim(S.devTpls.find(x => x.id === window._st.photo.tplId).ctrls.find(c => c.id === id)), geo.ido);
  ok(Math.abs(top - lim[1]) < .01, `${g}: ring stops at ${top}, limit ${lim[1]}`);
  await p.screenshot({ path: `out/conc-${g.replace(/\W/g, '')}.png` }); }
 console.log(fail.join('\n') || 'CONC OK', errs.join('|') || 'noerr'); await b.close(); })();
