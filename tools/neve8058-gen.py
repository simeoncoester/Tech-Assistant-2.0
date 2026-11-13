# Generator for the FACEPLATES entries 'Neve 8058' (channel strip) and 'Neve 8058 Master Section'.
# Built from photos of a Neve 8058 (modules 32408 direct/routing, 31102 preamp/EQ, 32404 aux/monitor) and its centre section.
# Usage: python3 tools/neve8058-gen.py > out.txt, then replace the two lines starting with  "Neve 8058  in index.html.
import json, sys
LB='#7fc4dc'; DB='#2f5fb5'; GREY='#b9bfc4'; INK='#eef0f2'; RD='#e8322b'; GN='#2fb85a'; YE='#f0c419'; WH='#efeadf'
LEDG='#35e06a'; LEDY='#f5c518'; LEDR='#ff3b30'; GAP='#0b0c0e'; RND={'ps':'rd'}
FAD=[['10',1],['5',.872],['0',.772],['5',.69],['10',.575],['20',.4],['30',.255],['40',.14],['∞',0]]

# ---------------- channel strip: four columns side by side ----------------
SW=100; GP=10; MG=6; TOP=30; COLH=545
CW=4*SW+3*GP+2*MG; CH=TOP+COLH+10
cols=['Routing','Preamp & EQ','Aux & Monitor','Fader']
d=[]; c=[]
def cx(k): return MG+k*(SW+GP)
def P(k,x,y): return [round((cx(k)+x)/CW,4), round((TOP+y)/CH,4)]
def T(k,x,y,t,sz=.8,col=INK): d.append(['txt',*P(k,x,y),t,sz,col])
def K(k,name,x,y,dia,col,ext=None):
    e=['k',name+'|',*P(k,x,y),round(dia/CW,4),col,'n']
    if ext: e.append(ext)
    c.append(e)
def B(k,name,x,y,col,dia=20,cap=None,ext=None):
    q={}
    if cap: q['cap']=cap; q['plain']=True
    if ext: q.update(ext)
    e=['p',name+'|',*P(k,x,y),round(dia/CW,4),col,'n']
    if q: e.append(q)
    c.append(e)
def L(k,name,x,y,col,dia=8): c.append(['p',name+'|',*P(k,x,y),round(dia/CW,4),col,'n',RND])
def SC(k,x,y,rad,labs,sz=.55,col=INK,a0=-135,a1=135): d.append(['scale',*P(k,x,y),round(rad/CW,4),labs,sz,col,a0,a1])
def TK(k,x,y,rad,n,a0=-135,a1=135): d.append(['ticks',*P(k,x,y),round(rad/CW,4),n,INK,a0,a1,.18,True])
def HL(k,y): x0=cx(k)/CW; yy=round((TOP+y)/CH,4); d.append(['poly',[[x0,yy],[x0+SW/CW,yy]],'#8f98a2',2])
for k in range(3): d.append(['rect',round((cx(k)+SW)/CW,4),0,round(GP/CW,4),1,GAP,GAP,0])
for k,n in enumerate(cols): d.append(['txt',round((cx(k)+SW/2)/CW,4),round(16/CH,4),n.upper(),1.0,'#c9d2dc'])
# col 0: 32408 direct / routing
for g,y0 in ((0,28),(1,166)):
    for r in range(4):
        n1=1+g*8+r*2
        B(0,f'Bus {n1}',34,y0+r*30,WH,20,str(n1)); B(0,f'Bus {n1+1}',68,y0+r*30,WH,20,str(n1+1))
L(0,'Direct LED',50,310,LEDG); d.append(['poly',[P(0,20,330),P(0,20,322),P(0,80,322),P(0,80,330)],'#cfd6dc',1.6])
B(0,'Pan',24,362,WH,22,'pan'); K(0,'Direct Level',68,362,34,LB,{'ks':'capblack'}); TK(0,68,362,24,11)
B(0,'Direct',50,425,WH,28,'direct'); T(0,50,470,'32408',.7)
# col 1: 31102 preamp & EQ (rings = frequency, inner = gain)
K(1,'Gain',50,40,36,DB,{'ks':'capblack'}); TK(1,50,40,25,13); T(1,50,76,'GAIN',.7)
for nm,y,labs,sw,rc,ic in [('HF',118,['10','12','16'],[-60,60],'#1d1f22',LB),('Mid',214,['.35','.7','1.6','3.2','4.8','7.2'],[-125,125],'#1d1f22',LB),('LF',310,['35','60','110','220'],[-90,90],'#1d1f22',LB),('Filter',404,['OFF','45','70','160','360'],[-120,120],'#1d1f22',GREY)]:
    a=sw[0]; b=sw[1]
    if nm=='Filter':
        K(1,'HPF Hz',50,y,50,rc,{'ks':'bakelite','sweep':sw}); K(1,'LPF kHz',50,y,28,ic,{'ks':'capblack','sweep':[-150,150]})
        SC(1,50,y,34,labs,.5,INK,a,b); T(1,50,y+44,'HPF · LPF',.6)
    else:
        unit='kHz' if nm!='LF' else 'Hz'
        K(1,f'{nm} {unit}',50,y,50,rc,{'ks':'bakelite','sweep':sw}); K(1,f'{nm} dB',50,y,28,ic,{'ks':'capblack'})
        SC(1,50,y,34,labs,.5,INK,a,b); T(1,50,y+44,nm.upper()+' '+unit,.6)
