# 端到端实跑记录

> 一个 `Power Bank 20000mAh 45W` 的 US 站点 SKU，走完七个环节。
> 以下所有输出都是**从本仓库真实跑出来的**，不是示意图。

[← 返回 README](../README.md) ｜ [架构 →](architecture.md)

---

## 0. 开工前

```bash
python3 lib/market_config.py --check
```

```
✅ id   USD  可以跑
✅ th   USD  可以跑
✅ uk   USD  可以跑
✅ us   USD  可以跑
✅ vn   USD  可以跑

全部市场就绪。
```

如果某个市场显示 `⚠️ 还差 1 项 · title.max_chars`，就去卖家中心查真实值填进 `markets/<m>.json`。**不填就停下来，不许用默认值顶替。**

```bash
python3 tests/run_asserts.py
```

```
[1] 数字解析：歧义不猜
  ✅ 样例 CSV 解析成功
  ✅ 50/50 行不丢
  ✅ 歧义数字 → 非零退出
  ✅ 歧义数字 → 提示 --number-locale
...
[10] 视频：只估算不设限（TikTok 不限时长/字幕/语速）
  ✅ 退出码 0
  ✅ 只估算不设限：返回总秒数
  ✅ 不判合格（无 pass 字段）

====================================================
✅ 全部通过
```

---

## 1. 市场分析

**输入**：从卖家中心导出的类目 CSV（本次用仓库里的 `tests/fixtures/parse-fixture.csv`）

```bash
python3 modules/01-market-research/scripts/category_parser.py \
    tests/fixtures/parse-fixture.csv --number-locale us -o /tmp/data.json
```

```
✅ 已写出 /tmp/data.json
   保留 6 / 6 行
   识别字段 8 个：brand, monthly_revenue, monthly_sales, price, rating, review_count, seller, title
```

`--number-locale` 是必须的：导出文件里同时存在 `1,299.00`（美式）和 `1.299,00`（欧式），含义相反。不指定口径时解析器**直接报错退出**，不猜。

```bash
python3 modules/01-market-research/scripts/market_metrics.py \
    /tmp/data.json --top 5 --currency USD --format md
```

节选：

```
## 1. 市场容量

| 指标 | 数值 |
|---|---|
| 样本商品数 | 6 |
| 月总销量 | 1,018.0 |
| 月总销售额 | USD 682,516.78 |
| 均价 | USD 1,180.79 |
| 中位价 | USD 1,434.43 |
| 价格范围 | USD 89.90 – USD 2,199.90 |
| 头部 5 名销售额占比 | 100.0% |

## 2. 品牌集中度

- 品牌数：**3**（有值覆盖 83%）
- CR3（销售额）：100.0% ｜ CR5：100.0% ｜ CR5 按销量：100.0%
- HHI：**4676.7**（0–10000，越高越集中）

> ⚠️ 主体数（3）≤ n（5），CR5 恒为 100%，无参考意义。
>    改看 HHI（4676.7）与 Top 榜的 revenue_share / item_share 对比。
> ⚠️ brand 列有值的样本 5/6（83%），未填行已排除，结论仅覆盖有值部分。

| # | 品牌 | 销售额 | 销售额占比 | 销量占比 | 商品数 |
|---|---|---|---|---|---|
| 1 | BrandB | USD 326,260.06 | 51.8% | 33.9% | 2 |
| 2 | BrandA | USD 279,623.72 | 44.4% | 23.4% | 2 |
| 3 | BrandC | USD 23,374.00 | 3.7% | 42.8% | 1 |
```

**注意脚本做了什么**：

- `CR5 = 100%` 但它**主动标注无参考意义** —— 主体数只有 3，分母不够。很多工具会把这个 100% 当成「高度垄断」直接汇报。
- 品牌列覆盖率 83% 也有显式警告。覆盖率低于 50% 时集中度直接报「不可计算」。
- 价格带波谷给的是「数学建议」，明确写「最终判断还要叠加成本和竞品强弱」。

**产出交给 02 的字段**：`target_price_range` / `recommended_config` / `brand_barrier` / `competitor_weakness`。

---

## 2. 产品策略与定价

**输入**：到岸成本 USD 12，目标售价 USD 39.99，US 站点该类目费率。

**关键点：费率不在配置文件里，必须当场填。** 不同类目、不同达人，费率能差一倍。

