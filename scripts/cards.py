#!/usr/bin/env python3
"""Render Xiaohongshu cards (1080x1440) and WeChat header (900x383) / thumb (500x500).
Usage: python3 scripts/cards.py data/YYYY-MM-DD.json
Editorial style: paper background, Noto Serif SC headlines, Noto Sans SC body, one vermilion accent.
Fonts auto-download to ~/.cache/ai-daily-fonts.
"""
import json, os, sys, re, urllib.request
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.expanduser('~/.cache/ai-daily-fonts'); os.makedirs(FD, exist_ok=True)
BASE = 'https://github.com/notofonts/noto-cjk/raw/main/'
FONTS = {'serif': 'Serif/SubsetOTF/SC/NotoSerifSC-Black', 'serifb': 'Serif/SubsetOTF/SC/NotoSerifSC-Bold',
         'bold': 'Sans/SubsetOTF/SC/NotoSansSC-Bold', 'med': 'Sans/SubsetOTF/SC/NotoSansSC-Medium',
         'reg': 'Sans/SubsetOTF/SC/NotoSansSC-Regular'}
def fp(k):
    p = os.path.join(FD, os.path.basename(FONTS[k]) + '.otf')
    if not os.path.exists(p) or os.path.getsize(p) < 1000: urllib.request.urlretrieve(BASE + FONTS[k] + '.otf', p)
    return p
_cache = {}
def F(k, s):
    if (k, s) not in _cache: _cache[(k, s)] = ImageFont.truetype(fp(k), s)
    return _cache[(k, s)]

PAPER = (244, 241, 234); CARD = (251, 250, 246); INK = (20, 20, 20); SUB = (74, 71, 64)
MUTE = (138, 133, 122); RULE = (217, 211, 199); RED = (200, 55, 45)
CN = '一二三四五六七八九十'
NOEND = '“‘（《「『(['
NOSTART = '，。、；：！？”’）》」』%,.!?;:)'

def wrap(d, text, font, w):
    out = []
    for seg in text.split('\n'):
        toks = re.findall(r'[A-Za-z0-9.\-_/@+#%’\']+|.', seg); cur = ''
        for t in toks:
            if d.textlength(cur + t, font=font) > w and cur.strip():
                if t in NOSTART:            # keep closing punctuation with previous char
                    cur, t = cur[:-1], cur[-1] + t
                while cur and cur[-1] in NOEND:  # opening punctuation never ends a line
                    cur, t = cur[:-1], cur[-1] + t
                out.append(cur.rstrip()); cur = t.lstrip()
            else: cur += t
        out.append(cur)
    return out

def text_block(d, x, y, text, font, w, fill, lh):
    text = text.replace('⭐', '星')
    for l in wrap(d, text, font, w): d.text((x, y), l, font=font, fill=fill); y += lh
    return y

def rule(d, y, x0=80, x1=1000, fill=INK, w=2): d.line([(x0, y), (x1, y)], fill=fill, width=w)

