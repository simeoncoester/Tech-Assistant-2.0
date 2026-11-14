# Generator for 'Neve Genesys' (channel strip) and 'Neve Genesys Master Section'
# after the AMS Neve "Genesys User Manual" (issue 11, panel drawings pages 44-90): channel section, processing,
# auxes, direct output, monitor path, channel meter + routing, automated fader; monitor panel with Tone/RTB, meters,
# Master SEL, Route SEL, Cue Mix 1/2, Talkback, Rev Returns, 8T auxes, aux masters/mix/headphones, control room.
# Drawings are black-and-white, so panel/knob colours are an assumption (light grey panel, black knobs).
import os, sys, json
d0=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(d0,'ssl4000eg-gen.py')).read(); exec(src[:src.index('# ================= channel strip')])
h=open(os.path.join(d0,'harrison32c-gen.py')).read(); exec(h[h.index("INK='#16181b'"):h.index("cols=['Input")])
GF=[[l,round(1-f,3)] for l,f in [('10',0),('5',.1),('0',.2),('5',.33),('10',.45),('20',.58),('30',.69),('40',.81),('∞',.95)]]
def LEDS(k,x,y0,y1,n,col='#35d06a',red=0):
    g.d.append(['leds',round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y0)/g.CH,4),round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y1)/g.CH,4),n,round(4/g.CW,4),col,0,'#ff4433'])
def LL(k,x,y,lab,col='#ff4433'): LED(k,x,y,col,4); T(k,x,y+11,lab,.14)

cols=['Channel','Processing & Pan','Auxes & Direct','Monitor','Meter & Routing','Fader']
g=build(cols,110,600,.6)
K,B,SC,HL,LED,F,T,KN,SW,TK=kit(g)
k=0
K(k,'Mic Gain',55,70,46,KB,'round'); TK(k,55,70,30); SC(k,55,70,38,['+20','+35','+55','+70'],.3)
for i,l in enumerate(['CH','DAW','FNC']): LL(k,33+i*22,118,l,'#ffb020')
SW(k,'48V',30,160,'+48V'); SW(k,'Hi Z',84,160,'HI Z')
SW(k,'Pad',30,196,'PAD'); SW(k,'Phase',84,196,'Ø')
SW(k,'90Hz',84,232,'90 Hz')
HL(k,258); T(k,55,272,'INPUT TRIM',.2)
KN(k,'Input Trim',36,310,30,'-15','+15','0')
for i,l in enumerate(['MIC','LN','DAW','DLN']): LL(k,84,288+i*22,l,'#35d06a')
T(k,55,580,'GENESYS',.3)
k=1
T(k,55,18,'PROCESSING',.22)
for i,l in enumerate(['DYN','EQ','INS 1','INS 2']): SW(k,l.replace(' ',''),30,44+i*36,l)
SW(k,'ORD',84,62,'ORD'); LL(k,70,100,'CH','#ffb020'); LL(k,98,100,'MON','#ffb020')
HL(k,190); T(k,55,204,'PAN',.22)
KN(k,'Pan',44,250,34,'L','R','C'); LED(k,86,280,'#ffb020',5); T(k,86,292,'IN',.16)
k=2
KN(k,'Aux 5/6 Pan',30,30,22,'L','R'); LL(k,84,30,'AUX 6')
for i,(nm,bt) in enumerate([('Aux 5/6','7/8'),('Aux 4','8'),('Aux 3','7'),('Aux 2','8'),('Aux 1','7')]):
    y=86+i*82
    SW(k,f'{nm} >8T',30,y-6,f'>8T {bt}')
    KN(k,nm,80,y,24,None,None,None); T(k,55,y+34,nm.upper(),.18)
    for j,l in enumerate(['PRE','ON','MON']): LL(k,26+j*29,y+46,l,'#35d06a')
