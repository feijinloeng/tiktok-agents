# TASK · 出图 Prompt

> 产出可直接粘贴到生图工具的 Prompt。图内文字**不写进 Prompt**，后期叠字。

---

# INPUT

`market` / `image_plan` / `image_copy` / `visual_tone_confirmed` /
`prompt_language`（en 默认，中文模型用 zh）/ `has_product_photo`

---

# Prompt 七槽位

```
[SUBJECT]      主体：是什么、形态、颜色、材质
[MATERIAL]     表面处理：哑光/亮面/金属/织物、纹理
[COMPOSITION]  构图：角度、位置、占画比例、留白
[LIGHTING]     光位：主光方向、软硬、色温
[BACKGROUND]   背景：纯白/纯色/实景（TikTok 全都可以）
[STYLE]        风格：产品摄影 / 3D 渲染 / 生活场景
[PARAMETERS]   比例、尺寸
```

## 原则

| 原则 | 说明 |
|---|---|
| 越具体越可控 | `white background` → `seamless pure white background, RGB 255,255,255` |
| 不说"好看" | 用可执行的视觉描述 |
| **文字不进出图 Prompt** | 生图模型对英文/泰文/越南文变音符号渲染不稳，统一后期叠字 |
| 一 Prompt 一镜头 | 不要试图生成"组合图" |

## 产品身份锁定（最容易翻车的地方）

出图前先固定，并**原样带进每条 Prompt 的否定清单**：

| 字段 | 例 |
|---|---|
| `shape` | rounded rectangle, corner radius ~8mm |
| `color` | 机身 `#1C1C1E`，按键 `#3A3A3C`（用 hex，不用形容词） |
| `logo_text` | `HX-20000` |
| `must_not_change` | 屏幕数字、Logo 位置、接口数量 |

---

# 负面 Prompt 标准库

```
text, watermark, logo, signature, border, frame, label, badge,
low resolution, blurry, jpeg artifacts, oversaturated,
distorted proportions, extra objects, cluttered background,
cartoon, illustration, plastic look
```

按图位追加：

- 首图：`additional props, accessories not included in the package`
- 场景图（不防水产品）：`rain, water, swimming pool, wet surface`
- 人物出镜：`recognizable face, celebrity likeness`

---

# 图位与技术处理

| 图位 | 怎么出 |
|---|---|
| 首图 / 卖点图 / 场景图 / 细节图 | AI 出图 Prompt |
| 参数图 / 尺寸图 / 保修图 | **排版图**，输出「版式规格」而不是 Prompt |
| 包装图 | **必须实拍** —— AI 生成的清单与实物不符会直接引发"配件缺失"差评 |

---

# FINAL OUTPUT

```markdown
## 1. 出图 Prompt（逐图：七槽位 + 负面 + 技术参数）
## 2. 需排版/实拍的图位：版式规格
## 3. 出图流程建议（批量出 5 选 1、后期叠字、品控检查点）
## 4. 图片合规扫描
```

# SELF-CHECK

- [ ] 七槽位齐备
- [ ] 每张都有负面 Prompt
- [ ] 文字未写进出图 Prompt
- [ ] 包装图标注「必须实拍」
- [ ] 参数/尺寸/保修图输出的是版式规格
- [ ] `must_not_change` 出现在每条否定清单里
