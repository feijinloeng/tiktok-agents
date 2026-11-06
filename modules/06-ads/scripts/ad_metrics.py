#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TikTok 广告诊断 —— 只算，不猜，不执行。

  python3 scripts/ad_metrics.py calc --market us --price 39.99 --product-cost 12 --shipping 4
  python3 scripts/ad_metrics.py diagnose --market us --price 39.99 --product-cost 12 \
      --file 广告报表.csv --target-roas 3

费率来自 markets/<market>.json。CSV 列名自动识别中/英；加购列可选——
**没有加购列就不会假装做了四段漏斗**，只做 CTR → 转化率 → ROAS。

漏斗纪律（硬规则）：前面一环不达标，就不许输出出价/预算调整。
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "lib"))
from market_config import MissingField, get, load  # noqa: E402

COLS = {
    "name": ["广告名称", "广告组", "计划名称", "campaign", "name", "ad_group", "adgroup"],
    "impressions": ["曝光量", "曝光", "展示量", "impressions", "imps"],
    "clicks": ["点击量", "点击数", "点击", "clicks"],
    "spend": ["花费", "消耗", "花费金额", "spend", "cost"],
    "orders": ["订单数", "订单", "成交订单", "orders", "conversions"],
    "gmv": ["销售额", "成交金额", "广告销售额", "gmv", "revenue"],
    "atc": ["加购", "加购数", "加入购物车", "add_to_cart", "atc"],
}


def _num(v, default=0.0, integer=False):
    if v is None:
        return default
    s = str(v).strip().replace(",", "").replace(" ", "").replace("%", "")
    for sym in ("R$", "$", "£", "฿"):
        s = s.replace(sym, "")
    if s in ("", "-", "—", "N/A", "nan"):
        return default
    try:
        return int(float(s)) if integer else float(s)
    except ValueError:
        return default


def _pick(header, kind):
    low = {h.strip().lower(): h for h in header}
    for cand in COLS[kind]:
        if cand.lower() in low:
            return low[cand.lower()]
    return None


def cost_model(args, cfg) -> dict:
    # 佣金/支付费率按类目不同，一律当场填；不猜、不设默认
    if args.referral_pct is None or args.payment_pct is None:
        sys.exit("[INPUT_MISSING] 缺 --referral-pct 或 --payment-pct（按类目查，脚本不猜）")
    referral, payment = float(args.referral_pct), float(args.payment_pct)
    pct = referral + payment + args.return_pct + args.tax_pct
    contrib = args.price - args.product_cost - args.shipping - args.price * pct / 100
    be_acos = contrib / args.price if args.price else 0
    return dict(market=args.market, currency=cfg["currency"], price=args.price,
                referral_pct=referral, payment_pct=payment,
                return_pct=args.return_pct, tax_pct=args.tax_pct,
                pre_ad_contribution=round(contrib, 2),
                break_even_acos=round(be_acos, 4),
                break_even_roas=round(1 / be_acos, 2) if be_acos > 0 else None)


def grade(row, m, args, be_roas, has_atc):
    """按漏斗顺序判，前段不达标就不碰出价。返回 (级别, 动作, 指标)。"""
    imp, clk = row["impressions"], row["clicks"]
    spend, orders = row["spend"], row["orders"]
    gmv = row["gmv"] or orders * m["price"]
    ctr = clk / imp if imp else 0
    cvr = orders / clk if clk else 0
    cpc = spend / clk if clk else 0
    atc_rate = (row["atc"] / clk) if (has_atc and clk) else None
    roas = gmv / spend if spend else None
    met = dict(ctr=round(ctr, 4), cvr=round(cvr, 4), cpc=round(cpc, 2),
               atc_rate=round(atc_rate, 4) if atc_rate is not None else None,
               roas=round(roas, 2) if roas else None, gmv=round(gmv, 2))
    acts = []

    if imp < args.min_impressions:
        return "INFO", [f"曝光 {imp:,.0f} < {args.min_impressions:,}，数据不足，本轮不动"], met
    if not spend:
        return "INFO", ["无花费，本轮不动"], met

    # ① CTR —— 素材问题，回流 04
    if ctr < args.min_ctr:
        acts.append(f"CTR {ctr:.2%} < {args.min_ctr:.0%} —— 回流 04 换首帧/主图（这是素材问题，不是出价问题）")
        acts.append("本轮不动出价与预算：前段不达标时不调出价（调了只是换个方式烧钱）")
        return "P0", acts, met

    # ② 加购（有数据才判）
    if has_atc and atc_rate is not None and atc_rate < args.min_atc:
        acts.append(f"加购率 {atc_rate:.2%} < {args.min_atc:.0%} —— 有点击没加购，回流 03 改价格展示/卖点顺序")
        acts.append("本轮不动出价与预算")
        return "P1", acts, met

    # ③ 转化率
    if cvr < args.min_cvr:
        acts.append(f"转化率 {cvr:.2%} < {args.min_cvr:.0%} —— 加购了不下单，回流 07 看评价/售后承诺")
        acts.append("本轮不动出价与预算")
        return "P1", acts, met

    # ④ 到这里才允许谈钱
    if roas is None or be_roas is None:
        return "INFO", ["缺盈亏线或 ROAS，无法判定"], met
    if roas < be_roas * 0.5:
        acts.append(f"ROAS {roas:.2f} < 盈亏线一半（{be_roas:.2f}）—— P0 止血")
        acts.append("预算降到最低档；不要暂停（暂停伤连续性）")
    elif roas < be_roas:
        acts.append(f"ROAS {roas:.2f} < 盈亏线 {be_roas:.2f} —— P1 改善")
        acts.append(f"出价按可承受 CPC {m['price'] * cvr * be_roas / 100:.2f} 以下微调，预算暂不动")
    elif args.target_roas and roas < args.target_roas:
        acts.append(f"ROAS {roas:.2f} 在盈亏线与目标 {args.target_roas} 之间 —— 维持，预算出价都不动")
    else:
        acts.append(f"ROAS {roas:.2f} ≥ 目标 —— P2 放量，预算 +20~30%，观察 3 天")
    acts.append("本轮明确不动：素材与 listing（一次只改一个病因）")
    return ("P0" if roas < be_roas * 0.5 else "P2" if roas >= (args.target_roas or be_roas) else "P1"), acts, met


