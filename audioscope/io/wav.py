"""基于标准库 ``wave`` 的 WAV 读写。

读入后统一转成 ``float64`` 并归一化到 ``[-1, 1]``；多声道返回形状
``(channels, n_samples)``，单声道返回一维数组。
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

from .._typing import FloatArray
from ..exceptions import InvalidParameterError, UnsupportedFormatError

# 采样位宽 -> (numpy dtype, 归一化除数, 直流偏移)
_PCM_FORMATS = {
    1: (np.uint8, 128.0, 128.0),
    2: (np.int16, 32768.0, 0.0),
    4: (np.int32, 2147483648.0, 0.0),
}


def read_wav(path: str | Path) -> tuple[FloatArray, int]:
    """读取 WAV 文件，返回 ``(samples, sr)``。"""
    with wave.open(str(path), "rb") as wav:
        n_channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        sr = wav.getframerate()
        n_frames = wav.getnframes()
        raw = wav.readframes(n_frames)

    if sampwidth not in _PCM_FORMATS:
        raise UnsupportedFormatError(f"暂不支持 {sampwidth * 8} 位的 WAV 采样")

    dtype, scale, offset = _PCM_FORMATS[sampwidth]
    mono = (np.frombuffer(raw, dtype=dtype).astype(np.float64) - offset) / scale
    if n_channels > 1:
        return np.asarray(mono.reshape(-1, n_channels).T, dtype=np.float64), int(sr)
    return np.asarray(mono, dtype=np.float64), int(sr)
