#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
install_dir="$repo_root/.local/bin"

mkdir -p "$install_dir"

curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="$install_dir" sh

printf '\nuv installed at: %s/uv\n' "$install_dir"
printf 'Run commands with: %s/uv <command>\n' "$install_dir"
