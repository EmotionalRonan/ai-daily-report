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

_CJK = r'[\u4e00-\u9fff]'
def pangu(s):
    s = re.sub(f'({_CJK})([A-Za-z0-9@#$])', r'\1 \2', s)
    s = re.sub(f'([A-Za-z0-9%$])({_CJK})', r'\1 \2', s)
    return s
def text_block(d, x, y, text, font, w, fill, lh):
    text = pangu(text.replace('⭐', '星'))
    lines = wrap(d, text, font, w); ww = w
    # avoid orphans: last line of 1-3 chars → narrow the measure a little
    while len(lines) > 1 and len(lines[-1].strip()) <= 3 and ww > w * 0.8:
        ww -= font.size // 2; lines2 = wrap(d, text, font, ww)
        if len(lines2) > len(lines): break
        lines = lines2
    for l in lines: d.text((x, y), l, font=font, fill=fill); y += lh
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

    # 1 cover — research rule: big title ≤3 lines, ≤8 chars/line, little else; key info above bottom 15%
    img, d = new()
    rule(d, 90, w=1); d.text((W // 2, 150), 'AI 日报', font=F('serif', 64), fill=INK, anchor='mm')
    rule(d, 212, w=4); rule(d, 222, w=1)
    d.text((80, 252), f'{y_}年{int(m_)}月{int(d_)}日 · {D["weekday"]}', font=F('reg', 28), fill=SUB)
    d.text((W - 80, 252), f'第 {D["issue"]} 期', font=F('reg', 28), fill=SUB, anchor='ra')
    lines = D['xhs'].get('cover', D['title']).split('\n')
    fs = 190
    while fs > 110 and max(d.textlength(l, font=F('serif', fs)) for l in lines) > 920: fs -= 6
    lh = int(fs * 1.22); y = 420 + (3 - len(lines)) * lh // 2
    d.rectangle((80, y - 50, 200, y - 40), fill=RED)
    for l in lines: d.text((76, y), l, font=F('serif', fs), fill=INK); y += lh
    y = text_block(d, 80, y + 30, D['xhs'].get('deck', D['subtitle']), F('med', 42), 920, SUB, 62)
    assert y < H * 0.85, ('cover overflow', y)
    d.text((80, H * 0.85 - 40), '左滑看今日头条 →', font=F('reg', 30), fill=RED, anchor='lb')
    footer(d, 1); save(img, 1)

    # 2 headlines
    for fs in (46, 44, 42, 40):
        img, d = new(); y = header(d, '今日头条', 'TOP STORIES')
        for i, h in enumerate(D['headlines']):
            d.text((80, y), f'头条{CN[i]}', font=F('bold', 26), fill=RED); y += 46
            y = text_block(d, 80, y, h['title'], F('serifb', fs), 920, INK, int(fs * 1.45)) + 12
            wf = max(32, fs - 10); y = text_block(d, 80, y, h['why'], F('reg', wf), 920, SUB, int(wf * 1.6)) + 8
            d.text((80, y), '来源：' + h['source'], font=F('reg', 24), fill=MUTE); y += 44
            if i < len(D['headlines']) - 1: rule(d, y + 6, fill=RULE, w=2); y += 40
        if y < H - 130: break
    assert y < H - 130, ('headline overflow', y)
    footer(d, 2); save(img, 2)

    # 3.. topics
    for ti, t in enumerate(topics):
        for fs, gap in ((42, 30), (40, 28), (38, 24), (36, 22), (34, 18)):
            img, d = new(); y = header(d, t['name'], t.get('kicker', ''))
            for j, it in enumerate(t['items']):
                if j: rule(d, y, fill=RULE, w=2); y += gap
                d.text((80, y + 4), f'{j + 1:02d}', font=F('serifb', 32), fill=RED)
                y = text_block(d, 150, y, it['title'], F('bold', fs), 850, INK, int(fs * 1.42)) + 6
                nf = max(32, fs - 6)
                y = text_block(d, 150, y, it['note'], F('reg', nf), 850, SUB, int(nf * 1.55)) + 4
                d.text((150, y), f'{it["src"]} · {it["metric"]}'.replace('⭐', '星'), font=F('reg', 26), fill=MUTE); y += 26 + gap
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
    d.text((120, 80), 'AI 日报', font=F('serif', 56), fill=INK)
    d.text((W2 - 110, 110), f'{dot} · 第 {D["issue"]} 期', font=F('reg', 36), fill=SUB, anchor='rm')
    rule(d, 172, 120, W2 - 110, INK, 5); rule(d, 186, 120, W2 - 110, INK, 2)  # keep text in top 60%: feed overlays title at bottom
    for fs in (120, 108, 96, 88):
        if d.textlength(pangu(D['title']), font=F('serif', fs)) <= W2 - 240: break
    d.text((120, 236), pangu(D['title']), font=F('serif', fs), fill=INK)
    d.text((124, 236 + int(fs * 1.35) + 16), pangu(D['subtitle']), font=F('reg', 46), fill=SUB)
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
