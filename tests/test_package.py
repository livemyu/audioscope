"""公共 API 的冒烟测试。"""

from __future__ import annotations

import audioscope as aus


def test_version_is_string() -> None:
    assert isinstance(aus.__version__, str)
    assert aus.__version__.count(".") >= 2


def test_public_api_surface() -> None:
    expected = {
        "Signal",
        "Spectrogram",
        "Browser",
        "load",
        "stft",
        "istft",
        "spectrogram",
        "melspectrogram",
        "chroma",
        "tone",
        "heatmap",
    }
    assert expected.issubset(set(aus.__all__))
