# Generator for 'SSL ORIGIN' (channel strip) and 'SSL ORIGIN Master Section'.
# Source: official SSL ORIGIN User Guide V2.0 (solidstatelogic.com), Appendix E recall sheets (channel p.47, master p.48)
# and the channel strip overview photo (p.5, knob colours). Helpers come from tools/ssl4000eg-gen.py.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
RED='#d23a32'; GRN='#2e8a4a'; BLU='#2f6fc4'; BLK='#1b1c1f'; WHT='#e9e9e6'; GY='#8f9398'
SFM=[['10',1],['5',.775],['0',.683],['5',.5],['10',.385],['20',.243],['30',.106],['∞',0]]
LFM=[['10',1],['0',.832],['10',.676],['15',.545],['20',.401],['30',.242],['40',.121],['50',.07],['∞',0]]
MXM=[['0',1],['5',.86],['10',.751],['15',.658],['20',.52],['30',.327],['40',.17],['50',.09],['∞',0]]
def kit(g):
    T=g.T; K=g.K; B=g.B; SC=g.SC; DOT=g.DOT; HL=g.HL; LED=g.LED; F=g.F
    def KN(k,name,x,y,dia,col,lo=None,hi=None,mid=None,unit=None,lab=None):
        K(k,name,x,y,dia,col); DOT(k,x,y,dia*.7)
        if lo: T(k,x-dia*.55,y+dia*.5+6,lo,.24)
        if hi: T(k,x+dia*.55,y+dia*.5+6,hi,.24)
        if mid: T(k,x,y-dia*.5-6,mid,.24)
        if unit: T(k,x,y+dia*.5+10,unit,.2)
        if lab: T(k,x,y+dia*.5+18,lab,.24)
    def BAR(k,x,y,t,w=None): w=w or len(t)*4.6+8; g.d.append(['rect',round((g.cx(k)+x-w/2)/g.CW,4),round((g.ry(k)+34+y-6)/g.CH,4),round(w/g.CW,4),round(12/g.CH,4),'#f0f0ee','none',1]); T(k,x,y+3,t,.26,'#1b1c1f')
    def LB(k,name,x,y,cap=None,dia=16,led=True,col=WH): B(k,name,x,y,cap,col,dia); 
    return T,K,B,SC,DOT,HL,LED,F,KN,BAR

# ================= channel strip (recall sheet columns) =================
cols=['Input & Sends','Filter & EQ','Routing & SF','Large Fader']
g=build(cols,110,640,.6)
T,K,B,SC,DOT,HL,LED,F,KN,BAR=kit(g)
k=0
KN(k,'Gain',30,42,30,RED,'+2','+70',None,'dB'); T(k,14,16,'GAIN',.3)
LED(k,74,14,'#ff4433',6); B(k,'48V',92,14,None,WH,14); T(k,92,28,'48V',.22)
B(k,'Phase',92,46,'Ø',WH,14)
B(k,'Drive',22,90,'DRIVE',WH,16); BAR(k,90,76,'CHAN')
B(k,'Line',22,116,'LINE',WH,16); LED(k,62,104,'#ff4433',5); T(k,74,107,'SF',.2); LED(k,62,118,'#35d06a',5); T(k,74,121,'LF',.2)
HL(k,130)
B(k,'Chan Path Flip',92,142,'PATH FLIP',WH,16)
KN(k,'Trim',30,168,26,WHT,'-20','+20','0','dB'); T(k,14,148,'TRIM',.28); BAR(k,90,170,'MON')
HL(k,196); BAR(k,30,204,'DIRECT OUT'); B(k,'Direct Pre',92,206,'PRE',WH,14)
B(k,'Direct Path Flip',30,226,'PATH FLIP',WH,14); LED(k,62,220,'#ff4433',5); LED(k,62,232,'#35d06a',5)
HL(k,244)
for i,(lab,y0) in enumerate([('ST CUE A',258),('ST CUE B',348)]):
    BAR(k,26,y0,lab); KN(k,f'Cue {"AB"[i]} Pan',78,y0+10,22,BLU,'L','R',None,None); T(k,62,y0-4,'PAN',.22)
    KN(k,f'Cue {"AB"[i]} Level',30,y0+52,24,GRN,'∞',None); B(k,f'Cue {"AB"[i]} Post',92,y0+44,'POST',WH,14); B(k,f'Cue {"AB"[i]} SF',92,y0+68,'SF',WH,14)
    HL(k,y0+84)
