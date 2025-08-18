# 架构

audioscope 的目标是：**核心可离线、绘图后端可插拔、代码可读可教学**。
围绕这一目标，代码分成若干职责清晰的子包。

```
audioscope/
├── types.py          # Signal / Spectrogram 两个不可变数据容器
├── config.py         # 全局默认参数
├── exceptions.py     # 统一的异常层次
├── utils.py          # 合成信号、归一化、声道混合
├── core/             # 纯 NumPy/SciPy 的 DSP 内核
│   ├── framing.py    # 分帧、居中填充
│   ├── windows.py    # 窗函数
│   ├── stft.py       # STFT / iSTFT
│   ├── spectrogram.py# 幅度谱 / 功率谱
│   ├── mel.py        # 梅尔滤波器组与梅尔谱
│   ├── chroma.py     # 色度特征
│   ├── convert.py    # Hz↔Mel、幅度↔dB 换算
│   └── resample.py   # 重采样（SciPy 多相 + 线性兜底）
├── features/         # 时域与频域统计特征
├── io/               # WAV 读写与统一加载入口
├── viz/              # 可视化：ASCII、颜色表、matplotlib 后端
├── interactive/      # Browser 交互式视口
├── export/           # npz / csv / png 导出（自带 PNG 编码器）
└── cli.py            # 命令行入口
```

## 数据流

一条典型的分析链路：

```
文件/合成信号 ──load/tone──▶ Signal
      │
      ▼
   core.stft ──▶ 复数谱 ──abs──▶ Spectrogram(kind="power")
      │                              │
      ├── mel.melspectrogram ───────▶ Spectrogram(kind="mel")
      ├── chroma.chroma ────────────▶ Spectrogram(kind="chroma")
      │
      ▼
   viz.* / interactive.Browser / export.*
```

所有变换的产物都收敛到同一个 `Spectrogram` 容器，因此可视化与导出层
不需要关心它来自哪种变换，只按 `kind` 选择默认样式即可。

## 分层原则

1. **core / features 不导入 viz。** DSP 内核对绘图一无所知，保证纯数值路径
   可以在没有任何绘图库的环境里运行。
2. **viz 内部再分层。** `ascii_render` 与 `colormaps` 零第三方依赖；
   `plots` 才依赖 matplotlib，且为惰性导入。
3. **export 不依赖 matplotlib。** PNG 通过内置编码器写出，契合“离线可跑”。