```bash
python3 modules/02-product-strategy/scripts/sku_pricing.py calc \
    --market us --cost 12 --price 39.99 \
    --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2
```

```
市场 us ｜ 佣金 6.0% + 支付 2.0% + 达人 15.0% + 退货 2.0% + 税 0.0% = 25.0% ｜ 广告 0.0%
净利率 45.0% ｜ 盈亏价 USD 16.00 ｜ 目标价 USD 26.67 ｜ 促销余量 USD 6.00 ｜ 盈亏线 ROAS 2.22
```

手算验证：

| 量 | 公式 | 结果 |
|---|---|---|
| 费率合计 | 6 + 2 + 15 + 2 | 25% |
| 广告前毛利 | 39.99 − 12 − 39.99×25% = 39.99 − 12 − 10.00 | **17.99** ✅ |
| 盈亏价 | 12 ÷ (1 − 0.25) | **16.00** ✅ |
| 盈亏线 ROAS | 39.99 ÷ 17.99 | **2.22** ✅ |

**少了费率会怎样**：

```
$ python3 modules/02-product-strategy/scripts/sku_pricing.py calc --market us --cost 5 --price 20
[INPUT_MISSING] 缺 --referral-pct / --payment-pct
                这两个费率每个类目都不同，脚本不猜。去卖家中心查到后填入。
```

这是本项目最关键的一个设计：**宁可拒绝执行，也不给一个看起来对的净利率。** 一个漏算达人佣金 15% 的定价表，会让整条品线亏钱。

**产出交给 03 的字段**：`core_selling_point`（一句话，必须能用 `spec_table` 里一个数字支撑）、`spec_table`、`target_price_range`、`promo_headroom`。

---

## 3. Listing 与合规

### 3.1 标题字符实测

```bash
python3 modules/03-listing/scripts/title_lint.py \
    "20000mAh Power Bank 45W USB-C 3 Ports LED Display" --market us
```

```
「49 / 90 字符」  总判定: ✅ 通过
  ⚠️  length               49/90 字符（利用率 54%），建议补到 80%+
  ✅ absolute             0 命中（查了 20 个词）
  ✅ price_promo_in_title 0 命中（查了 13 个词）
```

字符数是**实测**的，不是估的。上限 90 来自 `markets/us.json → title.max_chars`。

### 3.2 禁词拦截

```bash
python3 modules/03-listing/scripts/title_lint.py "The Best Power Bank Free Shipping" --market us
```

```
「33 / 90 字符」  总判定: ❌ 未通过
  ⚠️  length               33/90 字符（利用率 37%），建议补到 80%+
  ❌ absolute             命中：best、the best
  ❌ price_promo_in_title 命中：free shipping
```

退出码 = **1**。CI 里直接红。

完整正文扫描会给出**上下文片段和违规理由**：

```bash
python3 modules/03-listing/scripts/compliance_scan.py \
    --market us --title "The Best Power Bank, Free Shipping"
```

```
市场 us ｜ 扫描 34 字符 ｜ 总判定: ❌ 命中 3 处
  ❌ [absolute] 'best': …The Best Power Bank, Free Shipping …
      绝对化用语：无法举证，TikTok 与各国广告法均不接受
  ❌ [absolute] 'the best': …The Best Power Bank, Free Shipping …
      绝对化用语：无法举证，TikTok 与各国广告法均不接受
  ❌ [price_promo_in_title] 'free shipping': …The Best Power Bank, Free Shipping …
      促销信息不进标题：平台标题禁项，且容易与实时价格不一致
```

禁词来自 `core/compliance.json` 六组：`absolute` / `price_promo_in_title` / `health_claims` / `safety_overclaim` / `fake_proof` / `before_after`。**`title_lint.py` 和 `compliance_scan.py` 读同一份，不各抄一遍。**

干净文案会明确输出「无命中」—— 避免「真没命中」和「忘了扫」分不清。

### 3.3 参数溯源（含单位）

这是最容易出事的一步。`spec_table`：

```csv
参数,数值
Capacity,"20000 mAh"
Output,"45 W"
Ports,"3"
```

文案里把功率写成续航里程：

```bash
python3 modules/03-listing/scripts/spec_consistency.py \
    --spec spec.csv --text 文案.txt
```

