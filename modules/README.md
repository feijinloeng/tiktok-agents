# modules · 七个环节

每个环节一个目录，结构一致：

```
<NN>-<name>/
├── SKILL.md      # 入口：做什么、跑哪条命令、什么条件下停
├── prompts/      # 任务 Prompt（喂给模型）
├── scripts/      # 确定性算术层（能跑的先跑）
└── templates/    # 输入模板（复制后填）
```

| 目录 | 环节 |
|---|---|
| `01-market-research` | 类目分析：容量 / 集中度 / 价格带 / 配置 |
| `02-product-strategy` | 定位 / 配置 / 卖点 / 定价 / SKU |
| `03-listing` | 标题 / 详情 / 合规扫描 / 参数校验 |
| `04-images` | 商品图规划与出图 Prompt |
| `05-video` | 脚本 / 分镜 / 配音 / 字幕 |
| `06-ads` | 广告诊断 / 盈亏线 / 预算 |
| `07-reviews` | 评论归因 / 误解型识别 / 回流 |

共享层在仓库根：`core/`（规则）、`markets/`（平台数字）、`lib/`（配置读取）。

状态见 [../STATUS.md](../STATUS.md)，执行顺序见 [../runbook.md](../runbook.md)。
