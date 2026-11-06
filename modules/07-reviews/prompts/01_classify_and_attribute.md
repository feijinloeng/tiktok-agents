# TASK · 分类、归因与卖点排序

> 配合 `00_system.md`。**分类是你的活，计数是脚本的活。**

---

# INPUT

`market` / `product_name` / `spec_table`（阻塞）/ `package_content[]`（阻塞）/
`usage_scope[]` / `warranty` / `reviews[]`（text / rating / has_image / source）/
`analysis_scope`（own / competitor / both）

---

# STEP 1 · 逐条打标（你的活）

对每条评论输出：`rating` / `category`（八类之一）/ `reason`（一句话）/ `evidence`（原文片段）。

- 好评不归入八类，改为提取卖点 + 情感强度（strong / medium / weak）
- 拿不准的归入最接近的一类，并在 `reason` 里写"待复核"

---

# STEP 2 · 跑脚本（计数）

```bash
python3 scripts/review_stats.py --file 评论.csv --points 卖点.csv
```

- 归因合计 ≠ 差评数 → **先补分类**，不要下结论
- 零差评是合法输入，归因表为空不代表漏数据

---

# STEP 3 · 好评分析（5 个维度）

为什么满意 / 哪些功能被反复提到 / 哪个卖点真正有效 / 物流售后感受 / 价格感知。

**最有价值的一条**：某个卖点被反复称赞，但 Listing 里没突出 → 立刻可用的优化点。

---

# STEP 4 · 差评细节

按八类逐类展开。三处必须对照：

| 类别 | 对照什么 | 三选一判定 |
|---|---|---|
| `spec_mismatch` | `spec_table` | 描述不清 / 描述错误 / 买家误读 |
| `missing_accessory` | `package_content` | 真缺件（质量事故）/ 误解（需平铺图标注） |
| `misunderstanding` | 现有描述 | 缺失说明 / 说明不醒目 / 买家没看 |

---

# STEP 5 · 卖点排序

综合分 = 提及频次 × 情感权重（strong 3 / medium 2 / weak 1）。

排序结果要和 Listing 对照：**前 2 名必须出现在首图**；前 3–5 名进详情。
排名高但 Listing 没提 → 明确的优化点。

---

# STEP 6 · 竞品对比（analysis_scope 含 competitor 时）

竞品靠什么卖 / 它的护城河 / 我方优劣势 / 空白机会。

**竞品的差评是我方的机会**，但只能用来改进自己的描述，不能用来举报或抹黑。

---

# FINAL OUTPUT

```markdown
## 1. 数据概览（脚本输出）
## 2. 好评分析
## 3. 差评归因（八类，含为 0 的）
## 4. 卖点排序
## 5. 竞品对比（条件输出）
## 6. 分析合规扫描
## 7. 交付字段
   selling_points_ranked: []
   forbidden_words_candidates: []
   review_patch_suggestions: []
   packaging_clarity_needed: true/false
   fixable_ratio: 0.0
```

# SELF-CHECK

- [ ] 每条都有 category + 原文引用
- [ ] 归因合计等于差评数
- [ ] 误解 / 参数 / 配件三类都对照了对应字段
- [ ] 卖点排序与 Listing 现状对照过
