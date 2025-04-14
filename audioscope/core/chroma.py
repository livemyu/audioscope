"""色度特征（chroma / 音级能量分布）。

这里用一个简化的实现：把每个 FFT 频率 bin 按最接近的十二平均律音级
硬分配到 12 个色度通道上，再对幅度谱做累加。对于纯音，能量会集中在
正确的音级上，非常适合教学演示。
"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError
from ..types import Signal, Spectrogram
from .spectrogram import _as_array_and_sr, spectrogram

#: C 大调音名，索引 0 对应 C。
NOTE_NAMES: tuple[str, ...] = (
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
)


def chroma_filterbank(
    sr: int,
    n_fft: int,
    *,
    n_chroma: int = 12,
    a440: float = 440.0,
) -> FloatArray:
    """构造把 FFT bin 映射到音级的滤波器组，形状 ``(n_chroma, 1 + n_fft // 2)``。"""
    if n_chroma <= 0:
        raise InvalidParameterError("n_chroma 必须为正")
    n_bins = 1 + n_fft // 2
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)
    fb = np.zeros((n_chroma, n_bins), dtype=np.float64)

    valid = freqs > 0.0
    bin_idx = np.nonzero(valid)[0]
    # A4 = 440Hz 对应 MIDI 69；MIDI 对 12 取余即音级，且 0 号恰为 C。
    midi = 69.0 + 12.0 * np.log2(freqs[valid] / a440)
    chroma_idx = np.round(midi).astype(np.int64) % n_chroma
    fb[chroma_idx, bin_idx] = 1.0
    return fb
