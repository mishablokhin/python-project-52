install:
	uv sync

build:
	./build.sh

start-debug-local:
	uv run .venv/bin/python -m gunicorn --reload --log-level debug task_manager.wsgi

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

render-start:
	.venv/bin/python -m gunicorn task_manager.wsgi

make-migrations-local:
	.venv/bin/python manage.py makemigrations

migrate-local:
	.venv/bin/python manage.py migrate

collectstatic-local:
	.venv/bin/python manage.py collectstatic

compile-locale:
	.venv/bin/python manage.py compilemessages

lint:
	uv run flake8

test:
	.venv/bin/pytest --ds=task_manager.settings --cov=. --cov-report=term-missing