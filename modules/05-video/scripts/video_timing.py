#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配音时长估算 —— 只算，不设限。

TikTok 不限制视频时长、不限制字幕字符数、不限制语速，所以这里**不做合格判定**，
只回答一个问题：这段台词念出来大约多少秒，塞进目标时长够不够。

  python3 scripts/video_timing.py --script 配音稿.txt
  python3 scripts/video_timing.py --script 配音稿.txt --target 15 --wps 2.8

一行台词 = 一个分镜。空行与 # 注释忽略。
语速是物理经验值（不是平台规则），默认 2.5 词/秒，可用 --wps 改。
"""
import argparse
import json
import sys
import unicodedata
from pathlib import Path

DEFAULT_WPS = 2.5


def _emoji(text: str) -> bool:
    return any(unicodedata.category(c) in ("So", "Sk") or ord(c) >= 0x1F000 for c in text)


def main():
    ap = argparse.ArgumentParser(description="配音时长估算（不设限）")
    ap.add_argument("--script", required=True)
    ap.add_argument("--wps", type=float, default=DEFAULT_WPS, help="语速 词/秒（默认 2.5）")
    ap.add_argument("--target", type=float, help="可选：目标时长（秒），给了才做对比")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    p = Path(a.script)
    if not p.exists():
        sys.exit(f"[INPUT_MISSING] 找不到 {a.script}")
    lines = [x.strip() for x in p.read_text(encoding="utf-8").splitlines()
             if x.strip() and not x.strip().startswith("#")]
    if not lines:
        sys.exit(f"[INPUT_MISSING] {a.script} 没有有效台词")

    rows, t, notes = [], 0.0, []
    for i, text in enumerate(lines, 1):
        w = len(text.split())
        dur = w / a.wps
        rows.append(dict(index=i, text=text, words=w, chars=len(text),
                         est_seconds=round(dur, 2), timeline=f"{t:.1f}s → {t + dur:.1f}s"))
        if _emoji(text):
            notes.append(f"第 {i} 句疑似 emoji/特殊符号")
        t += dur
    total = round(t, 2)

    verdict = None
    if a.target:
        diff = round(total - a.target, 1)
        verdict = (f"口播 {total}s / 目标 {a.target:g}s，"
                   + (f"多 {diff}s（删词或减镜头）" if diff > 0 else f"余 {abs(diff)}s"))

    out = dict(wps=a.wps, total_seconds=total, target=a.target, verdict=verdict,
               rows=rows, notes=notes)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"\n语速 {a.wps} 词/秒 ｜ 共 {len(rows)} 句 ｜ 总口播 {total}s\n")
        print(f"{'#':<3}{'时长':<18}{'词':>4}{'字':>5}  台词")
        for r in rows:
            print(f"{r['index']:<3}{r['timeline']:<18}{r['words']:>4}{r['chars']:>5}  {r['text'][:44]}")
        if verdict:
            print(f"\n{verdict}")
        for n in notes:
            print(f"  ⚠️  {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