def build(dpath):
    D = json.load(open(dpath)); dt = D['date']; y_, m_, d_ = dt.split('-')
    dot = f'{y_}.{m_}.{d_}'; md = f'{int(m_)}.{int(d_)}'
    out = os.path.join(ROOT, 'reports', dt, 'xhs'); os.makedirs(out, exist_ok=True)
    W, H = 1080, 1440; topics = D.get('topics', [])[:3]; total = 3 + len(topics); files = []
    def save(img, n):
        f = os.path.join(out, f'{n:02d}.png'); img.save(f); files.append(f)
    def new():
        img = Image.new('RGB', (W, H), PAPER); return img, ImageDraw.Draw(img)
    def footer(d, n):
        rule(d, H - 110, fill=RULE, w=2)
        d.text((80, H - 70), f'AI 日报 · {dot}', font=F('reg', 26), fill=MUTE, anchor='lm')
        d.text((W - 80, H - 70), f'{n} / {total}', font=F('reg', 26), fill=MUTE, anchor='rm')
    def header(d, label, kicker):
        d.text((80, 96), label, font=F('serif', 64), fill=INK)
        d.text((W - 80, 140), kicker, font=F('med', 24), fill=RED, anchor='rm')
        rule(d, 196, w=4); rule(d, 206, w=1)
        return 250

    # 1 cover
    img, d = new()
    rule(d, 90, w=1); d.text((W // 2, 150), 'AI 日报', font=F('serif', 64), fill=INK, anchor='mm')
    rule(d, 212, w=4); rule(d, 222, w=1)
    d.text((80, 252), f'{y_}年{int(m_)}月{int(d_)}日 · {D["weekday"]}', font=F('reg', 26), fill=SUB)
    d.text((W - 80, 252), f'第 {D["issue"]} 期', font=F('reg', 26), fill=SUB, anchor='ra')
    d.text((80, 380), md, font=F('serif', 46), fill=RED)
    y = 450
    for fs in (118, 108, 98, 90):
        if len(wrap(d, D['title'], F('serif', fs), 920)) <= 3: break
    for l in wrap(d, D['title'], F('serif', fs), 920): d.text((80, y), l, font=F('serif', fs), fill=INK); y += int(fs * 1.28)
    y = text_block(d, 80, y + 18, D['subtitle'], F('reg', 36), 920, SUB, 54) + 50
    rule(d, y, fill=INK, w=2); y += 30
    d.text((80, y), '本期要闻', font=F('bold', 28), fill=RED); y += 58
    for i, h in enumerate(D['headlines']):
        d.text((80, y), CN[i], font=F('serifb', 34), fill=RED)
        y = text_block(d, 136, y, h['title'], F('med', 34), 864, INK, 50) + 22
    assert y < H - 130, ('cover overflow', y)
    footer(d, 1); save(img, 1)

    # 2 headlines
    for fs in (44, 42, 40, 38, 36):
        img, d = new(); y = header(d, '今日头条', 'TOP STORIES')
        for i, h in enumerate(D['headlines']):
            d.text((80, y), f'头条{CN[i]}', font=F('bold', 26), fill=RED); y += 46
            y = text_block(d, 80, y, h['title'], F('serifb', fs), 920, INK, int(fs * 1.45)) + 12
            y = text_block(d, 80, y, h['why'], F('reg', fs - 12), 920, SUB, int((fs - 12) * 1.65)) + 8
            d.text((80, y), '来源：' + h['source'], font=F('reg', 24), fill=MUTE); y += 44
            if i < len(D['headlines']) - 1: rule(d, y + 6, fill=RULE, w=2); y += 40
        if y < H - 130: break
    assert y < H - 130, ('headline overflow', y)
    footer(d, 2); save(img, 2)

    # 3.. topics
    for ti, t in enumerate(topics):
        for fs in (38, 36, 34, 32, 30):
            img, d = new(); y = header(d, t['name'], t.get('kicker', ''))
            for j, it in enumerate(t['items']):
                if j: rule(d, y, fill=RULE, w=2); y += 30
                d.text((80, y + 2), f'{j + 1:02d}', font=F('serifb', 30), fill=RED)
                y = text_block(d, 150, y, it['title'], F('bold', fs), 850, INK, int(fs * 1.45)) + 8
                y = text_block(d, 150, y, it['note'], F('reg', fs - 8), 850, SUB, int((fs - 8) * 1.65)) + 6
                d.text((150, y), f'{it["src"]} · {it["metric"]}'.replace('⭐', '星'), font=F('reg', 23), fill=MUTE); y += 52
            if y < H - 130: break
        assert y < H - 130, ('topic overflow', ti, y)
        footer(d, 3 + ti); save(img, 3 + ti)

    # last: editor notes
    for fs in (40, 38, 36, 34):
        img, d = new(); y = header(d, '编辑手记', 'NOTES')
        for c in D['comments']:
            d.rectangle((80, y + 10, 86, y + 10 + int(fs * 1.2)), fill=RED)
            y = text_block(d, 112, y, c, F('serifb', fs), 888, INK, int(fs * 1.62)) + 34
        y += 10; rule(d, y, fill=INK, w=2); y += 34
        y = text_block(d, 80, y, D['xhs'].get('closing', '你最关心哪一条？评论区聊聊。'), F('med', 34), 920, SUB, 52)
        if y < H - 200: break
    assert y < H - 200, ('notes overflow', y)
    d.text((80, H - 170), '每天早上 8 点见', font=F('bold', 34), fill=RED)
    footer(d, total); save(img, total)

    # WeChat header 900x383 (rendered 2x)
    W2, H2 = 1800, 766; img = Image.new('RGB', (W2, H2), PAPER); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 28, H2), fill=RED)
    d.text((120, 110), 'AI 日报', font=F('serif', 56), fill=INK)
    d.text((W2 - 110, 140), f'{dot} · 第 {D["issue"]} 期', font=F('reg', 36), fill=SUB, anchor='rm')
    rule(d, 205, 120, W2 - 110, INK, 5); rule(d, 219, 120, W2 - 110, INK, 2)
    for fs in (120, 108, 96, 88):
        if d.textlength(D['title'], font=F('serif', fs)) <= W2 - 240: break
    d.text((120, 290), D['title'], font=F('serif', fs), fill=INK)
    d.text((124, 290 + int(fs * 1.35) + 20), D['subtitle'], font=F('reg', 46), fill=SUB)
    wd = os.path.join(ROOT, 'reports', dt)
    img.resize((900, 383), Image.LANCZOS).save(os.path.join(wd, 'wechat_header.png'))
    # thumb 500x500 (rendered 2x)
    sq = Image.new('RGB', (1000, 1000), PAPER); d = ImageDraw.Draw(sq)
    rule(d, 250, 140, 860, INK, 6); rule(d, 266, 140, 860, INK, 2)
    d.text((500, 440), 'AI 日报', font=F('serif', 170), fill=INK, anchor='mm')
    rule(d, 600, 140, 860, INK, 2); rule(d, 616, 140, 860, INK, 6)
    d.text((500, 730), md, font=F('serif', 110), fill=RED, anchor='mm')
    sq.resize((500, 500), Image.LANCZOS).save(os.path.join(wd, 'wechat_thumb.png'))
    print('\n'.join(files))

if __name__ == '__main__': build(sys.argv[1])
