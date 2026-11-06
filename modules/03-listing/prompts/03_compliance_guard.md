# TASK · 合规扫描（可单独使用）

> 拿任意已有文案（自己写的 / 竞品参考 / 历史遗留）丢进来做复核。

---

# INPUT

| 字段 | 说明 |
|---|---|
| `scan_target` | 待扫描文本（标题 / 详情 / 图内文案 / 字幕） |
| `market` | us / uk / th / vn / id |
| `spec_table` | 参数基准（R3 用） |
| `brand_authorization` | 已授权品牌，可为空 |
| `usage_scope[]` | 允许的场景（R6 用） |
| `mode` | `in_flow`（要改写版）/ `audit_only`（只出报告） |

---

# 跑脚本

```bash
python3 scripts/compliance_scan.py --market us --title "<标题>" --text 详情.txt
```

脚本给**字面命中**。语义判断由你补：

- 脚本查不到的：暗示性表述（"like new"、"no one else can"）、前后对比暗示、场景越界
- 脚本会误报的：`off`/`free` 出现在非促销语境时，看上下文再定

---

# 逐条规则

```
R1 绝对化        o melhor→ 量化；best/#1/100%/perfect→ 改
R2 未授权品牌     → "compatible with X" 或删除
R3 参数虚标      数值+单位都要能对上 spec_table；对不上→记录 [PARAM_FIXED]
R4 促销词入标题  → 移到详情/图内 [MOVE_TO_DESCRIPTION]
R5 医疗/安全/收益 → 删除 [SENSITIVE_REMOVED]
R6 场景超范围    → 删除 [SCENE_DROPPED]
R7 伪造证明      认证/销量/评价/官方授权 → 删除 [FAKE_PROOF_REMOVED]
```

---

# 输出

```markdown
## 1. 扫描概览（每条规则的命中数，含 0）
## 2. 逐条明细（原文位置 / 片段 / 问题 / 改写后）
## 3. 改写后全文（mode = in_flow）
## 4. forbidden_words
## 5. 是否可发布（高危项全清才可发）
```

# 边界

1. **只报告，不臆断** —— 只标有文本证据的问题
2. **不评价审美**
3. **改写最小化** —— 只改违规部分，不借机重写整段
4. **改完要重扫** —— 替换品牌词可能引入新问题
5. **无命中也要输出完整结构**，第 5 段写"✅ 可发布"
