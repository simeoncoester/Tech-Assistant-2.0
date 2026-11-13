# Generator for the FACEPLATES entries 'Neve VR' (channel strip) and 'Neve VR Master Section'.
# Source: user's French course notes "Neve VR" (panel pictures and section descriptions, pages 3-20).
# Usage: python3 tools/nevevr-gen.py > out.txt, then replace the two lines starting with  "Neve VR  in index.html.
import json, sys
GRY='#c9cbcc'; DGY='#5a5d61'; ORG='#f29a2a'; BLU='#2e8bd0'; DBL='#2b3aa8'; YEL='#f2d23a'; RED='#e5402e'; TEAL='#1f9c84'; WH='#eeeae2'
TY='#f5d020'; TG='#35d06a'; TR='#ff4433'; TB='#3aa0e8'; GAP='#0b0c0e'; INK='#eef0f2'
FAD=[['10',1],['5',.87],['0',.77],['5',.69],['10',.575],['20',.4],['30',.255],['40',.14],['∞',0]]

def build(cols, SW, COLH, fs, title_sz=1.0):
    GP=10; MG=6; TOP=34
    CW=len(cols)*SW+(len(cols)-1)*GP+2*MG; CH=TOP+COLH+8
    d=[]; c=[]
    cx=lambda k: MG+k*(SW+GP)
    P=lambda k,x,y: [round((cx(k)+x)/CW,4), round((TOP+y)/CH,4)]
    class G: pass
    g=G()
    def T(k,x,y,t,sz=.5,col=INK): d.append(['txt',*P(k,x,y),t,sz,col])
    def K(k,name,x,y,dia,col,ks='capblack',ext=None):
        e={'ks':ks}
        if ext: e.update(ext)
        c.append(['k',name+'|',*P(k,x,y),round(dia/CW,4),col,'n',e])
    def B(k,name,x,y,cap=None,col=WH,dia=20,tab=None):
        q={'plain':True}
        if cap: q['cap']=cap
        c.append(['p',name+'|',*P(k,x,y),round(dia/CW,4),col,'n',q])
        if tab: d.append(['led',*P(k,x+dia*.5+5,y),round(5/CW,4),tab,False])
    def SC(k,x,y,rad,labs,sz=.42,a0=-135,a1=135): d.append(['scale',*P(k,x,y),round(rad/CW,4),labs,sz,INK,a0,a1])
    def TK(k,x,y,rad,n=11,a0=-135,a1=135): d.append(['ticks',*P(k,x,y),round(rad/CW,4),n,INK,a0,a1,.18,True])
    def HL(k,y): x0=cx(k)/CW; yy=round((TOP+y)/CH,4); d.append(['poly',[[x0,yy],[x0+SW/CW,yy]],'#7f8892',2])
    def LED(k,x,y,col,dia=6): d.append(['led',*P(k,x,y),round(dia/CW,4),col,False])
    def F(k,name,x,y0,y1,marks,zero):
        L=y1-y0; c.append(['f',name+'|',*P(k,x,(y0+y1)/2),round(L/16.9/CW,4),'#2a2d31','n',{'vert':True,'marks':marks,'zero':zero,'dbLabel':False}])
    def VU(k,x,y,w,h,lab): d.append(['vu',*P(k,x-w/2,y-h/2),round(w/CW,4),round(h/CH,4),{'label':lab}])
    def LEDS(k,x0,y0,x1,y1,n,col): d.append(['leds',*P(k,x0,y0),*P(k,x1,y1),n,round(5/CW,4),col,0,col])
    for k in range(len(cols)-1): d.append(['rect',round((cx(k)+SW)/CW,4),0,round(GP/CW,4),1,GAP,GAP,0])
    for k,n in enumerate(cols): d.append(['txt',round((cx(k)+SW/2)/CW,4),round(19/CH,4),n.upper(),title_sz,'#c9d2dc'])
    g.__dict__.update(T=T,K=K,B=B,SC=SC,TK=TK,HL=HL,LED=LED,F=F,VU=VU,LEDS=LEDS,d=d,c=c,CW=CW,CH=CH,cx=cx,GP=GP,MG=MG)
    return g

