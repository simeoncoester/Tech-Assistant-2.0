const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = []; const p = await (await b.newContext({ serviceWorkers: 'block' })).newPage(); p.on('pageerror', e => errs.push(e.message));
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const r = await p.evaluate(() => { const out = []; const st = newStage('Kompressor'); st.gear = 'Universal Audio 1176LN'; prAutoAttach(st); const t1 = st.photo && st.photo.tplId;
   st.photo.vals[S.devTpls.find(t => t.id === t1).ctrls[0].id] = { pos: .6 }; out.push(!!t1);
   st.gear = 'Fairchild 670'; prAutoAttach(st); out.push(st.photo && st.photo.tplId !== t1 && Object.keys(st.photo.vals).length === 0);
   st.photo.vals.x = { pos: .3 }; st.gear = 'Irgendein Kompressor'; prAutoAttach(st); out.push(st.photo === null);
   // own unbound photo + gear chosen afterwards keeps the photo and binds it
   const own = { id: 'own1', name: 'Kompressor', kind: 'Kompressor', ar: 2, ctrls: [] }; S.devTpls.push(own); const st2 = newStage('Kompressor'); st2.photo = { tplId: 'own1', vals: {} }; st2.gear = 'Mein Comp'; prAutoAttach(st2); out.push(st2.photo.tplId === 'own1' && own.gear === 'Mein Comp');
   st2.gear = 'Universal Audio 1176LN'; prAutoAttach(st2); out.push(st2.photo.tplId === t1);
   return out; });
 console.log(r, errs.join('|') || 'noerr'); await b.close(); })();
