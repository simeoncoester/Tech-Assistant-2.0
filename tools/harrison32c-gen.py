# Generator for 'Harrison 32Classic' (channel strip) and 'Harrison 32Classic Master Section'
# after the official Harrison "32Classic Manual / User Guide" (April 2024; figures 2-16: input, aux, EQ, routing, fader,
# mix bus masters 1-2/3-4/5-6 with cue/matrix, 7-8 with aux/return master and talkback, master module).
# The 32Classic is the current reissue of the classic Harrison 32C (EQ and filters identical). Light grey panel, black outline print.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
INK='#16181b'; KB='#202226'; SB='#e8e8e6'; RD='#d8352c'; BL='#2f6fc4'; GY='#8f9398'
FM=[[l,round(1-(y-158)/779,3)] for l,y in [('10',158),('5',254),('0',351),('5',447),('10',523),('20',619),('30',696),('40',792),('60',897),('∞',937)]]
MF=[['10',1],['5',.85],['0',.7],['5',.55],['10',.43],['20',.28],['30',.16],['40',.07],['60',.02],['∞',0]]
def kit(g):
    K,B,SC,HL,LED,F=g.K,g.B,g.SC,g.HL,g.LED,g.F
    T=lambda k,x,y,t,sz=.5,col=INK: g.T(k,x,y,t,min(.62,sz*2.3),col)
    for e in g.d:
        if e[0]=='txt' and e[5]=='#c9d2dc': e[5]=INK
    def TK(k,x,y,r,n=11): g.d.append(['ticks',round((g.cx(k)+x)/g.CW,4),round((g.ry(k)+34+y)/g.CH,4),round(r/g.CW,4),n,INK,-140,140,.22,True])
    def KN(k,name,x,y,dia,lo=None,hi=None,mid=None,lab=None,labs=None):
        K(k,name,x,y,dia,KB,'round'); TK(k,x,y,dia*.62)
        if labs: SC(k,x,y,dia*.62+8,labs,.24)
        if lo: T(k,x-dia*.55,y+dia*.5+7,lo,.22)
        if hi: T(k,x+dia*.55,y+dia*.5+7,hi,.22)
        if mid: T(k,x+dia*.3,y-dia*.5-5,mid,.22)
        if lab: T(k,x+dia*.62+4,y+3,lab,.26)
    def SW(k,name,x,y,lab=None,dia=13,led=True,col=SB):
        B(k,name,x,y,None,col,dia)
        if led: LED(k,x-dia*.5-7,y,'#ff4433',4)
        if lab: T(k,x,y+dia*.5+9,lab,.17)
    return K,B,SC,HL,LED,F,T,KN,SW,TK

cols=['Input & Stereo Aux','Aux & EQ','Filter & Routing','Fader']
g=build(cols,110,600,.6)
K,B,SC,HL,LED,F,T,KN,SW,TK=kit(g)
k=0; T(k,55,14,'32CLASSIC',.36)
T(k,55,34,'RETURN',.24); SW(k,'Return L',26,50,None); SW(k,'Return R',84,50,None); T(k,26,66,'L',.2); T(k,84,66,'R',.2)
HL(k,70)
SW(k,'Inline',30,88,None); T(k,18,74,'INLINE',.2); SW(k,'48V',84,88,'48v')
KN(k,'Mic Trim',32,128,26,None,None,None); T(k,44,152,'MIC',.18); T(k,14,152,'+20',.18); T(k,54,104,'+70',.16)
SW(k,'-20',84,120,'-20'); SW(k,'Phase',84,146,'Ø')
KN(k,'Line Trim',32,186,26,'-6',None); T(k,48,166,'+6',.18); T(k,46,206,'LINE',.18); LED(k,62,170,'#35d06a',8); T(k,80,172,'INPUT',.24)
SW(k,'Inst',84,194,'INST')
SW(k,'Trim',30,226,None); T(k,14,214,'TRIM',.18); SW(k,'Input Playback',84,226,'PLAY')
SW(k,'Line',30,256,None); T(k,14,244,'LINE',.18); SW(k,'Ins',84,256,'INS')
HL(k,276)
KN(k,'Stereo Aux Pan',32,306,24,'L','R'); SW(k,'Stereo Aux Playback',84,300,'PLAY')
SW(k,'Stereo Aux Pre',84,330,'PRE')
KN(k,'Stereo Aux Level',32,366,24,'off','+10','0'); SW(k,'Stereo Aux On',84,364,'ST AUX')
k=1
for i in range(4):
    n=i+1; y=24+i*62
    KN(k,f'Aux {n}',32,y+10,24,'off','+10','0'); T(k,62,y+2,str(n),.26)
    if n in (1,3): SW(k,f'Aux {n}-{n+1} Pre',84,y-2,'PRE')
    SW(k,f'Aux {n} On',84,y+24,str(n))
