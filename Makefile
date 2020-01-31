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

##################
# Tests and checks
##################
test:
	pipenv run pytest

coverage: ## Generate coverage report
	pipenv run py.test --cov=oscar --cov-report=term-missing
