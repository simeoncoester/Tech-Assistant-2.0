# Generator for the FACEPLATES entries 'API 1608-II' (channel strip: 548C + 444C fader) and 'API 1608-II Master Section'.
# Source: user's "1608-II and 2448 Recording Console Operator's Manual" (module drawings 548C, 265C, 168C, 840C, 845C, 268C, 940C, stereo returns).
# The EQ of each channel sits in a 500 slot (550A or 560) and is chosen as its own stage, so it is not part of this strip.
# Helpers come from tools/ssl4000eg-gen.py. Usage: python3 tools/api1608-gen.py > out.txt, then replace the lines starting with  "API 1608-II.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
INK='#f2f2f2'; BLU='#2b8ff0'; GRN='#169a2a'; YL='#f6f1a4'; SOLO='#f4e21a'; MUTE='#c8160c'; LG='#68c26a'; OR='#f7c254'; RD='#f06060'
CHF=[['10',1],['5',.8],['0',.684],['5',.516],['10',.389],['15',.289],['20',.221],['30',.126],['50',.047],['∞',0]]
PGF=[['0',1],['5',.78],['10',.65],['15',.52],['20',.40],['25',.30],['30',.23],['40',.13],['60',.05],['∞',0]]
def kit(g):
    K,B,SC,DOT,HL,LED,F=g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
    T=lambda k,x,y,t,sz=.5,col=None: g.T(k,x,y,t,sz,col or INK)
    D=lambda k,x,y,r,n=11,a0=-140,a1=140: g.d.append(['pdots',*[round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y)/g.CH,4)],round(r/g.CW,4),n,round(2.6/g.CW,4),BLU,a0,a1])
    Y=lambda k,name,x,y,cap=None,dia=18: B(k,name,x,y,cap,YL,dia)
    return K,B,SC,DOT,HL,LED,F,T,D,Y
def CONC(g,k,ring,inner,x,y,top,bot):
    # concentric knob after the drawings: outer ring = lower label, inner knob = upper label (symbol beside the knob)
    g.K(k,ring,x,y,30,'#169a2a','apiring'); g.K(k,inner,x,y,18,'#169a2a','api')
    g.T(k,x-26,y-12,top,.3,INK); g.T(k,x-26,y+16,bot,.3,INK)
    g.d.append(['pdots',round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y)/g.CH,4),round(21/g.CW,4),11,round(2.6/g.CW,4),BLU,-140,140])

# ================= channel strip =================
cols=['Routing','Aux Sends','Preamp & Solo','Fader']
g=build(cols,100,600,.75)
K,B,SC,DOT,HL,LED,F,T,D,Y=kit(g)
k=0; T(k,80,10,'548C',.5,BLU)
for r,(a,b) in enumerate([(7,8),(5,6),(3,4),(1,2)]):
    y=44+r*54; T(k,16,y+4,str(a),.5); Y(k,f'Bus {a}',38,y); Y(k,f'Bus {b}',66,y); T(k,88,y+4,str(b),.5)
HL(k,268); Y(k,'Bus Pan',66,292); T(k,88,296,'PAN',.4)
K(k,'Pan',32,346,32,'#141414','api'); D(k,32,346,24); T(k,14,382,'L',.32); T(k,32,384,'PAN',.34); T(k,50,382,'R',.32)
K(k,'Pan Trim',32,410,8,'#b08a3c','trim')
Y(k,'PGM',72,386); T(k,72,406,'PGM',.38)
Y(k,'FLTR',24,452); T(k,24,472,'FLTR',.36); Y(k,'INS',72,452); T(k,72,472,'INS',.36)
k=1
CONC(g,k,'Aux 7/8 Level','Aux 7/8 Pan',42,40,'PAN','LVL'); Y(k,'To Bus',82,40); T(k,82,60,'TO BUS',.3)
Y(k,'Aux 7/8 Pre',30,92); T(k,30,112,'PRE',.3); Y(k,'Aux 7/8',74,92); T(k,74,112,'7/8',.34)
HL(k,126)
CONC(g,k,'Aux 5/6 Level','Aux 5/6 Pan',42,166,'PAN','LVL')
Y(k,'Aux 5/6 Pre',30,218); T(k,30,238,'PRE',.3); Y(k,'Aux 5/6',74,218); T(k,74,238,'5/6',.34)
HL(k,252)
CONC(g,k,'Aux 3','Aux 4',42,292,'4','3'); Y(k,'Aux 4 On',82,292); T(k,82,312,'4',.34)
Y(k,'Aux 3/4 Pre',30,344); T(k,30,364,'PRE',.3); Y(k,'Aux 3 On',74,344); T(k,74,364,'3',.34)
HL(k,378)
CONC(g,k,'Aux 1','Aux 2',42,418,'2','1'); Y(k,'Aux 2 On',82,418); T(k,82,438,'2',.34)
Y(k,'Aux 1/2 Pre',30,470); T(k,30,490,'PRE',.3); Y(k,'Aux 1 On',74,470); T(k,74,490,'1',.34)
k=2; T(k,50,14,'PREAMP',.45)
K(k,'Gain',36,66,30,BLU,'api'); D(k,36,66,22); T(k,36,98,'GAIN',.34); T(k,10,112,'PK',.3); LED(k,24,108,'#e0241a',6)
Y(k,'Phase',78,40); T(k,78,60,'Ø',.4); Y(k,'MIC',78,86); T(k,78,106,'MIC',.34)
Y(k,'48V',36,140); T(k,36,160,'48V',.34); Y(k,'PAD',78,140); T(k,78,160,'PAD',.34)
HL(k,178)
Y(k,'Safe',26,214); T(k,26,234,'SAFE',.3); B(k,'Solo',74,214,'SOLO',SOLO,30)
Y(k,'Mute Grp',26,270); T(k,26,288,'MUTE',.28); T(k,26,298,'GRP',.28); B(k,'Mute',74,270,None,MUTE,30)
k=3
F(k,'Fader',40,40,560,CHF,.684)
g.T(k,80,20,'444C',.4,BLU)
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='api',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#0d0d0f',bg2='#060607',ink=INK,kc=GRN,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

