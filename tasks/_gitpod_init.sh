#!/bin/bash
set -e

. tasks/env.sh

cd ${PROJECT_PATH}
rm -rf node_modules
rm -rf venv-dev

cd ${PROJECT_PATH}
npm install
${SERVERLESS} --version

cd ${PROJECT_PATH}
python3 -m pip install --upgrade pip
pip install --upgrade wheel
pip install -r src/requirements.txt
