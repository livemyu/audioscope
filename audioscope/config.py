"""全局默认参数。

大多数高层函数（STFT、梅尔谱、色度等）都从这里读取默认值，用户
既可以在调用时逐个覆盖，也可以修改 :data:`DEFAULTS` 做全局调整。
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Config:
    """一组可复用的分析默认参数。"""

    sr: int = 22050
    n_fft: int = 2048
    hop_length: int = 512
    win_length: int | None = None
    window: str = "hann"
    n_mels: int = 128
    n_chroma: int = 12
    center: bool = True

    def with_overrides(self, **kwargs: object) -> Config:
        """返回一个覆盖了指定字段的新配置（原配置不变）。"""
        return replace(self, **kwargs)  # type: ignore[arg-type]


#: 库级别的默认配置实例。
DEFAULTS = Config()

__all__ = ["DEFAULTS", "Config"]
