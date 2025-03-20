"""短时傅里叶变换（STFT）及其逆变换。

约定输出频谱的形状为 ``(1 + n_fft // 2, n_frames)``，与 librosa 一致，
方便和现有生态互相印证。逆变换用加窗重叠相加（WOLA）重建波形。
"""

from __future__ import annotations

import numpy as np

from .._typing import ComplexArray, FloatArray
from ..exceptions import InvalidParameterError
from .framing import PadMode, frame, pad_center
from .windows import get_window


def _safe_pad_mode(mode: PadMode, n: int, pad: int) -> PadMode:
    """当信号太短、无法做 ``reflect`` 填充时，退回到零填充。"""
    if mode == "reflect" and pad >= n:
        return "constant"
    return mode


def stft(
    y: np.ndarray,
    *,
    n_fft: int = 2048,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: str = "hann",
    center: bool = True,
    pad_mode: PadMode = "reflect",
) -> ComplexArray:
    """计算信号的短时傅里叶变换。

    返回复数谱，形状 ``(1 + n_fft // 2, n_frames)``。
    """
    arr = np.asarray(y, dtype=np.float64)
    if arr.ndim != 1:
        raise InvalidParameterError("stft 只支持一维（单声道）信号")
    if n_fft <= 0:
        raise InvalidParameterError("n_fft 必须为正")
    if win_length is None:
        win_length = n_fft
    if hop_length is None:
        hop_length = win_length // 4
    if hop_length <= 0:
        raise InvalidParameterError("hop_length 必须为正")
    if win_length > n_fft:
        raise InvalidParameterError("win_length 不能大于 n_fft")

    win = get_window(window, win_length)
    if win_length < n_fft:
        win = pad_center(win, n_fft)

    if center:
        pad = n_fft // 2
        mode = _safe_pad_mode(pad_mode, arr.shape[0], pad)
        arr = np.pad(arr, pad, mode=mode)

    frames = frame(arr, n_fft, hop_length)
    windowed = frames * win[np.newaxis, :]
    spectrum = np.fft.rfft(windowed, n=n_fft, axis=1)
    return np.asarray(spectrum.T, dtype=np.complex128)


def istft(
    spectrum: np.ndarray,
    *,
    hop_length: int | None = None,
    win_length: int | None = None,
    n_fft: int | None = None,
    window: str = "hann",
    center: bool = True,
    length: int | None = None,
) -> FloatArray:
    """由 STFT 复数谱重建时域信号（加窗重叠相加）。"""
    s = np.asarray(spectrum, dtype=np.complex128)
    if s.ndim != 2:
        raise InvalidParameterError("istft 需要二维复数谱")
    n_bins, n_frames = s.shape
    if n_fft is None:
        n_fft = 2 * (n_bins - 1)
    if win_length is None:
        win_length = n_fft
    if hop_length is None:
        hop_length = win_length // 4

    win = get_window(window, win_length)
    if win_length < n_fft:
        win = pad_center(win, n_fft)

    frames = np.fft.irfft(s, n=n_fft, axis=0)
    expected = n_fft + hop_length * (n_frames - 1)
    # 显式标注为 FloatArray（秩无关），后续的切片重新赋值在各 numpy 版本下都成立。
    y: FloatArray = np.zeros(expected, dtype=np.float64)
    win_sum = np.zeros(expected, dtype=np.float64)
    win_sq = win * win
    for i in range(n_frames):
        start = i * hop_length
        y[start : start + n_fft] += frames[:, i] * win
        win_sum[start : start + n_fft] += win_sq

    nonzero = win_sum > 1e-8
    y[nonzero] /= win_sum[nonzero]

    if center and expected > n_fft:
        y = y[n_fft // 2 : expected - n_fft // 2]
    if length is not None:
        if length <= y.shape[0]:
            y = y[:length]
        else:
            y = np.pad(y, (0, length - y.shape[0]), mode="constant")
    return np.asarray(y, dtype=np.float64)


def stft_frequencies(sr: int, n_fft: int) -> FloatArray:
    """返回 STFT 每个频率 bin 的中心频率（Hz）。"""
    return np.asarray(np.fft.rfftfreq(n_fft, d=1.0 / sr), dtype=np.float64)


__all__ = ["istft", "stft", "stft_frequencies"]
