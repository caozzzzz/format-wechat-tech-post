# 微信公众号技术文章排版

`format-wechat-tech-post` 是一个面向微信公众号技术内容的 Codex Skill。它可以接收未经整理的原始文章，自动识别主题、重组章节、拆分操作步骤，并同时生成 Markdown 文档和可直接复制到微信公众号编辑器的内联样式 HTML。

它不仅负责“换颜色”，还会先完成文章编辑：整理口语化和重复内容，补全必要标题，将混杂的操作过程转换为有序步骤，再根据文章类型选择合适的模板和配色。

## 适用场景

- 技术教程、软件配置、工具使用与安装指南。
- 故障排查、问题复盘、经验总结和避坑说明。
- 将聊天记录、零散笔记或无序原稿整理成公众号文章。
- 制作纯文字文章或带操作截图的图文教程。
- 生成能在微信公众号编辑器中尽量保留样式的 HTML。
- 同时保留一份便于归档和继续修改的 Markdown 原稿。

## 核心能力

- **智能整理原稿**：识别主题、导语、前置条件、操作顺序、验证结果、异常处理与风险提醒。
- **自动划分结构**：根据语义生成大标题、小标题、步骤和列表，不机械照搬原文换行。
- **步骤重排**：把连续操作整理成顺序明确、粒度一致的教程步骤。
- **双格式输出**：一次生成 `.md` 与 `-wechat.html` 两份文件。
- **纯文字与截图模式**：没有图片时生成纯文字版；提供截图时生成带图注的图文版。
- **公众号粘贴兼容**：核心排版全部使用内联 `style`，避免依赖 class、`<style>`、脚本、Flexbox 或渐变。
- **自动模板与配色**：可由技能根据文章类型选择，也可以由用户明确指定。
- **严格校验**：检查禁用样式、标题层级、标签闭合、图片替代文字和文字对比度。

## 内置模板

模板控制文章的版式结构，与配色相互独立。

| 参数 | 中文名称 | 适合内容 | 主要特点 |
| --- | --- | --- | --- |
| `clean-guide` | 极简指南 | 通用技术教程 | 留白充足、浅色步骤卡、干扰最少 |
| `tech-manual` | 技术手册 | 配置、运维、开发文档 | 结构清楚、章节标识醒目 |
| `editorial-journal` | 编辑刊物 | 深度经验、复盘、观点长文 | 杂志式留白、阅读节奏舒缓 |
| `step-focus` | 步骤聚焦 | 多步骤安装和操作教程 | 大号序号、整步成组、操作感强 |
| `quiet-notes` | 知识笔记 | 短技巧、清单、学习笔记 | 轻量简洁、信息密度适中 |

## 内置配色

| 参数 | 中文名称 | 风格与用途 |
| --- | --- | --- |
| `github-blue` | GitHub 蓝 | 清爽专业，适合通用技术教程，也是默认配色 |
| `nord-arctic` | Nord 冰川 | 冷静克制，适合工具与效率文章 |
| `solarized-paper` | Solarized 米白 | 纸张质感，适合长文和代码阅读 |
| `material-indigo` | Material 靛蓝 | 现代醒目，适合产品与移动开发 |
| `jade-editorial` | 翡翠刊物 | 温润高级，适合经验总结与知识文章 |
| `burgundy-journal` | 勃艮第刊物 | 稳重、有编辑感，适合观点和深度复盘 |
| `amber-coffee` | 咖啡琥珀 | 温暖复古，适合个人经验和故事型教程 |

5 套模板与 7 套配色可以自由组合，共可形成 35 种排版组合。

## 目录结构

```text
format-wechat-tech-post/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    editorial-rules.md
    palettes.md
    smart-structuring.md
    templates.md
    text-only.md
    wechat-compatibility.md
    with-screenshots.md
  scripts/
    render_wechat.py
```

## 安装方法

将仓库克隆或下载到 Codex 的 Skills 目录：

```powershell
git clone https://github.com/caozzzzz/format-wechat-tech-post.git "$env:USERPROFILE\.codex\skills\format-wechat-tech-post"
```

也可以下载 ZIP，解压后确保 `SKILL.md` 位于技能目录根部。安装完成后，重新打开 Codex 会话或刷新技能列表。

## 使用方法

最简单的方式是直接粘贴原始文章，例如：

```text
使用 format-wechat-tech-post 整理下面这篇文章，生成公众号 HTML 和 Markdown：

（在这里粘贴未经整理的原稿）
```

原稿可以没有标题、顺序混乱或带有口语化表达，技能会先整理内容，再完成排版。

也可以指定样式：

```text
把下面的技术教程整理成公众号文章，使用“步骤聚焦”模板和“Nord 冰川”配色，
同时生成 Markdown 和可复制到公众号编辑器的 HTML。
```

提供截图时，可以说明图片应该放在哪一步；如果截图信息不足，技能会保留明确的待补图位置，不会虚构图片。

## 命令行渲染

将整理后的 Markdown 转换为公众号 HTML：

```powershell
python scripts/render_wechat.py input.md --output output-wechat.html --mode text --template clean-guide --palette github-blue
```

生成带截图的版本：

```powershell
python scripts/render_wechat.py input.md --output output-wechat.html --mode screenshots --template step-focus --palette nord-arctic
```

生成并执行严格校验：

```powershell
python scripts/render_wechat.py input.md --output output-wechat.html --mode screenshots --template tech-manual --palette jade-editorial --validate
```

查看全部模板或配色：

```powershell
python scripts/render_wechat.py input.md --output output.html --list-templates
python scripts/render_wechat.py input.md --output output.html --list-palettes
```

## 输出文件

每次完整处理至少输出两份文件：

```text
文章名称.md
文章名称-wechat.html
```

- Markdown 用于归档、版本管理和后续修改。
- HTML 用于复制到微信公众号编辑器。

复制方法：用浏览器打开生成的 HTML，按 `Ctrl+A` 全选、`Ctrl+C` 复制，然后粘贴到微信公众号编辑器中。

## 公众号兼容原则

- 每个主要正文元素都使用非空的内联 `style` 属性。
- 不依赖 CSS class、`<style>`、外链 CSS 或 JavaScript。
- 不使用公众号中表现不稳定的绝对定位、Flexbox、Grid 和渐变背景。
- 横向结构优先使用 `table`，步骤序号使用内联圆形 `span`。
- 代码、链接、路径、提示框和截图都针对移动端阅读优化。
- 卡片采用纯色背景、边框和圆角，减少复制粘贴后的样式丢失。

## 输出原则

- 保留原稿中的技术事实、命令、路径、版本号和警告。
- 不擅自补充原文没有的结论或关键参数。
- 缺少链接、截图或配置值时使用明确的“待补充”标记。
- 只保留真正需要的章节，避免为了套模板而过度分段。
- 未实际完成粘贴或发布时，不声称已经同步到公众号。

## 推荐工作流

1. 直接粘贴原始文章，不必提前手动整理。
2. 让技能自动重组标题、章节、步骤和提示信息。
3. 选择或自动匹配模板与配色。
4. 同时生成 Markdown 和公众号 HTML。
5. 执行严格校验并在移动端宽度下预览。
6. 将 HTML 全选复制到微信公众号编辑器，最后检查图片和链接。