T(k,86,272,'AUX',.36); HL(k,284)
for i,(nm,labs,lo,hi) in enumerate([('Hi',['6k'],'900','13k'),('Hi Mid',['2.8'],'400','6k'),('Lo Mid',['1.4'],'200','3.1'),('Lo',['280'],'40','600')]):
    y=312+i*70
    KN(k,f'{nm} Freq',30,y,24,lo,hi,None,None); T(k,30,y-18,labs[0],.2); T(k,58,y+4,nm.upper(),.22)
    KN(k,f'{nm} Gain',82,y+28,22,'-10','+10','0')
    if nm in ('Hi','Lo'): SW(k,f'{nm} Bell',84,y-16,'∩',13)
k=2
KN(k,'LP',32,34,26,'160','20k','6k',None); T(k,62,38,'LP',.26)
KN(k,'HP',32,96,26,'25','3.15','1.6',None); T(k,62,100,'HP',.26)
SW(k,'EQ',84,70,'EQ',16); SW(k,'Flt',84,104,'FLT',16)
HL(k,128)
for i,(a,b) in enumerate([(1,2),(3,4),(5,6),(7,8)]):
    y=150+i*30; SW(k,f'Bus {a}',30,y,None,15,False); T(k,14,y+3,f'{a}L',.2); LED(k,48,y,'#ff4433',4)
    SW(k,f'Bus {b}',80,y,None,15,False); LED(k,62,y,'#ff4433',4); T(k,96,y+3,f'R{b}',.2)
