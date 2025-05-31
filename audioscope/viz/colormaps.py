"""内置颜色表。

为了在没有 matplotlib 的情况下也能导出彩色图像，这里内置了几个常用
colormap 的锚点，运行时线性插值到任意长度。数值取自各 colormap 的
采样点，足够用于导出与教学，不追求逐位复现。
"""

from __future__ import annotations

import numpy as np

from .._typing import RGBArray
from ..exceptions import InvalidParameterError

# 每个 colormap 用若干 (r, g, b) 锚点表示，取值范围 0-1。
_ANCHORS: dict[str, list[tuple[float, float, float]]] = {
    "gray": [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],
    "magma": [
        (0.001, 0.000, 0.014),
        (0.316, 0.072, 0.485),
        (0.716, 0.215, 0.475),
        (0.965, 0.540, 0.373),
        (0.987, 0.991, 0.750),
    ],
    "viridis": [
        (0.267, 0.005, 0.329),
        (0.283, 0.141, 0.458),
        (0.254, 0.265, 0.530),
        (0.164, 0.471, 0.558),
        (0.128, 0.567, 0.551),
        (0.478, 0.821, 0.318),
        (0.993, 0.906, 0.144),
    ],
    "inferno": [
        (0.001, 0.000, 0.014),
        (0.341, 0.062, 0.429),
        (0.735, 0.215, 0.330),
        (0.978, 0.557, 0.035),
        (0.988, 0.998, 0.645),
    ],
}


def available_colormaps() -> list[str]:
    """返回所有内置 colormap 的名字。"""
    return sorted(_ANCHORS)


def get_colormap(name: str = "magma", n: int = 256) -> RGBArray:
    """把某个 colormap 插值成 ``(n, 3)`` 的 uint8 查找表。"""
    if name not in _ANCHORS:
        raise InvalidParameterError(f"未知 colormap：{name!r}，可选 {available_colormaps()}")
    if n <= 0:
        raise InvalidParameterError("n 必须为正")
    anchors = np.asarray(_ANCHORS[name], dtype=np.float64)
    xp = np.linspace(0.0, 1.0, anchors.shape[0])
    x = np.linspace(0.0, 1.0, n)
    channels = [np.interp(x, xp, anchors[:, c]) for c in range(3)]
    table = np.stack(channels, axis=1)
    return np.asarray(np.clip(table * 255.0, 0, 255).round(), dtype=np.uint8)


def apply_colormap(values: np.ndarray, name: str = "magma") -> RGBArray:
    """把归一化到 ``[0, 1]`` 的数组映射成 RGB 图像 ``(..., 3)`` uint8。"""
    arr = np.clip(np.asarray(values, dtype=np.float64), 0.0, 1.0)
    table = get_colormap(name, 256)
    idx = np.asarray(arr * 255.0, dtype=np.int64)
    return np.asarray(table[idx], dtype=np.uint8)


__all__ = ["apply_colormap", "available_colormaps", "get_colormap"]
