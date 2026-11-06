# 输入 · 广告诊断

---

```yaml
market: us
price: null                  # 售价 USD
product_cost: null           # 商品成本 USD
shipping: null               # 尾程运费 USD/单

# 费率：按类目查，脚本不猜
referral_pct: null
payment_pct: null
return_pct: 0
tax_pct: 0

target_roas: null            # 可选，不填就只对盈亏线
test_window_days: 7
```

## 广告导出 CSV

必需列（列名中英文都认）：

| 列 | 别名 |
|---|---|
| 曝光 | impressions / 曝光量 / 展示量 |
| 点击 | clicks / 点击量 |
| 花费 | spend / cost / 消耗 |
| 订单 | orders / conversions / 成交订单 |
| 广告名称 | campaign / name / 广告组 |
| 销售额 | gmv / revenue（可缺，缺了用 订单×售价 补） |
| **加购** | add_to_cart / atc（**可选**；没有就不做四段漏斗） |

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 曝光 300 就拿来看 | 数据不足，脚本会判 INFO 让你继续攒 |
| 没有加购列却要求"四段漏斗" | 脚本只跑 CTR→CVR→ROAS，不会假装 |
| 费率留空 | 直接 `[INPUT_MISSING]` |
