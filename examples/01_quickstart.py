"""快速上手：合成一个纯音，打印基本信息与 ASCII 波形。

运行：
    python examples/01_quickstart.py
"""

from __future__ import annotations

import audioscope as aus


def main() -> None:
    sr = 22050
    signal = aus.Signal(aus.tone(440.0, sr=sr, duration=1.0), sr)

    print(f"采样率: {signal.sr} Hz")
    print(f"时长:   {signal.duration:.2f} s")
    print(f"样本数: {signal.n_samples}")

    print("\n波形（ASCII）:")
    print(aus.waveform(signal.samples, width=72, height=9))

    print("\nsparkline:")
    print(aus.sparkline(signal.samples, width=72))


if __name__ == "__main__":
    main()
