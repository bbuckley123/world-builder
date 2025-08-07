#!/usr/bin/env bash
set -e

# Re-create venv
rm -rf .venv
uv venv .venv --python 3.13

# Activate & sync deps
source .venv/bin/activate
uv sync

python -m ensurepip

echo "✅ Ready!"