B(1,'EQ-Taster',80,166,WH,16)
B(1,'EQ In',32,486,WH,22,'eq'); B(1,'Phase',68,486,WH,22,'phase'); T(1,50,528,'31102',.7)
# col 2: 32404 aux & monitor
K(2,'Line Trim',50,30,26,GREY,{'ks':'capblack'}); TK(2,50,30,19,11); T(2,50,54,'LINE TRIM',.6)
L(2,'Line',20,74,LEDG); c.append(['s','Mic / Line|',*P(2,50,74),round(14/CW,4),'','n']); L(2,'Mic',80,74,LEDR)
T(2,20,88,'LINE',.5); T(2,80,88,'MIC',.5); HL(2,98)
for i,(x,y) in enumerate([(30,120),(70,120),(30,162),(70,162)]): K(2,f'Aux {i+1}',x,y,28,LB,{'ks':'capblack'}); TK(2,x,y,20,11); T(2,x,y+24,f'AUX {i+1}',.5)
B(2,'Aux 1-4 Taster A',34,205,WH,18); B(2,'Aux 1-4 Taster B',66,205,WH,18); L(2,'Aux 1-4 LED A',34,226,LEDY); L(2,'Aux 1-4 LED B',66,226,LEDR); HL(2,240)
for i,(x,y) in enumerate([(30,262),(70,262),(30,304),(70,304)]): K(2,f'Aux {i+5}',x,y,28,LB,{'ks':'capblack'}); TK(2,x,y,20,11); T(2,x,y+24,f'AUX {i+5}',.5)
for nm,x,y in [('Monitor Taster 1',30,345),('Monitor Taster 2',30,365),('Monitor Taster 3',70,345),('Monitor Taster 4',70,365)]: B(2,nm,x,y,WH,17)
L(2,'Pan LED',50,388,LEDG); T(2,50,400,'PAN',.55)
K(2,'Monitor Pan',50,425,34,LB,{'ks':'capblack'}); TK(2,50,425,24,11); T(2,16,452,'◄',.6); T(2,84,452,'►',.6)
K(2,'Mixdown Level',50,478,34,DB,{'ks':'capblack'}); TK(2,50,478,24,11)
B(2,'Mixdown Taster A',34,512,WH,16); B(2,'Mixdown Taster B',66,512,WH,16); L(2,'Mixdown LED A',34,528,LEDY,7); L(2,'Mixdown LED B',66,528,LEDR,7)
T(2,50,543,'MIXDOWN · 32404',.5)
# col 3: fader
fx=(cx(3)+38)/CW; fy=(TOP+COLH/2)/CH; fr=480/8.46/CW
c.append(['f','Fader|',round(fx,4),round(fy,4),round(fr,4),'#3aa3c9','n',{'vert':True,'marks':FAD,'zero':.772,'dbLabel':False}])
d.append(['txt',round((cx(3)+SW/2)/CW,4),round((TOP+COLH)/CH,4),'Neve',.9,'#e8322b'])
pages=[[n,round((cx(k)-(MG if k==0 else GP/2))/CW,4),0,round((cx(k)+SW+(MG if k==3 else GP/2))/CW,4),1] for k,n in enumerate(cols)]
strip=dict(kind='Channel Strip',pages=pages,ks='capblack',ps='sq',ar=round(CW/CH,4),bare=True,noTicks=True,bg='#3a4350',bg2='#2b323c',ink=INK,kc=LB,fs=17,brand='',model='',tx=.5,ty=.03,deco=d,c=c)

# ---------------- master section ----------------
MW=1000; S7=.99; OY=505; MH=OY+round(765*S7)+6
d=[]; c=[]
def X(px): return round(px/MW,4)
def Y(py): return round(py/MH,4)
def T(x,y,t,sz=.8,col=INK): d.append(['txt',X(x),Y(y),t,sz,col])
def K(name,x,y,dia,col,ext=None):
    e=['k',name+'|',X(x),Y(y),round(dia/MW,4),col,'n']
    if ext: e.append(ext)
    c.append(e)