for i in range(4):
    y0=446+i*48; n=i+1
    BAR(k,62,y0,f'AUX{n}',34); KN(k,f'Aux {n}',30,y0+20,22,GRN,'∞',None)
    B(k,f'Aux {n} Pre',92,y0+8,'PRE',WH,14); B(k,f'Aux {n} SF',92,y0+30,'SF',WH,14)
k=1
B(k,'HPF In',18,20,'IN',WH,14); KN(k,'HPF',72,26,26,WHT,'10','400',None,'Hz')
B(k,'HPF Path Flip',18,52,'PATH FLIP',WH,14); LED(k,40,48,'#ff4433',5); LED(k,40,60,'#35d06a',5); BAR(k,94,70,'HPF',22)
HL(k,82)
def BAND(k,y0,nm,col,lo,hi,frq=None,q=False,bell=False):
    KN(k,f'{nm} dB',28,y0,24,col,'-','+','0','dB'); T(k,14,y0+34,nm,.36)
    KN(k,f'{nm} Freq',78,y0+30,22,col,lo,hi,None,'kHz' if nm in('HF','HMF','LMF') else 'Hz')
    if bell: B(k,f'{nm} Bell',92,y0-2,'BELL',WH,14)
    if q: KN(k,f'{nm} Q',28,y0+66,22,col,None,None,None,None,'Q')
BAND(k,104,'HF',RED,'1.5','16',bell=True)
HL(k,170); BAND(k,192,'HMF',GRN,'.6','7',q=True)
B(k,'EQ Path Flip',92,270,'PATH FLIP',WH,14); LED(k,62,266,'#ff4433',5); LED(k,62,278,'#35d06a',5); B(k,'EQ In',92,296,'IN',WH,14)
HL(k,312); BAND(k,334,'LMF',BLU,'.2','2.5',q=True)
HL(k,436); BAND(k,456,'LF',BLK,'30','450',bell=True); BAR(k,94,526,'EQ',22)
k=2
BAR(k,22,12,'BUSES'); B(k,'Follow Path Pan',92,20,None,WH,14); T(k,62,22,'FOLLOW PATH PAN',.18)
B(k,'Bus Path Flip',22,52,'PATH FLIP',WH,14); LED(k,48,46,'#ff4433',5); T(k,58,49,'SF',.2); LED(k,48,58,'#35d06a',5); T(k,58,61,'LF',.2)
LED(k,30,84,'#2f8ff0',6); T(k,30,96,'ROUTED TO BUS',.18); B(k,'Route',80,84,'ROUTE',WH,16)
g.d.append(['rect',round((g.cx(k)+6)/g.CW,4),round((34+106)/g.CH,4),round(98/g.CW,4),round(14/g.CH,4),'#111214','none',1]); T(k,55,116,'OVERLOAD',.26,'#f0f0ee'); LED(k,20,113,'#ff4433',6)
KN(k,'SF Pan',62,148,26,BLU,'L','R'); T(k,28,152,'SF PAN',.26)
F(k,'Small Fader',22,180,400,SFM,.683)
for nm,cap,y in [('SF from LF','SF FROM LF',186),('SF 0dB','0dB',216),('SF Ins In','INS IN',246),('SF Ins Pre','INS PRE',276),('SF to Mix','SF TO MIX',306),('SF Solo','SOLO',336),('SF Cut','CUT',366)]:
    B(k,nm,84,y,cap,WH,16)
