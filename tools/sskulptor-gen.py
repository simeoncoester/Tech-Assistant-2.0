# Sound Skulptor 500-series modules measured from the user's photos (PDF "Sound Skulptor Geräte" + chat photos; used only as
# measuring templates, drawn anew): MP 4500, MP 566-II, MP AB528, DI 503J, MP 5.66, MP 5.99, MP 5.12, MP 573, EQ250,
# EQ 573-II, EQP 501, EQ 531T, LA 502, LA 502-T.  Reuses the photo-coordinate helper class D from sslphoto-gen.py.
import os, sys, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sslphoto-gen.py')).read()
exec(src[:src.index('R7 = ')])
OUT = {}
WH, RD, BK = '#f2f2ef', '#d8262b', '#1b1b1d'
def sw(g, name, x, y, three=True, col='', size=.15):   # toggle switch (3-way = dir, 2-way = switch), size for 500-series modules
    g.c.append(['d' if three else 's', name + '|', *g.P(x, y), size, col, 'n'])
def jack(g, x, y, d): g.d.append(['jack', *g.P(x, y), round(d / g.W, 4)])
def logo(g, x, y, s=26):   # Sound Skulptor emblem: shield with a pick
    h = s * 1.25
    g.d.append(['poly', [g.P(x - s / 2, y - h / 2), g.P(x + s / 2, y - h / 2), g.P(x + s / 2.6, y + h / 5), g.P(x, y + h / 2), g.P(x - s / 2.6, y + h / 5), g.P(x - s / 2, y - h / 2)], g.ink, 1.3])
    g.d.append(['poly', [g.P(x - s / 7, y + h / 6), g.P(x, y - h / 3), g.P(x + s / 7, y + h / 6)], g.ink, 1.3])
def ring(g, x, y, rad, n=11, a0=-150, a1=150, d=4): g.d.append(['pdots', *g.P(x, y), round(rad / g.W, 4), n, round(d / g.W, 4), g.ink, a0, a1])
def spokes(g, x, y, r0, n=11, a0=-150, a1=150): g.d.append(['ticks', *g.P(x, y), round(r0 / g.W, 4), n, g.ink, a0, a1, .45])

# ================= MP 4500 (photo 800x800, plate x 287..503, y 5..795)
g = D(287, 5, 503, 795, 30, '#f2f2f2')
g.T(335, 27, 'MP', 17); g.T(466, 27, '4500', 17); g.SCREW(398, 29, 16); g.SCREW(398, 773, 16)
g.K('Harmonics', 375, 105, 78, '#2a63d8', {'ks': 'neve'}, [(-110, '2'), (0, 'OFF'), (110, '8')], 56, -110, 110, 14, dots=False)
ring(g, 375, 105, 50, 9, -110, 110); g.T(325, 166, '2ND', 14); g.T(425, 166, '3RD', 14); g.T(375, 186, 'HARM.', 14)
g.LED(471, 77, 10, '#ff3b30'); g.B('48V', 471, 116, 32, RD, None, False); g.T(471, 155, '48V', 14)
g.B('Phase', 471, 215, 32, WH); g.T(471, 247, 'Ø', 15); g.B('Pad', 471, 309, 32, WH); g.T(471, 345, 'PAD', 14)
g.K('Gain', 375, 309, 68, '#df2a20', {'ks': 'neve', 'sweep': [-120, 30]}, [(a, t) for a, t in zip([-120, -90, -60, -30, 0, 30], ['45', '50', '55', '60', '65', '70'])], 72, px=14, dots=False)
for a, t in zip([-120, -90, -60, -30, 0, 30], ['15', '20', '25', '30', '35', '40']): g.LBL(375, 309, 50, a, t, 13)
g.d.append(['ticks', *g.P(375, 309), round(62 / g.W, 4), 6, g.ink, -120, 30, .12]); g.T(375, 365, 'dB', 14)
g.B('Hi Gain', 369, 397, 32, WH); g.T(369, 436, 'Hi GAIN', 14); g.LED(471, 405, 10, '#35d06a', True)
for nm, y, col in [('Level', 509, BK), ('HPF', 677, '#1e8a3c')]:
    g.K(nm, 375, y, 64, col, {'ks': 'neve'}, [(-150, '0'), (-100, '2'), (0, '5'), (100, '8'), (150, '10')], 54, px=14, dots=False)
    ring(g, 375, y, 44, 9); g.T(378, y + 74, nm.upper(), 14)
