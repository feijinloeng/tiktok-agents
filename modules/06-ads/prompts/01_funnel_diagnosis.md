# TASK · 漏斗诊断与动作清单

> 配合 `00_system.md`。**跑脚本，不要手算。**

---

# INPUT

`market` / `price` / `product_cost` / `shipping` / `referral_pct` / `payment_pct` /
`ad_report.csv`（列：广告名称/曝光/点击/花费/订单，可选加购、销售额）/
`test_window_days` / 可选 `existing_cover`（现用封面描述）/ `existing_title`

---

# STEP 1 · 跑脚本

```bash
python3 scripts/ad_metrics.py diagnose --market us --price 39.99 --product-cost 12 \
    --referral-pct 6 --payment-pct 2 --file ad.csv
```

输出：各组 CTR / CVR / 加购率（有列时）/ CPA / ROAS / 分级 / 动作。

脚本已按漏斗闸门判过，**不要覆盖它的结论**。你可以补充它看不到的语义信息（素材是什么、竞品在做什么）。

---

# STEP 2 · 逐组补充解读

对每个非 INFO 的组，补三件事：

1. **这一组投的是什么**（人群/素材/商品），脚本不知道
2. **病因指向哪个模块**：素材 → 04；详情/价格 → 03；评价 → 07
3. **本轮明确不动什么** —— 防止顺手改坏

---

# STEP 3 · 动作汇总

| 优先级 | 动作 | 涉及组 | 花费占比 | 复测周期 |
|---|---|---|---|---|
| P0 | | | | 7 天 |
| P1 | | | | 7 天 |

**一次只改一件事。** 指向同一病因的可以同批（例如 CTR 与首帧都属于素材），不同病因必须拆轮。

---

# STEP 4 · 复测

| 项 | 内容 |
|---|---|
| 时点 | 改动后 7 天 |
| 回收数据 | 同本轮字段 |
| 通过标准 | 被改动环节回到阈值以上，且 ROAS ≥ 盈亏线 |
| 未通过 | 回 STEP 2 重诊，**不加码同一动作** |
| 同步确认 | 期间有无大促/竞品动作/断货 |

---

# FINAL OUTPUT

```markdown
## 1. 整体概览
## 2. 逐组诊断（数据 / 判定 / 病因 / 动作 / 本轮不动）
## 3. 动作汇总
## 4. 复测方案
## 5. 建议合规扫描
## 6. 交付字段
   symptom_by_group: {}
   ctr_fail_groups: []      # → 04
   cvr_fail_groups: []      # → 07
   breakeven_roas: 0.0
   review_needed: true/false
## 7. 待确认
```

# SELF-CHECK

- [ ] 数字来自脚本
- [ ] 未在前段不达标时给调价
- [ ] 每组都有"不动的部分"
- [ ] 改动是否指向同一病因已说明
