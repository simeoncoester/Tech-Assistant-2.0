# Generator for 'SSL AWS 948' (channel strip) after the official SSL "AWS 916-924-948 Owner's Manual" (section 3, pages 3-5 to 3-11:
# input, meters, dynamics assign, HPF/EQ with G-EQ and Bell, cue/FX/EFX sends, Chop Pre/EFX, Return/In Line/Stereo, Rec/Track/Mix routing, V-pot pan, Sel/Solo/Cut, fader).
# The AWS centre section is mainly DAW control (TFT, transport); no master section is generated. Helpers from tools/ssl4000eg-gen.py.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
RED='#e0302a'; GRN='#2fb24a'; BLU='#25a6e8'; BLK='#151618'; GRYK='#b8b8b8'; WK='#ececec'
FM=[['10',1],['5',.91],['0',.82],['5',.73],['10',.64],['20',.53],['30',.425],['40',.33],['50',.24],['∞',.155]]
cols=['Input & Dynamics','Filter & EQ','Sends & Routing','Fader']
g=build(cols,110,600,.6)
K,B,SC,DOT,HL,LED,F=g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
T=g.T
def KN(k,name,x,y,dia,col,labs=None,unit=None,lab=None,lo=None,hi=None):
    K(k,name,x,y,dia,col,'round'); g.d.append(['pdots',round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y)/g.CH,4),round(dia*.68/g.CW,4),11,round(2.2/g.CW,4),'#f0f0f0',-140,140])
    if labs: SC(k,x,y,dia*.68+8,labs,.22)
    if lo: T(k,x-dia*.55,y+dia*.5+6,lo,.22)
    if hi: T(k,x+dia*.55,y+dia*.5+6,hi,.22)
    if unit: T(k,x,y+dia*.5+10,unit,.2)
    if lab: T(k,x-dia*.5-2,y-dia*.5-2,lab,.28)
