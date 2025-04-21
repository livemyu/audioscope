"""重采样。

优先使用 SciPy 的多相重采样（``scipy.signal.resample_poly``），在极少数
没有 SciPy 的场景下退回到线性插值，保证核心流程离线可用。
"""

from __future__ import annotations

from math import gcd

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError


def _linear_resample(y: np.ndarray, orig_sr: int, target_sr: int) -> FloatArray:
    """无 SciPy 时的兜底：简单线性插值。"""
    n_out = round(y.shape[0] * target_sr / orig_sr)
    if n_out <= 0:
        return np.zeros(0, dtype=np.float64)
    x_old = np.arange(y.shape[0], dtype=np.float64)
    x_new = np.linspace(0.0, y.shape[0] - 1, n_out)
    return np.asarray(np.interp(x_new, x_old, y), dtype=np.float64)


def resample(y: np.ndarray, orig_sr: int, target_sr: int) -> FloatArray:
    """把信号从 ``orig_sr`` 重采样到 ``target_sr``。"""
    if orig_sr <= 0 or target_sr <= 0:
        raise InvalidParameterError("采样率必须为正")
    arr = np.asarray(y, dtype=np.float64)
    if orig_sr == target_sr:
        return arr
    try:
        from scipy.signal import resample_poly
    except ImportError:
        return _linear_resample(arr, orig_sr, target_sr)
    divisor = gcd(orig_sr, target_sr)
    up = target_sr // divisor
    down = orig_sr // divisor
    return np.asarray(resample_poly(arr, up, down), dtype=np.float64)


__all__ = ["resample"]
