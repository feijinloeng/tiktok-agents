# TASK · 详情与卖点提炼

> 配合 `00_system.md` + `01_keyword_to_title.md` 的输出。

---

# INPUT

`market` / `category` / `product_name` / `spec_table` / `usage_scope[]` /
`core_selling_point`（02 产出，**不得改写**）/ `secondary_points[]` /
`package_content[]` / `warranty` / `notes_required` / `keyword_classified` /
（可选）`review_insights`（07 的差评归因）/ `competitor_weakness[]`

---

# 详情结构（TikTok）

```markdown
### 1 · 价值主张（1–2 句）
直接说解决什么问题，不写"欢迎光临"

### 2 · 核心卖点（3–5 条）
每条：卖点 — 量化支撑

### 3 · 使用场景（2–4 个）
必须落在 usage_scope 内；不写"让生活更美好"

### 4 · 参数表
值必须逐字符等于 spec_table（含单位）

### 5 · 包装清单
完整列出，并写明 **不含什么**（"Not included: ..."）—— 这是差评第一大来源

### 6 · 保修与售后
与 warranty 一致；不承诺做不到的事

### 7 · 注意事项（条件生成）
来源优先级：07 的误解型差评 → 产品天然限制 → 带 * 的测试条件
```

**前 3 行必须是价值主张 + 最强的一条卖点。** 手机上展开率很低，后面写得再好也要有人展开。

---

# 卖点真实化（强制改写）

| 输入（夸张） | 输出（可验证） |
|---|---|
| The strongest battery | 20000mAh, 45W output |
| Charges super fast | 0→60% in about 30 min* |
| Premium quality | ABS + PC shell, flame-retardant |
| Lasts forever | Over 500 charge cycles tested |
| Works with everything | USB-C and USB-A, supports iPhone/Samsung/tablets |

规则：**把形容词换成"名词 + 数字"**。带 `*` 的要在注意事项里补测试条件。

---

# 卖点分层（交给 04/05）

| 层级 | 卖点 | 支撑 | 用在哪 |
|---|---|---|---|
| 主卖点 | 直接引用 02 的 `core_selling_point` | | 主图 / 视频钩子 |
| 副卖点 | | | 详情 / 五点 / 视频中段 |
| 禁用卖点 | | | → forbidden_words |

---

# 参数一致性（必跑）

```bash
python3 scripts/spec_consistency.py --spec spec.csv --title "标题" --text 详情.txt
```

**只比数字不比单位是假通过** —— 脚本会连单位一起比（`45 W` vs `45 km` 会报错）。
`spec.csv` 里带逗号的小数要加引号：`"14,2 cm"`，否则 CSV 会切成两列。

---

# FINAL OUTPUT

```markdown
## 1. 详情正文
## 2. 卖点分层
## 3. 参数一致性（脚本输出）
## 4. 合规扫描
## 5. 交付下游字段
   secondary_points: []
   spec_table: {}
   forbidden_words: []
   visual_tone_hint: ""
   usage_scope_confirmed: []
```

# SELF-CHECK

- [ ] 前 3 行能独立说清这是什么、凭什么买
- [ ] 每个数值与 spec_table 逐字符一致（含单位）
- [ ] 包装清单写明"不含什么"
- [ ] 场景全部在 usage_scope 内
- [ ] 注意事项有明确来源，不是通用套话
