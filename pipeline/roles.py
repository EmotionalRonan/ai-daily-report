"""Four roles of the daily line, each one model call (or a few) plus hard checks in code.
Hand-offs go only through work/DATE/ and data/DATE.json, same as the manual line.
"""
import json, os, re, glob, io, datetime as dt
import llm
from net import article_text, get

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORBIDDEN = ['AI 生成', 'AI生成', 'AI 整理', 'AI整理', '自动生成', '由 AI', '由AI', '最炸', '必看', '5 分钟看完', '5分钟看完', '九大热点源']
WEEK = '一二三四五六日'

def P(*a): return os.path.join(ROOT, *a)
def role_prompt(name): return open(P('prompts', f'{name}.md')).read()
def jdump(o, path): json.dump(o, open(path, 'w'), ensure_ascii=False, indent=1)

HOUSE = ('你在一条每日科技 AI 日报生产线上工作，全部用简体中文。你不能上网，只能使用下面给出的材料；'
         '材料里没有的事实不要写，数字、人名、公司名、日期必须与材料一致。'
         '岗位说明里提到的 web_fetch、运行脚本、read_file 等动作已由程序代劳，结果就在材料里。只输出 JSON。')

def past_issues(day, n=5):
    out = []
    for f in sorted(glob.glob(P('data', '*.json')), reverse=True):
        d = json.load(open(f))
        if d['date'] >= day: continue
        out.append(d)
        if len(out) >= n: break
    return out

def section_meta(day):
    prev = past_issues(day, 1)
    return [{k: v for k, v in s.items() if k != 'items'} for s in prev[0]['sections']] if prev else []

# ------------------------------------------------------------------ 1 选题雷达
def radar(day, raw, wdir):
    past = past_issues(day)
    seen = sorted({h['url'] for d in past for h in d['headlines']} | {i['url'] for d in past for t in d.get('topics', []) for i in t['items']})
    compact = {k: {'error': v.get('error', ''), 'items': [{x: i.get(x, '') for x in ('en', 'url', 'metric', 'time', 'extra', 'status')} for i in v['items']]}
               for k, v in raw['sources'].items()}
    user = f'''日期：{day}（北京时间）。
岗位说明：
{role_prompt('radar')}

程序已经抓好 9 个来源的原始热榜（下面 RAW），你的工作是筛选、翻译、挑候选：
1. 每个来源挑 5 条与科技 / AI / 编程相关、最热的条目（不足 5 条就全给），按热度排；IT之家只挑科技数码。
2. 每条：title（中文标题，≤34 字）、en（原标题）、metric（照 RAW）、url（必须原样取自 RAW，禁止改写或编造）、time（MM-DD）、what（一句话发生了什么，≤40 字）；RAW 里带 status 的原样保留。
3. 列 6–8 个头条候选 candidates：title、url（必须取自 RAW，尽量是一手页面）、source、why（为什么重要，一句话）、best（最看好的 3 个为 true）、status（拿不准是一手消息就写 "待核"，否则 "ok"）。
4. 不要选往期已经写过的链接：{json.dumps(seen[:120], ensure_ascii=False)}
5. 来源打不开（error 非空且没有条目）就在 notes 里写一句原因。

输出 JSON：{{"sections":[{{"key":"hn","items":[...]}} ...9 个，key 依次为 hn, reddit, x, github, hf, verge_tc, qbitai, ithome, lobsters],"candidates":[...],"notes":"..."}}

RAW：
{json.dumps(compact, ensure_ascii=False)}'''
    out = llm.ask(HOUSE, user, temperature=0.3)
    raw_urls = {i['url'] for v in raw['sources'].values() for i in v['items']}
    meta = {m['key']: m for m in section_meta(day)}
    secs = []
    for s in out['sections']:
        items = [i for i in s.get('items', []) if i.get('url') in raw_urls][:5]
        secs.append(dict(meta.get(s['key'], {'key': s['key'], 'name': s['key']}), items=items))
    cands = [c for c in out.get('candidates', []) if c.get('url') in raw_urls]
    secs, cands = soften(secs), soften(cands)
    r = {'sections': secs, 'candidates': cands, 'notes': out.get('notes', ''),
         'errors': {k: v.get('error') for k, v in raw['sources'].items() if v.get('error')}}
    jdump(r, os.path.join(wdir, 'radar.json'))
    print('[radar]', {s['key']: len(s['items']) for s in secs}, 'candidates', len(cands))
    return r

