"""命令行入口 ``audioscope``。

不带输入文件时可以用 ``--tone`` / ``--chirp`` 现场合成信号，因此完全
离线也能跑通所有子命令。默认输出 ASCII 图，``--output`` 指定 ``.png``
时改用内置 PNG 编码器导出彩色图像。
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__
from .core.chroma import chroma
from .core.convert import power_to_db
from .core.mel import melspectrogram
from .core.spectrogram import spectrogram
from .exceptions import AudioscopeError
from .io.loader import load
from .types import Signal, Spectrogram
from .utils import chirp, tone
from .viz.ascii_render import heatmap, sparkline, waveform


def build_parser() -> argparse.ArgumentParser:
    """构造并返回命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="audioscope",
        description="音频可视化工具包：波形 / 声谱 / 梅尔 / 色度。",
    )
    parser.add_argument("--version", action="version", version=f"audioscope {__version__}")

    src = parser.add_argument_group("输入")
    src.add_argument("input", nargs="?", help="WAV 文件路径（省略则需配合 --tone/--chirp）")
    src.add_argument("--tone", type=float, metavar="HZ", help="合成指定频率的纯音")
    src.add_argument("--chirp", nargs=2, type=float, metavar=("F0", "F1"), help="合成线性扫频")
    src.add_argument("--sr", type=int, default=22050, help="采样率（合成时使用）")
    src.add_argument("--duration", type=float, default=2.0, help="合成信号时长（秒）")

    ana = parser.add_argument_group("分析参数")
    ana.add_argument("--n-fft", type=int, default=1024, dest="n_fft")
    ana.add_argument("--hop", type=int, default=256, dest="hop_length")
    ana.add_argument("--n-mels", type=int, default=64, dest="n_mels")

    out = parser.add_argument_group("输出")
    out.add_argument("--width", type=int, default=80)
    out.add_argument("--height", type=int, default=20)
    out.add_argument("-o", "--output", help="导出路径（.png 使用内置编码器）")
    out.add_argument("--cmap", default="magma")

    parser.add_argument(
        "command",
        choices=["info", "waveform", "spectrogram", "mel", "chroma"],
        help="要执行的操作",
    )
    return parser