```
参数 3 项 ｜ 文案中数字 2 处 ｜ 总判定: ❌ 存在参数漂移
  ❌ 45km（spec 里是 W）: …Output: 45 km range. Capacity: 20000 m…
  ⚠️ 以下参数在文案中从未出现（提醒补内容）：Ports（3）
```

退出码 = **1**。

三个方向的检查都在这里面：

| 方向 | 查什么 | 防止 |
|---|---|---|
| 正向 | 文案里每个数字是否能在 `spec_table` 找到 | 编造参数、笔误、口径不一 |
| 单位 | 数值对但单位不符（`45 W` → `45 km`） | 旧版会把这种情况判「通过」 |
| 反向 | `spec_table` 里的值是否一次都没出现 | 参数没讲，转化率静默流失 |

**三个脚本任一非零退出 = 不得交付。**

---

## 4 / 5. 商品图与短视频

### 04 商品图（无脚本）

TikTok 不限图片尺寸、不限背景、主图可带文字，所以本模块**没有校验脚本**，只产出：

- **8 个图位规划**：主图 / 场景 / 细节 / 规格 / 包装清单 / 对比 / 使用步骤 / 认证
- **七槽位出图 Prompt**：主体 / 环境 / 光线 / 机位 / 风格 / 文字层 / 负面 Prompt

唯一硬约束：**图内每个数字必须逐字符等于 `spec_table`**，用 03 的 `spec_consistency.py` 校验文字层。认证标志只能来自 `markets/<m>.json → certifications`，为空就不生成。

### 05 短视频

```bash
python3 modules/05-video/scripts/video_timing.py --script 配音稿.txt --target 15
```

```
语速 2.5 词/秒 ｜ 共 5 句 ｜ 总口播 16.8s

#  时长                   词    字  台词
1  0.0s → 3.2s          8   39  Hook: Never lose power on a trip again.
2  3.2s → 6.0s          7   41  20000 mAh holds three full phone charges.
3  6.0s → 9.2s          8   38  45 W refills your phone in 30 minutes.
4  9.2s → 13.2s        10   54  Three ports charge a phone, watch and earbud
5  13.2s → 16.8s        9   47  Carry it anywhere: 380 g, fits a jacket pock

口播 16.8s / 目标 15s，多 1.8s（删词或减镜头）
```

注意脚本的措辞：**「删词或减镜头」，不是「加快语速」。** 一行台词 = 一个分镜，超时只能减内容。

TikTok 不限视频时长、不限字幕字符、不限语速，所以脚本**不返回 pass/fail**，只回答一个问题：「这段台词念出来多少秒」。这条也有专门断言（`[10] 不判合格（无 pass 字段）`）。

---

## 6. 广告诊断

**先算成本侧**：

```bash
python3 modules/06-ads/scripts/ad_metrics.py calc \
    --market us --price 39.99 --product-cost 12 --shipping 4 \
    --referral-pct 6 --payment-pct 2
```

```
us ｜ 佣金 6.0% + 支付 2.0% ｜ 广告前贡献 USD 20.79 ｜ 盈亏线 ROAS 1.92（ACoS 52.0%）
```

**再读报表**：

```bash
python3 modules/06-ads/scripts/ad_metrics.py diagnose \
    --market us --price 39.99 --product-cost 12 --shipping 4 \
    --referral-pct 6 --payment-pct 2 --file 报表.csv
```

```
盈亏线 ROAS 1.92 ｜ 整体 ROAS 0.41 ｜ 净贡献 USD -75.61 ｜ 加购列 无（只跑 CTR→CVR→ROAS）

🔴 [P0] PowerBank-Broad-US  CTR 0.70%  CVR 1.19%  ROAS 0.41
     · CTR 0.70% < 1% —— 回流 04 换首帧/主图（这是素材问题，不是出价问题）
     · 本轮不动出价与预算：前段不达标时不调出价（调了只是换个方式烧钱）
```

**这是整套工具最有价值的一条纪律。**

CTR 只有 0.70%（及格线 1%），说明**点击这一环断了**。此时调出价完全没用 —— 出价影响的是曝光成本和竞价位次，救不了「没人想点」。

所以脚本：

- 只输出**素材层动作**（回流 04 换首帧 / 主图）
- **不输出任何出价或预算建议**
- 明确写「加购列 无（只跑 CTR→CVR→ROAS）」—— 没有加购数据就不会假装做了四段漏斗

