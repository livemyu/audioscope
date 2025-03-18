"""``audioscope.core.convert`` 的测试。"""

from __future__ import annotations

import numpy as np
import pytest
from audioscope.core.convert import (
    amplitude_to_db,
    db_to_power,
    hz_to_mel,
    mel_to_hz,
    power_to_db,
)


def test_hz_mel_roundtrip() -> None:
    freqs = np.array([0.0, 100.0, 440.0, 1000.0, 4000.0, 8000.0])
    assert np.allclose(mel_to_hz(hz_to_mel(freqs)), freqs, atol=1e-6)


def test_hz_to_mel_zero() -> None:
    assert np.isclose(hz_to_mel(np.array([0.0]))[0], 0.0)


def test_htk_roundtrip() -> None:
    freqs = np.array([50.0, 500.0, 5000.0])
    assert np.allclose(mel_to_hz(hz_to_mel(freqs, htk=True), htk=True), freqs, atol=1e-6)


def test_power_to_db_reference() -> None:
    assert np.isclose(power_to_db(np.array([1.0]), top_db=None)[0], 0.0)


def test_power_to_db_monotonic() -> None:
    db = power_to_db(np.array([0.01, 0.1, 1.0]), top_db=None)
    assert db[0] < db[1] < db[2]


def test_db_power_inverse() -> None:
    power = np.array([0.001, 0.5, 2.0])
    db = power_to_db(power, top_db=None)
    assert np.allclose(db_to_power(db), power, rtol=1e-6)
