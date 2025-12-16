#!/usr/bin/env bash
set -euo pipefail

# Simple script to run the Flask app in a local virtualenv.
# Usage:
#   ./run.sh [PORT]
# If `.venv` does not exist it will be created and `requirements.txt` installed.

PORT=${1:-5000}
VENV=".venv"
PY="$VENV/bin/python"

if [ ! -d "$VENV" ]; then
  echo "Creating virtualenv in $VENV..."
  python3 -m venv "$VENV"
  "$PY" -m pip install --upgrade pip
  echo "Installing requirements..."
  "$PY" -m pip install -r requirements.txt
fi

echo "Starting StockQuotes on http://127.0.0.1:$PORT"
exec "$PY" -u -c "from app import app; app.run(host='127.0.0.1', port=$PORT, debug=False)"