BAR(k,14,410,'SF',16)
B(k,'LF Ins In',22,436,'INS IN',WH,14); B(k,'LF Ins Pre',22,466,'INS PRE',WH,14)
KN(k,'LF Pan',78,452,26,BLU,'L','R'); T(k,78,428,'LF PAN',.26)
B(k,'LF to Mix',78,498,'LF TO MIX',WH,18); BAR(k,14,520,'LF',16)
k=3
B(k,'LF Solo',32,40,'SOLO',WH,26); B(k,'LF Cut',80,40,'CUT',WH,26)
F(k,'Large Fader',40,100,600,LFM,.832)
B(k,'LF 0dB',86,200,'0dB',WH,16)
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#3b3e43',bg2='#2a2c30',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

# ================= master section (recall sheet p.48, columns as on the console) =================
mcols=['Bus Masters 1-8','Bus Masters 9-16','Stereo Returns 1-2','Stereo Returns 3-4','Talkback & Monitor Levels','Mon Source & Select',
       'Bus Compressor','Mix Bus','Oscillator & Solo','Meters & Misc','Communications','Cues & Aux Masters']
g=build(mcols,110,620,.42,6)
T,K,B,SC,DOT,HL,LED,F,KN,BAR=kit(g)
for k,b0 in ((0,1),(1,9)):
    for i in range(8):
        n=b0+i; c,r=i%2,i//2; x=30+c*52; y=40+r*140
        KN(k,f'Bus {n} Trim',x-4,y,22,GY,'-10','+10','0','dB'); B(k,f'Bus {n} Route',x+16,y+44,str(n),WH,16); LED(k,x-6,y+44,'#2f8ff0',5)
for k,r0 in ((2,1),(3,3)):
    for j in range(2):
        n=r0+j; o=j*55
        LED(k,o+14,30,'#2f8ff0',5); T(k,o+14,44,'ROUTED',.16); B(k,f'Return {n} Route',o+40,30,None,WH,12); T(k,o+40,44,'ROUTE',.16)
        K(k,f'Return {n} Input Trim',o+28,84,18,GY); DOT(k,o+28,84,12); T(k,o+14,102,'-20',.15); T(k,o+42,102,'+20',.15); T(k,o+28,66,'INPUT TRIM',.15)
        K(k,f'Return {n} F/B A',o+28,140,18,GY); DOT(k,o+28,140,12); T(k,o+28,122,'F/BACK A',.15)
        K(k,f'Return {n} F/B B',o+28,196,18,GY); DOT(k,o+28,196,12); T(k,o+28,178,'F/BACK B',.15)
        K(k,f'Return {n} Level',o+28,260,22,GY); DOT(k,o+28,260,15); T(k,o+14,282,'∞',.18); T(k,o+42,282,'0',.16); T(k,o+28,240,'LEVEL',.16)
        for i,nm in enumerate(['MIX','AFL','CUT']): B(k,f'Return {n} {nm.title()}',o+36,316+i*30,None,WH,12); LED(k,o+18,316+i*30,'#ff4433' if nm=='CUT' else '#35d06a',5); T(k,o+18,328+i*30,nm,.15)
        T(k,o+27,420,f'RETURN {n}',.2)
