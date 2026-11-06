#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回归断言：只测会算钱和会放过错误的路径。零依赖。

  python3 tests/run_asserts.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "modules"
PARSER = A / "01-market-research/scripts/category_parser.py"
METRICS = A / "01-market-research/scripts/market_metrics.py"
PRICING = A / "02-product-strategy/scripts/sku_pricing.py"
LINT = A / "03-listing/scripts/title_lint.py"
SCAN = A / "03-listing/scripts/compliance_scan.py"
SPEC = A / "03-listing/scripts/spec_consistency.py"
VIDEO = A / "05-video/scripts/video_timing.py"
ADS = A / "06-ads/scripts/ad_metrics.py"
REVIEWS = A / "07-reviews/scripts/review_stats.py"
SAMPLE = ROOT / "tests/fixtures/parse-fixture.csv"

fails = []


def check(name, cond, detail=""):
    print(("  ✅ " if cond else "  ❌ ") + name + (f"  {detail}" if not cond and detail else ""))
    if not cond:
        fails.append(name)


def run(args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, env=e)


def filled_markets(tmp: Path) -> Path:
    """复制真实市场配置并填满，用于测“填完之后”的行为。"""
    d = tmp / "markets"
    shutil.copytree(ROOT / "markets", d)
    for f in d.glob("*.json"):
        cfg = json.loads(f.read_text(encoding="utf-8"))
        cfg["title"]["max_chars"] = 90
        f.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
    return d


