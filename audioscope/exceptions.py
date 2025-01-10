"""audioscope 的异常层次结构。

所有对外抛出的异常都继承自 :class:`AudioscopeError`，方便调用方
用一个 ``except`` 捕获本库产生的全部错误。
"""

from __future__ import annotations


class AudioscopeError(Exception):
    """所有 audioscope 异常的基类。"""


class InvalidParameterError(AudioscopeError, ValueError):
    """当传入的参数非法时抛出，例如 ``hop_length <= 0``。"""


class UnsupportedFormatError(AudioscopeError):
    """当音频文件的格式或编码方式不受支持时抛出。"""


class BackendNotAvailableError(AudioscopeError, RuntimeError):
    """当请求的绘图后端不可用时抛出，例如未安装 matplotlib。"""


__all__ = [
    "AudioscopeError",
    "BackendNotAvailableError",
    "InvalidParameterError",
    "UnsupportedFormatError",
]
