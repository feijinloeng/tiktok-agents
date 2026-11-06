---
name: tiktok-video
description: >-
  TikTok 短视频：脚本、分镜、AI 视频 Prompt、配音稿、字幕。含时长与字幕行长的确定性校验。当用户要「做视频 / 出分镜 / 配音字幕」时使用。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 05 · 短视频

一行台词 = 一个分镜。**时长和字幕交给脚本，不许心算。**

## 输入

1. `core_selling_point` + `secondary_points`
2. `usage_scope_confirmed`
3. 目标时长（15 / 30 / 其他）

## 命令

```bash
python3 scripts/video_timing.py --script 配音稿.txt --target 15
```

## 停止条件

- 口播超过「目标时长 × 0.8」→ 删词，不许加语速
- 口播不足一半 → 加卖点句，不要拉长留白
- 字幕超字符上限 → 拆行

## 边界

不渲染、不买版权素材；真人镜头只写拍摄指令，不出 AI 生成 Prompt。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
