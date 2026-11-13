# Generator for the FACEPLATES entries 'Neve 8424' and 'Neve 8424 Master Section' (pixel positions measured from the manual overview drawings).
# Usage: python3 tools/neve8424-gen.py > out.txt, then replace the two lines starting with  "Neve 8424  in index.html.
import sys
import json
YE='#f2d21a'; GN='#35d06a'; RD='#e8322b'; OR='#f29a1c'; INK='#f1f1ee'; GREY='#6b7078'; BLU='#2c3a8c'; DRD='#8a1422'; PUR='#5aa9e6'; BRN='#1c1c1e'; PNK='#6b7078'
LEDY='#f5c518'; LEDG='#35e06a'; GAP='#0b0c0e'
RND={'ps':'rd'}
CHM=[['+10',1],['+5',.873],['0',.779],['-5',.714],['-10',.572],['-15',.388],['-20',.279],['-30',.123],['-40',.069],['∞',0]]
MXM=[['0',1],['-5',.876],['-10',.781],['-15',.716],['-20',.577],['-25',.393],['-30',.279],['-40',.124],['-50',.065],['∞',0]]

# ================= channel strip =================
SW=88; GP=10; MG=6; TOP=30; COLH=350
CW=4*SW+3*GP+2*MG; CH=TOP+COLH+12
cols=[('Input & Cue',100),('Aux & Insert',380),('Pan & Routing',652),('Fader',0)]
def cx(k): return MG+k*(SW+GP)
d=[];c=[]
def P(k,px,py): return [round((cx(k)+px-510)/CW,4), round((TOP+py-cols[k][1])/CH,4)]
def T(k,px,py,t,sz=1,col=INK): x,y=P(k,px,py); d.append(['txt',x,y,t,sz,col])
def K(k,name,px,py,dia,col,ext=None):
    x,y=P(k,px,py); e=['k',name+'|',x,y,round(dia/CW,4),col,'n']
    if ext: e.append(ext)
    c.append(e)
def B(k,name,px,py,col,dia=24): x,y=P(k,px,py); c.append(['p',name+'|',x,y,round(dia/CW,4),col,'n'])
def L(k,name,px,py,col,dia=9): x,y=P(k,px,py); c.append(['p',name+'|',x,y,round(dia/CW,4),col,'n',RND])
def HL(k,py):
    x0=cx(k)/CW; d.append(['poly',[[x0,(TOP+py-cols[k][1])/CH],[x0+SW/CW,(TOP+py-cols[k][1])/CH]],'#9aa3ad',2])
for k in range(3): d.append(['rect',round((cx(k)+SW)/CW,4),0,round(GP/CW,4),1,GAP,GAP,0])
for k,(n,_) in enumerate(cols): d.append(['txt',round((cx(k)+SW/2)/CW,4),round(16/CH,4),n.upper(),1.05,'#c9d2dc'])
# col 0
B(0,'Dir Pre',531,131,YE); B(0,'A/B Ch IP',575,131,GN); T(0,531,152,'DIR PRE',.72); T(0,575,152,'A/B CH IP',.72); HL(0,160)
K(0,'Input Trim',538,190,44,DRD,{'ks':'marconi'})
L(0,'Trim I/P',523,227,LEDG); L(0,'Trim DIR',540,227,'#f4f4f4'); L(0,'Trim FNC',557,227,'#f4f4f4')
T(0,523,238,'I/P',.6); T(0,540,238,'DIR',.6); T(0,557,238,'FNC',.6); T(0,540,250,'TRIM',.8)
for i,(lab,col) in enumerate([('+24','#ff3b30'),('+18','#ffc21a'),('+10','#ffc21a'),('0','#3ee08a'),('-5','#3ee08a'),('-10','#3ee08a'),('-20','#3ee08a'),('SIG','#3ee08a')]):
    x,y=P(0,580,165+i*12.2); d.append(['led',x,y,round(8/CW,4),col,False]); T(0,592,165+i*12.2,lab,.55)
