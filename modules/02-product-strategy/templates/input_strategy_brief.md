# 输入 · 产品策略与定价

> 前置：01 输出 + `decision_approved: true`。

---

```yaml
market: us
category: ""

# 阻塞项：没确认就别往下做
decision_approved: false

# 来自 01
market_analysis:
  target_price_range: []
  recommended_config: {}
  opportunity_config: {}
  brand_barrier: low
  seller_barrier: medium
  competitor_weakness: []

company_capabilities: {}
after_sales_capacity: ""     # 只换货 / 能维修 / 有配件
```

## 成本与费率（逐 SKU）

```yaml
skus:
  - role: 引流款
    config: ""
    landed_cost_usd: null    # 到岸成本
    warehousing_usd: null
  - role: 主推款
    config: ""
    landed_cost_usd: null
    warehousing_usd: null
  - role: 高配款
    config: ""
    landed_cost_usd: null
  - role: 套装款
    config: ""
    landed_cost_usd: null

# 费率：按你这一类目当场查，脚本不猜
fees:
  referral_pct: null         # 必填，类目不同
  payment_pct: null          # 必填
  affiliate_pct: 0           # 不用达人填 0；每个达人不同，能差一倍
  return_pct: 0              # 服装鞋类建议 5–10
  tax_pct: 0

target_margin_pct: 30
```

## 跑脚本（数字以它为准）

```bash
python3 scripts/sku_pricing.py matrix --market us --file skus.csv \
    --referral-pct <你的> --payment-pct <你的> --affiliate-pct 15 --return-pct 2
```

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 费率填"行业常见的 6%" | 你这一类目可能不是 6%，净利率全错 |
| 四个 SKU 用同一个成本 | 高配款净利率会算得虚高 |
| `decision_approved` 没改 true | 脚本和 prompt 都会拒绝执行 |
| 达人佣金填了但实际不做达人 | 净利率被低估 15 个点 |
