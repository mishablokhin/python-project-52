install:
	uv sync

build:
	./build.sh

collectstatic:
	python hexlet-code/manage.py collectstatic --noinput

migrate:
	python hexlet-code/manage.py migrate

render-start:
	.venv/bin/python -m gunicorn --chdir hexlet-code task_manager.wsgi

start-debug-local:
	uv run .venv/bin/python -m gunicorn --chdir hexlet-code --reload --log-level debug task_manager.wsgi

make-migrations-local:
	.venv/bin/python hexlet-code/manage.py makemigrations

migrate-local:
	.venv/bin/python hexlet-code/manage.py migrate

collectstatic-local:
	.venv/bin/python hexlet-code/manage.py collectstatic

lint:
	uv run flake8 hexlet-code/task_manager