# 项目状态

> 最后更新：2026-11-06 · 7 个环节全部可跑 · CI 通过
> [← 返回 README](README.md)

## 完成度矩阵

| 模块 | 脚本层 | SKILL.md | prompts | templates | 说明 |
|---|---|---|---|---|---|
| 01 市场分析 | ✅ | ✅ | ✅ | ✅ | `category_parser.py` 拒绝歧义数字；`market_metrics.py` 覆盖率不足报「不可计算」 |
| 02 产品策略 | ✅ | ✅ | ✅ | ✅ | `sku_pricing.py` 计入达人佣金；缺费率直接拒绝执行 |
| 03 Listing | ✅ | ✅ | ✅ | ✅ | `compliance_scan.py` + `title_lint.py` + `spec_consistency.py` 三道闸门 |
| 04 商品图 | — | ✅ | ✅ | ✅ | **无脚本**：TikTok 不限尺寸/背景，主图可带字，只产出规划与出图 Prompt |
| 05 视频 | ✅ | ✅ | ✅ | ✅ | `video_timing.py` 纯估算不设限 |
| 06 广告 | ✅ | ✅ | ✅ | ✅ | `ad_metrics.py` 前段不达标不出出价建议 |
| 07 评论 | ✅ | ✅ | ✅ | ✅ | `review_stats.py` 八类归因 + 合计校验 |

## 公共层

| 文件 | 状态 |
|---|---|
| `markets/{us,uk,th,vn,id}.json` | ✅ 就绪。标题上限 90；费率按类目当场填 |
| `lib/market_config.py` | ✅ 含 `--check` |
| `core/compliance.json` | ✅ 6 类禁词库（英文） |
| `core/language-units.md` | ✅ 5 市场语言 / 单位 / 当地坑 |
| `core/handoff.md` | ✅ 定死 `spec_table` / `core_selling_point` 归属 |
| `runbook.md` | ✅ 每步输入 / 命令 / 停止条件 |
| `tests/run_asserts.py` | ✅ 10 组断言 |
| `.github/workflows/ci.yml` | ✅ Python 3.9 / 3.11 / 3.13 |

## 已知边界

- 不接平台 API，不操作卖家后台，不代改价、不代回评论
- 类目导出 CSV 与评论 CSV 由使用者提供，仓库不采集数据
- 每个类目的佣金率、支付费率、达人佣金率必须每次填入，脚本不猜
- 04 商品图没有确定性脚本，因为 TikTok 没有硬性图片规格

## 路线图（候选，不承诺）

- [ ] 增加 SG / MY / PH 市场配置
- [ ] 01 → 02 的半自动串联：把 `target_price_range` 直接生成 02 的输入模板
- [ ] CSV 列名自动映射，减少手工改表头
- [ ] 可选的 Markdown lint 与链接检查 CI

[← 返回 README](README.md)
