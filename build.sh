#!/usr/bin/env bash
set -o errexit

echo "--- Installing uv ---"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "--- Syncing dependencies ---"
uv sync

echo "--- Collecting static files ---"
uv run python manage.py collectstatic --no-input

echo "--- Running migrations ---"
uv run python manage.py migrate

echo "--- Build finished! ---"
