"""时域特征：均方根能量、过零率、幅度包络。"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray
from ..core.framing import frame
from ..exceptions import InvalidParameterError


def _framed(y: np.ndarray, frame_length: int, hop_length: int, *, center: bool) -> FloatArray:
    arr = np.asarray(y, dtype=np.float64)
    if center:
        pad = frame_length // 2
        arr = np.pad(arr, pad, mode="constant")
    if arr.shape[0] < frame_length:
        arr = np.pad(arr, (0, frame_length - arr.shape[0]), mode="constant")
    return frame(arr, frame_length, hop_length)


def rms(
    y: np.ndarray,
    *,
    frame_length: int = 2048,
    hop_length: int = 512,
    center: bool = True,
) -> FloatArray:
    """逐帧计算均方根（RMS）能量。"""
    if frame_length <= 0 or hop_length <= 0:
        raise InvalidParameterError("frame_length 与 hop_length 必须为正")
    frames = _framed(y, frame_length, hop_length, center=center)
    values = np.sqrt(np.mean(frames**2, axis=1))
    return np.asarray(values, dtype=np.float64)
