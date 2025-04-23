"""``audioscope.core.resample`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.core.resample import resample
from audioscope.exceptions import InvalidParameterError


def test_resample_identity_returns_same_length() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    assert resample(y, 8000, 8000).size == y.size


def test_resample_upsample_length() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    out = resample(y, 8000, 16000)
    assert abs(out.size - 2 * y.size) <= 2
