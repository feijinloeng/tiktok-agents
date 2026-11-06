# Changelog

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] — 2026-11-06

### Added
- 双语 README（[中文](README.md) / [English](README.en.md)），含架构图、工程亮点、阅读路线
- `docs/architecture.md` 分层架构、数据流、字段级契约
- `docs/walkthrough.md` 一个 Power Bank SKU 走完七环节的真实跑例
- `docs/design-decisions.md` 13 条设计决策与各自防住的事故
- `docs/assets/banner.svg` 仓库封面图
- GitHub Actions CI：Python 3.9 / 3.11 / 3.13 三版本跑 10 组断言
- `CONTRIBUTING.md` / `SECURITY.md` / `CODE_OF_CONDUCT.md`
- Issue / Pull Request 模板
- `Makefile`（`make check` / `make test`）
- MIT License

### Changed
- README 重排：架构前移，增加「30 秒看懂」与「建议阅读路线」

## [0.3.0] — 2026-11-05

### Changed
- 更名 TikTok Agent，全仓去掉旧平台残留
- 04 商品图删除规格校验脚本（TikTok 不限尺寸/背景，主图可带字）
- 05 `video_timing.py` 改为纯估算不设限（TikTok 不限时长/字幕/语速）
- 07 八类归因改为英文规范名，保留旧中文别名兼容

## [0.2.0] — 2026-11-05

### Changed
- 目录重整：`core/` `markets/` `lib/` 提到根级，模块改短名

### Removed
- 旧平台残留模块与引用

## [0.1.0] — 2026-11-05

### Added
- 七环节链路：市场分析 → 产品策略 → Listing → 图 / 视频 → 广告诊断 → 评论回流
- 9 个确定性脚本（零第三方依赖）
- `markets/` 5 个市场配置（US / UK / TH / VN / ID）
- `core/compliance.json` 6 类禁词库、`core/language-units.md`、`core/handoff.md`
- `tests/run_asserts.py` 10 组回归断言
