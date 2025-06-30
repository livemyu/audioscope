"""交互式浏览器。

:class:`Browser` 在一段声谱图上维护一个“视口”，可以前后翻页、按时间
定位、缩放，并把当前视口渲染成 ASCII 热力图——即使没有图形界面，也能
在终端里交互式地浏览长音频。
"""

from __future__ import annotations

from .._typing import FloatArray
from ..core.mel import melspectrogram
from ..exceptions import InvalidParameterError
from ..types import Signal, Spectrogram
from ..viz.ascii_render import heatmap


class Browser:
    """在声谱图上滑动的视口。

    方法（``next`` / ``prev`` / ``seek`` / ``zoom``）都返回 ``self``，因此
    可以链式调用。
    """

    def __init__(self, spec: Spectrogram, *, window: int = 100) -> None:
        if window <= 0:
            raise InvalidParameterError("window 必须为正")
        self.spec = spec
        self.window = min(window, spec.n_frames) or 1
        self.start = 0

    @classmethod
    def from_signal(cls, signal: Signal, *, window: int = 100, **kwargs: object) -> Browser:
        """先算梅尔谱，再包一个浏览器（便于直接浏览波形文件）。"""
        spec = melspectrogram(signal.samples, signal.sr, **kwargs)  # type: ignore[arg-type]
        return cls(spec, window=window)

    @property
    def stop(self) -> int:
        return min(self.start + self.window, self.spec.n_frames)

    @property
    def time_range(self) -> tuple[float, float]:
        """当前视口对应的时间区间（秒）。"""
        hop_sr = self.spec.hop_length / float(self.spec.sr)
        return (self.start * hop_sr, self.stop * hop_sr)

    def view(self) -> FloatArray:
        """返回当前视口内的数据切片。"""
        return self.spec.data[:, self.start : self.stop]

    def next(self, step: int | None = None) -> Browser:
        """向后滚动，默认滚动一个视口宽度。"""
        delta = self.window if step is None else step
        max_start = max(0, self.spec.n_frames - self.window)
        self.start = min(self.start + delta, max_start)
        return self

    def prev(self, step: int | None = None) -> Browser:
        """向前滚动。"""
        delta = self.window if step is None else step
        self.start = max(0, self.start - delta)
        return self

    def seek(self, time: float) -> Browser:
        """把视口起点定位到第 ``time`` 秒附近。"""
        frame = round(time * self.spec.sr / self.spec.hop_length)
        max_start = max(0, self.spec.n_frames - self.window)
        self.start = min(max(0, frame), max_start)
        return self

    def zoom(self, factor: float) -> Browser:
        """缩放视口宽度，``factor < 1`` 放大细节，``> 1`` 看得更宽。"""
        if factor <= 0:
            raise InvalidParameterError("factor 必须为正")
        new_window = round(self.window * factor)
        self.window = max(1, min(new_window, self.spec.n_frames))
        return self

    def render(self, *, width: int = 80, height: int = 20) -> str:
        """把当前视口渲染成 ASCII 热力图。"""
        return heatmap(self.view(), width=width, height=height)

    def __repr__(self) -> str:
        t0, t1 = self.time_range
        return f"Browser(frames={self.start}..{self.stop}, time={t0:.2f}..{t1:.2f}s)"


__all__ = ["Browser"]