T(k,55,262,'BUS',.3)
KN(k,'Pan',34,300,30,'L','R'); SW(k,'Bus Pan',84,288,'BUS PAN')
LED(k,64,326,'#2f8ff0',6); T(k,84,329,'PLAYBACK',.18)
SW(k,'Pan On',30,360,None); T(k,14,348,'PAN',.18); SW(k,'Main Mix',84,360,'MAIN MIX',15,True,'#e04a3a')
SW(k,'0 dB',30,392,None); T(k,14,380,'0 dB',.18); SW(k,'Solo',84,392,'SOLO')
k=3
B(k,'Mute',55,40,'32',SB,30)
g.d.append(['leds',round((g.cx(k)+22)/g.CW,4),round((34+90)/g.CH,4),round((g.cx(k)+22)/g.CW,4),round((34+250)/g.CH,4),20,round(4.5/g.CW,4),'#35d06a',0,'#ff4433'])
for v,y in [('PK',84),('11',94),('0',150),('20',214),('35',250)]: T(k,10,y,v,.18)
F(k,'Fader',66,90,580,FM,round(1-(351-158)/779,3))
strip=dict(kind='Channel Strip',pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#ecece9',bg2='#d9d9d6',ink=INK,kc=KB,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

mcols=['Cue/Matrix 1','Bus 1-2','Cue/Matrix 2','Bus 3-4','Cue/Matrix 3','Bus 5-6','Aux & Return Master','Bus 7-8','Master Module','Main Mix & Monitors']
g=build(mcols,110,600,.4,5)
K,B,SC,HL,LED,F,T,KN,SW,TK=kit(g)
def CUE(k,n):
    KN(k,f'Cue {n} Level',32,40,24,'off','+10','0'); B(k,f'Cue {n} Mute',84,40,str(n),SB,24); T(k,84,64,'MUTE',.2)
    T(k,36,88,'CUE/MATRIX OUTPUT',.16); SW(k,f'Cue {n} 0dB',84,84,'0 dB')
    SW(k,f'Cue {n} Dante',84,116,'DANTE')
    KN(k,f'Cue {n} Ret Mtx Level',32,150,22,'off','+10'); SW(k,f'Cue {n} Ret Mtx',84,146,'RET MTX')
    KN(k,f'Cue {n} Ster Aux Level',32,200,22,'off','+10'); SW(k,f'Cue {n} Ster Aux',84,196,'ST AUX')
    for i in range(4): KN(k,f'Cue {n} Aux {i+1} Level',32,250+i*46,22,'off','+10'); SW(k,f'Cue {n} Aux {i+1}',84,246+i*46,f'AUX {i+1}')
    for i,(a,b) in enumerate([('BUS 1-2','BUS 3-4'),('BUS 5-6','BUS 7-8'),('EXT 2','MAIN MIX'),('EXT 1','SOLO')]):
        y=446+i*28; SW(k,f'Cue {n} {a.title()}',24,y,None,13); T(k,24,y+14,a,.14); SW(k,f'Cue {n} {b.title()}',84,y,None,13); T(k,84,y+14,b,.14)
    SW(k,f'Cue {n} Talk',84,562,'TALK',13,False); T(k,40,565,'CUE / MATRIX',.18)
def BUS(k,a,b):
    for j,n in enumerate((a,b)):
        x=28+j*54
        g.d.append(['leds',round((g.cx(k)+x-12)/g.CW,4),round((g.ry(k)+34+16)/g.CH,4),round((g.cx(k)+x-12)/g.CW,4),round((g.ry(k)+34+120)/g.CH,4),16,round(4/g.CW,4),'#35d06a',0,'#ff4433'])
        KN(k,f'Bus {n} Pan',x,150,22,'L','R')
        for i,nm in enumerate(['PAN','INS','0 dB','MAIN MIX','SOLO']): B(k,f'Bus {n} {nm.title()}'+(' On' if nm=='PAN' else ''),x,192+i*26,None,SB,13); T(k,x,204+i*26,nm,.13)
        B(k,f'Bus {n} Mute',x,332,str(n),SB,20)
        F(k,f'Bus {n} Fader',x,370,590,FM,round(1-(351-158)/779,3))
for k,(n,a,b) in enumerate([(1,1,2),(2,3,4),(3,5,6)]): CUE(2*k,n); BUS(2*k+1,a,b)
k=6
for j,lab in enumerate(['RETURN MASTER','']):
    y0=20+j*156
    KN(k,f'{"Return" if j==0 else "Return 2"} R Level',30,y0+20,22,'off','+10','0',); T(k,52,y0+24,'R',.2)
    KN(k,f'{"Return" if j==0 else "Return 2"} L Level',30,y0+76,22,'off','+10','0'); T(k,52,y0+80,'L',.2)
    for i,nm in enumerate(['MUTE','MAIN MIX','SOLO' if j==0 else 'STER AUX']): SW(k,f'Return {j+1} {nm.title()}',84,y0+14+i*28,None,13); T(k,84,y0+26+i*28,nm,.13)
    if lab: T(k,55,y0+126,lab,.22)
HL(k,330); T(k,55,344,'AUX MASTER',.22)
for i in range(4): KN(k,f'Aux Master {i+1}',30,372+i*46,20,'off','+10'); SW(k,f'Aux Master {i+1} Solo',84,366+i*46,f'SOLO {i+1}',13)
k=7; BUS(k,7,8)
KN(k,'Talkback Level',30,560,18,'MIN','MAX'); B(k,'All Talk',90,566,None,SB,14); T(k,90,582,'ALL TALK',.14)
g.c.append(['p','Talkback Mic|',round((g.cx(k)+55)/g.CW,4),round((g.ry(k)+34+500)/g.CH,4),round(14/g.CW,4),'#2a2b2e','n',{'plain':True}])
k=8
T(k,55,14,'METER MODE',.24)
for i,nm in enumerate(['DANTE STATUS','DANTE STATUS 2']): LED(k,30,34+i*16,'#35d06a',5); T(k,66,37+i*16,nm.replace(' 2',''),.16)
for i,nm in enumerate(['LIGHT SHOW','PEAK HOLD','CLEAR']): B(k,nm.title(),24,80+i*28,None,SB,14); T(k,64,83+i*28,nm,.16)
HL(k,170); T(k,55,182,'INSTRUMENT/ INPUT',.2)
g.c.append(['p','Instrument Input|',round((g.cx(k)+70)/g.CW,4),round((g.ry(k)+34+212)/g.CH,4),round(22/g.CW,4),'#1b1c1f','n',{'plain':True}])
SW(k,'Inst Mic',84,252,'MIC'); SW(k,'Inst -20',84,278,'-20'); KN(k,'Inst Gain',30,284,24,'MIN','MAX'); SW(k,'Inst 48V',84,304,'48v'); SW(k,'Inst Main Mix',84,330,'MAIN MIX')
HL(k,352); T(k,55,364,'MAIN MIX MODES',.2)
for i,nm in enumerate(['INS','0 dB','SURROUND']): SW(k,'Main Mix '+nm.title(),84,384+i*28,nm)
HL(k,470); T(k,55,484,'MONITOR SOURCE',.2)
for i,nm in enumerate(['MUTE L','MUTE R','MONO','DIM']): SW(k,'Mon '+nm.title(),30+(i%2)*54,508+(i//2)*30,None,13); T(k,30+(i%2)*54,522+(i//2)*30,nm,.13)
k=9
KN(k,'Dim Level',30,40,22,'-20','-6',None,None); T(k,30,64,'DIM',.18)
KN(k,'Phones',30,96,22,'off','0'); T(k,30,120,'PHONES',.16)
KN(k,'Alt Level',30,152,22,'off','0'); T(k,30,176,'ALT',.16)
for i,nm in enumerate(['DANTE','SUR','EXT 1','EXT 2','MAIN MIX','ALT']): SW(k,'Source '+nm.title(),84,30+i*26,nm,13)
LED(k,66,186,'#ffb020',5); T(k,84,189,'SOLO',.16)
g.d.append(['leds',round((g.cx(k)+20)/g.CW,4),round((g.ry(k)+34+206)/g.CH,4),round((g.cx(k)+20)/g.CW,4),round((g.ry(k)+34+330)/g.CH,4),22,round(4/g.CW,4),'#35d06a',0,'#ff4433'])
g.d.append(['leds',round((g.cx(k)+32)/g.CW,4),round((g.ry(k)+34+206)/g.CH,4),round((g.cx(k)+32)/g.CW,4),round((g.ry(k)+34+330)/g.CH,4),22,round(4/g.CW,4),'#35d06a',0,'#ff4433']); T(k,26,342,'MAIN MIX',.16)
F(k,'Main Mix Fader',76,210,470,MF,.7,'#e04a3a')
KN(k,'Monitor Level',40,520,34,'off','0'); B(k,'Monitor Mute',88,524,'MUTE',SB,20); T(k,55,570,'MONITORS',.22)
master=dict(kind='Master Section',pages=pages_of(g,[('Cue/Matrix & Bus 1-2',0,1),('Cue/Matrix & Bus 3-6',2,4),('Bus 5-8 & Aux',5,7),('Master Module',8,9)],len(mcols)),ks='round',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#ecece9',bg2='#d9d9d6',ink=INK,kc=KB,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Harrison 32Classic',strip),('Harrison 32Classic Master Section',master)]))