logo(g, 471, 509, 30); g.B('HPF In', 471, 673, 32, WH); g.T(471, 707, 'IN', 14)
g.T(335, 777, 'Sound', 16); g.T(462, 777, 'Skulptor', 16)
OUT['Sound Skulptor MP 4500'] = g.out(kind='Preamp', ks='neve', ps='sq', bare=True, bg='#101012', bg2='#060607', kc=BK)

# ================= MP 566-II (plate x 231..462, y 9..791)
g = D(231, 9, 462, 791, 30, '#f2f2f2')
g.T(283, 35, 'MP', 18); g.T(401, 35, '566-II', 18); g.SCREW(342, 36, 16); g.SCREW(342, 762, 16)
for nm, y in [('Out', 135), ('Gain', 323)]:
    g.K(nm, 313, y, 118, BK, {'ks': 'bakelite'}, [(-150, '0'), (0, '5'), (150, '10')], 72, px=16, dots=False)
    ring(g, 313, y, 72, 11, -150, 150, 6)
g.T(320, 223, 'OUT', 17); g.T(316, 411, 'GAIN', 17)
g.B('Pad', 410, 84, 34, WH); g.T(414, 118, 'PAD', 16); g.B('Phase', 410, 235, 34, WH); g.T(410, 265, 'Φ', 17)
g.LED(406, 386, 9, '#ff3b30'); g.B('48V', 410, 423, 34, RD, None, False); g.T(413, 455, '48V', 16)
g.K('HPF', 315, 491, 66, BK, {'ks': 'bakelite'}, [(-150, '0'), (0, '5'), (150, '10')], 46, px=15, dots=False); ring(g, 315, 491, 42, 11, -150, 150, 5)
g.T(320, 562, 'HPF', 16); g.d.append(['poly', [g.P(364, 500), g.P(412, 500), g.P(412, 525)], g.ink, 1.5])
g.B('HPF In', 410, 550, 34, WH); g.T(410, 584, 'IN', 16)
jack(g, 320, 656, 76); g.T(406, 668, 'HIZ', 16); logo(g, 410, 723, 30)
OUT['Sound Skulptor MP 566-II'] = g.out(kind='Preamp', ks='bakelite', ps='sq', bare=True, bg='#5b6334', bg2='#4a5229', kc=BK)

# ================= MP AB528 (plate x 235..448, y 5..791)
g = D(235, 5, 448, 791, 30, '#f2f2f2')
g.T(257, 36, 'MP', 18); g.T(403, 35, 'AB528', 18); g.SCREW(322, 15, 14); g.SCREW(322, 770, 14)
g.K('Out', 325, 118, 70, '#8f949b', {'ks': 'neve'}, [(-150, '0'), (0, '5'), (150, '10')], 50, px=15, dots=False)
spokes(g, 325, 118, 42); g.T(345, 180, 'OUT', 16); g.LED(412, 198, 10, '#35d06a', True)
g.K('Gain', 339, 295, 136, '#e8241e', {'ks': 'chicken', 'sweep': [-100, 66]}, [(a, t) for a, t in zip([-100, -66, -33, 0, 33, 66], ['10', '20', '30', '40', '50', '60'])], 86, px=16, dots=False)
spokes(g, 339, 295, 74, 6, -100, 66); g.T(405, 373, 'dB', 16)
sw(g, 'Impedance 300 / 1200 / Line', 333, 450); g.T(345, 420, '1200', 15); g.T(294, 455, '300', 15); g.T(394, 455, 'LINE', 15)
sw(g, 'Polarity', 335, 523, False); g.T(294, 525, 'POL', 15); g.T(389, 525, 'REV', 15)
sw(g, '48V', 330, 580, False, RD); g.T(294, 585, '48V', 15); g.T(382, 585, 'ON', 15)
jack(g, 344, 664, 76); g.T(418, 673, 'Hi Z', 16); logo(g, 275, 727, 30); g.T(418, 753, 'LMW', 13); g.T(418, 773, '281F', 13)
OUT['Sound Skulptor MP AB528'] = g.out(kind='Preamp', ks='neve', bare=True, bg='#1f3046', bg2='#182638', kc=BK)

