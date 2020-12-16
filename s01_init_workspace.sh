#!/bin/bash -e

. _env.sh

# clean up
cd ${PROJECT_ROOT_PATH}
rm -rf ${PROJECT_ROOT_PATH}/workspace

# init local run env
cd ${PROJECT_ROOT_PATH}
mkdir -p ${PROJECT_ROOT_PATH}/workspace
python3 -m venv ${PROJECT_ROOT_PATH}/workspace/venv
. ${PROJECT_ROOT_PATH}/workspace/venv/bin/activate
pip install --upgrade pip wheel
pip install yq awscli
pip install -r src/requirements.txt

# download dynamodb local
cd ${PROJECT_ROOT_PATH}
curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o ${PROJECT_ROOT_PATH}/workspace/dynamodb_local_latest.tar.gz
