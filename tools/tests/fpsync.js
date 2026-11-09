const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
 const ctx = await b.newContext({ serviceWorkers: 'block' }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const r = await p.evaluate(() => { const st = newStage('Preamp'); st.gear = 'Neve 1073'; const t = prBuiltinFor(st); const n0 = t.ctrls.length, gid = t.ctrls[0].id;
   FACEPLATES['Neve 1073'].c.push(['k', 'Extra|EXTRA', .5, .5, .1]); fpSync(t); const n1 = t.ctrls.length, same = t.ctrls[0].id === gid;
   // simulate an old stored template without signature but matching
   const t2 = { ...t, fpSig: undefined, ctrls: t.ctrls.map(c => ({ ...c })) }; fpSync(t2);
   return [n0, n1, same, !!t.fpSig, t2.ctrls.length === n1 && t2.fpSig === t.fpSig]; });
 // persistence: stale template saved, reload -> synced
 await p.evaluate(() => { const t = S.devTpls.find(x => x.builtin === 'Neve 1073'); t.ctrls = t.ctrls.slice(0, 3); t.fpSig = 'old'; localStorage.setItem(LS_KEY, JSON.stringify(S)); });
 await p.reload(); await p.waitForTimeout(400);
 const r2 = await p.evaluate(() => { const t = S.devTpls.find(x => x.builtin === 'Neve 1073'); return t ? [t.ctrls.length, FACEPLATES['Neve 1073'].c.length] : 'none'; });
 console.log(r, r2, errs.join('|') || 'noerr'); await b.close(); })();
