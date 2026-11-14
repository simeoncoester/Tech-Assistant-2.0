# Generator for 'API Legacy AXS' (channel strip: 212 preamp, 225 compressor, 624 bus assign, 968 input module, 948 fader)
# and 'API Legacy AXS Master Section' after the official API "Legacy AXS Operator's Manual V2.0" (apiaudio.com).
# The 500 slot EQ (550A/550b/560) and the 2500C bus compressor are separate devices. Helpers from tools/api1608-gen.py.
import os, sys, json
d0=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(d0,'ssl4000eg-gen.py')).read(); exec(src[:src.index('# ================= channel strip')])
a=open(os.path.join(d0,'api1608-gen.py')).read(); i0=a.index("INK='#f2f2f2'"); exec(a[i0:a.index('# ================= channel strip',i0)])
cols=['212 & 225','624 Bus Assign','968 Small Fader','968 Aux & Large','948 Fader']
g=build(cols,100,600,.7)
K,B,SC,DOT,HL,LED,F,T,D,Y=kit(g)
k=0; T(k,50,10,'212',.4,BLU)
K(k,'Mic Gain',40,46,30,BLU,'api'); D(k,40,46,22); T(k,40,78,'GAIN',.32)
g.d.append(['leds',*[round((g.cx(k)+84)/g.CW,4),round((34+28)/g.CH,4)],*[round((g.cx(k)+84)/g.CW,4),round((34+70)/g.CH,4)],5,round(5/g.CW,4),'#35d06a',0,'#ff4433'])
Y(k,'48V',28,104); T(k,28,122,'48V',.3); Y(k,'-20',72,104); T(k,72,122,'-20',.3)
HL(k,140); T(k,50,154,'225',.4,BLU)
Y(k,'Comp In',80,174); T(k,80,192,'IN',.3)
K(k,'Threshold',36,192,26,'#e8e8e8','api'); SC(k,36,192,22,['-20','-10','0','+10'],.28,-135,135); T(k,36,224,'THRESH',.28)
K(k,'Ratio',36,262,26,'#141414','api'); SC(k,36,262,22,['1','2','4','∞'],.28,-135,135); T(k,36,294,'RATIO',.28)
K(k,'Attack',40,342,30,'#169a2a','apiring'); K(k,'Release',40,342,18,'#169a2a','api'); D(k,40,342,22); T(k,14,330,'R',.3); T(k,14,356,'A',.3)
T(k,40,380,'A 1–25ms · R .3–3s',.2)
Y(k,'Knee Hard/Soft',80,250); T(k,80,268,'HRD/SFT',.24); Y(k,'Type New/Old',80,300); T(k,80,318,'NEW/OLD',.24)
g.d.append(['leds',*[round((g.cx(k)+84)/g.CW,4),round((34+340)/g.CH,4)],*[round((g.cx(k)+84)/g.CW,4),round((34+410)/g.CH,4)],8,round(5/g.CW,4),'#ffb020',0,'#ff4433']); T(k,84,424,'-dB',.26)
k=1; T(k,80,10,'624',.4,BLU)
for i in range(12):
    a1=23-2*i; a2=24-2*i; y=34+i*30
    T(k,14,y+4,str(a1),.32); Y(k,f'Bus {a1}',36,y,None,16); Y(k,f'Bus {a2}',66,y,None,16); T(k,88,y+4,str(a2),.32)
HL(k,400)
for i,nm in enumerate(['ST C','ST B','ST A','PAN']):
    y=420+i*30; Y(k,f'SM {nm}',30,y,None,16); Y(k,f'LG {nm}',72,y,None,16); T(k,51,y+4,nm,.26)
