"""``audioscope.viz.colormaps`` 的测试。"""

from __future__ import annotations

import numpy as np
import pytest
from audioscope.exceptions import InvalidParameterError
from audioscope.viz.colormaps import apply_colormap, available_colormaps, get_colormap


def test_available_colormaps() -> None:
    names = available_colormaps()
    assert "magma" in names
    assert "viridis" in names


def test_get_colormap_shape_and_dtype() -> None:
    table = get_colormap("magma", 128)
    assert table.shape == (128, 3)
    assert table.dtype == np.uint8
