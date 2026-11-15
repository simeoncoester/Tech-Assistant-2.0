# Link Audio 500-series modules measured from the user's PDF photos ("link.pdf", 10 photos 996x996; only measuring templates,
# drawn anew): W92X (EQ), SLQ51X in four colour versions (EQ), F22X (filter), preamps SL9K-J, SL4K-E, PI312, PI512.
# Reuses the photo-coordinate helper class D from sslphoto-gen.py and small helpers from sskulptor-gen.py.
import os, sys, json
d0 = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(d0, 'sslphoto-gen.py')).read(); exec(src[:src.index('R7 = ')])
OUT = {}
WH, BK, GRY = '#e9eaec', '#1b1b1d', '#d6d8da'
RED, YEL, GRN = '#ff3b30', '#f5d22e', '#35d06a'
def ring(g, x, y, rad, n=13, a0=-150, a1=150, d=5, col=None): g.d.append(['pdots', *g.P(x, y), round(rad / g.W, 4), n, round(d / g.W, 4), col or g.ink, a0, a1])
def ticks(g, x, y, rad, n=12, a0=-150, a1=150, col='#d8262b'): g.d.append(['ticks', *g.P(x, y), round(rad / g.W, 4), n, col, a0, a1, .55, True])
def dial(g, nm, x, y, dia, col, labs=None, rad=None, px=12, sweep=(-150, 150)):
    # Link knob: grey skirt with coloured cap; white dots and red ticks alternate around it
    g.K(nm, x, y, dia, col, {'ks': 'neve', 'sweep': list(sweep)}, labs, rad or dia * .78, px=px, dots=False)
    ring(g, x, y, dia * .66, 11, sweep[0], sweep[1], 5.5); ticks(g, x, y, dia * .62, 10, sweep[0] + 15, sweep[1] - 15)
def logo(g, x, y, r=27):
    import math
    g.d.append(['shape', [g.P(x + r * math.cos(a / 12 * math.pi), y + r * math.sin(a / 12 * math.pi)) for a in range(24)], '#e2241e', '#f2f2f2']); g.T(x, y, 'LINK', 12, '#ffffff')
def hole(g, x, y, r=17): g.d.append(['led', *g.P(x, y), round(2 * r / g.W, 4), '#0a0a0b', False])
def strip(g, x0, x1, y0, y1, name, extra=''):
    g.R(x0, y0, x1 - x0, y1 - y0, '#e6e7e8', 'none', 2); g.T(x0 + 42, (y0 + y1) / 2, name, 18, '#1c1d20')
    if extra: g.T(x1 - 45, (y0 + y1) / 2, extra, 16, '#1c1d20')

# ================= W92X (photo 0: plate x 361..601, y 60..928)
g = D(352, 60, 603, 928, 30, '#f2f2f2')
hole(g, 467, 92); logo(g, 562, 93)
BANDS = [('HF', 130, 162, 213, '#3d8fe0', 'kHz', ['3', '3.5', '4', '6', '7', '10']),
         ('HMF', 290, 322, 375, '#2d9a5c', 'kHz', ['1', '2', '3', '5', '10', '16']),
         ('LMF', 450, 485, 535, '#f6d76a', 'Hz', ['60', '100', '200', '350', '500', '1000']),
         ('LF', 612, 645, 700, '#e8333a', 'Hz', ['50', '55', '70', '100', '200', '400'])]
FA = [-150, -110, -35, 35, 105, 150]
for i, (nm, ly, gy, fy, col, unit, fr) in enumerate(BANDS):
    g.T(373, gy - 50, nm, 13)
    dial(g, f'{nm} Gain', 395, gy, 76, col); g.T(395, gy + 46, '–  dB  +', 13)
    dial(g, f'{nm} Freq', 483, fy, 76, col, list(zip(FA, fr)), 53, px=12); g.T(483, fy + 50, unit, 12)
    g.B(f'{nm} In', 530, gy - 16, 30, WH); g.LED(582, gy - 16, 10, GRN)
    if i < 3:
        yy = BANDS[i + 1][2] - 64
        g.d.append(['poly', [g.P(365, yy), g.P(455, yy), g.P(485, yy + 14), g.P(598, yy + 14)], '#f2f2f2', 1.6])
