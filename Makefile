VENV = venv
.PHONY: build

all: setup server

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -Rf *.egg-info
	rm -Rf dist/
	rm -Rf build/

##################
# Install commands
##################
install: install-python install-test ## Install requirements for local development and production

install-python: ## Install python requirements
	pip install -r requirements.txt

install-test: ## Install test requirements
	pip install -e .[test]

venv: ## Create a virtual env and install test and production requirements
	$(shell which python3) -m venv $(VENV)
	$(VENV)/bin/pip install -e .[test]

setup:
	pip3 install --user --upgrade pipenv
	pipenv --version
	pipenv --python 3.5
	pipenv install
	pipenv shell

#############################
# Sandbox management commands
#############################
src: install build_src
build_src: src_clean src_load_data

src_clean:
	# Remove media
	-rm -rf src/files/media/images
	-rm -rf src/files/media/cache
	-rm -rf src/files/static
	-rm -f src/db.sqlite
	# Create database
	src/manage.py migrate

src_load_data:
	src/manage.py loaddata src/files/fixtures/data.json

src_image:
	docker build -t nanotek:latest .
##################
# Tests and checks
##################
test: venv ## Run tests
	$(PYTEST)

retest: venv ## Run failed tests only
	$(PYTEST) --lf

coverage: venv ## Generate coverage report
	$(PYTEST) --cov=apps

lint: ## Run flake8 and isort checks
	flake8 apps/
	flake8 tests/
	isort -c -q --recursive --diff apps/
	isort -c -q --recursive --diff tests/

##################
# Misc
##################
shell:
	pipenv shell

server:
	pipenv run ./manage.py migrate
	pipenv run ./manage.py runserver 127.0.0.1:8080
