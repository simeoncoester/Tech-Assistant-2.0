# Generator for 'SSL XL-Desk' (mono channel strip with VHD pre) and 'SSL XL-Desk Master Section'.
# Source: official SSL XL-Desk Owner's Manual and XL-Desk Recall Sheet (solidstatelogic.com, xl-desk downloads).
# Knob colours from the manual text (red gain, black trim/level, green cue/aux, blue pan/balance). Helpers from tools/ssl4000eg-gen.py.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
INK='#1d1f22'; RED='#d23a32'; GRN='#2e8a4a'; BLU='#2f6fc4'; BLK='#1b1c1f'; SB='#2a2b2e'; GY='#8f9398'
CHF=[['10',1],['5',.83],['0',.76],['5',.64],['10',.556],['20',.39],['30',.25],['∞',0]]
MXF=[['0',1],['5',.92],['10',.84],['15',.76],['20',.68],['30',.565],['40',.465],['50',.36],['60',.27],['∞',0]]
def kit(g):
    K,B,SC,DOT,HL,LED,F=g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
    T=lambda k,x,y,t,sz=.5,col=INK: g.T(k,x,y,t,sz,col)
    for e in g.d:
        if e[0]=='txt' and e[5]=='#c9d2dc': e[5]=INK
    def KN(k,name,x,y,dia,col,lo=None,hi=None,mid=None,unit=None):
        K(k,name,x,y,dia,col); g.d.append(['pdots',round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y)/g.CH,4),round(dia*.7/g.CW,4),11,round(2.2/g.CW,4),INK,-140,140])
        if lo: T(k,x-dia*.55,y+dia*.5+6,lo,.24)
        if hi: T(k,x+dia*.55,y+dia*.5+6,hi,.24)
        if mid: T(k,x,y-dia*.5-6,mid,.24)
        if unit: T(k,x,y+dia*.5+10,unit,.2)
    def SQ(k,name,x,y,cap=None,dia=16): B(k,name,x,y,cap,SB,dia)
    return T,K,B,SC,DOT,HL,LED,F,KN,SQ

cols=['Mic Pre & Trim','Cue, Aux & Pan','Fader']
g=build(cols,110,600,.6)
T,K,B,SC,DOT,HL,LED,F,KN,SQ=kit(g)
k=0; T(k,24,10,'MIC PRE',.3)
SQ(k,'VHD',24,34); T(k,24,50,'VHD',.22); SQ(k,'Hi-Z',24,74); T(k,24,90,'Hi-Z',.22)
SQ(k,'+48V',24,114); T(k,24,130,'+48V',.22); SQ(k,'Pad',24,154); T(k,24,170,'PAD',.22)
KN(k,'Harmonics',78,50,26,BLK,'2nd','3rd'); KN(k,'Mic Gain',78,140,28,RED,'+15','+75',None,'dB')
HL(k,190); T(k,20,204,'TRIM',.3)
KN(k,'Trim',36,244,28,BLK,'-20','+20','0','dB'); LED(k,46,282,'#35d06a',6)
SQ(k,'DAW',88,212); T(k,88,228,'DAW',.2); SQ(k,'Phase',88,248,'Ø'); SQ(k,'500',88,284); T(k,88,300,'500',.2)
SQ(k,'Chop Post',28,322); T(k,58,325,'CHOP POST',.2); SQ(k,'Ins',88,322); T(k,88,338,'INS',.2)
k=1; T(k,24,10,'CUE ST',.3)
KN(k,'Cue Pan',76,36,24,BLU,'L','R'); KN(k,'Cue Level',30,86,26,GRN,'∞',None)
SQ(k,'Cue Post',90,80); T(k,90,96,'POST',.2); SQ(k,'Alt',90,112); T(k,90,128,'ALT',.2)
KN(k,'Aux 1',76,160,26,GRN,'∞',None); T(k,32,162,'AUX 1',.26)
KN(k,'Aux 2',30,220,26,GRN,'∞',None); T(k,82,222,'AUX 2',.26)
HL(k,252); T(k,20,266,'PAN',.3); KN(k,'Pan',76,290,26,BLU,'L','R')
HL(k,320)
for i,b in enumerate('ABCD'): SQ(k,f'Mix {b}',20+i*24,350,b,16)
B(k,'Cut',50,392,'CUT',SB,22); B(k,'Solo',50,428,'SOLO',SB,22)
g.d.append(['rect',round((g.cx(k)+6)/g.CW,4),round((34+454)/g.CH,4),round(98/g.CW,4),round(50/g.CH,4),'#c9c9c9','none',2])
k=2; F(k,'Fader',50,40,580,CHF,.76)
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#e3e3e1',bg2='#cfcfcd',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