k=4
g.c.append(['p','Talkback Mic|',round((g.cx(k)+30)/g.CW,4),round((g.ry(k)+34+40)/g.CH,4),round(34/g.CW,4),'#2a2b2e','n',{'plain':True}]); T(k,30,66,'TALKBACK',.22)
K(k,'TB Trim',80,26,8,'#b08a3c','trim'); T(k,80,40,'TRIM',.18); B(k,'TB 48V',80,60,'48V',WH,12)
K(k,'Listen Trim',22,98,8,'#b08a3c','trim'); B(k,'Listen 48V',52,98,'48V',WH,12); T(k,86,100,'LISTEN',.2)
HL(k,120)
KN(k,'Alt Mon 1 Trim',32,150,20,GY,'-20','+20','0'); T(k,80,152,'ALT MON 1',.18)
KN(k,'Alt Mon 2 Trim',32,204,20,GY,'-20','+20','0'); T(k,80,206,'ALT MON 2',.18)
KN(k,'Dim Level',32,258,20,GY,'-30','-3'); T(k,80,260,'DIM LEVEL',.18)
B(k,'Mono',55,304,'MONO',WH,22)
B(k,'Phase L',22,344,'ØL',WH,14); B(k,'Mute L',22,374,'L',WH,14); B(k,'Mute R',88,374,'R',WH,14); T(k,55,376,'MUTE',.18)
K(k,'Monitor Level',55,436,46,BLK); DOT(k,55,436,32,13); T(k,30,470,'0',.2); T(k,80,470,'11',.2); T(k,55,480,'MONITOR LEVEL',.2)
B(k,'Dim',26,510,'DIM',WH,22); B(k,'Monitor Cut',84,510,'CUT',RED,22)
k=5
B(k,'Jack In Source',22,30,None,WH,18); T(k,62,33,'JACK IN',.2)
for i,nm in enumerate(['EXTERNAL 1','EXTERNAL 2','EXTERNAL 3','MIX']): B(k,'Source '+nm.title(),22,66+i*34,None,WH,18); T(k,66,69+i*34,nm,.2)
B(k,'Sum',22,204,None,WH,12); T(k,52,206,'SUM',.2); BAR(k,30,222,'MON SOURCE')
KN(k,'Alt 3 Phones',72,262,22,GY,'∞','0'); B(k,'Alt 3',22,262,'ALT 3',WH,18)
for i,nm in enumerate(['ALT MON 1','ALT MON 2','MAIN']): B(k,'Mon '+nm.title(),22,310+i*40,None,WH,18); T(k,66,313+i*40,nm,.2)
BAR(k,30,434,'MON SELECT')
k=6
g.d.append(['rect',round((g.cx(k)+10)/g.CW,4),round((g.ry(k)+34+10)/g.CH,4),round(90/g.CW,4),round(80/g.CH,4),'#111214','#777',2]); T(k,55,56,'GR METER',.22,'#9aa0a6')
for nm,x,y,labs,a0,a1,lab in [('Threshold',30,124,['-20','+20'],-135,135,'THRESHOLD - dB'),('Make Up',80,124,['0','+20'],-135,135,'MAKEUP - dB'),
                              ('Attack',30,196,['.1','.3','1','3','10','30'],-135,135,'ATTACK - ms'),('Release',80,196,['.1','.2','.4','.8','1.6','AUTO'],-135,135,'RELEASE - s'),
                              ('Ratio',30,268,['1.5','2','3','4','5','10'],-135,135,'RATIO'),('Sidechain HPF',80,268,['OFF','30','60','120','185','300'],-135,135,'SIDECHAIN HPF - Hz')]:
    K(k,nm,x,y,24,GY,'ssl',{'sweep':[a0,a1]}); SC(k,x,y,19,labs,.24,a0,a1); T(k,x,y+30,lab,.18)
