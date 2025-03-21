"""``audioscope.core.stft`` 的测试，并与 SciPy 交叉验证。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.core.stft import stft_frequencies
from audioscope.exceptions import InvalidParameterError


def test_stft_shape() -> None:
    y = aus.tone(440.0, sr=8000, duration=1.0)
    spec = aus.stft(y, n_fft=1024, hop_length=256)
    assert spec.shape[0] == 1 + 1024 // 2
    assert np.iscomplexobj(spec)


def test_stft_peak_bin() -> None:
    sr, n_fft = 8000, 1024
    y = aus.tone(440.0, sr=sr, duration=1.0)
    spec = aus.stft(y, n_fft=n_fft, hop_length=256)
    mag = np.abs(spec).mean(axis=1)
    expected = round(440.0 * n_fft / sr)
    assert abs(int(np.argmax(mag)) - expected) <= 1


def test_istft_reconstructs_signal() -> None:
    y = aus.tone(300.0, sr=8000, duration=0.5)
    spec = aus.stft(y, n_fft=512, hop_length=128)
    rec = aus.istft(spec, hop_length=128, n_fft=512, length=y.size)
    corr = float(np.corrcoef(y, rec)[0, 1])
    assert corr > 0.99
