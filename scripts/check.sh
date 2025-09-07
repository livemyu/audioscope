#!/usr/bin/env bash
# 一键运行与 CI 完全一致的本地检查。
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> ruff check"
uv run ruff check .

echo "==> ruff format --check"
uv run ruff format --check .

echo "==> mypy"
uv run mypy

echo "==> pytest"
uv run pytest "$@"

echo "全部通过 ✅"
