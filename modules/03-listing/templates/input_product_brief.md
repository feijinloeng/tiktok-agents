# 输入 · Listing（模块间核心契约）

> `spec_table` 是**唯一数值来源**。下游 04/05 的所有数字都必须能溯源到这里。

---

```yaml
market: us
category: ""
product_name: ""             # 市场语言

# 来自 02（不得改写）
core_selling_point: ""       # 一句话，含至少一个 spec_table 里的数字
secondary_points: []         # 3–5 条

# 人工录入
spec_table:
  # 值带单位；带逗号的小数要加引号
  "Capacity": "20000 mAh"
  "Output": "45 W"
  "Ports": "3"
  "Weight": "380 g"
  "Dimensions": "14.2 x 6.8 x 2.8 cm"

package_content:
  - "1x power bank"
  - "1x USB-C cable (30 cm)"
  - "1x user manual"
# 务必写清不含什么（会在详情里生成 "Not included: ..."）
not_included: ["wall charger", "carrying case"]

warranty: "12 months limited warranty"

usage_scope:
  - "daily commute"
  - "travel and flights"
  - "camping (dry conditions)"

brand_authorization: []      # 已授权品牌，没有就空
certifications: []           # 只填实际持有的
```

## 关键词三榜（`01_keyword_to_title.md` 用）

```yaml
keyword_top30_by_search: []
keyword_top30_by_ratio: []
keyword_top30_by_growth: []
```

---

## 关键约束

| 约束 | 说明 |
|---|---|
| 一个数字一个单位 | `45 W` 对，`45W / 45` 混写会让校验失配 |
| 不写"约""左右" | 参数表里只放确定值 |
| `package_content` 必须全 | 配件缺失是差评第一大来源 |
| `usage_scope` 写真实能力 | 不防水就别写户外露营 |

---

## 常见错误

| 错误 | 后果 |
|---|---|
| CSV 里 `14,2 cm` 不加引号 | CSV 切成两列，校验把 14 当成独立参数 |
| spec 写 `45 W`、文案写 `45 km` | 旧版会判"通过"，现在会报单位不符 |
| 从竞品标题抄参数 | 竞品续航 60km、你 35km，抄了就是虚标 |