# ================= DI 503J (plate x 255..472, y 5..791)
g = D(255, 5, 472, 791, 30, '#f2f2f2')
g.T(276, 36, 'DI', 18); g.T(431, 36, '503J', 18)
sw(g, 'Mode FET / Pasv / Tube', 339, 93); g.T(306, 91, 'FET', 14); g.T(384, 91, 'TUBE', 14); g.T(339, 120, 'PASV', 14)
g.d.append(['poly', [g.P(398, 98), g.P(398, 112), g.P(372, 112)], g.ink, 1.3])
for nm, y, lab in [('Dist', 127, 'DIST'), ('Polarity', 195, 'POL'), ('Preamp On', 259, 'ON'), ('Lift', 332, 'LIFT')]:
    g.B(nm, 397, y, 38, WH); g.T(398, y + 32, lab, 14)
g.K('Preamp', 328, 191, 72, BK, {'ks': 'bakelite'}, [(-150, '0'), (150, '10')], 46, px=14, dots=False); ring(g, 328, 191, 46, 6, 0, 150, 6); g.T(339, 247, 'PREAMP', 15)
g.d.append(['poly', [g.P(310, 256), g.P(310, 263), g.P(370, 263)], g.ink, 1.3])
g.T(294, 307, 'RE-AMP', 14); g.d.append(['poly', [g.P(258, 318), g.P(384, 318), g.P(384, 340)], g.ink, 1.3])
g.K('Re-Amp Level', 328, 350, 72, BK, {'ks': 'bakelite'}, [(-150, '0'), (150, '10')], 46, px=14, dots=False); ring(g, 328, 350, 46, 6, 0, 150, 6); g.T(339, 409, 'LEVEL', 15)
g.B('Re-Amp On', 339, 447, 40, WH); g.T(339, 482, 'ON', 14)
jack(g, 339, 545, 76); g.T(339, 607, 'OUT', 15); jack(g, 360, 673, 76); g.T(360, 730, 'INSTRUMENT', 14); logo(g, 279, 727, 30)
OUT['Sound Skulptor DI 503J'] = g.out(kind='Preamp', ks='bakelite', bare=True, bg='#545d2a', bg2='#454d22', kc=BK)

# ================= MP 5.66 / 5.99 / 5.12 / 573 (common lower part)
def lower(g, cx, ys, lx, rx, first, mid1, polmid=None, mute=False):
    a, b, c = ys
    sw(g, first[0], cx, a); g.T(lx, a, first[1], 15); g.T(rx, a, first[2], 15)
    if mid1: g.T(cx, a + 32, mid1, 15)
    sw(g, 'Polarity' + (' / Mute' if mute else ''), cx, b, mute); g.T(lx, b, 'POL', 15); g.T(rx, b, 'REV', 15)
    if mute: g.T(cx, b - 34, 'MUTE', 15)
    sw(g, '48V', cx, c, False, RD); g.T(lx, c, '48V', 15); g.T(rx, c, 'ON', 15)
g = D(262, 5, 473, 791, 30, '#f2f2f2')
g.T(303, 36, 'MP', 19); g.T(427, 36, '5.66', 19); g.SCREW(366, 36, 16); g.SCREW(366, 762, 16)
for nm, y, lab in [('Out', 118, 'OUT'), ('In', 282, 'IN')]:
    g.K(nm, 366, y, 120, BK, {'ks': 'bakelite'}, [(-150, '0'), (150, '10')], 70, px=17, dots=False); ring(g, 366, y, 72, 11, -150, 150, 6); g.T(375, y + 82, lab, 17)
