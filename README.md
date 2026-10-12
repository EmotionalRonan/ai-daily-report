# AI 日报

科技 · 人工智能 · 编程，每天早上 8 点出刊。每期三条头条、三个专题，外加九个平台的热榜，一份内容三种样式：

| 样式 | 文件 | 用法 |
|---|---|---|
| 网页版 | `reports/日期/index.html` | 直接浏览 / GitHub Pages |
| 公众号版 | `reports/日期/wechat.html` + `wechat_header.png` + `wechat_thumb.png` | 电脑浏览器打开 → 全选复制 → 粘贴到公众号编辑器（样式为内联，可保留） |
| 小红书版 | `reports/日期/xiaohongshu.md` + `xhs/01~06.png` | 6 张 3:4 卡片按顺序上传，正文与话题标签直接复制 |

## 最新一期

- **2026-10-12｜给AI装上“紧急刹车”** — [网页](reports/2026-10-12/index.html) · [公众号](reports/2026-10-12/wechat.html) · [小红书](reports/2026-10-12/xiaohongshu.md)

排版规范：[`docs/layout.md`](docs/layout.md)

往期目录：[`index.html`](index.html)

## 热点源（每源 Top 5）

| 源 | 取法 |
|---|---|
| Hacker News | 首页按分数排序（hn.algolia.com API） |
| Reddit | r/singularity、r/LocalLLaMA、r/OpenAI、r/ClaudeAI、r/MachineLearning、r/artificial 当日 Top |
| X / Twitter | 当日科技热帖（按浏览/互动），经公开聚合页与报道交叉核对 |
| GitHub Trending | 当日 stars 增长 |
| Hugging Face Papers | Daily Papers 按点赞 |
| The Verge · TechCrunch | AI 频道最新 |
| 量子位 | 中文 AI 热点 |
| IT之家 | 数码与硬件 |
| Lobsters | 硬核编程讨论 |

## 结构

```
data/YYYY-MM-DD.json     每期数据：头条、专题（topics）、各平台热榜、编辑手记、小红书文案
scripts/build.py         生成网页版 / 公众号版 / 小红书文案 + 往期目录
scripts/cards.py         生成小红书卡片与公众号头图、封面（PIL + 思源宋体/黑体，报纸版式）
reports/YYYY-MM-DD/      成品
```

```bash
pip install pillow
python3 scripts/build.py data/2026-10-12.json
python3 scripts/cards.py data/2026-10-12.json
```

> 关键事实均核对过原始来源；标注“据报道”“社区声称”的内容尚未得到官方证实。

## 生产线

每期由四个角色依次完成，岗位说明在 `prompts/`：选题雷达（采集 9 源）→ 主笔（写稿并对整期负责）→ 文字编辑（只核对、不改稿，不通过就退回主笔）→ 视觉排版（按 `docs/layout.md` 出图）。中间产物在 `work/DATE/`。发布到公众号和小红书由人工完成。
