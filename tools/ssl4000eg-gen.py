# Generator for the FACEPLATES entries 'SSL 4000 E/G' (I/O channel strip SL611G) and 'SSL 4000 E/G Master Section' (SL651G + centre section).
# Source: user's "SL4000 G Console Operator's Manual" (scanned PDF, sections 2 and 4) plus photos of 4000E/G consoles.
# E and G are nearly identical; the user asked to follow the G manual and name both "E/G".
# Usage: python3 tools/ssl4000eg-gen.py > out.txt, then replace the two lines starting with  "SSL 4000 E/G  in index.html.
import json, sys
GRY='#c9cbcc'; DGY='#4a4d52'; BLK='#1c1d20'; RED='#d8352c'; GRN='#2f8f4a'; BLU='#3d7fc4'; YEL='#e8c933'; ORG='#e8862a'; BRN='#7a2d24'; WH='#e9e7e1'
TY='#f5d020'; TG='#35d06a'; TR='#ff4433'; GAP='#0b0c0e'; INK='#eef0f2'
SMALL=[['10',1],['5',.897],['0',.788],['5',.66],['10',.542],['20',.374],['30',.264],['40',.154],['60',.055],['∞',0]]
LARGE=[['10',1],['5',.877],['0',.76],['5',.642],['10',.519],['20',.418],['30',.317],['40',.208],['50',.109],['∞',0]]

