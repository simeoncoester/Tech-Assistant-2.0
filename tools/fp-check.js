const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1200, height: 900 }, serviceWorkers: 'block' })).newPage();
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const only = process.argv[2] ? process.argv[2].split(',') : null;
 const rep = await p.evaluate(only => {
   const res = {};
   for (const [name, fp] of Object.entries(FACEPLATES)) { if (only && !only.includes(name)) continue;
     const W = 1000, H = Math.round(W / fp.ar);
     const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:0;top:0;width:1000px'; host.innerHTML = fpSvg(fp); document.body.append(host);
     const texts = [...host.querySelectorAll('text')].map(t => { const bb = t.getBBox(); const wx = bb.width * .03; return { t: t.textContent, x0: bb.x - wx, y0: bb.y + bb.height * .18, x1: bb.x + bb.width + wx, y1: bb.y + bb.height * .9 }; }).filter(t => t.t.trim() && t.x1 - t.x0 > 0);
     // texts inside a meter face are part of the meter
     const meters = (fp.deco || []).filter(d => d[0] === 'vu' || d[0] === 'vmeter').map(d => ({ x0: d[1] * W, y0: d[2] * H, x1: (d[1] + d[3]) * W, y1: (d[2] + d[4]) * H }));
     const inMeter = t => meters.some(m => t.x0 >= m.x0 - 2 && t.x1 <= m.x1 + 2 && t.y0 >= m.y0 - 2 && t.y1 <= m.y1 + 2);
     const ctrls = fp.c.map(q => { const [ty, nm, x, y, r, , , ext] = q, X = x * W, Y = y * H, R = r * W / 2; const sq = ((ext && ext.ps) || fp.ps) === 'sq';
       const dar = ext && ext.dar; const hx = ty === 'x' ? R : ty === 'p' ? R * (sq ? 1.22 : 1.28) : ty === 's' ? R * .95 : ty === 'f' ? R : R * 1.0, hy = ty === 'x' ? R / dar : ty === 's' ? R * 1.65 : ty === 'f' ? (ext && ext.vert ? R * 9 : R / 9) : hx;
       const hasScale = (fp.deco || []).some(d => d[0] === 'scale' && Math.abs(d[1] - x) < .004 && Math.abs(d[2] - y) < .004); const tick = ty === 'k' && !fp.noTicks && !hasScale ? R + Math.max(4, R * .1) + Math.max(6, R * .24) : hx;
       return { nm: nm.split('|')[0], ty, X, Y, hx, hy, tick, round: ty !== 'f' && ty !== 's' && ty !== 'x' }; });
     const obst = (fp.deco || []).filter(d => ['led', 'jack', 'lamp', 'screw'].includes(d[0])).map(d => ({ nm: d[0], X: d[1] * W, Y: d[2] * H, hx: d[3] * W / 2 * (d[0] === 'lamp' ? 1.3 : 1), round: true }));
     const issues = [];
     const tb = texts.filter(t => !inMeter(t));
     const ovT = (a, c) => { // text box vs control (circle / box), margin 1px
       if (c.round) { const cx = Math.max(a.x0, Math.min(c.X, a.x1)), cy = Math.max(a.y0, Math.min(c.Y, a.y1)); return Math.hypot(cx - c.X, cy - c.Y) < c.hx - 1; }
       return a.x1 > c.X - c.hx + 1 && a.x0 < c.X + c.hx - 1 && a.y1 > c.Y - c.hy + 1 && a.y0 < c.Y + c.hy - 1; };
     tb.forEach(a => ctrls.forEach(c => { if (ovT(a, c)) issues.push(`T/C "${a.t}" × ${c.nm || c.ty}`); else if (c.ty === 'k' && ovT(a, { ...c, hx: c.tick })) issues.push(`T/ticks "${a.t}" × ${c.nm}`); }));
     const ear = fp.ar > 1.8 && !fp.noEars && !fp.bare ? 42 : 4; tb.forEach(a => { if (a.x0 < ear || a.x1 > W - ear || a.y0 < 2 || a.y1 > H - 2) issues.push(`EDGE "${a.t}"`); });
     const hit = (a, m) => a.x1 > m.x0 + 1 && a.x0 < m.x1 - 1 && a.y1 > m.y0 + 1 && a.y0 < m.y1 - 1;
     tb.forEach(a => meters.forEach(m => { if (hit(a, m)) issues.push(`T/M "${a.t}" × meter`); }));
     ctrls.forEach(c => { const hy = c.round ? c.hx : c.hy; if (c.X - c.hx < ear - 2 || c.X + c.hx > W - ear + 2 || c.Y - hy < -1 || c.Y + hy > H + 1) issues.push(`C/EDGE ${c.nm}`);
       meters.forEach(m => { if (hit({ x0: c.X - c.hx, x1: c.X + c.hx, y0: c.Y - hy, y1: c.Y + hy }, m)) issues.push(`C/M ${c.nm} × meter`); }); });
     tb.forEach(a => obst.forEach(c => { if (ovT(a, c)) issues.push(`T/D "${a.t}" × ${c.nm}`); }));
     for (let i = 0; i < tb.length; i++) for (let j = i + 1; j < tb.length; j++) { const a = tb[i], c = tb[j]; const ox = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0), oy = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0); if (ox > 1.5 && oy > 1.5) issues.push(`T/T "${a.t}" × "${c.t}"`); }
     for (let i = 0; i < ctrls.length; i++) for (let j = i + 1; j < ctrls.length; j++) { const a = ctrls[i], c = ctrls[j]; if (Math.abs(a.X - c.X) < 1 && Math.abs(a.Y - c.Y) < 1) continue; // concentric pairs are intended
       const d = Math.hypot(a.X - c.X, a.Y - c.Y); if (a.round && c.round ? d < a.hx + c.hx - 2 : (Math.abs(a.X - c.X) < a.hx + c.hx - 2 && Math.abs(a.Y - c.Y) < a.hy + c.hy - 2)) issues.push(`C/C ${a.nm} × ${c.nm}`); }
     host.remove(); if (issues.length) res[name] = issues;
   }
   return res; }, only);
 for (const [k, v] of Object.entries(rep)) console.log(`## ${k} (${v.length})\n  ` + v.slice(0, 40).join('\n  '));
 console.log('DEVICES WITH ISSUES:', Object.keys(rep).length);
 await b.close(); })();
