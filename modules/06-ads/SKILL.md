---
name: tiktok-ads
description: >-
  TikTok Shop 广告诊断：广告前贡献 → 盈亏线 ROAS → 按 CTR/加购/转化/ROAS 顺序定位病因，给 P0/P1/P2 动作。当用户要「看 ROAS / 广告亏钱 / 预算怎么调」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 06 · 广告诊断

**决策层，不是机器人。** 漏斗前段不达标时不出出价建议；执行由人做。

## 输入

1. 广告导出 CSV（曝光/点击/花费/订单，有加购列更好）
2. 成本结构（成本 + 运费 + 费率）

## 命令

```bash
python3 scripts/ad_metrics.py calc --market us --price 39.99 --product-cost 12 --shipping 4 \
    --referral-pct 6 --payment-pct 2
python3 scripts/ad_metrics.py diagnose --market us --price 39.99 --product-cost 12 \
    --referral-pct 6 --payment-pct 2 --file 报表.csv
```

## 停止条件

- 佣金/支付费率必须当场填（按类目不同）
- 曝光 < 1000 → 数据不足，本轮不动
- 没有加购列 → 只跑 CTR→CVR→ROAS，不假装做过四段漏斗
- 前段不达标 → 脚本不给调价建议，别自己加

## 边界

不暂停广告（伤连续性）；不改后台预算与出价。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
