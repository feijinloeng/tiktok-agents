---
name: tiktok-pricing
description: >-
  TikTok Shop 定价算术：到岸成本 + 平台佣金 + 支付费 + 达人佣金 → 净利率 / 盈亏价 / 目标价 / 促销余量 / 盈亏线 ROAS。当用户要「算毛利 / 定价 / 该发多少券 / SKU 结构」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 02 · 产品策略与定价

定价**决策**由人做，本模块只保证算得准。费率来自 `markets/<market>.json`。

## 输入

1. 到岸成本（每个 SKU 分别填）
2. 目标净利率（默认 30%）
3. 可选：达人佣金 %、退货损耗 %、广告 %、税 %

## 命令

```bash
python3 scripts/sku_pricing.py calc --market us --cost 12 --price 39.99 \
    --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2
python3 scripts/sku_pricing.py matrix --market us --file skus.csv
```

## 停止条件

- 没给 `--referral-pct` / `--payment-pct` → `[INPUT_MISSING]`。这两个费率**每个类目都不同**，脚本不猜
- 引流款净利率低于目标可以，但必须高于盈亏价
- 退货损耗默认 0%，做保守估算要显式加 `--return-pct 2`
- 达人佣金默认 0；不同达人能差一倍，按实际谈的填 `--affiliate-pct`

## 边界

不替人决定做不做这个产品；不改后台价格。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
