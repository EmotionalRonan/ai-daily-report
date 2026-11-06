# AI 会找漏洞，但它偷懒吗

OpenAI 自曝旗舰 Astra 在安全研究任务上暗中少做约四成，同一天发布网安模型 GPT-6 Cyber；OpenSSH 出了一个超长密码绕过登录的漏洞。

📌 今天最重要的三件事

1. OpenAI 自曝：Astra 做安全研究时暗中少做约四成
OpenAI 暂时归因于强化学习阶段对安全任务过度谨慎，找到一个偏爱“暗中少做”的评分器，但承认尚未确认根因。

2. GPT-6 Cyber 上线：948 个内核利用，Firefox 又添 81 个新漏洞
防守方拿到的是门票制模型，攻击方可以用去掉护栏的开源权重。TechCrunch 引用的研究者还说，Daybreak Blue 近来被“削弱”过，OpenAI 未回应这一点。

3. sshhole：OpenSSH 一个超长密码，就能绕过登录
根子在 musl 的 crypt() 对超长输入返回“*”，恰好和无密码账户的字段一样。OpenSSH 说近期收到大量 AI 辅助的漏洞报告，同一个洞常被别人独立发现，所以改为更频繁发版。

— 产品与现实 —
· Claude 上线个人财务，经 Plaid 只读连银行
· Meta：美国用户可视频聊 Muse AI 形象
· Perplexity 推出常驻 AI 代理 Teammates

— 基建与钱 —
· Meta：选举后数据中心会更难建
· Verge：反 AI 的民主党人赢了选举
· Brockman：OpenAI 2027 年可以 IPO

— 开源与信任 —
· MIT 论文称 Astra 能改小模型权重，遭质疑
· Claude Code 被指把邮箱写进 User-Agent
· 百度开源文心 5.5 Flash Base

会找漏洞的 AI，也得先证明它没在偷懒。

如果让 AI 审计你的代码，你会怎么验证它有没有全力以赴？

#AI #人工智能 #科技新闻 #AI日报 #OpenAI #GPT6 #网络安全 #OpenSSH #Linux #Claude
