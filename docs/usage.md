# 用法

## 安装

```bash
pip install audioscope          # 核心：numpy + scipy
pip install "audioscope[plot]"  # 追加 matplotlib 后端
```

## 载入或合成信号

```python
import audioscope as aus

sig = aus.load("piano.wav")                 # 从 WAV 文件
sig = aus.load("piano.wav", sr=16000)       # 载入时重采样
tone = aus.Signal(aus.tone(440.0, sr=22050, duration=1.0), 22050)  # 合成纯音
```

`Signal` 提供 `duration`、`n_samples`、`segment(start, end)` 等便捷属性。

## 时频变换

```python
S = aus.stft(sig.samples, n_fft=2048, hop_length=512)   # 复数谱 (1+n_fft//2, 帧)
spec = aus.spectrogram(sig, n_fft=2048, hop_length=512)  # 功率谱 Spectrogram
mel = aus.melspectrogram(sig, n_mels=128)                # 梅尔谱
chr = aus.chroma(sig)                                    # 色度 (12, 帧)
y = aus.istft(S, hop_length=512)                         # 逆变换重建波形
```

## 特征

```python
rms = aus.rms(sig.samples)
zcr = aus.zero_crossing_rate(sig.samples)

spec = aus.spectrogram(sig, power=1.0)
centroid = aus.spectral_centroid(spec.data, spec.freqs)
rolloff = aus.spectral_rolloff(spec.data, spec.freqs)
```

## 可视化（离线）

不装 matplotlib 也能在终端里看图：

```python
mel = aus.melspectrogram(sig, n_mels=64)
print(aus.heatmap(aus.power_to_db(mel.data), width=100, height=24))
print(aus.sparkline(sig.samples, width=100))
```

装了 matplotlib 之后可以画正式图：

```python
import matplotlib.pyplot as plt
from audioscope.viz import plot_mel

plot_mel(mel)
plt.show()
```