HL(0,258)
L(0,'Cue Pan In',528,286,LEDG); T(0,528,297,'IN',.6); K(0,'Stereo Cue Pan',572,286,38,BLU); T(0,557,308,'L',.6); T(0,587,308,'R',.6); T(0,572,318,'PAN',.75)
K(0,'Stereo Cue Send',533,347,38,GREY); L(0,'Cue Pre',561,347,LEDY); L(0,'Cue On',576,347,LEDG); L(0,'Cue I/P C / I/P A',591,347,LEDG)
T(0,561,358,'PRE',.55); T(0,576,358,'ON',.55); T(0,591,358,'I/P C',.5); T(0,591,365,'I/P A',.5); T(0,545,375,'ST CUE',.75)
# col 1
for nm,ky,side in [('Aux 3',412,1),('Aux 2',480,0),('Aux 1',546,1)]:
    kx=572 if side else 533; lx=(518,531) if side else (576,590)
    K(1,nm,kx,ky,38,PNK); L(1,nm+' Pre',lx[0],ky,LEDY); L(1,nm+' On',lx[1],ky,LEDG); T(1,lx[0],ky+11,'PRE',.55); T(1,lx[1],ky+11,'ON',.55); T(1,553,ky+29,nm.upper(),.75); HL(1,ky+36)
B(1,'Insert In',531,609,YE); B(1,'Insert I/P C',575,609,YE); T(1,531,630,'IN',.72); T(1,575,630,'I/P C',.72); T(1,553,642,'INSERT',.8)
# col 2
K(2,'Pan',544,694,42,BLU); L(2,'Pan In',590,694,LEDG); T(2,590,705,'IN',.6); T(2,525,728,'L',.6); T(2,563,728,'R',.6); T(2,544,735,'PAN',.75); HL(2,744)
B(2,'Mix',531,769,OR); B(2,'Grp Pan',575,769,YE); T(2,531,789,'MIX',.7); T(2,575,789,'GRP PAN',.7)
for nm,px,py in [('Grp 1',531,812),('Grp 2',575,812),('Grp 3',531,855),('Grp 4',575,855)]: B(2,nm,px,py,OR); T(2,px,py+20,nm.upper(),.7)
x,y=P(2,553,848); d.append(['led',x,y,round(7/CW,4),'#f4f4f4',False]); T(2,553,860,'CUE',.5); HL(2,900)
B(2,'Solo',531,950,OR); B(2,'Cut',575,950,RD); x,y=P(2,553,940); d.append(['led',x,y,round(7/CW,4),'#3ee08a',False]); T(2,553,930,'ISO',.55); T(2,531,971,'SOLO',.8); T(2,575,971,'CUT',.8)
# col 3 fader
fx=(cx(3)+34)/CW; fy=(TOP+COLH/2+4)/CH; fr=300/8.46/CW
c.append(['f','Fader|',round(fx,4),round(fy,4),round(fr,4),'#3b3f45','n',{'vert':True,'marks':CHM,'zero':.779,'dbLabel':False}])
d.append(['txt',round((cx(3)+SW/2)/CW,4),round((TOP+COLH+2)/CH,4),'Neve',1.0,'#e8322b'])
pages=[[n,round((cx(k)-(MG if k==0 else GP/2))/CW,4),0,round((cx(k)+SW+(MG if k==3 else GP/2))/CW,4),1] for k,(n,_) in enumerate(cols)]
strip=dict(kind='Channel Strip',pages=pages,ks='nevecap',ps='sq',ar=round(CW/CH,4),bare=True,noTicks=True,bg='#39424c',bg2='#2a323b',ink=INK,kc=GREY,fs=17,brand='',model='',tx=.5,ty=.03,deco=d,c=c)

# ================= master section =================
MW=594; MH=1070
d=[];c=[]
def X(px): return round((px-272)/MW,4)
def Y(py): return round((py-230)/MH,4)
def T(px,py,t,sz=1,col=INK): d.append(['txt',X(px),Y(py),t,sz,col])
def K(name,px,py,dia,col,ext=None):
    e=['k',name+'|',X(px),Y(py),round(dia/MW,4),col,'n']
    if ext: e.append(ext)
    c.append(e)
