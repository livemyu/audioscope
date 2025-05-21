"""统一的音频加载入口 :func:`load`。"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ..core.resample import resample
from ..types import Signal
from ..utils import to_mono
from .wav import read_wav


def load(
    path: str | Path,
    *,
    sr: int | None = None,
    mono: bool = True,
    offset: float = 0.0,
    duration: float | None = None,
) -> Signal:
    """加载音频文件为 :class:`~audioscope.types.Signal`。

    参数
    ----
    sr: 目标采样率；``None`` 表示保留文件原始采样率。
    mono: 是否混合为单声道。
    offset / duration: 从第 ``offset`` 秒开始，最多读取 ``duration`` 秒。
    """
    samples, file_sr = read_wav(path)
    if mono:
        samples = to_mono(samples)

    if offset or duration is not None:
        start = round(offset * file_sr)
        stop = None if duration is None else start + round(duration * file_sr)
        samples = samples[..., start:stop]

    if sr is not None and sr != file_sr:
        samples = resample(samples, file_sr, sr)
        file_sr = sr

    return Signal(np.asarray(samples, dtype=np.float64), file_sr)


__all__ = ["load"]