g.LED(289, 223, 10, '#35d06a', True); g.T(344, 400, 'GAIN', 15)
lower(g, 345, (432, 502, 564), 296, 396, ('Gain Low / Mid / High', 'LOW', 'HIGH'), 'MID')
jack(g, 371, 677, 76); g.T(307, 711, 'HIGH Z', 15); logo(g, 453, 400, 28)
OUT['Sound Skulptor MP 5.66'] = g.out(kind='Preamp', ks='bakelite', bare=True, bg='#4b5528', bg2='#3d461f', kc=BK)
def mp59(key, bg, bg2, x0, x1, dx, nm, led):
    g = D(x0, 5, x1, 791, 30, '#f2f2f2')
    X = lambda x: x + dx
    g.T(X(282), 44, 'MP', 19); g.T(X(400), 41, nm, 19); g.SCREW(X(349), 41, 16); g.SCREW(X(349), 759, 16)
    g.K('Pad', X(353), 125, 74, BK, {'ks': 'bakelite'}, [(0, '6')], 50, px=16, dots=False); spokes(g, X(353), 125, 46); g.T(X(361), 186, 'PAD', 16)
    g.K('Gain', X(357), 295, 76, BK, {'ks': 'bakelite'}, [(-90, '2'), (0, '5'), (90, '8')], 58, px=17, dots=False); spokes(g, X(357), 295, 48); g.T(X(360), 368, 'GAIN', 16)
    g.LED(X(273), 235, 10, led, led != '#7d7f82')
    lower(g, X(330), (441, 507, 568), X(282), X(381), ('Gain Low / Mid / High', 'LOW', 'HIGH'), 'MID')
    jack(g, X(353), 668, 76); g.T(X(301), 705, 'HIGH Z', 15); logo(g, X(454), 414, 28)
    OUT[key] = g.out(kind='Preamp', ks='bakelite', bare=True, bg=bg, bg2=bg2, kc=BK)
mp59('Sound Skulptor MP 5.99', '#a3141a', '#860f14', 244, 455, 0, '5.99', '#7d7f82')
mp59('Sound Skulptor MP 5.12', '#111214', '#08090a', 257, 466, 13, '5.12', '#35d06a')
g = D(244, 5, 458, 791, 30, '#f2f2f2')
g.T(283, 41, 'MP', 19); g.T(410, 38, '573', 19); g.SCREW(347, 41, 16); g.SCREW(347, 753, 16)
g.K('Trim', 357, 114, 64, '#a7abb1', {'ks': 'neve'}, [(-150, '-10'), (0, '0'), (150, '10+')], 50, px=14, dots=False); spokes(g, 357, 114, 40); g.T(364, 182, 'dB', 15)
g.LED(273, 227, 10, '#35d06a', True)
g.K('Gain', 346, 291, 128, '#a3151c', {'ks': 'chicken', 'sweep': [-17, 141]}, [(a, t) for a, t in zip([-17, 15, 48, 80, 112, 141], ['10', '20', '30', '40', '50', '60'])], 78, px=16, dots=False)
g.T(278, 371, 'dB', 16)
sw(g, 'Impedance 300 / 1200 / Line', 326, 441); g.T(335, 405, '1200 Ω', 15); g.T(280, 443, '300', 15); g.T(380, 443, 'LINE', 15)
sw(g, 'Polarity / Mute', 328, 509); g.T(328, 475, 'MUTE', 15); g.T(278, 509, 'POL', 15); g.T(378, 509, 'REV', 15)
sw(g, '48V', 328, 568, False, RD); g.T(278, 568, '48V', 15); g.T(378, 568, 'ON', 15)
jack(g, 362, 677, 76); g.T(301, 709, 'HIGH Z', 15); logo(g, 456, 414, 28)
OUT['Sound Skulptor MP 573'] = g.out(kind='Preamp', ks='neve', bare=True, bg='#1d3150', bg2='#162640', kc=BK)

