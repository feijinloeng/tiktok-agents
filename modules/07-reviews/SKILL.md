---
name: tiktok-reviews
description: >-
  TikTok Shop 评论分析：八类差评归因、可修复率、好评卖点频次×强度排行、误解型识别 → 修补建议。当用户要「分析差评 / 卖点提炼 / 为什么转化低」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 07 · 评论分析

分类是模型做的，计数是脚本做的。**归因合计必须等于差评数。**

## 输入

1. 评论导出 CSV（rating 必填，category 由模型逐条填）
2. `spec_table` + `package_content`（判断参数/配件类差评的依据）

## 命令

```bash
python3 scripts/review_stats.py --file 评论.csv
python3 scripts/review_stats.py --file 评论.csv --points 卖点.csv --format json
```

## 停止条件

- 归因合计 ≠ 差评数 → 先补分类再下结论
- 评论 < 20 条 → 只作参考，不出百分比结论
- 零差评是合法输入，归因表为空不代表漏数据

## 边界

不代回评论、不诱导删评、不组织举报、不判断评论真伪。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
