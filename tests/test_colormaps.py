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


def test_apply_colormap_shape() -> None:
    data = np.linspace(0.0, 1.0, 20).reshape(4, 5)
    rgb = apply_colormap(data, "viridis")
    assert rgb.shape == (4, 5, 3)
    assert rgb.dtype == np.uint8


def test_apply_colormap_endpoints_differ() -> None:
    rgb = apply_colormap(np.array([[0.0, 1.0]]), "magma")
    assert not np.array_equal(rgb[0, 0], rgb[0, 1])