# ================= EQ250 stereo EQ (plate x 170..610, y 5..786)
g = D(170, 5, 610, 786, 22, '#f2f2f2')
g.T(394, 36, 'EQ250', 20)
for x, y in [(280, 33), (508, 33), (280, 762), (508, 762)]: g.SCREW(x, y, 18)
ROWS = [(90, '#2f7fe6', ['600', '1k2', '3k6', '7k2', '21k'], 'HF'), (229, BK, ['280', '560', '1k7', '3k4', '10k'], 'HMF'),
        (376, '#3f9e6c', ['90', '180', '540', '1k1', '3k'], 'MF'), (519, BK, ['30', '60', '180', '360', '1k'], 'LMF'), (662, '#ee3a24', ['15', '30', '90', '180', '500'], 'LF')]
for y, col, fr, nm in ROWS:
    g.K(f'{nm} Freq', 251, y, 70, col, {'ks': 'neve', 'sweep': [-130, 130]}, list(zip([-130, -90, 0, 90, 130], fr)), 53, px=12, dots=False)
    ring(g, 251, y, 44, 9, -130, 130, 5); g.T(251, y + 70, 'Hz', 13)
    g.K(f'{nm} Q', 394, y, 78, col, {'ks': 'neve', 'sweep': [-140, 140]}, [(-140, '1'), (-90, '3')] + ([] if nm == 'HF' else [(0, '5')]) + [(90, '7'), (140, '9')], 48, px=13, dots=False)
    ring(g, 394, y, 46, 9, -140, 140, 5)
    for xx, w in [(365, 1), (422, 2)]:
        g.d.append(['poly', [g.P(xx - 12, y + 82), g.P(xx - 3 * w, y + 82), g.P(xx, y + 70), g.P(xx + 3 * w, y + 82), g.P(xx + 12, y + 82)], g.ink, 1.3])
    g.K(f'{nm} Gain', 556, y, 78, col, {'ks': 'neve'}, [] if nm == 'HF' else [(0, '0')], 48, px=13, dots=False); ring(g, 556, y, 44, 11, -150, 150, 5); g.T(556, y + 70, '–  dB  +', 13)
g.B('HF Shelf', 473, 178, 30, WH); g.d.append(['poly', [g.P(458, 225), g.P(466, 225), g.P(466, 211), g.P(486, 211)], g.ink, 1.4])
g.T(470, 433, 'EQ', 15); g.B('EQ In', 470, 465, 30, '#e8261e', None, False); g.T(470, 493, 'IN', 15)
g.B('LF Shelf', 470, 600, 30, WH); g.d.append(['poly', [g.P(455, 630), g.P(475, 630), g.P(475, 644), g.P(483, 644)], g.ink, 1.4])
g.T(408, 752, 'Sound Skulptor', 17); g.T(408, 776, 'Stereo EQ', 17)
OUT['Sound Skulptor EQ250'] = g.out(kind='EQ', ks='neve', ps='sq', bare=True, bg='#13283c', bg2='#0d1e2e', kc=BK)

# ================= EQ 573-II (plate x 260..482, y 5..795)
g = D(260, 5, 482, 795, 30, '#f2f2f2')
g.T(282, 30, 'EQ', 19); g.T(435, 30, '573-II', 19); g.SCREW(356, 30, 16); g.SCREW(356, 762, 16)
def conc(nm, y, labs, sweep, inner_name):
    rad = 79 if nm.startswith('MF') else 92
    g.K(nm, 354, y, 108, '#c4161c', {'ks': 'nevein', 'sweep': sweep}, labs, rad, px=13, dots=False)
    g.d.append(['pdots', *g.P(354, y), round(67 / g.W, 4), 24, round(6 / g.W, 4), g.ink, sweep[0], sweep[1]])
    g.K(inner_name, 354, y, 70, BK, {'ks': 'bakelite'}, None)
