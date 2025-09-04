"""把梅尔谱导出成 PNG —— 使用内置编码器，无需 matplotlib / Pillow。

运行：
    python examples/04_export_png.py
会在当前目录生成 mel.png。
"""

from __future__ import annotations

from pathlib import Path

import audioscope as aus
from audioscope.export import save_image, save_npz


def main() -> None:
    sr = 22050
    sweep = aus.chirp(100.0, 8000.0, sr=sr, duration=4.0)
    mel = aus.melspectrogram(sweep, sr, n_fft=2048, hop_length=512, n_mels=128)

    out = Path("mel.png")
    save_image(mel, out, cmap="magma")
    save_npz(mel, "mel.npz")

    print(f"已写出 {out.resolve()}  ({out.stat().st_size} 字节)")
    print("已写出 mel.npz（可用 numpy.load 复现谱数据）")


if __name__ == "__main__":
    main()
