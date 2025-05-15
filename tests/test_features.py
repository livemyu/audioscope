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


def test_zcr_higher_for_high_frequency() -> None:
    low = zero_crossing_rate(aus.tone(100.0, sr=8000, duration=1.0))
    high = zero_crossing_rate(aus.tone(2000.0, sr=8000, duration=1.0))
    assert high.mean() > low.mean()


def test_amplitude_envelope_bounds() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    env = amplitude_envelope(y, frame_length=512, hop_length=256)
    assert np.all(env <= np.max(np.abs(y)) + 1e-9)


def _mag(y: np.ndarray, sr: int) -> tuple[np.ndarray, np.ndarray]:
    spec = aus.spectrogram(y, sr, n_fft=1024, hop_length=256, power=1.0)
    assert spec.freqs is not None
    return spec.data, spec.freqs


def test_spectral_centroid_tracks_frequency() -> None:
    low, freqs = _mag(aus.tone(200.0, sr=8000, duration=1.0), 8000)
    high, _ = _mag(aus.tone(3000.0, sr=8000, duration=1.0), 8000)
    assert spectral_centroid(high, freqs).mean() > spectral_centroid(low, freqs).mean()


def test_spectral_rolloff_within_nyquist() -> None:
    data, freqs = _mag(aus.tone(1000.0, sr=8000, duration=1.0), 8000)
    rolloff = spectral_rolloff(data, freqs)
    assert np.all(rolloff <= 4000.0)
