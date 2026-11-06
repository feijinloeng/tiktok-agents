# TASK · 容量 / 集中度 / 价格带 / 配置 / 竞品

> 配合 `00_system.md` + `scripts/market_metrics.py` 的产出。
> **前置门槛**：`precheck_pass = false` 时不许执行。

---

# INPUT

| 字段 | 来源 | 缺失 |
|---|---|---|
| `metrics_report` | `scripts/market_metrics.py` | **阻塞** |
| `cost_structure` | 人工 | 价格带判断缺"有没有利润" |
| `company_capabilities` | 人工 | 配置判断缺"能不能做" |
| `competitors[]` | 人工 | 无竞品分析 |

> **不要重算指标。** 怀疑数字有问题 → 输出 `[METRIC_SUSPECT]` 并说明理由，回去改脚本参数。

---

# STEP 1 · 数据可信度

| 项 | 值 | 判定 |
|---|---|---|
| 样本量 | | 充足 ≥50 / 偏小 30–49 / 不足 <30 |
| 品牌/卖家列覆盖 | | <50% → 集中度不可用 |
| 配置抽取失败数 | | >30% → 标注 |

---

# STEP 2 · 市场容量

引用脚本的：月总销量 / 月总销售额 / 均价 / 中位价 / 隐含均价（GMV÷销量）/ 单商品均销。

```
均值与中位差距大 → 分布偏斜，看隐含均价
单期快照 → 明写"无法判断趋势"，需要 ≥2 期（间隔 30 天）
新品表现：listing_age_days 缺失或不准时直接写"数据不可靠"
```

---

# STEP 3 · 集中度

品牌与卖家各一张表：主体数 / CR3 / CR{n} / HHI / 有值覆盖。

**两个容易误读的点：**

- 主体数 ≤ n 时 CR-n 恒 100% → 只看 HHI 与 Top 榜
- 某卖家 `item_share` 远高于 `revenue_share` → 数量占位，不是效率优势，可超越

脚本报「不可计算」时**不要自己估**，直接写缺列。

---

# STEP 4 · 价格带（四项交叉）

| 条件 | 判断 | 依据 |
|---|---|---|
| ① 销量高 | | 该带销量占比 |
| ② 平均销量高 | | 该带均销 vs 整体 |
| ③ 有利润 | | 用 cost_structure 反算该价位毛利率 |
| ④ 竞品不强 | | 商品数与头部占比 |

四项同时满足才是目标带。**销量最高的带往往竞争最激烈。**

---

# STEP 5 · 配置组合

逐维度引用 config_matrix：商品数 / 数量占比 / 总销量 / 平均销量 / 脚本给的四维 flag。

**「数量少但均销高」必须先查是否被头部占据。** 是 → 陷阱，不是机会。

---

# STEP 6 · 竞品

2–3 个：价格 / 月销 / 评分数 / 上架时长 / 核心配置 / 主图卖点 / 差评高发类。

输出：竞品靠什么卖、我方机会点（竞品普遍差评但买家在意的点）、风险点。
深度评论归因交给 07。

---

# FINAL OUTPUT

```markdown
## 1. 数据可信度
## 2. 市场容量
## 3. 集中度
## 4. 价格带
## 5. 配置组合
## 6. 竞品
## 7. 分析合规扫描
## 8. 交付 02 的字段
   target_price_range: []
   recommended_config: {}
   opportunity_config: {}
   brand_barrier: low/medium/high
   seller_barrier: low/medium/high
   competitor_weakness: []
   benchmark_for_launch: {days_to_ramp, reviews_needed, ad_dependency}
```

# SELF-CHECK

- [ ] 所有数值来自 metrics_report
- [ ] 集中度不可计算时未硬给百分比
- [ ] 单期数据未推趋势
- [ ] 价格带做了四项交叉
- [ ] 机会配置已核对是否被头部占据
- [ ] 末尾附合规扫描 + 下游字段
