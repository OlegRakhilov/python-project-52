#!/usr/bin/env bash
set -o errexit

# Мы не ставим uv через curl, так как в CI это может не сработать
# Используем обычный pip, который точно есть в образе
echo "--- Installing dependencies ---"
pip install --upgrade pip
pip install .

echo "--- Running migrations ---"
python manage.py migrate

echo "--- Collecting static files ---"
python manage.py collectstatic --no-input

echo "--- Build finished! ---"