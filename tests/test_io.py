"""``audioscope.io`` 的读写往返测试。"""

from __future__ import annotations

from pathlib import Path

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import UnsupportedFormatError
from audioscope.io import load, read_wav, write_wav


def test_wav_roundtrip_mono(tmp_path: Path) -> None:
    y = aus.tone(440.0, sr=8000, duration=0.25)
    path = tmp_path / "mono.wav"
    write_wav(path, y, 8000)
    back, sr = read_wav(path)
    assert sr == 8000
    assert back.shape == y.shape
    assert np.allclose(back, y, atol=1e-3)


def test_wav_roundtrip_stereo(tmp_path: Path) -> None:
    left = aus.tone(300.0, sr=8000, duration=0.1)
    right = aus.tone(600.0, sr=8000, duration=0.1)
    stereo = np.stack([left, right])
    path = tmp_path / "stereo.wav"
    write_wav(path, stereo, 8000)
    back, _ = read_wav(path)
    assert back.shape == (2, left.size)


def test_load_returns_signal(tmp_path: Path) -> None:
    y = aus.tone(440.0, sr=8000, duration=0.25)
    path = tmp_path / "a.wav"
    write_wav(path, y, 8000)
    sig = load(path)
    assert isinstance(sig, aus.Signal)
    assert sig.sr == 8000