g.d.append(['poly', [g.P(365, 765), g.P(455, 765), g.P(485, 780), g.P(598, 780)], '#f2f2f2', 1.6])
dial(g, 'Trim', 395, 815, 76, '#e5e6e8', [(-150, ''), (150, '')]); g.T(372, 880, '-20', 14); g.T(410, 880, 'TRIM', 14); g.T(448, 880, '+20', 14)
g.d.append(['poly', [g.P(484, 800), g.P(496, 788), g.P(512, 788)], '#f2f2f2', 1.6])
g.B('HPF', 525, 808, 37, WH); g.LED(580, 805, 10, YEL)
g.B('EQ On', 525, 857, 34, WH); g.T(484, 857, 'ON', 13); g.LED(580, 857, 10, GRN)
strip(g, 368, 595, 893, 925, 'W92X'); hole(g, 470, 909, 15)
OUT['Link Audio W92X'] = g.out(kind='EQ', ks='neve', ps='rd', bare=True, bg='#151617', bg2='#0b0c0d', kc=GRY)

# ================= SLQ51X (photo 1: plate x 334..581, y 50..935); four colour versions
def slq(key, cols, e_series, hf_top='14', hmf_top='7', lmf_low='.2', label=''):
    hf, hmf, lmf, lf = cols
    g = D(334, 50, 581, 935, 30, '#f2f2f2')
    hole(g, 408, 72); logo(g, 548, 72)
    for nm, y in [('HF', 100), ('HMF', 224), ('LMF', 518), ('LF', 760)]: g.T(354, y, nm, 12)
    for nm, y, col in [('HF Gain', 150, hf), ('HMF Gain', 272, hmf), ('LMF Gain', 570, lmf), ('LF Gain', 810, lf)]:
        dial(g, nm, 392, y, 84, col); g.T(392, y + 55, '–  dB  +', 14)
    for nm, y, col in [('HMF Q', 380, hmf), ('LMF Q', 700, lmf)]:
        dial(g, nm, 392, y, 84, col); g.T(392, y + 55, '⋏  Q  ⋀', 14)
    A = [-161, -110, -38, 45, 107, 146]
    for nm, y, col, labs, unit in [('HF Freq', 210, hf, ['1.4', '1.8', '4', '6', '9', hf_top], 'kHz'), ('HMF Freq', 345, hmf, ['.6', '.8', '2', '3', '4.5', hmf_top], 'kHz'),
                                   ('LMF Freq', 617, lmf, [lmf_low, '.3', '.7', '1', '1.5', '2'], 'kHz'), ('LF Freq', 750, lf, ['30', '50', '150', '200', '', '450'], 'Hz')]:
        dial(g, nm, 500, y, 84, col, list(zip(A, labs)), 56, px=13); g.T(509, y + 65, unit, 14)
    if e_series:
        btn = [('HF x3', 145, '×3'), ('HMF Shelf', 440, '⌐'), ('EQ On', 495, 'ON'), ('LMF Shelf', 545, '⌙'), ('LF /3', 845, '/3')]
    else:
        btn = [('HF Bell', 145, '⌒'), ('HMF Shelf', 440, '⌐'), ('EQ On', 495, 'ON'), ('LMF Shelf', 545, '⌙'), ('LF Bell', 845, '⌒')]
    for nm, y, t in btn:
        g.B(nm, 500, y, 36, WH); g.T(460, y if y != 145 else 135, t, 13)
    for y, c in [(440, YEL), (495, GRN), (550, YEL)]: g.LED(567, y, 10, c)
    strip(g, 340, 578, 900, 932, 'SLQ51X', label); hole(g, 455, 916, 15)
    OUT[key] = g.out(kind='EQ', ks='neve', ps='rd', bare=True, bg='#131415', bg2='#0a0a0b', kc=GRY)
