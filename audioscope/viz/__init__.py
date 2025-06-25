"""可视化子包：ASCII 渲染、颜色表、可选的 matplotlib 后端。"""

from __future__ import annotations

from .ascii_render import heatmap, sparkline, waveform
from .backends import available_backends, has_matplotlib
