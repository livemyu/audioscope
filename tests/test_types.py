"""``audioscope.types`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.types import Spectrogram


def test_signal_basic_properties(sine_signal: aus.Signal) -> None:
    assert sine_signal.n_samples == 8000
    assert sine_signal.sr == 8000
    assert np.isclose(sine_signal.duration, 1.0)
    assert len(sine_signal) == 8000


def test_signal_rejects_2d() -> None:
    with pytest.raises(InvalidParameterError):
        aus.Signal(np.zeros((2, 10)), 8000)


def test_signal_rejects_bad_sr() -> None:
    with pytest.raises(InvalidParameterError):
        aus.Signal(np.zeros(10), 0)


def test_signal_as_array(sine_signal: aus.Signal) -> None:
    arr = np.asarray(sine_signal)
    assert arr.shape == (8000,)
    converted = np.asarray(sine_signal, dtype=np.float32)
    assert converted.dtype == np.float32


def test_signal_segment(sine_signal: aus.Signal) -> None:
    seg = sine_signal.segment(0.25, 0.5)
    assert seg.n_samples == 2000
    assert seg.sr == sine_signal.sr
