"""``audioscope.utils`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.utils import frame_count, to_mono


def test_tone_length_and_dtype() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    assert y.shape == (4000,)
    assert y.dtype == np.float64


def test_tone_peak_frequency() -> None:
    sr = 8000
    y = aus.tone(500.0, sr=sr, duration=1.0)
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(y.size, 1 / sr)
    assert abs(freqs[int(np.argmax(spectrum))] - 500.0) < 2.0


@pytest.mark.parametrize("bad", [0.0, -10.0])
def test_tone_rejects_nonpositive_freq(bad: float) -> None:
    with pytest.raises(InvalidParameterError):
        aus.tone(bad)


def test_chirp_length() -> None:
    y = aus.chirp(100.0, 1000.0, sr=8000, duration=0.25)
    assert y.size == 2000
