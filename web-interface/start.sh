#!/usr/bin/env bash
# start.sh — Launch the Kiro Web Interface (FastAPI wrapper around kiro-cli acp)
#
# Usage:
#   ./start.sh            # start on 127.0.0.1:8770
#   PORT=9000 ./start.sh  # custom port
#   KIRO_WEB_AGENT=compass ./start.sh   # default agent
#   KIRO_WEB_CWD=/some/dir ./start.sh   # working dir for ACP session
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PORT="${PORT:-8770}"
HOST="${HOST:-127.0.0.1}"

if [[ ! -x ".venv/bin/uvicorn" ]]; then
    echo "❌ venv introuvable. Crée-le d'abord:"
    echo "   python3 -m venv .venv && .venv/bin/pip install fastapi 'uvicorn[standard]' websockets"
    exit 1
fi

echo "🌐 Kiro Web Interface → http://${HOST}:${PORT}"
echo "   Agent par défaut: ${KIRO_WEB_AGENT:-exp2} | cwd: ${KIRO_WEB_CWD:-~/HomeWspce/kiro-configs}"
echo "   Ctrl+C pour arrêter."
exec .venv/bin/uvicorn app:app --host "$HOST" --port "$PORT"
