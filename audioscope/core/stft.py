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
