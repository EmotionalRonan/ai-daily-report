# 编辑复核 2026-10-18

## 可以过
- 头条1 OpenCode：已打开官方 X 帖（两版）与 Startup Fortune/TSN 等转述；1.4%、邮件通知、与 Anthropic/OpenAI/Google 协同处理均与原帖一致；“密钥可能外泄”“账单已涨”写成“据报道”，正文已标明入口与损失待官方复盘。https://x.com/opencode/status/2111519637049319818
- 头条2 DeepSeek：已打开 HF 模型卡；Terminal-Bench 4.0 31.2→42.3、DeepSWE 74.2→77.0、MIT、1M 上下文均与卡一致；已注明“官方自报”。https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017
- 头条3 Anthropic：已打开研究页，21%→14%、27%→9%、管理 Claude 的表述一致；会议时间 +20% 来自 TechCrunch 对同一报告的转述。https://www.anthropic.com/research/employment-at-anthropic
- 抽查专题/热榜 8 条（Verge 三条、TC、量子位两条、GitHub 星数、HN 分数）与抓取结果一致；Reddit 一栏已标“缓存”。
- 禁用词 grep 无命中；body 80–150 字、topic title ≤32、note ≤40、comment ≤70、cover 每行 ≤8、deck ≤16 均已检查。

## 需要看
- 无阻塞项。提示：Reddit 本期抓到的是缓存页，发帖日约 10 月 11–12 日，已在热度栏标注。

## 配图
- 头条1：跳过。原文是 X 帖，只有账号头像，主笔写了 image_skip。结论：合理。
- 头条2：跳过。read_file 看过 HF 候选图，是渐变底+模型名的标题卡，不说明事件。结论：合理。
- 头条3：read_file 看过。og 图只是 Anthropic 字标，已退回主笔换成研究页 Figure 1（初级技术招聘占比折线图，14%/9% 与正文一致）。结论：通过。

VERDICT: PASS
