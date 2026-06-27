#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

OLLAMA_URL="http://localhost:${OLLAMA_PORT:-11434}/api/tags"
OPEN_WEBUI_URL="http://localhost:${OPEN_WEBUI_PORT:-3000}"
FAILED=0

echo "Checking Ollama at $OLLAMA_URL..."
if curl -fsS "$OLLAMA_URL" >/dev/null; then
  echo "OK: Ollama is reachable."
else
  echo "FAIL: Ollama is not reachable."
  FAILED=1
fi

echo "Checking Open WebUI at $OPEN_WEBUI_URL..."
if curl -fsS "$OPEN_WEBUI_URL" >/dev/null; then
  echo "OK: Open WebUI is reachable."
else
  echo "FAIL: Open WebUI is not reachable."
  FAILED=1
fi

if [ "$FAILED" -ne 0 ]; then
  echo "One or more services failed health checks."
  exit 1
fi

echo "All services are healthy."