slq('Link Audio SLQ51X', ['#f0358a', '#2d9a5c', '#3d9be0', '#1c1c1e'], True)
slq('Link Audio SLQ51X Brown', ['#c9262c', '#277a4c', '#3a7fc4', '#6b2f24'], False)
slq('Link Audio SLQ51X Orange', ['#ef2d2a', '#2d9a5c', '#3d9be0', '#f2771f'], False)
slq('Link Audio SLQ51X Black', ['#c9262c', '#277a4c', '#3a7fc4', '#1c1c1e'], False, '16', '9', '.15', 'BLACK')

# ================= F22X filter (photo 4: plate x 361..624, y 27..950)
g = D(361, 27, 624, 950, 30, '#f2f2f2')
hole(g, 490, 53); logo(g, 590, 57)
g.T(387, 107, 'LPF', 17)
dial(g, 'LPF Freq', 463, 157, 93, '#e8333a', list(zip([-150, -100, -35, 35, 100, 150], ['2', '3', '4', '6', '10', '22'])), 63, px=14); g.T(467, 216, 'kHz', 13)
g.B('LPF Range', 453, 257, 40, WH); g.T(400, 253, '0.5-22', 14); g.T(457, 292, 'RANGE', 14)
g.d.append(['poly', [g.P(384, 150), g.P(371, 150), g.P(371, 253), g.P(380, 253)], '#f2f2f2', 1.5])
dial(g, 'LPF Reso', 543, 253, 90, '#e8333a'); g.T(543, 311, 'RESO', 15)
dial(g, 'LPF Blend', 463, 367, 90, '#e8333a'); g.T(463, 420, 'BLEND', 11)
g.B('LPF On', 550, 360, 40, WH); g.LED(603, 361, 10, YEL); g.T(603, 383, 'ON', 14)
g.d.append(['poly', [g.P(366, 427), g.P(620, 427)], '#f2f2f2', 1.6])
g.T(387, 443, 'HPF', 17)
dial(g, 'HPF Blend', 467, 503, 86, '#3d8fe0'); g.T(467, 556, 'BLEND', 11)
g.B('HPF Range', 457, 600, 40, WH); g.T(400, 597, '20-150', 14); g.T(457, 636, 'RANGE', 14)
g.d.append(['poly', [g.P(384, 597), g.P(371, 597), g.P(371, 700), g.P(380, 700)], '#f2f2f2', 1.5])
dial(g, 'HPF Reso', 547, 603, 90, '#3d8fe0'); g.T(560, 657, 'RESO', 14)
dial(g, 'HPF Freq', 467, 700, 93, '#3d8fe0', list(zip([-150, -100, -35, 45, 150], ['20', '50', '150', '200', '500'])), 63, px=14); g.T(460, 755, 'Hz', 14)
g.B('HPF On', 550, 703, 40, WH); g.LED(602, 700, 10, YEL); g.T(603, 723, 'ON', 14)
g.d.append(['poly', [g.P(370, 797), g.P(470, 797), g.P(543, 747), g.P(613, 747)], '#f2f2f2', 1.6])
dial(g, 'Trim', 547, 830, 90, '#e5e6e8'); g.T(500, 879, '-20', 14); g.T(543, 881, 'TRIM', 14); g.T(588, 879, '+20', 14)
g.LED(410, 853, 10, GRN); g.B('On', 460, 853, 40, WH); g.T(410, 877, 'ON', 14)
strip(g, 370, 615, 907, 940, 'F22X'); hole(g, 490, 921, 15)
OUT['Link Audio F22X'] = g.out(kind='EQ', ks='neve', ps='rd', bare=True, bg='#131415', bg2='#0a0a0b', kc=GRY)

