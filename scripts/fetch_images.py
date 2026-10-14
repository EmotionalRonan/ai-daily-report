#!/usr/bin/env python3
"""Download each headline's lead image from its own source page (og:image / twitter:image).
Usage: python3 scripts/fetch_images.py data/YYYY-MM-DD.json
Writes reports/DATE/wechat/img/h1.jpg ... and sets headline["image"] = {"file", "src_url", "credit"} in the data file.
A headline may carry "image_url" set by hand (must still be the source's own picture); it wins over og:image.
Every picture found on each page is listed in work/DATE/img_candidates.json, so a reviewer can swap a decorative one
for a better one by setting "image_url". Headlines without a usable picture get no "image"; the reason is printed and appended to work/DATE/notes.md.
"""
import json, os, re, sys, io, html, urllib.request, urllib.parse
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8'}

def get(url, n=8_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(n), r.geturl()

def candidates(page_url):
    """Pictures from the article's own page: og/twitter image first, then <img> in page order (largest srcset entry)."""
    raw, final = get(page_url, 3_000_000)
    s = raw.decode('utf-8', 'ignore'); out = []
    og = og_image(s, final)
    if og: out.append(og)
    for m in re.finditer(r'<img\b[^>]*>', s, re.I):
        tag = m.group(0); best = None
        ss = re.search(r'srcset\s*=\s*["\']([^"\']+)', tag, re.I)
        if ss:
            parts = [p.strip().rsplit(' ', 1) for p in html.unescape(ss.group(1)).split(',') if p.strip()]
            parts = [(u, int(w[:-1]) if w.endswith('w') and w[:-1].isdigit() else 0) for u, *rest in parts for w in (rest or ['0w'])]
            if parts: best = max(parts, key=lambda x: x[1])[0]
        if not best:
            c = re.search(r'\b(?:data-)?src\s*=\s*["\']([^"\']+)', tag, re.I)
            best = c and html.unescape(c.group(1))
        if not best or best.startswith('data:'): continue
        u = urllib.parse.urljoin(final, best)
        if re.search(r'\.svg|logo|icon|avatar|favicon|sprite|pixel', u, re.I): continue
        if u not in out: out.append(u)
    return out[:12]

def og_image(s, final):
    for prop in ('og:image:secure_url', 'og:image', 'twitter:image', 'twitter:image:src'):
        for m in re.finditer(r'<meta[^>]+>', s, re.I):
            tag = m.group(0)
            if re.search(r'(property|name)\s*=\s*["\']%s["\']' % re.escape(prop), tag, re.I):
                c = re.search(r'content\s*=\s*["\']([^"\']+)', tag, re.I)
                if c: return urllib.parse.urljoin(final, html.unescape(c.group(1).strip()))
    return None

def main(dpath):
    D = json.load(open(dpath)); dt = D['date']
    out = os.path.join(ROOT, 'reports', dt, 'wechat', 'img'); os.makedirs(out, exist_ok=True)
    log = []; cand_log = {}
    for i, h in enumerate(D['headlines'], 1):
        h.pop('image', None)
        try:
            allc = candidates(h['url']) if not h.get('image_url') else [h['image_url']]
            cand_log[f'h{i}'] = allc if not h.get('image_url') else candidates(h['url'])
            cands = allc
            if not cands: raise ValueError('原文页没有图片')
            im = src = None; why = []
            for c in cands:
                try:
                    raw, _ = get(c); x = Image.open(io.BytesIO(raw)).convert('RGB')
                except Exception as ex2: why.append(f'{c[:60]}… 打不开'); continue
                if x.width < 600 or x.height < 300 or not (0.9 <= x.width / x.height <= 2.6):
                    why.append(f'{x.width}x{x.height} 不合用'); continue
                im, src = x, c; break
            if im is None: raise ValueError('；'.join(why[:4]) or '没有合用的图')
            if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            f = os.path.join(out, f'h{i}.jpg'); im.save(f, quality=86, optimize=True)
            h['image'] = {'file': f'wechat/img/h{i}.jpg', 'src_url': src, 'credit': h.get('image_credit') or h['source'],
                          'w': im.width, 'h': im.height}
            log.append(f'头条{i} 配图：{src}（{im.width}x{im.height}）')
        except Exception as ex:
            log.append(f'头条{i} 无配图：{ex}')
    json.dump(D, open(dpath, 'w'), ensure_ascii=False, indent=1)
    wd = os.path.join(ROOT, 'work', dt); os.makedirs(wd, exist_ok=True)
    json.dump(cand_log, open(os.path.join(wd, 'img_candidates.json'), 'w'), ensure_ascii=False, indent=1)
    with open(os.path.join(wd, 'notes.md'), 'a') as fh: fh.write('\n' + '\n'.join(log) + '\n')
    print('\n'.join(log))

if __name__ == '__main__': main(sys.argv[1])
