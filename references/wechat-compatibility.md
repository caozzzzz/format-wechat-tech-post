# 微信公众号兼容规则

## 允许的稳定布局

- 单列正文，建议最大视觉宽度 677px。
- `display:block` 和 `display:inline-block`。
- 简单 `table` 用于并排图标、标签或两列信息。
- 纯色 `background-color`、单色边框、适度圆角。
- 元素级内联 `style`。
- 地址、域名和代码块使用浅灰背景、深色文字与细边框，避免大面积纯黑色块。

## 禁用或避免

- `<style>`、`class`、`id` 选择器和外链样式表。
- `display:flex`、`display:grid`、绝对或固定定位。
- `linear-gradient`、复杂阴影、伪元素、动画和 JavaScript。
- 依赖 hover 才能看到的信息。

## 推荐视觉参数

- 正文：16px，行高 1.8，颜色 `#2f3337`。
- 一级小标题：20px，二级小标题：18px。
- 辅助文字：13–14px，颜色 `#7a7f87`。
- 强调色：`#2563eb`；警告色：`#b45309`；危险色：`#b42318`。
- 卡片背景：`#f7f8fa` 或 `#f9f9fb`。
- 正文段间距：12–16px；章节间距：28–36px。

## 粘贴校验

在最终 HTML 搜索并确保不存在：`class=`、`<style`、`display:flex`、`display: flex`、`display:grid`、`position:absolute`、`linear-gradient`。确认每个 section、p、span 均有非空 style。
