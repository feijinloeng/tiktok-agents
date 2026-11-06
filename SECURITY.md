# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.x | ✅ |
| < 1.0 | ❌ |

## Reporting a vulnerability

请使用 GitHub 的私密漏洞报告：仓库页 **Security → Advisories → Report a vulnerability**。

不要开公开 Issue，也不要在 Issue 里粘贴密钥、真实业务数据或可复现的敏感导出。

## 这个仓库的安全边界

- 仓库**不包含**任何 API Key、`.env`、账号凭据或真实业务数据；`.gitignore` 已忽略 `.env*`、`*.key`、`*.pem`、`secrets/`、`credentials/`
- 脚本只读本地文件，不发起网络请求，不接平台 API
- `prompts/` 会被喂给模型：如果你在其中发现可能诱导越权、泄露或绕过合规检查的内容，请按上面的方式报告
- 示例 CSV（`tests/fixtures/`）是合成数据，不含真实买家信息

## 使用者的责任

- 不要把真实导出、买家评论、订单数据提交到公开仓库
- 不要把佣金率、支付费率、供应商报价提交到公开仓库
- 发布 AI 生成或显著编辑的画面/配音时，遵守平台的原生标注要求
