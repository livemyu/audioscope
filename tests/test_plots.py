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
