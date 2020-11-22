#!/bin/bash

set -e

bad_exit(){
    echo "${0} stage"
    exit 1
}

# args
ARG_STAGE=${1}
if [ ! -f "stages/${ARG_STAGE}/conf.json" ]; then
    bad_exit
fi

MY_PATH=${PWD}

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

cd ${MY_PATH}/src
${SERVERLESS} create_domain --stage ${ARG_STAGE}
${SERVERLESS} deploy --stage ${ARG_STAGE} -v

cd ${MY_PATH}
deactivate
rm -rf venv-aws-deploy
rm -rf node_modules
