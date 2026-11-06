# 输入 · 评论分析

---

```yaml
market: us
product_name: ""
analysis_scope: own          # own / competitor / both

# 判参数/配件类差评的依据，缺了就不许判这两类
spec_table: {}
package_content: []
usage_scope: []
warranty: ""
```

## 评论 CSV

| 列 | 必需 | 说明 |
|---|---|---|
| `rating` | ✅ | 1–5，也认 `评分` / `stars` |
| `text` | ✅ | 原文，**不要预翻译** |
| `category` | 差评需要 | 八类之一（脚本认英文规范名，也兼容旧中文） |
| `has_image` | 可选 | 用于评估评价质量 |
| `source` | 可选 | own / competitor_a |

八类规范名：

```
misunderstanding / spec_mismatch / missing_accessory / usage_difficulty
quality / shipping_delay / damaged_defective / after_sales
```

## 卖点 CSV（可选）

```csv
卖点,频次,强度
20000mAh 真实容量,18,强
45W 快充,12,强
3 个接口,7,中
```

强度写 `强/中/弱` 或 `strong/medium/weak`。

---

## 常见错误

| 错误 | 后果 |
|---|---|
| 只导差评，不导中评 | 3 星是最有信息量的一档 |
| 评论先翻译成中文再分析 | 丢失表达线索（"I thought" 是误解型的关键词） |
| 买家昵称没删 | 泄露隐私，违反 C5 |
| 缺 `package_content` 却判"配件缺失" | 无法区分真缺件和误解 |
