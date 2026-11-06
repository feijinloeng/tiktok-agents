# Runbook · 一条链路从 0 到上架

> 每一步写清：输入、产物、停止条件。不满足停止条件就停，不要往下硬推。

---

## 0. 一次性准备

```bash
python3 lib/market_config.py --check      # 市场配置是否填满
python3 tests/run_asserts.py                     # 脚本是否正常
```

`--check` 报缺项就去卖家中心查，填 `markets/<market>.json` 里对应的 `null`。**不要猜。**

---

## 1. 市场分析（01）

| 项 | 内容 |
|---|---|
| 输入 | 你自己导出的类目 CSV（含：标题/价格/月销量/卖家/品牌，最好带配置列）+ 市场代码 |
| 命令 | `python3 modules/01-market-research/scripts/category_parser.py 数据.csv --number-locale us -o data.json` |
| | `python3 modules/01-market-research/scripts/market_metrics.py data.json --top 10 --currency USD --config-fields 功率 --format md` |
| 产物 | 容量 / 集中度 / 价格带 / 配置交叉表 |
| **停止条件** | 样本 < 30 → 不出百分比结论；品牌或卖家列有值覆盖 < 50% → 集中度报"不可计算"，不许当垄断看 |

## 2. 产品策略（02）

| 项 | 内容 |
|---|---|
| 输入 | 01 的 `target_price_range` / `recommended_config` + 成本结构 + `decision_approved: true` |
| 命令 | `python3 modules/02-product-strategy/scripts/sku_pricing.py calc --market us --cost 12 --price 39.99 \\\n    --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2` |
| 产物 | 各 SKU 净利率 / 盈亏价 / 目标价 / 促销余量 / 盈亏线 ROAS |
| **停止条件** | 没填 `decision_approved` 不做规格化；**佣金率/支付费率必须当场填**（按类目不同，脚本不猜） |

## 3. Listing（03）

| 项 | 内容 |
|---|---|
| 输入 | 02 的 `core_selling_point` / `spec_table` / `usage_scope` |
| 命令 | 写完后跑：`python3 modules/03-listing/scripts/title_lint.py "标题" --market us` |
| | `python3 modules/03-listing/scripts/compliance_scan.py --market us --title "标题" --text 详情.txt` |
| | `python3 modules/03-listing/scripts/spec_consistency.py --spec spec.csv --title "标题" --text 详情.txt` |
| 产物 | 标题 2–3 个备选 + 详情 + `forbidden_words` |
| **停止条件** | 三个脚本任一非零退出 → 改到达标再走。参数单位不符也算失败 |

## 4/5. 图与视频（04 / 05）

| 项 | 内容 |
|---|---|
| 输入 | 03 的 `core_selling_point` / `secondary_points` / `package_content` |
| 命令 | `python3 modules/05-video/scripts/video_timing.py --script 配音稿.txt --target 15` |
| **停止条件** | 图：TikTok 无硬性规格（不限尺寸/背景，可带字），只需图内数字与 `spec_table` 一致；视频：只估算，超了就删词不加语速 |

## 6. 广告诊断（06）

| 项 | 内容 |
|---|---|
| 输入 | 广告导出 CSV（曝光/点击/花费/订单，有加购更好）+ 成本结构 |
| 命令 | `python3 modules/06-ads/scripts/ad_metrics.py diagnose --market us --price 39.99 --product-cost 12 --file 报表.csv` |
| **停止条件** | 曝光 < 1000 → 数据不足，不动；**漏斗前段不达标时脚本不会给出价建议**，别自己加 |

## 7. 评论回流（07）

| 项 | 内容 |
|---|---|
| 输入 | 评论导出 CSV（rating 必填，category 由模型逐条分类） |
| 命令 | `python3 modules/07-reviews/scripts/review_stats.py --file 评论.csv` |
| **停止条件** | 归因合计 ≠ 差评数 → 先修数据；评论 < 20 条 → 结论只作参考 |

---

## 闭环纪律

- 一次只改一个**病因**；指向同一病因的可以同批。
- 每轮写明"本轮明确不动的部分"。
- 复测周期：广告 7 天，文案 14–30 天。
- 未达标**不加码同一动作**，回诊断重新定位。

---

## 改造进度

见 **[STATUS.md](STATUS.md)**。7 个模块的脚本、SKILL、prompt、输入模板均已 TikTok 化。

唯一还需要你维护的：**每个类目的佣金率与支付费率**（脚本每次都会要求你填）。
