#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容合规扫描 —— 唯一禁词来源是 core/compliance.json。

  python3 scripts/compliance_scan.py --market us --title "..." --text 文案.txt
  python3 scripts/compliance_scan.py --market uk --text 详情.md --json

只报命中的字面词，不做语义推断（推断留给 Agent）。无命中时也输出 "无命中"，
避免"真没命中"和"忘了扫"分不清。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "core"


def load_banlist() -> dict:
    p = CORE / "compliance.json"
    if not p.exists():
        sys.exit(f"[INPUT_MISSING] 找不到 {p}")
    return json.loads(p.read_text(encoding="utf-8"))["banned"]


def scan(text: str, ban: dict) -> list:
    low = text.lower()
    hits = []
    for group, spec in ban.items():
        for term in spec["terms"]:
            start = low.find(term.lower())
            while start != -1:
                # 词边界：前后不能是字母数字，避免 "off" 命中 "office"
                before = low[start - 1] if start else " "
                after = low[start + len(term):start + len(term) + 1] or " "
                if not before.isalnum() and not after.isalnum():
                    hits.append(dict(group=group, term=term,
                                     context=text[max(0, start - 30):start + len(term) + 30].replace("\n", " "),
                                     reason=spec["reason"]))
                    break
                start = low.find(term.lower(), start + 1)
    return hits


def main() -> None:
    ap = argparse.ArgumentParser(description="TikTok 内容合规扫描（字面命中，不做语义推断）")
    ap.add_argument("--market", required=True, help="市场代码：us / uk / th / vn / id")
    ap.add_argument("--title", help="标题文本")
    ap.add_argument("--text", help="文案文件（详情/字幕/图内文案）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.title and not a.text:
        sys.exit("[INPUT_MISSING] 给 --title 或 --text")

    text = ""
    if a.title:
        text += a.title + "\n"
    if a.text:
        p = Path(a.text)
        if not p.exists():
            sys.exit(f"[INPUT_MISSING] 找不到 {a.text}")
        text += p.read_text(encoding="utf-8")

    hits = scan(text, load_banlist())
    rep = dict(market=a.market, chars=len(text.strip()), hits=hits, ok=not hits)

    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"\n市场 {a.market} ｜ 扫描 {rep['chars']} 字符 ｜ "
              f"总判定: {'✅ 无命中' if rep['ok'] else f'❌ 命中 {len(hits)} 处'}")
        for h in hits:
            print(f"  ❌ [{h['group']}] {h['term']!r}: …{h['context']}…")
            print(f"      {h['reason']}")
        if not hits:
            print("  合规扫描：无命中")
    sys.exit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()
