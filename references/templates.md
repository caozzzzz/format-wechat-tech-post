# 内置排版模板

配色与排版相互独立。使用 `--template <名称>` 选择版式，再用 `--palette <名称>` 选择颜色。

| 名称 | 中文名 | 适合文章 | 主要特征 |
|---|---|---|---|
| `clean-guide` | 极简指南 | 通用技术教程 | 轻分割线、完整浅色步骤卡、干扰最少 |
| `tech-manual` | 技术手册 | 配置、运维、开发文档 | 方形章节标识、完整说明卡片、结构强 |
| `editorial-journal` | 编辑刊物 | 深度经验、复盘、观点长文 | 居中标题、短分隔线、杂志式留白 |
| `step-focus` | 步骤聚焦 | 多步骤安装与操作教程 | 章节侧边条、大号序号、整步内容成组、操作感强 |
| `quiet-notes` | 知识笔记 | 短技巧、清单、学习笔记 | 左线主标题、下划线章节、轻量步骤 |

列出模板：

`python scripts/render_wechat.py input.md -o output.html --list-templates`

组合示例：

`python scripts/render_wechat.py input.md -o output.html --template step-focus --palette nord-arctic --validate`

选择原则：步骤占正文一半以上时优先 `step-focus` 或 `tech-manual`；叙述和观点为主时优先 `editorial-journal`；内容较短时优先 `quiet-notes`；无法判断时使用 `clean-guide`。
