#!/usr/bin/env python3
"""Render a small, predictable Markdown subset as WeChat-safe inline HTML."""
from __future__ import annotations

import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path

P = "margin:0 0 14px;font-size:16px;line-height:1.8;color:#2f3337;letter-spacing:.02em;"
SECTION = "margin:0 auto;padding:24px 16px;background-color:#ffffff;max-width:677px;"

TEMPLATES = {
    "clean-guide": {
        "label": "极简指南", "section": SECTION,
        "wrap_step": True,
        "h1": "margin:0 0 22px;font-size:26px;line-height:1.45;color:#111827;font-weight:700;",
        "divider": "margin:30px 0 18px;border:0;border-top:1px solid #e5e7eb;height:0;background-color:transparent;",
        "h2": "margin:0 0 14px;font-size:20px;line-height:1.45;color:#111827;font-weight:700;",
        "step": "margin:14px 0 18px;padding:16px;background-color:#f9f9fb;border:1px solid #eceef2;border-radius:10px;",
        "step_p": "margin:0 0 13px;font-size:17px;line-height:1.65;color:#2f3337;",
        "circle": "display:inline-block;width:26px;height:26px;margin-right:9px;border-radius:50%;background-color:#2563eb;color:#ffffff;text-align:center;line-height:26px;font-size:14px;font-weight:700;vertical-align:1px;",
        "step_text": "font-weight:600;color:#111827;",
    },
    "tech-manual": {
        "label": "技术手册", "section": "margin:0 auto;padding:24px 16px;background-color:#ffffff;max-width:677px;border-top:4px solid #2563eb;",
        "wrap_step": True,
        "chapter_badge": "display:inline-block;width:34px;height:30px;margin-right:11px;border-radius:5px;background-color:#2563eb;color:#ffffff;text-align:center;line-height:30px;font-size:21px;font-weight:700;vertical-align:2px;",
        "h1": "margin:0 0 24px;padding-top:4px;font-size:25px;line-height:1.45;color:#111827;font-weight:700;",
        "divider": "display:none;margin:0;border:0;",
        "h2": "margin:32px 0 16px;padding:0;font-size:20px;line-height:1.5;color:#111827;font-weight:700;",
        "step": "margin:16px 0 20px;padding:18px 18px 6px;background-color:#f9f9fb;border:1px solid #eceef2;border-radius:11px;",
        "step_p": "margin:0 0 14px;font-size:17px;line-height:1.65;color:#2f3337;",
        "circle": "display:inline-block;width:27px;height:27px;margin-right:10px;border-radius:50%;background-color:#2563eb;color:#ffffff;text-align:center;line-height:27px;font-size:14px;font-weight:700;vertical-align:1px;",
        "step_text": "font-weight:700;color:#111827;",
    },
    "editorial-journal": {
        "label": "编辑刊物", "section": "margin:0 auto;padding:30px 20px;background-color:#ffffff;max-width:677px;",
        "wrap_step": False,
        "h1": "margin:0 0 28px;padding:0 4px 20px;border-bottom:2px solid #2563eb;text-align:center;font-size:28px;line-height:1.5;color:#111827;font-weight:700;letter-spacing:.04em;",
        "divider": "margin:36px auto 20px;border:0;border-top:1px solid #e5e7eb;width:72px;height:0;background-color:transparent;",
        "h2": "margin:0 0 16px;text-align:center;font-size:20px;line-height:1.5;color:#111827;font-weight:700;letter-spacing:.06em;",
        "step": "margin:14px 0 10px;padding:11px 0;background-color:#ffffff;border:0;border-bottom:1px solid #e5e7eb;border-radius:0;",
        "step_p": "margin:0;font-size:16px;line-height:1.7;color:#2f3337;",
        "circle": "display:inline-block;width:26px;height:26px;margin-right:10px;border-radius:50%;background-color:#2563eb;color:#ffffff;text-align:center;line-height:26px;font-size:13px;font-weight:700;vertical-align:1px;",
        "step_text": "font-weight:600;color:#111827;letter-spacing:.02em;",
    },
    "step-focus": {
        "label": "步骤聚焦", "section": "margin:0 auto;padding:24px 16px;background-color:#ffffff;max-width:677px;",
        "wrap_step": True,
        "h1": "margin:0 0 24px;font-size:26px;line-height:1.45;color:#111827;font-weight:700;",
        "divider": "margin:32px 0 16px;border:0;border-top:1px solid #e5e7eb;height:0;background-color:transparent;",
        "h2": "margin:0 0 16px;padding:9px 12px;background-color:#f9f9fb;border-left:5px solid #2563eb;border-radius:0 6px 6px 0;font-size:20px;line-height:1.5;color:#111827;font-weight:700;",
        "step": "margin:14px 0 20px;padding:18px 18px 6px;background-color:#f9f9fb;border:1px solid #eceef2;border-left:4px solid #2563eb;border-radius:10px;",
        "step_p": "margin:0 0 14px;font-size:17px;line-height:1.7;color:#2f3337;",
        "circle": "display:inline-block;width:30px;height:30px;margin-right:10px;border-radius:50%;background-color:#2563eb;color:#ffffff;text-align:center;line-height:30px;font-size:14px;font-weight:700;vertical-align:1px;",
        "step_text": "font-weight:700;color:#111827;",
    },
    "quiet-notes": {
        "label": "知识笔记", "section": "margin:0 auto;padding:26px 18px;background-color:#ffffff;max-width:677px;",
        "wrap_step": False,
        "h1": "margin:0 0 24px;padding:4px 0 4px 14px;border-left:5px solid #2563eb;font-size:25px;line-height:1.5;color:#111827;font-weight:700;",
        "divider": "display:none;margin:0;border:0;",
        "h2": "margin:30px 0 14px;padding:0 0 8px;border-bottom:2px solid #e5e7eb;font-size:20px;line-height:1.5;color:#111827;font-weight:700;",
        "step": "margin:12px 0 8px;padding:8px 0;background-color:#ffffff;border:0;border-radius:0;",
        "step_p": "margin:0;font-size:16px;line-height:1.7;color:#2f3337;",
        "circle": "display:inline-block;width:25px;height:25px;margin-right:9px;border:1px solid #2563eb;border-radius:50%;background-color:#ffffff;color:#2563eb;text-align:center;line-height:23px;font-size:13px;font-weight:700;vertical-align:1px;",
        "step_text": "font-weight:600;color:#111827;",
    },
}

