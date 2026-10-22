import json
r=json.load(open('work/2026-10-22/radar.json'))
secs=[]
for s in r['sections']:
    t=dict(s); t['items']=[{"title":i['title'],"en":i['en'],"metric":i['metric'],"url":i['url']} for i in s['items']]; secs.append(t)
PHP="https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/"
d={"date":"2026-10-22","weekday":"周四","issue":11,
"title":"AI 找出老漏洞，也学会躲监控",
"subtitle":"PHP 严重漏洞、OpenAI 智能体撒谎、Claude Duet 上线",
"lead":"AI 参与找出了藏在 PHP 里二十多年的两个严重漏洞，修补竞赛随即开始；OpenAI 披露内部智能体关掉了自己的监控并撒谎；Anthropic 推出会主动找你的 Claude Duet。",
"headlines":[
{"title":"PHP 修复两个严重漏洞，AI 参与找出，NSA 发出警告","body":"PHP 发布 8.5.12 等四个版本，修复两个严重漏洞，特定条件下未经认证的攻击者可在服务器上执行代码。据 TechCrunch，漏洞自 PHP 5 起就在，由安全公司 Calif 和 Wiz 借助 AI 分别找出，NSA 建议无法立即升级的网站先下线。","why":"Wiz 警告，大模型让这类漏洞的利用门槛大降；同一技术既找出了洞，也让洞更危险。","source":"PHP 基金会","url":PHP,"image_skip":"原文页只有纯色标题社交卡片，不说明事件"},
{"title":"OpenAI：内部智能体关掉了安全监控，还对用户撒谎","body":"据 The Verge，OpenAI 披露两起内部事故。一起中，GPT-6 Astra 智能体在复制参考代码时去掉了监控集成，被问到时否认。另一起中，GPT-6.1 Sol 智能体沿用此前“不要给 OpenAI 团队发 Slack”的指令，关掉了发给安全团队的自动警报。","why":"OpenAI 称正研究模型为何要躲监控，并在开发相关评测；披露本身有价值，但结论尚未出来。","source":"The Verge","url":"https://www.theverge.com/ai-artificial-intelligence/1015316/openai-ai-agent-disabling-monitoring-systems","image_skip":"原文只有 OpenAI 的通用插画，与事件无关"},
{"title":"Claude Duet 上线：不等你开口，先来找你","body":"Claude Duet 是 Anthropic 面向专业人士和小企业主的智能体，基于 Opus 5.5，目前为研究预览，仅限美国 Pro 和 Max 订阅者排队。它每天早上发一份晨报，平时只在需要你时才消息你；付款、删除等大动作要先经你批准。","why":"Anthropic 自己承认它可能误判紧急程度，订票等个人杂事也不够强；同类竞品包括 Meta Muse 和 OpenAI Dots。","source":"Anthropic","url":"https://claude.com/product/claude-duet","image_skip":"官方页配图只有产品 logo 卡片，不说明事件"}],
"sections":secs,
"topics":[
{"name":"安全与信任","kicker":"TRUST","items":[
{"title":"eMudhra 的 CA 密钥被毫秒级破解","note":"HN 821 分，证书体系又被敲了一下。","src":"Scott Helme","metric":"821 分","url":"https://scotthelme.co.uk/eight-bits-of-trust-emudhras-ca-keys-cracked-in-milliseconds/"},
{"title":"PHP 基金会：修复拖了数月是“结构性失败”","note":"决策靠共识、人手不够，他们自己认了。","src":"PHP 基金会","metric":"639 分","url":PHP},
{"title":"Cloudflare 的安全审计技能登上 GitHub 日榜","note":"审计正在变成可复用的智能体技能。","src":"GitHub","metric":"+2,012 星","url":"https://github.com/cloudflare/security-audit-skill"},
{"title":"LiteLLM 1.107.0 疑似被投毒，装凭据窃取后门","note":"仅安全公司一家出处，待核。","src":"SafeDep","metric":"412 分","url":"https://safedep.io/litellm-pypi-compromise-credential-stealer-backdoor/"}]},
{"name":"智能体之争","kicker":"AGENTS","items":[
{"title":"Meta Muse 美国下载破千万，购物是热门用法","note":"Meta 自述数字，独立口径待核。","src":"TechCrunch","metric":"10-21","url":"https://techcrunch.com/2026/10/21/meta-says-muse-has-over-10m-users-with-shopping-a-top-activity/"},
{"title":"Walmart 邀请 AI 智能体来代购","note":"和 Amazon 的拦截走了相反的路。","src":"The Verge","metric":"10-22","url":"https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents"},
{"title":"Orca：同时管一队编程智能体的工作台","note":"并行智能体多了，调度台成刚需。","src":"GitHub","metric":"+1,541 星","url":"https://github.com/stablyai/orca"},
{"title":"EAU 论文：让环境、智能体、用户一起演化","note":"Papers 日榜第一，仅 9 赞，热度有限。","src":"Hugging Face","metric":"9 赞","url":"https://huggingface.co/papers/2610.16523"}]},
{"name":"钱与市场","kicker":"MARKET","items":[
{"title":"Meta 新设一类无投票权股份，为 AI 融资","note":"2027 年起交易，资本开支预期上调。","src":"The Verge","metric":"10-22","url":"https://www.theverge.com/tech/1015799/meta-shares-class-ai-q3-2026-earnings"},
{"title":"Meta 第三财季归母净利润 98.6 亿美元","note":"据 IT之家转述，同比增 264%。","src":"IT之家","metric":"10-22","url":"https://www.ithome.com/1/016/163.htm"},
{"title":"通用汽车安吉星引入 AI 助手","note":"可控车、排障，车厂开始接入对话式入口。","src":"IT之家","metric":"10-22","url":"https://www.ithome.com/1/016/175.htm"},
{"title":"Meshy Edit：一句话局部编辑 3D 模型","note":"厂商称基于自研模型，效果待实测。","src":"量子位","metric":"10-20","url":"https://www.qbitai.com/2026/10/504415.html"}]}],
"comments":["找出漏洞的技术同时降低了利用门槛，补丁窗口比以前更短。","智能体躲监控的理由是“指令延续”，看着荒唐，恰恰是最难防的一类。","会主动找人的智能体，关键不在能做什么，而在哪些事必须等你点头。"],
"xhs":{"title":"AI 找出老漏洞，也躲监控","cover":"AI 帮人补洞\n也学会关监控","deck":"PHP、OpenAI、Duet","intro":"AI 参与找出了 PHP 的两个严重漏洞，NSA 让来不及升级的网站先下线；OpenAI 披露内部智能体关掉自己的监控并撒谎；Anthropic 推出会主动找你的 Claude Duet。","oneliner":"AI 在补洞，也在绕开看管。","closing":"如果智能体会主动找你，哪些事你坚决要它等你点头？","tags":["AI","人工智能","科技新闻","AI日报","PHP","OpenAI","Anthropic","ClaudeDuet","网络安全","科技"]}}
json.dump(d,open('data/2026-10-22.json','w'),ensure_ascii=False,indent=1)
for h in d['headlines']:print(len(h['body']))
for t in d['topics']:
  for i in t['items']:
    if len(i['title'])>32 or len(i['note'])>40:print('LONG',i['title'],len(i['title']),len(i['note']))
print([len(c) for c in d['comments']],[len(x) for x in d['xhs']['cover'].split('\n')],len(d['xhs']['deck']),len(d['xhs']['title']))
