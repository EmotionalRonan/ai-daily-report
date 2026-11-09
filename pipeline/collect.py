"""选题雷达·采集：9 个来源的原始热榜（不经模型），写 work/DATE/raw_sources.json。
Each source returns up to ~15 raw items {en/title, url, metric, time, extra}. Failures are recorded, never fatal.
"""
import json, os, re, html, sys, datetime as dt
from email.utils import parsedate_to_datetime
from net import get, get_json, strip_tags

NOW = dt.datetime.now(dt.timezone.utc)
WINDOW_H = 36

def _recent(t):
    return t is None or (NOW - t).total_seconds() < WINDOW_H * 3600

def _rss(url, n=20, window_h=WINDOW_H):
    raw, _ = get(url)
    out = []
    for it in re.findall(r'<(?:item|entry)\b.*?</(?:item|entry)>', raw, re.S):
        def tag(t):
            m = re.search(rf'<{t}\b[^>]*>(.*?)</{t}>', it, re.S)
            return html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', m.group(1))).strip() if m else ''
        link = tag('link') or (re.search(r'<link[^>]+href="([^"]+)"', it) or [None, ''])[1]
        when = None
        for t in ('pubDate', 'published', 'updated', 'dc:date'):
            v = tag(t)
            if v:
                try:
                    when = parsedate_to_datetime(v)
                except Exception:
                    try: when = dt.datetime.fromisoformat(v.replace('Z', '+00:00'))
                    except Exception: pass
                break
        if when and when.tzinfo is None: when = when.replace(tzinfo=dt.timezone.utc)
        if when and (NOW - when).total_seconds() > window_h * 3600: continue
        desc = strip_tags(tag('description') or tag('summary') or tag('content'))[:240]
        out.append({'en': strip_tags(tag('title')), 'url': link.strip(), 'time': when.isoformat() if when else '',
                    'metric': (when.astimezone(dt.timezone(dt.timedelta(hours=8))).strftime('%m-%d') if when else ''),
                    'extra': desc})
        if len(out) >= n: break
    return out

def hn():
    r = get_json('https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=40')
    hits = sorted(r['hits'], key=lambda h: -(h.get('points') or 0))
    return [{'en': h['title'], 'url': h.get('url') or f'https://news.ycombinator.com/item?id={h["objectID"]}',
             'metric': f'{h.get("points", 0)} 分', 'time': h.get('created_at', ''),
             'extra': f'{h.get("num_comments", 0)} 评论 · https://news.ycombinator.com/item?id={h["objectID"]}'} for h in hits[:18]]

SUBS = 'LocalLLaMA+MachineLearning+OpenAI+singularity+ClaudeAI+artificial'
def reddit():
    errs = []
    for host in ('www.reddit.com', 'old.reddit.com'):
        try:
            r = get_json(f'https://{host}/r/{SUBS}/top.json?t=day&limit=20', headers={'User-Agent': 'ai-daily-report/1.0 (by EmotionalRonan)'})
            out = []
            for c in r['data']['children']:
                p = c['data']
                created = dt.datetime.fromtimestamp(p['created_utc'], dt.timezone.utc)
                if not _recent(created): continue
                out.append({'en': p['title'], 'url': 'https://www.reddit.com' + p['permalink'],
                            'metric': f'{p["score"]} 赞 · {p["num_comments"]} 评论', 'time': created.isoformat(),
                            'extra': f'r/{p["subreddit"]} ' + (p.get('selftext') or '')[:200]})
            if out: return out
            errs.append(f'{host}: 返回的是旧缓存')
        except Exception as ex:
            errs.append(f'{host}: {ex}')
        try:
            items = _rss(f'https://{host}/r/{SUBS}/top/.rss?t=day')
            if items: return items
        except Exception as ex:
            errs.append(f'{host} rss: {ex}')
    raise RuntimeError('；'.join(errs))

def github():
    raw, _ = get('https://github.com/trending?since=daily', tries=4, timeout=40)
    out = []
    for art in re.findall(r'<article class="Box-row.*?</article>', raw, re.S):
        href = re.search(r'<h2[^>]*>\s*<a[^>]+href="([^"]+)"', art, re.S)
        if not href: continue
        desc = re.search(r'<p class="col-9[^"]*">(.*?)</p>', art, re.S)
        today = re.search(r'([\d,]+) stars today', art)
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', art)
        out.append({'en': href.group(1).strip('/'), 'url': 'https://github.com' + href.group(1),
                    'metric': f'+{today.group(1) if today else "?"} 星',
                    'extra': (strip_tags(desc.group(1)) if desc else '') + (f' [{lang.group(1)}]' if lang else '')})
    return out[:18]