HFL = list(zip([87, 119, 146, 172, 197, 229], ['OFF', '10', '12', '16', '20', '25']))
MFL = list(zip([90, 117, 141, 167, 194, 229, 265, 302, 339, 370, 401, 428], ['OFF', '0.27', '0.36', '0.5', '0.7', '1.1', '1.6', '2.3', '3.2', '4.8', '7.2', '10']))
LFL = list(zip([83, 122, 147, 171, 196, 228], ['OFF', '20', '35', '60', '110', '220']))
conc('HF Freq', 119, HFL, [87, 229], 'HF Gain'); conc('MF Freq', 305, MFL, [90, 428], 'MF Gain'); conc('LF Freq', 476, LFL, [83, 228], 'LF Gain')
g.B('HiQ', 438, 216, 32, WH); g.T(404, 211, 'HiQ', 13)
g.d.append(['poly', [g.P(296, 190), g.P(282, 190), g.P(277, 196), g.P(277, 210)], g.ink, 1.5]); g.T(282, 224, 'kHz', 15)
g.d.append(['poly', [g.P(272, 250), g.P(278, 250)], g.ink, 1.5]); g.d.append(['poly', [g.P(292, 250), g.P(298, 250)], g.ink, 1.5])
g.d.append(['poly', [g.P(277, 560), g.P(277, 576), g.P(285, 582), g.P(296, 582)], g.ink, 1.5]); g.T(277, 602, 'Hz', 15)
g.d.append(['poly', [g.P(272, 650), g.P(282, 625), g.P(298, 620)], g.ink, 1.5])
sw(g, 'Out XLR / Off / Pre', 432, 590, True, '', .1); g.T(452, 562, 'XLR', 13); g.T(398, 592, 'OFF', 13); g.T(452, 620, 'PRE', 13)
g.K('HPF', 340, 681, 80, BK, {'ks': 'bakelite', 'sweep': [84, 241]}, list(zip([84, 111, 138, 170, 203, 241], ['OFF', '25', '45', '70', '160', '360'])), 60, px=15, dots=False)
logo(g, 445, 410, 30)
OUT['Sound Skulptor EQ 573-II'] = g.out(kind='EQ', ks='bakelite', bare=True, bg='#17243a', bg2='#111b2d', kc=BK)

# ================= EQP 501 (plate x 240..458, y 5..795)
g = D(240, 5, 458, 795, 30, '#f2f2f2')
g.T(273, 29, 'EQP', 19); g.T(413, 29, '501', 19); g.SCREW(356, 16, 14); g.SCREW(356, 778, 14)
def conc2(nm, x, y, labs, sweep, inner, rad=72):
    g.K(nm, x, y, 112, '#c4161c', {'ks': 'nevein', 'sweep': sweep}, labs, rad, px=13, dots=False)
    g.d.append(['pdots', *g.P(x, y), round(63 / g.W, 4), 18, round(6 / g.W, 4), g.ink, sweep[0], sweep[1]])
    g.K(inner, x, y, 72, BK, {'ks': 'bakelite'}, None)
