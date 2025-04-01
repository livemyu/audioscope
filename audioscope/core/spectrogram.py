"""从 STFT 计算幅度谱 / 功率谱，封装为 :class:`Spectrogram`。"""

from __future__ import annotations

import numpy as np

from ..types import Signal, Spectrogram
from .stft import stft, stft_frequencies


def _as_array_and_sr(y: Signal | np.ndarray, sr: int) -> tuple[np.ndarray, int]:
    """允许高层函数同时接受 :class:`Signal` 或 ``(array, sr)``。"""
    if isinstance(y, Signal):
        return y.samples, y.sr
    return np.asarray(y), sr


def spectrogram(
    y: Signal | np.ndarray,
    sr: int = 22050,
    *,
    n_fft: int = 2048,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: str = "hann",
    center: bool = True,
    power: float = 2.0,
) -> Spectrogram:
    """计算（功率或幅度）声谱图。

    ``power=1`` 得到幅度谱，``power=2`` 得到功率谱。
    """
    samples, sr = _as_array_and_sr(y, sr)
    hop = hop_length if hop_length is not None else n_fft // 4
    s = stft(
        samples,
        n_fft=n_fft,
        hop_length=hop,
        win_length=win_length,
        window=window,
        center=center,
    )
    magnitude = np.abs(s)
    data = magnitude if power == 1.0 else magnitude**power
    kind = "magnitude" if power == 1.0 else "power"
    return Spectrogram(
        data=np.asarray(data, dtype=np.float64),
        sr=sr,
        hop_length=hop,
        n_fft=n_fft,
        kind=kind,
        freqs=stft_frequencies(sr, n_fft),
    )


__all__ = ["spectrogram"]
