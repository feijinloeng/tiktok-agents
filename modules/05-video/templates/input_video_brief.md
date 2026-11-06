# 输入 · 短视频

> TikTok **不限时长、不限字幕长度、不限语速**。所以这里只关心内容，不关心规格。

---

```yaml
market: us
mode: standard               # standard / variant
durations: [15]              # 你想做几个版本（不是平台要求）
product_name: ""

# 来自 02/03
core_selling_point: ""
secondary_points: []
spec_table: {}
forbidden_words: []
usage_scope_confirmed: []
title_final: ""              # CTA 要与标题一致

# 来自 04（可选）
visual_tone_confirmed: ""
hero_visual: ""

production_mode: mixed       # ai_generated / real_shoot / mixed
prompt_language: en
voice_style: ""              # 如 "friendly, 25-30s female"
```

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 15 秒版本塞 3 个卖点 | 一个都记不住 |
| 台词写书面语 | 念出来不像本地广告 |
| 数字不口语化（写 `20000mAh` 而不是 `twenty thousand milliamp hours`） | 配音会念错 |
| 真人镜头也给 AI Prompt | 肖像风险 |
