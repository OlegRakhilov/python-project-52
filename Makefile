setup:
	pip install --break-system-packages .
	python3 manage.py migrate
	
build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

dev:
	python3 manage.py runserver

shell:
	python3 manage.py shell

ci-install:
	uv sync

# Миграции для CI
ci-migrate:
	uv run python manage.py migrate

# Запуск тестов с генерацией XML отчета для SonarCloud
ci-test:
	uv run pytest --cov=. --cov-report=xml

# Остальные команды (для локальной разработки)
lint:
	uv run ruff check .

test:
	uv run pytest