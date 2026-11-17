# API DR-2402 Pure Analog Summing Box measured from the user's front drawing (1200x437, whole panel incl. rack ears) and
# coloured after the user's photos (dark blue panel, amber backlit VU meters). Drawn anew. Listed as Master Section.
import os, sys, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sslphoto-gen.py')).read()
exec(src[:src.index('R7 = ')])
OUT = {}
BK, SI, PK = '#1a1a1c', '#b9bcc2', '#ff6fb0'
g = D(0, 0, 1200, 437, 10, '#f2f4fa')
for x, y in [(14, 96), (14, 343), (1186, 96), (1186, 343)]: g.R(x - 11, y - 9, 22, 18, '#0b0d14', 'none', 9)   # rack ear slots
for x, y in [(70, 68), (70, 410), (1132, 68), (1132, 410)]: g.R(x - 9, y - 9, 18, 18, '#0b0d14', 'none', 9)
TEN = [str(i) for i in range(11)]
def tog(name, x, y): g.c.append(['s', name + '|', *g.P(x, y), .016, '', 'n'])
def vol(name, x, y, dia=52, rad=34, px=6.5): g.K(name, x, y, dia, BK, {'ks': 'chicken'}, TEN, rad, -145, 145, px)
def chan(n, x, y):   # y = pan centre
    g.T(x - 30, y - 24, str(n), 12)
    g.K(f'Pan {n}', x, y, 38, SI, {'ks': 'chicken'}); g.d.append(['ticks', *g.P(x, y), round(26 / g.W, 4), 11, g.ink, -135, 135, .45, True])
    g.T(x, y - 34, 'C', 7); g.T(x - 15, y + 27, 'L', 7.5); g.T(x + 16, y + 27, 'R', 7.5); g.T(x, y + 36, 'PAN', 8)
    tog(f'Ch {n} On', x + 37, y + 34); g.T(x + 47, y + 13, 'ON', 6.5)
    g.LED(x - 33, y + 47, 8, PK)
    vol(f'Volume {n}', x, y + 80); g.T(x, y + 123, 'VOLUME', 8)
for i in range(8):
    x = 131 + i * 94.1
    chan(i + 1, x, 46); chan(i + 9, x, 211)
for i, t in enumerate(['17-18', '19-20', '21-22', '23-24']):
    x = 131 + i * 189.3
    vol(f'Volume {t}', x, 381, 50, 32); g.T(x, 422, 'VOLUME', 8)
    g.LED(x - 30, 348, 8, PK); g.LED(x + 35, 348, 8, PK); g.T(x + 66, 349, t, 12)
    tog(f'Mute {t}', x + 91, 385); g.T(x + 91, 362, 'ON', 6.5); g.T(x + 91, 411, 'MUTE', 7)
for x, t in [(853, 'LEFT'), (980, 'RIGHT')]:
    g.T(x + 58, 78, t, 9); g.d.append(['vu', *g.P(x, 93), round(117 / g.W, 4), round(68 / g.H, 4), {'label': 'VU', 'lit': 'amber'}])
g.K('Master Volume', 978, 247, 90, BK, {'ks': 'chicken'}, TEN, 60, -145, 145, 10)
g.T(978, 317, 'VOLUME', 11)
tog('Master Mute', 893, 263); g.T(893, 232, 'ON', 8); g.T(893, 297, 'MUTE', 8)
tog('Insert / Bypass', 1062, 263); g.T(1062, 228, 'INSERT', 8); g.T(1062, 297, 'BYPASS', 8)
tog('Power', 978, 367); g.T(978, 343, 'ON', 8); g.T(978, 391, 'OFF', 8)
g.d.append(['poly', [g.P(842, 402), g.P(856, 409), g.P(842, 416), g.P(842, 402)], '#2fa8ff', 2]); g.T(866, 409, 'api', 9)
g.T(1000, 409, 'DR-2402 PURE ANALOG SUMMING BOX', 9)
OUT['API DR-2402'] = g.out(bare=True, kind='Master Section', ks='chicken', bg='#24399a', bg2='#1c2f84', kc=BK,
    pages=[['Kanäle 1–8', 0, 0, .72, .42], ['Kanäle 9–16', 0, .4, .72, .8], ['Stereo 17–24', 0, .76, .72, 1], ['Master', .68, 0, 1, 1]])
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in OUT.items()))
