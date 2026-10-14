import json,copy
old=json.load(open('data/2026-10-13.json'))
meta={s['key']:{k:v for k,v in s.items() if k!='items'} for s in old['sections']}
def I(t,e,m,u):return {"title":t,"en":e,"metric":m,"url":u}
hn=lambda i:"https://news.ycombinator.com/item?id=%s"%i
S={
'hn':[I("Gemini 4 Argon 发布","Gemini 4 Argon","916 分 · 703 评论",hn(50073879)),
 I("Rust 借用检查器被找出 11 年前的不健全漏洞","11 year old unsoundness bugs found in Rust borrow checker","656 分 · 365 评论",hn(50069499)),
 I("苹果发布 HomeView 智能家庭屏","Apple HomeView","637 分 · 759 评论",hn(50071017)),
 I("Firefox 推出企业版","Firefox Enterprise","615 分 · 254 评论",hn(50070302)),
 I("Anthropic 重新设计内部源码管理","Redesigning source control at Anthropic","480 分 · 477 评论",hn(50073633))],
'reddit':[I("GTA 5、使命召唤等游戏被 AI 逆向后移植到浏览器","r/singularity","820 赞 · 126 评论","https://www.reddit.com/r/singularity/comments/1x38qz0/gta_5_modern_warfare_2_halo_and_many_other_games/"),
 I("Opus 5.5 把星际火狐、索尼克 CD 移植到桌面","r/ClaudeAI","656 赞 · 232 评论","https://www.reddit.com/r/ClaudeAI/comments/1x3nkty/opus_55_is_insane_at_decompilation_ports/"),
 I("共用 Claude 账号后，他设了自定义指令","r/ClaudeAI","431 赞 · 128 评论","https://www.reddit.com/r/ClaudeAI/comments/1x395p7/claude_saved_my_marriage/"),
 I("Claude 项目功能改版，Max 用户喊“别动我的文件夹”","r/ClaudeAI","358 赞 · 143 评论","https://www.reddit.com/r/ClaudeAI/comments/1x33na4/new_projects_rolling_out_for_chat_and_cowork_oh/"),
 I("10–16GB 显存能跑的模型排行","r/LocalLLaMA","347 赞 · 85 评论","https://www.reddit.com/r/LocalLLaMA/comments/1x3gpyi/every_model_that_can_be_run_on_1016gb_vram_ranked/")],
'x':[I("X、Grok 与 Cursor 套餐合并为“The X Subscription”","@SpaceXSI","350万 浏览 · 1.35万 赞","https://x.com/SpaceXSI/status/2109783335296008414"),
 I("Zoho 创始人：软件业前景不明，今年不涨薪","@svembu","140万 浏览 · 1.17万 赞","https://x.com/svembu/status/2109770209703920008"),
 I("日本被报道宣布“网络空间紧急状态”（转述，待核）","@Polymarket","96万 浏览 · 1.43万 赞","https://x.com/Polymarket/status/2109748239931150347"),
 I("让 Claude 反编译 WHOOP 应用，它同意了","@uwwgo","55万 浏览 · 6300 赞","https://x.com/uwwgo/status/2109217632758976755")],
'github':[I("morluto/rea：用智能体逆向任何东西","Reverse engineer anything with agents","今日 +54,679 ⭐","https://github.com/morluto/rea"),
 I("bilawalsidhu/gods-eye-view：浏览器里的间谍卫星模拟器","Live open source spatial intelligence","今日 +1,961 ⭐","https://github.com/bilawalsidhu/gods-eye-view"),
 I("cathrynlavery/diagram-design：给编程智能体的 44 种图表","Editorial diagram design","今日 +1,815 ⭐","https://github.com/cathrynlavery/diagram-design"),
 I("debpalash/VoiceStudio：完全本地的 ElevenLabs 替代","Open-source local voice studio","今日 +1,748 ⭐","https://github.com/debpalash/VoiceStudio"),
 I("mksglu/context-mode：压缩编程智能体的上下文","Context window optimization","今日 +969 ⭐","https://github.com/mksglu/context-mode")],
'hf':[I("VIS-Ground：带上下文对齐的视频互动叙事","VIS-Ground","78 赞","https://huggingface.co/papers/2610.09326"),
 I("PR-OPD：用特权表示做智能体强化学习的自蒸馏","PR-OPD","24 赞","https://huggingface.co/papers/2609.36642"),
 I("CrossTimeEdit：跨十年的历史街景生成数据集","CrossTimeEdit","20 赞","https://huggingface.co/papers/2609.36616"),
 I("少训练多收获：不确定性引导的渐进收缩推理后训练","Uncertainty-Guided Progressive Contraction","7 赞","https://huggingface.co/papers/2610.12933"),
 I("分支式同策略蒸馏","Branching On-Policy Distillation","5 赞","https://huggingface.co/papers/2610.13481")],
'media':[I("OpenAI 员工因涉嫌在会议室装窃听器被捕","The Verge","10月13日","https://www.theverge.com/ai-artificial-intelligence/1010642/openai-employee-arrested-recording-device"),
 I("Shopify 向更多 AI 智能体开放商品目录","The Verge","10月13日","https://www.theverge.com/news/1010365/shopify-opens-its-catalog-up-to-more-ai-agents"),
 I("Facebook 将允许用 AI 定制你的信息流算法","The Verge","10月13日","https://www.theverge.com/tech/1010344/meta-facebook-your-algorithm-ai"),
 I("Cerebras CEO：人人都将拥有家用个人 AI 助手","TechCrunch","10月13日","https://techcrunch.com/2026/10/13/cerebras-ceo-says-were-nearing-a-future-where-everyone-has-a-personal-ai-assistant-at-home/"),
 I("Industrial Next 想让工厂机器人几分钟内切换任务","TechCrunch","10月13日","https://techcrunch.com/2026/10/13/industrial-next-wants-factory-robots-to-switch-tasks-in-minutes-not-weeks/")],
'qbit':[I("魔法原子具身 Agent 框架拿下 MolmoSpaces 全球第一","量子位","10月13日","https://www.qbitai.com/2026/10/503107.html"),
 I("梁文锋投了 Swin Transformer 作者，DeepSeek 开始布局具身大脑","量子位","10月13日","https://www.qbitai.com/2026/10/503093.html"),
 I("巴黎车展国产品牌独占三成，大众 CEO 呼吁抱团","量子位","10月13日","https://www.qbitai.com/2026/10/502992.html"),
 I("华为哈勃投了位 98 年博士，让机器人皮肤变色","量子位","10月13日","https://www.qbitai.com/2026/10/502954.html"),
 I("Claude 团队实测：AI 全自主复制进智能家电","量子位","10月13日","https://www.qbitai.com/2026/10/502920.html")],
'ithome':[I("苹果诉 OpenAI 窃取商业秘密案：法院准许调取招聘材料","IT之家","10月14日","https://www.ithome.com/1/012/643.htm"),
 I("IT早报：麒麟 9050 Pro 架构图公布，苹果 HomeView 发布","IT之家","10月14日","https://www.ithome.com/1/012/642.htm"),
 I("IDC：2026Q3 中国智能手机出货跌 15.4%，华为逆势涨 17.3%","IT之家","10月13日","https://www.ithome.com/1/012/376.htm"),
 I("Neuralink 前总裁的视力芯片，让患者重新读出单词","IT之家","10月14日","https://www.ithome.com/1/012/641.htm"),
 I("扎克伯格：Meta 豪赌数千亿美元，一度没把握能成","IT之家","10月14日","https://www.ithome.com/1/012/640.htm")],
'lobsters':[I("vfmaddrnd231pd 是谁？","Who is vfmaddrnd231pd??","70 分","https://lobste.rs/s/2h9opx/who_is_vfmaddrnd231pd"),
 I("请不要使用 uv-build","A plea not to use uv-build","64 分","https://lobste.rs/s/73ssw1/plea_not_use_uv_build"),
 I("Ente Locker 是否未署名抄了我的代码？","Did Ente Locker copy my code without attribution?","64 分","https://lobste.rs/s/uiulqe/did_ente_locker_copy_my_code_without"),
 I("回滚会继续，直到士气好转","The reverts will continue until morale improves","39 分","https://lobste.rs/s/aasanp/reverts_will_continue_until_morale"),
 I("那些新的好软件都去哪了？","Where is all the new, good software?","36 分","https://lobste.rs/s/hjhufj/where_is_all_new_good_software")]}
