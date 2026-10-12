#!/usr/bin/env python3
"""Build one issue: web HTML, WeChat (公众号) HTML, Xiaohongshu copy, archive index.
Usage: python3 scripts/build.py data/YYYY-MM-DD.json
Editorial style: paper background, serif headlines, one vermilion accent. No stock AI imagery.
"""
import json, os, html, glob, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import re as _re
_CJK = r'[\u4e00-\u9fff]'
def pangu(s):
    s = _re.sub(f'({_CJK})([A-Za-z0-9@#$])', r'\1 \2', s)
    s = _re.sub(f'([A-Za-z0-9%$])({_CJK})', r'\1 \2', s)
    return s
def e(x): return html.escape(pangu(str(x)))
CN_NUM = '一二三四五六七八九十'

def date_line(d):
    y, m, dd = d['date'].split('-')
    return f'{y}年{int(m)}月{int(dd)}日 · {d["weekday"]} · 第 {d["issue"]} 期'

def source_names(d):
    return '、'.join(s['name'] for s in d['sections'])

# ---------------------------------------------------------------- web
CSS = '''
:root{--paper:#f4f1ea;--card:#fbfaf6;--ink:#141414;--sub:#4a4740;--mute:#8a857a;--rule:#d9d3c7;--red:#c8372d}
@media (prefers-color-scheme:dark){:root{--paper:#15140f;--card:#1c1b16;--ink:#ece8de;--sub:#c2bdb0;--mute:#8a857a;--rule:#2f2d26;--red:#e0574c}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.8 -apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif}
a{color:inherit;text-decoration:none}a:hover{color:var(--red)}
.serif{font-family:"Noto Serif SC","Songti SC","STSong",Georgia,serif}
.wrap{max-width:760px;margin:0 auto;padding:0 22px}
.mast{border-bottom:3px double var(--ink);padding:34px 0 14px;text-align:center}
.mast .name{font:900 30px/1 "Noto Serif SC","Songti SC",serif;letter-spacing:.3em}
.mast .line{display:flex;justify-content:space-between;font-size:12px;color:var(--mute);margin-top:14px;border-top:1px solid var(--ink);padding-top:8px}
.cover{padding:40px 0 30px;border-bottom:1px solid var(--rule)}
.cover h1{font:900 clamp(34px,7vw,56px)/1.2 "Noto Serif SC","Songti SC",serif;margin:0 0 14px;letter-spacing:.02em}
.cover .deck{font-size:18px;color:var(--sub);margin:0 0 18px}
.cover .lead{color:var(--sub);margin:0}
.label{display:flex;align-items:center;gap:12px;margin:46px 0 18px;font-size:13px;letter-spacing:.2em;color:var(--red);font-weight:700}
.label:after{content:"";flex:1;height:1px;background:var(--rule)}
.label i{font-style:normal;color:var(--mute);letter-spacing:.12em;font-weight:400}
.story{padding:6px 0 26px;border-bottom:1px solid var(--rule);margin-bottom:24px}
.story:last-of-type{border-bottom:0}
.story .no{font:900 15px/1 "Noto Serif SC",serif;color:var(--red)}
.story h2{font:700 25px/1.45 "Noto Serif SC","Songti SC",serif;margin:8px 0 12px}
.story p{margin:0 0 12px;color:var(--sub)}
.story .why{color:var(--ink);border-left:2px solid var(--red);padding:2px 0 2px 14px;margin-top:14px}
.story .src{font-size:12px;color:var(--mute)}
.item{display:grid;grid-template-columns:1fr auto;gap:2px 18px;padding:16px 0;border-top:1px solid var(--rule)}
.item:first-of-type{border-top:0}
.item h3{margin:0;font-size:17px;line-height:1.55;font-weight:700}
.item p{grid-column:1/-1;margin:4px 0 0;color:var(--sub);font-size:15px}
.item .meta{grid-column:1/-1;font-size:12px;color:var(--mute);margin-top:4px}
.board{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:26px 28px}
.board h4{margin:0 0 6px;font-size:14px;padding-bottom:6px;border-bottom:2px solid var(--ink)}
.board ol{margin:0;padding:0;list-style:none;counter-reset:n}
.board li{counter-increment:n;font-size:14px;line-height:1.55;padding:7px 0 7px 22px;position:relative;border-bottom:1px dotted var(--rule)}
.board li:before{content:counter(n);position:absolute;left:0;top:7px;font:700 13px Georgia,serif;color:var(--red)}
.board li span{display:block;font-size:11px;color:var(--mute)}
.note{background:var(--card);border:1px solid var(--rule);padding:22px 24px}
.note p{margin:0 0 12px}.note p:last-child{margin:0}
footer{margin:56px 0 0;padding:18px 0 46px;border-top:3px double var(--ink);font-size:12px;color:var(--mute);display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:space-between}
@media(max-width:600px){body{font-size:16px}.story h2{font-size:21px}.mast .line{flex-direction:column;gap:2px;text-align:center}}
'''

