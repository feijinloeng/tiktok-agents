# 输入 · 商品图

> TikTok 对图片没有硬性规格：**不限尺寸、不限背景、主图可带字**。
> 所以这份模板只关心"讲什么"，不关心"合不合规"。

---

```yaml
market: us
category: ""
mode: standard               # standard / variant / iterate

# 来自 02/03
core_selling_point: ""
secondary_points: []
spec_table: {}
package_content: []
not_included: []
warranty: ""
usage_scope_confirmed: []
forbidden_words: []
visual_tone_hint: ""         # 如 "clean tech, cool tones"

certifications: []           # 只填实际持有的，空则不生成认证元素
has_product_photo: true      # 有实拍图吗
```

`mode = iterate` 额外填：

```yaml
existing_cover: ""           # 现用首图的描述
symptom: ""                  # 如 "CTR 0.8%，低于我的历史均值 1.5%"
```

---

## 单位与语言

- 图内文案：市场语言（US 用 inch/lb，其他用公制）
- 出图 Prompt：英文
- 一行文案 ≤ 20 字符

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 图内写 `20.000 mAh`，spec 是 `20000 mAh` | 数字写法不一致，买家会怀疑 |
| 包装图用 AI 生成 | 与实物不符 → 配件缺失差评 |
| `certifications` 空着却让 AI 画认证标志 | 违规且易被举报 |
