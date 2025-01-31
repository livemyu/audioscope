"""通用工具函数：合成信号、声道混合、幅度归一化等。

这些函数不依赖任何绘图后端，纯 NumPy 实现，可离线运行。测试与
示例中经常用 :func:`tone` / :func:`chirp` 生成可复现的输入信号。
"""

from __future__ import annotations

import numpy as np

from ._typing import FloatArray
from .exceptions import InvalidParameterError


def tone(
    freq: float,
    sr: int = 22050,
    duration: float = 1.0,
    *,
    amplitude: float = 0.5,
    phase: float = 0.0,
) -> FloatArray:
    """生成一个单频正弦波（纯音）。

    参数
    ----
    freq: 频率，单位 Hz，必须为正。
    sr: 采样率，单位 Hz。
    duration: 时长，单位秒。
    amplitude: 峰值幅度，取值一般在 ``[0, 1]``。
    phase: 初始相位，单位弧度。
    """
    if freq <= 0:
        raise InvalidParameterError("freq 必须为正数")
    if sr <= 0:
        raise InvalidParameterError("sr 必须为正整数")
    if duration < 0:
        raise InvalidParameterError("duration 不能为负数")
    n = round(sr * duration)
    t = np.arange(n, dtype=np.float64) / float(sr)
    y = amplitude * np.sin(2.0 * np.pi * freq * t + phase)
    return np.asarray(y, dtype=np.float64)