k=3
T(k,30,18,'DAW',.2); SW(k,'DAW',30,38,None,16,False); LL(k,16,62,'SND','#35d06a'); LL(k,44,62,'RET','#35d06a')
KN(k,'Mon Level',80,40,28,None,'+10'); LED(k,98,72,'#ffb020',4); T(k,98,84,'AUT',.14)
KN(k,'Mon Pan',30,120,28,'L','R'); LED(k,50,150,'#ffb020',4); T(k,50,162,'IN',.14)
LED(k,80,98,'#35d06a',4); T(k,80,110,'DMON',.14)
SW(k,'I/P 2',84,132,'I/P 2'); SW(k,'Mon CH',84,166,'CH')
for i,l in enumerate(['ISO','SEL','>8T','SOLO']): SW(k,'Mon '+l,30,200+i*38,l,15,True,'#f1d24a' if l=='SEL' else SB)
g.d.append(['rect',round((g.cx(k)+60)/g.CW,4),round((g.ry(k)+34+196)/g.CH,4),round(46/g.CW,4),round(70/g.CH,4),'none',INK,2])
T(k,83,206,'TO MON',.16)
for i,l in enumerate(['DYN','INS1','EQ','INS2']): LL(k,72+(i%2)*24,220+(i//2)*26,l,'#35d06a')
SW(k,'SWP',84,290,'SWP'); SW(k,'Mon Cut',84,330,'CUT',16,True,'#e04a3a')
k=4
T(k,55,16,'CH METER',.2); LEDS(k,40,30,250,24,'#35d06a')
for v,y in [('+22',34),('12',80),('4',124),('0',146),('8',190),('20',248)]: T(k,62,y,v,.16)
T(k,22,30,'+3',.16); T(k,22,140,'0',.16); T(k,22,248,'-20',.16)
for i,l in enumerate(['MON','CH']): SW(k,'Mix '+l,24+i*30,290,None,12,False); T(k,24+i*30,305,l,.13)
T(k,39,318,'MIX',.14)
for i,l in enumerate(['CH','SND','RET']): SW(k,'Mtr '+l,24+i*30,340,None,12,False); T(k,24+i*30,355,l,.13)
T(k,54,368,'MTR',.14)
for i in range(8): SW(k,f'8T {i+1}',22+(i%4)*24,394+(i//4)*36,None,12,False); T(k,22+(i%4)*24,409+(i//4)*36,str(i+1),.13)
T(k,58,474,'8T',.16); LL(k,40,500,'SIG','#35d06a'); LL(k,70,500,'GR','#ffb020')
k=5
SW(k,'Solo',30,30,'SOLO',16,False,'#f1d24a'); SW(k,'Cut',84,30,None,16,False,'#e04a3a'); T(k,84,48,'CUT',.17)
g.c.append(['x','Scribble|',round((g.cx(k)+55)/g.CW,4),round((g.ry(k)+34+80)/g.CH,4),round(84/g.CW,4),'#1d1d1f','n',{'dar':4,'lines':1,'ph':['Name'],'max':8}])
F(k,'Fader',62,120,580,GF,.8)
strip=dict(kind='Channel Strip',pages=pages_of(g,[('Channel & Processing',0,1),('Auxes & Monitor',2,3),('Meter & Fader',4,5)],len(cols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#e3e4e2',bg2='#cfd0ce',ink=INK,kc=KB,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

mcols=['Tone & RTB','Meters','Master SEL','Route SEL','Cue Mix 1','Cue Mix 2','Talkback','Rev Returns','Aux Masters & Mix','8T Auxes','Control Room','Monitor & Fader']
g=build(mcols,110,600,.5,6)
K,B,SC,HL,LED,F,T,KN,SW,TK=kit(g)
k=0
KN(k,'Sig Pres',30,40,24,'-35','+26','+4'); T(k,30,72,'SIG PRES',.16)
KN(k,'RTB',84,40,24); T(k,84,72,'RTB',.16)
KN(k,'Osc Level',44,120,28); T(k,44,152,'OSC LEVEL',.16); LL(k,90,108,'CAL','#35d06a'); LL(k,90,134,'PNK','#35d06a')
K(k,'Osc Frq',55,210,30,KB,'round'); TK(k,55,210,19); SC(k,55,210,30,['50Hz','440','1k','10k','15k','OFF'],.24)
for i,l in enumerate(['CH','8T','2T/MIX','LS']): SW(k,'Osc '+l.replace('/',' '),30+(i%2)*54,280+(i//2)*40,l,15,False)
k=1
for j,(grp,ls) in enumerate([('CH MTRS',['CH I/P','DAW SND','DAW RET']),('8T MTRS',['8T','AUX','EXT','CRM']),('2T MTRS',['MIX','CRM','2T','CUE 1/2'])]):
    y0=24+j*150; T(k,55,y0,grp,.2)
    for i,l in enumerate(ls): SW(k,f'{grp[:2]} Mtr {l}',30+(i%2)*54,y0+24+(i//2)*44,l,15,False)
k=2
T(k,55,18,'MASTER SEL',.2); SW(k,'Lock',55,40,'LOCK',15,False)
for i,l in enumerate(['MIC','LN','DAW']): SW(k,'Ch Sel '+l,22+i*33,92,l,13,False)
LED(k,100,72,'#35d06a',4); T(k,100,64,'DLN',.13); T(k,55,124,'CH SEL',.16)
for i,l in enumerate(['SWP','MIX']): SW(k,'Status '+l,36+i*38,150,l,13,False)
T(k,55,180,'STATUS',.16)
for i,l in enumerate(['CH SAFE','MON SAFE','I/L','LATCH','RESET','LINK']): SW(k,l.title(),30+(i%2)*50,206+(i//2)*40,l,13,False)
T(k,55,322,'SOLO',.16)
for i,l in enumerate(['DAW SND','DAW RTN','I/P 2']): SW(k,'Mon Sel '+l,22+i*33,350,l,13,False)
LED(k,100,330,'#35d06a',4); T(k,100,322,'DMON',.13); T(k,55,382,'MON SEL',.16)
k=3
T(k,55,18,'ROUTE SEL',.2)
for i,l in enumerate(['LOAD','SAVE','FILING','RTE SEL','◀','▶']): SW(k,'Route '+l,30+(i%2)*50,40+(i//2)*40,l,15,False)
for i in range(8): B(k,f'Route {i+1}',30+(i%2)*50,170+(i//2)*36,str(i+1),SB,15)
T(k,55,310,'8T',.16)
for i,l in enumerate(['CH','MON','L','R']): SW(k,'Route '+l if l in 'LR' else 'Route Path '+l,30+(i%2)*50,336+(i//2)*40,l,15,False)
T(k,55,410,'MIX',.16)
def CUE(k,n):
    KN(k,f'Cue {n} Ext',30,34,24); T(k,74,30,'EXT 1-4',.16); LL(k,30,64,'ON','#35d06a')
    KN(k,f'Cue {n} Util',80,100,24); T(k,80,72,'UTIL',.16)
    for i,l in enumerate(['MIX','ON','CRM']): LL(k,56+i*24,128,l,'#35d06a')
    KN(k,f'Cue {n} Aux',30,170,24); T(k,74,172,'AUX 1-6',.16); LL(k,30,140,'ON','#35d06a')
    for i,l in enumerate(['1/2','3/4','5','6']): LL(k,18+i*24,200,l,'#ffb020')
    KN(k,f'Cue {n} Tilt EQ',30,250,24,'+LF','+HF'); T(k,30,280,'TILT EQ',.14)
    LL(k,70,234,'MONO','#35d06a'); KN(k,f'Cue {n} Bal',80,290,24,'L','R'); T(k,80,318,'BAL',.14)
    KN(k,f'Cue {n} Level',30,350,24); LL(k,30,320,'ON','#35d06a'); T(k,30,380,'LEVEL',.14)
    T(k,70,410,f'CUE MIX {n}',.2)
CUE(4,1); CUE(5,2)
k=6
for i,l in enumerate(['CUE 1','CUE 2','SLATE','TB']): x=30+(i%2)*54; y=46+(i//2)*90; KN(k,'TB '+l.title(),x,y,26); T(k,x,y-22,l,.18); LED(k,x,y+30,'#35d06a',4)
for i,l in enumerate(['RED LIGHT','TB ALL']): SW(k,l.title(),30+i*54,250,l,18,False,'#e04a3a' if i==0 else SB)
B(k,'TB Spare',55,300,None,SB,18)
k=7
for j in range(2):
    y0=j*210; n=j+1
    K(k,f'Rev {n} Level',55,y0+44,40,KB,'round'); TK(k,55,y0+44,26); SC(k,55,y0+44,32,['∞','-30','-5','0','15'],.22)
    LL(k,34,y0+82,'REV','#35d06a'); LL(k,76,y0+82,'DAW','#35d06a')
    KN(k,f'Rev {n} To Cue',30,y0+128,22); T(k,30,y0+108,'TO CUE',.13)
    for i,l in enumerate(['PRE','ON','1/2']): LL(k,62+i*18,y0+126,l,'#35d06a')
    KN(k,f'Rev {n} Width',30,y0+172,20,'N','W'); KN(k,f'Rev {n} Pan',80,y0+172,20,'L','R'); T(k,80,y0+154,'PAN/BAL',.12); T(k,30,y0+154,'WIDTH',.12)
    T(k,55,y0+204,f'REV {n} RET',.16)
k=7
for i,l in enumerate(['MONO','ON','ISO','AFL']): SW(k,'Rev '+l.title(),22+i*22,446,None,11,False); T(k,22+i*22,460,l,.12)
k=8
T(k,55,16,'AUX MASTERS',.2)
for i in range(6): KN(k,f'Aux Master {i+1}',30+(i%2)*54,46+(i//2)*58,22); T(k,30+(i%2)*54,74+(i//2)*58,f'AUX {i+1}',.14)
HL(k,210); KN(k,'IMR',36,250,28); T(k,36,282,'IMR',.16); LL(k,84,236,'ON','#35d06a')
SW(k,'Mix Pre',84,272,'PRE'); SW(k,'Mix Ins',84,310,'INS'); T(k,55,344,'MIX',.18)
HL(k,360); T(k,55,374,'HEADPHONES',.18)
KN(k,'Headphones',55,426,30); LL(k,22,400,'CRM','#35d06a')
for i,l in enumerate(['EXT','1','CUE 2']): LL(k,26+i*29,466,l,'#35d06a')
k=9
for j in range(2):
    x0=j*54
    KN(k,f'8T{j+1} Aux 5/6 Pan',x0+28,40,20,'L','R')
    for i,l in enumerate(['AUX 5/6','AUX 3/4','AUX 1/2']):
        y=96+i*60; KN(k,f'8T{j+1} {l.title()}',x0+28,y,20); T(k,x0+28,y+20,l,.11)
        LL(k,x0+16,y+34,'PRE','#35d06a'); LL(k,x0+40,y+34,'ON','#35d06a')
    for i,l in enumerate(['ISO','SEL','PRE','INS']): SW(k,f'8T{j+1} {l}',x0+28,300+i*34,l,12,False,'#f1d24a' if l=='SEL' else SB)
    T(k,x0+28,446,f'8T{j+1}',.16)
k=10
T(k,55,16,'CONTROL ROOM',.2)
src_=['AUX 1','AUX 2','AUX 3','AUX 4','AUX 5','AUX 6','CUE 1','CUE 2','MIX','8T','2T','EXT 1','EXT 2','EXT 3','EXT 4','INT','EXT','SUM','INS','ST','ØL','PFL','SIF','M2 SEL','SWP']
for i,l in enumerate(src_):
    x=20+(i%4)*24; y=40+(i//4)*36; SW(k,'CRM '+l,x,y,None,11,False); T(k,x,y+14,l,.11)
for i,l in enumerate(['A','B','M1','M2']): SW(k,'Spk '+l,20+i*24,300,None,12,False,'#f1d24a'); T(k,20+i*24,316,l,.13)
k=11
for i,l in enumerate(['L','C','R','LS','S','RS']): SW(k,'LS Cut '+l,20+(i%3)*34,30+(i//3)*34,None,12,False); T(k,20+(i%3)*34,46+(i//3)*34,l,.13)
K(k,'Monitor Level',55,128,48,KB,'round'); TK(k,55,128,32)
for i,l in enumerate(['CUT','DIM','MONO']): SW(k,'Monitor '+l.title(),22+i*33,188,l,14,False,'#e04a3a' if l=='CUT' else SB)
SW(k,'Main Solo',30,236,'SOLO',14,False,'#f1d24a'); SW(k,'Main Cut',84,236,None,14,False,'#e04a3a'); T(k,84,252,'CUT',.14)
F(k,'Main Mix Fader',62,276,580,GF,.8,'#e04a3a'); T(k,24,592,'MIX L/R',.14)
master=dict(kind='Master Section',pages=pages_of(g,[('Tone, Meter & SEL',0,3),('Cue Mix & Talkback',4,6),('Returns & Auxes',7,9),('Control Room',10,11)],len(mcols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#e3e4e2',bg2='#cfd0ce',ink=INK,kc=KB,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Neve Genesys',strip),('Neve Genesys Master Section',master)]))