def B(name,x,y,col,dia=24,cap=None):
    e=['p',name+'|',X(x),Y(y),round(dia/MW,4),col,'n']
    if cap: e.append({'cap':cap,'plain':True})
    c.append(e)
def L(name,x,y,col,dia=9): c.append(['p',name+'|',X(x),Y(y),round(dia/MW,4),col,'n',RND])
def TK(x,y,rad,n=11): d.append(['ticks',X(x),Y(y),round(rad/MW,4),n,INK,-135,135,.18,True])
def SC(x,y,rad,labs,sz=.5,a0=-135,a1=135): d.append(['scale',X(x),Y(y),round(rad/MW,4),labs,sz,INK,a0,a1])
def BOX(x0,y0,x1,y1): d.append(['rect',X(x0),Y(y0),round((x1-x0)/MW,4),round((y1-y0)/MH,4),'none','#8f98a2',4])
def Z(px,py): return ((px-12)*S7, OY+(py-30)*S7)     # photo (main panel) pixels -> panel units
# meters
for lab,x,y in [('LF',115,70),('RF',300,70),('AUX',580,70),('LR',115,190),('RR',300,190)]:
    d.append(['vu',X(x-80),Y(y-48),round(160/MW,4),round(90/MH,4),{'label':'VU'}]); T(x,y+56,lab,.8)
d.append(['vu',X(500),Y(142),round(160/MW,4),round(90/MH,4),{'label':'PHASE'}]); T(580,246,'PHASE',.8)
d.append(['led',X(440),Y(60),round(12/MW,4),'#f2b230',False]); T(440,84,'SOLO',.7)
d.append(['vmeter',X(760),Y(30),round(70/MW,4),round(200/MH,4),{'left':['5','4','3','2','1','min'],'right':[],'face':'#f4f1e8'}]); T(795,248,'SEK.',.6)
T(900,140,'Neve',2.2,'#f1f1ee'); T(900,180,'8058',1.6,'#c9d2dc')
d.append(['poly',[[0,Y(268)],[1,Y(268)]],'#8f98a2',3])
# aux output switch bank
T(210,290,'AUX OUTPUT',.7)
for col in range(8):
    for r in range(3): B(f'Aux Output {col+1} · {r+1}',40+col*48,320+r*44,WH,24)
    T(40+col*48,455,str(col+1),.7)
BOX(14,276,410,470)
# phase meter
for i,lab in enumerate(['LF','RF','2','RR']): B('Phase Meter A '+lab,450,315+i*36,WH,22,lab)
for i,lab in enumerate(['LF','RF','LR','4']): B('Phase Meter B '+lab,500,315+i*36,WH,22,lab)
T(475,462,'PHASE METER',.55); BOX(425,276,525,470)
# oscillator
K('Osc Frequency',600,320,40,LB,{'ks':'chicken','sweep':[-135,135]}); SC(600,320,32,['OFF','40Hz','400Hz','1kHz','10kHz','15kHz','OFF'],.4)
K('Osc Level',600,395,34,LB,{'ks':'capblack'}); SC(600,395,26,['0','1','2','3','4','5','6','7','8','9','10'],.4)
c.append(['d','Osc Output|',X(600),Y(440),round(18/MW,4),'','n']); T(565,440,'4T',.5); T(636,440,'16T',.5)
T(600,462,'OSCILLATOR',.55); BOX(540,276,660,470)
# reverb returns to 4T
for i,x in enumerate((740,840)):
    K(f'Rev Return {i+1} to 4T',x,380,36,DB,{'ks':'capblack'}); TK(x,380,26); T(x,330,f'REV RETURN {i+1}',.5); T(x,345,'TO 4T',.5)
BOX(675,276,990,470); d.append(['poly',[[0,Y(500)],[1,Y(500)]],'#8f98a2',3])
# main panel (positions measured on the centre-section photo)
def KZ(name,px,py,dia,col,labs=None,lab=None):
    x,y=Z(px,py); K(name,x,y,dia,col,{'ks':'capblack'})
    if labs: SC(x,y,dia*.78,labs,.38)
    else: TK(x,y,dia*.72)
    if lab: T(x,y+dia*.95,lab,.5)