def web_html(d):
    heads = ''.join(f'''<article class="story"><div class="no">头条 {CN_NUM[i]}</div>
<h2><a href="{e(h["url"])}" target="_blank" rel="noopener">{e(h["title"])}</a></h2>
<p>{e(h["body"])}</p><p class="why">{e(h["why"])}</p><div class="src">来源：{e(h["source"])}</div></article>''' for i, h in enumerate(d['headlines']))
    topics = ''
    for t in d.get('topics', []):
        items = ''.join(f'''<div class="item"><h3><a href="{e(it["url"])}" target="_blank" rel="noopener">{e(it["title"])}</a></h3>
<p>{e(it["note"])}</p><div class="meta">{e(it["src"])} · {e(it["metric"])}</div></div>''' for it in t['items'])
        topics += f'<div class="label">{e(t["name"])}<i>{e(t.get("kicker",""))}</i></div>{items}'
    board = ''
    for s in d['sections']:
        lis = ''.join(f'<li><a href="{e(it["url"])}" target="_blank" rel="noopener">{e(it["title"])}</a><span>{e(it["metric"])}</span></li>' for it in s['items'])
        board += f'<div><h4><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a></h4><ol>{lis}</ol></div>'
    notes = ''.join(f'<p>{e(c)}</p>' for c in d['comments'])
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d["title"])} · AI 日报 {d["date"]}</title>
<meta name="description" content="{e(d["lead"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="mast"><div class="name">AI 日报</div><div class="line"><span>{date_line(d)}</span><span>科技 · 人工智能 · 编程</span></div></header>
<section class="cover"><h1>{e(d["title"])}</h1><p class="deck">{e(d["subtitle"])}</p><p class="lead">{e(d["lead"])}</p></section>
<div class="label">今日头条<i>TOP STORIES</i></div>{heads}
{topics}
<div class="label">各平台热榜<i>TRENDING</i></div><div class="board">{board}</div>
<div class="label">编辑手记<i>NOTES</i></div><div class="note">{notes}</div>
<footer><span>每天早上 8 点出刊 · <a href="../../index.html">往期</a> · <a href="wechat.html">公众号版</a> · <a href="xiaohongshu.md">小红书版</a></span><span>标注“据报道”“社区声称”的内容尚未得到官方证实</span></footer>
</div></body></html>'''

# ---------------------------------------------------------------- wechat
def wechat_html(d):
    INK = '#1f1f1f'; SUB = '#3f3f3f'; MUTE = '#888888'; RULE = '#e5e0d6'; RED = '#c8372d'
    SERIF = 'font-family:Noto Serif SC,Songti SC,STSong,serif;'
    P = f'margin:0 0 16px;font-size:15px;line-height:1.8;color:{SUB};letter-spacing:1px;text-align:justify;'
    def label(t, en=''):
        return (f'<section style="margin:36px 0 16px;border-top:2px solid {INK};padding-top:8px;">'
                f'<span style="font-size:18px;font-weight:bold;color:{INK};letter-spacing:2px;">{t}</span>'
                f'<span style="font-size:11px;color:{MUTE};letter-spacing:2px;margin-left:8px;">{en}</span></section>')
    o = [f'<section style="max-width:677px;margin:0 auto;padding:0 12px;font-family:-apple-system,PingFang SC,Microsoft YaHei,sans-serif;">',
         f'<section style="text-align:center;border-bottom:3px double {INK};padding:6px 0 10px;"><p style="margin:0;{SERIF}font-size:22px;font-weight:900;letter-spacing:8px;color:{INK};">AI 日报</p>'
         f'<p style="margin:8px 0 0;font-size:11px;color:{MUTE};letter-spacing:1px;">{date_line(d)}</p></section>',
         f'<p style="margin:26px 0 10px;{SERIF}font-size:26px;font-weight:900;line-height:1.35;color:{INK};">{e(d["title"])}</p>',
         f'<p style="margin:0 0 16px;font-size:15px;color:{SUB};">{e(d["subtitle"])}</p>',
         f'<p style="{P}">{e(d["lead"])}</p>', label('今日头条', 'TOP STORIES')]
    for i, h in enumerate(d['headlines']):
        o.append(f'<p style="margin:22px 0 4px;font-size:13px;font-weight:bold;color:{RED};{SERIF}">头条 {CN_NUM[i]}</p>')
        o.append(f'<p style="margin:0 0 10px;{SERIF}font-size:18px;font-weight:bold;line-height:1.55;letter-spacing:.5px;color:{INK};">{e(h["title"])}</p>')
        o.append(f'<p style="{P}">{e(h["body"])}</p>')
        o.append(f'<p style="margin:0 0 6px;padding-left:12px;border-left:2px solid {RED};font-size:15px;line-height:1.8;letter-spacing:1px;color:{INK};">{e(h["why"])}</p>')
        o.append(f'<p style="margin:0 0 8px;font-size:12px;color:{MUTE};">来源：{e(h["source"])}</p>')
    for t in d.get('topics', []):
        o.append(label(e(t['name']), e(t.get('kicker', ''))))
        for j, it in enumerate(t['items']):
            bt = '' if j == 0 else f'border-top:1px solid {RULE};'
            o.append(f'<section style="padding:12px 0;{bt}"><p style="margin:0 0 4px;font-size:16px;font-weight:bold;line-height:1.6;letter-spacing:.5px;color:{INK};">{e(it["title"])}</p>'
                     f'<p style="margin:0 0 4px;font-size:15px;line-height:1.8;letter-spacing:1px;color:{SUB};">{e(it["note"])}</p>'
                     f'<p style="margin:0;font-size:12px;color:{MUTE};">{e(it["src"])} · {e(it["metric"])}</p></section>')
    o.append(label('各平台热榜', 'TRENDING'))
    for s in d['sections']:
        o.append(f'<p style="margin:16px 0 4px;font-size:14px;font-weight:bold;color:{INK};">{e(s["name"])}</p>')
        for i, it in enumerate(s['items'], 1):
            o.append(f'<p style="margin:0;padding:3px 0;font-size:14px;line-height:1.75;color:{SUB};"><span style="color:{RED};font-family:Georgia,serif;margin-right:6px;">{i}</span>{e(it["title"])}<span style="color:{MUTE};font-size:12px;"> · {e(it["metric"])}</span></p>')
    o.append(label('编辑手记', 'NOTES'))
    o.append(f'<section style="background:#f4f1ea;padding:16px 18px;">' + ''.join(f'<p style="margin:0 0 10px;font-size:15px;line-height:1.8;letter-spacing:1px;color:{INK};">{e(c)}</p>' for c in d['comments']) + '</section>')
    o.append(f'<p style="margin:30px 0 4px;text-align:center;font-size:15px;color:{INK};">{e(d["xhs"].get("closing", "你最关心哪一条？欢迎留言。"))}</p>')
    o.append(f'<p style="margin:0 0 24px;text-align:center;font-size:12px;color:{MUTE};">每天早上 8 点见</p>')
    o.append(f'<p style="padding-top:10px;border-top:1px solid {RULE};font-size:12px;line-height:1.8;color:{MUTE};">本期参考：{e(source_names(d))}。标注“据报道”“社区声称”的内容尚未得到官方证实。</p></section>')
    body = '\n'.join(o)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{e(d["title"])}</title></head><body style="margin:0;padding:16px;background:#fff;">\n<!-- 电脑浏览器打开 → 全选复制 → 粘贴到公众号编辑器 -->\n{body}\n</body></html>'

# ---------------------------------------------------------------- xiaohongshu
def xhs_md(d):
    x = d['xhs']; L = [f'# {x["title"]}', '', x.get('intro', ''), '']
    L.append('📌 今天最重要的三件事')
    for i, h in enumerate(d['headlines'], 1):
        L += ['', f'{i}. {h["title"]}', h['why']]
    for t in d.get('topics', []):
        L += ['', f'— {t["name"]} —']
        for it in t['items'][:3]:
            L.append(f'· {it["title"]}')
    L += ['', x.get('oneliner', ''), '', x.get('closing', ''), '', ' '.join('#' + t for t in x['tags'])]
    return '\n'.join(L) + '\n'

# ---------------------------------------------------------------- archive
def index_html():
    rows = ''
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json')), reverse=True):
        d = json.load(open(f))
        rows += f'<a class="it" href="reports/{d["date"]}/index.html"><span>{d["date"]}</span><b>{e(d["title"])}</b><em>{e(d["subtitle"])}</em></a>'
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 日报 · 往期</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&display=swap" rel="stylesheet">
<style>{CSS}
.it{{display:grid;grid-template-columns:110px 1fr;gap:2px 16px;padding:18px 0;border-bottom:1px solid var(--rule)}}
.it span{{color:var(--mute);font:14px Georgia,serif;padding-top:3px}}.it b{{font:700 19px/1.5 "Noto Serif SC",serif}}.it em{{grid-column:2;color:var(--sub);font-style:normal;font-size:14px}}
@media(max-width:600px){{.it{{grid-template-columns:1fr}}.it em{{grid-column:1}}}}</style></head>
<body><div class="wrap"><header class="mast"><div class="name">AI 日报</div><div class="line"><span>往期合集</span><span>每天早上 8 点出刊</span></div></header>
<div style="margin-top:20px">{rows}</div></div></body></html>'''

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('data'); a = ap.parse_args()
    d = json.load(open(a.data)); out = os.path.join(ROOT, 'reports', d['date']); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w').write(web_html(d))
    open(os.path.join(out, 'wechat.html'), 'w').write(wechat_html(d))
    open(os.path.join(out, 'xiaohongshu.md'), 'w').write(xhs_md(d))
    open(os.path.join(ROOT, 'index.html'), 'w').write(index_html())
    print('built', out)
