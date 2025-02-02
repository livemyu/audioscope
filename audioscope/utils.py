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


def chirp(
    f0: float,
    f1: float,
    sr: int = 22050,
    duration: float = 1.0,
    *,
    amplitude: float = 0.5,
) -> FloatArray:
    """生成一段线性调频信号（从 ``f0`` 扫到 ``f1``）。"""
    if sr <= 0:
        raise InvalidParameterError("sr 必须为正整数")
    if duration <= 0:
        raise InvalidParameterError("duration 必须为正数")
    n = round(sr * duration)
    t = np.arange(n, dtype=np.float64) / float(sr)
    k = (f1 - f0) / duration
    phase = 2.0 * np.pi * (f0 * t + 0.5 * k * t * t)
    y = amplitude * np.sin(phase)
    return np.asarray(y, dtype=np.float64)


def to_mono(y: np.ndarray) -> FloatArray:
    """把多声道信号混合为单声道。

    约定多声道数组的形状为 ``(channels, n_samples)``；一维输入会原样返回。
    """
    arr = np.asarray(y, dtype=np.float64)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2:
        return np.asarray(arr.mean(axis=0), dtype=np.float64)
    raise InvalidParameterError("只支持一维或二维（channels, n）的输入")


def normalize(y: np.ndarray, *, peak: float = 1.0) -> FloatArray:
    """按峰值把信号线性缩放到 ``[-peak, peak]``。全零信号原样返回。"""
    arr = np.asarray(y, dtype=np.float64)
    max_abs = float(np.max(np.abs(arr))) if arr.size else 0.0
    if max_abs == 0.0:
        return arr
    return np.asarray(arr * (peak / max_abs), dtype=np.float64)


def frame_count(
    n_samples: int,
    frame_length: int,
    hop_length: int,
    *,
    center: bool = False,
    n_fft: int | None = None,
) -> int:
    """预测分帧后可以得到多少帧，便于提前分配数组。"""
    if frame_length <= 0 or hop_length <= 0:
        raise InvalidParameterError("frame_length 与 hop_length 必须为正")
    pad = (n_fft or frame_length) if center else 0
    padded = n_samples + pad
    if padded < frame_length:
        return 0
    return 1 + (padded - frame_length) // hop_length


__all__ = ["chirp", "frame_count", "normalize", "to_mono", "tone"]
