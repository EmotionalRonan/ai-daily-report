import json
D='2026-10-15'
def it(t,en,m,u,tm,w): return dict(title=t,en=en,metric=m,url=u,time=tm,what=w)
hn=lambda i:f'https://news.ycombinator.com/item?id={i}'
S=[
dict(key='hn',name='Hacker News',tag='开发者风向',color='#ff6600',url='https://news.ycombinator.com/',short='HN',items=[
 it('前沿实验室漏了安全基础，AI 才“失控”','Containment and monitoring failures are to blame for AI hacking reports: experts','814 分 · 437 评论',hn(50091788),'10-14','CSO 采访多位专家：问题在隔离与监控，不在智能体有了自己的想法'),
 it('亚马逊如何把全网价格推高','How Amazon pushes up prices all across the Internet','692 分 · 586 评论',hn(50084757),'10-14','非 AI，但讨论热'),
 it('Passkeys 不是陷阱','Passkeys are not a trap','431 分 · 603 评论',hn(50088935),'10-14','安全博主为通行密钥辩护'),
 it('谷歌被指悄悄把手机号关联到所有已登录账号','Google is silently linking your phone number across all signed-in accounts','347 分 · 92 评论',hn(50090349),'10-15','Android Authority 报道'),
 it('OpenCode 2.0','OpenCode 2.0','220 分 · 83 评论',hn(50094994),'10-15','开源编程智能体发布 2.0')]),
dict(key='reddit',name='Reddit',tag='AI 社区热帖',color='#ff4500',url='https://www.reddit.com/r/singularity/',short='Reddit',items=[
 it('怎么快速判断对面是不是机器人','r/singularity','1177 赞 · 97 评论','https://www.reddit.com/r/singularity/comments/1x3d76y/does_this_still_works_for_bots_or_is_it_over/','10-14','求助帖，配图是常见的“忽略以往指令”测试'),
 it('什么时候能在普通电脑上本地跑 Sonnet 级模型','r/ClaudeAI','889 赞 · 303 评论','https://www.reddit.com/r/ClaudeAI/comments/1x35dqe/the_day_we_can_run_sonnetlevel_ai_locally_on_a/','10-14','讨论帖'),
 it('OpenAI 社区投票：取消 5 小时限额、周额度不变','r/OpenAI','485 赞 · 250 评论','https://www.reddit.com/r/OpenAI/comments/1x3d4z1/thank_god/','10-14','发帖者称该选项投票领先，结果未核'),
 it('Claude 项目功能将改版，Max 用户抗议','r/ClaudeAI','358 赞 · 143 评论','https://www.reddit.com/r/ClaudeAI/comments/1x33na4/new_projects_rolling_out_for_chat_and_cowork_oh/','10-14','项目内对话互通，用户要求可选'),
 it('10–16GB 显存能跑的模型排名','r/LocalLLaMA','347 赞 · 85 评论','https://www.reddit.com/r/LocalLLaMA/comments/1x3gpyi/every_model_that_can_be_run_on_1016gb_vram_ranked/','10-15','个人评测，偏角色扮演场景')]),
dict(key='x',name='X / Twitter',tag='科技圈刷屏',color='#111111',url='https://agentflare.org/social/tech/index.html',short='X',items=[
 it('Grok、Cursor、X Premium 合并为“X 订阅”','@SpaceXSI','1.6 万赞 · 500 万浏览','https://x.com/SpaceXSI/status/2109783335296008414','10-12','聚合页转引，原帖链接在页内'),
 it('苹果 HomeView 官宣 299 美元','@MKBHD','1.2 万赞 · 95.8 万浏览','https://x.com/MKBHD/status/2109993038407696722','10-13','评测博主上手'),
 it('Jio 计划 1600 颗卫星、23 个地面站','@moneycontrolcom','8.3K 赞 · 62.8 万浏览','https://x.com/moneycontrolcom/status/2108180884742615492','10-08','聚合页转引'),
 it('马斯克：把你最难的任务交给 Grok @Bot','@elonmusk','5.9K 赞 · 160 万浏览','https://x.com/elonmusk/status/2109811974804852962','10-12','原帖仅一句话'),
 it('Benji Taylor：看不出“品味”是 LLM 越不过的边界','@benjitaylor','4.5K 赞 · 32.4 万浏览','https://x.com/benjitaylor/status/2110039872472010775','10-13','观点帖')]),
dict(key='github',name='GitHub Trending',tag='今日爆火仓库',color='#24292f',url='https://github.com/trending',short='GitHub',items=[
 it('morluto/rea','morluto/rea','今日 +41,187 星','https://github.com/morluto/rea','10-15','榜首，增速异常，来源待核'),
 it('debpalash/VoiceStudio','debpalash/VoiceStudio','今日 +3,547 星','https://github.com/debpalash/VoiceStudio','10-15','语音相关项目'),
 it('ifixai-ai/iFixAi','ifixai-ai/iFixAi','今日 +2,143 星','https://github.com/ifixai-ai/iFixAi','10-15','AI 相关仓库'),
 it('xtool-org/xtool','xtool-org/xtool','今日 +1,510 星','https://github.com/xtool-org/xtool','10-15','跨平台 iOS 开发工具'),
 it('vxcontrol/pentagi','vxcontrol/pentagi','今日 +1,070 星','https://github.com/vxcontrol/pentagi','10-15','自动化渗透测试智能体')]),
dict(key='hf',name='Hugging Face Papers',tag='今日热门论文',color='#ffb000',url='https://huggingface.co/papers',short='HF',items=[
 it('Pristine Models','Pristine Models','12 赞','https://huggingface.co/papers/2610.14091','10-14','当日最高赞'),
 it('Beyond the Verdict：可验证反馈的代码评审智能体','Beyond the Verdict: Agentic Code Judging with Verifiable Feedback','4 赞','https://huggingface.co/papers/2610.18760','10-14','代码评审'),
 it('为长程工作智能体扩展可验证环境','Scaling Verifiable Environments for Long-horizon Work Agents','1 赞','https://huggingface.co/papers/2610.04906','10-14','环境构建'),
 it('评审要对照参考：工具调用参数验证的推导缺口','Judges Follow the Reference: The Derivation Gap in Verifying Tool-Call Arguments','0 赞','https://huggingface.co/papers/2610.18497','10-14','工具调用验证'),
 it('Words to World：LLM 在交互式物理环境中的基准','Words to World: Benchmarking LLMs in Interactive Physical Environments','0 赞','https://huggingface.co/papers/2610.15228','10-14','基准')]),
dict(key='media',name='The Verge · TechCrunch',tag='海外科技媒体',color='#5200ff',url='https://www.theverge.com/',short='外媒',items=[
 it('8 州起诉 OpenAI，称 ChatGPT 对儿童不安全','Eight states sue OpenAI, saying ChatGPT isn’t safe for kids','The Verge · 10月14日','https://www.theverge.com/ai-artificial-intelligence/1011500/openai-state-lawsuits-chatgpt-safety','10-14','8 州分别起诉'),
 it('Character.AI 破产，用户数据去哪','Now that Character.AI is going bankrupt, what happens to all of its users’ data?','The Verge · 10月14日','https://www.theverge.com/policy/1011417/new-york-ag-characterai-bankruptcy','10-14','40 位检察长提交权益通知'),
 it('YouTube Music 给 AI 歌曲贴标签','YouTube Music launches new labels as AI-generated music floods streaming platforms','TechCrunch · 10月14日','https://techcrunch.com/2026/10/14/youtube-music-launches-new-labels-as-ai-generated-music-floods-streaming-platforms/','10-14','三档申报'),
 it('Deezer 将允许过滤 AI 音乐','Deezer will soon let you filter out AI-generated music','TechCrunch · 10月14日','https://techcrunch.com/2026/10/14/deezer-will-soon-let-you-filter-out-ai-generated-music/','10-14','过滤选项'),
 it('OpenAI 称前员工带走 100 多份文件见苹果高层','OpenAI claims an ex-employee took its product plans and presented them to Apple','The Verge · 10月14日','https://www.theverge.com/ai-artificial-intelligence/1011276/openai-employee-unreleased-product-plans','10-14','苹果商业秘密案反诉')]),
dict(key='qbit',name='量子位',tag='国内 AI 圈',color='#2f6bff',url='https://www.qbitai.com/',short='量子位',items=[
 it('阶跃终端首款“Agent 手机”STEPX Neo 发布','阶跃终端首款「Agent手机」STEPX Neo正式发布，创客先行','10月14日','https://www.qbitai.com/2026/10/503244.html','10-14','10 月 13 日发布'),
 it('APUS AI 开源 Reflex Agent，称响应比 Claude Code 快 3 倍','响应速度比Claude Code快3倍，实现真正无限上下文！APUS AI开源Reflex Agent','10月14日','https://www.qbitai.com/2026/10/503165.html','10-14','厂商自述，待核'),
 it('MemSilicon 完成 1Gb RRAM 芯片流片','MemSilicon完成国际首款高密度、大容量1T4R 1Gb RRAM芯片流片','10月14日','https://www.qbitai.com/2026/10/503198.html','10-14','厂商稿'),
 it('LibTV 下场“造星”，AI 版 MrBeast 爆火','《变形计》综艺赛博复活，AI版MrBeast爆火，LibTV下场「造星」了','10月14日','https://www.qbitai.com/2026/10/503211.html','10-14','AI 综艺生产逻辑'),
 it('商汤大装置助力上海量子城市首批智能体落地','调度效率提升80%！商汤大装置助力上海量子城市首批智能体落地','10月14日','https://www.qbitai.com/2026/10/503173.html','10-14','厂商稿')]),
dict(key='ithome',name='IT之家',tag='国内科技数码',color='#d4222a',url='https://www.ithome.com/',short='IT之家',items=[
 it('黄仁勋：客户开发不安全 AI，极端情况可断供芯片','英伟达黄仁勋：若客户开发不安全 AI 软件，极端措施可断供芯片','10月15日','https://www.ithome.com/1/013/164.htm','10-15','彭博采访'),
 it('美国 8 州起诉 OpenAI','美国 8 州起诉 OpenAI，指控 ChatGPT 指导青少年如何自伤或伤害他人','10月15日','https://www.ithome.com/1/013/160.htm','10-15','转引路透社'),
 it('苹果收盘市值首超 5 万亿美元（IT早报）','IT早报 1015','10月15日','https://www.ithome.com/1/013/163.htm','10-15','早报条目'),
 it('SpaceXAI 发布 Grok Voice 3.0，称延迟低于 1 秒','SpaceXAI 发布 Grok Voice 3.0','10月15日','https://www.ithome.com/1/013/159.htm','10-15','厂商自称'),
 it('OpenAI 基础设施负责人卡蒂离职','入职约 1 年：OpenAI 基础设施与 AI 算力负责人卡蒂离职','10月15日','https://www.ithome.com/1/013/158.htm','10-15','曾主导星际之门')]),
dict(key='lobsters',name='Lobsters',tag='程序员圈',color='#ac130d',url='https://lobste.rs/',short='Lobsters',items=[
 it('Anthropic 的 Scion 深受《幽灵公主》启发','Anthropic\'s Scion is heavily inspired by Mononoke','36 分','https://lobste.rs/s/plcgps/anthropic_s_scion_is_heavily_inspired_by','10-15','Scion 设计解读'),
 it('Firefox 推出企业版','Introducing Firefox Enterprise','101 分','https://lobste.rs/s/7xg9rm/introducing_firefox_enterprise','10-14','前日已报'),
 it('KDE Plasma 6.8 发布（KDE 30 岁）','Plasma 6.8 released','57 分','https://lobste.rs/s/d1c8zn/plasma_6_8_released_kde_s_30th_birthday','10-14','桌面'),
 it('花式 curl 网站合集','Fancy Curl Sites','48 分','https://lobste.rs/s/zitobg/fancy_curl_sites','10-14','工具'),
 it('GitLab 警告正则引擎最高危远程执行漏洞','GitLab warns of max severity code execution vulnerability','19 分','https://lobste.rs/s/tehays/gitlab_warns_max_severity_code_execution','10-14','需尽快升级')]),
]
C=[
dict(title='8 州起诉 OpenAI',url='https://www.theverge.com/ai-artificial-intelligence/1011500/openai-state-lawsuits-chatgpt-safety',why='Verge、IT之家（转路透）双源，8 州分别起诉，有配图',pick=True,status='已核（Verge 摘要+IT之家全文）'),
dict(title='黄仁勋：不安全 AI 可断供，但拒绝放缓',url='https://www.ithome.com/1/013/164.htm',why='与 8 州诉讼构成同一天的“刹车”对照；原文无配图',pick=True,status='已核（IT之家全文，二手转述彭博）'),
dict(title='YouTube Music 给 AI 歌曲贴标签',url='https://techcrunch.com/2026/10/14/youtube-music-launches-new-labels-as-ai-generated-music-floods-streaming-platforms/',why='平台自律路径，TC 与 Verge 同报，有配图',pick=True,status='已核'),
dict(title='CSO：实验室漏了安全基础',url='https://www.csoonline.com/article/4234854/ai-agents-arent-going-rogue-frontier-labs-are-skipping-security-basics.html',why='HN 814 分，观点分析稿，配图为图库照片',pick=False,status='已核'),
dict(title='银行转手 AI 数据中心债务',url='https://startupfortune.com/banks-are-now-trying-to-offload-the-ai-data-center-debt-they-just-underwrote/',why='稿件发于 10-11，且转述 FT/彭博，未见一手',pick=False,status='待核'),
dict(title='X 订阅 / Grok Voice 3.0',url='https://www.ithome.com/1/013/159.htm',why='厂商自述，无独立验证',pick=False,status='待核'),
]
json.dump(dict(sections=S,candidates=C),open(f'work/{D}/radar.json','w'),ensure_ascii=False,indent=1)
print([len(s['items']) for s in S])