这条有专门断言守着：

```
[8] 广告：前段不达标不许调出价
  ✅ 低 CTR 时给出回流素材
  ✅ 低 CTR 时不出价调整指令
```

---

## 7. 评论回流

**输入**：评论导出 CSV。`rating` 必填，差评行的 `category` 由模型逐条打标，脚本只做聚合。

```bash
python3 modules/07-reviews/scripts/review_stats.py --file 评论.csv
```

```
# 评论统计报告（确定性聚合）

## 1. 总体分布

- 评论总数：**10**
- 好评（4–5★）：**3**（30.0%）
- 中评（3★）：**1**（10.0%）
- 差评（1–2★）：**6**（60.0%）
- 带图评论：2（20.0%）

## 2. 差评归因

| 类别 | 条数 | 占差评比 | 可修复 |
|---|---|---|---|
| missing_accessory | 2 | 33.3% | ✅ |
| spec_mismatch | 1 | 16.7% | ✅ |
| misunderstanding | 1 | 16.7% | ✅ |
| usage_difficulty | 1 | 16.7% | ✅ |
| shipping_delay | 1 | 16.7% | ❌ |
| **合计** | **6** | 100.0% | **5 条可修 = 83.3%** |

> 可修复口径（--fixable 指定）：missing_accessory、misunderstanding、spec_mismatch、usage_difficulty。
> 可修复 = 改文案/补图/补说明即可解决，成本接近零；不可修复 = 物流/质量类，周期以周/月计。
```

八类归因（英文规范名，兼容旧中文别名）：

| 类别 | 含义 | 默认算可修 |
|---|---|---|
| `misunderstanding` | 误解型（买家以为产品有某功能） | ✅ |
| `spec_mismatch` | 参数不符合预期 | ✅ |
| `missing_accessory` | 配件缺失 | ✅ |
| `usage_difficulty` | 使用困难 | ✅ |
| `quality` | 产品质量问题 | ❌ |
| `shipping_delay` | 发货慢 | ❌ |
| `damaged_defective` | 破损 / 故障 / 退货 | ❌ |
| `after_sales` | 售后差 | ❌ |

**合计校验是硬闸门**：`归因合计 ≠ 差评数` 就说明有评论漏标，先修数据再下结论。零差评是合法输入，归因表为空不代表漏数据（有断言 `[9] 零差评不崩`）。

---

## 闭环：回到 03 / 04

差评归因直接指向修改动作：

| 归因 | 指向 | 改什么 |
|---|---|---|
| `misunderstanding` 占比高 | 03 | 文案把「不含什么」讲清，主图加对比图 |
| `spec_mismatch` 占比高 | 03 | 参数表与文案对齐，跑 `spec_consistency.py` |
| `missing_accessory` 占比高 | 04 | 包装清单图前置，详情写明 `Not included:` |
| `usage_difficulty` 占比高 | 04 / 03 | 加使用步骤图，文案补快速上手指引 |
| `shipping_delay` 占比高 | — | 文案里给真实时效预期，减少期待落差 |

**一次只改一个病因；每轮写明「本轮明确不动的部分」；广告复测 7 天，文案 14–30 天；未达标不加码同一动作，回诊断重新定位。**

---

## 复现这份记录

```bash
git clone https://github.com/feijinloeng/tiktok-agents.git
cd tiktok-agents

# 01
python3 modules/01-market-research/scripts/category_parser.py \
    tests/fixtures/parse-fixture.csv --number-locale us -o /tmp/data.json
python3 modules/01-market-research/scripts/market_metrics.py \
    /tmp/data.json --top 5 --currency USD --format md

# 02
python3 modules/02-product-strategy/scripts/sku_pricing.py calc \
    --market us --cost 12 --price 39.99 \
    --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2

# 03
python3 modules/03-listing/scripts/title_lint.py \
    "The Best Power Bank Free Shipping" --market us      # 预期 exit 1
python3 modules/03-listing/scripts/compliance_scan.py \
    --market us --title "The Best Power Bank, Free Shipping"   # 预期 exit 1

# 06
python3 modules/06-ads/scripts/ad_metrics.py calc \
    --market us --price 39.99 --product-cost 12 --shipping 4 \
    --referral-pct 6 --payment-pct 2
```

---

[← 返回 README](../README.md) ｜ [设计决策 →](design-decisions.md)
