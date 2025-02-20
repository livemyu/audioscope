"""``audioscope.core.framing`` 的测试。"""

from __future__ import annotations

import numpy as np
import pytest
from audioscope.core.framing import frame, pad_center
from audioscope.exceptions import InvalidParameterError


def test_frame_shape() -> None:
    y = np.arange(1000, dtype=np.float64)
    frames = frame(y, 256, 128)
    assert frames.shape == (1 + (1000 - 256) // 128, 256)


def test_frame_first_and_second_frame_content() -> None:
    y = np.arange(20, dtype=np.float64)
    frames = frame(y, 8, 4)
    assert np.array_equal(frames[0], y[0:8])
    assert np.array_equal(frames[1], y[4:12])


def test_frame_rejects_short_signal() -> None:
    with pytest.raises(InvalidParameterError):
        frame(np.zeros(4), 8, 2)