def BZ(name,px,py,col,dia=26,cap=None): x,y=Z(px,py); B(name,x,y,col,dia,cap)
def TZ(px,py,t,sz=.6): x,y=Z(px,py); T(x,y,t,sz)
ZEHN=['0','1','2','3','4','5','6','7','8','9','10']
for i,px in enumerate([207,298,391,485,580,675,768,864]): KZ(f'Aux Out {i+1}',px,75,34,LB,ZEHN,str(i+1))
TZ(538,126,'AUX OUTPUTS',.6)
for i,px in enumerate([193,285,383,480,577,673,770,868]): KZ(f'Group Out {i+1}',px,170,34,LB,ZEHN,str(i+1))
for i,px in enumerate([178,275,373,472,573,672,773,872]): KZ(f'Group Out {i+9}',px,258,34,LB,ZEHN,str(i+9))
TZ(538,310,'GROUP OUTPUTS',.6)
for lab,px in [('LF',165),('RF',262),('LR',363),('RR',465)]: KZ(f'4T Out {lab}',px,365,34,LB,ZEHN,lab)
TZ(320,425,'4T OUTPUTS',.6)
BZ('Solo Safe 24T',572,372,YE,30,'24t'); x,y=Z(625,372); L('Solo',x,y,LEDY); TZ(625,392,'solo',.45); BZ('Solo Safe 4T',675,372,YE,30,'4t'); TZ(623,413,'SOLO SAFE',.6)
BZ('Cue Rot',775,372,RD,30); BZ('Cue Grün',878,372,GN,30); TZ(826,413,'CUE',.6)
x,y=Z(140,495); K('Studio Loudspeaker',x,y,80,'#1b1d20',{'ks':'skirt'}); SC(x,y,52,ZEHN,.38)
BZ('Studio LS On',254,505,GN,30,'on'); TZ(170,572,'STUDIO LOUDSPEAKER',.46)
BZ('Input Mic',356,508,RD,30,'mic'); BZ('Input Line',405,508,GN,30,'line'); TZ(380,550,'channel input selector',.42)
BZ('4T Mixdown Tape In',505,508,RD,30,'tape in'); BZ('4T Mixdown Tape Out',553,508,GN,30,'tape out'); TZ(529,550,'4t mixdown',.42)
for i,(top,bot,col) in enumerate([('16t','16t',WH),('4t','4t',RD),('aux 3/4','aux 1/2',WH),('aux 7/8','aux 5/6',WH),('slate','mon',WH)]):
    px=630+i*53; BZ(f'Talkback {bot}',px,515,col,24); TZ(px,487,top,.42); TZ(px,545,bot,.42)
KZ('Talkback Level',925,505,36,LB,ZEHN); TZ(760,575,'TALKBACK',.6)
x,y=Z(110,665); K('Monitor Level',x,y,80,'#1b1d20',{'ks':'skirt'}); SC(x,y,52,ZEHN,.38)
BZ('Monitor Cut',235,668,RD,30,'cut')
x,y=Z(318,673); c.append(['s','Tape In / Tape Out|',X(x),Y(y),round(18/MW,4),'','n']); TZ(318,645,'tape in',.42); TZ(318,705,'tape out',.42)
for i in range(4):
    BZ(f'Monitor Aux {i+1}',392+i*43.6,642,WH,22,f'aux {i+1}'); BZ(f'Monitor Aux {i+5}',392+i*43.6,700,WH,22,f'aux {i+5}')
for i in range(2):
    for py in (642,700): x,y=Z(566+i*43.6,py); d.append(['rect',X(x-11),Y(y-11),round(22/MW,4),round(22/MH,4),'#dcd6c8','#9a948a',2])
TZ(345,620,'aux',.45)
BZ('Monitor Mode Stereo / Mono',668,673,WH,26); TZ(668,645,'stereo',.42); TZ(668,705,'mono',.42); TZ(668,738,'monitor mode',.42)
TZ(350,775,'MONITOR',.6)
BZ('Meter 24T Tape In',738,672,RD,30,'24t tape in'); BZ('Meter 24T Tape Out',786,672,GN,30,'24t tape out'); TZ(762,712,'24 track',.42)
BZ('Meter 4T Tape In',880,672,RD,30,'tape in'); BZ('Meter 4T Tape Out',930,672,GN,30,'tape out'); TZ(905,712,'4 track',.42)
TZ(860,775,'METERS',.6)
for box in [(130,40,960,135),(90,135,975,320),(75,322,525,432),(525,322,725,432),(725,322,980,432),(40,435,300,590),(305,435,598,590),(598,435,1000,590),(15,592,700,790),(705,592,1010,790)]:
    x0,y0=Z(box[0],box[1]); x1,y1=Z(box[2],box[3]); BOX(x0,y0,x1,y1)
mpages=[['Meter & Oszillator',0,0,1,Y(500)],['Aux & Group Outputs',0,Y(490),1,Y(Z(0,440)[1])],['Monitor & Talkback',0,Y(Z(0,428)[1]),1,1]]
master=dict(kind='Master Section',pages=mpages,ks='capblack',ps='sq',ar=round(MW/MH,4),bare=True,noTicks=True,bg='#3a4350',bg2='#2b323c',ink=INK,kc=LB,fs=17,brand='',model='',tx=.5,ty=.03,deco=d,c=c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Neve 8058',strip),('Neve 8058 Master Section',master)]))
