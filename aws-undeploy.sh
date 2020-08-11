#!/bin/bash

set -e

MY_PATH=${PWD}

cd ${MY_PATH}
. _env.sh

cd ${MY_PATH}
rm -rf venv-aws-deploy
rm -rf package-lock.json
rm -rf node_modules

cd ${MY_PATH}
npm install serverless serverless-python-requirements serverless-wsgi
npm update serverless serverless-python-requirements serverless-wsgi
SERVERLESS=${MY_PATH}/node_modules/.bin/serverless
${SERVERLESS} --version

cd ${MY_PATH}
python3 -m venv venv-aws-deploy
. venv-aws-deploy/bin/activate
pip install --upgrade pip wheel
pip install awscli

cd ${MY_PATH}/src
${SERVERLESS} remove

cd ${MY_PATH}
deactivate
rm -rf venv-aws-deploy
rm -rf package-lock.json
rm -rf node_modules
