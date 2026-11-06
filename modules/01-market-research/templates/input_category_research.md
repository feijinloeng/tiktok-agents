# 输入 · 类目调研

> 复制这份，填空后连同 `00_system.md` + `01_category_precheck.md` 一起提交。

---

## 1. 基础

```yaml
market: us                 # us / uk / th / vn / id
category: ""               # 如 power bank
platform: tiktok-shop
data_date: "2026-11-05"    # 数据快照日期，必填（单期数据无法判断趋势）
```

## 2. 数据（跑脚本产出）

```bash
python3 scripts/category_parser.py 你的导出.csv --number-locale us -o data.json
python3 scripts/market_metrics.py data.json --top 10 --currency USD \
    --config-fields 容量 --format md
```

把生成的 `.md` 报告原样贴到下面：

```markdown
<!-- metrics_report 粘贴处 -->
```

## 3. 公司能力（必填，缺=无法做前置判断）

```yaml
company_capabilities:
  has_stock: null            # true / false / null（不知道就写 null，不要写 false）
  supplier_stable: null
  cost_advantage: null
  after_sales_capacity: ""   # 能换货？能维修？有配件？
  warehouse_note: ""
```

> ⚠️ **不要预填 false**。`false` 是"公司确实做不到"，`null` 才是"还没确认"。
> 预填 false 会让前置判断直接判"不适合进入"，而你其实做得到。

## 4. 产品画像

```yaml
product_profile:
  volume_cm3: null
  weight_kg: null
  fragile: null
  has_battery: null
  needs_cert: []             # US: FCC/UL/CPSC；UK: UKCA；ID: SNI；TH: TISI
```

## 5. 成本（做利润承载力检验用）

```yaml
cost_structure:
  landed_cost: null          # 到岸成本 USD
  target_price: null
  expected_return_rate: null # 服装鞋类建议 5–10%
```

## 6. 竞品（可选）

```yaml
competitors:
  - name: ""
    price: null
    monthly_sales: null
    rating: null
    note: ""
```

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 成本写 0 | 利润承载力检验会判"必亏" |
| `has_stock: false` 但其实是没填 | 直接判"不建议进入" |
| 不填 `data_date` | 无法判断数据新旧 |
| 导出 CSV 的价格列混着 `1,234.56` 和 `1.234,56` | 解析会报 `--number-locale`，指定后重跑 |
