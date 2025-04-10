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


def test_melspectrogram_shape() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    mel = aus.melspectrogram(y, 8000, n_fft=512, hop_length=128, n_mels=24)
    assert mel.shape[0] == 24
    assert mel.kind == "mel"
    assert np.all(mel.data >= 0)


def test_melspectrogram_matches_manual_projection() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.5)
    spec = aus.spectrogram(y, 8000, n_fft=512, hop_length=128, power=2.0)
    fb = mel_filterbank(8000, 512, n_mels=24)
    mel = aus.melspectrogram(y, 8000, n_fft=512, hop_length=128, n_mels=24)
    assert np.allclose(mel.data, fb @ spec.data, rtol=1e-6)
