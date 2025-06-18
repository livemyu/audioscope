"""``audioscope.viz.ascii_render`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.viz.ascii_render import heatmap, sparkline, waveform


def test_heatmap_dimensions() -> None:
    data = np.random.default_rng(0).random((30, 50))
    art = heatmap(data, width=40, height=12)
    lines = art.splitlines()
    assert len(lines) == 12
    assert all(len(line) == 40 for line in lines)


def test_heatmap_rejects_1d() -> None:
    with pytest.raises(InvalidParameterError):
        heatmap(np.zeros(10))


def test_sparkline_length() -> None:
    y = aus.tone(5.0, sr=100, duration=1.0)
    assert len(sparkline(y, width=40)) == 40


def test_sparkline_empty() -> None:
    assert sparkline(np.zeros(0)) == ""


def test_waveform_forces_odd_height() -> None:
    y = aus.tone(5.0, sr=100, duration=1.0)
    art = waveform(y, width=30, height=8)
    assert len(art.splitlines()) == 9  # 偶数高度会 +1
