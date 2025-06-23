"""绘图后端探测。

核心与 ASCII 渲染始终可用；matplotlib 是可选后端，只有在真正需要
矢量 / 位图输出时才会用到。这里集中做“是否可用”的判断，避免在各处
重复写 try/except import。
"""

from __future__ import annotations

import importlib.util
from typing import Any

from ..exceptions import BackendNotAvailableError


def has_matplotlib() -> bool:
    """检测当前环境是否安装了 matplotlib。"""
    return importlib.util.find_spec("matplotlib") is not None


def available_backends() -> list[str]:
    """返回当前可用的后端列表，``ascii`` 总是可用。"""
    backends = ["ascii"]
    if has_matplotlib():
        backends.append("matplotlib")
    return backends


def require_matplotlib() -> Any:
    """导入并返回 ``matplotlib.pyplot``，不可用时抛出友好错误。"""
    if not has_matplotlib():
        raise BackendNotAvailableError(
            "该功能需要 matplotlib，请先安装：pip install 'audioscope[plot]'"
        )
    import matplotlib.pyplot as plt

    return plt


__all__ = ["available_backends", "has_matplotlib", "require_matplotlib"]
