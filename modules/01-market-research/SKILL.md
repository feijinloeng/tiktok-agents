---
name: tiktok-market-research
description: >-
  TikTok Shop 类目分析：市场容量、品牌/卖家集中度、价格带波谷、配置交叉表。当用户要「看类目 / 值不值得进 / 价格带 / 竞争集中度」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 01 · 市场分析

数字由脚本算，判断由你解读。**不要自己重算指标。**

## 输入

1. 你自己导出的类目 CSV（标题/价格/月销量/卖家/品牌，配置列另开一列）
2. 市场代码：us / uk / th / vn / id

## 命令

```bash
python3 scripts/category_parser.py 数据.csv --number-locale us -o data.json
python3 scripts/market_metrics.py data.json --top 10 --currency USD \
    --config-fields 功率 --format md
```

## 停止条件

- 样本 < 30 → 只给原始值，不出百分比结论
- 品牌或卖家列有值覆盖 < 50% → 集中度报「不可计算」，不许当垄断看
- 解析报 `--number-locale` 错误 → 指定口径重跑，不要手工改数

## 边界

不采集数据（导出由你提供）；不替代选品决策。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
