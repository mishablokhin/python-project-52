install:
	uv pip install --system .

build:
	./build.sh

collectstatic:
	python hexlet-code/manage.py collectstatic --noinput

migrate:
	python hexlet-code/manage.py migrate

render-start:
	gunicorn task_manager.wsgi

start-debug-local:
	uv run .venv/bin/python -m gunicorn --chdir hexlet-code --reload --log-level debug task_manager.wsgi

lint:
	uv run flake8 hexlet-code/task_manager