def fetch_articles(urls, wdir, limit=5000):
    path = os.path.join(wdir, 'articles.json')
    cache = json.load(open(path)) if os.path.exists(path) else {}
    for u in urls:
        if u in cache and cache[u].get('text'): continue
        try:
            cache[u] = article_text(u, limit)
        except Exception as ex:
            cache[u] = {'url': u, 'title': '', 'text': '', 'error': str(ex)[:200]}
    jdump(cache, path)
    return cache

# ------------------------------------------------------------------ 2 主笔
SCHEMA = '''data 字段（照往期格式）：
{"title": 本期标题 ≤18 字, "subtitle": 三条头条的关键词串 ≤30 字, "lead": 导语 ≤120 字,
 "headlines": [{"title": ≤40 字, "body": 80–150 字, "why": 一两句为什么重要, "source": 媒体名, "url": 原文链接}] ×3（凑不出 3 条扎实的就 2 条）,
 "topics": [{"name": 专题名（≤6 字，像「钱与基建」「开发者与社区」）, "kicker": 英文大写短词, "items": [{"title": ≤32 字, "note": ≤40 字有判断的点评, "src": 来源名, "metric": 热度或日期, "url": 链接}] ×4}] ×3,
 "comments": [3 条编辑手记，每条 ≤70 字],
 "xhs": {"title": ≤20 字, "cover": "2–3 行，用 \\n 分行，每行 ≤8 字", "deck": ≤16 字, "intro": 一两句, "oneliner": 一句判断, "closing": 一个具体问题, "tags": [8–10 个，不带 #]},
 "sources": []}
传闻或单一来源写“据报道 / 社区声称 / 称”；厂商自报数字写明是自报。'''

def lint(d):
    e = []
    hs = d.get('headlines', [])
    if not 2 <= len(hs) <= 3: e.append(f'头条应为 3 条（最少 2 条），现在 {len(hs)} 条')
    for i, h in enumerate(hs, 1):
        n = len(h.get('body', ''))
        if not 80 <= n <= 150: e.append(f'头条{i} body {n} 字，应 80–150 字')
        if len(h.get('title', '')) > 40: e.append(f'头条{i} 标题超过 40 字')
        for k in ('title', 'body', 'why', 'source', 'url'):
            if not h.get(k): e.append(f'头条{i} 缺 {k}')
    ts = d.get('topics', [])
    if len(ts) != 3: e.append(f'专题应为 3 个，现在 {len(ts)} 个')
    for t in ts:
        if len(t.get('name', '')) > 8: e.append(f'专题名「{t.get("name")}」超过 8 字（卡片标题会压到英文标签）')
        if len(t.get('items', [])) != 4: e.append(f'专题「{t.get("name")}」应 4 条，现在 {len(t.get("items", []))} 条')
        for it in t.get('items', []):
            if len(it.get('title', '')) > 32: e.append(f'专题条目「{it.get("title")}」标题超过 32 字')
            if len(it.get('note', '')) > 40: e.append(f'专题条目「{it.get("title")}」点评超过 40 字')
            if not it.get('url'): e.append(f'专题条目「{it.get("title")}」缺 url')
    cs = d.get('comments', [])
    if len(cs) != 3: e.append(f'编辑手记应 3 条，现在 {len(cs)} 条')
    for c in cs:
        if len(c) > 70: e.append(f'编辑手记超过 70 字：{c[:20]}…')
    x = d.get('xhs', {})
    if len(x.get('title', '')) > 20: e.append('xhs.title 超过 20 字')
    lines = x.get('cover', '').split('\n')
    if not 2 <= len(lines) <= 3 or any(len(l) > 8 for l in lines): e.append(f'xhs.cover 应 2–3 行、每行 ≤8 字：{lines}')
    if len(x.get('deck', '')) > 16: e.append('xhs.deck 超过 16 字')
    if not 8 <= len(x.get('tags', [])) <= 10: e.append('xhs.tags 应 8–10 个')
    for path, text in _strings(d):
        for w in FORBIDDEN:
            if w in text: e.append(f'出现禁用词「{w}」（位置 {path}：{text[:30]}…）')
    return e

