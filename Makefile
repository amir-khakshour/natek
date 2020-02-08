VENV = venv
.PHONY: build

all: setup server

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -Rf *.egg-info
	rm -Rf dist/
	rm -Rf build/

setup:
	sudo apt install python3.5 python3-pip
	sudo pip3.5 install --user --upgrade pipenv
	pipenv --version
	pipenv --python 3.5
	pipenv install
	pipenv shell

shell:
	pipenv shell

server:
	pipenv run ./manage.py migrate
	pipenv run ./manage.py runserver 127.0.0.1:8080

venv: ## Create a virtual env and install test and production requirements
	$(shell which python3) -m venv $(VENV)
	$(VENV)/bin/pip3 install -e .[test]
	$(VENV)/bin/pip3 install -r docs/requirements.txt

##################
# Tests and checks
##################
test: venv ## Run tests
	$(PYTEST)

retest: venv ## Run failed tests only
	$(PYTEST) --lf

coverage: venv ## Generate coverage report
	$(PYTEST) --cov=apps --cov-report=term-missing

lint: ## Run flake8 and isort checks
	flake8 apps/
	flake8 tests/
	isort -c -q --recursive --diff apps/
	isort -c -q --recursive --diff tests/

test_migrations: install-migrations-testing-requirements ## Tests migrations
	cd sandbox && ./test_migrations.sh