def hf():
    r = get_json('https://huggingface.co/api/daily_papers?limit=30')
    r = sorted(r, key=lambda p: -(p.get('paper', {}).get('upvotes') or 0))
    return [{'en': p['paper']['title'], 'url': f'https://huggingface.co/papers/{p["paper"]["id"]}',
             'metric': f'{p["paper"].get("upvotes", 0)} 赞', 'time': p.get('publishedAt', ''),
             'extra': (p['paper'].get('ai_summary') or p['paper'].get('summary') or '')[:220]} for p in r[:15]]

def verge_tc():
    a = _rss('https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 12)
    b = _rss('https://techcrunch.com/category/artificial-intelligence/feed/', 12)
    for x in a: x['extra'] = 'The Verge · ' + x['extra']
    for x in b: x['extra'] = 'TechCrunch · ' + x['extra']
    return a + b

def qbitai(): return _rss('https://www.qbitai.com/feed', 15, window_h=72)
def ithome(): return _rss('https://www.ithome.com/rss/', 40)

def lobsters():
    r = get_json('https://lobste.rs/hottest.json')
    return [{'en': p['title'], 'url': p.get('url') or p['short_id_url'], 'metric': f'{p["score"]} 分',
             'time': p.get('created_at', ''), 'extra': ' '.join(p.get('tags', [])) + f' · {p["comments_url"]}'} for p in r[:18]]

def x_search():
    """X has no open API: ask the model with Google Search grounding for today's most-viewed AI/tech posts."""
    import llm
    day = NOW.astimezone(dt.timezone(dt.timedelta(hours=8))).strftime('%Y-%m-%d')
    q = (f'Search the web for the most viewed / most liked posts on X (Twitter) about AI and technology in the 24 hours before {day} '
         '(Beijing time). Return JSON {"items":[{"en": post summary in English, "author": "@handle", "url": "https://x.com/... status url if found, else the article url reporting it", '
         '"metric": "views or likes as reported", "time": "YYYY-MM-DD", "extra": "where this was reported"}]} with up to 10 items. '
         'Only include posts you actually found in search results; never invent URLs or numbers.')
    out, srcs = llm.ask('You are a careful news researcher.', q, search=True)
    items = out.get('items', [])
    for it in items:
        it['status'] = '待核'
        it['en'] = (it.get('author', '') + ' ' + it.get('en', '')).strip()
    return items

SOURCES = [('hn', hn), ('reddit', reddit), ('x', x_search), ('github', github), ('hf', hf),
           ('verge_tc', verge_tc), ('qbitai', qbitai), ('ithome', ithome), ('lobsters', lobsters)]

def collect(day, wdir, use_llm=True):
    res = {'date': day, 'fetched_at': NOW.isoformat(), 'sources': {}}
    for key, fn in SOURCES:
        if key == 'x' and not use_llm:
            res['sources'][key] = {'items': [], 'error': 'skipped (no LLM)'}; continue
        try:
            items = [i for i in fn() if i.get('url')]
            res['sources'][key] = {'items': items}
            print(f'[collect] {key}: {len(items)}')
        except Exception as ex:
            res['sources'][key] = {'items': [], 'error': str(ex)[:300]}
            print(f'[collect] {key}: FAILED {str(ex)[:200]}')
    # reddit fallback through search grounding when blocked
    if use_llm and not res['sources']['reddit']['items']:
        try:
            import llm
            q = (f'Search for the top Reddit posts of the last 24 hours (before {day}) in r/LocalLLaMA, r/singularity, r/OpenAI, r/ClaudeAI, '
                 'r/MachineLearning, r/artificial. Return JSON {"items":[{"en": post title, "url": reddit permalink or a page quoting it, '
                 '"metric": "upvotes/comments if shown", "extra": "subreddit"}]} up to 10 items. Never invent URLs or numbers.')
            out, _ = llm.ask('You are a careful news researcher.', q, search=True)
            items = [dict(i, status='待核') for i in out.get('items', []) if i.get('url')]
            res['sources']['reddit'] = {'items': items, 'error': res['sources']['reddit'].get('error', '') + '；已用搜索补位'}
            print(f'[collect] reddit via search: {len(items)}')
        except Exception as ex:
            print('[collect] reddit search fallback failed', ex)
    os.makedirs(wdir, exist_ok=True)
    json.dump(res, open(os.path.join(wdir, 'raw_sources.json'), 'w'), ensure_ascii=False, indent=1)
    return res

if __name__ == '__main__':
    day = sys.argv[1]; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    collect(day, os.path.join(root, 'work', day + '-pipeline'), use_llm='--no-llm' not in sys.argv)
