# Generator for 'AMEK BC2' (channel strip = module BC1115/4) and 'AMEK BC2 Master Section' (group modules BC1125/4 x4,
# masters BC1135/4 L/R, aux master / oscillator / communications BC1146, monitor BC1156), measured from the user's photos
# (PDF "AMEK_BCII", Retrosonic sale photos + studio photos). Knobs: light-grey fluted skirt with coloured cap (red gain/pan,
# grey EQ, teal frequency), aux sends as concentric pairs (grey ring + black cap); square grey/black buttons, red PFL.
import os, sys, json
d0 = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(d0, 'ssl4000eg-gen.py')).read(); exec(src[:src.index('# ================= channel strip')])
INK = '#eef0f2'; YL = '#e2cf6e'; RD = '#d8322c'; GR = '#c7c9cc'; GB = '#9fa3a8'; BK = '#18191b'; TE = '#1fa3a3'
CAP_G = '#c9cbce'; CAP_B = '#1c1d1f'; PFL = '#e3392b'; OR = '#f0643a'
# printed fader scale measured on the channel photo (y in photo px) -> positions 0..1
FY = [('+10', 593), ('+5', 663), ('0', 738), ('-5', 823), ('-10', 905), ('-20', 1012), ('-30', 1092), ('-40', 1167), ('-50', 1220), ('-60', 1246), ('∞', 1280)]
FM = [[l, round(1 - (y - 593) / 687, 3)] for l, y in FY]
FZ = round(1 - (738 - 593) / 687, 3)

def kit(g):
    P = lambda k, x, y: [round((g.cx(k) + x) / g.CW, 4), round((g.ry(k) + 34 + y) / g.CH, 4)]
    def T(k, x, y, t, sz=.22, col=INK): g.d.append(['txt', *P(k, x, y), t, min(.62, sz * 2.4), col])
    def VT(k, x, y, t, sz=.2, col=INK, st=9): g.d.append(['vtxt', *P(k, x, y), t, min(.62, sz * 2.4), col, round(st * 1.15 / g.CH, 4)])
    def DOTS(k, x, y, rad, n=11, a0=-150, a1=150): g.d.append(['pdots', *P(k, x, y), round(rad / g.CW, 4), n, round(2.6 / g.CW, 4), INK, a0, a1])
    def KN(k, name, x, y, dia, col, n=11, ring=True, ext=None):
        e = {'ks': 'ssl'}; e.update(ext or {})
        g.c.append(['k', name + '|', *P(k, x, y), round(dia / g.CW, 4), col, 'n', e])
        if ring: DOTS(k, x, y, dia * .72, n)
    def CONC(k, name, a, b, x, y, dia=44):   # concentric aux pair: grey outer ring, black inner cap
        g.c.append(['k', f'{name} {b}|', *P(k, x, y), round(dia / g.CW, 4), GB, 'n', {'ks': 'ssl'}])   # outer ring = aux 2 / 4
        g.c.append(['k', f'{name} {a}|', *P(k, x, y), round(dia * .55 / g.CW, 4), BK, 'n', {'ks': 'ssl'}])   # inner cap = aux 1 / 3
        DOTS(k, x, y, dia * .66, 11)
    def BT(k, name, x, y, cap=None, col=CAP_B, dia=22): g.c.append(['p', name + '|', *P(k, x, y), round(dia / g.CW, 4), col, 'n', dict({'plain': True}, **({'cap': cap} if cap else {}))])
    def LED(k, x, y, col='#ff3b30', dia=6): g.d.append(['led', *P(k, x, y), round(dia / g.CW, 4), col, False])
    def LINE(k, pts): g.d.append(['poly', [P(k, x, y) for x, y in pts], INK, 1.2])
    def SW(k, name, x, y, three=True): g.c.append(['d' if three else 's', name + '|', *P(k, x, y), round(16 / g.CW, 4), '', 'n'])
    def FADER(k, name, y0, y1, col):
        g.F(k, name, 48, y0, y1, FM, FZ, col)
        g.LED(k, 92, y1 + 18, '#ff3b30', 6); T(k, 92, y1 + 6, 'REM', .17); T(k, 92, y1 + 30, 'ON', .17)
    return P, T, VT, DOTS, KN, CONC, BT, LED, LINE, SW, FADER

