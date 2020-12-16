#!/bin/bash

set -e

PROJECT_ROOT_PATH=${PWD}

kill_pid() {
  if [ -f "$1" ];then
    kill `cat $1` || true
    rm $1
  fi
}

# fuck gitpod
unset PIPENV_VENV_IN_PROJECT
unset PIP_USER
unset PYTHONUSERBASE

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/dynamodb.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-static.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-mutable.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-deploygen.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-tmp.pid
rm -rf local-test-tmp

# init local run env
cd ${PROJECT_ROOT_PATH}
mkdir -p local-test-tmp
python3 -m venv local-test-tmp/venv-local-test
. local-test-tmp/venv-local-test/bin/activate
pip install --upgrade pip wheel
pip install yq awscli
pip install -r src/requirements.txt

# download dynamodb local
mkdir -p local-test-tmp
mkdir -p cache
curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz.sha256 -o local-test-tmp/dynamodb_local_latest.tar.gz.sha256
TMP0=`cat local-test-tmp/dynamodb_local_latest.tar.gz.sha256 | awk '{print $1}'`
TMP1=0 ; echo "${TMP0} cache/dynamodb_local_latest.tar.gz" | sha256sum -c - || TMP1=$?
if [ "${TMP1}" != "0" ]; then
  rm -f cache/dynamodb_local_latest.tar.gz
  curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o cache/dynamodb_local_latest.tar.gz
fi
echo "${TMP0} cache/dynamodb_local_latest.tar.gz" | sha256sum -c -
cp cache/dynamodb_local_latest.tar.gz local-test-tmp/

# unzip dynamodb local
mkdir -p ${PROJECT_ROOT_PATH}/local-test-tmp/dynamodb_local
cd ${PROJECT_ROOT_PATH}/local-test-tmp/dynamodb_local
tar -xzvf ${PROJECT_ROOT_PATH}/local-test-tmp/dynamodb_local_latest.tar.gz

# run dynamodb
cd ${PROJECT_ROOT_PATH}/local-test-tmp
java -Djava.library.path=./dynamodb_local/DynamoDBLocal_lib -jar dynamodb_local/DynamoDBLocal.jar -inMemory &
echo $! > dynamodb.pid

# load dynamodb setting
cd ${PROJECT_ROOT_PATH}
#yq -r .provider.region                                          src/serverless.yml | tr -d '\n' > local-test-tmp/region
#echo -n us-east-1 > local-test-tmp/region'
jq -r  .AWS_REGION stages/local/conf.json | tr -d '\n' > local-test-tmp/region
yq -cM .resources.Resources.Db.Properties.AttributeDefinitions   src/serverless.yml | tr -d '\n' > local-test-tmp/db.AttributeDefinitions
yq -cM .resources.Resources.Db.Properties.KeySchema              src/serverless.yml | tr -d '\n' > local-test-tmp/db.KeySchema
yq -cM .resources.Resources.Db.Properties.GlobalSecondaryIndexes src/serverless.yml | tr -d '\n' > local-test-tmp/db.GlobalSecondaryIndexes
yq -r  .resources.Resources.Db.Properties.BillingMode            src/serverless.yml | tr -d '\n' > local-test-tmp/db.BillingMode

# create table
cd ${PROJECT_ROOT_PATH}
aws dynamodb create-table \
    --table-name tmp_table \
    --attribute-definitions file://local-test-tmp/db.AttributeDefinitions \
    --key-schema file://local-test-tmp/db.KeySchema \
    --global-secondary-indexes file://local-test-tmp/db.GlobalSecondaryIndexes \
    --billing-mode file://local-test-tmp/db.BillingMode \
    --endpoint-url http://localhost:8000 \
    --region `cat local-test-tmp/region`
aws dynamodb wait table-exists \
    --table-name tmp_table \
    --endpoint-url http://localhost:8000 \
    --region `cat local-test-tmp/region`

# emulate bucket
cd ${PROJECT_ROOT_PATH}
mkdir local-test-tmp/public-mutable
mkdir local-test-tmp/public-deploygen
mkdir local-test-tmp/public-tmp
mkdir local-test-tmp/private-mutable
mkdir local-test-tmp/private-deploygen
mkdir local-test-tmp/private-tmp
python -m http.server 8100 --directory ${PROJECT_ROOT_PATH}/public-static &
echo $! > local-test-tmp/public-static.pid
python -m http.server 8101 --directory ${PROJECT_ROOT_PATH}/local-test-tmp/public-mutable &
echo $! > local-test-tmp/public-mutable.pid
python -m http.server 8102 --directory ${PROJECT_ROOT_PATH}/local-test-tmp/public-deploygen &
echo $! > local-test-tmp/public-deploygen.pid
python -m http.server 8103 --directory ${PROJECT_ROOT_PATH}/local-test-tmp/public-tmp &
echo $! > local-test-tmp/public-tmp.pid

# environ
export STAGE=local
export CONF_PATH=${PROJECT_ROOT_PATH}/stages/local/conf.json
export PUBLIC_STATIC_PATH=${PROJECT_ROOT_PATH}/public-static
export PUBLIC_DEPLOYGEN_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/public-deploygen
export PUBLIC_MUTABLE_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/public-mutable
export PUBLIC_TMP_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/public-tmp
export PRIVATE_STATIC_PATH=${PROJECT_ROOT_PATH}/private-static
export PRIVATE_DEPLOYGEN_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/private-deploygen
export PRIVATE_MUTABLE_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/private-mutable
export PRIVATE_TMP_PATH=${PROJECT_ROOT_PATH}/local-test-tmp/private-tmp
export DB_TABLE_NAME=tmp_table
export DYNAMODB_ENDPOINT_URL=http://localhost:8000
export DYNAMODB_REGION=`cat ${PROJECT_ROOT_PATH}/local-test-tmp/region`

# local run
cd ${PROJECT_ROOT_PATH}/src
export FLASK_APP=endpoint.py
flask run

cd ${PROJECT_ROOT_PATH}
deactivate
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/dynamodb.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-static.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-mutable.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-deploygen.pid
kill_pid ${PROJECT_ROOT_PATH}/local-test-tmp/public-tmp.pid
rm -rf local-test-tmp