# ================= master section =================
mcols=['840C Oscillator','840C Meter & Solo','840C Talkback','845C C/R Source','845C Monitor','168C Bus 1-4','168C Bus 5-8','265C Aux 1-4','265C Aux 5-8',
       'Stereo Returns 1-2','Stereo Returns 3-4','268C PGM Master','940C PGM Fader']
g=build(mcols,110,600,.38,7)
K,B,SC,DOT,HL,LED,F,T,D,Y=kit(g)
k=0
K(k,'Osc Frequency',55,70,40,'#c41a10','api',{'sweep':[-110,110]}); SC(k,55,70,30,['20','50','400','1K','2K','5K','15K'],.28,-110,110)
K(k,'Osc Level',40,170,26,'#c41a10','api'); D(k,40,170,19); T(k,84,174,'LEVEL',.34)
Y(k,'Osc Bus',34,232); T(k,74,236,'BUS',.36); Y(k,'Osc On',34,280); T(k,74,284,'ON',.36)
T(k,55,320,'OSCILLATOR',.38); HL(k,334)
K(k,'Peak Threshold',55,392,26,'#c41a10','api',{'sweep':[-120,120]}); SC(k,55,392,24,['+4','+8','+12','+16','+20','+24'],.28,-120,120); T(k,55,438,'dBu',.26,BLU); T(k,55,452,'PEAK THRESHOLD',.28)
k=1
for nm,x,y in [('SM',28,30),('LRG',28,52),('DIR',78,52)]: LED(k,x,y,'#f1d61e',7); T(k,x-16 if x<50 else x+16,y+3,nm,.28,BLU)
B(k,'VU CH',30,96,'VU CH',LG,30); B(k,'VU BUS',80,96,'VU BUS',LG,30)
B(k,'Flip',30,146,'FLIP',LG,30); B(k,'0dB SM',80,146,'0dB SM',OR,30); T(k,30,172,'CLEAR',.28,BLU)
HL(k,186)
K(k,'Solo Level',40,230,28,'#f2e31d','api'); D(k,40,230,20); T(k,86,234,'LEVEL',.32)
Y(k,'SIP',58,290); T(k,24,294,'SIP',.34); Y(k,'AFL',58,332); T(k,24,336,'AFL',.34)
B(k,'Solo Clear',84,312,'SOLO CLEAR',OR,28); T(k,55,368,'SOLO MASTER',.32)
k=2
LED(k,30,24,'#ffffff',8); T(k,72,27,'T/B MIC CAL',.26,BLU)
K(k,'T/B Bus Level',34,70,26,'#e8e8e8','api'); D(k,34,70,19); B(k,'T/B Bus',82,70,'BUS',OR,28)
K(k,'T/B Aux Level',34,134,26,'#169a2a','api'); D(k,34,134,19); B(k,'T/B Aux',82,134,'AUX',OR,28)
B(k,'T/B All',82,200,'T/B ALL',RD,28); T(k,55,240,'TALKBACK',.34); HL(k,254)
K(k,'Headphones',34,300,26,'#e0e0e0','api'); D(k,34,300,19); Y(k,'Phones On',82,300); T(k,82,320,'ON',.32); T(k,55,348,'HEADPHONES',.32)
k=3; T(k,80,10,'845C',.45,BLU)
for i,n in enumerate(['3','2','1']): Y(k,f'6-Track {n}',30,50+i*44); T(k,12,54+i*44,n,.36)
T(k,78,94,'6-TRACK',.3); T(k,78,106,'PLAYBACK',.3)
for i,n in enumerate(['7/8','5/6','3/4','1/2']): Y(k,f'Aux Sends {n}',30,200+i*44); T(k,10,204+i*44,n,.3)
T(k,80,262,'AUX',.3); T(k,80,274,'SENDS',.3)
Y(k,'C/R PGM',30,388); T(k,10,392,'PGM',.3); T(k,55,428,'C/R SOURCE',.32)
k=4
B(k,'Alt 2',80,40,'ALT 2',LG,30); B(k,'Mono',34,88,'MONO',RD,30); B(k,'Alt 1',80,88,'ALT 1',LG,30)
B(k,'Monitor Cut',34,136,'CUT',RD,30); B(k,'Main Spkr',80,136,'MAIN SPKR',LG,30)
K(k,'Control Room',55,226,50,'#141414','api'); D(k,55,226,34,13); T(k,55,272,'CONTROL ROOM',.32)
HL(k,290); K(k,'Dim Level',34,348,24,'#141414','api'); D(k,34,348,17); T(k,34,376,'DIM LEVEL',.26); B(k,'Dim',82,330,'DIM',OR,28)
for k,b0 in ((5,4),(6,8)):
    if k==5: T(k,80,8,'168C',.4,BLU)
    for i in range(4):
        n=b0-i; y=40+i*142
        T(k,22,y-12,'CAL',.24,BLU); K(k,f'Bus {n} Cal',44,y-14,8,'#b08a3c','trim')
        K(k,f'Bus {n} Level',34,y+28,26,'#141414','api'); D(k,34,y+28,19); T(k,16,y+52,'∞',.3); T(k,52,y+52,'0',.26)
        Y(k,f'Bus {n} PGM RT',82,y+4); T(k,82,y+22,'RT',.28); T(k,82,y+34,'PGM',.28); Y(k,f'Bus {n} PGM LT',82,y+50); T(k,82,y+68,'LT',.28)
        Y(k,f'Bus {n} On',30,y+86); T(k,30,y+104,'ON',.28); Y(k,f'Bus {n} Solo',82,y+86); T(k,82,y+104,'SOLO',.28); T(k,56,y+118,f'BUS {n}',.32)
