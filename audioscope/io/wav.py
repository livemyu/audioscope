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


def write_wav(path: str | Path, y: np.ndarray, sr: int, *, sampwidth: int = 2) -> None:
    """把浮点信号写成 16 位（默认）PCM WAV。"""
    if sampwidth != 2:
        raise UnsupportedFormatError("write_wav 目前只支持 16 位输出")
    if sr <= 0:
        raise InvalidParameterError("采样率必须为正")
    arr = np.asarray(y, dtype=np.float64)
    if arr.ndim == 1:
        n_channels = 1
        interleaved = arr
    elif arr.ndim == 2:
        n_channels = arr.shape[0]
        interleaved = arr.T.reshape(-1)
    else:
        raise InvalidParameterError("只支持一维或二维（channels, n）信号")

    clipped = np.clip(interleaved, -1.0, 1.0)
    pcm = np.round(clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(n_channels)
        wav.setsampwidth(2)
        wav.setframerate(int(sr))
        wav.writeframes(pcm.tobytes())


__all__ = ["read_wav", "write_wav"]
