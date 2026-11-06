---
name: tiktok-agent
description: >-
  TikTok Agent —— TikTok Shop（US / UK / TH / VN / ID）运营工具箱。覆盖选品分析、产品策略与定价、
  Listing 文案、商品图、短视频物料、广告诊断、评论回流七个环节。
  当用户要「看类目 / 定价 / 写标题 / 做详情 / 做主图 / 做视频 / 差评分析 / 广告诊断」时使用。
  NOT for 其他电商平台、账号操作、刷单刷评等平台禁止行为。
allowed-tools:
  - Bash(python *)
  - Read
  - Write
---

# TikTok Agent

只做 TikTok Shop。链路：

```
01 市场分析 → 02 产品策略 → 03 Listing → 04 图 / 05 视频 → 上架
                                              ↓
                              06 广告诊断 + 07 评论回流 → 改 03/04 → 复测
```

## 三条底线（任何模块都继承）

1. **数字不猜** —— 平台数字只写在 `markets/<market>.json`。读到 `null` 就停下报 `[UNVERIFIED]`，不许用默认值顶替。
2. **算的不交给模型** —— 定价、盈亏线、字符数、时长一律跑脚本；模型只解读。
3. **买家可见文本 = 目标市场语言**；内部备注用中文。所有数值必须溯源到 `spec_table`。

## 目录

```
SKILL.md          # 本文件：路由 + 三条底线
runbook.md        # 执行手册：每步输入 / 命令 / 停止条件
STATUS.md         # 每个环节的完成度
core/             # 规则：compliance.json（禁词）/ language-units.md / handoff.md
markets/          # 平台数字：us uk th vn id（唯一来源）
lib/              # market_config.py（读配置 + 校验）
modules/          # 01-market-research … 07-reviews
tests/            # run_asserts.py（10 组断言）
```

## 路由

| 用户要做的事 | 打开 |
|---|---|
| 看类目 / 市场容量 / 价格带 / 配置机会 | [modules/01-market-research/SKILL.md](modules/01-market-research/SKILL.md) |
| 定价 / SKU 结构 / 毛利 / 盈亏线 | [modules/02-product-strategy/SKILL.md](modules/02-product-strategy/SKILL.md) |
| 标题 / 详情 / 卖点 / 关键词 / 合规扫描 | [modules/03-listing/SKILL.md](modules/03-listing/SKILL.md) |
| 主图 / 场景图 / 细节图 / 出图 Prompt | [modules/04-images/SKILL.md](modules/04-images/SKILL.md) |
| 视频 / 分镜 / 配音 / 字幕 | [modules/05-video/SKILL.md](modules/05-video/SKILL.md) |
| 广告诊断 / ROAS / 出价 | [modules/06-ads/SKILL.md](modules/06-ads/SKILL.md) |
| 差评归因 / 卖点提炼 | [modules/07-reviews/SKILL.md](modules/07-reviews/SKILL.md) |

**执行顺序与停止条件看 [runbook.md](runbook.md)。** 模块状态看 [STATUS.md](STATUS.md)。

## 公共层（不要在模块里复制）

| 文件 | 作用 |
|---|---|
| `markets/<m>.json` | **唯一**平台数字来源（标题上限、图片规格、视频规格、费率） |
| `core/compliance.json` | **唯一**禁词来源（`title_lint.py` 与 `compliance_scan.py` 都读它） |
| `core/language-units.md` | 每市场语言与单位（US 用 inch/lb） |
| `core/handoff.md` | 模块间契约：`spec_table` 与 `core_selling_point` 的归属 |
| `lib/market_config.py` | 读配置 + 校验。`python3 lib/market_config.py --check` |

## 开工前

```bash
python3 lib/market_config.py --check     # 哪些市场还没填满
python3 tests/run_asserts.py                    # 脚本层的回归断言
```

## 边界

不接平台 API、不操作后台、不代改价、不代回评论；不提供刷单刷评等违规做法。
