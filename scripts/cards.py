#!/usr/bin/env python3
"""Render Xiaohongshu cards (1080x1440) and WeChat header/thumb for one issue.
Usage: python3 scripts/cards.py data/YYYY-MM-DD.json
Backgrounds: assets/bg_xhs_DATE.jpg (3:4) and assets/bg_wx_DATE.jpg (wide); falls back to gradient.
Fonts: Noto Sans SC, auto-downloaded to ~/.cache/ai-daily-fonts.
"""
import json, os, sys, re, urllib.request
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD=os.path.expanduser('~/.cache/ai-daily-fonts'); os.makedirs(FD,exist_ok=True)
URL='https://github.com/notofonts/noto-cjk/raw/main/Sans/SubsetOTF/SC/NotoSansSC-{}.otf'
def font_path(w):
    p=os.path.join(FD,f'NotoSansSC-{w}.otf')
    if not os.path.exists(p): urllib.request.urlretrieve(URL.format(w),p)
    return p
B=font_path('Bold'); R=font_path('Regular')
def F(s,b=True): return ImageFont.truetype(B if b else R,s)
NAVY=(10,18,40); BLUE=(47,107,255); RED=(240,70,70); WHITE=(255,255,255); INK=(20,22,28); GREY=(107,111,122); BG=(246,245,241)
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def wrap(d,text,font,w):
    lines=[]
    for seg in text.split('\n'):
        toks=re.findall(r'[A-Za-z0-9.\-_/@+]+|.',seg); cur=''
        for t in toks:
            if t in '，。、；：！？”）》?!,.' and cur: cur+=t; continue
            if d.textlength(cur+t,font=font)>w and cur: lines.append(cur.rstrip()); cur=t.lstrip()
            else: cur+=t
        lines.append(cur)
    return lines
def cover_crop(img,W,H):
    r=max(W/img.width,H/img.height); img=img.resize((int(img.width*r)+1,int(img.height*r)+1),Image.LANCZOS)
    l=(img.width-W)//2; t=(img.height-H)//2; return img.crop((l,t,l+W,t+H))
def bg(path,W,H):
    if os.path.exists(path): return cover_crop(Image.open(path).convert('RGB'),W,H).convert('RGBA')
    im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=(10,18+int(20*y/H),40+int(50*y/H),255))
    return im
def shade(img,alpha=240,until=0.62,horizontal=False):
    W,H=img.size; ov=Image.new('RGBA',(W,H)); od=ImageDraw.Draw(ov)
    n=W if horizontal else H
    for i in range(n):
        a=int(alpha*max(0,1-i/(n*until)))
        od.line([(i,0),(i,H)] if horizontal else [(0,i),(W,i)],fill=(5,10,30,a))
    return Image.alpha_composite(img,ov)
def pill(img,box,r,fill):
    ov=Image.new('RGBA',img.size); ImageDraw.Draw(ov).rounded_rectangle(box,r,fill=fill); return Image.alpha_composite(img,ov)

