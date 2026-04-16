#!/usr/bin/env python3
"""
Translate remaining Chinese in en/*.html using Google (deep-translator).

Policy:
- HTML body (notes, headings, etc.): translate any text node that still contains CJK.
- Inline <script> quiz data: quiz stems (`text:`), `options:`, `correct:`, `num:` are
  already English — those lines are never sent to the translator.
  Lines that contain CJK (mostly `explanations` strings and mixed notes) are translated.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPS = ROOT / "tools" / "pydeps"
sys.path.insert(0, str(DEPS))

from bs4 import BeautifulSoup  # noqa: E402
from deep_translator import GoogleTranslator  # noqa: E402

CJK = re.compile(r"[\u4e00-\u9fff]")
translator = GoogleTranslator(source="zh-CN", target="en")
_cache: dict[str, str] = {}


def tr(s: str) -> str:
    if not s or not CJK.search(s):
        return s
    key = s
    if key in _cache:
        return _cache[key]
    try:
        out = translator.translate(s)
        _cache[key] = out
        return out
    except Exception as e:
        print("TRANSLATE FAIL:", repr(s[:100]), e)
        return s


def _skip_quiz_metadata_line(line: str) -> bool:
    """Skip question/options/correct — already English; do not machine-translate."""
    lst = line.lstrip()
    if lst.startswith("text:"):
        return True
    if lst.startswith("options:"):
        return True
    if lst.startswith("correct:"):
        return True
    if lst.startswith("num:"):
        return True
    return False


def translate_script_body(body: str) -> str:
    lines = body.split("\n")
    out = []
    for line in lines:
        if _skip_quiz_metadata_line(line):
            out.append(line)
            continue
        if CJK.search(line) and len(line) < 12000:
            out.append(tr(line))
        else:
            out.append(line)
    return "\n".join(out)


def translate_html_string(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent is None:
            continue
        if parent.name in ("script", "style"):
            continue
        if CJK.search(str(text_node)):
            text_node.replace_with(tr(str(text_node)))

    for script in soup.find_all("script"):
        if script.get("src"):
            continue
        if not script.string or not CJK.search(script.string):
            continue
        new_body = translate_script_body(script.string)
        script.string.replace_with(new_body)

    return str(soup)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=Path)
    args = ap.parse_args()
    files = args.files if args.files else sorted(ROOT.glob("en/*.html"))
    for path in files:
        path = Path(path)
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        if not CJK.search(raw):
            print(path.name, "skip (no CJK)")
            continue
        print("Translating", path.name, "...")
        try:
            out = translate_html_string(raw)
        except Exception as e:
            print("FAIL", path, e)
            continue
        path.write_text(out, encoding="utf-8")
        print("  ->", len(CJK.findall(out)), "CJK chars left")


if __name__ == "__main__":
    main()
