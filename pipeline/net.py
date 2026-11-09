"""Small HTTP helpers shared by the pipeline (stdlib only)."""
import json, time, urllib.request, urllib.error, gzip, re, html

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126 Safari/537.36')

def get(url, headers=None, timeout=25, tries=2, limit=6_000_000):
    h = {'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8', 'Accept-Encoding': 'gzip'}
    h.update(headers or {})
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read(limit)
                if r.headers.get('Content-Encoding') == 'gzip':
                    raw = gzip.decompress(raw)
                return raw.decode(r.headers.get_content_charset() or 'utf-8', 'ignore'), r.geturl()
        except urllib.error.HTTPError as ex:
            last = ex
            if ex.code in (401, 403, 404, 410): break
        except Exception as ex:
            last = ex
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f'{url} -> {last}')

def get_json(url, **kw):
    return json.loads(get(url, **kw)[0])

def post_json(url, body, headers=None, timeout=240):
    h = {'Content-Type': 'application/json', 'User-Agent': 'ai-daily-report-pipeline'}
    h.update(headers or {})
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=h, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f'HTTP {ex.code}: {ex.read().decode("utf-8", "ignore")[:600]}')

def strip_tags(s):
    s = re.sub(r'<(script|style|noscript|svg|nav|footer|header|aside|form)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<br\s*/?>|</p>|</h\d>|</li>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    return re.sub(r'\n\s*\n+', '\n', s).strip()

def article_text(url, limit=5000):
    """Readable text of a page: paragraphs inside <article>/<main> when present, else all <p>."""
    raw, final = get(url, timeout=25)
    m = re.search(r'<article\b.*?</article>', raw, re.S | re.I) or re.search(r'<main\b.*?</main>', raw, re.S | re.I)
    body = m.group(0) if m else raw
    paras = [strip_tags(p) for p in re.findall(r'<p\b[^>]*>(.*?)</p>', body, re.S | re.I)]
    paras = [p for p in paras if len(p) > 30]
    text = '\n'.join(paras) if sum(map(len, paras)) > 400 else strip_tags(body)
    t = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
    title = strip_tags(t.group(1)) if t else ''
    return {'url': final, 'title': title[:200], 'text': text[:limit]}