def build(cols, SW, COLH, title_sz=1.0, PR=None):
    # PR = columns per row; more columns wrap into further rows (keeps the panel near square so print sizes stay right)
    GP=10; MG=6; TOP=34; PR=PR or len(cols); NR=(len(cols)+PR-1)//PR; RH=TOP+COLH+8
    CW=PR*SW+(PR-1)*GP+2*MG; CH=NR*RH+(NR-1)*GP
    d=[]; c=[]
    cx=lambda k: MG+(k%PR)*(SW+GP)
    ry=lambda k: (k//PR)*(RH+GP)
    P=lambda k,x,y: [round((cx(k)+x)/CW,4), round((ry(k)+TOP+y)/CH,4)]
    class G: pass
    g=G()
    def T(k,x,y,t,sz=.5,col=INK): d.append(['txt',*P(k,x,y),t,sz,col])
    def K(k,name,x,y,dia,col,ks='ssl',ext=None):
        e={'ks':ks}
        if ext: e.update(ext)
        c.append(['k',name+'|',*P(k,x,y),round(dia/CW,4),col,'n',e])
    def B(k,name,x,y,cap=None,col=WH,dia=20,tab=None):
        q={'plain':True}
        if cap: q['cap']=cap
        c.append(['p',name+'|',*P(k,x,y),round(dia/CW,4),col,'n',q])
        if tab: d.append(['led',*P(k,x,y+dia*.5+6),round(5/CW,4),tab,False])
    def SC(k,x,y,rad,labs,sz=.42,a0=-135,a1=135): d.append(['scale',*P(k,x,y),round(rad/CW,4),labs,sz,INK,a0,a1])
    def DOT(k,x,y,rad,n=11,a0=-140,a1=140): d.append(['pdots',*P(k,x,y),round(rad/CW,4),n,round(2.2/CW,4),INK,a0,a1])
    def HL(k,y): x0=cx(k)/CW; yy=round((ry(k)+TOP+y)/CH,4); d.append(['poly',[[x0,yy],[x0+SW/CW,yy]],'#8a929b',2])
    def LED(k,x,y,col,dia=6): d.append(['led',*P(k,x,y),round(dia/CW,4),col,False])
    def F(k,name,x,y0,y1,marks,zero,col='#b9bcbf'):
        L=y1-y0; q={'vert':True,'zero':zero,'dbLabel':False}
        q['marks']=marks or LARGE
        if not marks: q['plain']=True
        c.append(['f',name+'|',*P(k,x,(y0+y1)/2),round(L/16.9/CW,4),col,'n',q])
    def VU(k,x,y,w,h,o): d.append(['vu',*P(k,x-w/2,y-h/2),round(w/CW,4),round(h/CH,4),o])
    def X(k,name,x,y,w,ph): c.append(['x',name+'|',*P(k,x,y),round(w/CW,4),'#f2f2f2','n',{'dar':.8,'lines':1,'ph':[ph],'max':2}])
    for r in range(NR):
        y0=round(r*(RH+GP)/CH,4); h=round(RH/CH,4); n=min(PR,len(cols)-r*PR)
        for j in range(n if n<PR else n-1): d.append(['rect',round((MG+j*(SW+GP)+SW)/CW,4),y0,round(GP/CW,4),h,GAP,GAP,0])
        if r: d.append(['rect',0,round((r*(RH+GP)-GP)/CH,4),1,round(GP/CH,4),GAP,GAP,0])
    for k,n in enumerate(cols): d.append(['txt',round((cx(k)+SW/2)/CW,4),round((ry(k)+19)/CH,4),n.upper(),title_sz,'#c9d2dc'])
    g.__dict__.update(T=T,K=K,B=B,SC=SC,DOT=DOT,HL=HL,LED=LED,F=F,VU=VU,X=X,d=d,c=c,CW=CW,CH=CH,cx=cx,ry=ry,RH=RH,GP=GP,MG=MG,SW=SW,PR=PR)
    return g

def pages_of(g, groups, ncols):
    out=[]
    for n,a,b in groups:
        rowlast=min(ncols-1,(a//g.PR+1)*g.PR-1)
        x0=g.cx(a)-(g.MG if a%g.PR==0 else g.GP/2); x1=g.cx(b)+g.SW+(g.MG if b==rowlast else g.GP/2)
        y0=max(0,g.ry(a)-g.GP/2); y1=min(g.CH,g.ry(a)+g.RH+g.GP/2)
        out.append([n,round(x0/g.CW,4),round(y0/g.CH,4),round(x1/g.CW,4),round(y1/g.CH,4)])
    return out

# ================= channel strip (SL611G I/O module) =================
cols=['Routing','Input & Dynamik','Filter & EQ','Cue & Aux','Small Fader','Large Fader']
g=build(cols,100,600,.75)
T,K,B,SC,DOT,HL,LED,F,X=g.T,g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F,g.X
# 0 group trim + routing matrix
K(0,'Group Trim',28,36,26,BLK); DOT(0,28,36,18); T(0,14,62,'-30',.34); T(0,42,62,'0dB',.34); T(0,28,74,'TRIM',.36); T(0,28,10,'pull Solo Isolate',.28)
B(0,'Float',76,26,'FLOAT',WH,20); B(0,'Direct',76,56,'DIRECT',WH,20); HL(0,88)
T(0,50,102,'SL611G',.38)
labs=[str(i) for i in range(1,33)]+['LF','RF','LB','RB']
for i,l in enumerate(labs):
    r,cc=divmod(i,4); x=16+cc*23; y=128+r*36
    LED(0,x,y-12,TR,5); B(0,'Route '+l,x,y,l,WH,16)
K(0,'Routing Pan',30,470,28,RED); DOT(0,30,470,20); T(0,30,446,'C',.36); T(0,12,498,'ODD',.32); T(0,48,498,'EVEN',.32)
B(0,'Pan',78,470,'PAN',WH,20)
# 1 channel input + dynamics
K(1,'Line Trim',28,34,24,GRY); DOT(1,28,34,17); T(1,14,58,'-20',.32); T(1,42,58,'+20',.32); T(1,12,14,'LINE',.36); T(1,40,14,'0',.32); LED(1,54,22,TG)
K(1,'Mic Gain',28,94,24,RED); DOT(1,28,94,17,12); T(1,14,118,'+4',.32); T(1,42,118,'+70',.32); T(1,12,74,'MIC',.36); LED(1,54,82,TR)
B(1,'Flip',80,24,'FLIP',WH,18); B(1,'Sub GP',80,50,'SUB GP',WH,18); B(1,'Phase',80,76,'Ø',WH,18); B(1,'+48V',80,102,'+48V',WH,18); HL(1,132)
T(1,26,144,'DYNAMICS',.4)
K(1,'Comp Ratio',26,180,24,BLK); SC(1,26,180,18,['1','2','3','5','8','20','∞'],.3); T(1,26,206,'RATIO',.32)
T(1,74,146,'pull RELEASE',.26); T(1,74,155,'for fast attack',.26); B(1,'Link',76,174,'LINK',WH,18)
K(1,'Comp Threshold',74,224,24,BLK); SC(1,74,224,18,['+10','0','-5','-10','-20'],.3); T(1,74,250,'THRESHOLD',.3)
T(1,26,222,'COMPRESS',.32)
K(1,'Comp Release',26,256,24,BLK); SC(1,26,256,18,['.1','.4','1','4'],.3); T(1,26,282,'RELEASE',.32)
K(1,'Gate Threshold',74,292,24,GRN); SC(1,74,292,18,['-30','-12','+10'],.3); T(1,74,318,'THRESHOLD',.3)
B(1,'Gate',76,342,'GATE',WH,18)
K(1,'Gate Range',26,318,24,GRN); SC(1,26,318,18,['0','20','40'],.3); T(1,26,344,'RANGE',.32)
T(1,26,358,'EXPAND',.32)
K(1,'Gate Release',26,392,24,GRN); SC(1,26,392,18,['.1','.4','1','4'],.3); T(1,26,418,'RELEASE',.32)
for i,v in enumerate(['20','14','10','6','3']):
    y=380+i*16; LED(1,62,y,TG,6); T(1,75,y+3,v,.3); LED(1,88,y,TY if i>1 else TR,6)
T(1,50,474,'DYNAMICS to',.34)
B(1,'Dyn Ch In',22,500,'CH IN',WH,18,TG); B(1,'Dyn Ch Out',50,500,'CH OUT',WH,18,TG); B(1,'Dyn Mon',78,500,'MON',WH,18,TG)
# 2 filters + EQ
T(2,14,10,'FILTERS',.34)
K(2,'LPF kHz',70,36,24,GRY,'ssl',{'sweep':[-140,140]}); SC(2,70,36,18,['OUT','12','8','5','4','3.5','3'],.28,-140,140)
K(2,'HPF Hz',28,66,24,GRY,'ssl',{'sweep':[-140,140]}); SC(2,28,66,18,['OUT','20','70','120','200','300','350'],.28,-140,140)
B(2,'Split',76,84,'SPLIT',WH,18); HL(2,104)
def GAIN(n,x,y,col,lab=None):
    K(2,n,x,y,22,col); DOT(2,x,y,16); T(2,x,y-20,'0',.3); T(2,x-14,y+20,'-',.34); T(2,x+14,y+20,'+',.34)
    if lab: T(2,x-14,y-22,lab,.3)
def FRQ(n,x,y,col,labs,unit):
    K(2,n,x,y,22,col,'ssl',{'sweep':[-140,140]}); SC(2,x,y,17,labs,.27,-140,140); T(2,x,y+24,unit,.28)
GAIN('HF dB',26,132,RED,'HF'); B(2,'x3',78,120,'x3',WH,16)
FRQ('HF kHz',72,166,RED,['1.5','2','5','8','10','14','16'],'kHz')
GAIN('HMF dB',26,206,GRN)
FRQ('HMF kHz',72,240,GRN,['.6','.8','1.5','3','4.5','6','7'],'kHz')
K(2,'HMF Q',26,270,22,GRN); SC(2,26,270,16,['3','2','1.5','1','.5'],.27); T(2,10,248,'HMF',.3)
B(2,'Insert Pre',78,288,'PRE',WH,16); B(2,'Insert In',78,312,'IN',WH,16); T(2,52,300,'INSERT',.26)
GAIN('LMF dB',26,334,BLU)
FRQ('LMF kHz',72,362,BLU,['.2','.3','.8','1','1.5','2','2.5'],'kHz')
K(2,'LMF Q',26,398,22,BLU); SC(2,26,398,16,['3','2','1.5','1','.5'],.27); T(2,10,376,'LMF',.3)
FRQ('LF Hz',72,430,BLK,['30','50','100','200','300','375','450'],'Hz')
B(2,'Div 3',78,470,'÷3',WH,16)
GAIN('LF dB',26,458,BLK,'LF')
T(2,50,494,'EQUALISER to',.32)
B(2,'EQ Ch',22,516,'CH',WH,18,TG); B(2,'EQ Flt Dyn S-C',50,516,'FLT DYN S-C',WH,18,TG); B(2,'EQ Mon',78,516,'MON',WH,18,TG)
LED(2,70,566,TR,7); T(2,40,569,'OVERLOAD',.3)
# 3 cue + aux sends
T(3,12,10,'CUES',.36)
K(3,'Cues Pan',28,38,22,BLK); DOT(3,28,38,16); T(3,28,18,'C',.3); T(3,14,58,'L',.3); T(3,42,58,'R',.3)
for i,nm in enumerate(['Stereo','Aux 1','Aux 2','Aux 3','Aux 4']):
    y=104+i*96; lab='STEREO' if i==0 else str(i)
    K(3,nm,30,y,24,DGY); DOT(3,30,y,17); T(3,16,y+22,'∞',.36); T(3,12 if i else 22,y-24,lab,.32)
    B(3,nm+' Pre',78,y-16,'PRE',WH,18); B(3,nm+' Small Fader',78,y+14,'SMALL FADER',WH,18)
# 4 monitor input + small fader
B(4,'Ready Group',28,26,'READY GROUP',WH,22); B(4,'Ready Tape',72,26,'READY TAPE',WH,22)
B(4,'Record',50,72,'RECORD',RED,28); T(4,50,102,'from CHANNEL',.28)
B(4,'Small Input',76,124,'INPUT',WH,18); B(4,'Small Output',76,150,'OUTPUT',WH,18); LED(4,56,137,TG,5)
F(4,'Small Fader',30,130,400,SMALL,.788)
LED(4,56,212,TY,5); B(4,'Small Solo',76,212,'SOLO',WH,18); LED(4,56,240,TR,5); B(4,'Small Cut',76,240,'CUT',RED,18)
K(4,'F/B Pan',74,290,22,BLK); DOT(4,74,290,16); T(4,74,270,'C',.3); T(4,92,282,'F',.3); T(4,92,302,'B',.3)
B(4,'F/B Pan In',74,328,'IN',WH,18)
K(4,'Quad Pan',72,386,26,RED); DOT(4,72,386,18); T(4,72,364,'C',.3); T(4,58,412,'L',.3); T(4,86,412,'R',.3)
LED(4,30,430,TG,6); T(4,30,444,'to ROUTING',.28)
# 5 large fader
B(5,'Large Solo',28,30,'SOLO',WH,26); B(5,'Large Cut',72,30,'CUT',RED,26)
d=g.d; d.append(['rect',*[round((g.cx(5)+8)/g.CW,4),round((34+62)/g.CH,4)],round(84/g.CW,4),round(54/g.CH,4),'#e6e2d6','#9a9a9a',2]); T(5,50,92,'SCRIBBLE STRIP',.3,'#555')
X(5,'VCA Group',22,150,18,'0'); T(5,22,172,'VCA',.3)
LED(5,18,196,TY,6); T(5,34,199,'trim',.28); LED(5,18,212,TG,6); T(5,34,215,'abs',.28)
c=g.c; c.append(['s','Status|',*[round((g.cx(5)+22)/g.CW,4),round((34+262)/g.CH,4)],round(16/g.CW,4),'','n']); T(5,22,236,'status',.28)
F(5,'Large Fader',66,150,570,LARGE,.76)
T(5,18,580,'SSL',.5)
pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols))
strip=dict(kind='Channel Strip',pages=pages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#3a3d42',bg2='#26282c',ink=INK,kc=GRY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

# ================= master section (SL651G + centre section) =================
mcols=['Status & Osc','Talkback & Komm.','Cue-Aux Sends','Local Aux Sends','Echo Return 1','Echo Return 2','Echo Return 3','Echo Return 4','Externe Quellen','Quad Compressor','Control Room','Stereo VCA 1-2','Stereo VCA 3-4','VCA 1-2','VCA 3-4','VCA 5-6','VCA 7-8']
g=build(mcols,110,660,.5,9)
T,K,B,SC,DOT,HL,LED,F,VU=g.T,g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F,g.VU
k=0
for i,v in enumerate(['48V','+18V','+11V','-18V']): LED(k,17+i*25,22,TG,6); T(k,17+i*25,10,v,.28)
HL(k,38); T(k,55,50,'OSCILLATOR',.34)
B(k,'Osc Groups',22,74,'GROUPS',WH,20); B(k,'Osc Quad Bus',55,74,'QUAD BUS',WH,20); B(k,'Osc On',88,74,'ON',WH,20)
K(k,'Osc Frequency',28,130,24,BLK,'chicken',{'sweep':[15,265]}); SC(k,28,130,19,['50','100','220','440','1K','3K','10K','15K'],.28,15,265)
K(k,'Osc Level',80,130,24,GRY); SC(k,80,130,18,['-10','-5','0','5','10','+20'],.28,-110,135)
K(k,'Osc Cal',62,162,8,'#b08a3c','trim'); T(k,78,166,'cal.',.28); HL(k,180)
for i,(nm,cap) in enumerate([('Master Ch Input Flip','MASTER CH INPUT FLIP'),('VCAs to Monitor',"VCA'S TO MONITOR"),('Mix to Cues','MIX TO CUES'),('Auto Cue','AUTO CUE'),('Record','RECORD'),('Replay','REPLAY'),('Mix','MIX'),('Status Lock','STATUS LOCK')]):
    B(k,nm,16+(i%4)*26,206+(i//4)*30,cap,RED if nm=='Status Lock' else WH,22)
T(k,55,262,'STATUS',.34); HL(k,274)
K(k,'VCA Trim dB',20,310,22,GRY); SC(k,20,310,16,['-15','0','+15'],.26); T(k,20,334,'dB',.28)
K(k,'Auto Fade Rate',55,310,22,GRY); SC(k,55,310,16,['1','3','5','10','20','40','60'],.24); T(k,55,334,'RATE-S',.26)
K(k,'AFL Level',90,310,22,GRY); DOT(k,90,310,15); T(k,90,334,'LEVEL',.26)
B(k,'VCA Trim',20,358,'VCA TRIM',WH,22); B(k,'Auto Fade',55,358,'AUTO FADE',WH,22); B(k,'AFL',90,358,'AFL',WH,22); HL(k,384)
T(k,55,398,'METERS',.34)
B(k,'Desk Output',22,420,'DESK OUTPUT',WH,22); B(k,'Follow Monitor',55,420,'FOLLOW MONITOR',WH,22); B(k,'External Source',88,420,'EXTERNAL SOURCE',WH,22); HL(k,446)
T(k,55,460,'PLASMA',.34)
for i,cap in enumerate(['STORE PEAK','DISPLAY PEAK','CLEAR PEAK','SPECTRA','SPECTRA ON SOLO','+10dB ON SPECTRA','VU','PPM','VCAs']):
    B(k,cap.title().replace('Db','dB'),22+(i%3)*33,484+(i//3)*30,cap,WH,22)
k=1
for i,(nm,lab) in enumerate([('TB to Cans','TB to cans'),('TB to Studio','TB to studio'),('Slate Level','slate level'),('Listen 1','listen 1'),('Listen 2','listen 2')]):
    x=28 if i%2==0 else 82; y=36+(i//2)*62
    K(k,nm,x,y,24,GRY); DOT(k,x,y,17); T(k,x-14,y+22,'∞',.32); T(k,x+14,y+22,'0',.3); T(k,x,y+34,lab,.3)
T(k,82,174,'pull = off',.26); HL(k,198)
T(k,55,212,'COMMUNICATIONS',.32)
for i,(nm,cap,col) in enumerate([('Listen Mic to Tape','LISTEN MIC TO TAPE',WH),('Listen Mic','LISTEN MIC',WH),('Red Light','RED LIGHT',RED),('Omni','OMNI',WH),('TB Cues','CUES',WH),('M.D.','M.D.',WH),('TB Cue Stereo','CUE STEREO',WH),('TB Cue 1','CUE 1',WH),('TB Cue 2','CUE 2',WH)]):
    B(k,nm,22+(i%3)*33,238+(i//3)*32,cap,col,24)
k=2
for i,nm in enumerate(['Cue Stereo','Aux 1','Aux 2','Aux 3','Aux 4']):
    y=40+i*118
    for j,(part,col) in enumerate([('HF',GRY),('LF',GRY),('Level',DGY)]):
        x=20+j*35; K(k,f'{nm} {part}',x,y+(0 if j<2 else 40),20,col); DOT(k,x,y+(0 if j<2 else 40),14)
        if j<2: T(k,x-11,y+18,'-15',.24); T(k,x+11,y+18,'+15',.24); T(k,x,y-18,'0',.26); T(k,x,y+28,part,.28)
        else: T(k,x-10,y+58,'∞',.3); T(k,x+10,y+58,'0',.26)
    T(k,34,y+50,nm.upper(),.3)
T(k,90,22,'±15dB',.24); T(k,90,32,'HF 10k',.24); T(k,90,42,'LF 100',.24)
k=3
for i,nm in enumerate(['Stereo','Aux 1','Aux 2','Aux 3','Aux 4']):
    y=34+i*124
    for j,part in enumerate(['HF','LF']):
        x=22+j*36; K(k,f'Local {nm} {part}',x,y,20,GRY); DOT(k,x,y,14); T(k,x,y-18,'0',.26); T(k,x-11,y+18,'-15',.24); T(k,x+11,y+18,'+15',.24); T(k,x,y+28,part,.28)
    x=90; K(k,f'Local {nm}',x,y+8,20,DGY); DOT(k,x,y+8,14); T(k,x-10,y+26,'∞',.3); T(k,x+10,y+26,'0',.26); T(k,x,y+38,nm.upper(),.28)
    B(k,f'Local {nm} AFL',30,y+62,'AFL',WH,18,TY); B(k,f'Local {nm} Split',62,y+62,'↓',WH,18,TG)
for k in range(4,8):
    n=k-3
    def KB(nm,y,col,lo,hi,mid=None):
        K(k,nm,30,y,24,col); DOT(k,30,y,17); T(k,16,y+22,lo,.28); T(k,44,y+22,hi,.28)
        if mid: T(k,30,y-22,mid,.28)
    KB(f'Return {n} Spin',40,GRY,'off','0'); T(k,30,76,'spin',.28); B(k,f'Return {n} In',80,30,'IN',WH,20)
    KB(f'Return {n} Cans',140,GRY,'∞','0'); T(k,30,176,'cans',.28)
    cues=[('CUE 1','Cue 1'),('CUE 2','Cue 2'),('CUE ST','Cue St')]
    for j,(cap,nm) in enumerate(cues):
        if (n==1 and j==0) or (n==2 and j==1): B(k,f'Return {n} Blank {j+1}',80,96+j*28,None,WH,20)
        else: B(k,f'Return {n} {nm}',80,96+j*28,cap,WH,20)
    KB(f'Return {n} Width',260,BLK,'S','M','C'); T(k,30,296,'width',.28)
    B(k,f'Return {n} F/B Pan',80,248,'F/B PAN',WH,20); B(k,f'Return {n} L/R Pan',80,278,'L/R PAN',WH,20)
    KB(f'Return {n} Balance',370,RED,'L','R','C'); T(k,30,406,'balance',.28)
    B(k,f'Return {n} L Cut',80,358,'L CUT',RED,20); B(k,f'Return {n} R Cut',80,388,'R CUT',RED,20)
    KB(f'Return {n} Level',480,DGY,'∞','0'); B(k,f'Return {n} AFL',80,470,'AFL',WH,20,TY)
    T(k,55,560,f'RETURN {n}',.4)
k=8
srcL=['CUE STEREO','CUE 1','CUE 2','CUE 3','CUE 4','STEREO 1','STEREO 2','STEREO 3','STEREO 4','STEREO 5','QUAD DISC','QUAD TAPE 1','QUAD BUS']
srcR=srcL[:12]+['QUAD TAPE 2']
for i in range(13):
    B(k,'Ext Studio '+srcL[i].title(),30,22+i*31,srcL[i],WH,22); B(k,'Ext Monitors '+srcR[i].title(),80,22+i*31,srcR[i],WH,22)
B(k,'External to Studio',30,432,'EXTERNAL TO STUDIO',WH,24); B(k,'External to Monitors',80,432,'EXTERNAL TO MONITORS',WH,24); HL(k,462)
T(k,55,476,'STUDIO',.34)
for x,nm in ((26,'Cues'),(84,'SLS')):
    K(k,'Studio '+nm,x,516,24,GRY,'ssl',{'sweep':[-140,140]}); SC(k,x,516,18,[str(v) for v in range(11)],.24,-140,140); T(k,x,546,nm.upper(),.3)
LED(k,55,516,'#9aa0a6',9); T(k,55,532,'TB MIC',.24)
k=9
VU(k,55,70,96,70,{'label':'dB','gr':True}); HL(k,122)
K(k,'Quad Threshold',28,160,26,GRY); SC(k,28,160,19,['-15','0','+15'],.28); T(k,28,190,'THRESHOLD',.28)
K(k,'Quad Make-Up',82,160,26,GRY); SC(k,82,160,19,['0','7.5','+15'],.28); T(k,82,190,'MAKE-UP',.28)
K(k,'Quad Attack',28,240,26,GRY,'ssl',{'sweep':[-120,120]}); SC(k,28,240,19,['.1','.3','1','3','10','30'],.27,-120,120); T(k,28,270,'ATTACK-ms',.27)
K(k,'Quad Release',82,240,26,GRY,'ssl',{'sweep':[-120,120]}); SC(k,82,240,21,['.1','.3','.6','1.2','Auto'],.25,-120,120); T(k,82,270,'RELEASE-S',.27)
K(k,'Quad Ratio',28,322,26,GRY,'ssl',{'sweep':[-60,60]}); SC(k,28,322,19,['2','4','10'],.28,-60,60); T(k,28,352,'RATIO',.28)
B(k,'Quad Comp In',82,322,'IN',WH,26); T(k,55,380,'QUAD COMPRESSOR',.32)
k=10
K(k,'Monitor',55,84,34,BLK,'ssl',{'sweep':[-140,140]}); SC(k,55,84,25,[str(v) for v in range(11)],.27,-140,140); T(k,55,118,'MONITOR',.3)
K(k,'Mini LS',16,40,18,GRY); DOT(k,16,40,13); T(k,16,60,'MINI LS',.24)
K(k,'Dim Level',94,40,18,GRY); DOT(k,94,40,13); T(k,94,60,'DIM level',.24)
for i,nm in enumerate(['Mono','Stereo','Quad']): B(k,nm,80,146+i*28,nm.upper(),WH,22)
T(k,80,226,'MONITOR MATRIX',.24)
for i,nm in enumerate(['Alt','Mini','Dim','Cut']): B(k,'Monitors '+nm,80,252+i*28,nm.upper(),RED if nm=='Cut' else WH,22)
T(k,80,362,'MONITORS',.26)
F(k,'Main Fader',24,140,370,None,.76)
HL(k,382); T(k,55,396,'MONITOR CUTS & TRIMS',.26)
for i,nm in enumerate(['LB','LF','RF','RB']):
    x=16+i*26; K(k,nm+' Trim',x,418,8,'#b08a3c','trim'); B(k,nm+' Cut',x,450,nm,WH,22)
T(k,16,432,'-3',.22); T(k,94,432,'+3',.22)
def FADERS(k,pref,n0,btns):
    for i in range(2):
        x=30+i*50; n=n0+i; nm=f'{pref} {n}'
        T(k,x,14,str(n),.4)
        g.X(k,nm+' Group',x,42,16,'0'); T(k,x-20,30,'VCA',.24)
        LED(k,x-8,68,TY,5); LED(k,x+8,68,TG,5)
        F(k,nm+' Fader',x,92,520,LARGE,.76)
        for j,(b,col) in enumerate(btns): B(k,f'{nm} {b.title()}',x,550+j*30,b,col,20)
FADERS(11,'Stereo VCA',1,[('AFL',WH),('CUT',RED)]); FADERS(12,'Stereo VCA',3,[('AFL',WH),('CUT',RED)])
for j in range(4): FADERS(13+j,'VCA',1+2*j,[('SOLO',WH),('CUT',RED)])
mpages=pages_of(g,[('Status & Talkback',0,1),('Aux Sends',2,3),('Echo Returns',4,7),('Monitor & Quad Comp',8,10),('Stereo VCAs',11,12),('VCA-Gruppen',13,16)],len(mcols))
master=dict(kind='Master Section',pages=mpages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#3a3d42',bg2='#26282c',ink=INK,kc=GRY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('SSL 4000 E/G',strip),('SSL 4000 E/G Master Section',master)]))