B(k,'Insert Return',30,330,None,WH,18); T(k,30,350,'INSERT RETURN',.18); B(k,'Comp In',80,330,None,WH,20); LED(k,80,354,'#ff4433',6); T(k,80,366,'IN',.2)
BAR(k,40,390,'BUS COMPRESSOR')
k=7
B(k,'Mix Insert',24,40,None,WH,16); LED(k,24,62,'#35d06a',6); T(k,24,74,'INSERT',.2)
F(k,'Mix Fader',70,40,560,MXM,1,'#e04a3a'); BAR(k,30,590,'MIX BUS')
k=8
B(k,'Ext In',22,30,None,WH,16); T(k,52,32,'EXT IN',.18); B(k,'Osc In',22,62,'IN',WH,14); B(k,'400Hz On',22,94,'400Hz ON',WH,14); LED(k,60,78,'#35d06a',5); T(k,60,90,'ON',.16)
KN(k,'Osc Level',84,40,20,GY,'∞','+10'); T(k,84,22,'OSC LEVEL',.16)
B(k,'Osc to Mix',84,84,'TO MIX',WH,14); B(k,'Osc to Buses',84,112,'TO BUSES',WH,14); BAR(k,34,132,'OSCILLATOR')
HL(k,146)
B(k,'SF SIP',18,166,'SF SIP',WH,12); B(k,'LF SIP',18,196,'LF SIP',WH,12); B(k,'Subgrp SIP',18,226,'SUBGRP SIP',WH,12)
B(k,'Solo Link',50,166,'SOLO LINK',WH,12); B(k,'PFL',84,166,'PFL',WH,12)
LED(k,50,200,'#ffb020',6); T(k,50,212,'SOLO ACTIVE',.15); B(k,'Solo Clear',84,206,'SOLO CLEAR',WH,18)
KN(k,'In Front Balance',34,272,20,GY,'AFL','MIX'); T(k,34,252,'IN FRONT BALANCE',.15)
KN(k,'Solo Level',84,272,20,GY,'∞','0'); T(k,84,252,'SOLO LEVEL',.15)
B(k,'Red Light',55,320,'RED LIGHT',RED,18); BAR(k,34,350,'SOLO MASTER')
k=9
for i,(nm,cap) in enumerate([('Mix Meter Follow Mon','MIX METER FOLLOW MON SOURCE'),('Peak Mode Select','PEAK MODE SELECT'),('Peak Clear','PEAK CLEAR'),('Dim Chan Meters','DIM CHAN METERS'),('Dim Mon Meters','DIM MON METERS')]):
    B(k,nm,26+(i%2)*56,36+(i//2)*58,None,WH,20); T(k,26+(i%2)*56,60+(i//2)*58,cap,.13)
BAR(k,28,200,'METERS')
HL(k,216)
for i,nm in enumerate(['AUTO SLEEP','WAKE/SLEEP','SHIFT / CLEAR ROUTE']): B(k,nm.title(),24,246+i*40,None,WH,20); LED(k,46,246+i*40,'#35d06a',5); T(k,78,249+i*40,nm,.14)
BAR(k,20,370,'MISC')
k=10
for j,col in enumerate(['STUDIO','FOLDBACK A','FOLDBACK B']):
    x=24+j*32; T(k,x,14,col,.14)
    for i,src in enumerate(['EXT 1','JACK IN','CONTROL ROOM','STEREO CUE A','STEREO CUE B']):
        B(k,f'{col.title()} {src.title()}',x,32+i*26,None,WH,12)
    K(k,f'{col.title()} Level',x,182,16,GY); DOT(k,x,182,11)
    B(k,f'{col.title()} AFL',x,216,None,WH,12); LED(k,x,230,'#35d06a',4)
    B(k,f'{col.title()} Talk',x,254,None,WH,12); LED(k,x,268,'#ffb020',4)
T(k,55,290,'AFL · TALK',.16)
KN(k,'Talkback Level',30,326,20,GY,'∞','0'); T(k,30,350,'TALKBACK LEVEL',.14)
KN(k,'Listen Level',80,326,20,GY,'∞','0'); T(k,80,350,'LISTEN LEVEL',.14)
B(k,'Send Listen to Talkback',55,374,None,WH,12); T(k,55,388,'SEND LISTEN TO TALKBACK',.13)
for i,nm in enumerate(['SLATE','LISTEN','TALK ALL','SWITCHED EXT TB OUT']): B(k,nm.title(),16+i*26,418,None,WH,18); T(k,16+i*26,440,nm.split()[0],.13)
BAR(k,40,470,'COMMUNICATIONS')
k=11
for i,nm in enumerate(['STEREO CUE A','STEREO CUE B','AUX 1','AUX 2','AUX 3','AUX 4']):
    y=40+i*82; B(k,f'{nm.title()} AFL',22,y,None,WH,14); LED(k,22,y+18,'#35d06a',5)
    KN(k,f'{nm.title()} Master',68,y,24,GY,'∞','+10','0','dB'); T(k,68,y+34,nm,.17)
BAR(k,44,540,'CUES AND AUX MASTERS')
master=dict(kind='Master Section',pages=pages_of(g,[('Bus Masters & Returns',0,3),('Monitor & Talkback',4,5),('Bus Compressor & Mix',6,7),('Oscillator, Solo & Meters',8,9),('Communications & Cues',10,11)],len(mcols)),ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#3b3e43',bg2='#2a2c30',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('SSL ORIGIN',strip),('SSL ORIGIN Master Section',master)]))
