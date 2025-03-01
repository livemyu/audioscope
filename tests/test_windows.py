"""``audioscope.core.windows`` 的测试。"""

from __future__ import annotations

import numpy as np
import pytest
from audioscope.core.windows import get_window
from audioscope.exceptions import InvalidParameterError


@pytest.mark.parametrize("name", ["hann", "hamming", "blackman", "bartlett", "boxcar"])
def test_window_length(name: str) -> None:
    assert get_window(name, 64).shape == (64,)


def test_boxcar_is_ones() -> None:
    assert np.allclose(get_window("boxcar", 16), 1.0)


def test_symmetric_hann_endpoints_are_zero() -> None:
    w = get_window("hann", 65, fftbins=False)
    assert np.isclose(w[0], 0.0, atol=1e-9)
    assert np.isclose(w[-1], 0.0, atol=1e-9)


def test_periodic_and_symmetric_differ() -> None:
    assert not np.allclose(
        get_window("hann", 32, fftbins=True),
        get_window("hann", 32, fftbins=False),
    )


def test_aliases() -> None:
    assert np.allclose(get_window("hanning", 16), get_window("hann", 16))
    assert np.allclose(get_window("rectangular", 16), get_window("boxcar", 16))


def test_unknown_window_raises() -> None:
    with pytest.raises(InvalidParameterError):
        get_window("nope", 16)
