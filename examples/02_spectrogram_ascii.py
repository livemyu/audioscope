"""在终端里画声谱图，完全不需要 matplotlib。

运行：
    python examples/02_spectrogram_ascii.py
"""

from __future__ import annotations

import audioscope as aus


def main() -> None:
    sr = 16000
    # 一段从 200Hz 扫到 6kHz 的扫频信号，声谱图上会看到一条斜线。
    sweep = aus.chirp(200.0, 6000.0, sr=sr, duration=3.0)

    spec = aus.spectrogram(sweep, sr, n_fft=1024, hop_length=256)
    db = aus.power_to_db(spec.data)

    print("扫频信号的功率声谱图（低频在下，时间自左向右）:")
    print(aus.heatmap(db, width=90, height=24))


if __name__ == "__main__":
    main()
