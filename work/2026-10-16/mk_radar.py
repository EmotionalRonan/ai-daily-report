import json
D='2026-10-16'
def it(t,en,m,u,tm,w): return dict(title=t,en=en,metric=m,url=u,time=tm,what=w)
hn=lambda i:f'https://news.ycombinator.com/item?id={i}'
gh=lambda r:f'https://github.com/{r}'
rd='https://www.reddit.com'
S=[
dict(key='hn',name='Hacker News',tag='开发者风向',color='#ff6600',url='https://news.ycombinator.com/',short='HN',items=[
 it('Meta 发布 Muse Spark Open','Muse Spark Open','576 分 · 326 评论',hn(50107379),'10-15','Meta 开放 8160 亿参数模型权重，官方称可在两台 Mac Studio 上本地运行'),
 it('神经网络其实很“干净”','Neural networks are clean','466 分 · 178 评论',hn(50105647),'10-15','Goodfire 的可解释性长文'),
 it('定向广告成了零点击间谍软件的通道','AdFection: Targeted ads turned into a pipeline for zero-click mercenary spyware','364 分 · 531 评论',hn(50101813),'10-15','Citizen Lab 调查报告'),
 it('想下载个 ISO，结果写出了内核提权漏洞','Wanted to download an ISO, ended up writing a kernel exploit','344 分 · 169 评论',hn(50070625),'10-15','路由器固件安全分析，非 AI'),
 it('Steam 客户端已比 Epic 新的“vibe coded”启动器快','Steam Client is now faster than Epic\'s new vibe coded launcher','269 分 · 270 评论',hn(50105635),'10-15','AI 写代码的另一面，来源待核')]),
dict(key='reddit',name='Reddit',tag='AI 社区热帖',color='#ff4500',url='https://www.reddit.com/r/singularity/',short='Reddit',items=[
 it('Opus 5.5 把 SNES 老游戏移植到桌面','r/ClaudeAI','656 赞 · 232 评论',rd+'/r/ClaudeAI/comments/1x3nkty/opus_55_is_insane_at_decompilation_ports/','10-15','发帖人事后承认“反编译”说法不准，更像模拟器加静态重编译'),
 it('Karpathy：LLM 能力差距在拉大','r/singularity','790 赞 · 200 评论',rd+'/r/singularity/comments/1x3gsc4/andrej_karpathy_breaks_down_the_capability_gap/','10-15','转发 X 长帖截图，此前已上榜'),
 it('GTA 5、使命召唤等游戏被 AI 逆向后移植到浏览器','r/singularity','820 赞 · 126 评论',rd+'/r/singularity/comments/1x38qz0/gta_5_modern_warfare_2_halo_and_many_other_games/','10-14','Destructoid 报道'),
 it('免费 Adobe 克隆作者开源 Office 复刻','r/singularity','1481 赞 · 332 评论',rd+'/r/singularity/comments/1x3daf9/shock_and_awe_creator_of_free_adobe_clones/','10-14','Tom\'s Hardware 报道，已多日在榜'),
 it('Claude 项目改版，Max 用户要求可选','r/ClaudeAI','358 赞 · 143 评论',rd+'/r/ClaudeAI/comments/1x33na4/new_projects_rolling_out_for_chat_and_cowork_oh/','10-14','社区反馈帖')]),
dict(key='x',name='X / Twitter',tag='科技圈刷屏',color='#111111',url='https://agentflare.org/social/tech/index.html',short='X',items=[
 it('马斯克：Grok Bot 像雇了个聪明员工','@elonmusk','7.7K 赞 · 340 万浏览','https://x.com/elonmusk/status/2109955246923641259','10-13','原帖一句话'),
 it('马斯克：Grok Bot 代买乐高，到货后自动停止查物流','@elonmusk','9.9K 赞 · 190 万浏览','https://x.com/elonmusk/status/2110138164811833534','10-13','原帖，自述'),
 it('Matthew Berman：“任何东西都能逆向，软件完了”','@MatthewBerman','3.87 万赞 · 370 万浏览','https://x.com/MatthewBerman/status/2108245653843509415','10-08','观点帖'),
 it('Grok Voice 3.0 称“全球领先对话语音模型”','@elonmusk','5.0K 赞 · 78.7 万浏览','https://x.com/elonmusk/status/2110483960312799675','10-14','厂商自评，未经第三方核实'),
 it('Polymarket：贝佐斯称 AI 可让美国人每周只工作 3 天','@Polymarket','7.4K 赞 · 58.9 万浏览','https://x.com/Polymarket/status/2108190299830771725','10-08','转述，待核')]),
dict(key='github',name='GitHub Trending',tag='今日爆火仓库',color='#24292f',url='https://github.com/trending',short='GitHub',items=[
 it('morluto/rea','morluto/rea','今日 +32,314 星',gh('morluto/rea'),'10-16','“用智能体逆向一切”，榜首且增速异常，来源待核'),
 it('debpalash/VoiceStudio','debpalash/VoiceStudio','今日 +3,024 星',gh('debpalash/VoiceStudio'),'10-16','开源、完全本地的语音工作室'),
 it('NationalSecurityAgency/ghidra','NationalSecurityAgency/ghidra','今日 +1,369 星',gh('NationalSecurityAgency/ghidra'),'10-16','NSA 的逆向工程框架，随“逆向”热重回榜单'),
 it('K-Dense-AI/scientific-agent-skills','K-Dense-AI/scientific-agent-skills','今日 +1,091 星',gh('K-Dense-AI/scientific-agent-skills'),'10-16','给智能体装科研技能'),
 it('affaan-m/ECC','affaan-m/ECC','今日 +1,013 星',gh('affaan-m/ECC'),'10-16','智能体 harness 性能优化')]),
dict(key='hf',name='Hugging Face Papers',tag='今日热门论文',color='#ffb000',url='https://huggingface.co/papers',short='HF',items=[
 it('CLASHarness：测量电脑操作中的多智能体冲突','CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use','25 赞','https://huggingface.co/papers/2610.19128','10-15','可控、可验证的多智能体冲突基准'),
 it('APEX-Harm：共享办公空间里的智能体安全评测','APEX-Harm: Evaluating Agent Safety in Shared Professional Workspaces','12 赞','https://huggingface.co/papers/2610.13623','10-15','职场场景下的智能体安全'),
 it('线性注意力的长上下文能力','History Replays Itself: Unleashing Long-Context Capability in Linear Attention','9 赞','https://huggingface.co/papers/2610.15715','10-15','让线性注意力吃下长上下文'),
 it('PreciseCoder：超越单测奖励的调试','PreciseCoder: Faithful and Generalizable Debugging Beyond Unit-Test Rewards','4 赞','https://huggingface.co/papers/2610.18755','10-15','代码调试训练'),
 it('FreeSolo：线性时间稀疏注意力','FreeSolo: Linear-time Sparse Attention with Zero-Shot Length Extrapolation','3 赞','https://huggingface.co/papers/2610.17191','10-15','零样本长度外推')]),
dict(key='media',name='The Verge · TechCrunch',tag='海外科技媒体',color='#5200ff',url='https://www.theverge.com/',short='外媒',items=[
 it('Anthropic 让 METR 研究员以员工权限入驻','Anthropic is letting METR researchers look under the hood with employee-level access','TechCrunch','https://techcrunch.com/2026/10/15/anthropic-is-letting-metr-researchers-look-under-the-hood-with-employee-level-access/','10-15','6 名研究员，Anthropic 放弃否决发布的权利'),
 it('谷歌 Universal Cart 在美国上线','Google\'s Universal Cart shopping tool launches in the US','TechCrunch','https://techcrunch.com/2026/10/15/googles-universal-cart-shopping-tool-launches-in-the-us/','10-15','搜索和 Gemini 里的跨商家购物车'),
 it('亚马逊 Bee 推出两款 AI 录音设备，75 美元起','Amazon\'s Bee launches two new personal AI devices, starting at $75','TechCrunch','https://techcrunch.com/2026/10/15/amazons-bee-launches-two-new-personal-ai-devices-starting-at-75/','10-15','Frontier 74.99 美元、Eclipse 99.99 美元'),
 it('Meta 与苹果合作，让 Muse 模型在 Mac 上跑得更好','Meta and Apple team up to make Muse AI models run better on Macs','The Verge','https://www.theverge.com/news/1012293/meta-apple-muse-spark-open-ai-model-mlx','10-16','MLX 适配'),
 it('ChatGPT 现在能看你的 Chrome 标签页','ChatGPT can peek at your Chrome tabs now','The Verge','https://www.theverge.com/ai-artificial-intelligence/1012510/openai-chatgpt-google-chrome-tabs','10-16','仅见标题，细节待核')]),
dict(key='qbit',name='量子位',tag='国内 AI 圈',color='#2f6bff',url='https://www.qbitai.com/',short='量子位',items=[
 it('阶跃发布首款 Agent 手机 STEPX Neo','阶跃终端首款「Agent手机」STEPX Neo正式发布','量子位','https://www.qbitai.com/2026/10/503244.html','10-14','大模型原生智能体手机'),
 it('APUS 开源 Reflex Agent，称响应比 Claude Code 快 3 倍','APUS AI开源Reflex Agent','量子位','https://www.qbitai.com/2026/10/503165.html','10-14','厂商自述，未经第三方测试'),
 it('《变形计》赛博复活，LibTV 下场“造星”','LibTV','量子位','https://www.qbitai.com/2026/10/503211.html','10-14','AI 视频内容'),
 it('MemSilicon 完成 1Gb RRAM 芯片流片','MemSilicon','量子位','https://www.qbitai.com/2026/10/503198.html','10-14','称国际首款高密度大容量'),
 it('千问办公电商版：几百元开店','千问','量子位','https://www.qbitai.com/2026/10/503303.html','10-15','偏推广稿')]),
dict(key='ithome',name='IT之家',tag='国内科技数码',color='#d4222a',url='https://www.ithome.com/',short='IT之家',items=[
 it('宣称“美国最强开源 AI 模型”：Meta 发布 Muse Spark Open','Muse Spark Open','IT之家','https://www.ithome.com/1/013/706.htm','10-16','国内跟进'),
 it('亚马逊 Bee 推出 Frontier 与 Eclipse，74.99 美元起','Bee','IT之家','https://www.ithome.com/1/013/702.htm','10-16','AI 录音可穿戴'),
 it('库克称苹果智能月底在华测试','Apple Intelligence','IT早报','https://www.ithome.com/1/013/710.htm','10-16','IT早报条目，细节待核'),
 it('DeepSeek 宕机 5 小时补偿公布','DeepSeek','IT早报','https://www.ithome.com/1/013/710.htm','10-16','IT早报条目，细节待核'),
 it('谷歌安卓地震预警累计推送超 10 亿次','Android Earthquake Alerts','IT之家','https://www.ithome.com/1/013/708.htm','10-16','覆盖 200 多个国家和地区')]),
dict(key='lobsters',name='Lobsters',tag='程序员圈',color='#ac130d',url='https://lobste.rs/',short='Lobsters',items=[
 it('Anthropic 的 Scion 深受 Mononoke 启发','Anthropic\'s Scion is heavily inspired by Mononoke','138 分 · 48 评论','https://lobste.rs/s/plcgps/anthropic_s_scion_is_heavily_inspired_by','10-15','10-14 期已写过 Scion'),
 it('Mozilla 推出 Firefox Enterprise','Introducing Firefox Enterprise','128 分 · 35 评论','https://lobste.rs/s/7xg9rm/introducing_firefox_enterprise','10-15','企业版浏览器'),
 it('我自托管了什么','What I Self-Host','80 分 · 44 评论','https://lobste.rs/s/j4tlzg/what_i_self_host','10-15','个人清单'),
 it('decomp.dev 停止服务','Sunsetting decomp.dev','55 分 · 11 评论','https://lobste.rs/s/kaerns/sunsetting_decomp_dev','10-15','反编译社区站点'),
 it('JPEG XL 与 AVIF 在网页场景对比','JPEG XL vs AVIF for web use-cases','40 分 · 14 评论','https://lobste.rs/s/uejdwj/jpeg_xl_vs_avif_for_web_use_cases','10-15','图像格式评测')]),
]
C=[
 dict(title='Meta 开放 Muse Spark Open 权重',url='https://research.meta.ai/blog/muse-spark-open',why='HN 576 分，Meta 官方页、TC、Verge、IT之家同日跟进，有配图',pick=True,status='已核（Meta 官方页全文）'),
 dict(title='Anthropic 让 METR 以员工权限入驻',url=S[5]['items'][0]['url'],why='TC 全文，承接 9 月“放缓前沿”主张，与这期主线契合',pick=True,status='已核（TC 全文）'),
 dict(title='谷歌 Universal Cart 在美国上线',url=S[5]['items'][1]['url'],why='TC 全文，智能体结账走 UCP 协议',pick=True,status='已核（TC 全文）'),
 dict(title='亚马逊 Bee 两款新设备',url=S[5]['items'][2]['url'],why='TC 全文，价格与订阅明确',pick=False,status='已核（TC 全文）'),
 dict(title='Opus 5.5 移植 SNES 游戏',url=S[1]['items'][0]['url'],why='Reddit 热帖，但发帖人自承术语不准，二手来源',pick=False,status='待核'),
 dict(title='morluto/rea 登顶 GitHub Trending',url=gh('morluto/rea'),why='今日 +32,314 星，增速异常，缺一手解释',pick=False,status='待核'),
 dict(title='Steam 比 Epic 的 vibe coded 启动器快',url=S[0]['items'][4]['url'],why='HN 269 分，单一来源',pick=False,status='待核'),
]
json.dump(dict(sections=S,candidates=C),open(f'work/{D}/radar.json','w'),ensure_ascii=False,indent=1)
print([len(s['items']) for s in S])
