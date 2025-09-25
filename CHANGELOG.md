# 更新日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)，
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [Unreleased]

## [0.3.0] - 2025-09

### 新增
- 交互式 `Browser`：在声谱图上滑动视口，支持前后翻页、按时间定位与缩放。
- 内置 PNG 编码器（仅依赖标准库 `zlib`），`export.save_image` 可离线导出彩色声谱图。
- 命令行新增 `--chirp` 合成扫频信号，`-o *.png` 直接导出图片。

### 变更
- `Spectrogram` 增加 `kind` 字段，绘图与导出会据此选择默认样式。
- 色度特征改为按最近音级硬分配，纯音的能量集中更明显（更利于教学演示）。

## [0.2.0] - 2025-06

### 新增
- 梅尔滤波器组与梅尔声谱图（Slaney 归一化）。
- 色度（chroma）特征与音名标签。
- 频谱统计特征：谱质心、带宽、滚降点、平坦度。
- 纯文本渲染：ASCII 热力图、sparkline、波形柱状图。

### 修复
- 修正短信号在 `center=True` 下 `reflect` 填充越界的问题。

## [0.1.0] - 2025-03

### 新增
- 核心 DSP：分帧、窗函数、STFT / iSTFT、声谱图。
- WAV 读写（基于标准库 `wave`）与统一的 `load` 入口。
- 时域特征：RMS、过零率、幅度包络。
- 首个命令行入口与基础测试、CI。

[Unreleased]: https://github.com/livemyu/audioscope/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/livemyu/audioscope/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/livemyu/audioscope/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/livemyu/audioscope/releases/tag/v0.1.0
