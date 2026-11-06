# Contributing

> 这是一个公开的 Agent 工程实践项目，欢迎 Issue 与 PR。改动请尽量保持现有的分层与契约。

## 本地校验

```bash
make check     # 市场配置是否填满
make test      # 10 组回归断言
```

提交前这两条必须通过。

## 目录约定

```
modules/<NN>-<name>/
├── SKILL.md      # 入口：做什么、跑哪条命令、什么条件下停
├── prompts/      # 任务 Prompt（模型判断层）
├── scripts/      # 确定性算术（能算的必须先算）
└── templates/    # 输入模板（复制后填）
```

- **数字只放一处**：平台数字进 `markets/<market>.json`，禁词进 `core/compliance.json`，不要复制进 prompt 或脚本。
- **能算的不要交给模型**：字符数、费率、毛利、时长、占比一律写脚本，并配一条断言。
- **会算错的路径必须有断言**：新增脚本或修改公式时，在 `tests/run_asserts.py` 补一组。

## 加一个新市场

1. 复制 `markets/us.json` → `markets/<new>.json`，只填确认过的值，其余保持 `null`
2. 在 `core/language-units.md` 补一行语言 / 单位 / 当地坑
3. 跑 `python3 lib/market_config.py --check <new>`，应报缺项 —— 这是正确行为
4. 查到真实数字后填入，重跑 `--check` 变 ✅

不需要改任何脚本或 prompt。

## 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: add SG market config
fix: count affiliate commission in break-even price
docs: clarify spec_table ownership
test: cover zero-negative-review input
```

## 不接受

- 刷单、刷评、组织举报、诱导删评等平台禁止行为
- 把 API Key、`.env`、真实业务数据提交进仓库
- 为了「看起来完整」而伪造平台数字（`null` 必须保持 `null`，直到核实）

## 安全问题

见 [SECURITY.md](SECURITY.md)。
