import json
D='2026-10-15'
sec=json.load(open(f'work/{D}/radar.json'))['sections']
secs=[dict(key=s['key'],name=s['name'],tag=s['tag'],color=s['color'],url=s['url'],short=s['short'],
  items=[dict(title=i['title'],en=i['en'],metric=i['metric'],url=i['url']) for i in s['items']]) for s in sec]
V='https://www.theverge.com/'
d=dict(date=D,weekday='周四',issue=4,title='刹车没人踩，只好别人来装',
subtitle='8 州起诉 OpenAI、黄仁勋拒绝放缓、YouTube 给 AI 歌曲贴标签',
lead='美国 8 个州同一天起诉 OpenAI，黄仁勋在伦敦说不安全的客户可以断供、但行业不该放缓，YouTube Music 则开始给 AI 歌曲贴标签。实验室自己不愿踩刹车，律师、供应商和平台正在各装一道。',
headlines=[
 dict(title='8 州分别起诉 OpenAI，称 ChatGPT 对儿童不安全',
  body='艾奥瓦、堪萨斯、内布拉斯加、西弗吉尼亚、阿肯色、亚利桑那、爱达荷、蒙大拿 8 州，14 日分别起诉 OpenAI，称其为利润牺牲安全、违反消费者保护法。据 IT之家转述路透社，这是各州对 AI 公司迄今最大规模的协调诉讼。',
  why='过去是一个个家庭告，现在是州政府成批告。诉求包括让法院责令改变 ChatGPT 的运行方式，比罚款更伤。',
  source='The Verge',url='https://www.theverge.com/ai-artificial-intelligence/1011500/openai-state-lawsuits-chatgpt-safety'),
 dict(title='黄仁勋：不安全的客户可断供，但行业不该放缓',
  body='黄仁勋在伦敦接受彭博社采访时说，若客户被认定开发不安全的 AI，英伟达会停止供货，但这目前只是“假设性问题”，会先沟通。他拒绝 Anthropic 等高管提出的全行业放缓，并称五年内向英国 AI 安全研究提供 2.5 亿美元算力。',
  why='同一天，一边是州政府要求刹车，一边是卖铲子的人说只管加速、用 AI 监控 AI。这笔算力捐赠，也是他对“放缓”的回答。',
  source='IT之家（转述彭博社）',url='https://www.ithome.com/1/013/164.htm',image_skip='IT之家原文只有占位图，没有与事件相关的配图'),
 dict(title='YouTube Music 给 AI 参与的歌曲加标签',
  body='YouTube Music 周三起推出标签，AI 参与作曲或人声的歌曲会在播放页标注，点开可看 AI 的具体角色。合作方可申报“完全 AI、部分 AI、无 AI”三档，Auto-Tune 修音算无 AI。YouTube 只做披露，不因此取消变现资格。',
  why='Deezer 做的是降权和过滤，YouTube 选的是只披露。同一个问题，平台各有各的答案。听歌的人从此多一个能看的信号。',
  source='TechCrunch',url='https://techcrunch.com/2026/10/14/youtube-music-launches-new-labels-as-ai-generated-music-floods-streaming-platforms/'),
],
sections=secs,
topics=[
 dict(name='谁该为失控的 AI 负责',kicker='LIABILITY',items=[
  dict(title='CSO：智能体没“造反”，是实验室漏了安全基础',note='多位专家称隔离与监控缺位；OpenAI、Anthropic 未回应。',src='CSO Online',metric='HN 814 分',url='https://www.csoonline.com/article/4234854/ai-agents-arent-going-rogue-frontier-labs-are-skipping-security-basics.html'),
  dict(title='40 位州检察长盯上 Character.AI 的破产出售',note='要求出售时保护用户数据，纽约州检察长牵头披露调查。',src='The Verge',metric='10月14日',url='https://www.theverge.com/policy/1011417/new-york-ag-characterai-bankruptcy'),
  dict(title='OpenAI 称前员工带着 100 多份文件见苹果高层',note='OpenAI 一方指控，苹果案仍在审理。',src='The Verge',metric='10月14日',url='https://www.theverge.com/ai-artificial-intelligence/1011276/openai-employee-unreleased-product-plans'),
  dict(title='赛力斯起诉男子 AI 造谣，索赔百万',note='仅见 IT早报标题，案情细节待核。',src='IT之家',metric='10月15日',url='https://www.ithome.com/1/013/163.htm')]),
 dict(name='平台先给 AI 内容贴标签',kicker='LABEL',items=[
  dict(title='Deezer 将让用户过滤掉纯 AI 音乐',note='7 月称每天收到近 9 万首完全 AI 曲目。',src='TechCrunch',metric='10月14日',url='https://techcrunch.com/2026/10/14/deezer-will-soon-let-you-filter-out-ai-generated-music/'),
  dict(title='安卓用 Gemini 在短信里识别慢热型诈骗',note='“增强保护”未来几周推出，走云端分析。',src='The Verge',metric='10月14日',url='https://www.theverge.com/tech/1010928/android-scam-protection-enhanced-protection-google-messages'),
  dict(title='Apate 派 AI 智能体假扮受害者，诱骗骗子',note='用来收集诈骗情报，思路是以骗治骗。',src='TechCrunch',metric='10月14日',url='https://techcrunch.com/2026/10/14/apate-sends-ai-agents-undercover-to-get-scammed-so-they-can-gather-fraud-intelligence/'),
  dict(title='Flock 称麦克风只识别枪声，官网说法不同',note='监控公司的隐私争议还在发酵。',src='TechCrunch',metric='10月14日',url='https://techcrunch.com/2026/10/14/flock-ceo-says-its-microphones-detect-just-gunshots-its-website-says-different/')]),
 dict(name='钱与岗位的另一面',kicker='MONEY',items=[
  dict(title='银行急着转手 AI 数据中心债务',note='据 FT、彭博转述，380 亿美元债卖了半年；稿件 10 月 11 日发。',src='Startup Fortune',metric='HN 248 分',url='https://startupfortune.com/banks-are-now-trying-to-offload-the-ai-data-center-debt-they-just-underwrote/'),
  dict(title='苹果收盘市值首超 5 万亿美元',note='IT早报条目，同期苹果在与 OpenAI 打官司。',src='IT之家',metric='10月15日',url='https://www.ithome.com/1/013/163.htm'),
  dict(title='OpenAI 基础设施负责人卡蒂离职',note='入职约一年，曾主导“星际之门”。',src='IT之家',metric='10月15日',url='https://www.ithome.com/1/013/158.htm'),
  dict(title='麦肯锡面试：先和 AI 客户对谈 10 分钟',note='AI 不打分，由真人评估；仅部分办公室试点。',src='The Verge',metric='10月14日',url='https://www.theverge.com/news/1011654/mckinsey-ai-client-interview')]),
],
comments=[
 '8 州诉讼最该看的不是罚款，而是要求法院改 ChatGPT 的运行方式。',
 '黄仁勋说“假设性问题”，等于没承诺。真正的约束仍在法院和平台手里。',
 'YouTube 只披露、Deezer 过滤降权。要不要听 AI 歌，现在多了个依据。'],
xhs=dict(title='没人踩刹车，别人来装了',cover='刹车没人踩\n别人来装',deck='8 州诉讼与平台标签',
 intro='美国 8 个州同一天起诉 OpenAI；黄仁勋说客户不安全可以断供，但行业不该放缓；YouTube Music 开始给 AI 歌曲贴标签。',
 oneliner='实验室不愿自己踩刹车，法院、供应商和平台各装了一道。',
 closing='如果歌单里的 AI 歌能一键过滤，你会打开吗？',
 tags=['AI','人工智能','科技新闻','AI日报','OpenAI','ChatGPT','英伟达','黄仁勋','YouTube','AI安全']))
json.dump(d,open(f'data/{D}.json','w'),ensure_ascii=False,indent=1)
for h in d['headlines']:print(len(h['body']),h['title'])
for t in d['topics']:
  for i in t['items']:print(len(i['title']),len(i['note']))
print([len(c) for c in d['comments']],[len(x) for x in d['xhs']['cover'].split('\n')],len(d['xhs']['deck']),len(d['xhs']['title']))
