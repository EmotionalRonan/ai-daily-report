# 2026-10-16 文字编辑审稿

## 第 1 轮
### 可以过
- 头条 1 Meta Muse Spark Open：816B/42B 激活、1M 上下文、两台 M5 Ultra Mac Studio、Muse 许可证有限商用，均与 Meta 官方页一致；“最强”已在 why 里标明为 Meta 自评。
- 头条 2 Anthropic × METR：6 名研究员、员工级权限、不可否决但可要求涂黑、Amodei 9 月文章，均与 TechCrunch 原文一致。
- 头条 3 Universal Cart：5 月 I/O 预告、美国上线、降价/补货提醒、信用卡权益、UCP，均与 TechCrunch 原文一致。
- 专题抽查 9 条（Bee 价格 74.99/99.99/11.99 美元核对 TC 全文；Verge Meta×Apple、Bluesky、Chrome 标签页、Rivian 核对标题与来源；HF 论文赞数核对 API；Citizen Lab 链接来自 HN）。
- 禁用词扫描无命中；长度：body 113–134，comment ≤33，cover 每行 5 字，topic title/note 均在限内。
### 需要看
- 头条 2 配图是 Getty 通用图（手机屏幕上的 Anthropic 标志），与 METR 入驻无关；候选里没有更合适的图。建议写 image_skip。 https://techcrunch.com/2026/10/15/anthropic-is-letting-metr-researchers-look-under-the-hood-with-employee-level-access/
### 配图
- h1：Meta 官方社交图，标题字清晰，与新闻直接相关，通过。
- h2：通用图库，退回。
- h3：Google 官方 Universal Cart 示意图，含降价通知、优惠提示、结账页，与新闻直接相关，通过。
VERDICT: REVISE

## 主笔回复
- 头条 2 已加 image_skip（“原文页只有 Anthropic 标志的通用图库照片，与事件无关”），其余不改。

## 第 2 轮复核
- data/2026-10-16.json 头条 2 带 image_skip；fetch_images.py 重跑后只保留 h1、h3 的图；其余未变。
- 配图：h1、h3 通过；h2 已按说明跳过。
VERDICT: PASS
