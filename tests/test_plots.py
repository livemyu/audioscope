"""matplotlib 后端的测试（未安装时自动跳过）。"""

from __future__ import annotations

import audioscope as aus
import pytest
from audioscope.viz.backends import available_backends, has_matplotlib

pytest.importorskip("matplotlib")

import matplotlib

matplotlib.use("Agg")

from audioscope.viz.plots import (
    plot_chroma,
    plot_mel,
    plot_spectrogram,
    plot_waveform,
)


def test_ascii_backend_always_available() -> None:
    assert "ascii" in available_backends()


def test_matplotlib_reported_available() -> None:
    assert has_matplotlib() is True


def test_plot_waveform_returns_axes() -> None:
    sig = aus.Signal(aus.tone(440.0, sr=8000, duration=0.3), 8000)
    ax = plot_waveform(sig)
    assert ax.get_xlabel() == "时间 / s"


def test_plot_spectrogram() -> None:
    spec = aus.spectrogram(aus.tone(440.0, sr=8000, duration=0.3), 8000, n_fft=512)
    ax = plot_spectrogram(spec)
    assert ax is not None


def test_plot_mel_and_chroma() -> None:
    y = aus.tone(440.0, sr=8000, duration=0.3)
    assert plot_mel(aus.melspectrogram(y, 8000, n_mels=16)) is not None
    assert plot_chroma(aus.chroma(y, 8000)) is not None
