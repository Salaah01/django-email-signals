SHELL := /bin/bash
VENV = venv
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_dir_full_path := $(abspath $(current_dir))

# -----------------------------------------------------------------------------
# LOCAL USAGE

# Create a virtual environment
.PHONY: venv
venv:
	python3 -m venv venv
	source venv/bin/activate

# Install dependencies
py-install: requirements.txt
	${PIP} install -r requirements.txt


# Updates the requirements.txt
update-python-pkgs:
	pip-compile requirements.in

node-install:
	npm install

# Runs migrations and runs the local development server
runserver: py-install
	${PYTHON} email_signals/manage.py migrate
	${PYTHON} email_signals/manage.py runserver

# Runs tests
test: py-install
	${PYTHON} runtests.py

# Runs formatter
format: py-install
	${PYTHON} -m black email_signals/.

# Runs linter
lint: py-install
	${PYTHON} -m flake8 --exclude=migrations email_signals/.

# Builds node packages
build-node: node-install
	npm run build

# Builds the package ready for deployment
build-package:
	${PYTHON} setup.py sdist bdist_wheel

# Uploads the package to PyPI
upload-package:
	${PYTHON} -m twine upload dist/*
