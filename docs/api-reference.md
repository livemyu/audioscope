# API 参考

本页列出稳定的公共接口。带 `*` 的参数为仅限关键字参数。

## 顶层命名空间 `audioscope`

### 数据类型

- `Signal(samples, sr)` — 单声道波形容器。属性：`n_samples`、`duration`；
  方法：`segment(start, end)`。
- `Spectrogram(data, sr, hop_length, n_fft, kind="power", freqs=None, bin_labels=None)`
  — 时频容器。属性：`n_bins`、`n_frames`、`shape`、`times`。

### 合成与工具

- `tone(freq, sr=22050, duration=1.0, *, amplitude=0.5, phase=0.0)`
- `chirp(f0, f1, sr=22050, duration=1.0, *, amplitude=0.5)`
- `normalize(y, *, peak=1.0)`

### 变换

- `stft(y, *, n_fft=2048, hop_length=None, win_length=None, window="hann", center=True, pad_mode="reflect")`
- `istft(spectrum, *, hop_length=None, win_length=None, n_fft=None, window="hann", center=True, length=None)`
- `spectrogram(y, sr=22050, *, n_fft=2048, hop_length=None, power=2.0, ...)`
- `melspectrogram(y, sr=22050, *, n_fft=2048, n_mels=128, fmin=0.0, fmax=None, htk=False, power=2.0, ...)`
- `chroma(y, sr=22050, *, n_fft=2048, n_chroma=12, ...)`

### 换算

- `hz_to_mel(f, *, htk=False)` / `mel_to_hz(m, *, htk=False)`
- `power_to_db(power, *, ref=1.0, amin=1e-10, top_db=80.0)`
- `amplitude_to_db(amp, ...)` / `db_to_amplitude(db, *, ref=1.0)`

### 特征

- `rms(y, *, frame_length=2048, hop_length=512, center=True)`
- `zero_crossing_rate(y, ...)` / `amplitude_envelope(y, ...)`
- `spectral_centroid(spec, freqs)`、`spectral_bandwidth(spec, freqs, *, p=2.0)`
- `spectral_rolloff(spec, freqs, *, roll_percent=0.85)`、`spectral_flatness(spec, *, amin=1e-10)`

### 可视化（离线）

- `heatmap(data, *, width=80, height=20, chars=...)`
- `sparkline(y, *, width=80)` / `waveform(y, *, width=80, height=9)`

### 交互

- `Browser(spec, *, window=100)` — 方法 `next` / `prev` / `seek` / `zoom` /
  `render`；类方法 `Browser.from_signal(signal, *, window=100, **kwargs)`。

## 子模块

### `audioscope.core`

`frame`、`pad_center`、`get_window`、`stft_frequencies`、`mel_filterbank`、
`mel_frequencies`、`chroma_filterbank`、`resample`。

### `audioscope.viz`

`plot_waveform`、`plot_spectrogram`、`plot_mel`、`plot_chroma`（需 matplotlib）；
`get_colormap`、`apply_colormap`、`available_colormaps`；
`available_backends`、`has_matplotlib`。

### `audioscope.export`

`save_image`、`save_npz`、`save_csv`、`write_png`。

### `audioscope.io`

`load`、`read_wav`、`write_wav`。

## 异常

- `AudioscopeError` — 基类
- `InvalidParameterError`（同时是 `ValueError`）
- `UnsupportedFormatError`
- `BackendNotAvailableError`（同时是 `RuntimeError`）
