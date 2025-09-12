# 贡献指南

感谢你愿意为 audioscope 出一份力！无论是修 bug、加功能，还是补文档、
写示例，都非常欢迎。

## 开发环境

本项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖：

```bash
git clone https://github.com/livemyu/audioscope
cd audioscope
uv sync --extra dev --extra plot
```

## 本地检查

提交前请确保下面几项都通过（它们与 CI 完全一致）：

```bash
uv run ruff check .            # 静态检查
uv run ruff format --check .   # 代码格式
uv run mypy                    # 类型检查
uv run pytest                  # 测试
```

也可以直接跑一键脚本：

```bash
./scripts/check.sh
```

推荐启用 pre-commit，让检查在每次提交时自动运行：

```bash
uv run pre-commit install
```

## 代码约定

- 面向用户的函数请写类型标注与简洁的中文 docstring。
- 核心 DSP 尽量只依赖 NumPy / SciPy，绘图相关放到 `viz` 且保持 matplotlib 可选。
- 新增或修改行为时补充对应测试；数值算法建议给出可解释的断言（例如峰值位置）。

## 提交信息

小步提交、一个提交只做一件事。信息可用中文或英文，推荐 `feat: ` / `fix: `
之类的前缀，但不强制。

## 分支与 PR

从 `main` 切出特性分支，PR 请填写模板并关联相关 issue。CI 全绿后即可合并。
