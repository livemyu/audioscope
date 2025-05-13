"""``audioscope.features`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.features import (
    amplitude_envelope,
    rms,
    spectral_bandwidth,
    spectral_centroid,
    spectral_flatness,
    spectral_rolloff,
    zero_crossing_rate,
)


def test_rms_of_constant_signal() -> None:
    y = np.full(4096, 0.3)
    values = rms(y, frame_length=1024, hop_length=512, center=False)
    assert np.allclose(values, 0.3, atol=1e-9)


def test_rms_frame_count() -> None:
    y = aus.tone(440.0, sr=8000, duration=1.0)
    values = rms(y, frame_length=1024, hop_length=256)
    assert values.ndim == 1 and values.size > 0
