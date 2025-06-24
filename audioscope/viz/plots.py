"""基于 matplotlib 的高层绘图函数。

所有函数都接受一个可选的 ``ax``；不传时会自动新建。matplotlib 未安装
时抛出 :class:`~audioscope.exceptions.BackendNotAvailableError`，可改用
:mod:`audioscope.viz.ascii_render` 中的纯文本渲染。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from ..core.convert import power_to_db
from ..types import Signal, Spectrogram
from .backends import require_matplotlib


def plot_waveform(signal: Signal, *, ax: Any = None, color: str = "#1f77b4") -> Any:
    """绘制时域波形，返回对应的 matplotlib ``Axes``。"""
    plt = require_matplotlib()
    if ax is None:
        _, ax = plt.subplots()
    times = np.arange(signal.n_samples) / float(signal.sr)
    ax.plot(times, signal.samples, color=color, linewidth=0.8)
    ax.set_xlabel("时间 / s")
    ax.set_ylabel("幅度")
    ax.set_title("波形")
    return ax


def plot_spectrogram(
    spec: Spectrogram,
    *,
    ax: Any = None,
    cmap: str = "magma",
    db: bool = True,
) -> Any:
    """把 :class:`Spectrogram` 画成热力图。"""
    plt = require_matplotlib()
    if ax is None:
        _, ax = plt.subplots()
    data = power_to_db(spec.data) if db else spec.data
    extent = [0.0, float(spec.times[-1]) if spec.n_frames else 0.0, 0.0, spec.n_bins]
    ax.imshow(data, origin="lower", aspect="auto", cmap=cmap, extent=extent)
    ax.set_xlabel("时间 / s")
    ax.set_ylabel("频率 bin")
    ax.set_title(f"{spec.kind} 谱")
    return ax