def W(k,name,x,y,cap=None,dia=16): B(k,name,x,y,cap,WK,dia)
k=0
g.d.append(['rect',round((g.cx(k)+14)/g.CW,4),round((34+8)/g.CH,4),round(82/g.CW,4),round(150/g.CH,4),'#1d1e21','#888',4])
T(k,32,24,'REC',.3,'#ff4433'); T(k,78,24,'EDIT',.3,'#35d06a'); T(k,32,38,'OVER',.24,'#ff4433'); T(k,78,38,'OVER',.24,'#ff4433')
for col_x in (34,76): g.d.append(['leds',round((g.cx(k)+col_x)/g.CW,4),round((34+52)/g.CH,4),round((g.cx(k)+col_x)/g.CW,4),round((34+148)/g.CH,4),12,round(5/g.CW,4),'#35d06a',0,'#ff4433'])
for i,v in enumerate(['0','2','4','6','8','10','14','20','30','40','50','60']): T(k,55,58+i*8.2,v,.17,'#ddd')
for i in range(8): W(k,f'Group {i+1}',22+(i%4)*22,180+(i//4)*28,str(i+1),14)
W(k,'Group Pre',36,240,'PRE',16); W(k,'Group Pan',78,240,'PAN',16)
for i,nm in enumerate(['IP','OP','1','2']): W(k,f'Dyn {nm}',22+i*22,276,nm,14)
T(k,55,296,'DYNAMICS',.24)
HL(k,308)
KN(k,'Mic',30,340,24,RED,None,None,'MIC','+12','+75'); W(k,'48V',86,326,'48V',14); W(k,'Pad',86,354,'PAD',14)
KN(k,'Line',30,402,24,GRYK,None,None,'LINE','-20','+20'); W(k,'L Phase',86,388,'LØ',14); W(k,'R Phase',86,416,'RØ',14)
W(k,'Flip',86,446,'FLIP',14); LED(k,52,330,'#ff4433',5); LED(k,52,392,'#35d06a',5)
k=1
KN(k,'HPF',36,40,24,BLK,['20','30','60','100','300','500'],'Hz','HPF')
W(k,'G-EQ',90,76,'G-EQ',14); W(k,'HF Bell',90,104,'BELL',14)
KN(k,'HF Gain',30,108,22,RED,None,'dB','HF','-','+'); KN(k,'HF Freq',76,150,22,RED,['1.5','2','5','10','15','22'],'kHz')
KN(k,'HMF Gain',30,196,22,GRN,None,'dB','HMF','-','+'); KN(k,'HMF Freq',76,238,22,GRN,['.6','1','2','3','5','7'],'kHz'); KN(k,'HMF Q',30,276,22,GRN,None,'Q')
W(k,'Pre',90,280,'PRE',14); W(k,'Ins In',90,306,'INS IN',14); W(k,'EQ In',90,332,'EQ IN',14); LED(k,72,306,'#ffb020',5); LED(k,72,332,'#35d06a',5)
KN(k,'LMF Gain',30,362,22,BLU,None,'dB','LMF','-','+'); KN(k,'LMF Freq',76,404,22,BLU,['.2','.3','.6','1','1.6','2'],'kHz'); KN(k,'LMF Q',30,440,22,BLU,None,'Q')
KN(k,'LF Freq',76,488,22,BLK,['40','60','150','220','600'],'Hz'); KN(k,'LF Gain',30,530,22,BLK,None,'dB','LF','-','+'); W(k,'LF Bell',90,540,'BELL',14)
k=2
W(k,'Chop Pre/EFX',36,24,None,14); T(k,36,40,'CHOP PRE/EFX',.16)
KN(k,'Cue St Pan',82,40,22,BLU,None,None,None,'L','R'); T(k,22,64,'CUE ST',.24)
KN(k,'Cue St Level',30,100,24,GRN,None,None,None,'∞')
for i,nm in enumerate(['REC/MIX','CUE','CUE B','EFX','ON']): LED(k,62,64+i*14,'#ffb020',4); T(k,74,67+i*14,nm,.13)
W(k,'Cue Post',96,104,'POST',14)
T(k,16,150,'FX1',.24); KN(k,'FX1 Level',80,170,24,GRN,None,None,None,'∞')
for i,nm in enumerate(['FX3','EFX','ON']): LED(k,30,160+i*14,'#ffb020',4); T(k,44,163+i*14,nm,.13)
T(k,16,212,'FX2',.24); KN(k,'FX2 Level',30,236,24,GRN,None,None,None,'∞')
for i,nm in enumerate(['FX4','EFX','ON']): LED(k,62,224+i*14,'#ffb020',4); T(k,76,227+i*14,nm,.13)
W(k,'Alt/EFX Sel',92,272,'ALT EFX SEL',16)
HL(k,292)
W(k,'Return',36,310,'RETURN',14); T(k,36,330,'IN LINE',.16); T(k,36,342,'STEREO',.16)
W(k,'Rec',30,366,'REC',14); T(k,30,384,'TRACK',.16); W(k,'Mix',30,404,'MIX',14)
KN(k,'Pan/Width',80,384,26,BLU,None,None,None,'L','R'); T(k,80,358,'PAN/WIDTH',.16)
HL(k,430)
W(k,'V-Pot Solo',24,466,'SOLO',14); W(k,'V-Pot Cut',96,466,'CUT',14)
K(k,'V-Pot',60,474,30,BLU,'round'); g.d.append(['ticks',round((g.cx(k)+60)/g.CW,4),round((34+474)/g.CH,4),round(22/g.CW,4),11,'#bbb',-140,140,.2])
k=3
g.d.append(['rect',round((g.cx(k)+6)/g.CW,4),round((34+8)/g.CH,4),round(98/g.CW,4),round(44/g.CH,4),'#2c1b16','none',2]); T(k,55,34,'DISPLAY',.24,'#ff8a5a')
W(k,'Sel',55,82,'SEL',20); W(k,'Solo',32,114,'SOLO',20); B(k,'Cut',78,114,'CUT','#f0d0d0',20)
F(k,'Fader',62,160,580,FM,.82)
W(k,'Fader Flip',26,190,None,14)
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#48494d',bg2='#38393c',ink='#f0f0f0',kc=BLU,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
n=[q[1] for q in strip['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(f"  {json.dumps('SSL AWS 948')}: {json.dumps(strip,ensure_ascii=False)},\n")
