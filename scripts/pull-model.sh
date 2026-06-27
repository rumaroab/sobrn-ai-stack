#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-llama3.1:8b}"
CONTAINER_NAME="sobrn-ollama"

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  echo "Ollama container '$CONTAINER_NAME' is not running."
  echo "Start the stack first: docker compose up -d"
  exit 1
fi

echo "Pulling model '$MODEL' inside $CONTAINER_NAME..."
docker exec "$CONTAINER_NAME" ollama pull "$MODEL"
echo "Model '$MODEL' is ready."
