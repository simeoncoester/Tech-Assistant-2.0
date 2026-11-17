# Klark Teknik EQP-KT (Pultec-style program equaliser) measured from the user's product photo (1600x1600, panel x 73..1527,
# y 640..906; photo only used as measuring template, drawn anew). Reuses the photo-coordinate helper class D from sslphoto-gen.py.
import os, sys, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sslphoto-gen.py')).read()
exec(src[:src.index('R7 = ')])
OUT = {}
BK = '#151515'
g = D(73, 640, 1527, 906, 10, '#1d1e20')
for x, y in [(95, 655), (95, 891), (1505, 655), (1505, 891)]: g.R(x - 15, y - 9, 30, 18, '#f4f4f2', 'none', 9)   # rack ear slots
for x, y in [(185, 693), (185, 848), (1410, 693), (1410, 848)]: g.SCREW(x, y, 20)
TEN = [str(i) for i in range(11)]
for name, x, t in [('LF Boost', 355, 'BOOST'), ('LF Cut', 565, 'CUT'), ('HF Boost', 930, 'BOOST'), ('HF Cut', 1140, 'CUT')]:
    g.T(x, 649, t, 12)
    g.K(name, x, 730, 116, BK, {'ks': 'bakelite'}, TEN, 64, -145, 145, 10.5, dots=False)
g.T(750, 681, 'EQP-KT', 12); g.T(750, 696, 'PROGRAM EQUALISER', 11)
F7 = [-90, -60, -30, 0, 30, 60, 90]
g.T(677, 744, 'Hz', 11); g.K('LF Frequency', 677, 826, 72, BK, {'ks': 'chicken'}, list(zip(F7, ['20', '30', '60', '100', '200', '400', '800'])), 62, -90, 90, 10)
g.T(680, 890, 'LF BOOST/CUT', 12)
g.T(820, 744, 'kHz', 11); g.K('HF Boost Frequency', 820, 826, 72, BK, {'ks': 'chicken'}, list(zip(F7, ['3', '4', '5', '8', '10', '12', '16'])), 60, -90, 90, 10)
g.T(818, 890, 'HF BOOST', 12)
g.K('Bandwidth', 1035, 826, 76, BK, {'ks': 'chicken'}, TEN, 58, -150, 150, 10, dots=False)
g.T(973, 873, 'SHARP', 11); g.T(1102, 873, 'BROAD', 11); g.T(1035, 890, 'BANDWIDTH', 12)
g.T(1247, 744, 'kHz', 11); g.K('HF Cut Frequency', 1247, 826, 72, BK, {'ks': 'chicken'}, list(zip([-60, -30, 0, 30, 60], ['3', '4', '5', '10', '20'])), 60, -60, 60, 10)
g.T(1247, 890, 'HF CUT', 12)
g.c.append(['s', 'EQ On|', *g.P(248, 830), .022, '', 'n']); g.T(248, 793, 'EQ ON', 12); g.T(250, 882, 'BYPASS', 12)
g.c.append(['s', 'Power|', *g.P(1350, 830), .022, '', 'n']); g.T(1350, 882, 'POWER', 12)
g.d.append(['lamp', *g.P(1350, 693), round(40 / g.W, 4), '#ff6a1a'])
g.R(1352, 762, 140, 22, '#141414', '#6d6e70', 3); g.T(1422, 773, 'KLARK TEKNIK', 11, '#f2f2f2')
OUT['Klark Teknik EQP-KT'] = g.out(bare=True, kind='EQ', ks='bakelite', bg='#d9dad5', bg2='#c9cac5', kc=BK)
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in OUT.items()))
