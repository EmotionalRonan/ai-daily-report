# 2026-11-19 审稿

## 可以过
- 头条 1 Gemini 4 Neon：打开谷歌原文核对——11 月 18 日发布、输入 3 美元/输出 15 美元每百万 token、100 万上下文、AA 指数 xhigh 61 分排第三、高档位每任务成本比 Carbon 低 32%，均与原文一致；跑分来源已写明为谷歌引用。
- 头条 2 Nginx：打开 Wiz 原文核对——两个 CVE 编号、CVSS 9.2、1.9.5 起、修复版 1.30.7/1.31.9、可先关 HTTP/2、Rapid7/Xint 等独立发现、Wiz 用 Atlas 工具发现，均一致。
- 头条 3 Anthropic：打开 TechCrunch 原文核对——83 美元、区间 70–78、约 1.5 万亿完全稀释估值、5 月 9650 亿、纳斯达克 ANT、周四开始交易，均一致；已标“据报道”。
- 专题抽查 8 条：Java4Shell、PyPI agent-framework（Wiz 页内摘要）、Genie 4（谷歌原文）、Gemini Tasks（谷歌博文描述）、nginx2root（Lobsters）、纳德拉（TC 标题）、OpenAI×AMD 14%（IT之家标题）、英伟达员工大会（IT之家标题）：标题与出处相符；转述类已在 note 里标注。
- 禁用词扫描无命中；长度：body 143/149/135，topic title ≤31，note ≤25，comment ≤40，cover 每行 ≤8，xhs 标题 20。

## 需要看
- 无硬伤。提示：Reddit 的 top.json 返回的是 10 月旧缓存，热榜 Reddit 一栏改用当日搜索结果，条目已标注转述；X 一栏同为转述。

## 配图
- h1：谷歌原文头图，霓虹字“Gemini 4 Neon”，清晰，和事件直接相关，通过。
- h2：Wiz 原文头图，写有 NGINX、HTTP/2 RCE 与两个 CVE 编号，清晰，通过。
- h3：原文页唯一的图是模糊的 Claude 应用图标，与定价事件关系弱，主笔已写 image_skip，不用图，通过。

VERDICT: PASS
- 回改：intro 里“由 AI 工具发现”命中禁用词，已改“借助 AI 工具”。
