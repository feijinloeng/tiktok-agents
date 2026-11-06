# 模块间契约

> 两个字段归属定死，其余都是派生。旧版本这三处说法互相矛盾，导致上游定 200kg、下游做 150kg。

## 字段归属

| 字段 | 谁产出 | 谁消费 | 规则 |
|---|---|---|---|
| `spec_table` | **人工输入** | 全部模块 | **唯一数值来源**。任何输出里的数字必须能溯源到这里，逐字符一致 |
| `core_selling_point` | **02 产品策略** | 03 / 04 / 05 | **只有一个**。03 不得改写，只能把它拆成标题词/主图文案/视频钩子 |
| `secondary_points[]` | 02 | 03 / 04 / 05 | 3–5 条 |
| `forbidden_words[]` | 03（合规扫描产出） | 04 / 05 | 下游硬拦截，不许自行放宽 |
| `currency` | 市场配置 | 02 / 06 | 独立字段，不混进数值列 |

## 为什么这么定

- **`spec_table` 人工录入**：模型读参数会把 `45 W` 说成 `45 km`，这类错误在旧版实测出现过。
- **`core_selling_point` 归 02**：卖点是产品决策（配置 vs 竞品），不是文案决策。归 03 会让"写手决定卖什么"。
- 03 若发现卖点与 `spec_table` 冲突，**停下来报错**，不许自行改规格。

## 交接格式

```yaml
# 02 交 03/04/05
core_selling_point: ""        # 一句话，必须能用 spec_table 里的一个数字支撑
secondary_points: []          # 3–5 条
spec_table: {}                # 参数 → 值（带单位）
usage_scope_confirmed: []     # 允许表达的使用场景
forbidden_words: []

# 03 交 04/05
title_final: ""
visual_tone_hint: ""
package_content: []           # 含"不含什么"
```

## 跨模块一致性检查（上架前必跑）

```bash
python3 modules/03-listing/scripts/spec_consistency.py \
    --spec spec.csv --title "标题" --text 详情.txt
```

失败 = 参数漂移，不许上架。