def main():
    tmp = Path(tempfile.mkdtemp())
    mk = filled_markets(tmp)
    env = {"TT_MARKETS_DIR": str(mk)}

    print("\n[1] 数字解析：歧义不猜")
    r = run([PARSER, SAMPLE, "-o", tmp / "s.json"])
    check("样例 CSV 解析成功", r.returncode == 0, (r.stdout + r.stderr)[:200])
    if r.returncode == 0:
        d = json.loads((tmp / "s.json").read_text(encoding="utf-8"))
        check("50/50 行不丢", len(d["items"]) == d["meta"]["row_count_raw"])
    bad = tmp / "bad.csv"
    bad.write_text("商品名称,价格,月销量\nA,20.000,5\n", encoding="utf-8")
    r = run([PARSER, bad, "-o", tmp / "x.json"])
    check("歧义数字 → 非零退出", r.returncode != 0)
    check("歧义数字 → 提示 --number-locale", "--number-locale" in r.stdout + r.stderr)

    print("\n[2] 未核实的市场配置必须拒绝执行")
    r = run([PRICING, "calc", "--market", "us", "--cost", "5", "--price", "20"])
    check("定价：没给佣金率 → INPUT_MISSING", "INPUT_MISSING" in r.stdout + r.stderr, r.stdout[:150])
    r = run([LINT, "Test title", "--market", "vn", "--max-chars", "90"], env)
    check("标题：--max-chars 可覆盖", r.returncode == 0, r.stdout[:150])

    print("\n[3] 定价：达人佣金计入 + 数学正确")
    r = run([PRICING, "calc", "--market", "us", "--cost", "12", "--price", "39.99",
             "--referral-pct", "6", "--payment-pct", "2", "--affiliate-pct", "15",
             "--return-pct", "2", "--json"], env)
    check("退出码 0", r.returncode == 0, r.stderr[:200])
    if r.returncode == 0:
        o = json.loads(r.stdout)
        check("费率合计 = 6+2+15+2 = 25%", abs(o["fee_pct_total"] - 25) < 1e-9, str(o["fee_pct_total"]))
        check("广告前毛利 = 39.99-12-10.00 = 17.99", abs(o["pre_ad_margin"] - 17.99) < 0.02, str(o["pre_ad_margin"]))
        check("盈亏价 = 12/0.75 = 16.00", abs(o["break_even_price"] - 16.0) < 0.02, str(o["break_even_price"]))
        check("输出含 promo_headroom", "promo_headroom" in o)
        check("不再有 break_even_roas_at_this_ad", "break_even_roas_at_this_ad" not in o)

    print("\n[4] 合规：唯一禁词来源")
    r = run([SCAN, "--market", "us", "--title", "The Best Power Bank, Free Shipping"])
    check("绝对化+促销词 → 退出码 1", r.returncode == 1, r.stdout[:150])
    check("报出 absolute 分组", "[absolute]" in r.stdout)
    r = run([SCAN, "--market", "us", "--title", "20000mAh Power Bank, 45W USB-C"])
    check("干净标题 → 退出码 0 且写“无命中”", r.returncode == 0 and "无命中" in r.stdout)

    print("\n[5] 标题：长度与禁词")
    r = run([LINT, "Free Shipping Power Bank", "--market", "us"], env)
    check("促销词 → 未通过", r.returncode == 1, r.stdout[:150])
    r = run([LINT, "20000mAh Power Bank 45W USB-C 3 Ports LED Display", "--market", "us"], env)
    check("干净标题 → 通过", r.returncode == 0, r.stdout[:200])

    print("\n[6] 参数一致性：数值 + 单位")
    spec = tmp / "spec.csv"
    spec.write_text('参数,数值\nPotencia,"45 W"\nAutonomia,"60 km"\n', encoding="utf-8")
    ok = tmp / "ok.txt"; ok.write_text("Potencia 45 W. Autonomia 60 km.\n", encoding="utf-8")
    bad = tmp / "bad.txt"; bad.write_text("Potencia 45 km.\n", encoding="utf-8")
    check("45W 对 45W → 通过", run([SPEC, "--spec", spec, "--text", ok]).returncode == 0)
    r = run([SPEC, "--spec", spec, "--text", bad])
    check("45km 冒充 45W → 失败", r.returncode == 1 and "spec 里是 W" in r.stdout, r.stdout[:200])

    print("\n[7] 市场指标：--top 与缺列")
    norm = tmp / "s.json"
    r = run([METRICS, norm, "--top", "5", "--format", "md", "-o", tmp / "m5"])
    r = run([METRICS, SAMPLE.replace(".csv", "")] if False else [METRICS, norm, "--top", "5",
            "--format", "md", "-o", tmp / "m5"])
    nb = tmp / "nb.json"
    items = [{"price": p, "monthly_sales": s, "monthly_revenue": p * s} for p, s in [(100, 10), (200, 5), (300, 3)]]
    nb.write_text(json.dumps({"meta": {"source_file": "x"}, "items": items}, ensure_ascii=False), encoding="utf-8")
    r = run([METRICS, nb, "--format", "md", "-o", tmp / "nb"])
    check("缺品牌列 → 报不可计算", r.returncode == 0 and "不可计算" in r.stdout, r.stdout[:200])
    check("不再出现 100% 假垄断", "CR3（销售额）：100.0%" not in r.stdout)
    r = run([METRICS, tmp / "s.json", "--top", "5", "--format", "md", "-o", tmp / "m5c", "--currency", "USD"])
    check("--top 5 不崩", r.returncode == 0, (r.stdout + r.stderr)[-300:])

    print("\n[8] 广告：前段不达标不许调出价")
    ad = tmp / "ad.csv"
    ad.write_text("广告名称,曝光量,点击量,花费,订单数\nA,48200,675,210.60,3\n", encoding="utf-8")
    r = run([ADS, "diagnose", "--market", "us", "--price", "39.99", "--product-cost", "12",
             "--referral-pct", "6", "--payment-pct", "2", "--file", ad, "--min-ctr", "0.03", "--json"], env)
    check("退出码 0", r.returncode == 0, r.stderr[:300])
    if r.returncode == 0:
        acts = " ".join(json.loads(r.stdout)["campaigns"][0]["actions"])
        check("低 CTR 时给出回流素材", "回流 04" in acts, acts[:200])
        check("低 CTR 时不出价调整指令", not any(k in acts for k in ("降至", "微调", "低于")), acts[:200])

    print("\n[9] 评论：零差评不崩")
    g = tmp / "g.csv"
    g.write_text("rating,text,category\n5,otimo,\n4,bom,\n", encoding="utf-8")
    r = run([REVIEWS, "--file", g])
    check("零差评 → 退出码 0 且有说明", r.returncode == 0 and "没有差评" in r.stdout, (r.stdout + r.stderr)[-300:])

    print("\n[10] 视频：只估算不设限（TikTok 不限时长/字幕/语速）")
    v = tmp / "vo.txt"
    v.write_text("Great power bank for travel\nTwenty thousand milliamp hours\nCharges your phone fast\n"
                 "Compact and light\nBuy it today\n", encoding="utf-8")
    r = run([VIDEO, "--script", v, "--target", "15", "--json"])
    check("退出码 0", r.returncode == 0, (r.stdout + r.stderr)[:300])
    if r.returncode == 0:
        d = json.loads(r.stdout)
        check("只估算不设限：返回总秒数", d["total_seconds"] > 0, str(d.get("total_seconds")))
        check("不判合格（无 pass 字段）", "pass" not in d)

    print("\n" + "=" * 52)
    if fails:
        print(f"❌ {len(fails)} 条失败")
        for f in fails:
            print(f"   - {f}")
        return 1
    print("✅ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