def B(name,px,py,col,dia=15): c.append(['p',name+'|',X(px),Y(py),round(dia/MW,4),col,'n'])
def L(name,px,py,col,dia=7): c.append(['p',name+'|',X(px),Y(py),round(dia/MW,4),col,'n',RND])
def LED(px,py,col,on=False,dia=6.5): d.append(['led',X(px),Y(py),round(dia/MW,4),col,on])
def LN(pts,w=2): d.append(['poly',[[X(a),Y(b)] for a,b in pts],'#9aa3ad',w])
# frame lines
LN([(272,400),(710,400)]); LN([(272,540),(710,540)]); LN([(403,400),(403,540)]); LN([(533,400),(533,540)]); LN([(606,400),(606,838)]); LN([(710,258),(710,838)]); LN([(710,540),(866,540)])
LN([(710,258),(866,258)]); LN([(788,258),(788,540)]); LN([(710,458),(866,458)]); LN([(272,838),(866,838)],3)
for x in (337.5,403,468.5,534): LN([(x,540),(x,838)],1)
LN([(272,655),(606,655)],1); LN([(272,722),(606,722)],1); LN([(606,785),(710,785)],1)
d.append(['rect',X(272),Y(838),1,round(10/MH,4),GAP,GAP,0])
LN([(272,898),(866,898)],1); LN([(272,952),(866,952)],1)
# meters
d.append(['vu',X(281),Y(255),round(170/MW,4),round(84/MH,4),{'label':'VU'}]); d.append(['vu',X(530),Y(255),round(170/MW,4),round(84/MH,4),{'label':'VU'}])
T(365,349,'LEFT',.8); T(615,349,'RIGHT',.8); T(365,381,'Neve',3.0,'#f1f1ee'); T(615,381,'8424',2.8,'#c9d2dc')
T(468,274,'⠿',1.6,'#111'); T(468,293,'TB MIC',.55); K('TB Level',509,274,22,GREY); T(509,293,'TB LEVEL',.55); T(490,303,'+4 OSC',.5)
for i,(nm,lab) in enumerate([('Meter Mix','MIX'),('Meter G1/2','G1/2'),('Meter G3/4','G3/4'),('Meter Aux 1/2','AUX 1/2'),('Meter Aux 3','AUX 3'),('Meter Mon','MON'),('Meter Cue','CUE'),('Meter Rev 1','REV 1'),('Meter Rev 2','REV 2')]):
    px=465+25*(i%3); py=316+28*(i//3); B(nm,px,py,YE); T(px,py+14,lab,.55)
T(490,396,'METER SEL',.6)
# reverb returns
for n,ox in ((1,0),(2,130.7)):
    K(f'Rev {n} Level',299+ox,419,26,GREY); L(f'Rev {n} On',331+ox,419,LEDG); L(f'Rev {n} Iso',342+ox,419,LEDG); T(331+ox,428,'ON',.5); T(342+ox,428,'ISO',.5); T(299+ox,438,'LEVEL',.6)
    K(f'Rev {n} To Cue',376+ox,419,26,GREY); T(376+ox,438,'TO CUE',.6); L(f'Rev {n} To Cue On',372+ox,450,LEDG); T(383+ox,451,'ON',.5)
    K(f'Rev {n} Bal',336+ox,469,30,BLU); L(f'Rev {n} Bal In',303+ox,469,LEDG); T(303+ox,478,'IN',.5); T(322+ox,490,'L',.5); T(350+ox,490,'R',.5); T(336+ox,496,'BAL',.6)
    for i,lab in enumerate(['MIX','GRP 1/2','GRP 3/4','AFL']): B(f'Rev {n} '+lab.title(),300+ox+25*i,512,YE); T(300+ox+25*i,526,lab,.5)
    T(336+ox,535,f'REV RETURN {n}',.6)
# headphone 2 + global
K('Headphone 2 Level',570,419,26,PNK); T(570,439,'LEVEL',.6)
for i,lab in enumerate(['MIX','EXT','MON','CUE','AUX 2/3']): L('HP2 '+lab,547+11.5*i,449,LEDY,6.5); T(547+11.5*i+(1.5 if i==4 else 0),457,lab,.34 if i<4 else .28)
T(570,466,'HEADPHONE 2',.6)
for i,(nm,lab,col) in enumerate([('Solo Safe','SOLO SAFE',OR),('Reset','RESET',OR),('48 Mix','48 MIX',OR),('Aux On/Pre','AUX ON/PRE',GN),('IPC Mtr','IPC MTR',OR),('Master A/B Ch IP','A/B CH IP',GN)]):
    px=545+24.5*(i%3); py=482+28*(i//3); B(nm,px,py,col); T(px,py+14,lab,.38)
T(570,535,'MASTER',.6)
# aux & cue masters
for nm,px,py in [('Aux 3',628,419),('Cue',688,419),('Aux 1',628,484),('Aux 2',688,484)]:
    K(nm+' Master',px,py,26,GREY); T(px,py+18,nm.upper(),.6); lx=651 if px<650 else 665; L(nm+' Master On',lx,py,LEDG); T(lx,py+9,'ON',.45)
    B(nm+' AFL',px,py+33,YE); T(650 if px<650 else 666,py+33,'AFL',.5)
T(658,535,'AUX & CUE MASTERS',.55)
# groups & mix
for g in range(5):
    ox=65.4*g; nm='Mix' if g==4 else f'Grp {g+1}'
    T(284+ox,546,nm.upper(),.5)
    hx=(584 if g==4 else 318+ox); lx=(557 if g==4 else 291+ox); ex=(587 if g==4 else 322+ox)
    K(nm+' EQ HF',hx,575,22,PUR); T(hx,591,'− 10k +',.46); K(nm+' EQ LF',lx,622,24,BRN); T(lx,640,'− 220 +',.46); L(nm+' EQ In',ex,622,LEDG); T(ex,631,'EQ IN',.42)
    if g<4:
        K(nm+' Pan',298+ox,685,30,BLU); L(nm+' Pan In',332+ox,685,LEDG); T(332+ox,694,'IN',.45); T(285+ox,706,'L',.5); T(311+ox,706,'R',.5); T(298+ox,713,'PAN',.55)
        labs=[('Mix L','MIX L'),('Mix R','MIX R'),('500-1','500-1'),('500-2','500-2'),('Ins In','INS IN'),('Pre','PRE')]; bx=(288+ox,321+ox)
    else:
        K('Width',556,685,24,PNK); L('Width In',587,685,LEDG); T(587,694,'IN',.45); T(556,713,'WIDTH',.55)
        labs=[('M Bus Inj L','M BUS INJ L'),('M Bus Inj R','M BUS INJ R'),('500 1/2','500 1/2'),('Cue Bus','CUE BUS'),('Ins In','INS IN'),('Pre','PRE')]; bx=(554,586)
    for i,(a,lab) in enumerate(labs): px=bx[i%2]; py=739+29.5*(i//2); B(nm+' '+a,px,py,OR); T(px,py+13.5,lab,.4 if g<4 else .34)
# control room
for i,(a,lab) in enumerate([('CR Mix','MIX'),('CR Ext','EXT'),('CR i-MON','i-MON')]): B(a,627+30.5*i,557,OR); T(627+30.5*i,570.5,lab,.5)
T(658,579,'CONTROL ROOM SOURCE',.5)
LED(658,588,'#ffc21a'); T(658,596,'AFL/PFL',.42); L('PFL',658,606,LEDG,6.5); T(658,613,'PFL',.42); K('TB Dim',658,620.5,7,'#b08a3c',{'ks':'trim'}); T(658,628,'TB DIM',.36)
K('AFL/PFL Level',628,607,24,PNK); T(628,627,'AFL/PFL',.5); K('Dim Level',688,607,24,DRD); T(688,627,'DIM',.5)
K('Monitor Level',658,666,52,RD); T(658,702,'MONITOR LEVEL',.55)
for i,(a,lab,col) in enumerate([('CR Cut','CUT',RD),('CR Dim','DIM',OR),('CR Mono','MONO',OR),('Speaker A','A',OR),('Speaker M1','M1',OR),('Speaker M2','M2',OR)]):
    px=627+30.5*(i%3); py=722+31*(i//3); B(a,px,py,col); T(px,py+13.5,lab,.5)
T(658,780,'CONTROL ROOM MONITOR',.5)
K('M1 Trim',673,738,6,'#b08a3c',{'ks':'trim'}); K('M2 Trim',702,738,6,'#b08a3c',{'ks':'trim'})
for nm,px in [('TB Ext Trim',611),('Cue TB Trim',640),('Slate TB Trim',670),('RTB Trim',701)]: K(nm,px,787.5,6,'#b08a3c',{'ks':'trim'})
T(611,794,'TB',.3)
for i,(a,lab) in enumerate([('Cue TB','CUE TB'),('Slate TB','SLATE TB'),('RTB','RTB')]): B(a,627+30.5*i,800,YE); T(627+30.5*i,814,lab,.5)
# 1073 preamps & DI
for n,ox in ((1,0),(2,79)):
    LED(723+ox,265,'#3ee08a'); T(723+ox,273,'SIG',.45)
    K(f'Mic Pre {n} Gain',749+ox,310,46,DRD,{'ks':'marconi','sweep':[-150,165]})
    d.append(['scale',X(749+ox),Y(310),round(33/MW,4),['30','40','50','OFF','60','70','80'],.42,INK,-150,0])
    d.append(['scale',X(749+ox),Y(310),round(33/MW,4),['+20','+10','0','-10','OFF','20'],.42,INK,35,165])
    T(776+ox,277,'dB',.45); T(721+ox,345,'MIC',.5); T(776+ox,345,'LINE',.45)
    K(f'Mic Pre {n} Trim',749+ox,367,24,GREY); T(749+ox,386,'TRIM',.55); T(735+ox,381,'-20',.36); T(763+ox,381,'+5',.36); LED(775+ox,352,'#3ee08a'); T(775+ox,360,f'TO CH {16+n}',.4)
    for i,(a,lab,col) in enumerate([('Phase','Ø',YE),('Lo Z','Lo Z',YE),('+48V','+48V',RD)]): B(f'Mic Pre {n} '+a,723+ox+25*i,403,col); T(723+ox+25*i,417,lab,.5)
    for i,lab in enumerate(['500-1','500-2']): B(f'Mic Pre {n} '+lab,736+ox+25*i,430,YE); T(736+ox+25*i,444,lab,.5)
    T(719+ox,453,'1073',.45); T(766+ox,453,f'MIC PRE {n}',.5)
    LED(723+ox,468,'#3ee08a'); T(723+ox,476,'SIG',.45); K(f'DI {n} Level',749+ox,480,24,GREY); T(749+ox,499,'LEVEL',.55); T(735+ox,494,'-20',.36); T(763+ox,494,'+5',.36); LED(775+ox,466,'#3ee08a'); T(775+ox,474,f'TO CH {18+n}',.4)
    for i,lab in enumerate(['-25','500-1','500-2']): B(f'DI {n} '+lab,723+ox+25*i,512,YE); T(723+ox+25*i,526,lab,.5)
    T(749+ox,535,f'INSTRUMENT DI {n}',.5)
d.append(['rect',X(716),Y(548),round(144/MW,4),round(232/MH,4),'#20262d','#566370',4]); T(788,664,'500 SERIES',.9,'#8794a1'); T(749,832,'500-1',.45); T(827,832,'500-2',.45)
# lower panel
for g in range(4):
    ox=65.4*g; B(f'Grp {g+1} Solo',288+ox,881,YE,14); B(f'Grp {g+1} Cut',321+ox,881,RD,14); LED(305+ox,876,'#3ee08a'); T(305+ox,868,'ISO',.42); T(288+ox,894,'SOLO',.5); T(321+ox,894,'CUT',.5)
    c.append(['f',f'Grp {g+1} Fader|',X(305+ox),Y(1122),.0468,'#3b3f45','n',{'vert':True,'marks':CHM,'zero':.779,'dbLabel':False}]); T(305+ox,964,f'GRP {g+1}',.6)
B('Mix Cut',570,881,RD,14); T(570,894,'CUT',.5)
c.append(['f','Mix Fader|',X(571),Y(1122),.0468,'#3b3f45','n',{'vert':True,'marks':MXM,'zero':1,'dbLabel':False}]); T(571,964,'MIX',.6)
d.append(['rect',X(662),Y(903),round(113/MW,4),round(22/MH,4),'#7fd9e6','#1a1d21',4])
for nm,px,lab in [('Screen Home',616,'⌂'),('Screen Back',640,'◀'),('Screen Next',795,'▶'),('Screen Enter',819,'↵'),('Screen Ctrl',843,'CTRL')]: B(nm,px,914,YE,14); T(px,930,lab,.5)
T(716,936,'SERVICES',.5)
T(290,1285,'Neve',1.2,'#e8322b')
mpages=[['Meter & Returns',0,0,.745,.292],['1073 & DI',.73,.02,1,.292],['Gruppen & Mix',0,.285,.57,.572],['Control Room',.555,.285,1,.572],['Fader',0,.575,1,1]]
master=dict(kind='Master Section',pages=mpages,ks='nevecap',ps='sq',ar=round(MW/MH,4),bare=True,noTicks=True,bg='#39424c',bg2='#2a323b',ink=INK,kc=GREY,fs=16,brand='',model='',tx=.5,ty=.03,deco=d,c=c)
out=''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Neve 8424',strip),('Neve 8424 Master Section',master)])
sys.stdout.write(out)
names=[x[1] for x in c]; assert len(names)==len(set(names)), [n for n in names if names.count(n)>1]
names=[x[1] for x in strip['c']]; assert len(names)==len(set(names))

