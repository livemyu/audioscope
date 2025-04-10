"""``audioscope.core.mel`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
from audioscope.core.mel import mel_filterbank, mel_frequencies


def test_mel_frequencies_monotonic() -> None:
    freqs = mel_frequencies(20, fmin=0.0, fmax=4000.0)
    assert freqs.shape == (20,)
    assert np.all(np.diff(freqs) > 0)


def test_mel_filterbank_shape_and_nonneg() -> None:
    fb = mel_filterbank(8000, 512, n_mels=32)
    assert fb.shape == (32, 1 + 512 // 2)
    assert np.all(fb >= 0)


def test_mel_filterbank_each_band_has_energy() -> None:
    fb = mel_filterbank(8000, 1024, n_mels=40)
    assert np.all(fb.sum(axis=1) > 0)
