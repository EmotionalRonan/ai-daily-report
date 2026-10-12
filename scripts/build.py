#!/usr/bin/env python3
"""Build one issue of AI Daily: web HTML, WeChat (公众号) HTML, Xiaohongshu copy + cards.
Usage: python3 scripts/build.py data/YYYY-MM-DD.json [--cover path/to/cover_bg.png]
"""
import json, sys, os, html, glob, re, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

def web_html(d):
    nav = ''.join(f'<a href="#{s["key"]}" style="--c:{s["color"]}">{e(s["name"])}</a>' for s in d['sections'])
    heads = ''.join(f'''<article class="head">
      <div class="num">{i:02d}</div>
      <div><h3><a href="{e(h["url"])}" target="_blank">{e(h["title"])}</a></h3>
      <p>{e(h["body"])}</p><p class="why"><b>为什么重要</b>{e(h["why"])}</p>
      <span class="src">{e(h["source"])}</span></div></article>''' for i,h in enumerate(d['headlines'],1))
    secs = ''
    for s in d['sections']:
        lis = ''.join(f'''<li><span class="rk">{i}</span><div><a href="{e(it["url"])}" target="_blank">{e(it["title"])}</a>
          <div class="meta">{e(it.get("en",""))}<span>{e(it["metric"])}</span></div></div></li>''' for i,it in enumerate(s['items'],1))
        secs += f'''<section class="src-card" id="{s["key"]}" style="--c:{s["color"]}">
        <header><span class="dot"></span><h2>{e(s["name"])}</h2><em>{e(s["tag"])}</em>
        <a class="more" href="{e(s["url"])}" target="_blank">源站 ↗</a></header><ol>{lis}</ol></section>'''
    com = ''.join(f'<li>{e(c)}</li>' for c in d['comments'])
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 日报 {d["date"]}｜{e(d["title"])}</title>
<meta name="description" content="{e(d["lead"])}">
<style>
:root{{--bg:#f6f5f1;--ink:#14161c;--mute:#6b6f7a;--line:#e4e2dc;--card:#fff;--accent:#2f6bff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0d0f14;--ink:#eceef3;--mute:#9aa0ad;--line:#232733;--card:#151821}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 -apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif}}
a{{color:inherit;text-decoration:none}}a:hover{{color:var(--accent)}}
.hero{{background:radial-gradient(1200px 500px at 80% -10%,#2f6bff55,transparent),linear-gradient(135deg,#0a1228,#111a3a);color:#fff;padding:56px 20px 44px}}
.wrap{{max-width:880px;margin:0 auto}}
.kicker{{display:inline-flex;gap:10px;align-items:center;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#aac2ff}}
.kicker b{{background:#f04646;color:#fff;padding:3px 10px;border-radius:99px;letter-spacing:.05em}}
.hero h1{{font-size:clamp(32px,6vw,54px);line-height:1.15;margin:16px 0 10px;font-weight:800}}
.hero .sub{{color:#c9d6ff;font-size:17px}}.hero .lead{{margin-top:22px;color:#dfe6ff;max-width:680px}}
nav{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;gap:8px;overflow-x:auto;padding:12px 20px;scrollbar-width:none}}
nav a{{white-space:nowrap;font-size:13px;padding:5px 12px;border-radius:99px;border:1px solid var(--line);background:var(--card)}}
nav a:hover{{border-color:var(--c);color:var(--c)}}
main{{padding:28px 20px 60px}}h2.t{{font-size:13px;letter-spacing:.14em;color:var(--mute);text-transform:uppercase;margin:34px 0 14px}}
.head{{display:grid;grid-template-columns:64px 1fr;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 22px 18px;margin-bottom:14px}}
.head .num{{font:800 34px/1 Georgia,serif;color:var(--accent)}}.head h3{{margin:0 0 8px;font-size:20px;line-height:1.45}}
.head p{{margin:0 0 10px;color:var(--mute)}}.why{{background:color-mix(in srgb,var(--accent) 9%,transparent);border-left:3px solid var(--accent);padding:10px 14px;border-radius:8px;color:var(--ink)!important}}
.why b{{margin-right:8px;color:var(--accent)}}.src{{font-size:12px;color:var(--mute)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:14px}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}.head{{grid-template-columns:1fr}}}}
.src-card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px;border-top:4px solid var(--c)}}
.src-card header{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}.src-card h2{{font-size:18px;margin:0}}
.src-card em{{font-style:normal;font-size:12px;color:var(--mute)}}.dot{{width:10px;height:10px;border-radius:50%;background:var(--c)}}
.more{{margin-left:auto;font-size:12px;color:var(--mute)}}ol{{list-style:none;margin:0;padding:0}}
li{{display:grid;grid-template-columns:28px 1fr;gap:6px;padding:11px 0;border-top:1px dashed var(--line)}}li:first-child{{border-top:0}}
.rk{{font:700 15px/1.6 Georgia,serif;color:var(--c)}}li a{{font-weight:600;line-height:1.5}}
.meta{{font-size:12px;color:var(--mute);display:flex;justify-content:space-between;gap:10px;margin-top:3px}}.meta span{{white-space:nowrap}}
.take{{background:linear-gradient(135deg,#0a1228,#17234d);color:#fff;border-radius:18px;padding:22px 26px}}.take li{{display:block;border:0;padding:6px 0 6px 22px;position:relative}}
.take li:before{{content:"▶";position:absolute;left:0;color:#f04646;font-size:12px;top:10px}}
footer{{text-align:center;color:var(--mute);font-size:13px;padding:30px 20px 50px}}
</style></head><body>
<header class="hero"><div class="wrap"><div class="kicker"><b>AI 日报</b>{d["date"]} · {d["weekday"]} · 第 {d["issue"]} 期</div>
<h1>{e(d["title"])}</h1><div class="sub">{e(d["subtitle"])}</div><p class="lead">{e(d["lead"])}</p></div></header>
<nav><div class="wrap">{nav}</div></nav>
<main class="wrap"><h2 class="t">今日头条</h2>{heads}
<h2 class="t">九大热点源 · 各取 Top 5</h2><div class="grid">{secs}</div>
<h2 class="t">编辑点评</h2><div class="take"><ul style="margin:0;padding:0">{com}</ul></div></main>
<footer>AI 日报 · 每天 08:00（北京时间）更新 · <a href="../../index.html">往期</a> · 公众号版 <a href="wechat.html">wechat.html</a> · 小红书版 <a href="xiaohongshu.md">xiaohongshu.md</a></footer>
</body></html>'''

def wechat_html(d):
    P='margin:0 0 14px;font-size:15px;line-height:1.85;color:#3c404e;letter-spacing:.5px;'
    def h2(t,c='#2f6bff'): return f'<h2 style="margin:30px 0 16px;padding:6px 14px;background:{c};color:#fff;font-size:17px;border-radius:4px;display:inline-block;">{t}</h2>'
    o=[f'<section style="max-width:677px;margin:0 auto;font-family:-apple-system,PingFang SC,Microsoft YaHei,sans-serif;">',
       f'<section style="padding:22px 20px;background:linear-gradient(135deg,#0a1228,#17234d);border-radius:10px;color:#fff;"><p style="margin:0;font-size:12px;letter-spacing:2px;color:#aac2ff;">AI 日报 · {d["date"]} · 第{d["issue"]}期</p><p style="margin:10px 0 6px;font-size:24px;font-weight:bold;line-height:1.35;">{e(d["title"])}</p><p style="margin:0;font-size:13px;color:#c9d6ff;">{e(d["subtitle"])}</p></section>',
       f'<p style="margin:18px 0;font-size:14px;line-height:1.8;color:#6e7482;">{e(d["lead"])}</p>', h2('今日头条')]
    for i,h in enumerate(d['headlines'],1):
        o.append(f'<p style="margin:18px 0 8px;font-size:17px;font-weight:bold;line-height:1.5;color:#14161c;"><span style="color:#2f6bff;font-family:Georgia,serif;font-size:22px;margin-right:6px;">{i:02d}</span>{e(h["title"])}</p>')
        o.append(f'<p style="{P}">{e(h["body"])}</p>')
        o.append(f'<section style="margin:0 0 20px;padding:10px 14px;background:#ecf3ff;border-left:4px solid #2f6bff;border-radius:6px;font-size:14px;line-height:1.8;color:#1e4696;"><strong>为什么重要：</strong>{e(h["why"])}</section>')
    o.append(h2('九大热点源 · Top 5','#14161c'))
    for s in d['sections']:
        o.append(f'<section style="margin:18px 0;border:1px solid #e4e2dc;border-top:4px solid {s["color"]};border-radius:8px;padding:12px 16px;"><p style="margin:0 0 6px;font-size:16px;font-weight:bold;color:#14161c;">{e(s["name"])} <span style="font-size:12px;font-weight:normal;color:#8a8f99;">{e(s["tag"])}</span></p>')
        for i,it in enumerate(s['items'],1):
            o.append(f'<p style="margin:0;padding:8px 0;border-top:1px dashed #eee;font-size:14px;line-height:1.6;color:#2a2d36;"><span style="color:{s["color"]};font-weight:bold;margin-right:6px;">{i}</span>{e(it["title"])}<br><span style="font-size:12px;color:#9096a3;">{e(it["metric"])}</span></p>')
        o.append('</section>')
    o.append(h2('编辑点评','#f04646'))
    o.append('<section style="padding:16px 18px;background:#0a1228;border-radius:10px;">'+''.join(f'<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:#fff;"><span style="color:#f04646;">▶ </span>{e(c)}</p>' for c in d['comments'])+'</section>')
    o.append('<p style="margin:28px 0 4px;text-align:center;font-size:16px;font-weight:bold;color:#14161c;">你最关心哪一条？评论区聊聊</p><p style="margin:0 0 24px;text-align:center;font-size:13px;color:#8a8f99;">每天早上 8 点更新，记得星标</p>')
    o.append('<p style="padding-top:12px;border-top:1px solid #e4e2dc;font-size:12px;color:#9096a3;">信息来源：'+'、'.join(s['name'] for s in d['sections'])+'</p></section>')
    body='\n'.join(o)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>公众号版 · AI 日报 {d["date"]}</title></head><body style="margin:0;padding:16px;background:#fff;">\n<!-- 在电脑浏览器打开 → 全选复制 → 粘贴到公众号编辑器 -->\n{body}\n</body></html>'

def xhs_md(d):
    nums=['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    lines=[f'# {d["xhs"]["title"]}','',f'{d["date"]} 科技/AI 热点速递，9 个热点源各挑最炸的👇','']
    for i,h in enumerate(d['headlines']): lines.append(f'{nums[i]} {h["title"]}')
    lines+=['','🔥 各平台在聊什么：']
    for s in d['sections']:
        lines.append(f'· {s["name"]}：{s["items"][0]["title"]}')
    lines+=['','💡 一句话：'+d['xhs'].get('oneliner',''),'','你最关心哪条？评论区见👇','',' '.join('#'+t for t in d['xhs']['tags'])]
    return '\n'.join(lines)+'\n'

def index_html():
    issues=sorted(glob.glob(os.path.join(ROOT,'data','*.json')),reverse=True)
    rows=''
    for f in issues:
        d=json.load(open(f)); dt=d['date']
        rows+=f'<a class="it" href="reports/{dt}/index.html"><span>{dt}</span><b>{e(d["title"])}</b><em>{e(d["subtitle"])}</em></a>'
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 日报 · 往期</title>
<style>body{{margin:0;background:#0a1228;color:#fff;font:16px/1.7 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}}.w{{max-width:760px;margin:0 auto;padding:60px 20px}}
h1{{font-size:44px;margin:0}}p{{color:#aac2ff}}.it{{display:grid;grid-template-columns:120px 1fr;gap:4px 16px;padding:18px 0;border-top:1px solid #23305a;color:#fff;text-decoration:none}}
.it span{{color:#7f93c9;font-family:Georgia,serif}}.it em{{grid-column:2;color:#9fb0dd;font-style:normal;font-size:14px}}.it:hover b{{color:#7aa2ff}}</style></head>
<body><div class="w"><h1>AI 日报</h1><p>科技 · AI · 编程热点，每天 08:00 更新。9 个热点源各取 Top 5。</p>{rows}</div></body></html>'''

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('data'); a=ap.parse_args()
    d=json.load(open(a.data)); out=os.path.join(ROOT,'reports',d['date']); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w').write(web_html(d))
    open(os.path.join(out,'wechat.html'),'w').write(wechat_html(d))
    open(os.path.join(out,'xiaohongshu.md'),'w').write(xhs_md(d))
    open(os.path.join(ROOT,'index.html'),'w').write(index_html())
    print('built',out)