conc2('Atten Freq', 354, 110, [(-110, '⏻'), (11, '5'), (43, '10'), (75, '20')], [-110, 75], 'HF Atten', 80)
g.T(387, 189, 'ATTEN', 14); sw(g, 'Atten / KCS', 378, 213, False, '', .08); g.T(382, 240, 'KCS', 14)
g.LED(380, 258, 10, '#35d06a', True); g.T(380, 278, 'EQ ON', 15)
BW = list(zip([-155, -122, -89, -56, -22, 15, 43, 70, 94, 115, 139], ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']))
g.K('Bandwidth', 295, 246, 70, BK, {'ks': 'bakelite', 'sweep': [-155, 139]}, BW, 50, px=14, dots=False); g.T(297, 312, 'B.WIDTH', 15)
conc2('HF Boost Freq', 373, 376, list(zip([-102, -67, -47, 0, 42, 71, 100, 127, 151, 175, 200, 225], ['2.5', '3', '3.5', '4', '5', '6', '7', '8', '10', '12', '15', '18'])), [-102, 225], 'HF Boost')
g.T(388, 484, 'KCS', 14); sw(g, 'HF Boost / KCS', 425, 484, False, '', .08); g.T(425, 514, 'BOOST', 14)
g.K('LF Atten', 295, 522, 70, BK, {'ks': 'bakelite', 'sweep': [-155, 139]}, BW, 50, px=14, dots=False); g.T(299, 586, 'ATTEN', 15)
conc2('LF Freq', 373, 657, list(zip([-99, -66, -29, 7, 42, 71], ['15', '20', '30', '45', '60', '100'])), [-99, 71], 'LF Boost')
g.T(385, 743, 'CPS', 14); sw(g, 'LF Boost / CPS', 425, 743, False, '', .08); g.T(425, 773, 'BOOST', 14)
logo(g, 292, 733, 30)
OUT['Sound Skulptor EQP 501'] = g.out(kind='EQ', ks='bakelite', bare=True, bg='#141d2c', bg2='#0e1520', kc=BK)

# ================= EQ 531T (photo 663x412, plate x 3..105, y 3..410)
g = D(3, 3, 105, 410, 14, '#f4f4f0')
g.T(16, 16, 'EQ', 9); g.T(89, 16, '531T', 9); g.SCREW(59, 17, 8); g.SCREW(59, 394, 8); logo(g, 97, 39, 11)
for nm, fy, gy, col, labs in [('HF', 59, 111, '#2d6fc4', [(31, 33, '9k'), (46, 33, '12k'), (8, 64, '2k'), (11, 85, 'Off')]),
                              ('MF', 158, 211, BK, [(30, 133, '2k3'), (46, 133, '5k'), (9, 145, '1k'), (11, 184, 'Off')]),
                              ('LF', 258, 311, '#b8191e', [(30, 233, '270'), (46, 233, '450'), (9, 243, '180'), (11, 284, 'Off')])]:
    g.K(f'{nm} Freq', 29, fy, 36, col, {'ks': 'nevein'}, None); ring(g, 29, fy, 23, 7, -150, 30, 2.2)
    for x, y, t in labs: g.T(x, y, t, 5.5 if x < 12 else 6.5)
    g.T(39, fy + 31, 'Hz', 6.5)
    g.T(82, fy + 7, f'— {nm} —', 7); g.d.append(['poly', [g.P(82, fy + 13), g.P(82, gy - 26)], g.ink, 1])
    g.K(f'{nm} Gain', 76, gy, 40, col, {'ks': 'nevein'}, [(0, '0')], 27, px=6.5, dots=False); ring(g, 76, gy, 25, 11, -150, 150, 2.4)
    g.T(82, gy + 32, '–  dB  +', 7)
g.B('EQ In', 39, 212, 12, '#e8261e', None, False); g.T(16, 212, 'EQ IN', 6)
g.K('HPF Freq', 29, 359, 40, '#8d9299', {'ks': 'nevein'}, None); ring(g, 29, 359, 26, 7, -30, 150, 2.4)
g.T(39, 329, '70', 6.5); g.T(51, 375, '400', 6.5); g.T(40, 384, 'Hz', 6.5)
g.B('HPF', 77, 357, 16, WH); g.T(77, 372, 'HPF', 7)
g.T(26, 396, 'Sound', 8); g.T(85, 400, 'Skulptor', 8)
OUT['Sound Skulptor EQ 531T'] = g.out(kind='EQ', ks='nevein', ps='sq', bare=True, bg='#5d672f', bg2='#4c5626', kc=BK)

# ================= LA 502 and LA 502-T (photos 662x412 / 654x412, plate width ~112 px)
def la(key, tube):
    g = D(3, 3, 115 if tube else 116, 410, 14, '#f4f4f0')
    g.T(26 if tube else 29, 16, 'LA', 9); g.T(80 if tube else 87, 16, '502-T' if tube else '502', 9)
    if not tube: g.SCREW(61, 17, 8); g.SCREW(61, 392, 8)
    for nm, y in [('Peak', 71 if tube else 59), ('Gain', 342 if tube else 334)]:
        if tube:
            g.K(nm, 57, y, 70, BK, {'ks': 'bakelite', 'sweep': [-155, 155]}, ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'], 46, -155, 155, 5.5, dots=False)
            g.d.append(['ticks', *g.P(57, y), round(38 / g.W, 4), 41, g.ink, -155, 155, .14, True])
            g.d.append(['vtxt', *g.P(8, y + 12), nm.upper(), g.sz(6), g.ink, round(8 / g.H, 4)])
        else:
            labs = [(-148, '0'), (-58, '30'), (62, '70'), (130, '100')] if nm == 'Peak' else [(-146, '0'), (-54, '30'), (11, '50'), (64, '70'), (128, '100')]
            g.K(nm, 58, y, 70, BK, {'ks': 'bakelite', 'sweep': [-148, 130]}, labs, 44, px=6.5, dots=False)
            g.d.append(['ticks', *g.P(58, y), round(38 / g.W, 4), 31, g.ink, 0, 130, .14, True])
            g.T(66, y + 46 if nm == 'Peak' else y + 44, nm.upper(), 7.5)
    if tube:
        rows = [(143, 'Ratio 3 / 6 / 20', '3', '6', '20'), (187, 'HPF Off / 100 / 200', '0', '200', '100Hz'), (227, 'Attack 5 / 10 / 20', '5', '20', '10mS'), (268, 'On / Off / Stereo', 'ON', 'STEREO', 'OFF')]
        tx, lx, rx = 42, 28, 66
        for y, nm, l, r, b in rows:
            sw(g, nm, tx, y); g.T(lx - (6 if l == 'ON' else 0), y, l, 6.5); g.T(rx + (12 if r == 'STEREO' else 0), y, r, 6.5); g.T(tx + 4, y + 15, b, 6.5)
        for y, t in [(143, 'RATIO'), (187, 'HPF'), (227, 'ATTK')]: g.d.append(['vtxt', *g.P(11, y - 4 * len(t) + 4), t, g.sz(6), g.ink, round(7.5 / g.H, 4)])
        logo(g, 96, 136, 12); g.T(91, 162, 'GR dB', 6.5); lx2, ly = 82, (174, 252)
        g.T(24, 400, 'Sound', 8); g.T(86, 400, 'Skulptor', 8); g.SCREW(55, 400, 8)
    else:
        rows = [(138, 'Ratio 3 / 6 / 20', 'RATIO', '3', '6', '20(LIM)'), (179, 'HPF Off / 100 / 200', 'HPF', '0', '200', '100Hz'), (221, 'Attack 5 / 10 / 20', 'ATTK', '5', '20', '10mS')]
        for y, nm, t, l, r, b in rows:
            sw(g, nm, 50, y); g.T(22, y - 12, t, 7); g.T(20, y + 2, l, 6.5); g.T(68, y + 2, r, 6.5); g.T(56, y + 16, b, 6.5)
        sw(g, 'Bypass / In / Stereo', 50, 266); g.T(21, 256, 'BYP', 7); g.T(72, 256, 'STER.', 7); g.T(45, 284, 'IN', 7)
        g.T(105, 126, 'GR', 7); g.T(105, 138, 'dB', 7); g.T(105, 151, '–', 7); lx2, ly = 91, (161, 239)
    for i, t in enumerate(['3', '6', '9', '12', '16', '20']):
        y = ly[0] + i * (ly[1] - ly[0]) / 5; g.LED(lx2, y, 6, '#ff3b30'); g.T(lx2 + 14, y, t, 6.5)
    OUT[key] = g.out(kind='Kompressor', ks='bakelite', bare=True, bg='#5d672f' if tube else '#14181d', bg2='#4c5626' if tube else '#0c0f12', kc=BK)
la('Sound Skulptor LA 502', False); la('Sound Skulptor LA 502-T', True)

sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in OUT.items()))
