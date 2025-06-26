"""可视化子包：ASCII 渲染、颜色表、可选的 matplotlib 后端。"""

from __future__ import annotations

from .ascii_render import heatmap, sparkline, waveform
from .backends import available_backends, has_matplotlib
from .colormaps import apply_colormap, available_colormaps, get_colormap
from .plots import plot_chroma, plot_mel, plot_spectrogram, plot_waveform

__all__ = [
    "apply_colormap",
    "available_backends",
    "available_colormaps",
    "get_colormap",
    "has_matplotlib",
    "heatmap",
    "plot_chroma",
    "plot_mel",
    "plot_spectrogram",
    "plot_waveform",
    "sparkline",
    "waveform",
]
