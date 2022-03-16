VENV = venv
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_dir_full_path := $(abspath $(current_dir))

# -----------------------------------------------------------------------------
# LOCAL USAGE

# Create a virtual environment
venv:
	python3 -m venv venv

# Install dependencies
py-install: venv email_signals/requirements.txt email_signals/requirements.dev.txt package.json package-lock.json
	${PIP} install -r email_signals/requirements.txt
	${PIP} install -r email_signals/requirements.dev.txt

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
build: node-install
	npm run build