for k,a0 in ((7,4),(8,8)):
    if k==7: T(k,80,8,'265C',.4,BLU)
    for i in range(4):
        n=a0-i; y=46+i*140
        K(k,f'Aux {n} Master',32,y+10,26,'#169a2a','api'); D(k,32,y+10,19); T(k,14,y+34,'∞',.3); T(k,52,y+34,'+6',.26); T(k,50,y-12,'0',.26)
        T(k,80,y-14,f'AUX SEND {n}',.26); Y(k,f'Aux {n} Ext In',82,y+16); T(k,82,y+34,'EXT IN',.24)
        Y(k,f'Aux {n} On',30,y+66); T(k,30,y+84,'ON',.26); Y(k,f'Aux {n} T/B',82,y+56); T(k,82,y+74,'T/B',.26)
        Y(k,f'Aux {n} VU',30,y+104); T(k,30,y+120,'VU',.26); Y(k,f'Aux {n} Solo',82,y+96); T(k,82,y+112,'SOLO',.26)
for k,r0 in ((9,1),(10,3)):
    for j in range(2):
        n=r0+j; o=j*55; T(k,o+27,10,f'RET {n}',.3)
        for i,(nm,cap) in enumerate([('7/8','7/8'),('PGM','PGM'),('Aux In','AUX IN'),('500 Ins','500 INS'),('Mono','MONO'),('Ins','INS')]):
            Y(k,f'Return {n} {nm}',o+16,36+i*32,None,14); T(k,o+38,40+i*32,cap,.2)
        Y(k,f'Return {n} Safe',o+16,236,None,14); T(k,o+38,240,'SAFE',.2)
        B(k,f'Return {n} Solo',o+27,270,'SOLO',SOLO,20); B(k,f'Return {n} Mute',o+27,300,f'R{n}',MUTE,20)
        F(k,f'Return {n} Fader',o+22,330,580,CHF,.684)
k=11; T(k,80,8,'268C',.4,BLU); Y(k,'PGM Insert',55,40); T(k,55,60,'PGM INSERT',.28)
for i,s2 in enumerate(['RT','LT']):
    y=110+i*130; T(k,24,y-16,'CAL',.24,BLU); K(k,f'PGM {s2} Cal',24,y,8,'#b08a3c','trim')
    K(k,f'PGM {s2} Trim',66,y+16,26,'#e8e8e8','api'); D(k,66,y+16,19); T(k,66,y+44,'TRIM',.26)
    Y(k,f'PGM {s2} On',24,y+50); T(k,24,y+68,'ON',.26); T(k,55,y+86,f'PGM {s2}',.3)
k=12; T(k,80,8,'940C',.4,BLU); T(k,80,30,'PGM',.6)
F(k,'PGM Fader',70,60,560,PGF,1,'#f02a10')
for nm,y,col in [('READ',380,'#3aa53a'),('UPDATE',430,'#f3ee32'),('WRITE',480,'#c4200f')]: LED(k,26,y,col,10); T(k,26,y-12,nm,.24)
master=dict(kind='Master Section',pages=pages_of(g,[('Oszillator & Solo',0,1),('Talkback & Monitor',2,4),('Summing Busse',5,6),('Aux Masters',7,8),('Stereo Returns',9,10),('Program Bus',11,12)],len(mcols)),ks='api',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#0d0d0f',bg2='#060607',ink=INK,kc=GRN,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('API 1608-II',strip),('API 1608-II Master Section',master)]))