# ================= channel strip BC1115/4 (three columns of one module)
cols = ['Input & EQ', 'Aux & Routing', 'Fader']
g = build(cols, 110, 560, .55)
P, T, VT, DOTS, KN, CONC, BT, LED, LINE, SW, FADER = kit(g)
k = 0
T(k, 50, 8, 'BC1115/4', .26)
BT(k, '48V', 50, 32, '48v', CAP_G, 24); BT(k, 'Line', 50, 64, 'LINE', CAP_G, 24)
KN(k, 'Gain', 50, 122, 44, RD, ring=False, ext={'sweep': [-150, 150]})
g.d.append(['scale', *P(k, 50, 122), round(38 / g.CW, 4), ['-20', '', '-30', '', '-40', '', '', '-50', '', '-60', '', '-70'], .48, INK, -150, 150])
g.d.append(['scale', *P(k, 50, 122), round(38 / g.CW, 4), ['', '+15', '', '+5', '', '-5', '-15', '', '-25', '', '-35', ''], .48, YL, -150, 150])
VT(k, 103, 96, 'MIC', .19); VT(k, 103, 126, 'LINE', .19, YL); VT(k, 103, 164, 'SENS', .19)
BT(k, 'Phase', 50, 182, 'Ø', CAP_G, 24); BT(k, 'HPF', 50, 212, '⁄‾', CAP_B, 24)
g.HL(k, 232)
T(k, 24, 246, '▲6K', .18); T(k, 24, 258, '▲12K', .18); BT(k, 'HF 6K / 12K', 76, 250, None, CAP_B, 22)
for nm, y, lab in [('HF', 292, 'HF'), ('MF', 340, 'MF'), ('LF', 432, 'LF')]:
    KN(k, f'{nm} Gain', 40, y, 32, GR, 13); T(k, 90, y + 6, lab, .2); T(k, 14, y + 22, '–', .2); T(k, 66, y + 22, '+', .2); T(k, 40, y - 24, '0', .17)
KN(k, 'MF Freq', 40, 386, 32, TE, ring=False, ext={'sweep': [-150, 150]})
g.d.append(['scale', *P(k, 40, 386), round(28 / g.CW, 4), ['.25', '.5', '', '2', '4', '6', '7'], .42, INK, -150, 150]); T(k, 88, 390, 'kHz', .18)
LINE(k, [(84, 238), (104, 238), (104, 258), (88, 258)])
T(k, 26, 466, '▲80Hz', .17); T(k, 26, 478, '▲160Hz', .17); BT(k, 'LF 80 / 160', 78, 472, None, CAP_B, 22)
T(k, 26, 510, 'EQ', .22); BT(k, 'EQ In', 66, 508, 'IN', CAP_B, 24)
k = 1
for nm, a, b, y in [('Aux', 1, 2, 40), ('Aux', 3, 4, 162)]:
    CONC(k, nm, a, b, 42, y); T(k, 92, y - 22, 'AUX', .2); T(k, 22, y + 34, '0', .17); T(k, 54, y + 34, '10', .17); T(k, 90, y + 28, f'{a} ◐ {b}', .18)
    BT(k, f'Aux {a}/{b} Pre', 50, y + 64, 'PRE', CAP_G, 24); LINE(k, [(104, y - 14), (104, y + 64), (66, y + 64)])
KN(k, 'Pan', 42, 290, 38, RD, 9); T(k, 42, 262, 'C', .18); T(k, 22, 318, 'L', .18); T(k, 62, 318, 'R', .18); T(k, 92, 272, 'PAN', .2)
BT(k, 'Pan In', 42, 344, 'IN', CAP_B, 24); LINE(k, [(104, 280), (104, 344), (58, 344)])
for i, (nm, cap) in enumerate([('Route 1+2', '1+2'), ('Route 3+4', '3+4'), ('Stereo', 'ST'), ('Mute', 'MUTE')]): BT(k, nm, 42, 382 + i * 36, cap, CAP_B, 24)
LED(k, 80, 490, '#ff3b30', 7); T(k, 92, 516, 'PEAK', .18); LED(k, 92, 532, '#f5d22e', 7)
k = 2
FADER(k, 'Fader', 36, 478, '#d4d5d3'); BT(k, 'PFL', 50, 538, 'PFL', PFL, 24)
strip = dict(kind='Channel Strip', pages=pages_of(g, [(n, i, i) for i, n in enumerate(cols)], len(cols)), ks='ssl', ps='sq', ar=round(g.CW / g.CH, 4), bare=True, noTicks=True,
             bg='#3b3c3f', bg2='#2c2d30', ink=INK, kc=GR, fs=22, brand='', model='', tx=.5, ty=.03, deco=g.d, c=g.c)

# ================= master section: modules side by side as on the console
mcols = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Master L', 'Master R', 'Aux Master', 'Monitor']
g = build(mcols, 110, 1170, .55)
P, T, VT, DOTS, KN, CONC, BT, LED, LINE, SW, FADER = kit(g)
def sends(k, pre):
    for a, b, y in [(1, 2, 320), (3, 4, 420)]:
        CONC(k, f'{pre} Aux', a, b, 42, y, 40); T(k, 92, y - 20, 'AUX', .19); T(k, 22, y + 30, '0', .16); T(k, 52, y + 30, '10', .16); T(k, 90, y + 26, f'{a} ◐ {b}', .17)
        BT(k, f'{pre} Aux {a}/{b} Pre', 50, y + 52, 'PRE', CAP_G, 22)
