"""Model client. Default: Google Gemini (native API, supports JSON output, images and Google Search grounding).
Env: GEMINI_API_KEY (or LLM_API_KEY), LLM_MODEL (optional; newest gemini *pro* is picked when unset).
Set LLM_PROVIDER=openai with LLM_BASE_URL/LLM_API_KEY/LLM_MODEL to use any OpenAI-compatible API (no search grounding).
"""
import os, json, re, base64, time
from net import post_json, get_json

PROVIDER = os.environ.get('LLM_PROVIDER', 'gemini')
KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('LLM_API_KEY', '')
G = os.environ.get('GEMINI_BASE', 'https://generativelanguage.googleapis.com/v1beta')
_model = os.environ.get('LLM_MODEL') or None
USAGE = {'calls': 0, 'in': 0, 'out': 0}

def _gh():
    return {'x-goog-api-key': KEY} if KEY else {}

def model():
    global _model
    if _model: return _model
    if PROVIDER == 'gemini':
        _model = 'gemini-flash-latest'  # free tier has no Pro quota; set LLM_MODEL=gemini-pro-latest on a paid key
        return _model
    if PROVIDER != 'gemini': raise RuntimeError('LLM_MODEL is required for openai provider')
    names = [m['name'].split('/')[-1] for m in get_json(f'{G}/models?pageSize=200', headers=_gh()).get('models', [])
             if 'generateContent' in m.get('supportedGenerationMethods', [])]
    pro = [n for n in names if re.match(r'gemini-[\d.]+-pro', n) and not re.search(r'tts|image|audio|live|exp|computer', n)]
    def ver(n):
        v = re.match(r'gemini-([\d.]+)', n).group(1)
        return (tuple(int(x) for x in v.split('.')), 'preview' not in n, -len(n))
    if not pro: raise RuntimeError(f'no gemini pro model in {names[:20]}')
    _model = sorted(pro, key=ver)[-1]
    print('[llm] model =', _model)
    return _model

def _parse_json(t):
    t = t.strip()
    m = re.search(r'```(?:json)?\s*(.*?)```', t, re.S)
    if m: t = m.group(1)
    a, b = t.find('{'), t.rfind('}')
    return json.loads(t[a:b + 1])

def chain():
    fb = os.environ.get('LLM_FALLBACK_MODELS') or ('gemini-3.6-flash,gemini-2.5-flash' if PROVIDER == 'gemini' else '')
    return [model()] + [m.strip() for m in fb.split(',') if m.strip() and m.strip() != model()]

def ask(system, user, *, json_out=True, images=(), search=False, temperature=0.4, tries=6):
    """One model call. images: list of (mime, bytes). search: allow Google Search grounding (gemini only).
    Returns parsed JSON (json_out) or text; with search also returns the grounding sources as ('sources', [...])."""
    if not KEY:
        raise RuntimeError('缺少 GEMINI_API_KEY：请在仓库 Settings → Secrets and variables → Actions 的 Repository secrets 里添加')
    last = None
    for i in range(tries):
        try:
            ms = chain(); m = ms[i % len(ms)]   # 503 / timeout on one model -> try the next one
            print(f'[llm] call {m} ({len(user)} chars)', flush=True)
            if PROVIDER == 'gemini':
                return _gemini(system, user, json_out, images, search, temperature, m)
            return _openai(system, user, json_out, images, temperature)
        except Exception as ex:
            last = ex; print(f'[llm] retry {i + 1}: {str(ex)[:300]}')
            if re.search(r'HTTP (400|401|403)\b', str(ex)):   # bad / missing / unauthorised key: retrying won't help
                raise RuntimeError(f'LLM 鉴权失败（检查 GEMINI_API_KEY）: {str(ex)[:300]}')
            time.sleep(10 * (i + 1))
    raise RuntimeError(f'LLM failed: {last}')

def _gemini(system, user, json_out, images, search, temperature, mdl=None):
    parts = [{'text': user}] + [{'inline_data': {'mime_type': m, 'data': base64.b64encode(b).decode()}} for m, b in images]
    body = {'system_instruction': {'parts': [{'text': system}]}, 'contents': [{'role': 'user', 'parts': parts}],
            'generationConfig': {'temperature': temperature}}
    if search:
        body['tools'] = [{'google_search': {}}]
    elif json_out:
        body['generationConfig']['responseMimeType'] = 'application/json'
    m = (os.environ.get('LLM_SEARCH_MODEL') or 'gemini-2.5-flash') if search else (mdl or model())  # free tier grounds search only on 2.5 Flash
    r = post_json(f'{G}/models/{m}:generateContent', body, headers=_gh())
    USAGE['calls'] += 1
    u = r.get('usageMetadata', {}); USAGE['in'] += u.get('promptTokenCount', 0); USAGE['out'] += u.get('candidatesTokenCount', 0)
    c = r['candidates'][0]
    text = ''.join(p.get('text', '') for p in c.get('content', {}).get('parts', []) if not p.get('thought'))
    out = _parse_json(text) if json_out else text
    if search:
        srcs = [ch.get('web', {}) for ch in c.get('groundingMetadata', {}).get('groundingChunks', [])]
        return out, srcs
    return out

def _openai(system, user, json_out, images, temperature):
    base = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
    content = [{'type': 'text', 'text': user}] + [
        {'type': 'image_url', 'image_url': {'url': f'data:{m};base64,{base64.b64encode(b).decode()}'}} for m, b in images]
    body = {'model': model(), 'temperature': temperature,
            'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': content}]}
    if json_out: body['response_format'] = {'type': 'json_object'}
    r = post_json(f'{base}/chat/completions', body, headers={'Authorization': f'Bearer {KEY}'})
    USAGE['calls'] += 1
    t = r['choices'][0]['message']['content']
    return _parse_json(t) if json_out else t
