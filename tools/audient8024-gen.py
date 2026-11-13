# Generator for the FACEPLATES entries 'Audient ASP8024-HE' (channel strip) and 'Audient ASP8024-HE Master Section'.
# Source: user's "ASP8024-HE Product Brochure" (page 10 channel strip picture, page 3 VCA bus compressor, feature texts pages 3/7/8).
# The building helpers come from tools/ssl4000eg-gen.py (everything before its channel strip part).
# Usage: python3 tools/audient8024-gen.py > out.txt, then replace the two lines starting with  "Audient ASP8024-HE  in index.html.
import os, sys, json
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl4000eg-gen.py')).read()
exec(src[:src.index('# ================= channel strip')])
BLU='#2f63b8'; PNK='#c4406e'; BK='#1d1e21'; GY='#8f9398'; DK='#3a3d42'
SF=[['10',1],['5',.777],['0',.642],['5',.496],['10',.379],['20',.231],['40',.098],['∞',0]]

# ================= channel strip =================
cols=['Bus Routing','Aux & EQ','Mitten & SF Pan','Short Fader','Long Fader']
g=build(cols,100,600,.75)
T,K,B,SC,DOT,HL,LED,F=g.T,g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
def AUX(k,n,x,y,col=GY):
    K(k,f'Aux {n}' if n.isdigit() else f'Cue {n}',x,y,26,col); DOT(k,x,y,18); T(k,x-16,y+22,'∞',.34); T(k,x+16,y+22,'0',.3); T(k,x,y+24,'dB',.24); T(k,x+27,y+4,'→ '+n,.4)
def PAIR(k,a,b,y0,lab,cue=False):
    pre='Cue' if cue else 'Aux'
    AUX(k,a,30,y0); AUX(k,b,30,y0+64)
    B(k,f'{pre} {a}-{b} SF',84,y0-12,'SF',WH,18); B(k,f'{pre} {a}-{b} Pre',84,y0+16,'PRE',DK,18); T(k,84,y0+38,'CUE' if cue else 'AUX',.3)
    B(k,f'{pre} {a}-{b} '+('SF B' if cue else 'Link'),84,y0+64,'SF' if cue else lab,WH,18)
k=0
for i in range(12):
    r,c=divmod(i,4); x=16+c*23; y=26+r*52
    B(k,f'Bus {i+1}/{i+13}',x,y,None,WH,16); T(k,x,y+19,str(i+1),.36); g.d.append(['rect',round((g.cx(k)+x-8)/g.CW,4),round((34+y+23)/g.CH,4),round(16/g.CW,4),round(11/g.CH,4),'#d5d7da','none',2]); T(k,x,y+32,str(i+13),.32,'#1d1f22')
