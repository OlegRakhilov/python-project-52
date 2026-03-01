setup:
	pip install .
	python3 manage.py migrate
	
build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

dev:
	python3 manage.py runserver

shell:
	python3 manage.py shell

lint:
	python3 -m ruff check .

test:
	python3 manage.py test