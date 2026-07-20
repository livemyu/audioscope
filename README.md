# audioscope
“本仓库主要作为内部/特定环境自动化部署与二次开发的基准模板（Base Template）。”

[![CI](https://github.com/livemyu/audioscope/actions/workflows/ci.yml/badge.svg)](https://github.com/livemyu/audioscope/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**音频可视化工具包**：波形 / 短时傅里叶谱（STFT）/ 梅尔谱 / 色度 / 声谱图等多种可视化，
支持交互式浏览与离线导出，面向音频分析与教学。

- 🧮 **NumPy / SciPy 内核**：DSP 全部基于成熟的科学计算库，结果可与 librosa 相互印证。
- 🎨 **绘图后端可选**：内置纯文本（ASCII）渲染与自带的极简 PNG 编码器，**没有 matplotlib 也能出图**。
- 📴 **离线可跑**：核心与导出流程零重型依赖，适合远程终端、CI 日志与课堂演示。
- 🔎 **交互式浏览**：`Browser` 在长音频上滑动视口，前后翻页、按时间定位、缩放。

## 安装

```bash
pip install audioscope          # 仅核心（numpy + scipy）
pip install "audioscope[plot]"  # 额外启用 matplotlib 后端
```

## 快速上手

```python
import audioscope as aus

# 合成一个 440Hz 的纯音（也可以用 aus.load("xxx.wav")）
sig = aus.Signal(aus.tone(440, sr=22050, duration=1.0), 22050)

# 梅尔声谱图
mel = aus.melspectrogram(sig, n_fft=1024, hop_length=256, n_mels=64)

# 不装任何绘图库，直接在终端里看
print(aus.heatmap(aus.power_to_db(mel.data), width=80, height=16))
```

命令行同样开箱即用（无需音频文件）：

```bash
audioscope --tone 440 --duration 2 mel
audioscope --chirp 200 4000 -o sweep.png spectrogram
```

## 功能一览

| 模块 | 内容 |
| --- | --- |
| `audioscope.core` | 分帧、窗函数、STFT/iSTFT、声谱、梅尔、色度、单位换算、重采样 |
| `audioscope.features` | RMS、过零率、包络、谱质心 / 带宽 / 滚降 / 平坦度 |
| `audioscope.viz` | ASCII 热力图 / sparkline / 波形、颜色表、matplotlib 后端 |
| `audioscope.interactive` | `Browser` 交互式视口 |
| `audioscope.export` | `.npz` / `.csv` / `.png`（内置 PNG 编码器）导出 |

更多内容见 [`docs/`](./docs)：[架构](./docs/architecture.md) ·
[用法](./docs/usage.md) · [设计笔记](./docs/design-notes.md) ·
[API 参考](./docs/api-reference.md)。

## 开发

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy
uv run pytest
```

## 许可

[MIT](./LICENSE) © Huang Yu
