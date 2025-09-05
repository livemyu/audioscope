# 示例

这些脚本都可离线运行，不需要音频文件（内部用合成信号），大多数也
不需要 matplotlib。

| 脚本 | 说明 | 额外依赖 |
| --- | --- | --- |
| [`01_quickstart.py`](./01_quickstart.py) | 合成纯音，打印信息与 ASCII 波形 | 无 |
| [`02_spectrogram_ascii.py`](./02_spectrogram_ascii.py) | 在终端里画扫频信号的声谱图 | 无 |
| [`03_mel_and_chroma.py`](./03_mel_and_chroma.py) | 和弦的梅尔谱与色度能量 | 无 |
| [`04_export_png.py`](./04_export_png.py) | 用内置 PNG 编码器导出彩色声谱图 | 无 |

运行方式：

```bash
python examples/01_quickstart.py
```

或安装后用命令行做同样的事：

```bash
audioscope --tone 440 --duration 1 waveform
audioscope --chirp 200 6000 --duration 3 spectrogram
```
