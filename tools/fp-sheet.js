const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1600, height: 1200 }, serviceWorkers: 'block' })).newPage();
 await p.addInitScript(() => { localStorage.setItem('drumtech-onboarded','1'); sessionStorage.setItem('drumtech-nosplash','1'); });
 await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(300);
 const names = await p.evaluate(() => Object.keys(FACEPLATES));
 const wide = names.filter(n => 0), groups = [];
 const ws = await p.evaluate(() => Object.entries(FACEPLATES).filter(([k, f]) => f.ar >= 1).map(([k]) => k)), vs = names.filter(n => !ws.includes(n));
 for (let i = 0; i < ws.length; i += 6) groups.push(['w', ws.slice(i, i + 6)]);
 for (let i = 0; i < vs.length; i += 7) groups.push(['v', vs.slice(i, i + 7)]);
 let k = 0;
 for (const [t, g] of groups) {
   await p.evaluate(([t, g]) => { document.body.innerHTML = ''; document.body.style.cssText = 'margin:0;background:#000;display:flex;flex-wrap:wrap;gap:8px;padding:8px;width:1584px';
     g.forEach(n => { const fp = FACEPLATES[n], W = 1000, H = Math.round(W / fp.ar); const d = document.createElement('div'); d.style.cssText = t === 'w' ? 'width:1580px' : 'height:1150px';
       let svg = fpSvg(fp); const knobs = fp.c.map(q => { const [ty, , x, y, r] = q; const R = r * W / 2; return ty === 'k' ? `<circle cx="${x * W}" cy="${y * H}" r="${R}" fill="#777" stroke="#ddd" stroke-width="2" opacity=".85"/>` : ty === 's' ? `<rect x="${x * W - R * .5}" y="${y * H - R * 1.6}" width="${R}" height="${R * 1.6}" fill="#ccc"/>` : ''; }).join('');
       svg = svg.replace('</svg>', knobs + '</svg>').replace(/width="\d+" height="\d+"/, t === 'w' ? 'width="1580"' : 'height="1150"');
       d.innerHTML = svg; document.body.append(d); }); }, [t, g]);
   await p.waitForTimeout(300); await p.screenshot({ path: `${process.argv[2]}/sheet${k++}.png`, fullPage: true });
 }
 console.log(k, 'sheets'); await b.close(); })();
