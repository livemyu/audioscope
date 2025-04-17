"""``audioscope.core.chroma`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.core.chroma import NOTE_NAMES, chroma_filterbank


def test_chroma_filterbank_shape() -> None:
    fb = chroma_filterbank(8000, 1024)
    assert fb.shape == (12, 1 + 1024 // 2)


@pytest.mark.parametrize(
    ("freq", "pitch_class"),
    [(440.0, 9), (261.63, 0), (329.63, 4)],  # A4, C4, E4
)
def test_chroma_peaks_at_expected_pitch_class(freq: float, pitch_class: int) -> None:
    y = aus.tone(freq, sr=8000, duration=1.0)
    ch = aus.chroma(y, 8000, n_fft=2048, hop_length=512)
    assert int(np.argmax(ch.data.sum(axis=1))) == pitch_class


def test_chroma_labels() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.3)
    ch = aus.chroma(y, 8000, n_fft=1024, hop_length=256)
    assert ch.bin_labels == NOTE_NAMES
    assert ch.shape[0] == 12
