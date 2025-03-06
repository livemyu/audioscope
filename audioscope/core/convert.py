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
