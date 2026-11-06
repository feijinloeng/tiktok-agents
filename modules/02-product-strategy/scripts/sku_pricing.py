#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TikTok 定价算术 —— 只算，不猜，不定价（定价决策由人做）。

  python3 scripts/sku_pricing.py calc --market us --cost 12 --price 39.99 \
      --referral-pct 6 --payment-pct 2 --affiliate-pct 15
  python3 scripts/sku_pricing.py matrix --market uk --file examples/sample-skus.csv

费率来自 markets/<market>.json（唯一来源）。未核实的字段会直接报 [UNVERIFIED]。
公式：
  广告前毛利 = 售价 − 到岸成本 − 售价×(referral + payment + affiliate + 退货 + 税)
  净利率     = (广告前毛利 − 售价×广告%) ÷ 售价
  盈亏价     = 成本 ÷ (1 − 费率合计%)
  目标价     = 成本 ÷ (1 − 费率合计% − 广告% − 目标净利%)
"""
import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from market_config import MissingField, get, load  # noqa: E402


def build_fees(args) -> dict:
    """所有百分比都是"占售价"。

    佣金与支付费率**每个类目都不同**，达人也**每个达人不同**——所以一律当场填，
    不设默认值、不写进市场配置。缺了就报 INPUT_MISSING。"""
    missing = [n for n, v in (("--referral-pct 平台佣金率", args.referral_pct),
                              ("--payment-pct 支付费率", args.payment_pct)) if v is None]
    if missing:
        sys.exit("[INPUT_MISSING] 缺：" + "、".join(missing) +
                 "\n                这两个费率按类目不同，脚本不猜。去卖家中心查你这一类目的数值。")
    return dict(
        referral=float(args.referral_pct),
        payment=float(args.payment_pct),
        affiliate=float(args.affiliate_pct),
        returns=float(args.return_pct),
        tax=float(args.tax_pct),
        ad=float(args.ad_pct),
    )


def compute(price: float, cost: float, f: dict, target_margin: float) -> dict:
    pct = f["referral"] + f["payment"] + f["affiliate"] + f["returns"] + f["tax"]
    pre_ad = price - cost - price * pct / 100
    net = pre_ad - price * f["ad"] / 100
    denom = 1 - pct / 100
    tm = target_margin / 100
    denom_t = denom - f["ad"] / 100 - tm
    return dict(
        price=price, cost=cost,
        fee_pct_total=round(pct, 4),
        pre_ad_margin=round(pre_ad, 2),
        pre_ad_rate=round(pre_ad / price, 4) if price else 0,
        net_margin=round(net, 2),
        net_rate=round(net / price, 4) if price else 0,
        break_even_price=round(cost / denom, 2) if denom > 0 else None,
        target_price=round(cost / denom_t, 2) if denom_t > 0 else None,
        break_even_roas=round(price / pre_ad, 2) if pre_ad > 0 else None,
        promo_headroom=round((net / price - tm) * price, 2) if price and net / price > tm else 0,
    )


def _num(v, default=0.0):
    if v is None:
        return default
    s = str(v).strip().replace("R$", "").replace("$", "").replace("£", "").replace("฿", "").replace("%", "").replace(" ", "")
    if s in ("", "-", "—", "N/A", "nan"):
        return default
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = f"{head}.{tail}" if len(tail) <= 2 else head + tail
    try:
        return float(s)
    except ValueError:
        return default


def _fees_line(market, f):
    return (f"市场 {market} ｜ 佣金 {f['referral']}% + 支付 {f['payment']}% + 达人 {f['affiliate']}%"
            f" + 退货 {f['returns']}% + 税 {f['tax']}% = {sum([f['referral'], f['payment'], f['affiliate'], f['returns'], f['tax']])}%"
            f" ｜ 广告 {f['ad']}%")


def cmd_calc(args, cfg) -> int:
    f = build_fees(args)
    r = compute(args.price, args.cost, f, args.target_margin)
    out = dict(mode="calc", market=args.market, currency=cfg["currency"], **r,
               fees=f, target_margin=args.target_margin)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not args.json:
        print(f"\n{_fees_line(args.market, f)}")
        print(f"净利率 {r['net_rate']:.1%} ｜ 盈亏价 {cfg['currency']} {r['break_even_price']:,.2f}"
              f" ｜ 目标价 {cfg['currency']} {r['target_price']:,.2f}"
              f" ｜ 促销余量 {cfg['currency']} {r['promo_headroom']:,.2f}"
              f" ｜ 盈亏线 ROAS {r['break_even_roas']}")
        if f["returns"] == 0:
            print("  ⚠️  退货损耗按 0% 计 —— 想做保守估计加 --return-pct 2")
    return 0


def cmd_matrix(args, cfg) -> int:
    rows = list(csv.DictReader(open(args.file, encoding="utf-8-sig"))) if Path(args.file).exists() else []
    if not rows:
        sys.exit(f"[INPUT_MISSING] 读不到 {args.file} 或没有数据行")
    low = {h.strip().lower(): h for h in rows[0]}

    def col(*cands):
        for c in cands:
            if c in low:
                return low[c]
        return None

    c_name = col("角色", "名称", "sku", "role", "name") or list(rows[0])[0]
    c_price, c_cost = col("售价", "价格", "price"), col("到岸成本", "成本", "cost")
    if not c_price or not c_cost:
        sys.exit(f"[INPUT_MISSING] 认不出售价/成本列（表头：{list(rows[0])}）")

    f = build_fees(args)
    tm = args.target_margin
    out_rows, ladder = [], []
    for r in rows:
        price, cost = _num(r.get(c_price)), _num(r.get(c_cost))
        if price <= 0 or cost <= 0:
            out_rows.append(dict(sku=r.get(c_name), error="价格或成本非正数"))
            continue
        out_rows.append(dict(sku=r[c_name].strip(), **compute(price, cost, f, tm)))

    ok = sorted([r for r in out_rows if "price" in r], key=lambda x: x["price"])
    for a, b in zip(ok, ok[1:]):
        gap = b["price"] - a["price"]
        ladder.append(dict(frm=a["sku"], to=b["sku"], gap=round(gap, 2),
                           gap_pct=round(gap / a["price"], 4)))

    notes = []
    under = [r["sku"] for r in ok if r["net_rate"] < tm / 100]
    if under:
        notes.append(f"净利率低于目标 {tm:g}%：{'、'.join(under)}（引流款可刻意低于，但须高于盈亏价）")
    if len(ok) >= 2 and max(ok, key=lambda x: x["net_rate"])["price"] < ok[-1]["price"]:
        notes.append("最高净利率不是最高价 SKU —— 若不是刻意设计，检查高配的成本")

    out = dict(mode="matrix", market=args.market, currency=cfg["currency"],
               fees=f, target_margin=tm, skus=out_rows, price_ladder=ladder, notes=notes)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not args.json:
        print(f"\n{_fees_line(args.market, f)} ｜ 目标净利 {tm:g}%\n")
        print(f"{'SKU':<16}{'售价':>10}{'净利率':>9}{'盈亏价':>10}{'目标价':>10}{'促销余量':>10}")
        for r in out_rows:
            if "error" in r:
                print(f"{r['sku']:<16}  ⚠️ {r['error']}")
                continue
            mark = "✅" if r["net_rate"] >= tm / 100 else "⚠️"
            print(f"{r['sku']:<16}{r['price']:>10,.2f}{r['net_rate']:>9.1%}"
                  f"{r['break_even_price']:>10,.2f}{r['target_price']:>10,.2f}"
                  f"{r['promo_headroom']:>10,.2f} {mark}")
        for l in ladder:
            print(f"  阶梯 {l['frm']} → {l['to']}：差 {l['gap']:,.2f}（{l['gap_pct']:.0%}）")
        for n in notes:
            print(f"  ℹ️  {n}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="TikTok 定价算术（只算不定价）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, helptext in (("calc", "单 SKU"), ("matrix", "多 SKU 矩阵")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--market", required=True, help="us / uk / th / vn / id")
        p.add_argument("--target-margin", type=float, default=30, help="目标净利率 %%（默认 30）")
        p.add_argument("--referral-pct", type=float, help="平台佣金率 %%（按类目填，必填）")
        p.add_argument("--payment-pct", type=float, help="支付处理费率 %%（必填）")
        p.add_argument("--affiliate-pct", type=float, default=0, help="达人佣金 %%（不用达人填 0；每个达人不同）")
        p.add_argument("--return-pct", type=float, default=0, help="退货损耗 %%（默认 0，建议填 2）")
        p.add_argument("--tax-pct", type=float, default=0, help="综合税率 %%")
        p.add_argument("--ad-pct", type=float, default=0, help="广告费占售价 %%")
        p.add_argument("--json", action="store_true")
        if name == "calc":
            p.add_argument("--cost", type=float, required=True)
            p.add_argument("--price", type=float, required=True)
        else:
            p.add_argument("--file", required=True)
    args = ap.parse_args()
    try:
        cfg = load(args.market)
    except MissingField as e:
        sys.exit(str(e))
    try:
        sys.exit(cmd_calc(args, cfg) if args.cmd == "calc" else cmd_matrix(args, cfg))
    except MissingField as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
