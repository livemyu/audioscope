# audioscope

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
