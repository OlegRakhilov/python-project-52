build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

dev:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

lint:
	uv run ruff check .