def main():
    ap = argparse.ArgumentParser(description="TikTok 广告诊断（只算不执行）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("calc", "diagnose"):
        p = sub.add_parser(name)
        p.add_argument("--market", required=True)
        p.add_argument("--price", type=float, required=True)
        p.add_argument("--product-cost", type=float, required=True)
        p.add_argument("--shipping", type=float, default=0, help="尾程运费/件")
        p.add_argument("--referral-pct", type=float, help="平台佣金率 %%（必填）")
        p.add_argument("--payment-pct", type=float, help="支付处理费率 %%（必填）")
        p.add_argument("--return-pct", type=float, default=0)
        p.add_argument("--tax-pct", type=float, default=0)
        p.add_argument("--json", action="store_true")
        if name == "diagnose":
            p.add_argument("--file", required=True)
            p.add_argument("--target-roas", type=float)
            p.add_argument("--min-impressions", type=int, default=1000)
            p.add_argument("--min-ctr", type=float, default=0.01, help="CTR 及格线（默认 1%%）")
            p.add_argument("--min-atc", type=float, default=0.08, help="加购率及格线（默认 8%%）")
            p.add_argument("--min-cvr", type=float, default=0.01, help="转化率及格线（默认 1%%）")
    a = ap.parse_args()

    try:
        cfg = load(a.market)
        m = cost_model(a, cfg)
    except MissingField as e:
        sys.exit(str(e))

    if a.cmd == "calc":
        out = dict(mode="calc", **m)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        if not a.json:
            print(f"\n{m['market']} ｜ 佣金 {m['referral_pct']}% + 支付 {m['payment_pct']}%"
                  f" ｜ 广告前贡献 {m['currency']} {m['pre_ad_contribution']:,.2f}"
                  f" ｜ 盈亏线 ROAS {m['break_even_roas']}（ACoS {m['break_even_acos']:.1%}）")
        return 0

    p = Path(a.file)
    if not p.exists():
        sys.exit(f"[INPUT_MISSING] 找不到 {a.file}")
    rows = list(csv.DictReader(p.open(encoding="utf-8-sig")))
    if not rows:
        sys.exit(f"[INPUT_MISSING] {a.file} 没有数据行")
    header = list(rows[0])
    col = {k: _pick(header, k) for k in COLS}
    need = ["name", "impressions", "clicks", "spend", "orders"]
    miss = [k for k in need if not col[k]]
    if miss:
        sys.exit(f"[INPUT_MISSING] 认不出列：{miss}（表头：{header}）")
    has_atc = bool(col["atc"])

    results, total_spend, total_gmv = [], 0.0, 0.0
    for r in rows:
        row = dict(name=(r.get(col["name"]) or "?").strip(),
                   impressions=_num(r.get(col["impressions"]), integer=True),
                   clicks=_num(r.get(col["clicks"]), integer=True),
                   spend=_num(r.get(col["spend"])),
                   orders=_num(r.get(col["orders"]), integer=True),
                   gmv=_num(r.get(col["gmv"])) if col["gmv"] else 0.0,
                   atc=_num(r.get(col["atc"]), integer=True) if has_atc else 0)
        lvl, acts, met = grade(row, m, a, m["break_even_roas"], has_atc)
        total_spend += row["spend"]
        total_gmv += met["gmv"]
        results.append(dict(campaign=row["name"], grade=lvl, **met, actions=acts))

    out = dict(mode="diagnose", cost_model=m, has_atc=has_atc,
               total=dict(campaigns=len(results), spend=round(total_spend, 2),
                          gmv=round(total_gmv, 2),
                          roas=round(total_gmv / total_spend, 2) if total_spend else None,
                          net_contribution=round(m["pre_ad_contribution"] / m["price"] * total_gmv - total_spend, 2)),
               campaigns=sorted(results, key=lambda x: x["grade"]))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not a.json:
        icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢", "INFO": "⚪"}
        print(f"\n盈亏线 ROAS {m['break_even_roas']} ｜ 整体 ROAS {out['total']['roas']}"
              f" ｜ 净贡献 {m['currency']} {out['total']['net_contribution']:,.2f}"
              f" ｜ 加购列 {'有' if has_atc else '无（只跑 CTR→CVR→ROAS）'}\n")
        for c in out["campaigns"]:
            print(f"{icon[c['grade']]} [{c['grade']}] {c['campaign']}  CTR {c['ctr']:.2%}"
                  f"  CVR {c['cvr']:.2%}  ROAS {c['roas']}")
            for x in c["actions"]:
                print(f"     · {x}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
