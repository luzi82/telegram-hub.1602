#!/bin/bash

PROJECT_ROOT_PATH=${PWD}

# fuck gitpod
unset PIPENV_VENV_IN_PROJECT
unset PIP_USER
unset PYTHONUSERBASE

# clean up
cd ${PROJECT_ROOT_PATH}
rm -rf venv-local-test

# init local run env
cd ${PROJECT_ROOT_PATH}
python3 -m venv venv-local-test
. venv-local-test/bin/activate
pip install --upgrade pip wheel
pip install -r src/requirements.txt

# local run
cd ${PROJECT_ROOT_PATH}/src
export FLASK_APP=endpoint.py
flask run
