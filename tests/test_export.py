"""``audioscope.export`` 的测试，重点验证内置 PNG 编码器。"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.export import save_csv, save_image, save_npz, write_png

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _read_png_header(path: Path) -> tuple[int, int]:
    raw = path.read_bytes()
    assert raw[:8] == _PNG_SIGNATURE
    # IHDR 紧跟在 8 字节签名 + 4 字节长度 + 4 字节 tag 之后。
    width, height = struct.unpack(">II", raw[16:24])
    return width, height


def test_write_png_roundtrip_header(tmp_path: Path) -> None:
    rgb = np.zeros((7, 11, 3), dtype=np.uint8)
    path = tmp_path / "img.png"
    write_png(rgb, path)
    assert _read_png_header(path) == (11, 7)


def test_write_png_pixels_are_decodable(tmp_path: Path) -> None:
    rgb = np.random.default_rng(0).integers(0, 255, (4, 4, 3), dtype=np.uint8)
    path = tmp_path / "img.png"
    write_png(rgb, path)
    raw = path.read_bytes()
    # 找到 IDAT 数据并解压，校验字节数 = 高 * (1 + 宽*3)。
    idat_start = raw.index(b"IDAT") + 4
    length = struct.unpack(">I", raw[idat_start - 8 : idat_start - 4])[0]
    decompressed = zlib.decompress(raw[idat_start : idat_start + length])
    assert len(decompressed) == 4 * (1 + 4 * 3)


def test_write_png_rejects_bad_shape(tmp_path: Path) -> None:
    with pytest.raises(InvalidParameterError):
        write_png(np.zeros((4, 4), dtype=np.uint8), tmp_path / "bad.png")


def test_save_image(tmp_path: Path) -> None:
    spec = aus.melspectrogram(aus.tone(440.0, sr=8000, duration=0.5), 8000, n_mels=16)
    path = tmp_path / "mel.png"
    save_image(spec, path)
    assert path.exists() and path.stat().st_size > 0
