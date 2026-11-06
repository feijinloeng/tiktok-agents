# TASK · 脚本与分镜

> 配合 `00_system.md`。

---

# INPUT

`market` / `mode`（standard / variant）/ `durations`（如 [15] [30] [15,30]）/
`product_name` / `core_selling_point` / `secondary_points[]` / `spec_table` /
`forbidden_words[]` / `usage_scope_confirmed[]` / `title_final` /
`visual_tone_confirmed` / `hero_visual` / `production_mode`（ai_generated / real_shoot / mixed）

**时长不设限。** `durations` 是你想做几个版本，不是平台要求。

---

# STEP 1 · 钩子候选

| # | 类型 | 钩子文案 | 画面 | 选定 |
|---|---|---|---|---|
| A | 痛点直击 | | | |
| B | 结果前置 | | | |
| C | 反常识 | | | |

禁止：自我介绍 / Logo 开场 / "Antes de começar..." / 静态商品图。

---

# STEP 2 · 分镜表（核心产出）

| 镜号 | 时长 | 画面内容 | 运镜 | 字幕 | 音效/人声 |
|---|---|---|---|---|---|
| 1 | 0–3s | | | | |

硬要求：

- **画面要具体到能拍**：不写"展示产品"，写"手持充电宝，屏幕显示 87%，插入数据线"
- 每镜标运镜（哪怕写"固定"）
- 字幕必填，避开底部 15–20%
- 15s 版 4–6 镜，30s 版 7–10 镜

`production_mode` 差异：

| 模式 | 处理 |
|---|---|
| ai_generated | 避免复杂手部动作与真人互动 |
| real_shoot | 标道具与场地 |
| mixed | 逐镜标 `[AI]` / `[实拍]` |

**真人镜头只写拍摄指令**（机位/动作/景别/道具），不出 AI 生成 Prompt。

---

# STEP 3 · 时长核对（跑脚本）

```bash
python3 scripts/video_timing.py --script 配音稿.txt --target 15
```

脚本只估算，不判合格。超了就**删词或减镜头**，不靠提速硬塞。

---

# FINAL OUTPUT

```markdown
## 1. 钩子方案
## 2. 分镜表
## 3. 时长估算（脚本输出）
## 4. 配乐与音效需求（标注需可商用）
## 5. 视频合规扫描
## 6. 交付字段
   hook_final: ""
   shot_count: 0
   subtitle_lines: []
   cta_line: ""
```

# SELF-CHECK

- [ ] 每镜四列（画面/运镜/字幕/音效）无空缺
- [ ] 画面具体到能直接拍
- [ ] 真人镜头无 AI Prompt
- [ ] 字幕避开底部 UI
- [ ] 钩子与 CTA 和 title_final 一致
