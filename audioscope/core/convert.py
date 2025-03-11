"""频率与幅度的单位换算：赫兹↔梅尔、线性幅度↔分贝。

梅尔刻度默认用 Slaney 公式（与 librosa 一致），也可切到 HTK 公式。
"""

from __future__ import annotations

import numpy as np

from .._typing import FloatArray

# Slaney 梅尔刻度的分段参数。
_F_SP = 200.0 / 3.0
_MIN_LOG_HZ = 1000.0
_MIN_LOG_MEL = _MIN_LOG_HZ / _F_SP
_LOGSTEP = float(np.log(6.4) / 27.0)


def hz_to_mel(frequencies: np.ndarray | float, *, htk: bool = False) -> FloatArray:
    """把频率（Hz）换算成梅尔刻度。"""
    f = np.asarray(frequencies, dtype=np.float64)
    if htk:
        return np.asarray(2595.0 * np.log10(1.0 + f / 700.0), dtype=np.float64)

    mels = f / _F_SP
    log_region = f >= _MIN_LOG_HZ
    with np.errstate(divide="ignore", invalid="ignore"):
        safe = np.where(f > 0.0, f, _MIN_LOG_HZ)
        log_vals = _MIN_LOG_MEL + np.log(safe / _MIN_LOG_HZ) / _LOGSTEP
    mels = np.where(log_region, log_vals, mels)
    return np.asarray(mels, dtype=np.float64)


def mel_to_hz(mels: np.ndarray | float, *, htk: bool = False) -> FloatArray:
    """梅尔刻度换算回频率（Hz），是 :func:`hz_to_mel` 的逆运算。"""
    m = np.asarray(mels, dtype=np.float64)
    if htk:
        return np.asarray(700.0 * (10.0 ** (m / 2595.0) - 1.0), dtype=np.float64)

    freqs = _F_SP * m
    log_region = m >= _MIN_LOG_MEL
    log_vals = _MIN_LOG_HZ * np.exp(_LOGSTEP * (m - _MIN_LOG_MEL))
    freqs = np.where(log_region, log_vals, freqs)
    return np.asarray(freqs, dtype=np.float64)


def power_to_db(
    power: np.ndarray,
    *,
    ref: float = 1.0,
    amin: float = 1e-10,
    top_db: float | None = 80.0,
) -> FloatArray:
    """功率谱转分贝：``10 * log10(power / ref)``，并做下限裁剪。"""
    if amin <= 0:
        raise ValueError("amin 必须为正")
    s = np.abs(np.asarray(power, dtype=np.float64))
    ref_value = max(abs(ref), amin)
    log_spec = 10.0 * np.log10(np.maximum(amin, s))
    log_spec -= 10.0 * np.log10(np.maximum(amin, ref_value))
    if top_db is not None:
        if top_db < 0:
            raise ValueError("top_db 不能为负")
        log_spec = np.maximum(log_spec, float(log_spec.max()) - top_db)
    return np.asarray(log_spec, dtype=np.float64)


def amplitude_to_db(
    amplitude: np.ndarray,
    *,
    ref: float = 1.0,
    amin: float = 1e-5,
    top_db: float | None = 80.0,
) -> FloatArray:
    """幅度谱转分贝，等价于对功率谱 ``|S|**2`` 调用 :func:`power_to_db`。"""
    magnitude = np.abs(np.asarray(amplitude, dtype=np.float64))
    return power_to_db(magnitude**2, ref=ref**2, amin=amin**2, top_db=top_db)


def db_to_power(db: np.ndarray, *, ref: float = 1.0) -> FloatArray:
    """分贝转功率，是 :func:`power_to_db` 的逆运算。"""
    arr = np.asarray(db, dtype=np.float64)
    return np.asarray(ref * np.power(10.0, 0.1 * arr), dtype=np.float64)


def db_to_amplitude(db: np.ndarray, *, ref: float = 1.0) -> FloatArray:
    """分贝转线性幅度，是 :func:`amplitude_to_db` 的逆运算。"""
    arr = np.asarray(db, dtype=np.float64)
    return np.asarray(ref * np.power(10.0, 0.05 * arr), dtype=np.float64)


__all__ = [
    "amplitude_to_db",
    "db_to_amplitude",
    "db_to_power",
    "hz_to_mel",
    "mel_to_hz",
    "power_to_db",
]
