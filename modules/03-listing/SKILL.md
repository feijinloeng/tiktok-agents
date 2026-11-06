---
name: tiktok-listing
description: >-
  TikTok Shop 标题与详情：字符实测、禁词拦截、参数溯源（数值+单位）。当用户要「写标题 / 写详情 / 查合规 / 查参数对不对」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 03 · Listing 内容与合规

守住下限：不超字、不踩禁词、参数不漂移。上限（点不点得动）要上架看真实 CTR。

## 输入

1. `spec_table`（参数 → 值，带单位）
2. `core_selling_point`（由 02 产出，不得改写）
3. 标题/详情草稿

## 命令

```bash
python3 scripts/title_lint.py "标题" --market us
python3 scripts/compliance_scan.py --market us --title "标题" --text 详情.txt
python3 scripts/spec_consistency.py --spec spec.csv --title "标题" --text 详情.txt
```

## 停止条件

- 三个脚本任一非零退出 → 改到达标才交付
- 单位不符（45 km 冒充 45 W）也算失败
- `spec_table` 里带逗号的小数要加引号，否则 CSV 会切碎

## 边界

不生成图片/视频；不做竞品抄袭。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
