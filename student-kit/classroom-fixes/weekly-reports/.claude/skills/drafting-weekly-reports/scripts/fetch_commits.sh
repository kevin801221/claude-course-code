#!/usr/bin/env bash
# 保留原 CLI，交給 Python 的 JSON encoder 處理 Git/gh 文字。
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$script_dir/fetch_commits.py" "$@"
