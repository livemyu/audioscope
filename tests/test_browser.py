"""``audioscope.interactive.Browser`` 的测试。"""

from __future__ import annotations

import audioscope as aus
import pytest
from audioscope.exceptions import InvalidParameterError


def _spec() -> aus.Spectrogram:
    y = aus.chirp(100.0, 3000.0, sr=8000, duration=2.0)
    return aus.melspectrogram(y, 8000, n_fft=512, hop_length=128, n_mels=32)


def test_browser_view_shape() -> None:
    browser = aus.Browser(_spec(), window=20)
    assert browser.view().shape[1] == 20


def test_browser_next_prev_are_bounded() -> None:
    spec = _spec()
    browser = aus.Browser(spec, window=10)
    for _ in range(1000):
        browser.next()
    assert browser.stop <= spec.n_frames
    browser.prev(10_000)
    assert browser.start == 0


def test_browser_seek_and_time_range() -> None:
    browser = aus.Browser(_spec(), window=10)
    browser.seek(1.0)
    t0, t1 = browser.time_range
    assert t0 <= 1.0 <= t1


def test_browser_zoom_changes_window() -> None:
    browser = aus.Browser(_spec(), window=20)
    browser.zoom(0.5)
    assert browser.window == 10


def test_browser_zoom_rejects_nonpositive() -> None:
    with pytest.raises(InvalidParameterError):
        aus.Browser(_spec()).zoom(0.0)


def test_browser_render_lines() -> None:
    art = aus.Browser(_spec(), window=20).render(width=40, height=10)
    assert len(art.splitlines()) == 10


def test_browser_from_signal() -> None:
    sig = aus.Signal(aus.tone(440.0, sr=8000, duration=1.0), 8000)
    browser = aus.Browser.from_signal(sig, window=15, n_fft=512, hop_length=128, n_mels=16)
    assert browser.spec.kind == "mel"
    assert isinstance(browser.render(), str)
