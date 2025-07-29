"""命令行接口的测试。"""

from __future__ import annotations

from pathlib import Path

import pytest
from audioscope.cli import main


def test_cli_info(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--tone", "440", "--duration", "0.5", "info"]) == 0
    out = capsys.readouterr().out
    assert "采样率" in out


def test_cli_waveform() -> None:
    assert main(["--tone", "440", "--duration", "0.3", "waveform"]) == 0


@pytest.mark.parametrize("command", ["spectrogram", "mel", "chroma"])
def test_cli_spectral_commands(command: str) -> None:
    assert main(["--tone", "440", "--duration", "0.5", command]) == 0
