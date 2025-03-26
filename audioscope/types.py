"""核心数据容器：:class:`Signal` 与 :class:`Spectrogram`。

两者都是不可变的 dataclass（``frozen=True``），持有 NumPy 数组以及
必要的元信息（采样率、跳距等）。因为字段里含有 ndarray，无法安全地
自动生成 ``__eq__``，所以这里显式关闭（``eq=False``）。
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ._typing import FloatArray
from .exceptions import InvalidParameterError


@dataclass(frozen=True, eq=False)
class Signal:
    """一段单声道时域波形。

    参数
    ----
    samples: 一维 ``float64`` 数组。
    sr: 采样率，单位 Hz。
    """

    samples: FloatArray
    sr: int

    def __post_init__(self) -> None:
        arr = np.asarray(self.samples, dtype=np.float64)
        if arr.ndim != 1:
            raise InvalidParameterError("Signal 只接受一维（单声道）样本")
        if self.sr <= 0:
            raise InvalidParameterError("采样率 sr 必须为正整数")
        object.__setattr__(self, "samples", arr)

    @property
    def n_samples(self) -> int:
        """样本点数。"""
        return int(self.samples.shape[0])

    @property
    def duration(self) -> float:
        """时长，单位秒。"""
        return self.n_samples / float(self.sr)

    def __len__(self) -> int:
        return self.n_samples

    def __array__(self, dtype: object = None, copy: bool | None = None) -> FloatArray:
        # numpy 会在拿到 float64 数组后自行完成到目标 dtype 的转换。
        return self.samples

    def segment(self, start: float, end: float) -> Signal:
        """按时间（秒）截取一段，返回新的 :class:`Signal`。"""
        if end < start:
            raise InvalidParameterError("end 不能早于 start")
        i0 = max(0, round(start * self.sr))
        i1 = min(self.n_samples, round(end * self.sr))
        return Signal(self.samples[i0:i1], self.sr)

    def __repr__(self) -> str:
        return f"Signal(n_samples={self.n_samples}, sr={self.sr}, duration={self.duration:.3f}s)"


@dataclass(frozen=True, eq=False)
