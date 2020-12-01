#!/bin/bash

. _env.sh

# clean up
cd ${PROJECT_ROOT_PATH}
rm -rf venv-workspace

# init local run env
cd ${PROJECT_ROOT_PATH}
python3 -m venv venv-workspace
. venv-workspace/bin/activate
pip install --upgrade pip wheel
pip install -r src/requirements.txt
