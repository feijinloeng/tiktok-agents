# TASK · 图片规划与图内文案

> 配合 `00_system.md` + 02/03 的输出。

---

# INPUT

`market` / `category` / `mode`（standard / variant / iterate）/
`core_selling_point` / `secondary_points[]` / `spec_table` / `package_content[]` /
`warranty` / `usage_scope_confirmed[]` / `forbidden_words[]` / `visual_tone_hint` /
`certifications`（仅填实际持有的）

---

# STEP 1 · 图位规划（8 张，按需第 9 张）

| # | 图位 | 承载信息 | 画面 | 图内文案 | 字符 |
|---|---|---|---|---|---|
| 1 | 首图 | 一眼说清是什么 | | | |
| 2 | 卖点图 | core_selling_point | | | |
| 3 | 参数图 | spec_table 可视化（≤6 项） | | | |
| 4 | 场景图 | usage_scope[0] | | | |
| 5 | 细节图 | secondary_points 最有视觉冲击的一项 | | | |
| 6 | 尺寸图 | 具体数值 + 参照物 | | | |
| 7 | 包装图 | package_content，写明不含什么 | | | |
| 8 | 保修图 | warranty 时长与范围 | | | |

## 各图位要求

- **首图**：产品占画面主体，一眼可辨；可带 1 句主文案（≤4 词）
- **卖点图**：只讲 `core_selling_point`；画面必须直接支撑这句话（说 45W 就要出现功率标识或快充对比）
- **参数图**：≤6 个参数，多了手机上看不清
- **场景图**：必须来自 `usage_scope_confirmed`；**不防水的产品不出现水**
- **细节图**：微距，强调材质与做工
- **尺寸图**：数值 + 参照物（手、常见物体），不要只写数字
- **包装图**：完整平铺 + 明确"Not included: ..."，这是对冲误解型差评最有效的一张
- **保修图**：时长 + 范围 + 客服通道；不生成仿平台官方标识

---

# STEP 2 · 图内文案

三条硬规则：

1. **写信息，不写情绪** —— `20000mAh · 45W · 3 ports`，不写 `Amazing!`
2. **数值与 spec_table 完全一致**（含小数点与千分位写法）
3. **一句话只讲一件事**

字符上限：主文案 ≤ 20 字符/行、≤ 2 行；字号 ≥ 图高 4%。

---

# STEP 3 · 平台差异（mode = variant）

同一套图铺不同市场时，至少换：图内语言、单位（US 英制 / 其他公制）、主文案卖点方向。
**不要只换语言不换构图。**

`mode = iterate`：输入现有首图描述 + 症状（如 CTR 低于 1%），**只改首图**，其余不动。

---

# FINAL OUTPUT

```markdown
## 1. 图位规划
## 2. 图内文案明细（逐图：主文案/副文案/字符数/位置）
## 3. 平台/变体差异
## 4. 图片合规扫描
## 5. 交付 05 的字段
   visual_tone_confirmed: ""
   hero_visual: ""
   key_visual_moments: []
```

# SELF-CHECK

- [ ] 每张图一个信息，无重复功能
- [ ] 首图一眼可辨
- [ ] 卖点图与 core_selling_point 严格对应
- [ ] 包装图写了"不含什么"
- [ ] `certifications` 为空时没生成任何认证元素
