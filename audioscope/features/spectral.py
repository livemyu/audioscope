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
