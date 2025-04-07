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


def mel_filterbank(
    sr: int,
    n_fft: int,
    *,
    n_mels: int = 128,
    fmin: float = 0.0,
    fmax: float | None = None,
    htk: bool = False,
    norm: str | None = "slaney",
) -> FloatArray:
    """构造形状为 ``(n_mels, 1 + n_fft // 2)`` 的梅尔滤波器组。"""
    if n_mels <= 0:
        raise InvalidParameterError("n_mels 必须为正")
    if fmax is None:
        fmax = sr / 2.0

    n_bins = 1 + n_fft // 2
    fftfreqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)
    mel_f = mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax, htk=htk)
    fdiff = np.diff(mel_f)
    ramps = np.subtract.outer(mel_f, fftfreqs)

    weights = np.zeros((n_mels, n_bins), dtype=np.float64)
    for i in range(n_mels):
        lower = -ramps[i] / fdiff[i]
        upper = ramps[i + 2] / fdiff[i + 1]
        weights[i] = np.maximum(0.0, np.minimum(lower, upper))

    if norm == "slaney":
        enorm = 2.0 / (mel_f[2 : n_mels + 2] - mel_f[:n_mels])
        weights *= enorm[:, np.newaxis]
    return np.asarray(weights, dtype=np.float64)
