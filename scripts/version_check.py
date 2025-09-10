#!/usr/bin/env python
"""校验 ``pyproject.toml`` 与 ``audioscope/_version.py`` 中的版本号是否一致。

发布前跑一遍，避免打出的 tag 与包内版本对不上。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parent.parent


def pyproject_version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))
    return str(data["project"]["version"])


def module_version() -> str:
    text = (ROOT / "audioscope" / "_version.py").read_text("utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if match is None:
        raise SystemExit("在 _version.py 中找不到 __version__")
    return match.group(1)


def main() -> int:
    proj, mod = pyproject_version(), module_version()
    if proj != mod:
        print(f"版本不一致: pyproject={proj} 而 _version.py={mod}")
        return 1
    print(f"版本一致: {proj}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
