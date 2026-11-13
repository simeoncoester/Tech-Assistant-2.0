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
# style 'he' = Heritage Edition (dark panel, colours of the HE brochure picture); 'orig' = ASP8024 (light grey panel, colours of the user's console photo)
def mk_strip(style):
    global INK
    he=style=='he'; old=INK; INK='#eef0f2' if he else '#1b2a33'
    AUXC=GY if he else '#2e6a52'; CUEC=GY if he else '#2f7fd0'; HFC=BLU if he else '#d93a35'; LFC=PNK if he else '#5c6068'
    HMC=BLU if he else '#2e6a52'; LMC=PNK if he else '#2f7fd0'; PANC=BK if he else '#2f7fd0'
    cols=['Bus Routing','Aux & EQ','Mitten & SF Pan','Short Fader','Long Fader']
    g=build(cols,100,600,.75)
    K,B,SC,DOT,HL,LED,F=g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
    T=lambda k,x,y,t,sz=.5,col=None: g.T(k,x,y,t,sz,col or INK)
    def AUX(k,n,x,y,col=None):
        K(k,f'Aux {n}' if n.isdigit() else f'Cue {n}',x,y,26,col or (AUXC if n.isdigit() else CUEC)); DOT(k,x,y,18); T(k,x-16,y+22,'∞',.34); T(k,x+16,y+22,'0',.3); T(k,x,y+24,'dB',.24); T(k,x+27,y+4,'→ '+n,.4)
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
    K(k,'HF dB',68,354,34,HFC); DOT(k,68,354,24); T(k,58,384,'dB',.26); T(k,86,384,'±15',.26)
    B(k,'100Hz',22,418,None,DK,16); T(k,22,404,'100Hz',.28); T(k,22,438,'LF',.5)
    K(k,'LF dB',68,430,34,LFC); DOT(k,68,430,24); T(k,58,460,'dB',.26); T(k,86,460,'±15',.26)
    HL(k,478); B(k,'HMF/LMF In',20,500,'IN',WH,18); T(k,52,504,'-0-0-',.36); B(k,'HMF/LMF SF',84,500,'SF',WH,18)
    k=2
    K(k,'HMF kHz',40,40,26,HMC,'ssl',{'sweep':[-140,140]}); SC(k,40,40,19,['0.45','0.7','3.2','7.5','20'],.27,-140,140); T(k,40,66,'kHz',.26); T(k,84,56,'HMF',.55)
    K(k,'HMF BW',24,104,24,HMC); DOT(k,24,104,17); T(k,24,124,'BW',.26)
    K(k,'HMF dB',70,112,34,HMC); DOT(k,70,112,24); T(k,60,142,'dB',.26); T(k,88,142,'±15',.26)
    HL(k,152)
    K(k,'LMF Hz',40,190,26,LMC,'ssl',{'sweep':[-140,140]}); SC(k,40,190,19,['50','75','175','750','1k5'],.27,-140,140); T(k,40,216,'Hz',.26); T(k,84,206,'LMF',.55)
    K(k,'LMF BW',24,254,24,LMC); DOT(k,24,254,17); T(k,24,274,'BW',.26)
    K(k,'LMF dB',70,262,34,LMC); DOT(k,70,262,24); T(k,60,292,'dB',.26); T(k,88,292,'±15',.26)
    HL(k,304)
    B(k,'Copy LF',22,336,None,WH,18); T(k,22,318,'COPY LF',.28); T(k,66,320,'MIC',.32,'#ff4a3d'); T(k,66,334,'TAPE',.32); T(k,22,362,'↓ SOURCE',.28)
    K(k,'SF Pan',62,392,30,PANC); DOT(k,62,392,21); T(k,48,418,'L',.3); T(k,76,418,'R',.3); T(k,62,368,'PAN',.28)
    B(k,'SF Mix',86,436,'MIX',WH,18)
    k=3
    F(k,'Short Fader',28,40,380,SF,.642)
    B(k,'SF Solo',78,250,'SOLO',WH,24); B(k,'SF Cut',78,296,'CUT',WH,24)
    g.d.append(['rect',round((g.cx(k)+8)/g.CW,4),round((34+404)/g.CH,4),round(84/g.CW,4),round(30/g.CH,4),'#c9ccd0','none',4])
    B(k,'Ch Flip',24,500,None,WH,18); T(k,24,520,'CH FLIP',.28); T(k,68,494,'TAPE',.32,'#7fd34a'); T(k,68,510,'MIC',.32)
    k=4
    K(k,'LF Pan',34,46,32,PANC); DOT(k,34,46,22); T(k,20,74,'L',.3); T(k,48,74,'R',.3); T(k,72,40,'PAN',.28)
    B(k,'LF Mix',84,62,'MIX',WH,18)
    B(k,'LF Solo',30,118,'SOLO',WH,24); B(k,'LF Cut',74,118,'CUT',WH,24)
    g.d.append(['rect',round((g.cx(k)+8)/g.CW,4),round((34+150)/g.CH,4),round(84/g.CW,4),round(30/g.CH,4),'#c9ccd0','none',4])
    F(k,'Long Fader',40,210,580,SF,.642)
    if not he:
        for e in g.d:
            if e[0]=='txt' and e[5]=='#c9d2dc': e[5]='#1b2a33'
    pages=pages_of(g,[(n,k,k) for k,n in enumerate(cols)],len(cols))
    INK=old
    return dict(kind='Channel Strip',pages=pages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2a2e34' if he else '#cfd0d0',bg2='#1d2025' if he else '#b9baba',ink='#eef0f2' if he else '#1b2a33',kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
strip=mk_strip('he'); strip_orig=mk_strip('orig')

# ================= master section =================
# Layout after the ASP8024 manual drawings the user sent (compressor, oscillator, solo, communications/talkback, control room,
# studio, bus master trims, aux masters, stereo input, sub group, master fader). style 'he' = Heritage Edition (dark panel,
# compressor as in the HE brochure, Heritage/Bass/Treble), style 'orig' = original ASP8024 (light grey panel, compressor with GR LEDs).
SG=[['10',1],['5',.777],['0',.704],['5',.557],['10',.426],['20',.248],['30',.12],['40',.074],['∞',0]]
MF=[['0',1],['5',.787],['10',.663],['15',.523],['20',.402],['30',.229],['40',.106],['50',.065],['∞',0]]
def mk_master(style):
    he=style=='he'
    MAR=PNK if he else '#7b2340'; CY=BLU if he else '#4fb8bb'; YB='#e8c23a'; RB='#e0483a'; SB=DK if he else '#b9bcbf'
    ink='#eef0f2' if he else '#163838'; barc='#3a3f47' if he else '#5cc5a3'; bart='#dfe3e8' if he else '#123030'
    global INK
    old=INK; INK=ink
    mcols=['Compressor','Oscillator & Solo','Communications','Control Room','Studio','Bus Master Trims','Aux Masters',
           'Stereo In 1-2','Stereo In 3-4','Sub Groups 1-2','Sub Groups 3-4','Sub Groups 5-6','Sub Groups 7-8','Master Fader']
    g=build(mcols,110,600,.5,7)
    K,B,SC,DOT,HL,LED,F=g.K,g.B,g.SC,g.DOT,g.HL,g.LED,g.F
    T=lambda k,x,y,t,sz=.5,col=None: g.T(k,x,y,t,sz,col or INK)
    for e in g.d:
        if e[0]=='txt' and e[5]=='#c9d2dc': e[5]=ink if not he else e[5]
    def BAR(k,y,t,x0=6,w=98): g.d.append(['rect',round((g.cx(k)+x0)/g.CW,4),round((34+y-7)/g.CH,4),round(w/g.CW,4),round(14/g.CH,4),barc,'none',2]); T(k,x0+w/2,y+3,t,.3,bart)
    def KN(k,name,x,y,dia,col,labs=None,a0=-135,a1=135,lab=None,sz=.25):
        K(k,name,x,y,dia,col,'ssl',{'sweep':[a0,a1]} if labs and (a0,a1)!=(-135,135) else None); DOT(k,x,y,dia*.7,11,a0,a1)
        if labs: SC(k,x,y,dia*.7+7,labs,sz,a0,a1)
        if lab: T(k,x,y+dia*.5+17,lab,.26)
    def L010(k,name,x,y,dia,col,lab='LEVEL'): K(k,name,x,y,dia,col); DOT(k,x,y,dia*.7); T(k,x-dia*.55,y+dia*.5+6,'0',.24); T(k,x+dia*.55,y+dia*.5+6,'10',.24); T(k,x,y+dia*.5+12,lab,.24)
    # 0 compressor
    k=0
    if he:
        KN(k,'Threshold',30,56,24,CY); T(k,30,30,'THRESHOLD',.26); T(k,14,80,'LOWER',.22); T(k,46,80,'HIGHER',.22)
        KN(k,'Gain Make-Up',82,56,24,CY); T(k,82,30,'GAIN MAKE-UP',.24); T(k,68,80,'LESS',.22); T(k,96,80,'MORE',.22)
        y1=140
    else:
        BAR(k,10,'GAIN REDUCTION - dB'); g.d.append(['leds',*[round((g.cx(k)+12)/g.CW,4),round((34+34)/g.CH,4)],*[round((g.cx(k)+98)/g.CW,4),round((34+34)/g.CH,4)],12,round(6/g.CW,4),'#ff6b5a',0,'#ff6b5a'])
        for i,v in enumerate(['24','22','20','18','16','14','12','10','8','6','4','2']): T(k,12+i*86/11,26,v,.2)
        K(k,'Threshold',30,82,22,CY); DOT(k,30,82,15); T(k,30,60,'THRESHOLD',.24); T(k,14,104,'-20',.22); T(k,46,104,'+20',.22)
        K(k,'Make Up',82,82,22,CY); DOT(k,82,82,15); T(k,82,60,'MAKE UP',.24); T(k,68,104,'0',.22); T(k,96,104,'40',.22)
        y1=160
    KN(k,'Attack',26,y1,22,CY,['.1','.3','1','3','10','30'],-140,140,None,.22); T(k,26,y1+30,'ATTACK - mS',.22)
    KN(k,'Release',80,y1,22,CY,['.1','.3','.6','1.2','2.4','AUTO'],-140,140,None,.22); T(k,80,y1+30,'RELEASE - S',.22)
    KN(k,'Ratio',30,y1+94,28,CY,['2:1','4:1','10:1'],-45,45); T(k,30,y1+124,'RATIO',.26)
    if he: T(k,82,y1+74,'BASS',.4); T(k,82,y1+88,'EXPAND',.28); T(k,82,y1+102,'↓',.4); B(k,'Bass Expand',82,y1+122,None,WH,16)
    B(k,'Comp In',30,y1+176,'IN','#3d8bff' if he else YB,24)
    # 1 oscillator + solo
    k=1; BAR(k,10,'OSCILLATOR')
    B(k,'Osc Freq A',20,40,None,SB,16); B(k,'Osc Freq B',20,82,None,SB,16); T(k,24,64,'FREQ Hz',.22)
    for i,v in enumerate(['40','1k','10k','15k']): T(k,44+i*12,64,v,.2)
    B(k,'Osc Bus',90,40,None,SB,16); T(k,90,58,'BUS',.24); B(k,'Osc Mix',90,82,None,SB,16); T(k,90,100,'MIX',.24)
    L010(k,'Osc Level',30,132,22,CY); B(k,'Osc On',80,132,'ON',RB,24)
    BAR(k,200,'SOLO')
    L010(k,'Solo Level',30,236,26,MAR); KN(k,'Solo in Front',82,236,20,MAR); T(k,70,256,'SOLO',.2); T(k,94,256,'MIX',.2); T(k,82,266,'SOLO IN FRONT',.2)
    B(k,'SIP',38,300,'SIP',RB,24); B(k,'AFL/PFL',84,300,None,SB,14); T(k,84,318,'AFL/PFL',.22)
    # 2 communications / talkback (+ HE mix bus)
    k=2; BAR(k,10,'COMMUNICATIONS'); L010(k,'Talkback Level',55,48,28,MAR)
    BAR(k,104,'TALKBACK')
    for i,n in enumerate(['SLATE','SLS','FB']): B(k,'TB '+n.title(),22+i*33,134,n,YB,24)
    if he:
        BAR(k,190,'MIX BUS'); B(k,'Heritage',55,222,'HERITAGE',WH,24); T(k,55,246,'RETRO IRON',.24)
        B(k,'Bass Boost',30,282,'BASS',WH,22); B(k,'Treble Boost',80,282,'TREBLE',WH,22)
    # 3 control room
    k=3; BAR(k,10,'CONTROL ROOM'); BAR(k,30,'SOURCE SELECT')
    for i,n in enumerate(['MIX','TAPE 1','TAPE 2','TAPE 3']): B(k,'Source '+n.title(),16+i*26,56,n,YB,20)
    BAR(k,84,'SPEAKER SELECT')
    for i in range(3): L010(k,f'Alt {i+1} Level',42+i*26,110,16,CY,'')
    for i,n in enumerate(['MAIN','ALT 1','ALT 2','ALT 3']): B(k,'Speaker '+n.title(),16+i*26,152,n,YB,20)
    BAR(k,180,'MAIN MONITORS'); L010(k,'Monitor Level',72,218,30,MAR)
    B(k,'Mono',20,210,None,SB,14); T(k,20,226,'MONO',.22)
    B(k,'Cut Left',14,250,None,SB,13); B(k,'Cut Right',36,250,None,SB,13); T(k,14,266,'CUT L',.2); T(k,36,266,'CUT R',.2)
    B(k,'Monitor Cut',30,296,'CUT',RB,22); B(k,'Dim',82,296,'DIM',YB,22)
    # 4 studio
    k=4; BAR(k,10,'STUDIO'); T(k,22,30,'SPK',.26); T(k,58,30,'FB A',.26); T(k,92,30,'FB B',.26)
    for j,(gname,x0) in enumerate([('Speakers',8),('Foldback A',44),('Foldback B',78)]):
        for i,n in enumerate(['Tape 1','Tape 2','C/RM']): B(k,f'{gname} {n}',x0+6,52+i*24,None,SB,12)
        for i,n in enumerate(['Aux A','Aux B']): B(k,f'{gname} {n} L',x0+4,124+i*28,None,SB,11); B(k,f'{gname} {n} R',x0+20,124+i*28,None,SB,11)
    for i,n in enumerate(['TAPE 1','TAPE 2','C/RM']): T(k,34,55+i*24,n,.18)
    for i,n in enumerate(['AUX A','AUX B']): T(k,58,140+i*28,n,.18)
    T(k,55,184,'L — R',.22)
    L010(k,'Studio Speakers Level',20,214,22,CY,''); L010(k,'Foldback A Level',56,214,22,MAR,''); L010(k,'Foldback B Level',92,214,22,MAR,'')
    B(k,'Studio On',20,266,'ON',RB,20); B(k,'Foldback A Solo',56,266,'SOLO',YB,20); B(k,'Foldback B Solo',92,266,'SOLO',YB,20)
    # 5 bus master trims
    k=5
    for i in range(24):
        r,c=divmod(i,3); x=22+c*33; y=26+r*66
        K(k,f'Bus Master {i+1}',x,y,20,MAR); DOT(k,x,y,14); T(k,x,y-17,'0',.2); T(k,x-12,y+20,'-10',.18); T(k,x+12,y+20,'+10',.18); T(k,x,y+32,f'{(i%12)+1}/{(i%12)+13}' if False else str(i+1),.28)
    # 6 aux masters
    k=6
    for i,n in enumerate(['A','B']+[str(j) for j in range(1,13)]): # count after the user's console photo: Aux A, B and 1-12 (14 auxiliaries)
        r,c=divmod(i,2); x=30+c*50; y=30+r*82
        K(k,f'Aux {n} Master',x,y,22,MAR if n in 'AB' else CY); DOT(k,x,y,15); T(k,x-13,y+19,'0',.2); T(k,x+13,y+19,'10',.2)
        B(k,f'Aux {n} Solo',x,y+44,'SOLO',YB,18); T(k,x,y+62,f'AUX {n}',.24)
        if n in ('3','4'): B(k,f'Aux {n} Link',x+20,y-16,None,SB,10); T(k,x+20,y-28,'LINK→'+('1' if n=='3' else '2'),.16)
    # 7/8 stereo inputs (two modules per column)
    for k,base in ((7,1),(8,3)):
        for m in range(2):
            n=base+m; o=m*55; T(k,o+27,10,f'ST {n}',.28)
            for i,(a,b2) in enumerate([('1-2','13-14'),('3-4','15-16'),('5-6','17-18'),('7-8','19-20'),('9-10','21-22'),('11-12','23-24')]):
                r,c=divmod(i,2); x=o+15+c*25; y=30+r*34; B(k,f'Stereo {n} Route {a}',x,y,None,SB,12); T(k,x,y+13,a,.17); T(k,x,y+21,b2,.15)
            B(k,f'Stereo {n} Shift',o+15,140,None,SB,12); T(k,o+15,128,'13-24',.17); T(k,o+15,154,'SHIFT',.17)
            for j,lab in enumerate(['F/B A','F/B B']):
                y=184+j*54; K(k,f'Stereo {n} {lab}',o+27,y,18,MAR); DOT(k,o+27,y,12); T(k,o+27,y-15,lab,.18); T(k,o+16,y+15,'0',.17); T(k,o+38,y+15,'10',.17)
            K(k,f'Stereo {n} Gain',o+27,296,18,CY); DOT(k,o+27,296,12); T(k,o+27,281,'0',.17); T(k,o+14,311,'-20',.16); T(k,o+40,311,'+20',.16); T(k,o+27,320,'GAIN',.17)
            K(k,f'Stereo {n} Level',o+27,368,22,MAR); DOT(k,o+27,368,15); T(k,o+14,386,'0',.17); T(k,o+40,386,'10',.17); T(k,o+27,394,'LEVEL',.17)
            B(k,f'Stereo {n} Mix',o+42,416,None,SB,11); T(k,o+42,430,'MIX',.16)
            B(k,f'Stereo {n} Solo',o+16,450,'SOLO',YB,16); B(k,f'Stereo {n} Cut',o+39,450,'CUT',RB,16)
    # 9-12 sub groups
    for j in range(4):
        k=9+j
        for i in range(2):
            x=30+i*50; n=1+2*j+i
            T(k,x,12,f'SUB GROUP {n}',.2)
            K(k,f'Sub Group {n} Pan',x,46,22,CY); DOT(k,x,46,15); T(k,x,28,'C',.2); T(k,x-12,68,'L',.22); T(k,x+12,68,'R',.22)
            B(k,f'Sub Group {n} Mix',x,90,None,SB,12); T(k,x,104,'MIX',.18)
            B(k,f'Sub Group {n} Solo',x-11,124,'SOLO',YB,18); B(k,f'Sub Group {n} Cut',x+11,150,'CUT',RB,18)
            F(k,f'Sub Group {n} Fader',x,190,570,SG,.704)
    # 13 master fader
    k=13; F(k,'Master Fader',40,60,570,MF,1)
    mpages=pages_of(g,[('Compressor & Solo',0,1),('Talkback & Control Room',2,3),('Studio',4,4),('Bus Trims & Aux',5,6),('Stereo Inputs',7,8),('Sub Groups & Master',9,13)],len(mcols))
    INK=old
    return dict(kind='Master Section',pages=mpages,ks='ssl',ps='sq',ar=round(g.CW/g.CH,4),bare=True,noTicks=True,bg='#2a2e34' if he else '#c9c8c6',bg2='#1d2025' if he else '#b3b2b0',ink=ink,kc=GY,fs=16,brand='',model='',tx=.5,ty=.03,deco=g.d,c=g.c)
master=mk_master('he'); master_orig=mk_master('orig')
for e in (strip,strip_orig,master,master_orig):
    n=[q[1] for q in e['c']]; assert len(n)==len(set(n)), [x for x in n if n.count(x)>1]
sys.stdout.write(''.join(f"  {json.dumps(k)}: {json.dumps(v,ensure_ascii=False)},\n" for k,v in [('Audient ASP8024-HE',strip),('Audient ASP8024',strip_orig),('Audient ASP8024-HE Master Section',master),('Audient ASP8024 Master Section',master_orig)]))
