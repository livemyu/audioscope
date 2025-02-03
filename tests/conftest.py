"""pytest 全局夹具：可复现的合成信号。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest

SR = 8000


@pytest.fixture
def sr() -> int:
    return SR


@pytest.fixture
def sine(sr: int) -> np.ndarray:
    """440Hz、时长 1 秒的纯音。"""
    return aus.tone(440.0, sr=sr, duration=1.0)


@pytest.fixture
def sine_signal(sr: int, sine: np.ndarray) -> aus.Signal:
    return aus.Signal(sine, sr)


@pytest.fixture
def white_noise(sr: int) -> np.ndarray:
    rng = np.random.default_rng(0)
    return rng.standard_normal(sr).astype(np.float64) * 0.1