# ================= Preamps SL9K-J / SL4K-E / PI312 / PI512 (photo 6: plate x 336..592, y 34..965; same layout)
GA = [-170, -143, -112, -80, -43, -10, 28, 56, 128, 153]
def pre(key, name, col, gain):
    g = D(336, 34, 592, 965, 30, '#f2f2f2')
    hole(g, 465, 58); logo(g, 555, 58)
    g.T(362, 90, 'GAIN', 14)
    g.K('Gain', 438, 178, 118, col, {'ks': 'neve', 'sweep': [-170, 153]}, [(a, t) for a, t in zip(GA, gain) if t], 86, px=13, dots=False)
    ring(g, 438, 178, 76, 12, -170, 153, 6); ticks(g, 438, 178, 72, 11, -160, 143)
    g.R(533, 106, 52, 296, 'none', '#f2f2f2', 1)
    g.T(546, 120, 'PK', 12); g.LED(567, 120, 10, RED)
    for i, (t, y) in enumerate(zip(['14', '12', '9', '6', '3', '0', '4', '8', '12', '16', '22'], [164, 187, 207, 228, 250, 273, 295, 316, 337, 358, 380])):
        g.T(547, y, t, 12); g.LED(567, y, 10, RED if i == 0 else YEL if i < 5 else GRN)
    g.T(539, 262, '+', 11); g.T(539, 282, '–', 11)
    g.d.append(['poly', [g.P(342, 275), g.P(532, 275)], '#f2f2f2', 1.6])
    for nm, y, lab, led in [('48V', 305, '48V', RED), ('Pad', 360, 'PAD', GRN), ('Polarity', 416, 'POL', GRN)]:
        g.T(357, y, lab, 14); g.LED(383, y, 10, led); g.B(nm, 425, y - 3, 42, WH)
    g.d.append(['poly', [g.P(345, 476), g.P(352, 466), g.P(362, 466)], '#f2f2f2', 1.6]); g.LED(383, 470, 10, YEL); g.B('HPF', 425, 468, 42, WH)
    dial(g, 'HPF Freq', 508, 470, 98, '#3d8fe0', [(-144, '10'), (-44, '80'), (60, '150'), (136, '250')], 66, px=13); g.T(522, 525, 'Hz', 14)
    g.d.append(['poly', [g.P(345, 581), g.P(355, 581), g.P(363, 590)], '#f2f2f2', 1.6]); g.LED(383, 585, 10, YEL); g.B('LPF', 425, 585, 42, WH)
    dial(g, 'LPF Freq', 512, 592, 98, '#3d8fe0', [(-139, '3.5'), (-25, '7'), (52, '10'), (94, '14'), (125, '20')], 64, px=13); g.T(512, 652, 'kHz', 11)
    g.T(357, 707, 'COL', 14); g.LED(384, 705, 10, YEL); g.B('Colour', 428, 705, 42, WH)
    dial(g, 'Drive', 505, 714, 90, '#d8333a'); g.T(536, 770, 'DRV', 13)
    g.d.append(['poly', [g.P(345, 781), g.P(588, 781)], '#f2f2f2', 1.6])
    g.K('Fader', 430, 855, 118, '#d8333a', {'ks': 'neve', 'sweep': [-145, 133]}, [(-145, '-100'), (-98, '-20'), (-39, '-10'), (48, '0'), (92, '6'), (133, '12')], 80, px=12, dots=False)
    ring(g, 430, 855, 74, 12, -145, 133, 6); ticks(g, 430, 855, 70, 11, -135, 123)
    g.d.append(['poly', [g.P(470, 808), g.P(478, 793), g.P(489, 793)], '#f2f2f2', 1.5]); g.T(530, 909, 'FADER', 14)
    strip(g, 340, 588, 929, 957, name); hole(g, 465, 943, 15)
    OUT[key] = g.out(kind='Preamp', ks='neve', ps='rd', bare=True, bg='#151617', bg2='#0b0c0d', kc=GRY)
pre('Link Audio SL9K-J', 'SL9K-J', '#c8262d', ['16', '18', '20', '22', '28', '34', '40', '46', '64', '68'])
pre('Link Audio SL4K-E', 'SL4K-E', '#2f86d8', ['26', '30', '34', '', '42', '46', '50', '54', '66', '68'])
pre('Link Audio PI312', 'PI312', '#f2dc86', ['26', '30', '34', '36', '40', '42', '46', '48', '56', '60'])
pre('Link Audio PI512', 'PI512', '#2e8a5a', ['26', '30', '34', '36', '40', '42', '46', '48', '56', '60'])

sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in OUT.items()))