for n, lab in zip(range(1, 5), ['1', '2', '3', '4']):   # button routes the aux return to this subgroup
    k = n - 1; pre = f'Group {n}'
    T(k, 55, 6, 'BC1125/4', .22)
    BT(k, f'{pre} Return Mute', 50, 28, 'MUTE', CAP_B, 22); BT(k, f'{pre} Return PFL', 50, 56, 'PFL', PFL, 22)
    KN(k, f'{pre} Return Level', 46, 102, 36, BK); T(k, 26, 132, '0', .16); T(k, 66, 132, '10', .16); VT(k, 100, 84, 'LEVEL', .17)
    BT(k, f'{pre} Return ST', 50, 152, 'ST', CAP_B, 22); BT(k, f'{pre} Return to Group', 50, 180, lab, CAP_B, 22)
    g.HL(k, 204)
    sends(k, pre)
    KN(k, f'{pre} Pan', 42, 518, 34, RD, 9); T(k, 42, 494, 'C', .16); T(k, 92, 504, 'PAN', .18); T(k, 24, 544, 'L', .16); T(k, 60, 544, 'R', .16)
    BT(k, f'{pre} Pan In', 42, 566, 'IN', CAP_B, 22); LINE(k, [(104, 510), (104, 566), (56, 566)])
    BT(k, f'{pre} Stereo', 50, 612, 'ST', CAP_B, 22); BT(k, f'{pre} Mute', 50, 640, 'MUTE', CAP_B, 22); LED(k, 86, 640, '#ff3b30', 6)
    FADER(k, f'{pre} Fader', 680, 1090, '#2f8a43'); BT(k, f'{pre} PFL', 50, 1148, 'PFL', PFL, 22)
for i, side in enumerate(['L', 'R']):
    k = 4 + i; pre = f'Master {side}'
    T(k, 55, 6, 'BC1135/4', .22)
    sends(k, pre)
    g.d.append(['rect', *P(k, 16, 586), round(78 / g.CW, 4), round(24 / g.CH, 4), OR, 'none', 2]); T(k, 55, 598, 'MASTER', .2, '#ffffff')
    BT(k, f'{pre} Mute', 50, 640, 'MUTE', CAP_B, 22); LED(k, 86, 640, '#ff3b30', 6)
    FADER(k, f'{pre} Fader', 680, 1090, '#d8322c'); BT(k, f'{pre} PFL', 50, 1148, 'PFL', PFL, 22)
k = 6
T(k, 55, 6, 'BC1146', .22)
T(k, 26, 22, 'X10', .17); T(k, 26, 34, 'X100', .17); T(k, 26, 50, 'X1', .17); LINE(k, [(42, 28), (50, 28)])
BT(k, 'Osc x10', 70, 28, None, CAP_B, 22); BT(k, 'Osc x1', 70, 54, None, CAP_B, 22); LED(k, 96, 54, '#ff3b30', 6)
KN(k, 'Osc Freq', 66, 112, 34, TE, ring=False, ext={'sweep': [-150, -30]})
for i, t in enumerate(['150', '125', '100', '60', '40', '30']): T(k, 20, 88 + i * 10, t, .15)
VT(k, 36, 106, 'Hz', .15); VT(k, 101, 98, 'FREQ', .16)
BT(k, 'Osc Groups', 70, 158, 'GRPS', CAP_B, 22); BT(k, 'Osc Stereo', 70, 186, 'ST', CAP_B, 22)
g.HL(k, 208)
KN(k, 'PFL Level', 50, 250, 38, RD); VT(k, 101, 232, 'PFL', .16); T(k, 30, 282, '0', .16); T(k, 68, 282, '10', .16)
T(k, 28, 300, 'METER', .16); T(k, 28, 311, 'ONLY', .16); BT(k, 'Meter Only', 70, 304, None, CAP_B, 22); LED(k, 96, 304, '#ff3b30', 6); LED(k, 88, 332, '#d6b23a', 8)
g.HL(k, 348)
for i in range(4):
    y = 360 + i * 132; n = i + 1
    KN(k, f'Aux {n} Master', 50, y + 30, 38, BK); T(k, 30, y + 62, '0', .16); T(k, 68, y + 62, '10', .16); VT(k, 101, y + 18, 'AUX', .16)
    T(k, 26, y + 80, 'TALK', .16); BT(k, f'Aux {n} Talk', 70, y + 80, None, CAP_G, 18)
    T(k, 26, y + 104, 'MUTE', .16); BT(k, f'Aux {n} Mute', 70, y + 104, str(n), CAP_B, 18); LED(k, 96, y + 104, '#ff3b30', 6)
    BT(k, f'Aux {n} PFL', 70, y + 128, 'PFL', PFL, 18)
