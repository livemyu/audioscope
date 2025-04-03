"""``audioscope.core.spectrogram`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
from audioscope.types import Spectrogram


def test_spectrogram_power_is_magnitude_squared() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    mag = aus.spectrogram(y, 8000, n_fft=512, hop_length=128, power=1.0)
    power = aus.spectrogram(y, 8000, n_fft=512, hop_length=128, power=2.0)
    assert np.allclose(power.data, mag.data**2, rtol=1e-6)


def test_spectrogram_kind_labels() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    assert aus.spectrogram(y, 8000, power=1.0).kind == "magnitude"
    assert aus.spectrogram(y, 8000, power=2.0).kind == "power"


def test_spectrogram_accepts_signal() -> None:
    sig = aus.Signal(aus.tone(440.0, sr=8000, duration=0.5), 8000)
    spec = aus.spectrogram(sig, n_fft=512, hop_length=128)
    assert isinstance(spec, Spectrogram)
    assert spec.sr == 8000
    assert spec.freqs is not None and spec.freqs.shape[0] == spec.n_bins
