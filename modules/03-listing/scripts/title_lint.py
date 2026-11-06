#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TikTok 标题校验 —— 字符数是实测值，不是估算。

  python3 scripts/title_lint.py "标题文本" --market us
  python3 scripts/title_lint.py --file titles.txt --market uk --keywords "power bank,20000mah"
  python3 scripts/title_lint.py "标题" --market us --json

标题上限来自 markets/<market>.json（未核实会直接报 [UNVERIFIED]）；
禁词来自 core/compliance.json（与 compliance_scan.py 同一份，不另抄）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "lib"))
from market_config import MissingField, get, load  # noqa: E402

EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF]")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
# 泰语/越南语无空格分词，词数判断会失效 —— 只有拉丁语系才查堆砌与全大写
LATIN_RE = re.compile(r"[A-Za-z\u00C0-\u017F]")


def ban_terms() -> dict:
    p = ROOT / "core" / "compliance.json"
    if not p.exists():
        sys.exit(f"[INPUT_MISSING] 找不到 {p}")
    b = json.loads(p.read_text(encoding="utf-8"))["banned"]
    return {"absolute": b["absolute"]["terms"], "price_promo_in_title": b["price_promo_in_title"]["terms"]}


def analyse(title: str, cfg: dict, args, ban: dict) -> dict:
    t = title.strip()
    n = len(t)
    limit = args.max_chars or get(cfg, "title.max_chars")
    res = []

    if n > limit:
        res.append(("FAIL", "length", f"{n} 字符 > 上限 {limit} —— 超出会被截断"))
    elif n < limit * 0.7:
        res.append(("WARN", "length", f"{n}/{limit} 字符（利用率 {n / limit:.0%}），建议补到 80%+"))
    else:
        res.append(("PASS", "length", f"{n}/{limit} 字符"))

    low = t.lower()
    for group, terms in ban.items():
        hits = [w for w in terms if re.search(rf"(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])", low)]
        if hits:
            res.append(("FAIL", group, f"命中：{'、'.join(hits)}"))
        else:
            res.append(("PASS", group, f"0 命中（查了 {len(terms)} 个词）"))

    if args.forbidden:
        extra = [w.strip() for w in args.forbidden.split(",") if w.strip()]
        hits = [w for w in extra if w.lower() in low]
        res.append(("FAIL" if hits else "PASS", "forbidden",
                    f"命中自定义禁词：{'、'.join(hits)}" if hits else f"0 命中（查了 {len(extra)} 个词）"))

    if args.keywords:
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        miss = [k for k in kws if k.lower() not in low]
        res.append(("WARN" if miss else "PASS", "keywords",
                    f"核心词未覆盖：{'、'.join(miss)}" if miss else f"{len(kws)} 个核心词全覆盖"))

    if EMOJI_RE.search(t):
        res.append(("FAIL", "emoji", f"表情/符号：{EMOJI_RE.findall(t)[:5]}"))

    if LATIN_RE.search(t):
        caps = [w for w in re.findall(r"[A-Za-z]{4,}", t) if w.isupper()]
        if caps:
            res.append(("WARN", "all_caps", f"全大写词：{'、'.join(caps[:6])}"))
        words = re.findall(r"[A-Za-z\u00C0-\u017F0-9]+", low)
        dup = [w for w in set(words) if words.count(w) >= 3 and len(w) > 2]
        if dup:
            res.append(("FAIL", "duplicates", f"重复 ≥3 次：{'、'.join(dup)}（堆砌降权）"))

    if CJK_RE.search(t):
        res.append(("FAIL", "locale", f"标题含中文 —— 买家可见文本必须是 {cfg['language']}"))

    ok = not any(lv == "FAIL" for lv, _, _ in res)
    return dict(market=args.market, chars=n, limit=limit, ok=ok, checks=res)


def main():
    ap = argparse.ArgumentParser(description="TikTok 标题校验（字符数实测）")
    ap.add_argument("title", nargs="?")
    ap.add_argument("--file", help="一行一个标题")
    ap.add_argument("--market", required=True, help="us / uk / th / vn / id")
    ap.add_argument("--max-chars", type=int, help="临时覆盖平台标题上限（默认读市场配置）")
    ap.add_argument("--forbidden", help="额外禁词，逗号分隔")
    ap.add_argument("--keywords", help="核心关键词，逗号分隔（查覆盖）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    titles = ([x.strip() for x in Path(a.file).read_text(encoding="utf-8").splitlines() if x.strip()]
              if a.file else [a.title] if a.title else [])
    if not titles:
        sys.exit("[INPUT_MISSING] 给标题文本或 --file")

    try:
        cfg = load(a.market)
        reports = [analyse(t, cfg, a, ban_terms()) for t in titles]
        limit = reports[0]["limit"]
    except MissingField as e:
        sys.exit(str(e))

    if a.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], ensure_ascii=False, indent=2))
    else:
        icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌"}
        for r in reports:
            print(f"\n「{r['chars']} / {limit} 字符」  总判定: {'✅ 通过' if r['ok'] else '❌ 未通过'}")
            for lv, name, detail in r["checks"]:
                print(f"  {icon[lv]} {name:<20} {detail}")
    sys.exit(0 if all(r["ok"] for r in reports) else 1)


if __name__ == "__main__":
    main()
