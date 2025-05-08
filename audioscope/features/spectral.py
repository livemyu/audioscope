"""频谱统计特征：谱质心、带宽、滚降点、平坦度。

这些函数都接受一个幅度谱 ``S``（形状 ``(n_bins, n_frames)``）以及对应的
频率轴 ``freqs``，返回按帧排列的一维结果。
"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError


def _check(spec: np.ndarray, freqs: np.ndarray) -> tuple[FloatArray, FloatArray]:
    s = np.abs(np.asarray(spec, dtype=np.float64))
    f = np.asarray(freqs, dtype=np.float64)
    if s.ndim != 2:
        raise InvalidParameterError("频谱 S 必须是二维数组")
    if f.shape[0] != s.shape[0]:
        raise InvalidParameterError("freqs 的长度必须等于频率 bin 数")
    return s, f


def spectral_centroid(spec: np.ndarray, freqs: np.ndarray) -> FloatArray:
    """谱质心：每帧频谱能量的“重心”频率。"""
    s, f = _check(spec, freqs)
    total = s.sum(axis=0)
    total = np.where(total > 0.0, total, 1.0)
    centroid = (f[:, np.newaxis] * s).sum(axis=0) / total
    return np.asarray(centroid, dtype=np.float64)


def spectral_bandwidth(spec: np.ndarray, freqs: np.ndarray, *, p: float = 2.0) -> FloatArray:
    """谱带宽：频率相对谱质心的 ``p`` 阶展宽。"""
    s, f = _check(spec, freqs)
    centroid = spectral_centroid(s, f)
    total = s.sum(axis=0)
    total = np.where(total > 0.0, total, 1.0)
    deviation = np.abs(f[:, np.newaxis] - centroid[np.newaxis, :]) ** p
    bw = (deviation * s).sum(axis=0) / total
    return np.asarray(bw ** (1.0 / p), dtype=np.float64)


def spectral_rolloff(
    spec: np.ndarray, freqs: np.ndarray, *, roll_percent: float = 0.85
) -> FloatArray:
    """谱滚降点：累计能量达到 ``roll_percent`` 时对应的频率。"""
    if not 0.0 < roll_percent < 1.0:
        raise InvalidParameterError("roll_percent 必须落在 (0, 1) 区间")
    s, f = _check(spec, freqs)
    cumulative = np.cumsum(s, axis=0)
    threshold = roll_percent * cumulative[-1, :]
    reached = cumulative >= threshold[np.newaxis, :]
    idx = np.argmax(reached, axis=0)
    return np.asarray(f[idx], dtype=np.float64)
