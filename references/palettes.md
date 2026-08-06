# 内置配色方案

使用 `--palette <名称>` 选择主题。全部主题均为适合公众号正文的浅色方案，并保持高对比、纯色背景与内联样式。

| 名称 | 中文名 | 气质与适用场景 |
|---|---|---|
| `github-blue` | GitHub 蓝 | 清爽专业，适合通用技术教程；默认主题 |
| `nord-arctic` | Nord 冰川 | 冷静克制，适合工具与效率文章 |
| `solarized-paper` | Solarized 米白 | 纸张质感，适合长文与代码阅读 |
| `material-indigo` | Material 靛蓝 | 现代醒目，适合产品与移动开发 |
| `jade-editorial` | 翡翠刊物 | 温润高级，适合经验总结与知识类文章 |
| `burgundy-journal` | 勃艮第刊物 | 稳重编辑感，适合观点与深度复盘 |
| `amber-coffee` | 咖啡琥珀 | 温暖复古，适合个人经验和故事型教程 |

查看列表：

`python scripts/render_wechat.py input.md -o output.html --list-palettes`

生成指定主题：

`python scripts/render_wechat.py input.md -o output.html --palette nord-arctic --validate`