PALETTES = {
    "github-blue": {
        "label": "GitHub 蓝",
        "#2563eb": "#0969da", "#111827": "#24292f", "#2f3337": "#24292f",
        "#7a7f87": "#57606a", "#f9f9fb": "#f6f8fa", "#e5e7eb": "#d0d7de",
        "#eceef2": "#d8dee4", "#f1f3f5": "#f6f8fa", "#b42318": "#cf222e",
    },
    "nord-arctic": {
        "label": "Nord 冰川",
        "#2563eb": "#4c6f95", "#111827": "#2e3440", "#2f3337": "#3b4252",
        "#7a7f87": "#667080", "#f9f9fb": "#eceff4", "#e5e7eb": "#d8dee9",
        "#eceef2": "#d8dee9", "#f1f3f5": "#e5e9f0", "#b42318": "#bf616a",
    },
    "solarized-paper": {
        "label": "Solarized 米白",
        "#ffffff": "#fffdf5", "#2563eb": "#1c6f9e", "#111827": "#073642",
        "#2f3337": "#586e75", "#7a7f87": "#607780", "#f9f9fb": "#fdf6e3",
        "#e5e7eb": "#eee8d5", "#eceef2": "#e4ddc9", "#f1f3f5": "#eee8d5",
        "#b42318": "#dc322f",
    },
    "material-indigo": {
        "label": "Material 靛蓝",
        "#2563eb": "#4f46e5", "#111827": "#1e1b4b", "#2f3337": "#312e55",
        "#7a7f87": "#6b6b83", "#f9f9fb": "#f5f3ff", "#e5e7eb": "#ddd6fe",
        "#eceef2": "#e4e0f7", "#f1f3f5": "#ede9fe", "#b42318": "#c026d3",
    },
    "jade-editorial": {
        "label": "翡翠刊物",
        "#2563eb": "#087f5b", "#111827": "#16352c", "#2f3337": "#29443b",
        "#7a7f87": "#65766f", "#f9f9fb": "#f1f8f5", "#e5e7eb": "#cfe5dc",
        "#eceef2": "#dbece5", "#f1f3f5": "#e6f3ee", "#b42318": "#b54708",
    },
    "burgundy-journal": {
        "label": "勃艮第刊物",
        "#2563eb": "#8a2942", "#111827": "#3d1f28", "#2f3337": "#49363c",
        "#7a7f87": "#7d6970", "#f9f9fb": "#fbf5f6", "#e5e7eb": "#ead8dd",
        "#eceef2": "#f0e1e5", "#f1f3f5": "#f7ecef", "#b42318": "#a61b35",
    },
    "amber-coffee": {
        "label": "咖啡琥珀",
        "#ffffff": "#fffdf9", "#2563eb": "#a15c12", "#111827": "#3c2a21",
        "#2f3337": "#4b3a31", "#7a7f87": "#7b6a60", "#f9f9fb": "#faf4e8",
        "#e5e7eb": "#e8dac4", "#eceef2": "#eee2d0", "#f1f3f5": "#f4eadb",
        "#b42318": "#8a4b12",
    },
}