T(k,30,546,'SM',.3); T(k,72,546,'LG',.3)
k=2; T(k,80,10,'968',.4,BLU)
K(k,'SF Trim',28,34,22,'#5a5d61','api'); D(k,28,34,16); T(k,28,56,'TRIM',.24); LED(k,12,62,'#ff4433',5); T(k,24,66,'PK',.22)
for i,(nm,cap) in enumerate([('SF to 24','24'),('SF Filt','FILT'),('EQ SM','EQ SM'),('Aux 5-12 SM','AUX 5-12')]): Y(k,nm,20,90+i*26,None,14); T(k,44,93+i*26,cap,.24,BLU if cap in('EQ SM',) else INK)
F(k,'Small Fader',76,30,230,[['10',1],['5',.86],['0',.74],['5',.6],['10',.46],['20',.3],['30',.18],['∞',0]],.74)
K(k,'SF Pan',30,224,24,'#141414','api'); D(k,30,224,18); T(k,16,246,'L',.24); T(k,44,246,'R',.24)
for i,(nm,cap) in enumerate([('SF Safe','SAFE'),('SF Phase','Ø'),('Alt','ALT'),('SF Ins','INS')]): Y(k,nm,20,274+i*26,None,14); T(k,44,277+i*26,cap,.24,BLU if cap=='ALT' else INK)
B(k,'SF Solo',78,284,'SOLO',SOLO,26); B(k,'SF Mute',78,330,None,MUTE,26)
k=3
rows=[('Aux 11/12','Aux 9/10',True),('Aux 7/8',None,True),('Aux 5/6',None,True),('Aux 3/4',None,False),('Aux 1/2',None,False)]
for i,nm in enumerate(['Aux 9/10 - 11/12','Aux 7/8','Aux 5/6','Aux 3/4','Aux 1/2']):
    y=30+i*58
    if i<3: CONC(g,k,f'{nm} Level',f'{nm} Pan',40,y,'PAN','LVL')
    else:
        a1,a2=nm.split()[1].split('/'); CONC(g,k,f'Aux {a1}',f'Aux {a2}',40,y,a2,a1)
ons=[('Aux 11/12 On','11/12'),('Aux 9/10-11/12 Pre','PRE'),('Aux 9/10 On','9/10'),('Aux 7/8 On','7/8'),('Aux 5/6-7/8 Pre','PRE '),('Aux 5/6 On','5/6'),('Aux 3/4 On','3/4'),('Aux 1/2-3/4 Pre','PRE  '),('Aux 1/2 On','1/2')]
for i,(nm,cap) in enumerate(ons): Y(k,nm,84,20+i*28,None,14); T(k,84,34+i*28,cap.strip(),.2)
HL(k,290)
K(k,'LF Trim',28,314,22,'#5a5d61','api'); D(k,28,314,16); T(k,28,336,'TRIM',.24); LED(k,12,340,'#ff4433',5)
Y(k,'Dir Pre',84,306,None,14); T(k,84,320,'DIR PRE',.2); Y(k,'Dir SM',84,334,None,14); T(k,84,348,'DIR SM',.2)
Y(k,'Line Pad -6',20,364,None,14); T(k,44,367,'PAD -6',.22); Y(k,'Comp Lrg',20,392,None,14); T(k,48,395,'COMP LRG',.2,BLU)
K(k,'LF Filter Sweep',78,374,20,BLU,'api'); D(k,78,374,14); Y(k,'LF Filt',84,404,None,14); T(k,84,418,'FILT',.2)
K(k,'LF Pan',30,436,28,'#141414','api'); D(k,30,436,20); T(k,16,462,'L',.24); T(k,44,462,'R',.24)
for i,(nm,cap) in enumerate([('LF Safe','SAFE'),('LF Phase','Ø'),('Flip','FLIP'),('LF Ins','INS')]): Y(k,nm,20,482+i*26,None,14); T(k,44,485+i*26,cap,.24,BLU if cap=='FLIP' else INK)
B(k,'LF Solo',78,470,'SOLO',SOLO,26); B(k,'LF Mute',78,516,None,MUTE,26)
k=4; T(k,80,10,'948',.4,BLU)
B(k,'Automation Mute',30,40,'MUTE',MUTE,22)
for nm,y,col in [('Switch Overwrite',84,'#c4200f'),('Static',120,'#2b8ff0'),('Sub-Mode',144,'#2f9a2f'),('Read',180,'#2f9a2f'),('Update',216,'#f3ee32'),('Write',252,'#c4200f')]:
    B(k,nm,22,y,None,col,12); g.c[-1][7]['ps']='rd'; T(k,22,y-12,nm.upper(),.18)
F(k,'Large Fader',72,60,580,CHF,.684)
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='api',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#0d0d0f',bg2='#060607',ink=INK,kc=GRN,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

