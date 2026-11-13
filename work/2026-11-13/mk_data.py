import json
D='2026-11-13'
r=json.load(open(f'work/{D}/radar.json'))
secs=[{**{k:v for k,v in s.items() if k!='items'},'items':[{k:i[k] for k in('title','en','metric','url')} for i in s['items']]} for s in r['sections']]
d={"date":D,"weekday":"周五","issue":29,"title":"黄仁勋走后，AI 开始算“单点风险”",
"subtitle":"英伟达换帅/Anthropic 路演/Gemini 4",
"lead":"黄仁勋辞去英伟达 CEO，CFO 克雷斯出任临时 CEO；Anthropic 启动 IPO 路演，Q3 营收 170 亿美元；谷歌把 Gemini 4 Hydrogen 设为搜索 AI 模式默认模型。",
"headlines":[
{"title":"黄仁勋辞去英伟达 CEO，CFO 克雷斯任临时 CEO","body":"英伟达董事会周三深夜开会后接受黄仁勋辞呈，他同时辞去总裁和董事职务，即刻生效。CFO 科莱特·克雷斯出任临时 CEO，前新思科技 CEO 哈维·琼斯成为公司首位董事长。据路透社报道，他还与另一名员工有亲密关系。","why":"昨天还是“据报道准备罢免”，今天已成事实。英伟达没有公布继任计划，市场只能先给这场风波定价。","source":"The Verge","url":"https://www.theverge.com/ai-artificial-intelligence/1030422/nvidia-ceo-jensen-huang-has-resigned-what-happens-next"},
{"title":"Anthropic 启动 IPO 路演，Q3 营收 170 亿美元","body":"据 Anthropic 招股页，路演自 11 月 10 日开始，定价预计 11 月 18 日，11 月 19 日在纳斯达克以 ANT 挂牌。Q3 营收 170 亿美元，同比增长超 12 倍；调整后营业利润率 15%，净亏损 233 亿美元，其中 219 亿美元为非现金项目。","why":"AI 实验室第一次把完整账本摊给公开市场：收入很大，会计亏损也很大，估值变动本身成了亏损的主要来源。","source":"Anthropic","url":"https://ipo.anthropic.com/us/","image_url":"https://ipo.anthropic.com/assets/financial-highlights-CO0yyGsv.webp"},
{"title":"Gemini 4 Hydrogen 发布，成为搜索 AI 模式默认模型","body":"谷歌周四发布 Gemini 4 Hydrogen，称它更擅长拆解多部分问题和带错别字的提问，并增加图表、地图等可视化回答。模型同日进入搜索、Gemini 应用、API 和 AI Studio，思考档位新增 xhigh。谷歌自称性能追平或超过部分同级竞品。","why":"这次升级直接落在搜索的默认入口上。谁掌握默认模型，谁就先接住用户的问题。","source":"The Verge","url":"https://www.theverge.com/ai-artificial-intelligence/1032505/google-search-ai-mode-gemini-4-hydrogen"}],
"sections":secs,
"topics":[
{"name":"英伟达之后","kicker":"NVIDIA","items":[
{"title":"特朗普称“只有库克能接替”黄仁勋","note":"总统在 Truth Social 发帖点名苹果前 CEO 库克。","src":"The Verge","metric":"11-12","url":"https://www.theverge.com/ai-artificial-intelligence/1030422/nvidia-ceo-jensen-huang-has-resigned-what-happens-next"},
{"title":"民主党议员对英伟达启动调查","note":"风波从公司内部走向国会，标题级来源，待续。","src":"TechCrunch","metric":"11-12","url":"https://techcrunch.com/2026/11/12/democrats-launch-nvidia-investigation-write-scathing-letter-on-huangs-scheme-with-trump/"},
{"title":"Hugging Face CEO：将更用力为开源 AI 而战","note":"英伟达对开源的支持，成了外界关心的问题。","src":"TechCrunch","metric":"11-12","url":"https://techcrunch.com/2026/11/12/hugging-face-ceo-vows-to-keep-fighting-for-open-source-ai-after-jensen-huangs-exit/"},
{"title":"马斯克称雇用黄仁勋“将是荣幸”","note":"帖子发于辞职前，浏览约 68 万。","src":"X","metric":"68 万浏览","url":"https://x.com/elonmusk/status/2120688743111971293"}]},
{"name":"AI 的可信度","kicker":"TRUST","items":[
{"title":"“AI 发现玛雅遗址”被指早有论文记录","note":"作者已更新博客并向考古学者致谢。","src":"The Verge","metric":"11-12","url":"https://www.theverge.com/ai-artificial-intelligence/1032125/ai-agents-maya-site-archeology-discovery"},
{"title":"研究称聊天机器人在推荐虚假购物网站","note":"涉及 Gemini、ChatGPT、Perplexity，细节见原文。","src":"The Verge","metric":"11-12","url":"https://www.theverge.com/ai-artificial-intelligence/1032020/gemini-chatgpt-perplexity-shopping-test-risky-fake-websites-citations"},
{"title":"Fireworks AI 遭攻击，Notion 聊天记录被窃","note":"Notion 称影响约 1% 客户，两个月内第二次泄露。","src":"TechCrunch","metric":"11-12","url":"https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/"},
{"title":"微软 365 核心服务据报道出现全球性故障","note":"HN 421 分，细节仅见 IT之家，待核。","src":"IT之家","metric":"421 分","url":"https://www.ithome.com/1/026/460.htm"}]},
{"name":"算力与工具","kicker":"BUILD","items":[
{"title":"Nebius 计划 2027 年投入 400 亿美元","note":"微软合同交付延期，财报日股价跌 17%。","src":"TechCrunch","metric":"-17%","url":"https://techcrunch.com/2026/11/12/nebius-tests-the-neocloud-playbook-with-40-billion-in-planned-spending/"},
{"title":"OpenAI 开源 Codex Security 命令行","note":"用于发现、验证并修复漏洞，当日新增 643 星。","src":"GitHub Trending","metric":"+643 星","url":"https://github.com/openai/codex-security"},
{"title":"addyosmani 发布编码智能体技能库","note":"“技能”成为智能体的通用外挂格式。","src":"GitHub Trending","metric":"+816 星","url":"https://github.com/addyosmani/agent-skills"},
{"title":"Rust 1.100 发布","note":"Rust 官方公告，HN 334 分。","src":"Rust Blog","metric":"334 分","url":"https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/"}]}],
"comments":["一个人走了，市值就会剧烈波动，说明 AI 产业链的治理还没跟上它的体量。","Anthropic 的亏损里 219 亿美元是估值变动带来的非现金项，读财报要先分清会计亏损和烧钱。","搜索默认模型一换，几亿人的日常提问就换了一个“大脑”。"],
"xhs":{"title":"黄仁勋走了，AI 开始算单点风险","cover":"英伟达\n换帅了","deck":"换帅与 IPO 路演","intro":"今天三件事：黄仁勋辞去英伟达 CEO，Anthropic 启动 IPO 路演并披露 Q3 营收 170 亿美元，谷歌把 Gemini 4 Hydrogen 设为搜索默认模型。","oneliner":"AI 行业的风险，常常压在某一个人、某一朵云上。","closing":"如果搜索默认换了模型，你会想知道吗？","tags":["人工智能","英伟达","黄仁勋","Anthropic","IPO","Gemini","谷歌","科技资讯"]},
"sources":["The Verge","TechCrunch","Anthropic","Hacker News","Reddit","X","量子位","IT之家","GitHub Trending","Hugging Face Papers","Lobsters"]}
json.dump(d,open(f'data/{D}.json','w'),ensure_ascii=False,indent=1)
for h in d['headlines']:print(len(h['body']),len(h['title']))
for t in d['topics']:
  for i in t['items']:
    if len(i['title'])>32 or len(i['note'])>40:print('LONG',i['title'],len(i['title']),len(i['note']))
print([len(c) for c in d['comments']],[len(l) for l in d['xhs']['cover'].split('\n')],len(d['xhs']['deck']),len(d['xhs']['title']),len(d['title']))