def _strings(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from _strings(v, f'{p}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from _strings(v, f'{p}[{i}]')
    elif isinstance(o, str):
        yield p.lstrip('.'), o

def soften(o):
    """News that is *about* AI-generated content is fine; keep the banned phrase out by writing AIGC."""
    if isinstance(o, dict): return {k: soften(v) for k, v in o.items()}
    if isinstance(o, list): return [soften(v) for v in o]
    if isinstance(o, str): return re.sub(r'AI\s*生成', 'AIGC ', o).replace('AIGC 内容', 'AIGC 内容').replace('  ', ' ')
    return o

def _materials(arts, urls, n=4000):
    out = []
    for u in urls:
        a = arts.get(u) or {}
        out.append(f'### {u}\n标题：{a.get("title", "")}\n' + (a.get('text', '')[:n] or f'（原文打不开：{a.get("error", "")}，只能依据雷达摘要，须写“据报道”或换一条）'))
    return '\n\n'.join(out)

def writer(day, rdr, wdir):
    cand_urls = [c['url'] for c in rdr['candidates']]
    arts = fetch_articles(cand_urls, wdir)
    past = [d['title'] for d in past_issues(day)]
    user = f'''日期：{day}。岗位说明：
{role_prompt('writer')}

{SCHEMA}

雷达结果（sections 会原样作为热榜放进成品，你只需要写其余字段；专题条目从 sections 里挑，url 照抄）：
{json.dumps({'sections': rdr['sections'], 'candidates': rdr['candidates']}, ensure_ascii=False)}

头条候选原文（关键事实只能来自这里）：
{_materials(arts, cand_urls)}

往期标题（不要重复角度）：{past}

输出 JSON：{{"judgment_md": "judgment.md 全文，Markdown，≥300 字，含「## 核心判断」「## 头条入选」（每条对应 radar 里哪一条）「## 落选」（≥3 行，以 - 开头）三节", "data": {{按上面字段}}}}'''
    out = llm.ask(HOUSE, user, temperature=0.5)
    data = out['data']
    for round_ in range(2):
        errs = lint(data)
        if not errs: break
        print('[writer] lint', errs)
        fix = llm.ask(HOUSE, f'下面的 data 有硬性格式问题，逐条修正后输出完整 JSON {{"data": ...}}，事实不变：\n问题：{errs}\n\n{SCHEMA}\n\ndata：{json.dumps(data, ensure_ascii=False)}', temperature=0.2)
        data = fix['data']
    open(os.path.join(wdir, 'judgment.md'), 'w').write(out['judgment_md'].strip() + '\n')
    return finalize(day, data, rdr)

def finalize(day, data, rdr):
    d0 = dt.date.fromisoformat(day)
    past = past_issues(day, 1)
    full = {'date': day, 'weekday': '周' + WEEK[d0.weekday()], 'issue': (past[0]['issue'] + 1) if past else 1}
    for k in ('title', 'subtitle', 'lead', 'headlines'): full[k] = data[k]
    full['sections'] = soften(rdr['sections'])
    for k in ('topics', 'comments', 'xhs'): full[k] = data[k]
    full['sources'] = data.get('sources', [])
    jdump(full, P('data', f'{day}.json'))
    return full

# ------------------------------------------------------------------ 3 文字编辑
def _img_bytes(path, maxw=900):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80); return b.getvalue()

def url_alive(u):
    try: get(u, timeout=20, tries=1, limit=4000); return True
    except Exception as ex: return 'HTTP Error 403' in str(ex) or '429' in str(ex)  # blocked for bots, not dead

def editor(day, wdir, round_no):
    import subprocess, sys
    dpath = P('data', f'{day}.json')
    subprocess.run([sys.executable, P('scripts', 'fetch_images.py'), dpath], check=True)
    d = json.load(open(dpath))
    h_urls = [h['url'] for h in d['headlines']]
    t_urls = [i['url'] for t in d['topics'] for i in t['items']]
    arts = fetch_articles(h_urls + t_urls, wdir)
    hard = lint(d)
    for u in h_urls + t_urls:
        a = arts.get(u, {})
        if not a.get('text') and not url_alive(u): hard.append(f'链接打不开：{u}')
    cands = json.load(open(os.path.join(wdir, 'img_candidates.json'))) if os.path.exists(os.path.join(wdir, 'img_candidates.json')) else {}
    images, img_desc = [], []
    for i, h in enumerate(d['headlines'], 1):
        im = h.get('image')
        if im:
            images.append(('image/jpeg', _img_bytes(P('reports', day, im['file']))))
            img_desc.append(f'第 {len(images)} 张图 = 头条{i} 的配图（{im["src_url"]}）；该页其他候选图：{cands.get(f"h{i}", [])[:8]}')
        else:
            img_desc.append(f'头条{i} 当前无配图（image_skip：{h.get("image_skip", "未说明")}）；候选图：{cands.get(f"h{i}", [])[:8]}')
    slim = {k: v for k, v in d.items() if k != 'sections'}
    user = f'''日期：{day}，第 {round_no} 轮审稿。岗位说明：
{role_prompt('editor')}

稿件 data（热榜 sections 已略去）：
{json.dumps(slim, ensure_ascii=False)}

头条原文（必须逐条核对）：
{_materials(arts, h_urls, 5000)}

专题原文（抽查 ≥8 条）：
{_materials(arts, t_urls, 1200)}

配图（附在消息里的图片，按顺序）：
{chr(10).join(img_desc)}

程序检查发现的硬性问题（如有，必须列入需要看）：{hard}

输出 JSON：{{"ok": ["可以过的条目，一句话说明核对了什么"], "issues": [{{"item": "头条1 / 专题某条 / 手记…", "problem": "一句话", "source": "出处链接", "suggest": "建议怎么改"}}],
"images": [{{"headline": 1, "verdict": "ok|replace|skip", "reason": "一句话", "suggest_url": "replace 时从候选里挑一张"}}], "verdict": "PASS 或 REVISE"}}
只报会出事的问题（事实错、数字错、出处不符、传闻当事实、禁用词、超长、配图无关），措辞偏好不算。'''
    out = llm.ask(HOUSE, user, images=images, temperature=0.1)
    issues = out.get('issues', []) + [{'item': '格式', 'problem': h, 'source': '', 'suggest': ''} for h in hard]
    bad_imgs = [x for x in out.get('images', []) if x.get('verdict') != 'ok'
                and not (x.get('verdict') == 'skip' and not d['headlines'][int(x['headline']) - 1].get('image'))]
    verdict = 'PASS' if not issues and not bad_imgs and out.get('verdict') == 'PASS' else 'REVISE'
    md = [f'# 审稿（第 {round_no} 轮）', '', '## 可以过'] + [f'- {x}' for x in out.get('ok', [])]
    md += ['', '## 需要看'] + ([f'- {x["item"]}：{x["problem"]}' + (f'（{x["source"]}）' if x.get('source') else '') + (f' 建议：{x["suggest"]}' if x.get('suggest') else '') for x in issues] or ['- 无'])
    md += ['', '## 配图'] + [f'- 头条{x["headline"]}：{x["verdict"]}，{x.get("reason", "")}' + (f' 建议换：{x["suggest_url"]}' if x.get('suggest_url') else '') for x in out.get('images', [])]
    md += ['', f'VERDICT: {verdict}']
    path = os.path.join(wdir, 'review.md')
    prev = open(path).read().rstrip() + '\n\n' if round_no > 1 and os.path.exists(path) else ''
    open(path, 'w').write(prev + '\n'.join(md) + '\n')
    print(f'[editor] round {round_no}: {verdict}, {len(issues)} issues, {len(bad_imgs)} image problems')
    return verdict, issues, out.get('images', [])

def revise(day, wdir, issues, images, round_no):
    dpath = P('data', f'{day}.json'); d = json.load(open(dpath))
    rdr = json.load(open(os.path.join(wdir, 'radar.json')))
    arts = json.load(open(os.path.join(wdir, 'articles.json')))
    slim = {k: v for k, v in d.items() if k not in ('sections',)}
    user = f'''你是主笔，文字编辑退回了稿件。逐条处理「需要看」：能改就改，不改写明理由。配图：编辑建议 replace 的，在该头条加 "image_url"（用建议的地址）；建议 skip 的，删掉 image_url 并写 "image_skip": "原因"。
有事实疑点又无法用原文证实的条目直接换成 sections 里另一条或删去（头条最少 2 条）。

{SCHEMA}

编辑意见：{json.dumps(issues, ensure_ascii=False)}
配图意见：{json.dumps(images, ensure_ascii=False)}

当前 data（不含热榜）：{json.dumps(slim, ensure_ascii=False)}

原文材料：
{_materials(arts, [h['url'] for h in d['headlines']] + [i['url'] for t in d['topics'] for i in t['items']], 2500)}

可替换用的热榜：{json.dumps(rdr['sections'], ensure_ascii=False)}

输出 JSON：{{"data": 修改后的完整 data（不含 sections/date/weekday/issue）, "responses": [{{"item": "...", "action": "已改 / 不改", "reason": "一句话"}}]}}'''
    out = llm.ask(HOUSE, user, temperature=0.3)
    data = out['data']
    for h in data.get('headlines', []):
        h.pop('image', None)
    finalize(day, data, rdr)
    with open(os.path.join(wdir, 'review.md'), 'a') as f:
        f.write(f'\n## 主笔回复（第 {round_no} 轮）\n' + '\n'.join(f'- {r["item"]}：{r["action"]}，{r.get("reason", "")}' for r in out.get('responses', [])) + '\n')

# ------------------------------------------------------------------ 4 视觉排版
def designer(day, wdir):
    import subprocess, sys
    dpath = P('data', f'{day}.json')
    for s in ('fetch_images.py', 'build.py', 'cards.py'):
        subprocess.run([sys.executable, P('scripts', s), dpath], check=True)
    d = json.load(open(dpath))
    # README 最新一期
    rd = open(P('README.md')).read()
    line = (f'- **{day}｜{d["title"]}**（{d["subtitle"]}）· [网页](reports/{day}/index.html) · 公众号 reports/{day}/wechat/wechat.html · 小红书 reports/{day}/xhs/xiaohongshu.md')
    rd = re.sub(r'(## 最新一期\n\n)- \*\*.*?\n', lambda m: m.group(1) + line + '\n', rd, count=1, flags=re.S)
    open(P('README.md'), 'w').write(rd)
    # 看图：小红书卡片 + 头图，交给模型查溢出/乱码/孤字
    pngs = sorted(glob.glob(P('reports', day, 'xhs', '*.png'))) + [P('reports', day, 'wechat', 'header.png')]
    imgs = [('image/jpeg', _img_bytes(p, 720)) for p in pngs]
    out = llm.ask(HOUSE, f'''你是视觉排版。按顺序附上 {len(imgs)} 张图（{[os.path.basename(p) for p in pngs]}）。
逐张检查：文字溢出或被裁切、乱码方块、行首标点、单字孤行、图上文字与下面正文不一致。
正文：{json.dumps({k: d[k] for k in ('title', 'subtitle', 'xhs')}, ensure_ascii=False)}
输出 JSON {{"ok": true/false, "problems": ["文件名：问题"]}}''', images=imgs, temperature=0.1)
    note = f'{day} 排版检查（模型看图）：{len(pngs)} 张，' + ('无问题' if out.get('ok') else '问题：' + '；'.join(out.get('problems', [])))
    with open(os.path.join(wdir, 'notes.md'), 'a') as f: f.write('\n' + note + '\n')
    print('[designer]', note)
    return out
