# audioscope

[![CI](https://github.com/livemyu/audioscope/actions/workflows/ci.yml/badge.svg)](https://github.com/livemyu/audioscope/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

轻量级 Python 音频信号处理与可视化工具包。提供波形、短时傅里叶变换（STFT）、梅尔声谱图（Mel-Spectrogram）、色度图（Chroma）等时频分析能力，支持终端纯文本渲染与零重型依赖离线导出。

## 主要特性

- **高效 DSP 内核**：核心算法基于 NumPy / SciPy 实现，STFT/iSTFT 支持向量化加窗重叠相加重建（WOLA），算法结果与行业标准保持一致。
- **离线与零重型依赖**：内置纯文本 ASCII 灰度渲染与自研二进制 PNG 编码器，无需安装 Matplotlib 或 Pillow 即可在无界面的 Linux/CI 环境中导出高清彩色声谱图。
- **终端交互浏览**：通过 `Browser` 视图对长音频流进行滑动窗口浏览、时间定位与缩放分析。
- **高工程规范**：全库具备 100% 严格类型标注（Strict Type Hints），内置完整单元测试与测试覆盖率校验。

## 安装

安装核心核心依赖（仅依赖 NumPy + SciPy）：

```bash
pip install audioscope
```

启用可选的 Matplotlib 绘图后端：

```bash
pip install "audioscope[plot]"
```

## 快速上手

### Python API

```python
import audioscope as aus

# 合成 440Hz 纯音信号（采样率 22050Hz，时长 1.0 秒）
sig = aus.Signal(aus.tone(440, sr=22050, duration=1.0), 22050)

# 计算梅尔声谱图
mel = aus.melspectrogram(sig, n_fft=1024, hop_length=256, n_mels=64)

# 终端输出 ASCII 热力图
print(aus.heatmap(aus.power_to_db(mel.data), width=80, height=16))
```

### 命令行工具 (CLI)

```bash
# 生成扫频信号并在终端查看梅尔声谱图
audioscope --chirp 200 4000 --duration 2 mel

# 导出声谱图为 PNG 图像文件（无 Matplotlib 依赖）
audioscope --tone 440 -o sweep.png spectrogram
```

## 模块架构一览

| 模块 | 说明 |
| --- | --- |
| `audioscope.core` | 分帧、窗函数、STFT/iSTFT 向量化重建、声谱图、梅尔谱、色度特征、单位换算、重采样 |
| `audioscope.features` | 逐帧 RMS 能量、过零率（ZCR）、幅度包络、谱质心、谱带宽、谱滚降点、谱平坦度 |
| `audioscope.viz` | ASCII 热力图渲染、Sparkline、波形渲染、颜色表映射、Matplotlib 惰性加载后端 |
| `audioscope.interactive` | `Browser` 长音频视口滑动与交互浏览 |
| `audioscope.export` | `.npz` / `.csv` 数据导出与内置二进制 PNG 图片编码导出 |

详细技术文档见 [`docs/`](./docs)：[架构说明](./docs/architecture.md) · [使用指南](./docs/usage.md) · [设计笔记](./docs/design-notes.md) · [API 参考](./docs/api-reference.md)。

## 开发与验证

本地搭建开发环境并执行类型校验与单元测试：

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy
uv run pytest
```

## 许可证

[MIT](./LICENSE) © Huang Yu
