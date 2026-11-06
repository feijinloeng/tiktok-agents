# TASK · 关键词分类与标题

> 配合 `00_system.md`。

---

# INPUT

| 字段 | 说明 | 缺失 |
|---|---|---|
| `market` / `category` | — | 无法定语言与上限 |
| `mode` | `single` / `variant` / `iterate` | 无法定输出套数 |
| `product_name` | 产品通用名（市场语言） | 无法生成 |
| `keyword_top30_by_search[]` | 搜索量前 30 | 分类缺一维 |
| `keyword_top30_by_ratio[]` | 供需比前 30 | 同上 |
| `keyword_top30_by_growth[]` | 增长率前 30 | 同上 |
| `spec_table` | 参数表 | **数值词全缺** |
| `brand_authorization` | 已授权品牌，可为空 | 品牌词无法拦 |

`mode = variant` 需要 `variant_count`（2–3）；`mode = iterate` 需要 `existing_title` + `symptom`。

---

# STEP 1 · 关键词分七类

| 类别 | 定义 | 例（power bank） |
|---|---|---|
| 核心词 | 说明产品是什么 | power bank, portable charger |
| 参数词 | 功率/容量/尺寸 | 20000mAh, 45W |
| 人群词 | 适合谁 | for iPhone, for travel |
| 功能词 | 有什么功能 | fast charging, LED display |
| 场景词 | 用在哪 | camping, flight, road trip |
| 配件词 | 含什么 | with cable, 3 outputs |
| **风险词** | 禁用：他人品牌、与实际不符的参数 | Anker, 30000mAh（实际 20000） |

**风险词不得出现在买家可见文本里，但必须在内部清单里逐条列出**（下游 04/05 要用）。
这不是矛盾：一个管"发布内容"，一个管"交接清单"。

---

# STEP 2 · 组标题

```
核心产品词 + 核心参数 + 功能/场景 + 人群/补充
```

硬要求：

1. 字符数用 `title_lint.py` 实测并标注（例：`82/90`）
2. 主关键词落在最前
3. 参数只用 `spec_table` 的真实值与单位
4. 不做同义反复（`Power Bank Portable Charger Power Bank` ❌）
5. 不塞没有搜索量的词凑满 90
6. `single` → 3 个备选，方向不同；`variant` → 2–3 套实质差异；`iterate` → 只改症状指向的位置

---

# STEP 3 · 自检（跑脚本）

```bash
python3 scripts/title_lint.py "<标题>" --market us --keywords "power bank,20000mah"
python3 scripts/compliance_scan.py --market us --title "<标题>"
```

两项都退出码 0 才算通过。

---

# FINAL OUTPUT

```markdown
## 1. 关键词分类
### 1.1 高频词（出现在 ≥2 个榜单）
### 1.2 七类汇总
### 1.3 风险词清单（内部用）
## 2. 标题方案（按 mode）
## 3. 标题自检（脚本输出）
## 4. 合规扫描
## 5. 交付下游字段
   title_final: ""
   keyword_classified: {}
   forbidden_words: []
```

# SELF-CHECK

- [ ] 三榜合并去重，每个词归入七类之一
- [ ] 风险词完整列出，且未出现在标题里
- [ ] 字符数是实测值
- [ ] variant 模式两三套相似度 < 70%