# ================= channel strip =================
cols=['Routing','Input & Dynamik','Aux','EQ','Track & Monitor','Large Fader']
g=build(cols,100,600,16,.8)
T,K,B,SC,TK,HL,LED,F=g.T,g.K,g.B,g.SC,g.TK,g.HL,g.LED,g.F
# 0 matrix routing + upper quad bus
for r in range(12):
    a=1+2*r; b=a+1
    B(0,f'Bus {a}/{a+24}',30,26+r*25,f'{a}/{a+24}',WH,19,TY); B(0,f'Bus {b}/{b+24}',70,26+r*25,f'{b}/{b+24}',WH,19,TY)
B(0,'Layer 1-24',30,330,'1-24',RED,19,TR); B(0,'Layer 25-48',70,330,'25-48',RED,19,TR); T(0,50,350,'MTK',.45); HL(0,358)
for nm,x,y in [('QB> 1',30,378),('QB> 2',70,378),('QB> 3',30,404),('QB> 4',70,404)]: B(0,nm,x,y,nm[-1],WH,19,TG)
B(0,'B\'NCE',70,436,'B\'NCE',WH,19,TR)
K(0,'Upper Pan',32,470,30,DBL); TK(0,32,470,22); T(0,14,494,'L',.45); T(0,50,494,'R',.45)
B(0,'Pan',70,500,'PAN',WH,19,TY); T(0,50,530,'QB >',.5)
# 1 input, filter, dynamics
K(1,'Line Gain',30,40,28,GRY); SC(1,30,40,21,['-10','0','10'],.4,-120,120); T(1,30,64,'LINE',.45)
B(1,'Input C/O',74,34,'C/O',WH,20); T(1,74,52,'INPUT',.42)
B(1,'Phase',28,90,'Ø',WH,20,TR)
K(1,'Mic Gain',70,94,32,RED,'capblack',{'sweep':[40,320]}); SC(1,70,94,23,['20','30','40','50','70'],.4,40,320); T(1,92,118,'MIC',.42)
B(1,'GRP',28,124,'GRP',RED,20)
B(1,'Pad -30',70,140,'-30',RED,20); T(1,26,146,'pull ph OFF',.32)
HL(1,160)
K(1,'LPF kHz',30,192,28,TEAL); SC(1,30,192,21,['7.5','8','9','10','13','18'],.36); T(1,30,216,'pull FILT',.34)
K(1,'HPF Hz',72,198,28,TEAL); SC(1,72,198,21,['31.5','50','80','150','240','315'],.34); T(1,72,222,'Hz',.38)
HL(1,232)
B(1,'Key',28,250,'KEY',WH,18,TY); B(1,'L/C',72,250,'L/C',WH,18,TG); B(1,'Inv',28,274,'INV',WH,18,TY); B(1,'Dyn Link',72,274,'→',WH,18,TR)
for nm,x,y,col,labs,lab in [('Hysteresis',28,316,GRY,['5','10','15','20','25'],'HYST25'),('Gate Threshold',28,370,GRY,['-25','-10','0','+7','+15'],'THR'),
                            ('Gate Range',28,428,YEL,['0','10','20','30','40','50'],'RGE'),('Gate Release',28,484,GRY,['0.03','0.3','3s'],'REL'),
                            ('Comp Gain',72,316,RED,['0','6','12','18','24','30'],'GAIN'),('Comp Threshold',72,370,GRY,['-10','-4','+2','+8','+14','+20'],'THR'),
                            ('Ratio',72,428,ORG,['1','2','3','5','lim'],'RAT'),('Comp Release',72,484,GRY,['0.03','0.3','3s','AUTO'],'REL')]:
    K(1,nm,x,y,26,col); SC(1,x,y,19,labs,.32); T(1,x,y+26,lab,.38)
