#!/usr/bin/env bash
# Build the Gentle Productivity Manual site into ./site
set -euo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
python3 scripts/build.py --clean --out "${1:-site}"
