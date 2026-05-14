#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 apps/grok-kb-agent-suite/backend/server.py --port "${PORT:-8765}"
