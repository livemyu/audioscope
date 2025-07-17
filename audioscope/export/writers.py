"""导出：谱数据（npz / csv）与彩色图像（自带极简 PNG 编码器）。

PNG 编码只用到标准库 ``zlib`` 与 ``struct``，因此即便没有 matplotlib /
Pillow，也能把声谱图导出成彩色图片，契合“离线可跑”的目标。
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

import numpy as np

from .._typing import FloatArray
from ..core.convert import power_to_db
from ..exceptions import InvalidParameterError
from ..types import Spectrogram
from ..viz.colormaps import apply_colormap

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _png_chunk(tag: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + tag
        + payload
        + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
    )


def write_png(rgb: np.ndarray, path: str | Path) -> None:
    """把 ``(H, W, 3)`` 的 uint8 数组写成 PNG 文件。"""
    arr = np.asarray(rgb, dtype=np.uint8)
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise InvalidParameterError("write_png 需要形状为 (H, W, 3) 的数组")
    height, width, _ = arr.shape

    raw = bytearray()
    for row in arr:
        raw.append(0)  # 每行的过滤类型：None
        raw.extend(row.tobytes())

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        _PNG_SIGNATURE
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _png_chunk(b"IEND", b"")
    )
    Path(path).write_bytes(png)


def _normalize(data: np.ndarray) -> FloatArray:
    lo = float(np.min(data))
    hi = float(np.max(data))
    norm = np.zeros_like(data) if hi - lo < 1e-12 else (data - lo) / (hi - lo)
    return np.asarray(norm, dtype=np.float64)


def save_image(
    spec: Spectrogram,
    path: str | Path,
    *,
    cmap: str = "magma",
    db: bool = True,
) -> None:
    """把声谱图上色后导出为 PNG（低频在下）。"""
    data = power_to_db(spec.data) if db else spec.data
    norm = _normalize(data)
    rgb = apply_colormap(norm, cmap)
    write_png(np.flipud(rgb), path)


def save_npz(spec: Spectrogram, path: str | Path) -> None:
    """把谱数据及关键元信息保存为 ``.npz``。"""
    np.savez(
        path,
        data=spec.data,
        sr=np.asarray(spec.sr),
        hop_length=np.asarray(spec.hop_length),
        n_fft=np.asarray(spec.n_fft),
        kind=np.asarray(spec.kind),
    )


def save_csv(data: np.ndarray, path: str | Path, *, delimiter: str = ",") -> None:
    """把二维数组保存为 CSV。"""
    arr = np.asarray(data, dtype=np.float64)
    if arr.ndim != 2:
        raise InvalidParameterError("save_csv 需要二维数组")
    np.savetxt(path, arr, delimiter=delimiter, fmt="%.6g")


__all__ = ["save_csv", "save_image", "save_npz", "write_png"]
