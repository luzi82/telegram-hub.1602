#!/bin/bash

. _env.sh

. ${PROJECT_ROOT_PATH}/venv-workspace/bin/activate

cd ${PROJECT_ROOT_PATH}/src
export FLASK_APP=${PROJECT_ROOT_PATH}/src/endpoint.py
flask run
