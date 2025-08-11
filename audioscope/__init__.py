"""audioscope —— 面向分析与教学的音频可视化工具包。

以 NumPy / SciPy 为内核，绘图后端可选，核心流程离线可跑。顶层命名空间
汇总了最常用的加载、变换、特征与可视化接口::

    import audioscope as aus

    sig = aus.Signal(aus.tone(440, sr=22050, duration=1.0), 22050)
    spec = aus.melspectrogram(sig)
    print(aus.heatmap(spec.data))
"""

from __future__ import annotations

from ._version import __version__
from .core.chroma import chroma, chroma_filterbank
from .core.convert import (
    amplitude_to_db,
    db_to_amplitude,
    hz_to_mel,
    mel_to_hz,
    power_to_db,
)
from .core.mel import mel_filterbank, melspectrogram
from .core.spectrogram import spectrogram
from .core.stft import istft, stft
from .exceptions import (
    AudioscopeError,
    BackendNotAvailableError,
    InvalidParameterError,
    UnsupportedFormatError,
)
from .features.spectral import (
    spectral_bandwidth,
    spectral_centroid,
    spectral_flatness,
    spectral_rolloff,
)
from .features.time_domain import amplitude_envelope, rms, zero_crossing_rate
from .interactive.browser import Browser
from .io.loader import load
from .types import Signal, Spectrogram
from .utils import chirp, normalize, tone
from .viz.ascii_render import heatmap, sparkline, waveform
