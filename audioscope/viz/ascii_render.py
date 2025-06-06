"""纯文本（ASCII / Unicode）渲染。

这是本项目“离线可跑”的核心：不依赖任何绘图库，就能在终端里画出
波形、包络和声谱热力图，适合远程终端、CI 日志与教学演示。
"""

from __future__ import annotations

import numpy as np

from ..exceptions import InvalidParameterError

#: 由浅到深的灰度字符梯度。
DENSITY_CHARS = " .:-=+*#%@"

#: 用于 sparkline 的 8 级方块。
_BARS = "▁▂▃▄▅▆▇█"


def _resize(data: np.ndarray, height: int, width: int) -> np.ndarray:
    """用最近邻把二维数组缩放到 ``(height, width)``。"""
    rows = np.linspace(0, data.shape[0] - 1, height).round().astype(np.int64)
    cols = np.linspace(0, data.shape[1] - 1, width).round().astype(np.int64)
    return data[np.ix_(rows, cols)]


def _normalize(data: np.ndarray) -> np.ndarray:
    lo = float(np.min(data))
    hi = float(np.max(data))
    if hi - lo < 1e-12:
        return np.zeros_like(data)
    return (data - lo) / (hi - lo)


def heatmap(
    data: np.ndarray,
    *,
    width: int = 80,
    height: int = 20,
    chars: str = DENSITY_CHARS,
) -> str:
    """把二维数组渲染成 ASCII 热力图（低频在下、时间自左向右）。"""
    arr = np.asarray(data, dtype=np.float64)
    if arr.ndim != 2:
        raise InvalidParameterError("heatmap 需要二维数组")
    if width <= 0 or height <= 0:
        raise InvalidParameterError("width 与 height 必须为正")
    resized = _resize(arr, height, width)
    norm = _normalize(resized)
    levels = np.asarray(norm * (len(chars) - 1), dtype=np.int64)
    rows = ["".join(chars[v] for v in row) for row in levels]
    return "\n".join(reversed(rows))


def sparkline(y: np.ndarray, *, width: int = 80) -> str:
    """把一维序列压缩成单行 sparkline。"""
    arr = np.asarray(y, dtype=np.float64)
    if arr.ndim != 1:
        raise InvalidParameterError("sparkline 需要一维数组")
    if arr.size == 0:
        return ""
    if arr.size > width:
        idx = np.linspace(0, arr.size - 1, width).round().astype(np.int64)
        arr = arr[idx]
    norm = _normalize(arr)
    levels = np.asarray(norm * (len(_BARS) - 1), dtype=np.int64)
    return "".join(_BARS[v] for v in levels)
