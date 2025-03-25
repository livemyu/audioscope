"""``audioscope.core.stft`` 的测试，并与 SciPy 交叉验证。"""

from __future__ import annotations

import audioscope as aus
import numpy as np
import pytest
from audioscope.core.stft import stft_frequencies
from audioscope.exceptions import InvalidParameterError


def test_stft_shape() -> None:
    y = aus.tone(440.0, sr=8000, duration=1.0)
    spec = aus.stft(y, n_fft=1024, hop_length=256)
    assert spec.shape[0] == 1 + 1024 // 2
    assert np.iscomplexobj(spec)


def test_stft_peak_bin() -> None:
    sr, n_fft = 8000, 1024
    y = aus.tone(440.0, sr=sr, duration=1.0)
    spec = aus.stft(y, n_fft=n_fft, hop_length=256)
    mag = np.abs(spec).mean(axis=1)
    expected = round(440.0 * n_fft / sr)
    assert abs(int(np.argmax(mag)) - expected) <= 1


def test_istft_reconstructs_signal() -> None:
    y = aus.tone(300.0, sr=8000, duration=0.5)
    spec = aus.stft(y, n_fft=512, hop_length=128)
    rec = aus.istft(spec, hop_length=128, n_fft=512, length=y.size)
    corr = float(np.corrcoef(y, rec)[0, 1])
    assert corr > 0.99


def test_stft_frequencies() -> None:
    freqs = stft_frequencies(8000, 1024)
    assert freqs.shape == (513,)
    assert np.isclose(freqs[0], 0.0)
    assert np.isclose(freqs[-1], 4000.0)


def test_stft_rejects_2d() -> None:
    with pytest.raises(InvalidParameterError):
        aus.stft(np.zeros((2, 100)))


def test_stft_matches_scipy() -> None:
    scipy_signal = pytest.importorskip("scipy.signal")
    sr, n_fft, hop = 8000, 256, 64
    y = aus.chirp(100.0, 2000.0, sr=sr, duration=0.5)
    ours = np.abs(aus.stft(y, n_fft=n_fft, hop_length=hop, center=False))
    _, _, ref = scipy_signal.stft(
        y,
        fs=sr,
        window="hann",
        nperseg=n_fft,
        noverlap=n_fft - hop,
        boundary=None,
        padded=False,
    )
    # 逐帧比较峰值频率 bin 的位置，验证时频结构一致。
    m = min(ours.shape[1], ref.shape[1])
    peak_ours = np.argmax(ours[:, :m], axis=0)
    peak_ref = np.argmax(np.abs(ref)[:, :m], axis=0)
    assert np.mean(np.abs(peak_ours - peak_ref) <= 2) > 0.8
