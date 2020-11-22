#!/bin/bash

set -e

MY_PATH=${PWD}

if [ -z ${STAGE+x} ]; then export STAGE=dev; fi

# fuck gitpod
unset PIPENV_VENV_IN_PROJECT
unset PIP_USER
unset PYTHONUSERBASE

cd ${MY_PATH}
rm -rf venv-aws-deploy
rm -rf node_modules

cd ${MY_PATH}
npm install
SERVERLESS=${MY_PATH}/node_modules/.bin/serverless
${SERVERLESS} --version

cd ${MY_PATH}
python3 -m venv venv-aws-deploy
. venv-aws-deploy/bin/activate
pip install --upgrade pip wheel
pip install awscli
if [[ ! -e ${MY_PATH}/venv-aws-deploy/bin/python3.7 ]]; then
  ln -s ${MY_PATH}/venv-aws-deploy/bin/python3 ${MY_PATH}/venv-aws-deploy/bin/python3.7
fi

# verify if aws credentials are good
aws sts get-caller-identity

cd ${MY_PATH}/src
${SERVERLESS} --stage ${STAGE} create_domain
${SERVERLESS} --stage ${STAGE} deploy

cd ${MY_PATH}
deactivate
rm -rf venv-aws-deploy
rm -rf node_modules
