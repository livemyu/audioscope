"""把一维信号切分为可能重叠的短帧。

分帧是所有短时分析（STFT、能量、过零率等）的第一步。这里用
``sliding_window_view`` 做到零拷贝的滑窗，再按跳距抽取，避免 Python
层的循环。
"""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from .._typing import FloatArray
from ..exceptions import InvalidParameterError

#: ``numpy.pad`` 支持的填充模式，抽成别名方便在各处复用。
PadMode = Literal[
    "constant",
    "edge",
    "linear_ramp",
    "maximum",
    "mean",
    "median",
    "minimum",
    "reflect",
    "symmetric",
    "wrap",
    "empty",
]


def pad_center(x: np.ndarray, size: int, *, mode: PadMode = "constant") -> FloatArray:
    """把一维数组居中补零（或按 ``mode``）到长度 ``size``。"""
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 1:
        raise InvalidParameterError("pad_center 只支持一维数组")
    n = arr.shape[0]
    if size < n:
        raise InvalidParameterError(f"目标长度 {size} 小于输入长度 {n}")
    left = (size - n) // 2
    right = size - n - left
    return np.asarray(np.pad(arr, (left, right), mode=mode), dtype=np.float64)