B(k,'+12 Shift',18,186,None,WH,18); T(k,18,170,'+12',.3); T(k,18,206,'SHIFT',.3)
B(k,'Follow Pan',52,186,None,DK,18); T(k,52,170,'FOLLOW',.3); T(k,52,206,'PAN',.3)
B(k,'Routing LF',84,186,None,WH,18); T(k,84,206,'LF',.34); HL(k,222)
PAIR(k,'1','2',254,'7-8'); PAIR(k,'3','4',394,'9-10')
k=1
PAIR(k,'5','6',26,'11-12'); PAIR(k,'A','B',160,None,True)
HL(k,262); T(k,50,276,'EQUALISER',.36)
B(k,'HF/LF In',20,298,'IN',WH,18); T(k,52,302,'>-<',.4); B(k,'HF/LF SF',84,298,'SF',WH,18)
B(k,'Air',22,342,None,DK,16); T(k,22,328,'AIR',.3); T(k,22,362,'HF',.5)
K(k,'HF dB',68,354,34,BLU); DOT(k,68,354,24); T(k,58,384,'dB',.26); T(k,86,384,'±15',.26)
B(k,'100Hz',22,418,None,DK,16); T(k,22,404,'100Hz',.28); T(k,22,438,'LF',.5)
K(k,'LF dB',68,430,34,PNK); DOT(k,68,430,24); T(k,58,460,'dB',.26); T(k,86,460,'±15',.26)
HL(k,478); B(k,'HMF/LMF In',20,500,'IN',WH,18); T(k,52,504,'-0-0-',.36); B(k,'HMF/LMF SF',84,500,'SF',WH,18)
k=2
K(k,'HMF kHz',40,40,26,BLU,'ssl',{'sweep':[-140,140]}); SC(k,40,40,19,['0.45','0.7','3.2','7.5','20'],.27,-140,140); T(k,40,66,'kHz',.26); T(k,84,56,'HMF',.55)
K(k,'HMF BW',24,104,24,BLU); DOT(k,24,104,17); T(k,24,124,'BW',.26)
K(k,'HMF dB',70,112,34,BLU); DOT(k,70,112,24); T(k,60,142,'dB',.26); T(k,88,142,'±15',.26)
HL(k,152)
K(k,'LMF Hz',40,190,26,PNK,'ssl',{'sweep':[-140,140]}); SC(k,40,190,19,['50','75','175','750','1k5'],.27,-140,140); T(k,40,216,'Hz',.26); T(k,84,206,'LMF',.55)
K(k,'LMF BW',24,254,24,PNK); DOT(k,24,254,17); T(k,24,274,'BW',.26)
K(k,'LMF dB',70,262,34,PNK); DOT(k,70,262,24); T(k,60,292,'dB',.26); T(k,88,292,'±15',.26)
HL(k,304)
B(k,'Copy LF',22,336,None,WH,18); T(k,22,318,'COPY LF',.28); T(k,66,320,'MIC',.32,'#ff4a3d'); T(k,66,334,'TAPE',.32); T(k,22,362,'↓ SOURCE',.28)
K(k,'SF Pan',62,392,30,BK); DOT(k,62,392,21); T(k,48,418,'L',.3); T(k,76,418,'R',.3); T(k,62,368,'PAN',.28)
B(k,'SF Mix',86,436,'MIX',WH,18)
k=3
F(k,'Short Fader',28,40,380,SF,.642)
B(k,'SF Solo',78,250,'SOLO',WH,24); B(k,'SF Cut',78,296,'CUT',WH,24)
g.d.append(['rect',round((g.cx(k)+8)/g.CW,4),round((34+404)/g.CH,4),round(84/g.CW,4),round(30/g.CH,4),'#c9ccd0','none',4])
B(k,'Ch Flip',24,500,None,WH,18); T(k,24,520,'CH FLIP',.28); T(k,68,494,'TAPE',.32,'#7fd34a'); T(k,68,510,'MIC',.32)
k=4
K(k,'LF Pan',34,46,32,BK); DOT(k,34,46,22); T(k,20,74,'L',.3); T(k,48,74,'R',.3); T(k,72,40,'PAN',.28)
B(k,'LF Mix',84,62,'MIX',WH,18)
B(k,'LF Solo',30,118,'SOLO',WH,24); B(k,'LF Cut',74,118,'CUT',WH,24)
g.d.append(['rect',round((g.cx(k)+8)/g.CW,4),round((34+150)/g.CH,4),round(84/g.CW,4),round(30/g.CH,4),'#c9ccd0','none',4])
F(k,'Long Fader',40,210,580,SF,.642)
pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols))
strip=dict(kind='Channel Strip',pages=pages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2a2e34',bg2='#1d2025',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)

# ================= master section =================
mcols=['VCA Bus Compressor','Mix Bus','Control Room','Talkback & Solo','Aux Masters','Bus Masters','Sub Groups 1-2','Sub Groups 3-4','Sub Groups 5-6','Sub Groups 7-8']
g=build(mcols,110,600,.5,5)
T,K,B,SC,DOT,HL,LED,F=g.T,g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
k=0
K(k,'Threshold',30,56,24,BLU); DOT(k,30,56,17); T(k,30,30,'THRESHOLD',.26); T(k,14,80,'LOWER',.22); T(k,46,80,'HIGHER',.22)
K(k,'Gain Make-Up',82,56,24,BLU); DOT(k,82,56,17); T(k,82,30,'GAIN MAKE-UP',.24); T(k,68,80,'LESS',.22); T(k,96,80,'MORE',.22)
K(k,'Attack',30,140,28,BLU,'ssl',{'sweep':[-140,140]}); SC(k,30,140,21,['0.1','0.3','1','3','10','30'],.25,-140,140); T(k,30,172,'ATTACK [mS]',.24)
K(k,'Release',82,140,28,BLU,'ssl',{'sweep':[-140,140]}); SC(k,82,140,21,['0.1','0.3','0.6','1.2','2.4','AUTO'],.24,-140,140); T(k,82,172,'RELEASE [S]',.24)
K(k,'Ratio',30,234,28,BLU,'ssl',{'sweep':[-45,45]}); SC(k,30,234,21,['2:1','4:1','10:1'],.25,-45,45); T(k,30,264,'RATIO',.26)
T(k,82,214,'BASS',.4); T(k,82,228,'EXPAND',.28); T(k,82,242,'↓',.4); B(k,'Bass Expand',82,262,None,WH,16)
B(k,'Comp In',30,310,'IN','#3d8bff',22)
k=1
B(k,'Heritage',30,40,'HERITAGE',WH,24); T(k,30,64,'RETRO IRON',.26)
B(k,'Bass Boost',30,100,'BASS',WH,22); B(k,'Treble Boost',80,100,'TREBLE',WH,22)
F(k,'Mix Fader',55,150,560,None,.642); T(k,55,580,'MIX',.4)
k=2
K(k,'Monitor Level',55,62,44,'#d6d8da','alu'); DOT(k,55,62,30,15); T(k,55,104,'MONITOR',.32)
for i,n in enumerate(['A','B','C','D']): B(k,'Speaker '+n,17+i*25,140,n,WH,18)
T(k,55,160,'SPEAKERS',.28); HL(k,172)
for i,n in enumerate(['MIX','EXT 1','EXT 2','EXT 3']): B(k,'Source '+n.title(),17+i*25,196,n,WH,18)
T(k,55,216,'SOURCE',.28); HL(k,228)
K(k,'Engineer Phones',30,268,26,GY); DOT(k,30,268,18); T(k,30,294,'PHONES',.26)
k=3
K(k,'Talkback Level',30,50,26,GY); DOT(k,30,50,18); T(k,30,76,'TALKBACK',.26)
for i,n in enumerate(['STUDIO','FOLDBACK','BUS']): B(k,'TB '+n.title(),84,30+i*30,n,WH,22)
HL(k,128)
B(k,'Solo in Front',30,160,'SOLO IN FRONT',WH,24); K(k,'Solo in Front Level',80,160,24,GY); DOT(k,80,160,17); T(k,80,184,'LEVEL',.26)
k=4
for i in range(14):
    r,c=divmod(i,2); x=30+c*50; y=28+r*60
    K(k,f'Aux Master {i+1}',x,y,22,GY); DOT(k,x,y,16); T(k,x,y+24,str(i+1),.3)
    if c==0: B(k,f'Aux Link {i+1}-{i+2}',55,y,'LINK',DK,12)
for i,n in enumerate(['A','B']): K(k,f'Cue {n} Master',30+i*50,452,24,BK); DOT(k,30+i*50,452,17); T(k,30+i*50,478,f'CUE {n}',.28)
k=5
for i in range(24):
    r,c=divmod(i,3); x=22+c*33; y=28+r*60
    K(k,f'Bus Master {i+1}',x,y,20,GY); DOT(k,x,y,14); T(k,x,y+22,str(i+1),.3)
for j in range(4):
    k=6+j
    for i in range(2):
        x=30+i*50; n=1+2*j+i
        T(k,x,14,str(n),.4)
        K(k,f'Sub Group {n} Pan',x,46,22,BK); DOT(k,x,46,15); T(k,x-12,68,'L',.26); T(k,x+12,68,'R',.26)
        B(k,f'Sub Group {n} Solo',x,96,'SOLO',WH,20); B(k,f'Sub Group {n} Cut',x,124,'CUT',WH,20)
        F(k,f'Sub Group {n} Fader',x,160,560,SF,.642)
mpages=pages_of(g,[('Compressor & Mix',0,1),('Monitor & Talkback',2,3),('Aux Masters',4,4),('Bus Masters',5,5),('Sub Groups',6,9)],len(mcols))
master=dict(kind='Master Section',pages=mpages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2a2e34',bg2='#1d2025',ink=INK,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
for e in (strip,master):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Audient ASP8024-HE',strip),('Audient ASP8024-HE Master Section',master)]))
