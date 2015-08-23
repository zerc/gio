.PHONY: clean-pyc clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "run - run development server"
	@echo "install - install all deps"

clean: clean-pyc

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

run: clean
	python gio/manage.py runserver

pull:
	python gio/manage.py pull

test: clean
	python gio/tests.py

install:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt
	@echo 'Done! Try type "make run" now'
