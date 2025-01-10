"""跨模块共享的类型别名。

集中定义可以让核心 DSP 函数的签名更短，也方便在 numpy 的
``NDArray`` 泛型上做统一约束。
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

#: 一维或二维的实数数组，统一使用 ``float64``。
FloatArray = NDArray[np.float64]

#: 复数频谱数组，统一使用 ``complex128``。
ComplexArray = NDArray[np.complex128]

#: RGB 图像数组，统一使用 ``uint8``（形状 ``(..., 3)``）。
RGBArray = NDArray[np.uint8]

__all__ = ["ComplexArray", "FloatArray", "RGBArray"]