def build(dpath):
    D=json.load(open(dpath)); dt=D['date']; md=dt[5:].replace('-','.')
    out=os.path.join(ROOT,'reports',dt,'xhs'); os.makedirs(out,exist_ok=True)
    W,H=1080,1440; total=6; files=[]
    def save(img,n):
        f=os.path.join(out,f'{n:02d}.png'); img.convert('RGB').save(f); files.append(f)
    # 1 cover
    img=shade(bg(os.path.join(ROOT,'assets',f'bg_xhs_{dt}.jpg'),W,H),245,0.62); d=ImageDraw.Draw(img)
    d.rounded_rectangle((80,110,380,170),30,fill=RED); d.text((105,116),'每日AI日报',font=F(38),fill=WHITE)
    d.text((80,200),md,font=F(150),fill=WHITE)
    y=390
    for l in wrap(d,D['title'].replace('“','').replace('”',''),F(100),920): d.text((80,y),l,font=F(100),fill=WHITE); y+=125
    d.text((84,y+20),D['subtitle'],font=F(40,False),fill=(200,215,255))
    img=pill(img,(80,1290,760,1360),35,(255,255,255,45)); d=ImageDraw.Draw(img)
    d.text((110,1300),f'9大热点源 · 各取Top5 →',font=F(38),fill=WHITE); save(img,1)
    # shared card frame
    def frame(tag,title,page):
        img=Image.new('RGBA',(W,H),BG+(255,)); d=ImageDraw.Draw(img); d.rectangle((0,0,W,250),fill=NAVY)
        d.rounded_rectangle((70,60,70+d.textlength(tag,font=F(34))+50,115),28,fill=RED); d.text((95,64),tag,font=F(34),fill=WHITE)
        d.text((70,135),title,font=F(66),fill=WHITE)
        d.text((70,H-60),f'每日AI日报 · {dt}',font=F(30,False),fill=GREY,anchor='lm'); d.text((W-70,H-60),f'{page}/{total}',font=F(30,False),fill=GREY,anchor='rm')
        return img,d
    # 2 headlines
    img,d=frame('今日头条','这3件事最重要',2); y=290
    for i,h in enumerate(D['headlines'],1):
        tl=wrap(d,h['title'],F(44),830); bl=wrap(d,h['why'],F(34,False),860)
        hh=32+len(tl)*60+12+len(bl)*52+28
        d.rounded_rectangle((60,y,W-60,y+hh),28,fill=WHITE)
        d.ellipse((95,y+30,163,y+98),fill=BLUE); d.text((129,y+64),str(i),font=F(40),fill=WHITE,anchor='mm')
        yy=y+28
        for l in tl: d.text((188,yy),l,font=F(44),fill=INK); yy+=60
        yy+=12
        for l in bl: d.text((100,yy),l,font=F(34,False),fill=GREY); yy+=52
        y+=hh+24
    assert y<H-90,('headlines overflow',y); save(img,2)
    # 3-5 sources, 3 per card, top3 each
    secs=D['sections']
    for ci in range(3):
        group=secs[ci*3:ci*3+3]
        for fs in range(34,24,-1):
          lh=int(fs*1.4); gap=int(fs*0.5)
          img,d=frame('热点源 Top 3',' · '.join(s.get('short',s['name']) for s in group),3+ci); y=285
          for s in group:
            c=hexc(s['color']); items=s['items'][:3]
            rows=[wrap(d,it['title'],F(fs,False),820) for it in items]
            hh=86+sum(len(r)*lh+gap for r in rows)+10
            d.rounded_rectangle((60,y,W-60,y+hh),24,fill=WHITE); d.rounded_rectangle((60,y,W-60,y+12),6,fill=c)
            d.text((95,y+30),s['name'],font=F(40),fill=INK); d.text((W-95,y+42),s['tag'],font=F(28,False),fill=GREY,anchor='rm')
            yy=y+92
            for i,r in enumerate(rows,1):
                d.text((98,yy),str(i),font=F(fs),fill=c)
                for l in r: d.text((140,yy),l,font=F(fs,False),fill=INK); yy+=lh
                yy+=gap
            y+=hh+22
          if y<H-90: break
        assert y<H-90,('source overflow',ci,y); save(img,3+ci)
    # 6 end
    img=shade(bg(os.path.join(ROOT,'assets',f'bg_xhs_{dt}.jpg'),W,H),250,1.2); d=ImageDraw.Draw(img)
    d.text((80,360),'编辑点评',font=F(48),fill=(200,215,255)); y=450
    for c in D['comments']:
        for l in wrap(d,c,F(44),900): d.text((80,y),l,font=F(44),fill=WHITE); y+=64
        y+=30
    img=pill(img,(80,y+30,1000,y+150),30,(255,255,255,50)); d=ImageDraw.Draw(img)
    d.text((120,y+62),'你最关心哪一条？评论区聊聊',font=F(44),fill=WHITE)
    d.text((80,H-140),'关注我，每天早上8点看懂AI',font=F(42),fill=WHITE); d.text((W-70,H-60),f'{total}/{total}',font=F(30,False),fill=(200,215,255),anchor='rm')
    save(img,6)
    # WeChat header 900x383 + thumb
    W2,H2=1800,766
    img=shade(bg(os.path.join(ROOT,'assets',f'bg_wx_{dt}.jpg'),W2,H2),235,0.65,True); d=ImageDraw.Draw(img)
    d.rounded_rectangle((110,120,420,190),35,fill=RED); d.text((140,126),'每日AI日报',font=F(44),fill=WHITE)
    d.text((110,230),D['title'],font=F(100),fill=WHITE)
    d.text((112,390),f'{dt} · {D["subtitle"]}',font=F(44,False),fill=(200,215,255))
    wd=os.path.join(ROOT,'reports',dt); img.convert('RGB').resize((900,383),Image.LANCZOS).save(os.path.join(wd,'wechat_header.png'))
    sq=shade(bg(os.path.join(ROOT,'assets',f'bg_wx_{dt}.jpg'),1000,1000),200,1.0); d=ImageDraw.Draw(sq)
    d.text((500,420),'AI日报',font=F(170),fill=WHITE,anchor='mm'); d.text((500,600),md,font=F(120),fill=(200,215,255),anchor='mm')
    sq.convert('RGB').resize((500,500),Image.LANCZOS).save(os.path.join(wd,'wechat_thumb.png'))
    print('\n'.join(files))
if __name__=='__main__': build(sys.argv[1])
