#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市场配置的唯一入口。

规则：**所有平台数字只写在 markets/<market>.json，不写进 prompt、不写进脚本。**
值为 null = 未核实。任何脚本读到 null 必须报 [UNVERIFIED] 并停下，不许用默认值顶替。

用法：
    python3 lib/market_config.py --check          # 看 5 个市场还差哪些字段
    python3 lib/market_config.py --check us       # 只看 us
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETS = Path(os.environ.get("TT_MARKETS_DIR", ROOT / "markets"))
CORE = ROOT / "core"

# 只有"平台写死的数字"才放配置。费率不在这里——每个类目、每个达人都不同，
# 必须在下单/投放那一步由使用者当场填（脚本会强制要求）。
REQUIRED = [
    "title.max_chars",
]


class MissingField(Exception):
    """字段未核实。消息本身就告诉使用者去哪查、查哪个字段。"""


def load(market: str) -> dict:
    p = MARKETS / f"{market}.json"
    if not p.exists():
        avail = "、".join(sorted(x.stem for x in MARKETS.glob("*.json")))
        raise MissingField(f"[INPUT_MISSING] 没有市场配置 {market}。可用：{avail}")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def get(cfg: dict, dotted: str):
    """取一个嵌套字段；null 或不存在 → 抛 MissingField。"""
    cur = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise MissingField(f"[UNVERIFIED] markets/{cfg.get('market')}.json 缺字段 {dotted}")
        cur = cur[part]
    if cur is None:
        raise MissingField(
            f"[UNVERIFIED] markets/{cfg.get('market')}.json → {dotted} 未核实。\n"
            f"             去卖家中心查到后填入，再重跑。不要用默认值顶替。"
        )
    return cur


def missing(cfg: dict) -> list:
    out = []
    for key in REQUIRED:
        try:
            get(cfg, key)
        except MissingField:
            out.append(key)
    return out


def ready(cfg: dict) -> bool:
    return not missing(cfg)


def check_all(only: str | None = None) -> int:
    files = sorted(MARKETS.glob("*.json"))
    if only:
        files = [f for f in files if f.stem == only]
    if not files:
        print("[INPUT_MISSING] markets/ 下没有配置文件")
        return 1
    bad = 0
    for f in files:
        cfg = json.loads(f.read_text(encoding="utf-8"))
        miss = missing(cfg)
        head = f"{f.stem:<4} {cfg.get('currency'):<4}"
        if not miss:
            print(f"✅ {head} 可以跑")
            continue
        bad += 1
        print(f"⚠️  {head} 还差 {len(miss)} 项：")
        for m in miss:
            print(f"      · {m}")
    print()
    if bad:
        print(f"{bad} 个市场未就绪。填 markets/<market>.json 里对应的 null 即可，不用改任何脚本。")
        return 2
    print("全部市场就绪。")
    return 0


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] != "--check":
        print(__doc__)
        sys.exit(1)
    sys.exit(check_all(args[1] if len(args) > 1 else None))


if __name__ == "__main__":
    main()