g.HL(k, 892); T(k, 55, 904, 'COMMUNICATIONS', .17)
KN(k, 'Return T/B', 52, 940, 32, RD); VT(k, 100, 922, 'RET T/B', .15, st=8)
KN(k, 'Talkback Mic', 52, 994, 32, GR); VT(k, 100, 984, 'MIC', .15)
for i, (nm, cap) in enumerate([('Talk Groups', 'GRPS'), ('Talk Stereo', 'ST'), ('Talk Ext 1', '1'), ('Talk Ext 2', '2')]): BT(k, nm, 80, 1030 + i * 26, cap, CAP_B, 20)
T(k, 40, 1094, 'EXT', .16); LINE(k, [(64, 1082), (56, 1082), (56, 1108), (64, 1108)])
BT(k, 'Talk', 34, 1134, 'TALK', '#e05a54', 34); T(k, 55, 1160, 'AUX MASTER', .16)
k = 7
T(k, 55, 6, 'BC1156', .22)
for i, (nm, l, r, top, three) in enumerate([('T/B to Monitor', 'L', 'L+R', 'OFF', True), ('PFL to Monitor', 'L', 'L+R', 'OFF', True), ('Monitor Mute', 'L', 'R', 'L+R', True),
                                             ('Monitor Mono', 'L', 'R', 'L+R', True), ('Monitor Phase', 'L−Ø', 'L+Ø', 'OFF', True)]):
    y = 40 + i * 34
    SW(k, nm, 70, y, three); T(k, 48, y + 2, l, .15); T(k, 96, y + 2, r, .15)
    if top: T(k, 70, y - 14, top, .14)
for i, t in enumerate(['T/B', 'PFL', 'MUTE', 'MONO', '']): T(k, 20, 42 + i * 34, t, .15)
T(k, 55, 222, 'MONITOR STATUS', .16); g.HL(k, 232)
g.d.append(['jack', *P(k, 55, 262), round(30 / g.CW, 4)]); T(k, 55, 292, 'HEADPHONES', .16); g.HL(k, 304)
for i in range(8): BT(k, f'B Playback {i + 1}', 72, 326 + i * 30, None, CAP_G, 22)
VT(k, 28, 340, 'B PLAYBACK SOURCE', .15, st=10); LINE(k, [(52, 320), (40, 320), (40, 546), (52, 546)])
for i, cap in enumerate(['PB1', 'PB2', 'AUX', 'AUX', '1+2', '3+4', 'ST', '']): BT(k, f'A Direct {i + 1}', 72, 580 + i * 30, cap or None, CAP_B, 22)
VT(k, 28, 590, 'A DIRECT SOURCE', .15, st=10); LINE(k, [(52, 574), (40, 574), (40, 800), (52, 800)])
T(k, 30, 836, 'L-B', .15); T(k, 30, 847, 'R-A', .15); BT(k, 'L-B R-A', 72, 842, None, CAP_G, 22); LED(k, 98, 842, '#d6b23a', 6)
T(k, 30, 876, 'SPK 2', .15); BT(k, 'Speaker 2', 72, 876, None, CAP_G, 22)
T(k, 30, 910, 'MONO', .15); BT(k, 'Mono', 72, 910, None, CAP_G, 22)
KN(k, 'Monitor Level', 60, 968, 42, BK); T(k, 38, 1002, '0', .16); T(k, 80, 1002, '10', .16); VT(k, 104, 948, 'LEVEL', .15)
g.HL(k, 1016)
for i, (nm, col, lab) in enumerate([('A / B', '#e8e8e4', 'A ▸ B'), ('Dim', '#3cbf5a', 'DIM'), ('Monitor Mute', '#e04a3a', 'MUTE')]):
    y = 1046 + i * 40; BT(k, nm if nm != 'Monitor Mute' else 'Monitor Cut', 64, y, None, col, 30); VT(k, 24, y - 12, lab.replace(' ', ''), .14, st=7)
T(k, 55, 1162, 'MONITOR', .17)
master = dict(kind='Master Section', pages=pages_of(g, [('Gruppen 1-4', 0, 3), ('Master L/R', 4, 5), ('Aux Master', 6, 6), ('Monitor', 7, 7)], len(mcols)), ks='ssl', ps='sq',
              ar=round(g.CW / g.CH, 4), bare=True, noTicks=True, bg='#3b3c3f', bg2='#2c2d30', ink=INK, kc=GR, fs=16, brand='', model='', tx=.5, ty=.03, deco=g.d, c=g.c)
for e in (strip, master):
    n = [q[1] for q in e['c']]; assert len(n) == len(set(n)), [x for x in n if n.count(x) > 1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in [('AMEK BC2', strip), ('AMEK BC2 Master Section', master)]))
