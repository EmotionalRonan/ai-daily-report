import json
D='2026-10-16'
sec=json.load(open(f'work/{D}/radar.json'))['sections']
secs=[dict(key=s['key'],name=s['name'],tag=s['tag'],color=s['color'],url=s['url'],short=s['short'],
  items=[dict(title=i['title'],en=i['en'],metric=i['metric'],url=i['url']) for i in s['items']]) for s in sec]
TC='https://techcrunch.com/2026/10/15/'
d=dict(date=D,weekday='周五',issue=5,title='模型交到你手上，审计员请进屋里',
subtitle='Meta 开放 Muse Spark Open、Anthropic 引入 METR、谷歌购物车上线',
lead='Meta 放出 8160 亿参数的开放权重模型，称两台 Mac Studio 就能在桌面跑；Anthropic 让 METR 研究员带着员工权限入驻；谷歌的 Universal Cart 在美国上线。能力在往外放，监督在往里走。',
headlines=[
 dict(title='Meta 开放 Muse Spark Open，称两台 Mac Studio 可本地运行',
  body='Meta 15 日放出 Muse Spark Open 权重：816B 总参数、42B 激活、1M 上下文，面向编程与智能体任务。官方称它是目前最强的美国开放权重模型，可用两台 M5 Ultra Mac Studio 在桌面运行，采用有限商用条款的 Muse 许可证。',
  why='“最强”是 Meta 自己的说法，完整评测报告还没放出。能不能在家里跑，才是它和前几代开放模型真正拉开的地方。',
  source='Meta AI Research',url='https://research.meta.ai/blog/muse-spark-open'),
 dict(title='Anthropic 让 METR 研究员以员工权限入驻，放弃否决发布权',
  body='Anthropic 向非营利评测机构 METR 的 6 名研究员开放员工级权限：公司笔记本、办公室和接近内部风险团队的工具。METR 将自行发布对其风险与事故的评估，Anthropic 不能否决，只能要求涂黑客户数据等几类信息。',
  why='这兑现了 Dario Amodei 9 月提出的“让外部评估者进实验室”。比银行驻场检查员更进一步的是，涂黑本身也可以被公开评论。',
  source='TechCrunch',url=TC+'anthropic-is-letting-metr-researchers-look-under-the-hood-with-employee-level-access/',image_skip='原文页只有 Anthropic 标志的通用图库照片，与事件无关'),
 dict(title='谷歌 Universal Cart 在美国上线，智能体可直接结账',
  body='Universal Cart 15 日在美国上线，覆盖谷歌搜索和 Gemini 应用。它能跨商家收集商品，降价或补货时提醒，还会结合信用卡权益推荐付款方式、找优惠码。结账走谷歌今年推出的开放标准 UCP，让智能体与零售商对接。',
  why='谷歌 5 月在 I/O 上预告过这个功能。购物车是入口，真正的争夺点是 UCP：谁的协议成为智能体下单的默认路径。',
  source='TechCrunch',url=TC+'googles-universal-cart-shopping-tool-launches-in-the-us/'),
],
sections=secs,
topics=[
 dict(name='能力往外放',kicker='OPEN',items=[
  dict(title='Meta 与苹果合作，优化 Muse 模型在 Mac 上运行',note='与 Meta 官方页同日，MLX 是关键。',src='The Verge',metric='10月16日',url='https://www.theverge.com/news/1012293/meta-apple-muse-spark-open-ai-model-mlx'),
  dict(title='Opus 5.5 把 SNES 老游戏移植到桌面',note='发帖人自承“反编译”说法不准。',src='Reddit',metric='656 赞',url='https://www.reddit.com/r/ClaudeAI/comments/1x3nkty/opus_55_is_insane_at_decompilation_ports/'),
  dict(title='VoiceStudio：完全本地运行的开源语音工作室',note='今日涨星第二，本地化是卖点。',src='GitHub',metric='+3,024 星',url='https://github.com/debpalash/VoiceStudio'),
  dict(title='APUS 开源 Reflex Agent，称更快',note='厂商自述，暂无第三方测试。',src='量子位',metric='10月14日',url='https://www.qbitai.com/2026/10/503165.html')]),
 dict(name='监督往里走',kicker='OVERSIGHT',items=[
  dict(title='CLASHarness：测量电脑操作中的多智能体冲突',note='今日 HF 论文榜首，基准可验证。',src='Hugging Face',metric='25 赞',url='https://huggingface.co/papers/2610.19128'),
  dict(title='APEX-Harm：共享职场空间里的智能体安全评测',note='把风险放进真实办公场景。',src='Hugging Face',metric='12 赞',url='https://huggingface.co/papers/2610.13623'),
  dict(title='Citizen Lab：定向广告成了零点击间谍软件通道',note='调查报告，HN 讨论 531 条。',src='Hacker News',metric='364 分',url='https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/'),
  dict(title='ChatGPT 现在能看你的 Chrome 标签页',note='仅见标题，权限细节待核。',src='The Verge',metric='10月16日',url='https://www.theverge.com/ai-artificial-intelligence/1012510/openai-chatgpt-google-chrome-tabs')]),
 dict(name='智能体进入日常',kicker='DAILY',items=[
  dict(title='亚马逊 Bee 推出两款 AI 录音设备，74.99 美元起',note='Pro 订阅 11.99 美元/月。',src='TechCrunch',metric='10月15日',url=TC+'amazons-bee-launches-two-new-personal-ai-devices-starting-at-75/'),
  dict(title='阶跃发布首款 Agent 手机 STEPX Neo',note='大模型原生智能体手机，细节待核。',src='量子位',metric='10月14日',url='https://www.qbitai.com/2026/10/503244.html'),
  dict(title='Bluesky 的 AI 工具 Attie 可做游戏和应用',note='生成后直接在社交上分享。',src='The Verge',metric='10月16日',url='https://www.theverge.com/tech/1012374/bluesky-ai-attie-small-social-games-apps'),
  dict(title='Rivian 车里要来 AI 智能体',note='仅见 TC 标题，细节待核。',src='TechCrunch',metric='10月15日',url=TC+'ai-agents-are-coming-to-rivians-cars/')]),
],
comments=[
 '“最强开放模型”是 Meta 的自评，完整评测报告要等后续放出。',
 'METR 能公开评论涂黑是否合理，这比“允许独立评估”更有约束力。',
 '购物车只是入口，UCP 才是谷歌想让智能体默认走的路。'],
xhs=dict(title='模型进桌面，审计员进屋',cover='模型进桌面\n审计员进屋',deck='Meta、Anthropic、谷歌',
 intro='Meta 开放 8160 亿参数模型权重，称两台 Mac Studio 就能本地跑；Anthropic 让 METR 研究员以员工权限入驻；谷歌 Universal Cart 在美国上线。',
 oneliner='能力在往外放，监督在往里走。',
 closing='如果模型能在家里跑，你会想自己试试吗？',
 tags=['AI','人工智能','科技新闻','AI日报','Meta','Anthropic','谷歌','开源模型','AI安全','智能体']))
json.dump(d,open(f'data/{D}.json','w'),ensure_ascii=False,indent=1)
for h in d['headlines']:print(len(h['body']),h['title'])
for t in d['topics']:
  for i in t['items']:
    if len(i['title'])>32 or len(i['note'])>40:print('LONG',len(i['title']),len(i['note']),i['title'])
print([len(c) for c in d['comments']],[len(x) for x in d['xhs']['cover'].split('\n')],len(d['xhs']['deck']),len(d['xhs']['title']))
