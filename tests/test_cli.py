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


def test_cli_chirp_source() -> None:
    assert main(["--chirp", "200", "2000", "--duration", "0.5", "spectrogram"]) == 0


def test_cli_missing_input_returns_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["info"]) == 1
    assert "错误" in capsys.readouterr().out


def test_cli_export_png(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    out = tmp_path / "mel.png"
    code = main(["--tone", "440", "--duration", "0.5", "-o", str(out), "mel"])
    assert code == 0
    assert out.exists()
    assert "已导出" in capsys.readouterr().out