T(1,28,338,'EXP',.32); T(1,50,400,'pull -30 · -20',.3); T(1,50,456,'pull FAST',.3)
B(1,'Gate',28,532,'GATE',WH,18,TG); T(1,72,532,'AUTO',.36)
# 2 aux sends 1-8
for p,(o,e) in enumerate([(7,8),(5,6),(3,4),(1,2)]):
    y0=8+p*146
    B(2,f'Aux {e} Pre',26,y0+16,'PRE',WH,18,TB); K(2,f'Aux {o}-{e} Pan',74,y0+18,24,BLU); TK(2,74,y0+18,17); T(2,74,y0+36,'PAN',.34)
    K(2,f'Aux {e}',30,y0+56,26,DGY); TK(2,30,y0+56,19); B(2,f'Aux {e} On',74,y0+62,str(e),WH,18,TG)
    B(2,f'Aux {o} Pre',74,y0+92,'PRE',WH,18,TB)
    K(2,f'Aux {o}',30,y0+104,26,DGY); TK(2,30,y0+104,19); B(2,f'Aux {o} On',74,y0+120,str(o),WH,18,TG)
    B(2,f'Aux {o}-{e} Stereo',30,y0+136,f'{o}-{e}',WH,16,TY); T(2,62,y0+138,'ST',.36)
# 3 EQ
B(3,'Ins',28,22,'INS',WH,18,TG); B(3,'PreEQ',72,22,'PREQ',WH,18,TY); B(3,'Dyn Sidechain',72,46,'DYN',WH,18,TR)
def FREQ(name,x,y,col,labs,unit):
    K(3,name,x,y,30,col,'capblack',{'sweep':[32,328]}); SC(3,x,y,22,labs,.34,32,328); T(3,x-20,y+22,unit,.34)
FREQ('HF kHz',34,84,ORG,['1.5','3','4.7','7','11','17'],'kHz')
K(3,'HF Gain',76,110,24,ORG); T(3,64,130,'−',.4); T(3,88,130,'+',.4)
B(3,'HF Hi-Q',28,134,'HI-Q',WH,18,TY); B(3,'HF Shelf',76,146,'⌐',WH,18,TY)
FREQ('HMF kHz',34,190,BLU,['.8','1.4','2.3','3.6','5.6','8.7'],'kHz')
K(3,'HMF Gain',76,214,24,BLU); T(3,64,234,'−',.4); T(3,88,234,'+',.4)
K(3,'HMF Q',34,252,22,BLU); T(3,34,270,'Q',.38)
K(3,'LMF Gain',76,284,24,GRY); T(3,64,304,'−',.4); T(3,88,304,'+',.4)
FREQ('LMF Hz',34,326,GRY,['190','360','580','870','1k4','2k'],'Hz')
K(3,'LMF Q',76,348,22,GRY); T(3,76,366,'Q',.38)
B(3,'LF Hi-Q',28,384,'HI-Q',WH,18,TY); B(3,'LF Shelf',76,388,'⌐',WH,18,TY)
FREQ('LF Hz',34,436,DGY,['33','63','100','150','240','370'],'Hz')
K(3,'LF Gain',76,462,24,DGY); T(3,64,482,'−',.4); T(3,88,482,'+',.4)
B(3,'EQ',28,498,'EQ',WH,18,TG)
# 4 track, monitor path, small fader, lower quad bus
K(4,'Track',32,42,30,RED); SC(4,32,42,22,['-10','0','+10'],.36,-120,120); T(4,32,66,'TRACK',.38)
B(4,'DIR',76,30,'DIR',RED,20); B(4,'OD',76,60,'OD',WH,22); LED(4,14,82,TR); T(4,40,84,'ATO MTK',.32)
for i,(nm,cap,tab) in enumerate([('Mode C/O','C/O',TY),('Swap','SWAP',TR),('Chop','CHOP',TR),('Mon Dyn','DYN',TG),('Mon Ins','INS',TG),('Mon EQ','EQ',TG),('Mon Aux 7-8','7-8',TG),('Mon Aux 5-6','5-6',TG),('Mon Aux 3-4','3-4',TG),('Mon Aux 1-2','1-2',TG)]):
    B(4,nm,72,112+i*26,cap,WH,18,tab)
