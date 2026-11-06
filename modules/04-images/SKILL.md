---
name: tiktok-images
description: >-
  TikTok Shop 商品图规划与出图 Prompt：8 个图位分工、图内文案、七槽位 Prompt、负面 Prompt。当用户要「做主图 / 场景图 / 细节图 / 出图提示词」时使用。
allowed-tools:
  - Read
metadata:
  version: 0.1.0
  platform: tiktok-shop
  markets: us, uk, th, vn, id
---

# 04 · 商品图

出图交给生图模型；本模块只给规划与 Prompt。**TikTok 不限尺寸、不限背景、主图可带字**，所以不做规格校验。

## 输入

1. 产品实拍图
2. `spec_table` + `package_content`（含「不含什么」）
3. 市场代码

## 命令

无脚本。TikTok 对图片没有硬性规格：**不限最小尺寸、不限背景、主图可以带文字**。
所以本模块只产出规划与出图 Prompt，不做机器校验。

## 停止条件

- 图内出现的每个数字必须逐字符等于 `spec_table`（用 03 的 `spec_consistency.py` 校验文案层）
- 认证标志只能来自 `certifications`，空则不生成
- 场景必须是产品真实能做到的（不防水的产品不出现水）

## 边界

不渲染、不修图、不剥离平台水印或 AI 标识。

---
共用层：[market_config.py](../../lib/market_config.py) ｜ [compliance.json](../../core/compliance.json) ｜
[语言与单位](../../core/language-units.md) ｜ [交接契约](../../core/handoff.md)