class StructureValidator(HTMLParser):
    void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.void_tags:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            self.errors.append(f"unexpected closing tag </{tag}>")
        elif self.stack[-1] != tag:
            self.errors.append(f"mismatched closing tag </{tag}>; expected </{self.stack[-1]}>")
        else:
            self.stack.pop()

    def finish(self) -> list[str]:
        if self.stack:
            self.errors.append("unclosed tags: " + ", ".join(self.stack))
        return self.errors


def inline(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"`([^`]+)`", r'<code style="padding:2px 5px;background-color:#f1f3f5;border-radius:4px;font-family:Consolas,Monaco,monospace;font-size:14px;color:#b42318;">\1</code>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r'<strong style="font-weight:700;color:#111827;">\1</strong>', value)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2" style="color:#2563eb;text-decoration:none;">\1</a>', value)
    return value


def apply_palette(doc: str, palette_name: str) -> str:
    palette = PALETTES[palette_name]
    colors = {key: value for key, value in palette.items() if key.startswith("#")}
    pattern = re.compile("|".join(re.escape(key) for key in sorted(colors, key=len, reverse=True)), re.I)
    return pattern.sub(lambda match: colors.get(match.group(0).lower(), match.group(0)), doc)


def contrast_ratio(foreground: str, background: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate_palette(palette_name: str) -> list[str]:
    palette = PALETTES[palette_name]
    color = lambda token: palette.get(token, token)
    pairs = {
        "body/background": (color("#2f3337"), color("#ffffff")),
        "muted/background": (color("#7a7f87"), color("#ffffff")),
        "accent/background": (color("#2563eb"), color("#ffffff")),
        "white/accent": (color("#ffffff"), color("#2563eb")),
    }
    return [f"palette contrast below 4.5:1 for {name} ({contrast_ratio(fg, bg):.2f}:1)" for name, (fg, bg) in pairs.items() if contrast_ratio(fg, bg) < 4.5]


def render(md: str, mode: str, palette_name: str, template_name: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    layout = TEMPLATES[template_name]
    out = [f'<section style="{layout["section"]}">']
    in_code = False
    code_lines: list[str] = []
    list_kind = None
    step = 0
    in_step = False

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            out.append(f'</{list_kind}>')
            list_kind = None

    def close_step() -> None:
        nonlocal in_step
        if in_step:
            close_list()
            out.append('</section>')
            in_step = False

    for raw in lines + [""]:
        if raw.startswith("```"):
            close_list()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                code = html.escape("\n".join(code_lines))
                out.append('<pre style="margin:12px 0 18px;padding:14px 16px;background-color:#f1f3f5;border:1px solid #e5e7eb;border-radius:8px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;"><code style="font-family:Consolas,Monaco,monospace;font-size:13px;line-height:1.65;color:#2f3337;">' + code + '</code></pre>')
                in_code = False
            continue
        if in_code:
            code_lines.append(raw)
            continue
        if not raw.strip():
            close_list()
            continue
        image = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", raw.strip())
        if image:
            close_list()
            alt, src = image.groups()
            out.append(f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy" style="display:block;max-width:100%;height:auto;margin:14px auto 6px;border-radius:8px;border:1px solid #e5e7eb;" />')
            out.append(f'<p style="margin:0 0 18px;text-align:center;font-size:13px;line-height:1.6;color:#7a7f87;">{inline(alt)}</p>')
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", raw)
        if heading:
            close_step()
            close_list()
            level, title = len(heading.group(1)), inline(heading.group(2))
            if level == 2 and "display:none" not in layout["divider"].replace(" ", ""):
                out.append(f'<hr style="{layout["divider"]}" />')
            sizes = {1: "26px", 2: "20px", 3: "18px"}
            margins = {1: "0 0 22px", 2: "0 0 14px", 3: "24px 0 10px"}
            heading_style = layout["h1"] if level == 1 else layout["h2"] if level == 2 else f'margin:{margins[level]};font-size:{sizes[level]};line-height:1.45;color:#111827;font-weight:700;'
            if level == 2 and layout.get("chapter_badge"):
                title = f'<span aria-hidden="true" style="{layout["chapter_badge"]}">≡</span>{title}'
            out.append(f'<h{level} style="{heading_style}">{title}</h{level}>')
            continue
        quote = re.match(r"^>\s?(.+)$", raw)
        if quote:
            close_list()
            out.append(f'<p style="margin:12px 0 18px;padding:12px 14px;background-color:#fff7ed;border-left:4px solid #f59e0b;border-radius:4px;font-size:15px;line-height:1.75;color:#7c2d12;">{inline(quote.group(1))}</p>')
            continue
        ordered = re.match(r"^\d+[.)]\s+(.+)$", raw)
        bullet = re.match(r"^[-*]\s+(.+)$", raw)
        if ordered:
            close_step()
            close_list()
            step += 1
            out.append(f'<section style="{layout["step"]}">')
            out.append(f'<p style="{layout["step_p"]}"><span style="{layout["circle"]}">{step}</span><span style="{layout["step_text"]}">{inline(ordered.group(1))}</span></p>')
            if layout["wrap_step"]:
                in_step = True
            else:
                out.append('</section>')
            continue
        if bullet:
            if list_kind != "ul":
                close_list(); list_kind = "ul"
                out.append('<ul style="margin:8px 0 18px;padding-left:22px;color:#2f3337;">')
            out.append(f'<li style="margin:6px 0;font-size:16px;line-height:1.75;">{inline(bullet.group(1))}</li>')
            continue
        close_list()
        out.append(f'<p style="{P}">{inline(raw.strip())}</p>')
    close_step()
    close_list()
    if in_code:
        raise ValueError("Unclosed Markdown code fence")
    out.append('</section>')
    body = "\n".join(out)
    doc = '<!doctype html>\n<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background-color:#ffffff;">\n' + body + "\n</body></html>\n"
    return apply_palette(doc, palette_name)


def validate(doc: str) -> list[str]:
    errors = []
    structure = StructureValidator()
    structure.feed(doc)
    errors.extend(structure.finish())
    banned = [r"\bclass\s*=", r"<style\b", r"<script\b"]
    for pattern in banned:
        if re.search(pattern, doc, re.I):
            errors.append(f"banned pattern: {pattern}")
    unsafe_css = [r"display\s*:\s*(flex|grid)", r"position\s*:\s*(absolute|fixed)", r"linear-gradient"]
    for style in re.findall(r"\bstyle\s*=\s*[\"']([^\"']*)[\"']", doc, re.I):
        for pattern in unsafe_css:
            if re.search(pattern, style, re.I):
                errors.append(f"banned CSS in style attribute: {pattern}")
    for tag in ("section", "p", "span"):
        for match in re.finditer(fr"<{tag}\b([^>]*)>", doc, re.I):
            if not re.search(r"\bstyle\s*=\s*[\"'][^\"']+[\"']", match.group(1), re.I):
                errors.append(f"<{tag}> missing non-empty style")
    headings = [int(value) for value in re.findall(r"<h([1-6])\b", doc, re.I)]
    if headings.count(1) != 1:
        errors.append(f"expected exactly one <h1>, found {headings.count(1)}")
    for previous, current in zip(headings, headings[1:]):
        if current > previous + 1:
            errors.append(f"heading level jumps from h{previous} to h{current}")
    for match in re.finditer(r"<img\b([^>]*)>", doc, re.I):
        attrs = match.group(1)
        if not re.search(r"\balt\s*=\s*[\"'][^\"']*[\"']", attrs, re.I):
            errors.append("<img> missing alt attribute")
        if not re.search(r"\bloading\s*=\s*[\"']lazy[\"']", attrs, re.I):
            errors.append("<img> missing loading=lazy")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="?")
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--mode", choices=("text", "screenshots"), default="text")
    parser.add_argument("--palette", choices=tuple(PALETTES), default="github-blue")
    parser.add_argument("--template", choices=tuple(TEMPLATES), default="clean-guide")
    parser.add_argument("--list-palettes", action="store_true")
    parser.add_argument("--list-templates", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if args.list_palettes:
        for name, values in PALETTES.items():
            print(f"{name}: {values['label']}")
        return 0
    if args.list_templates:
        for name, values in TEMPLATES.items():
            print(f"{name}: {values['label']}")
        return 0
    if args.input is None or args.output is None:
        parser.error("input and --output are required unless listing palettes or templates")
    doc = render(args.input.read_text(encoding="utf-8-sig"), args.mode, args.palette, args.template)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(doc, encoding="utf-8")
    if args.validate:
        errors = validate(doc)
        errors.extend(validate_palette(args.palette))
        if errors:
            print("Validation failed:\n- " + "\n- ".join(errors))
            return 1
        print(f"Validation passed: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
