#!/bin/bash -e

. _env.sh

# clean up
cd ${PROJECT_ROOT_PATH}
rm -rf dev

# init local run env
cd ${PROJECT_ROOT_PATH}
python3 -m venv dev/venv
. dev/venv/bin/activate
pip install --upgrade pip wheel
pip install -r src/requirements.txt
