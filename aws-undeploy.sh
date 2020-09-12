#!/bin/bash

set -e

MY_PATH=${PWD}

cd ${MY_PATH}
rm -rf venv-aws-undeploy
rm -rf node_modules

cd ${MY_PATH}
npm install
SERVERLESS=${MY_PATH}/node_modules/.bin/serverless
${SERVERLESS} --version

cd ${MY_PATH}
python3 -m venv venv-aws-undeploy
. venv-aws-undeploy/bin/activate
pip install --upgrade pip wheel
pip install awscli

cd ${MY_PATH}/src
${SERVERLESS} remove
${SERVERLESS} delete_domain

cd ${MY_PATH}
deactivate
rm -rf venv-aws-undeploy
rm -rf node_modules
