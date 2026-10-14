#!/usr/bin/env python3
"""Gate before push. Any failure prints the reason and exits 1 — do not push until it passes.
Usage: python3 scripts/check.py DATE
"""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dt = sys.argv[1]; W = os.path.join(ROOT, 'work', dt); R = os.path.join(ROOT, 'reports', dt)
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)
def read(p):
    try: return open(p).read()
    except Exception: return ''

# 1 选题雷达留底
try:
    radar = json.load(open(os.path.join(W, 'radar.json')))
    secs = radar.get('sections', [])
    filled = [s_.get('key') for s_ in secs if s_.get('items')]
    need(len(filled) >= 9, f'radar.json 只有 {len(filled)} 个来源有条目（要 9 个）：{filled}')
    for s_ in secs:
        need(all(it.get('url') for it in s_.get('items', [])), f'radar.json 的 {s_.get("key")} 有条目缺 url')
    need(len(radar.get('candidates', [])) >= 3, 'radar.json 头条候选少于 3 个')
except Exception as ex:
    bad.append(f'radar.json 缺失或读不了：{ex}')

# 2 主笔留底
j = read(os.path.join(W, 'judgment.md'))
need(len(j) >= 300, f'judgment.md 太短（{len(j)} 字符，要 ≥300）')
need('核心判断' in j, 'judgment.md 没写「核心判断」')
need('入选' in j, 'judgment.md 没写头条入选理由')
need('落选' in j and len(re.findall(r'^\s*[-*\d]', j.split('落选', 1)[-1], re.M)) >= 3, 'judgment.md 落选候选少于 3 条')

# 3 编辑留底
rv = read(os.path.join(W, 'review.md')).strip()
need(rv.splitlines()[-1:] == ['VERDICT: PASS'], 'review.md 最后一行不是 VERDICT: PASS')
need('配图' in rv, 'review.md 没有逐条核对配图')
need(os.path.exists(os.path.join(W, 'notes.md')), 'notes.md 缺失')

# 4 成品
D = json.load(open(os.path.join(ROOT, 'data', f'{dt}.json')))
nh = len(D['headlines']); nt = len(D.get('topics', [])[:3])
for f in ['index.html', 'wechat/wechat.html', 'wechat/wechat_links.html', 'wechat/header.png', 'wechat/thumb.png', 'xhs/xiaohongshu.md']:
    need(os.path.exists(os.path.join(R, f)), f'缺 reports/{dt}/{f}')
pngs = sorted(glob.glob(os.path.join(R, 'xhs', '*.png')))
need(len(pngs) == 2 + nh + nt, f'xhs 卡片 {len(pngs)} 张，应为 {2 + nh + nt} 张')
stray = [f for f in os.listdir(R) if f not in ('index.html', 'wechat', 'xhs')] if os.path.isdir(R) else []
need(not stray, f'reports/{dt}/ 根下有多余文件：{stray}')
for i, h in enumerate(D['headlines'], 1):
    im = h.get('image')
    if im:
        need(os.path.exists(os.path.join(R, im['file'])), f'头条{i} 配图文件不存在')
    else:
        need(h.get('image_skip'), f'头条{i} 没有配图，也没写 image_skip 原因')
wx = read(os.path.join(R, 'wechat/wechat.html'))
need('原文地址' in wx and '<sup' in wx, 'wechat.html 缺热榜角标或文末原文地址')
need('href="http' not in wx.split('<body', 1)[-1], 'wechat.html 正文里出现了外链')
text = wx + read(os.path.join(R, 'index.html')) + read(os.path.join(R, 'xhs/xiaohongshu.md'))
for w in ['AI 生成', 'AI生成', 'AI 整理', 'AI整理', '自动生成', '由 AI', '由AI']:
    need(w not in text, f'成品里出现禁用词「{w}」')

if bad:
    print('CHECK FAIL'); print('\n'.join('- ' + b for b in bad)); sys.exit(1)
print('CHECK PASS')
