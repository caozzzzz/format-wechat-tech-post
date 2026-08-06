---
name: format-wechat-tech-post
description: 将用户直接粘贴的无序技术原文智能整理为结构完整的微信公众号文章，自动拟定或优化标题、识别导语与背景、划分章节、提取并排序操作步骤、合并重复内容、整理提示与风险，然后生成可直接复制的内联样式 HTML 和 Markdown。用于技术经验、教程、故障复盘、工具推荐，以及纯文字或附截图文章；强调简洁、清晰、移动端可读和公众号粘贴兼容。
---

# 微信公众号技术贴排版

接收用户直接粘贴的原始文字，即使内容无序、没有标题、步骤混杂或口语化，也要先完成编辑整理，再同时交付 `文章名.md` 与 `文章名-wechat.html`。HTML 必须能在浏览器中全选复制后粘贴到公众号编辑器，并尽可能保留样式。

## 选择版式

- 没有图片，或图片只作补充：使用“纯文字版”。
- 用户提供截图、图片路径或明确要求图文教程：使用“附截图版”。
- 信息不足时继续完成可确定部分，用醒目的占位标记保留缺图位置，不虚构截图。

使用具体版式前读取对应参考：

- 原稿无序、口语化、没有标题或步骤混杂：先读取 [references/smart-structuring.md](references/smart-structuring.md)。
- 所有文章都先读取 [references/editorial-rules.md](references/editorial-rules.md)，执行通用编辑与版式检查。
- 纯文字版：读取 [references/text-only.md](references/text-only.md)。
- 附截图版：读取 [references/with-screenshots.md](references/with-screenshots.md)。
- 修改样式或手写 HTML：读取 [references/wechat-compatibility.md](references/wechat-compatibility.md)。
- 用户要求选择、对比或调整颜色：读取 [references/palettes.md](references/palettes.md)，从 7 套内置方案中选择。
- 用户要求选择、对比或调整整体版式：读取 [references/templates.md](references/templates.md)，从 5 套内置模板中选择。

## 工作流

1. 将用户粘贴的内容视为原始素材，而不是已经定稿的文章。先识别主题、读者目标、前置条件、动作顺序、结果、异常处理和风险。
2. 对原稿进行智能重组：拟定或精简标题，补充必要的小标题，将连续动作转换为有序步骤，将并列信息转换为列表，合并重复表达，把排查与恢复方法移到对应章节。
3. 保留技术事实、命令、路径、版本号和警告，不擅自改变结论。缺少链接、截图、版本或关键参数时使用明确的“待补充”标记，不猜测。
4. 整理为：标题、导语、适用场景/问题、准备工作、操作步骤、验证结果、常见问题/恢复方法、风险提醒或总结。只保留原稿真正需要的章节。
   标题、首屏密度、章节数量、步骤粒度和风险表达必须符合通用编辑规则；这些要求适用于所有文章，而非某个示例。
5. 先生成语义清楚的 Markdown。代码围栏注明语言；截图使用描述性替代文字。
6. 运行 `scripts/render_wechat.py` 从 Markdown 生成内联样式 HTML：

   `python scripts/render_wechat.py input.md --output output-wechat.html --mode text --template clean-guide --palette github-blue`

   图文版使用 `--mode screenshots`。
7. 运行严格校验：

   `python scripts/render_wechat.py input.md --output output-wechat.html --mode screenshots --validate`

   校验必须覆盖：公众号禁用样式、标签闭合、唯一主标题、标题层级、图片替代文字、代码围栏闭合，以及正文/辅助文字/强调色的最低 4.5:1 对比度。

8. 用浏览器打开 HTML，检查手机宽度下的换行、截图尺寸、代码横向滚动和层级。修正后重新校验。
9. 若用户要求代贴且已有可控制、已登录的公众号编辑器，先打开生成的 HTML 并复制正文，再粘贴到目标编辑器；不要发布，不要覆盖已有草稿，除非用户明确授权。无法控制登录态时，交付 HTML 并说明“浏览器打开后 Ctrl+A、Ctrl+C，再粘贴”。

## 默认行为

- 用户只粘贴文章、没有额外说明时，直接执行完整流程，不要求用户先整理 Markdown。
- 自动判断纯文字版或附截图版；没有真实图片时使用纯文字版。
- 自动选择最匹配文章气质的内置配色；用户指定配色时服从用户选择。
- 自动根据内容类型选择模板：操作密集型优先步骤聚焦/技术手册，叙述型优先编辑刊物，短内容优先知识笔记，无法判断时使用极简指南。
- 同时生成 Markdown 和公众号 HTML，不只在对话中返回排版建议。
- 不把原文中的换行机械地当成章节；按语义关系重新分组。

## 硬性约束

- 正文中的每个 `section`、`p`、`span` 都必须有非空 `style` 属性。
- 不使用 `class`、`<style>`、外链 CSS、脚本、表单、SVG、`position:absolute`、flex/grid 或 CSS 渐变。
- 卡片使用纯色背景、边框、圆角；横向结构使用 `table`。
- 步骤序号使用内联 `span`：`display:inline-block`、固定宽高、`border-radius:50%`、相同 `line-height`。
- 代码块使用 `pre`/`code`、等宽字体、自动换行或横向滚动；不得把命令智能引号化。
- 图片使用绝对或可访问 URL；设置 `max-width:100%;height:auto;display:block`，并紧跟简短图注。
- 不声称已同步、已粘贴或已发布，除非实际操作成功。

## 交付

至少返回 Markdown 和 HTML 的绝对路径，并简述所用版式、校验结果与复制方法。若含图片，再列出缺失、不可访问或仍为本地路径的图片。
