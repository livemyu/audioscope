"""音频输入输出。

为了保证“离线可跑、依赖最少”，读写只基于标准库 ``wave`` 模块，原生
支持 8/16/32 位 PCM 及 32 位浮点 WAV。
"""

from __future__ import annotations

from .loader import load
from .wav import read_wav, write_wav

__all__ = ["load", "read_wav", "write_wav"]
