"""梅尔谱与色度：对比不同音符在色度图上的位置。

运行：
    python examples/03_mel_and_chroma.py
"""

from __future__ import annotations

import audioscope as aus
import numpy as np
from audioscope.core.chroma import NOTE_NAMES


def main() -> None:
    sr = 22050
    # C 大三和弦：C4 + E4 + G4
    freqs = {"C4": 261.63, "E4": 329.63, "G4": 392.00}
    tones = [aus.tone(f, sr=sr, duration=2.0) for f in freqs.values()]
    chord = np.sum(tones, axis=0)

    mel = aus.melspectrogram(chord, sr, n_fft=2048, hop_length=512, n_mels=48)
    print("梅尔谱:")
    print(aus.heatmap(aus.power_to_db(mel.data), width=80, height=16))

    chroma = aus.chroma(chord, sr, n_fft=2048, hop_length=512)
    energy = chroma.data.sum(axis=1)
    print("\n各音级能量（应在 C / E / G 处最高）:")
    for name, value in sorted(zip(NOTE_NAMES, energy, strict=False), key=lambda kv: -kv[1])[:5]:
        print(f"  {name:2s}  {value:8.2f}")


if __name__ == "__main__":
    main()
