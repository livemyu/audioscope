"""梅尔滤波器组与梅尔声谱图。

滤波器组采用三角滤波 + Slaney 面积归一化（``norm="slaney"``），与
librosa 的默认行为一致。
"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError
from ..types import Signal, Spectrogram
from .convert import hz_to_mel, mel_to_hz
from .spectrogram import _as_array_and_sr, spectrogram


def mel_frequencies(
    n_mels: int = 128,
    *,
    fmin: float = 0.0,
    fmax: float = 11025.0,
    htk: bool = False,
) -> FloatArray:
    """在梅尔刻度上均匀取点，再换算回赫兹，得到各梅尔带的中心频率。"""
    min_mel = float(hz_to_mel(np.asarray([fmin]), htk=htk)[0])
    max_mel = float(hz_to_mel(np.asarray([fmax]), htk=htk)[0])
    mels = np.linspace(min_mel, max_mel, n_mels)
    return np.asarray(mel_to_hz(mels, htk=htk), dtype=np.float64)
