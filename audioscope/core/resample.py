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
