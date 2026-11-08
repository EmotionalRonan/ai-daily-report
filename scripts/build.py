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
.story figure{margin:4px 0 16px}.story figure img{display:block;width:100%;height:auto;border:1px solid var(--rule);background:var(--card)}
.story figcaption{font-size:12px;color:var(--mute);margin-top:6px}
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

def fig(h):
    im = h.get('image')
    if not im: return ''
    return (f'<figure><a href="{e(h["url"])}" target="_blank" rel="noopener"><img src="{e(im["file"])}" alt="{e(h["title"])}" loading="lazy" '
            f'width="{im.get("w", "")}" height="{im.get("h", "")}"></a><figcaption>图片来源：{e(im["credit"])}</figcaption></figure>')

def web_html(d):
    heads = ''.join(f'''<article class="story"><div class="no">头条 {CN_NUM[i]}</div>
<h2><a href="{e(h["url"])}" target="_blank" rel="noopener">{e(h["title"])}</a></h2>
{fig(h)}<p>{e(h["body"])}</p><p class="why">{e(h["why"])}</p><div class="src">来源：{e(h["source"])}</div></article>''' for i, h in enumerate(d['headlines']))
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
<footer><span>每天早上 8 点出刊 · <a href="../../index.html">往期</a> · <a href="wechat/wechat.html">公众号版</a> · <a href="xhs/xiaohongshu.md">小红书版</a></span><span>标注“据报道”“社区声称”的内容尚未得到官方证实</span></footer>
</div></body></html>'''

# ---------------------------------------------------------------- wechat
PAGES = 'https://emotionalronan.github.io/ai-daily-report'

def wechat_html(d, linked=False):
    """linked=False：普通订阅号版，正文不放外链（会被拦截），热榜加角标、文末列原文地址，配合「阅读原文」跳网页版。
    linked=True：已开通外链权限的账号用，标题直接可点。"""
    web = f'{PAGES}/reports/{d["date"]}/'
    refs = []
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
        if h.get('image'):
            src = f'{PAGES}/reports/{d["date"]}/{h["image"]["file"]}'
            o.append(f'<section style="margin:4px 0 16px;"><img src="{src}" style="display:block;width:100%;height:auto;" alt="">'
                     f'<p style="margin:6px 0 0;font-size:12px;color:{MUTE};">图片来源：{e(h["image"]["credit"])}</p></section>')
        o.append(f'<p style="{P}">{e(h["body"])}</p>')
        o.append(f'<p style="margin:0 0 6px;padding-left:12px;border-left:2px solid {RED};font-size:15px;line-height:1.8;letter-spacing:1px;color:{INK};">{e(h["why"])}</p>')
        o.append(f'<p style="margin:0 0 8px;font-size:12px;color:{MUTE};">来源：{e(h["source"])}</p>')
    for t in d.get('topics', []):
        o.append(label(e(t['name']), e(t.get('kicker', ''))))
        for j, it in enumerate(t['items']):
            bt = '' if j == 0 else f'border-top:1px solid {RULE};'
            o.append(f'<section style="padding:12px 0;{bt}"><p style="margin:0 0 4px;font-size:16px;font-weight:bold;line-height:1.6;letter-spacing:.5px;color:{INK};">{(f'<a href="{html.escape(it["url"])}" style="color:{INK};text-decoration:none;">{e(it["title"])}</a>' if linked and it.get('url') else e(it["title"]))}</p>'
                     f'<p style="margin:0 0 4px;font-size:15px;line-height:1.8;letter-spacing:1px;color:{SUB};">{e(it["note"])}</p>'
                     f'<p style="margin:0;font-size:12px;color:{MUTE};">{e(it["src"])} · {e(it["metric"])}</p></section>')
    o.append(label('各平台热榜', 'TRENDING'))
    if not linked:
        o.append(f'<p style="margin:0 0 6px;font-size:12px;line-height:1.7;color:{MUTE};">想看原文，点文末「阅读原文」进网页版，每条都能一键打开；也可以按角标在文末找到对应地址。</p>')
    A = f'color:{SUB};text-decoration:none;border-bottom:1px solid {RULE};'
    for s in d['sections']:
        o.append(f'<p style="margin:16px 0 4px;font-size:14px;font-weight:bold;color:{INK};">{e(s["name"])}</p>')
        for i, it in enumerate(s['items'], 1):
            if linked and it.get('url'):
                t = f'<a href="{html.escape(it["url"])}" style="{A}">{e(it["title"])}</a>'
            elif it.get('url'):
                refs.append(it['url']); t = f'{e(it["title"])}<sup style="color:{RED};font-size:10px;margin-left:2px;">[{len(refs)}]</sup>'
            else:
                t = e(it['title'])
            o.append(f'<p style="margin:0;padding:3px 0;font-size:14px;line-height:1.75;color:{SUB};"><span style="color:{RED};font-family:Georgia,serif;margin-right:6px;">{i}</span>{t}<span style="color:{MUTE};font-size:12px;"> · {e(it["metric"])}</span></p>')
    o.append(label('编辑手记', 'NOTES'))
    o.append(f'<section style="background:#f4f1ea;padding:16px 18px;">' + ''.join(f'<p style="margin:0 0 10px;font-size:15px;line-height:1.8;letter-spacing:1px;color:{INK};">{e(c)}</p>' for c in d['comments']) + '</section>')
    o.append(f'<p style="margin:30px 0 4px;text-align:center;font-size:15px;color:{INK};">{e(d["xhs"].get("closing", "你最关心哪一条？欢迎留言。"))}</p>')
    o.append(f'<p style="margin:0 0 24px;text-align:center;font-size:12px;color:{MUTE};">每天早上 8 点见</p>')
    if refs:
        o.append(label('原文地址', 'LINKS'))
        o.append(f'<p style="margin:0 0 8px;font-size:12px;color:{MUTE};">长按可复制；网页版：{web}</p>')
        o.extend(f'<p style="margin:0;padding:2px 0;font-size:11px;line-height:1.6;color:{MUTE};word-break:break-all;"><span style="color:{RED};">[{k}]</span> {html.escape(u)}</p>' for k, u in enumerate(refs, 1))
    o.append(f'<p style="margin-top:20px;padding-top:10px;border-top:1px solid {RULE};font-size:12px;line-height:1.8;color:{MUTE};">本期参考：{e(source_names(d))}。标注“据报道”“社区声称”的内容尚未得到官方证实。</p></section>')
    body = '\n'.join(o)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{e(d["title"])}</title></head><body style="margin:0;padding:16px;background:#fff;">\n<!-- 电脑浏览器打开网页版里的这份文件（{web}wechat/wechat.html）→ 全选复制 → 粘贴到公众号编辑器，配图会随之转存；若有图没带过去，用 wechat/img/ 里的同名图手动插入。发布时把「原文链接」设为 {web} -->\n{body}\n</body></html>'

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
GENERIC_TAGS = {'AI', '人工智能', '科技新闻', 'AI日报', '科技'}

def _issue_cover(d):
    """First headline photo from the source page; fall back to the issue header."""
    for h in d.get('headlines', []):
        im = h.get('image')
        if im and im.get('file') and os.path.exists(os.path.join(ROOT, 'reports', d['date'], im['file'])):
            return f'reports/{d["date"]}/{im["file"]}', True
    return f'reports/{d["date"]}/wechat/header.png', False

def _tags(d):
    return [t for t in d.get('xhs', {}).get('tags', []) if t not in GENERIC_TAGS]

def _short_date(d):
    y, m, dd = d['date'].split('-')
    return f'{int(m)}月{int(dd)}日'

INDEX_CSS = '''
body{background:var(--paper)}
.top{position:sticky;top:0;z-index:9;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule)}
.top .in{max-width:1180px;margin:0 auto;padding:0 22px;height:58px;display:flex;align-items:center;gap:28px}
.logo{font:900 21px/1 "Noto Serif SC","Songti SC",serif;letter-spacing:.12em;display:flex;align-items:center;gap:8px}
.logo i{width:10px;height:10px;background:var(--red);display:inline-block}
.nav{display:flex;gap:22px;font-size:14px;color:var(--sub)}
.nav a.on{color:var(--ink);font-weight:700;box-shadow:inset 0 -2px var(--red)}
.top .meta{margin-left:auto;font-size:12px;color:var(--mute)}
.page{max-width:1180px;margin:0 auto;padding:0 22px}
.strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(300px,1fr);gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:26px 0 8px;scrollbar-width:none}
.strip::-webkit-scrollbar{display:none}
.slide{scroll-snap-align:start;position:relative;border-radius:10px;overflow:hidden;aspect-ratio:16/10;background:var(--card);border:1px solid var(--rule)}
.slide img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.slide:hover img{transform:scale(1.03)}
.slide .cap{position:absolute;inset:auto 0 0 0;padding:46px 18px 16px;background:linear-gradient(transparent,rgba(0,0,0,.78));color:#fff}
.slide .cap small{font-size:12px;opacity:.85;letter-spacing:.06em}
.slide .cap b{display:block;font:700 19px/1.45 "Noto Serif SC","Songti SC",serif;margin-top:4px}
.slide.text{background:var(--card)}
.slide.text img{object-fit:contain;background:var(--paper)}
.slide.text .cap{background:linear-gradient(transparent,rgba(20,20,20,.72))}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:44px;padding:26px 0 0}
.sec{display:flex;align-items:baseline;gap:12px;margin:8px 0 6px;font:700 18px/1 "Noto Serif SC",serif}
.sec small{font:400 12px/1 sans-serif;color:var(--mute);letter-spacing:.08em}
.sec:after{content:"";flex:1;height:1px;background:var(--rule)}
.filter{font-size:13px;color:var(--mute);margin:10px 0 0;display:none}
.filter.on{display:block}.filter a{color:var(--red);margin-left:8px}
.card{display:grid;grid-template-columns:260px minmax(0,1fr);gap:22px;padding:24px 0;border-bottom:1px solid var(--rule)}
.card .ph{display:block;border-radius:8px;overflow:hidden;aspect-ratio:16/10;background:var(--card);border:1px solid var(--rule)}
.card .ph img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.card .ph.text img{object-fit:cover;object-position:left center}
.card:hover .ph img{transform:scale(1.03)}
.chips{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:12px;color:var(--red)}
.chips a:hover{text-decoration:underline}
.chips a+a:before{content:"·";color:var(--mute);margin-right:10px}
.card h2{font:700 22px/1.45 "Noto Serif SC","Songti SC",serif;margin:8px 0 8px}
.card p{margin:0;color:var(--sub);font-size:15px;line-height:1.75;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card .by{margin-top:12px;font-size:12px;color:var(--mute);display:flex;gap:12px}
.card .by b{color:var(--ink);font-weight:600}
aside .box{margin:8px 0 34px}
.hot{list-style:none;margin:14px 0 0;padding:0}
.hot li{display:grid;grid-template-columns:minmax(0,1fr) 74px;gap:12px;padding:12px 0;border-bottom:1px dotted var(--rule)}
.hot li b{display:block;font-size:14px;line-height:1.55;font-weight:600}
.hot li span{font-size:11px;color:var(--mute)}
.hot li img{width:74px;height:50px;object-fit:cover;border-radius:4px;border:1px solid var(--rule)}
.hot li .no{grid-column:1/-1}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.tags a{font-size:13px;padding:5px 11px;border:1px solid var(--rule);border-radius:999px;background:var(--card)}
.tags a em{font-style:normal;color:var(--mute);font-size:11px;margin-left:5px}
.tags a:hover{border-color:var(--red)}
.about{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:18px 20px;font-size:14px;color:var(--sub);line-height:1.8}
.about b{color:var(--ink)}
.about .lk{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:13px;color:var(--red)}
.foot{max-width:1180px;margin:56px auto 0;padding:20px 22px 46px;border-top:3px double var(--ink);font-size:12px;color:var(--mute);display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:space-between}
@media(max-width:960px){.grid{grid-template-columns:1fr}aside{border-top:3px double var(--ink);padding-top:20px}}
@media(max-width:640px){.top .meta{display:none}.nav{gap:16px}.strip{grid-auto-columns:84%}.card{grid-template-columns:1fr;gap:14px}.card h2{font-size:20px}}
'''

def index_html():
    issues = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json')), reverse=True)]
    if not issues: return ''
    # featured strip: latest 6 issues
    strip = ''
    for d in issues[:6]:
        src, photo = _issue_cover(d)
        strip += (f'<a class="slide{"" if photo else " text"}" href="reports/{d["date"]}/index.html">'
                  f'<img src="{src}" alt="{e(d["title"])}" loading="lazy">'
                  f'<span class="cap"><small>第 {d["issue"]} 期 · {_short_date(d)} {e(d["weekday"])}</small><b>{e(d["title"])}</b></span></a>')
    # main list
    cards = ''
    for d in issues:
        src, photo = _issue_cover(d)
        tg = _tags(d)[:3]
        chips = ''.join(f'<a href="#tag={html.escape(t)}" data-t="{html.escape(t)}">{e(t)}</a>' for t in tg)
        alltags = '|'.join(html.escape(t) for t in _tags(d))
        n = len(d.get('headlines', []))
        cards += (f'<article class="card" data-tags="|{alltags}|">'
                  f'<a class="ph{"" if photo else " text"}" href="reports/{d["date"]}/index.html"><img src="{src}" alt="{e(d["title"])}" loading="lazy"></a>'
                  f'<div><div class="chips">{chips}</div>'
                  f'<h2><a href="reports/{d["date"]}/index.html">{e(d["title"])}</a></h2>'
                  f'<p>{e(d["subtitle"])}</p>'
                  f'<div class="by"><b>第 {d["issue"]} 期</b><span>{d["date"]} · {e(d["weekday"])}</span><span>{n} 条头条</span></div></div></article>')
    # sidebar: headlines from the latest 7 issues
    hot = ''
    for d in issues[:7]:
        h = (d.get('headlines') or [{}])[0]
        im = h.get('image')
        img = ''
        if im and os.path.exists(os.path.join(ROOT, 'reports', d['date'], im['file'])):
            img = f'<img src="reports/{d["date"]}/{im["file"]}" alt="" loading="lazy">'
        hot += (f'<li><a href="reports/{d["date"]}/index.html"><b>{e(h.get("title", d["title"]))}</b>'
                f'<span>{_short_date(d)} · {e(h.get("source", ""))}</span></a>{img}</li>')
    # tag cloud
    cnt = {}
    for d in issues:
        for t in set(_tags(d)): cnt[t] = cnt.get(t, 0) + 1
    top = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))[:16]
    tags = ''.join(f'<a href="#tag={html.escape(t)}" data-t="{html.escape(t)}">{e(t)}<em>{c}</em></a>' for t, c in top)
    latest = issues[0]
    js = '''<script>
function apply(){var m=decodeURIComponent(location.hash).match(/^#tag=(.+)$/),t=m?m[1]:'',n=0;
document.querySelectorAll('.card').forEach(function(c){var ok=!t||c.dataset.tags.indexOf('|'+t+'|')>=0;c.style.display=ok?'':'none';if(ok)n++});
var f=document.getElementById('flt');f.className='filter'+(t?' on':'');if(t)f.innerHTML='标签「'+t.replace(/[<>&]/g,'')+'」共 '+n+' 期<a href="#">清除</a>';
if(t)document.getElementById('list').scrollIntoView({behavior:'smooth'})}
window.addEventListener('hashchange',apply);apply();</script>'''
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 日报 · 每天早上 8 点的科技与 AI 要闻</title>
<meta name="description" content="每天整理过去 24 小时的科技与 AI 要闻：三条头条、三个专题、各平台热榜。">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&display=swap" rel="stylesheet">
<style>{CSS}{INDEX_CSS}</style></head><body>
<header class="top"><div class="in"><a class="logo" href="index.html"><i></i>AI 日报</a>
<nav class="nav"><a class="on" href="index.html">首页</a><a href="reports/{latest["date"]}/index.html">最新一期</a><a href="#tags">标签</a><a href="https://github.com/EmotionalRonan/ai-daily-report" target="_blank" rel="noopener">GitHub</a></nav>
<span class="meta">已出 {len(issues)} 期 · 每天早上 8 点</span></div></header>
<main class="page"><section class="strip">{strip}</section>
<div class="grid"><div id="list"><div class="sec">全部期刊<small>{issues[-1]["date"]} 至 {latest["date"]}</small></div><div class="filter" id="flt"></div>{cards}</div>
<aside><div class="box"><div class="sec">近 7 期头条</div><ol class="hot">{hot}</ol></div>
<div class="box" id="tags"><div class="sec">热门标签</div><div class="tags">{tags}</div></div>
<div class="box about"><b>关于 AI 日报</b><br>每天早上 8 点，从 Hacker News、Reddit、GitHub、Hugging Face、The Verge、量子位、IT之家等平台挑出过去 24 小时最值得读的科技与 AI 新闻。厂商自报的数字和传闻都会标明。
<div class="lk"><a href="reports/{latest["date"]}/index.html">读最新一期</a><a href="reports/{latest["date"]}/wechat/wechat.html">公众号版</a><a href="https://github.com/EmotionalRonan/ai-daily-report" target="_blank" rel="noopener">源码</a></div></div></aside></div></main>
<footer class="foot"><span>© 2026 AI 日报 · EmotionalRonan</span><span>标注“据报道”“社区声称”的内容尚未得到官方证实</span></footer>
{js}</body></html>'''

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('data'); a = ap.parse_args()
    d = json.load(open(a.data)); out = os.path.join(ROOT, 'reports', d['date']); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w').write(web_html(d))
    wx = os.path.join(out, 'wechat'); xh = os.path.join(out, 'xhs')
    os.makedirs(wx, exist_ok=True); os.makedirs(xh, exist_ok=True)
    open(os.path.join(wx, 'wechat.html'), 'w').write(wechat_html(d))
    open(os.path.join(wx, 'wechat_links.html'), 'w').write(wechat_html(d, linked=True))
    open(os.path.join(xh, 'xiaohongshu.md'), 'w').write(xhs_md(d))
    open(os.path.join(ROOT, 'index.html'), 'w').write(index_html())
    print('built', out)