F(4,'Small Fader',30,110,350,FAD,.77)
B(4,'Small Solo',30,388,'SOLO',WH,18,TY); B(4,'Small Cut',72,388,'CUT',RED,18)
for nm,x,y in [('QB< 1',30,420),('QB< 2',72,420),('QB< 3',30,446),('QB< 4',72,446)]: B(4,nm,x,y,nm[-1],WH,18,TG)
LED(4,30,472,TR); T(4,30,484,'SMALL FADER',.3); B(4,'Ret',72,474,'RET',WH,18,TY)
B(4,'Lower Pan',72,502,'PAN',WH,18,TY); K(4,'Lower Pan Knob',34,528,28,DBL); TK(4,34,528,20); T(4,18,550,'L',.4); T(4,50,550,'R',.4); T(4,72,550,'QB <',.42)
# 5 large fader
B(5,'Cut Group A',74,26,'A',RED,18); B(5,'Cut Group B',74,52,'B',RED,18)
B(5,'Large Solo',30,86,'SOLO',WH,22); B(5,'Large Cut',74,86,'CUT',RED,22)
F(5,'Large Fader',38,130,580,FAD,.77)
g.d.append(['txt',round((g.cx(5)+50)/g.CW,4),round((34+596)/g.CH,4),'Neve',.8,'#e8322b'])
pages=[[n,round((g.cx(k)-(g.MG if k==0 else g.GP/2))/g.CW,4),0,round((g.cx(k)+100+(g.MG if k==len(cols)-1 else g.GP/2))/g.CW,4),1] for k,n in enumerate(cols)]
strip=dict(kind='Channel Strip',pages=pages,ks='capblack',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2c2f34',bg2='#1d1f23',ink=INK,kc=GRY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

# ================= master section =================
mcols=['Osc & Meter','Aux Master','Cue 1 Mix','Cue 2 Mix','Rev 1','Rev 2','Rev 3','Rev 4','Status & Solo','Control Room','Talkback']
g=build(mcols,110,660,16,.55)
T,K,B,SC,TK,HL,LED,VU,LEDS=g.T,g.K,g.B,g.SC,g.TK,g.HL,g.LED,g.VU,g.LEDS
# 0 oscillator + meter switches
K(0,'Signal LED Threshold',55,46,26,RED); SC(0,55,46,20,['SIG','+4','+8','+20','+26'],.32); T(0,55,76,'SIGNAL LED THRESHOLD',.32)
LED(0,30,104,TR); B(0,'Cal',70,104,'CAL',WH,20); K(0,'Cal Trim',30,124,8,'#b08a3c','trim')
K(0,'Osc Level',55,170,28,GRY); TK(0,55,170,20); T(0,55,196,'LEVEL',.4)
K(0,'Osc Frequency',55,246,28,'#1c1d20','chicken',{'sweep':[-140,140]}); SC(0,55,246,24,['OFF','40Hz','100','400','1k','4k','10k','15k','OFF'],.3,-140,140); T(0,55,282,'FREQUENCY',.38)
B(0,'Osc MTK',55,310,'MTK',WH,22); B(0,'Osc MIX',55,340,'MIX',WH,22); HL(0,362)
LED(0,32,384,TY); T(0,32,398,'SOLO',.36); LED(0,78,384,TR); T(0,78,398,'RECALL',.36)
B(0,'Bargraph VU',32,428,'VU',WH,20); B(0,'Bargraph PPM',78,428,'PPM',WH,20)
B(0,'6dB Dump',32,462,'6dB DUMP',WH,20); B(0,'Digital Cal',78,462,'DIGITAL CAL',WH,20); HL(0,486)
LEDS(0,16,520,94,520,15,'#3ee08a'); T(0,55,538,'PHASE',.38)
VU(0,55,598,92,56,'2T')
# 1 aux master
for p,(o,e) in enumerate([(7,8),(5,6),(3,4),(1,2)]):
    y0=6+p*160
    B(1,f'Aux Master {e} On',30,y0+16,str(e),WH,18,TB); K(1,f'Aux Master {o}-{e} Bal',80,y0+18,24,BLU); TK(1,80,y0+18,17); T(1,80,y0+36,'BAL',.34)
    K(1,f'Aux Master {e}',32,y0+58,28,GRY); TK(1,32,y0+58,20)
    B(1,f'Aux Master {o} On',80,y0+74,str(o),WH,18,TG)
    K(1,f'Aux Master {o}',32,y0+108,28,GRY); TK(1,32,y0+108,20)
    B(1,f'Aux Master {o}-{e} Stereo',80,y0+128,f'{o}-{e}',WH,16,TY); T(1,46,y0+144,'ST',.34)
# 2/3 cue mixes
for k,n in ((2,1),(3,2)):
    rows=[('7','8'),('5','6'),('3','4'),('1','2'),('5-6','7-8'),('1-2','3-4')]
    for r,(a,b) in enumerate(rows):
        B(k,f'Cue {n} Aux {a}',32,30+r*26,a,WH,18,TY); B(k,f'Cue {n} Aux {b}',78,30+r*26,b,WH,18,TY)
    T(k,10,96,'AUX',.36)
    B(k,f'Cue {n} Mon',32,198,'MON',WH,18,TY); B(k,f'Cue {n} Patch',78,198,'PATCH',WH,18,TY)
    B(k,f'Cue {n} Mix 1-2',32,224,'1-2',WH,18,TY); B(k,f'Cue {n} Mix 3-4',78,224,'3-4',WH,18,TY); HL(k,244)
    B(k,f'Cue {n} Filter 82',32,262,'82',WH,18); B(k,f'Cue {n} Filter 47',32,288,'47',WH,18); T(k,78,276,'FILTER 150',.34)
    B(k,f'Cue {n} EQ',32,314,'EQ',WH,18,TG)
    K(k,f'Cue {n} HF 10k',42,356,26,ORG); TK(k,42,356,19); T(k,82,360,'10k',.36)
    K(k,f'Cue {n} LF 100',42,410,26,'#1c1d20'); TK(k,42,410,19); T(k,82,414,'100',.36)
    K(k,f'Cue {n} Bal',42,464,26,BLU); TK(k,42,464,19); T(k,82,468,'BAL',.36)
    K(k,f'Cue {n} Level',42,520,28,GRY); TK(k,42,520,20); T(k,82,524,'LEVEL',.36)
    B(k,f'Cue {n} Bal On',32,566,'BAL',WH,18,TG); B(k,f'Cue {n} On',32,594,'ON',WH,18,TG); T(k,55,636,f'CUE {n}',.5)
# 4-7 reverb returns
for k in range(4,8):
    n=k-3
    K(k,f'Rev {n} Cue/Rev 2',42,40,26,GRY); TK(k,42,40,19); T(k,84,36,'CUE/REV',.32); T(k,84,48,'2',.32); B(k,f'Rev {n} Cue 2 On',32,80,'ON',WH,18,TG)
    K(k,f'Rev {n} Cue/Rev 1',42,122,26,GRY); TK(k,42,122,19); T(k,84,118,'CUE/REV',.32); T(k,84,130,'1',.32); B(k,f'Rev {n} Cue 1 On',32,162,'ON',WH,18,TG); HL(k,182)
    for nm,x,y in [('1',32,200),('2',78,200),('3',32,226),('4',78,226)]: B(k,f'Rev {n} Route {nm}',x,y,nm,WH,18,TG)
    HL(k,246)
    B(k,f'Rev {n} Filter 82',32,264,'82',WH,18); B(k,f'Rev {n} Filter 47',32,290,'47',WH,18); T(k,78,278,'FILTER 150',.34)
    B(k,f'Rev {n} EQ',32,316,'EQ',WH,18,TG)
    K(k,f'Rev {n} HF 10k',42,358,26,ORG); TK(k,42,358,19); T(k,82,362,'10k',.36)
    K(k,f'Rev {n} LF 100',42,412,26,'#1c1d20'); TK(k,42,412,19); T(k,82,416,'100',.36)
    K(k,f'Rev {n} Bal',42,466,26,BLU); TK(k,42,466,19); T(k,82,470,'BAL',.36)
    K(k,f'Rev {n} Level',42,522,28,GRY); TK(k,42,522,20); T(k,82,526,'LEVEL',.36)
    B(k,f'Rev {n} Bal On',32,568,'BAL',WH,18,TG); B(k,f'Rev {n} On',32,596,'ON',WH,18,TG); T(k,55,636,f'REV {n}',.5)
# 8 status, multitrack monitors, meters, cues, solo + cut, studio monitor
k=8
B(k,'Status Lock',55,36,'STATUS LOCK',RED,26)
for i,(nm,col) in enumerate([('Broadcast',ORG),('MIC',RED),('Fader Swap',BLU),('Mix Down',WH)]):
    y=82+i*30; B(k,nm+' ←',20,y,'←',col,18); B(k,nm,55,y,nm.upper(),col,22); B(k,nm+' →',90,y,'→',col,18)
T(k,55,200,'STATUS',.42); HL(k,210)
B(k,'MT Monitors O/P',22,232,'O/P',RED,20); B(k,'MT Monitors P/B',55,232,'P/B',TEAL,20); B(k,'MT Monitors O/D',88,232,'O/D',ORG,20); T(k,55,252,'MULTITRACK MONITORS',.3); HL(k,262)
B(k,'Meters O/P',22,282,'O/P',RED,20); B(k,'Meters P/B',55,282,'P/B',TEAL,20); B(k,'Meters Follow Mon',88,282,'FOLLOW MON',WH,20)
B(k,'Meters Mix 1-2',22,310,'MIX 1-2',WH,20); B(k,'Meters Mix 3-4',55,310,'MIX 3-4',WH,20); B(k,'Meters Ext',88,310,'EXT',WH,20); T(k,55,330,'METERS',.38); HL(k,340)
B(k,'Mixed Cues',35,360,'MIXED CUES',WH,22); B(k,'Cues Post EQ',75,360,'CUES POST EQ',WH,22); T(k,55,382,'CUES',.38); HL(k,392)
for i,(nm,cap,col) in enumerate([('Chan Safe','CHAN SAFE',WH),('Mon Safe','MON SAFE',WH),('PFL','PFL',WH),('Latch','LATCH',WH),('I/L','I/L',WH),('Reset','RESET',WH),('Cut A','CUT A',RED),('Cut B','CUT B',RED),('Solo Link','SOLO LINK',WH)]):
    B(k,nm,22+33*(i%3),412+(i//3)*28,cap,col,20)
T(k,55,488,'SOLO + CUT',.38); HL(k,498)
K(k,'RTB Level 1',26,520,20,GRY); K(k,'RTB Level 2',84,520,20,GRY); T(k,55,522,'RTB LEVEL',.3)
K(k,'Studio Monitor Level',55,570,28,DBL); TK(k,55,570,20)
B(k,'Studio Monitor Cut',22,614,'CUT',RED,20); B(k,'Studio Monitor Ext',55,614,'EXT',WH,20); B(k,'Studio Monitor Follow Mon',88,614,'FOLLOW MON',WH,20); T(k,55,640,'STUDIO MONITOR',.34)
# 9 control room
k=9
left=['8','7','6','5','4','3','2','1','7-8','5-6','3-4','1-2','2','1','3-4','1-2']
for r in range(16):
    lab=left[r]; grp='Aux' if r<12 else ('Cue' if r<14 else 'Mix')
    B(k,f'CR {grp} {lab}',34,26+r*19,lab,WH,16,TY)
    B(k,f'CR Ext {16-r}',80,26+r*19,str(16-r),WH,16,TG)
T(k,14,140,'AUX',.3); T(k,14,282,'CUE',.3); T(k,14,320,'MIX',.3)
K(k,'AFL/PFL Level',20,358,18,GRY)
B(k,'AFL/PFL',24,384,'AFL PFL',WH,20); B(k,'INT',55,384,'INT',WH,20); B(k,'EXT',86,384,'EXT',WH,20)
B(k,'Cut L',24,412,'CUT L',RED,20); B(k,'Cut R',55,412,'CUT R',RED,20); B(k,'L-R Swap',86,412,'L-R SWAP',WH,20)
B(k,'Large',24,440,'LARGE',WH,20); B(k,'Small',55,440,'SMALL',WH,20); B(k,'Mini',86,440,'MINI',WH,20)
for i,x in enumerate((24,55,86)): K(k,['Large','Small','Mini'][i]+' Trim',x,462,7,'#b08a3c','trim')
K(k,'Dim Level',22,494,20,GRY); T(k,22,512,'DIM',.34); B(k,'Bal In',55,488,'IN',WH,16,TG); K(k,'CR Bal',88,494,20,GRY); T(k,88,512,'L BAL R',.3)
K(k,'CR Level',55,548,32,DBL); TK(k,55,548,23); T(k,55,576,'LEVEL',.38)
B(k,'CR Cut',24,604,'CUT',RED,20); B(k,'CR Dim',55,604,'DIM',WH,20); B(k,'CR Mono',86,604,'MONO',WH,20); T(k,55,630,'CONTROL ROOM MONITOR',.3)
# 10 talkback + main meters
k=10
K(k,'Phones',28,44,22,GRY); K(k,'TB Level',82,44,22,GRY); T(k,28,62,'PHONES',.32); T(k,82,62,'TB LEVEL',.32)
K(k,'TB to Cues & SLS',55,94,22,GRY); T(k,55,112,'TB TO CUES & SLS',.3)
for i,(nm,cap,col) in enumerate([('Red Light','RED LIGHT',RED),('RTB','RTB',WH),('All','ALL',WH),('Auto TB','AUTO TB',ORG),('SLS','SLS',ORG),('Slate','SLATE',WH),('Cue 1','CUE 1',ORG),('Cue 2','CUE 2',ORG),('F/B 1-2','F/B 1-2',BLU),('F/B 3-4','F/B 3-4',BLU),('F/B 5-6','F/B 5-6',BLU),('F/B 7-8','F/B 7-8',BLU)]):
    B(k,nm,30+50*(i%2),140+(i//2)*28,cap,col,20)
T(k,55,310,'TALKBACK',.42); HL(k,322)
VU(k,55,380,96,58,'2T L'); VU(k,55,452,96,58,'2T R'); VU(k,55,524,96,58,'MON L'); VU(k,55,596,96,58,'MON R')
mpages=[[n,round((g.cx(a)-(g.MG if a==0 else g.GP/2))/g.CW,4),0,round((g.cx(b)+110+(g.MG if b==10 else g.GP/2))/g.CW,4),1] for n,a,b in [('Osc & Aux Master',0,1),('Cue Mixes',2,3),('Reverb Returns',4,7),('Status & Solo',8,8),('Control Room & Talkback',9,10)]]
master=dict(kind='Master Section',pages=mpages,ks='capblack',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2c2f34',bg2='#1d1f23',ink=INK,kc=GRY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Neve VR',strip),('Neve VR Master Section',master)]))
