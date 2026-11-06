# TASK · 误解型识别与修补

> 本模块投入产出比最高的任务：**改一句话或补一张图，消除一类差评。**

---

# INPUT

`market` / `spec_table` / `package_content[]` / `usage_scope[]` / `warranty` /
`reviews[]` / `attribution`（01 的输出）/ `current_description` / `current_images`

---

# STEP 1 · 判定链

对每条误解型：

```
1. 买家投诉的具体是什么？
2. 该信息在哪个字段里（spec_table / package_content / usage_scope / warranty）？
3. 现有 Listing 里有没有说到？
   没提     → 缺失说明
   提了但埋着 → 说明不醒目
   提了很醒目 → 买家没看 → 换成图
4. 给修补动作
```

| 判定 | 修补 | 成本 |
|---|---|---|
| 缺失说明 | 新增一条 | 低 |
| 说明不醒目 | 前置到首屏/首条 | 中 |
| 买家没看 | 文字 → **图** | 中 |

**文字会被跳过，图不会。** 包装清单做成平铺图 + `Not included: ...`，比写一段话有效得多。

⚠️ 如果对照后发现问题是真的（描述与实物不符）→ 那**不是误解**，是 `spec_mismatch`，走修正描述或修产品。

---

# STEP 2 · 修补文案（可直接粘贴）

四条规则：

| 规则 | 正例 | 反例 |
|---|---|---|
| 正面陈述，不辩解 | `The charger does not include a cable.` | `Buyer didn't read` |
| 给边界，不说做不到 | `For light slopes and paved roads.` | `Cannot climb slopes.` |
| 前置到醒目位置 | 首条 | 段末 |
| 带具体数值 | `The cable is 30 cm.` | `The cable is short.` |

---

# STEP 3 · 参数红线

把反复被投诉的参数提炼成禁词候选：

| 被投诉参数 | 买家预期 | spec_table 实际 | 禁词候选 |
|---|---|---|---|
| 续航 | 60 km | 35 km | `60 km` `long range` |

**价值在防患**：这些词常出现在竞品关键词表里，照抄就等于主动制造虚标。

---

# STEP 4 · 可修复性

| 项 | 数量 | 占比 |
|---|---|---|
| 差评总数 | | |
| 可由改描述/改图修复 | | |
| 需改产品 | | |
| 需改物流 | | |

**把这个数叫"内容可干预占比"，不要叫"可修复率"** —— 真正能不能修好，要 14–30 天后复测才知道。

---

# FINAL OUTPUT

```markdown
## 1. 误解型判定（逐条）
## 2. 修补文案（可直接粘贴）
## 3. 需补的图（回流 04）
## 4. 参数红线 → forbidden_words_candidates
## 5. 内容可干预占比
## 6. 分析合规扫描
```

# SELF-CHECK

- [ ] 每条都对照了具体字段
- [ ] 三种判定已区分
- [ ] 与描述确实不符的已改判为 spec_mismatch
- [ ] 文案是市场语言且可直接粘贴
- [ ] 配件类已判断是否需补图
- [ ] 用的是"内容可干预占比"，不是"可修复率"