mcols=['Input Select & Osc','Stereo Returns 1-3','Stereo Returns 4-6','Aux Masters 1-6','Aux Masters 7-12','Multitrack 1-12','Multitrack 13-24','Program A & B','Program C & GM','Monitor Select','Speakers & Studio','Solo','Talkback']
g=build(mcols,110,600,.4,7)
K,B,SC,DOT,HL,LED,F,T,D,Y=kit(g)
k=0; T(k,55,12,'INPUT SELECT',.28)
for i,(nm,cap,col) in enumerate([('Flip','FLIP',LG),('SM Alt Line','SM ALT',LG),('All Clr','ALL CLR',OR),('Comp Lrg','COMP LRG',LG),('Comp Byp','COMP BYP',OR),('0dB SM','0dB SM',OR)]):
    B(k,nm,30+(i%2)*50,40+(i//2)*44,cap,col,26)
HL(k,180); T(k,55,194,'OSCILLATOR',.28)
K(k,'Osc Frequency',55,236,34,'#c41a10','api',{'sweep':[-110,110]}); SC(k,55,236,26,['20','50','400','1K','2K','5K','15K'],.26,-110,110)
K(k,'Osc Level',36,300,24,'#c41a10','api'); D(k,36,300,17); T(k,80,302,'LEVEL',.28)
Y(k,'Osc Bus',30,340); T(k,62,342,'BUS',.26); Y(k,'Osc On',30,372); T(k,62,374,'ON',.26)
for k,r0 in ((1,1),(2,4)):
    for j in range(3):
        n=r0+j; o=j*36+4
        T(k,o+16,10,f'R{n}',.26)
        for i,cap in enumerate(['GM','STC','STB','STA','MONO','BUS','INS','SAFE']): Y(k,f'Return {n} {cap.title()}',o+16,28+i*24,None,12); T(k,o+16,40+i*24,cap,.15)
        K(k,f'Return {n} Trim',o+16,232,14,'#5a5d61','api'); T(k,o+16,248,'TRIM',.15)
        B(k,f'Return {n} Solo',o+16,270,'SOLO',SOLO,16); B(k,f'Return {n} Mute',o+16,294,None,MUTE,16)
        F(k,f'Return {n} Fader',o+14,330,580,CHF,.684)
for k,a0 in ((3,1),(4,7)):
    for i in range(6):
        n=a0+i; y=26+i*92
        K(k,f'Aux {n} Master',30,y+14,22,'#169a2a','api'); D(k,30,y+14,16); T(k,30,y-6,f'AUX {n}',.24)
        for j,cap in enumerate(['ON','T/B','AFL']): Y(k,f'Aux {n} {cap}',80,y+j*22,None,12); T(k,62,y+3+j*22,cap,.16)
        g.d.append(['leds',*[round((g.cx(k)+12)/g.CW,4),round((g.ry(k)+34+y+40)/g.CH,4)],*[round((g.cx(k)+50)/g.CW,4),round((g.ry(k)+34+y+40)/g.CH,4)],5,round(4/g.CW,4),'#35d06a',0,'#ff4433'])
for k,b0 in ((5,1),(6,13)):
    for i in range(12):
        n=b0+i; c,r=i%2,i//2; x=30+c*50; y=28+r*92
        K(k,f'Bus {n} Level',x,y+10,20,'#141414','api'); D(k,x,y+10,14); T(k,x,y-8,str(n),.26)
        K(k,f'Bus {n} Cal',x-14,y+40,7,'#b08a3c','trim'); Y(k,f'Bus {n} On',x+10,y+42,None,12); T(k,x+10,y+56,'ON',.15)
for j,nm in enumerate(['STA','STB','STC','GM']):
    k=7+j//2; o=12+(j%2)*50; T(k,o+18,12,nm,.26)
    for i,cap in enumerate(['ON','INS']+(['GM'] if nm!='GM' else ['EXT'])): Y(k,f'{nm} {cap.title()}',o+4,36+i*26,None,12); T(k,o+4,48+i*26,cap,.14)
    K(k,f'{nm} Cal',o+30,40,7,'#b08a3c','trim'); T(k,o+30,54,'CAL',.13)
    F(k,f'{nm} Master Fader',o+6,150,580,PGF,1,'#f02a10' if nm=='GM' else '#d8d8d8')
k=9; T(k,55,12,'MONITOR SELECT',.26)
for i,nm in enumerate(['GM','STA','STB','STC','AUX 1/2','AUX 3/4','AUX 5/6','AUX 7/8','AUX 9/10','AUX 11/12']): B(k,'Mon '+nm.title(),28,34+i*28,nm,LG,20)
B(k,'Pgm Mntr',28,326,'MNTR',OR,20)
for i,nm in enumerate(['2T1','2T2','2T3','2T4','6T1','6T2']): B(k,'Play '+nm,82,34+i*28,nm,LG,20)
B(k,'2T4 +4/-10',82,212,'+4/-10',WH,16); B(k,'Play Mntr',82,246,'MNTR',OR,20); B(k,'Sel Lock',82,290,'SEL LOCK',RD,20)
K(k,'C/R Level',55,420,48,'#141414','api'); D(k,55,420,34,13); T(k,55,462,'C/R LEVEL',.26)
k=10; T(k,55,12,'CONTROL ROOM',.26)
for i,(nm,cap,col) in enumerate([('Main Spkr','MAIN SPKR',LG),('Alt 1','ALT 1',LG),('Alt 2','ALT 2',LG),('Dim','DIM',OR),('C/R Cal','C/R CAL',OR),('Mono','MONO',RD),('All Cut','ALL CUT',RD)]):
    B(k,nm,30+(i%2)*50,36+(i//2)*36,cap,col,22)
K(k,'Dim Level',80,180,20,'#141414','api'); D(k,80,180,14); T(k,80,200,'DIM LEVEL',.18)
for i,nm in enumerate(['LEFT','RIGHT','CNTR','SUR L','SUR R']): B(k,'Cut '+nm.title(),20+(i%3)*35,236+(i//3)*32,nm,RD,18)
HL(k,310); T(k,55,324,'STUDIO',.26)
for i,(nm,cap,col) in enumerate([('Stu Cut','STU CUT',RD),('Stu Ext In','EXT IN',LG),('Stu Alt Out','ALT OUT',LG)]): B(k,nm,22+i*33,350,cap,col,20)
K(k,'Studio Level',55,410,30,'#141414','api'); D(k,55,410,22); T(k,55,438,'STUDIO LEVEL',.18)
k=11; T(k,55,12,'SOLO',.26)
for i,(nm,cap,col) in enumerate([('Mix Over','MIX OVER',LG),('SIP SM','SIP SM',LG),('SIP LRG','SIP LRG',LG),('SIP Link','SIP LINK',LG),('PFL','PFL',LG),('PFL 2','PFL 2',LG),('Mom','MOM',LG),('Add','ADD',LG),('Latch','LATCH',LG),('Solo Clr','SOLO CLR',OR)]):
    B(k,nm,30+(i%2)*50,36+(i//2)*36,cap,col,22)
K(k,'Mix Over Solo',30,236,22,'#f2e31d','api'); D(k,30,236,16); T(k,30,258,'MIX OVER SOLO',.16)
K(k,'Solo Level',80,236,22,'#f2e31d','api'); D(k,80,236,16); T(k,80,258,'SOLO LEVEL',.16)
k=12; T(k,55,12,'TALKBACK',.26)
g.c.append(['p','Talkback Mic|',round((g.cx(k)+30)/g.CW,4),round((g.ry(k)+34+40)/g.CH,4),round(26/g.CW,4),'#2a2b2e','n',{'plain':True}])
K(k,'TB Mic Gain',80,40,20,'#e8e8e8','api'); D(k,80,40,14); T(k,80,60,'GAIN',.18)
K(k,'Rev Gain',30,96,18,'#e8e8e8','api'); T(k,30,114,'REV GAIN',.15); K(k,'Ext TBK Gain',80,96,18,'#e8e8e8','api'); T(k,80,114,'EXT TBK',.15)
Y(k,'Ext TBK On',80,132,None,12)
for i,nm in enumerate(['REV','STU','BUS','AUX']):
    y=166+i*48; K(k,f'{nm.title()} Level',30,y,20,'#e8e8e8','api'); D(k,30,y,14); B(k,f'{nm.title()} Talk',80,y,nm,OR,22)
B(k,'T/B All',55,370,'T/B ALL',RD,26)
master=dict(kind='Master Section',pages=pages_of(g,[('Input Select & Returns',0,2),('Aux & Multitrack',3,5),('Multitrack 13-24',6,6),('Program Masters',7,8),('Monitor & Studio',9,10),('Solo & Talkback',11,12)],len(mcols)),ks='api',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#0d0d0f',bg2='#060607',ink=INK,kc=GRN,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('API Legacy AXS',strip),('API Legacy AXS Master Section',master)]))
