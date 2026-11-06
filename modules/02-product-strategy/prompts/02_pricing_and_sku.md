# TASK · 定价与 SKU 结构

> 配合 `00_system.md`。**数字一律跑脚本，不心算。**

---

# INPUT

| 字段 | 说明 | 缺失 |
|---|---|---|
| `decision_approved` | **阻塞** | 停止 |
| 逐 SKU `cost_structure` | 成本 + 物流 + 仓储 | **阻塞** |
| `referral_pct` / `payment_pct` | 按类目当场查 | **阻塞**（脚本会拒绝） |
| `affiliate_pct` | 达人佣金，不用则 0 | 影响净利率 |
| `target_price_range`（01） | 市场锚点 | 无锚点 |
| `final_config`（01 产品决策） | SKU 差异依据 | — |
| `target_margin_pct` | 目标净利率，默认 30 | — |

---

# STEP 1 · 跑脚本（禁止手算）

```bash
python3 scripts/sku_pricing.py matrix --market us --file skus.csv \
    --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2
```

输出即事实：`pre_ad_margin` / `net_rate` / `break_even_price` / `target_price` / `promo_headroom` / `break_even_roas`。

**不要自己套公式再写一遍** —— 你复算会和脚本对不上，那时以脚本为准。

---

# STEP 2 · 逐项判读

| 输出 | 怎么用 |
|---|---|
| `net_rate` vs `target_margin` | 低于目标：确认是否引流款刻意为之 |
| `break_even_price` | 售价底线；券后价跌破它就是真亏 |
| `target_price` | 目标毛利反算的定价参考 |
| `promo_headroom` | 发券不破目标的额度 |
| `price_ladder` | 相邻价差：太小互相蚕食，太大留空位给竞品 |

## 价格阶梯双向检查

- 引流 → 主推 差 40% 以上 → 买家停在引流款，主推拿不到成交
- 相邻只差 5% → 全选高配，引流款失去意义

## 引流款特殊处理

低于盈亏价时必须输出：

```
[引流款战略亏损]
每单亏 X ｜ 目的：拉点击/破零 ｜ 可承受量：每月最多 N 单或 ≤N%
退出条件：主推款月销达到 N 单后下架或提价
```

没有这个标注，不许给低于成本的定价。

---

# STEP 3 · 促销工具（TikTok 有券、闪购、Bundle）

| 工具 | 用在哪 | 校验 |
|---|---|---|
| 卖家券 | 主推/高配（不是引流款） | 券后价仍在盈亏价之上 |
| 限时闪购 | 清库存 / 测价格弹性 | 同上；写明结束时间 |
| Bundle | 提客单 | 组合成本增幅 < 售价增幅 |

券的作用是**缩小价格差距**，所以优先发在主推/高配，把实际成交价拉近引流款。

---

# STEP 4 · 交 06 的指标

| SKU | 定价 | 盈亏价 | 盈亏线 ROAS | 可否投流 |
|---|---|---|---|---|
| 主推 | | | | ✅ |
| 引流 | | | | ⚠️ 见战略亏损 |

若某 SKU 的盈亏线 ROAS 远高于你品类的常见区间，**说明广告模型不成立**，在定价阶段就放弃，不要等投放后才发现。

---

# FINAL OUTPUT

```markdown
## 1. 成本结构（逐 SKU）
## 2. 脚本输出（原样贴，不要改写数字）
## 3. 判读与结论
## 4. SKU 四角色结构 + 价格阶梯
## 5. 促销方案
## 6. 交 06 的盈亏线
## 7. 建议合规扫描
## 8. 交付字段
   sku_structure: []
   main_sku: ""
   breakeven_roas_by_sku: {}
   promo_plan: []
   strategic_loss_sku: null
```

# SELF-CHECK

- [ ] 数字来自脚本，未手算
- [ ] 佣金/支付/达人佣金是使用者给的值
- [ ] 券后价仍在盈亏价之上
- [ ] 引流款低于盈亏价时有战略亏损标注
- [ ] 价格阶梯做了双向检查
- [ ] 已输出各 SKU 盈亏线给 06