d={"date":"2026-10-14","weekday":"周三","issue":3,
"title":"代码涨十倍，应用层却在倒下",
"subtitle":"Gemini 4 Argon、Anthropic 自研版本控制、Character.ai 破产出售",
"lead":"谷歌发布 Gemini 4 Argon，Anthropic 披露内部每天合并三万多个代码改动；同一天，AI 角色聊天应用 Character.ai 申请破产出售。模型和代码在加速，靠模型吃饭的应用层并不都撑得住。",
"headlines":[
{"title":"谷歌发布 Gemini 4 Argon，编码与长上下文成绩领先但并非全胜","body":"谷歌 DeepMind 发布 Gemini 4 Argon，先向 Google AI Pro 与 Ultra 订阅用户开放。官方对比中 DeepSWE 77.9%、Vals Index 68.9% 居首，但 FrontierSWE v2、Terminal-bench 4.0 落后于 GPT-6 Astra 或 Opus 5.5。","why":"成绩单是谷歌自己挑的，赢多输少；Chrome 六百万行代码重构这类案例，比分数更值得看。独立评测出来前，不必急着换模型。","source":"Google DeepMind","url":"https://deepmind.google/models/gemini/"},
{"title":"Anthropic 自研 Scion 取代 git：日合并量一年内涨十倍","body":"Anthropic 工程博客称，内部日合并代码改动从 5 月约 2,500 个增至 9 月超 3 万个，git 成了瓶颈。7 人团队用 5 个月自研版本控制系统 Scion，迁走整个 monorepo，CPU 与内存规模降到原镜像方案的 1/200。","why":"写代码不再是瓶颈，合并、测试、审核才是。同时他们也明说：Scion 只适合超大 monorepo，不是 git 的通用替代。","source":"Anthropic Engineering","url":"https://www.anthropic.com/engineering/redesigning-source-control"},
{"title":"Character.ai 启动 Chapter 11，平台暂时照常运行","body":"Character.ai 宣布自愿启动 Chapter 11 破产程序，通过法院监督出售公司。官方称平台暂时照常运行，订阅与计费不变，预计 11 月底或 12 月初完成出售；若没有可行报价，平台将被关停。用户可导出数据或删除账号。","why":"这是应用层的风险提示：模型越来越强，不等于靠模型做产品的公司都活得下来。在用的人，先把聊天记录导出来。","source":"Character.ai 官方博客","url":"https://blog.character.ai/an-update-on-character-ai/"}],
"sections":[dict(meta[k],items=S[k]) for k in ['hn','reddit','x','github','hf','media','qbit','ithome','lobsters']],
"topics":[
{"name":"AI 写代码的另一面","kicker":"CODE","items":[
 {"title":"Opus 5.5 把星际火狐、索尼克 CD 移植到桌面","note":"作者自己改口：更像专用模拟器，不算干净反编译。","src":"Reddit r/ClaudeAI","metric":"656 赞","url":"https://www.reddit.com/r/ClaudeAI/comments/1x3nkty/opus_55_is_insane_at_decompilation_ports/"},
 {"title":"Xbox 公开拥抱 AI 游戏移植与反编译","note":"微软给“AI 移植老游戏”盖了官方章。","src":"The Verge","metric":"10月13日","url":"https://www.theverge.com/news/1010406/xbox-labs-game-decompiling-emulation-exploration"},
 {"title":"Google Play 让 vibe coding 应用易上架","note":"写应用越来越快，上架这一步也在让路。","src":"The Verge","metric":"10月13日","url":"https://www.theverge.com/tech/1009066/google-play-vibe-coded-android-apps-launch"}]},
{"name":"窃听、窃密、植入","kicker":"SECURITY","items":[
 {"title":"OpenAI 工程师被控在高管会议室藏录音设备","note":"检方指控，尚未定罪；设备 9 月 30 日被发现。","src":"SF Standard","metric":"10月13日","url":"https://sfstandard.com/2026/10/13/openai-engineer-arrested-alleged-bugging-executive-conference-room/"},
 {"title":"法院裁定 OpenAI 须向苹果提交招聘材料","note":"已收集的 5 天内交，其余 14 天内。","src":"TechCrunch","metric":"10月13日","url":"https://techcrunch.com/2026/10/13/judge-orders-openai-to-turn-over-hiring-records-in-apple-trade-secrets-case/"},
 {"title":"Ledger 确认经销商渠道的钱包被植入间谍芯片","note":"被篡改的设备售价近原价的一半。","src":"BleepingComputer","metric":"10月12日","url":"https://www.bleepingcomputer.com/news/security/ledger-confirms-hardware-wallet-spy-implant-behind-crypto-thefts/"}]},
{"name":"硬件进家门","kicker":"HARDWARE","items":[
 {"title":"苹果 HomeView 发布，11 月 13 日开售","note":"7 英寸屏、A18 芯片，能识别最多 6 人；Siri AI 先出英语版。","src":"Apple","metric":"HN 637 分","url":"https://www.apple.com/apple-homeview/"},
 {"title":"Science Corp 首例 Stargardt 患者植芯片","note":"创始人 Max Hodak 是 Neuralink 前总裁。","src":"TechCrunch","metric":"10月13日","url":"https://techcrunch.com/2026/10/13/science-corporation-implants-its-vision-restoring-chip-in-its-first-stargardt-disease-patient/"},
 {"title":"Cerebras CEO：人人家里都会有个人 AI 助手","note":"他是卖芯片的，判断先打个折听。","src":"TechCrunch","metric":"10月13日","url":"https://techcrunch.com/2026/10/13/cerebras-ceo-says-were-nearing-a-future-where-everyone-has-a-personal-ai-assistant-at-home/"}]}],
"comments":["对比表是谷歌自己选的，两项编码测试没赢。等独立评测再下结论。","Scion 那篇值得细读：不是模型多强，而是 git 先扛不住了。合并、测试、审核成了新瓶颈。","Character.ai 公告里订阅照常、数据可导出。在用这类应用的人，现在就导一份聊天记录。"],
"xhs":{"title":"代码涨十倍，应用层先倒了","cover":"代码涨十倍\n基建先扛不住","deck":"Gemini 4 与 Scion","intro":"Anthropic 内部每天合并 3 万多个代码改动，git 先扛不住了；谷歌发了 Gemini 4 Argon；Character.ai 却申请了破产出售。","oneliner":"模型和代码在加速，靠模型吃饭的产品，不一定跟得上。","closing":"你在用的 AI 应用里，有没有哪个让你担心它哪天会关停？","tags":["AI","人工智能","AI编程","科技新闻","AI日报","Gemini","Anthropic","CharacterAI","程序员","开源"]}}
json.dump(d,open('data/2026-10-14.json','w'),ensure_ascii=False,indent=1)
for h in d['headlines']:print(len(h['body']))
for t in d['topics']:
  for i in t['items']:
    if len(i['title'])>32 or len(i['note'])>40:print('LONG',len(i['title']),len(i['note']),i['title'])
for c in d['comments']:print('c',len(c))
x=d['xhs'];print(len(x['title']),[len(l) for l in x['cover'].split('\n')],len(x['deck']))
