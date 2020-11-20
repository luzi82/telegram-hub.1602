#!/bin/bash

PROJECT_ROOT_PATH=${PWD}

# init local run env
cd ${PROJECT_ROOT_PATH}
pipenv --three
pipenv install -r src/requirements.txt

# local run
export FLASK_APP=src/endpoint.py
cd ${PROJECT_ROOT_PATH}
pipenv run flask run
