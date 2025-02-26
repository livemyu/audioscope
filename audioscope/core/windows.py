"""常用窗函数。

统一提供 ``fftbins``（周期 / 对称）选项：做频谱分析时通常用周期窗
（``fftbins=True``），做滤波器设计时用对称窗。所有实现均为 NumPy，
不依赖 SciPy。
"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError

_ALIASES = {
    "hanning": "hann",
    "rectangular": "boxcar",
    "rect": "boxcar",
    "none": "boxcar",
    "triangular": "bartlett",
}


def get_window(window: str, n: int, *, fftbins: bool = True) -> FloatArray:
    """按名字生成长度为 ``n`` 的窗。

    支持 ``hann`` / ``hamming`` / ``blackman`` / ``bartlett`` / ``boxcar``
    （以及它们的常见别名）。未知名字会抛出 :class:`InvalidParameterError`。
    """
    if n <= 0:
        raise InvalidParameterError("窗长 n 必须为正")
    if n == 1:
        return np.ones(1, dtype=np.float64)

    key = _ALIASES.get(window.lower(), window.lower())
    if key == "boxcar":
        return np.ones(n, dtype=np.float64)

    # 周期窗除以 n，对称窗除以 n-1。
    m = n if fftbins else n - 1
    k = np.arange(n, dtype=np.float64)
    if key == "hann":
        w = 0.5 - 0.5 * np.cos(2.0 * np.pi * k / m)
    elif key == "hamming":
        w = 0.54 - 0.46 * np.cos(2.0 * np.pi * k / m)
    elif key == "blackman":
        w = 0.42 - 0.5 * np.cos(2.0 * np.pi * k / m) + 0.08 * np.cos(4.0 * np.pi * k / m)
    elif key == "bartlett":
        w = 1.0 - np.abs((k - m / 2.0) / (m / 2.0))
    else:
        raise InvalidParameterError(f"未知的窗函数：{window!r}")
    return np.asarray(w, dtype=np.float64)


__all__ = ["get_window"]
