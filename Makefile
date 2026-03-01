build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

dev:
	python manage.py runserver

shell:
	python manage.py shell

lint:
	ruff check .

test:
	python manage.py test