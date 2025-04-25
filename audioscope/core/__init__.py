"""核心 DSP 内核：分帧、窗函数、STFT、谱、梅尔与色度。

这里的实现只依赖 NumPy（重采样会用到 SciPy），不涉及任何绘图，
可以在完全离线的环境下运行。
"""

from __future__ import annotations

from .chroma import chroma, chroma_filterbank
from .convert import (
    amplitude_to_db,
    db_to_amplitude,
    db_to_power,
    hz_to_mel,
    mel_to_hz,
    power_to_db,
)
from .framing import frame, pad_center
from .mel import mel_filterbank, mel_frequencies, melspectrogram
from .resample import resample
from .spectrogram import spectrogram
