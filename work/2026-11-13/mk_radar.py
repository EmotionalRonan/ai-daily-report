import json
D='2026-11-13'
old=json.load(open('work/2026-11-12/radar.json'))
meta={s['key']:s for s in old['sections']}
def sec(key,items):
    m={k:v for k,v in meta[key].items() if k!='items'}
    m['items']=[dict(zip(['title','en','metric','url','time','what'],i)) for i in items]
    return m
S=[
sec('hn',[
("英伟达 CEO 黄仁勋辞职","Jensen Huang resigns","2767 分","https://apnews.com/article/nvidia-megaspeed-china-singapore-huang-5403f152a601cf82ce939f1d24fffa0f","11-12","美联社报道黄仁勋辞去 CEO。"),
("Anthropic 公开招股网站上线","Anthropic IPO","792 分","https://ipo.anthropic.com/us/","11-12","披露 Q3 营收、路演与上市时间表。"),
("谷歌发布 Gemini 4 Hydrogen","Gemini 4 Hydrogen","437 分","https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/","11-12","谷歌新模型，进入搜索与 API。"),
("微软 365 服务降级","Service degradation on Microsoft 365","421 分","https://status.cloud.microsoft/","11-12","微软状态页显示服务异常。"),
("Rust 1.100 发布","Rust 1.100","334 分","https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/","11-12","Rust 官方发布 1.100 版本。")]),
sec('reddit',[
("GTA 5、使命召唤等被 AI 逆向移植到浏览器","GTA 5, Modern Warfare 2, Halo ported to browser via AI reverse-engineering","820 赞","https://www.destructoid.com/vibe-coded-games-in-browsers/","11-12","r/singularity 热帖，来源 Destructoid。"),
("用 Opus 5.5 把星际火狐等老游戏移植到桌面","Opus 5.5 is INSANE at decompilation / ports","656 赞","https://www.reddit.com/r/ClaudeAI/comments/1x3nkty/opus_55_is_insane_at_decompilation_ports/","11-12","作者自述；后又更正“反编译”说法。"),
("OpenAI 用量限制投票，网友称“谢天谢地”","Thank god","485 赞","https://i.redd.it/7k83wzkkbvuh1.jpeg","11-12","r/OpenAI 讨论每周限额与 5 小时限制。"),
("Claude 项目功能改版引用户反对","New Projects rolling out for Chat and Cowork","358 赞","https://www.reddit.com/gallery/1x33na4","11-11","r/ClaudeAI 用户抗议项目内对话互通。"),
("10–16GB 显存可跑模型排行","Every Model That Can Be Run On 10-16GB VRAM Ranked","347 赞","https://www.reddit.com/r/LocalLLaMA/comments/1x3gpyi/every_model_that_can_be_run_on_1016gb_vram_ranked/","11-12","作者主观评测，偏角色扮演。")]),
sec('x',[
("马斯克回应“请雇用黄仁勋”：“那将是荣幸”","Elon Musk: That would be an honor","68 万浏览","https://x.com/elonmusk/status/2120688743111971293","11-12","回复 zerohedge；转述自 Business Insider 等。"),
("英伟达官方宣布 CEO 交接的帖子","Nvidia announces CEO transition","6 万赞（转述）","https://ailately.com/rn","11-12","据 Ai Lately 统计；转述。"),
("Hugging Face CEO：将更用力为开源 AI 而战","Clem Delangue on Huang's exit","转述","https://www.usatoday.com/story/tech/2026/11/12/what-does-jensen-huangs-resignation-mean-for-ai/92739989007/","11-12","据 USA Today 转述其 X 帖。"),
("Grok 被问“间谍、妻子还是员工”，选了妻子","Grok's reply to Huang question","转述","https://www.ndtvprofit.com/trending/how-you-lose-a-4t-company-groks-savage-reply-to-spy-wife-or-employee-question-about-jensen-huang-12316557","11-12","NDTV Profit 报道的 X 热帖。"),
("Perplexity CEO 感谢黄仁勋","Aravind Srinivas on Huang","转述","https://www.hindustantimes.com/trending/us/your-grit-and-perseverance-should-always-be-remembered-perplexity-ceo-aravind-srinivas-after-jensen-huang-resigns-as-nvidia-ceo-101794503589143.html","11-12","Hindustan Times 转述其 X 帖。")]),
sec('github',[
("Meta 开源设计系统 astryx","meta/astryx","+1830 星","https://github.com/meta/astryx","11-12","可定制、面向智能体的开源设计系统。"),
("个人理财应用 sure","we-promise/sure","+967 星","https://github.com/we-promise/sure","11-12","开源个人理财应用。"),
("面向编码智能体的工程技能库","addyosmani/agent-skills","+816 星","https://github.com/addyosmani/agent-skills","11-12","生产级工程技能集合。"),
("谷歌 Chrome：让编码智能体跟上网页最佳实践","GoogleChrome/modern-web-guidance-src","+739 星","https://github.com/GoogleChrome/modern-web-guidance-src","11-12","Chrome 团队的网页开发指南源码。"),
("OpenAI Codex Security 命令行与 SDK","openai/codex-security","+643 星","https://github.com/openai/codex-security","11-12","用于发现、验证并修复安全漏洞。")]),
sec('hf',[
("为长期运行的智能体自适应调度大模型服务","Evolving Infra: Agent-Adaptive LLM Serving at Scale","11 赞","https://huggingface.co/papers/2611.12304","11-12","论文。"),
("对齐在 Transformer 的何处出现","Where Does Alignment Emerge and What Does It Mean?","6 赞","https://huggingface.co/papers/2611.12869","11-12","论文。"),
("面向实时模型预测控制的 GPU 加速二次规划求解器","FAME-QP","4 赞","https://huggingface.co/papers/2611.13766","11-13","论文。"),
("在不确定的解码步骤提升权重精度","Precision on Demand","4 赞","https://huggingface.co/papers/2611.14418","11-13","论文。"),
("评测复杂购物建议的量表基准","CARTBench","3 赞","https://huggingface.co/papers/2611.05862","11-12","论文。")]),
sec('verge_tc',[
("谷歌新模型更擅长理解复杂问题","Google's new Gemini model is better at understanding complicated questions","The Verge","https://www.theverge.com/ai-artificial-intelligence/1032505/google-search-ai-mode-gemini-4-hydrogen","11-12","Gemini 4 Hydrogen 成为 AI 模式默认模型。"),
("不，AI 智能体并没有发现未知的玛雅遗址","No, AI agents did not discover a previously unknown Maya site","The Verge","https://www.theverge.com/ai-artificial-intelligence/1032125/ai-agents-maya-site-archeology-discovery","11-12","该遗址一年多前已有论文记录。"),
("Fireworks AI 遭攻击，Notion 用户聊天记录被窃","Cyberattack on Fireworks AI allowed hackers to access Notion customers' chat transcripts","TechCrunch","https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/","11-12","Fireworks 两个月内第二次数据泄露。"),
("Nebius 计划 2027 年投入 400 亿美元","Nebius tests the neocloud playbook with $40 billion in planned spending","TechCrunch","https://techcrunch.com/2026/11/12/nebius-tests-the-neocloud-playbook-with-40-billion-in-planned-spending/","11-12","财报日股价跌 17%。"),
("研究称 AI 聊天机器人在推荐虚假购物网站","AI chatbots are recommending fake retail websites, study finds","The Verge","https://www.theverge.com/ai-artificial-intelligence/1032020/gemini-chatgpt-perplexity-shopping-test-risky-fake-websites-citations","11-12","涉及 Gemini、ChatGPT、Perplexity。")]),
sec('qbitai',[
("Anthropic 启动 IPO 路演","Anthropic IPO roadshow","量子位","https://www.qbitai.com/2026/11/509381.html","11-12","量子位报道路演与估值。"),
("马斯克已准备好聘请黄仁勋","Musk ready to hire Huang","量子位","https://www.qbitai.com/2026/11/509334.html","11-12","报道黄仁勋风波与马斯克表态。"),
("Anthropic 玻璃翼计划被质疑：近 4 万个候补漏洞只修了 217 条","Project Glasswing questioned","量子位","https://www.qbitai.com/2026/11/509291.html","11-12","标题所述，未核。"),
("MiniMax 开源生图模型，原生 4K","MiniMax open-sources image model","量子位","https://www.qbitai.com/2026/11/509440.html","11-13","量子位标题所述，未核。"),
("Grok 泄露 SpaceX、特斯拉工资绩效","Grok leaks internal pay data","量子位","https://www.qbitai.com/2026/11/509355.html","11-12","量子位标题所述，未核。")]),
sec('ithome',[
("星舰明日第 15 次试飞，“筷子”首次挑战双级捕获","Starship Flight 15","IT之家","https://www.ithome.com/1/026/467.htm","11-13","IT之家报道。"),
("OpenAI、Anthropic、谷歌等五家 AI 巨头遭起诉","Five AI companies sued","IT之家","https://www.ithome.com/1/026/466.htm","11-13","原告要求叫停 ChatGPT、Gemini、Claude。"),
("Anthropic、OpenAI 遭专利诉讼，涉五项神经网络专利","Patent suit vs Anthropic, OpenAI","IT之家","https://www.ithome.com/1/026/464.htm","11-13","IT之家报道。"),
("英伟达总市值重回 4 万亿美元上方","Nvidia market cap back above $4T","IT之家","https://www.ithome.com/1/026/462.htm","11-13","此前曾在黄仁勋辞职后失守。"),
("微软 365 核心服务全球性瘫痪，正逐步恢复","Microsoft 365 outage","IT之家","https://www.ithome.com/1/026/460.htm","11-13","Outlook、OneDrive、Teams 受影响。")]),
sec('lobsters',[
("我是如何意外成为百万富翁的","How I accidentally became a millionaire","216 分","https://lyra.horse/blog/2026/11/disinformation-machine/","11-12","Lobsters 热帖。"),
("Rust 1.100.0 发布","Announcing Rust 1.100.0","58 分","https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/","11-12","官方公告。"),
("Baochip 入门","Hello Baochip","49 分","https://ratfactor.com/cards/hello-baochip","11-12","芯片入门笔记。"),
("《Let Over Lambda》全书免费上线","Let Over Lambda is now freely available","46 分","https://letoverlambda.com/","11-12","Lisp 宏经典。"),
("Gemini 协议的“反营销”面向","The anti-marketing aspect of the Gemini network","21 分","https://ploum.net/2026-11-12-anti-marketing-gemini.html","11-12","此 Gemini 为小众网络协议。")]),
]
cands=[
{"title":"黄仁勋辞去英伟达 CEO","url":"https://www.theverge.com/ai-artificial-intelligence/1030422/nvidia-ceo-jensen-huang-has-resigned-what-happens-next","why":"HN 2767 分；Verge 全文已读，董事会、临时 CEO、股价均可核。","pick":True,"status":"ok"},
{"title":"Anthropic IPO 路演与 Q3 财务","url":"https://ipo.anthropic.com/us/","why":"一手招股页：营收 170 亿美元、11 月 19 日挂牌 ANT。","pick":True,"status":"ok"},
{"title":"Gemini 4 Hydrogen 发布","url":"https://www.theverge.com/ai-artificial-intelligence/1032505/google-search-ai-mode-gemini-4-hydrogen","why":"HN 437 分；Verge 全文已读。","pick":True,"status":"ok"},
{"title":"玛雅遗址“发现”被指早有记录","url":"https://www.theverge.com/ai-artificial-intelligence/1032125/ai-agents-maya-site-archeology-discovery","why":"HN 910 分的帖子被 Verge 反驳；放专题。","pick":False,"status":"ok"},
{"title":"Nebius 2027 年 400 亿美元投入","url":"https://techcrunch.com/2026/11/12/nebius-tests-the-neocloud-playbook-with-40-billion-in-planned-spending/","why":"TC 全文已读；放专题。","pick":False,"status":"ok"},
{"title":"Fireworks AI 泄露 Notion 聊天记录","url":"https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/","why":"TC 全文已读；放专题。","pick":False,"status":"ok"},
{"title":"微软 365 大范围故障","url":"https://www.ithome.com/1/026/460.htm","why":"HN 421 分，仅标题级来源，待核细节。","pick":False,"status":"待核"},
]
json.dump({"sections":S,"candidates":cands},open(f'work/{D}/radar.json','w'),ensure_ascii=False,indent=1)
print('ok',len(S))