mcols=['Stereo Returns','Master Trims','Mix B, C, D','Mix A & Solo','Monitoring','Foldback & Talk']
g=build(mcols,110,600,.5)
T,K,B,SC,DOT,HL,LED,F,KN,SQ=kit(g)
k=0
for j,y0 in enumerate((10,300)):
    n=j+1; T(k,22,y0,f'ST RET {n}',.26)
    SQ(k,f'Return {n} St Cue',30,y0+26); T(k,30,y0+42,'ST CUE',.18); SQ(k,f'Return {n} Mono',30,y0+64); T(k,30,y0+80,'MONO',.18)
    KN(k,f'Return {n} Balance',80,y0+40,22,BLU,'L','R'); KN(k,f'Return {n} Level',80,y0+120,24,BLK,'∞',None,None,'LEVEL')
    SQ(k,f'Return {n} AFL',30,y0+116); LED(k,14,y0+116,'#9aa0a6',5); T(k,30,y0+132,'AFL',.18)
    for i,b in enumerate('ABCD'): SQ(k,f'Return {n} {b}',20+i*24,y0+176,b,14)
k=1
for i,(nm,b2) in enumerate([('ST CUE','TO A'),('AUX 1','PRE'),('AUX 2','PRE')]):
    y=30+i*170; T(k,55,y-14,nm,.26)
    KN(k,f'{nm.title()} Master',55,y+20,26,GRN,'∞','+10','0')
    SQ(k,f'{nm.title()} AFL',55,y+66); LED(k,32,y+66,'#9aa0a6',5); T(k,80,y+68,'AFL',.2)
    SQ(k,f'{nm.title()} {b2.title()}',55,y+100); T(k,82,y+102,b2,.2)
k=2
for i,m in enumerate('BCD'):
    y0=14+i*196; T(k,55,y0,f'MIX {m}',.32)
    for j,nm in enumerate(['500','INS','SUM','TO A']): B(k,f'Mix {m} {nm.title()}',30+(j%2)*50,y0+30+(j//2)*44,None,SB,18); T(k,30+(j%2)*50,y0+48+(j//2)*44,nm,.18)
    KN(k,f'Mix {m} Level',36,y0+138,24,BLK,'∞','+10','0'); SQ(k,f'Mix {m} AFL',88,y0+138); T(k,88,y0+154,'AFL',.18)
k=3
for j,nm in enumerate(['500','INS','SUM','COMP']): B(k,f'Mix A {nm.title()}',28,30+j*40,None,SB,18); T(k,62,32+j*40,nm,.2)
F(k,'Mix A Fader',36,200,580,MXF,1,'#e04a3a')
g.d.append(['rect',round((g.cx(k)+58)/g.CW,4),round((34+200)/g.CH,4),round(48/g.CW,4),round(110/g.CH,4),'#cfcfcd','none',2]); T(k,82,214,'SOLO MASTER',.16)
for j,nm in enumerate(['CLEAR','SAFE','AFL']): B(k,f'Solo {nm.title()}',82,236+j*28,None,SB,14); T(k,82,250+j*28,nm,.15)
k=4
KN(k,'AFL Level',28,40,22,BLK,'∞','+6',None,'AFL'); KN(k,'Dim Level',28,104,22,BLK,'-30','-3',None,'DIM')
K(k,'Monitor Level',40,190,40,BLK); SC(k,40,190,30,['0','1','2','3','4','5','6','7','8','9','10','11'],.22,-140,140); T(k,40,232,'MONITOR LEVEL',.18)
B(k,'Dim',22,280,'DIM',SB,20); B(k,'Monitor Cut',62,280,'CUT',SB,20)
T(k,80,22,'MON SELECT',.18)
for j,nm in enumerate(['SUB','MINI 1','MINI 2','MONO']): B(k,'Mon '+nm.title(),84,46+j*36,None,SB,16); T(k,84,62+j*36,nm,.16)
T(k,40,320,'MON SOURCE',.18)
for j,nm in enumerate(['SUM','JACK','EXT','MIX A']): B(k,'Source '+nm.title(),20+j*24,346,None,SB,14); T(k,20+j*24,362,nm,.13)
k=5
T(k,55,14,'FOLDBACK',.26); T(k,30,30,'A ST CUE',.18); T(k,80,30,'B AUX 1',.18)
KN(k,'Foldback A Level',30,64,22,BLK,None,None,None,'LEVEL'); KN(k,'Foldback B Level',80,64,22,BLK,None,None,None,'LEVEL')
SQ(k,'Foldback A Mon',30,110); T(k,30,126,'MON',.18); SQ(k,'Foldback B Mon',80,110); T(k,80,126,'MON',.18)
B(k,'Talk A',30,160,'TALK A',SB,20); B(k,'Talk B',80,160,'TALK B',SB,20)
HL(k,188); T(k,55,202,'H/P',.24)
KN(k,'Headphone Level',34,236,22,BLK,None,None,None,'LEVEL'); SQ(k,'H/P F/B A',84,224,'F/B A',14); SQ(k,'H/P F/B B',84,252,'F/B B',14)
KN(k,'Talk Level',34,304,22,BLK,None,None,None,'TALK'); KN(k,'Listen Level',84,304,22,BLK,None,None,None,'LISTEN')
B(k,'Listen',55,352,'LISTEN',SB,20)
master=dict(kind='Master Section',pages=pages_of(g,[('Returns & Trims',0,1),('Mix Busse',2,3),('Monitor & Foldback',4,5)],len(mcols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#e3e3e1',bg2='#cfcfcd',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('SSL XL-Desk',strip),('SSL XL-Desk Master Section',master)]))
