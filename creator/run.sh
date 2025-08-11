#!/bin/bash
set -euo pipefail

# Wipe output directory
rm -rf output/*

# Run steps in order
uv run namebuilder
uv run name_chopper -l oceans=1 -l continents=1 -l regions=1 -l cities=1 --seed 42
uv run descriptionbuilder
uv run imagebuilder
uv run package_world
