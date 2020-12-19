#!/bin/bash -e

. _env.sh

MY_TMP_DIR_PATH=${PROJECT_ROOT_PATH}/dev.local.tmp

export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${MY_TMP_DIR_PATH}/dynamodb.pid
kill_pid ${MY_TMP_DIR_PATH}/public-static.pid
kill_pid ${MY_TMP_DIR_PATH}/public-mutable.pid
kill_pid ${MY_TMP_DIR_PATH}/public-deploygen.pid
kill_pid ${MY_TMP_DIR_PATH}/public-tmp.pid
rm -rf ${MY_TMP_DIR_PATH}
mkdir -p ${MY_TMP_DIR_PATH}

# activate venv
. ${PROJECT_ROOT_PATH}/dev_env/venv/bin/activate

# update dynamodb local
mkdir -p ${MY_TMP_DIR_PATH}
curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz.sha256 -o ${MY_TMP_DIR_PATH}/dynamodb_local_latest.tar.gz.sha256
TMP0=`cat ${MY_TMP_DIR_PATH}/dynamodb_local_latest.tar.gz.sha256 | awk '{print $1}'`
TMP1=1 ; echo "${TMP0} ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz" | sha256sum -c - || TMP1=$?
if [ "${TMP1}" != "0" ]; then
  rm -f ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz
  curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz
fi
echo "${TMP0} ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz" | sha256sum -c -

# unzip dynamodb local
cd ${PROJECT_ROOT_PATH}
mkdir -p ${MY_TMP_DIR_PATH}/dynamodb_local
cd ${MY_TMP_DIR_PATH}/dynamodb_local
tar -xzvf ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz

# run dynamodb local
cd ${MY_TMP_DIR_PATH}
java -Djava.library.path=./dynamodb_local/DynamoDBLocal_lib -jar dynamodb_local/DynamoDBLocal.jar -inMemory &
echo $! > dynamodb.pid

# load dynamodb setting
cd ${PROJECT_ROOT_PATH}
jq -r  .AWS_REGION ${PROJECT_ROOT_PATH}/stages/local/conf.json | tr -d '\n' > ${MY_TMP_DIR_PATH}/region
yq -cM .resources.Resources.Db.Properties.AttributeDefinitions   ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${MY_TMP_DIR_PATH}/db.AttributeDefinitions
yq -cM .resources.Resources.Db.Properties.KeySchema              ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${MY_TMP_DIR_PATH}/db.KeySchema
yq -cM .resources.Resources.Db.Properties.GlobalSecondaryIndexes ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${MY_TMP_DIR_PATH}/db.GlobalSecondaryIndexes
yq -r  .resources.Resources.Db.Properties.BillingMode            ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${MY_TMP_DIR_PATH}/db.BillingMode

# create table
cd ${PROJECT_ROOT_PATH}
aws dynamodb create-table \
    --table-name tmp_table \
    --attribute-definitions file://${MY_TMP_DIR_PATH}/db.AttributeDefinitions \
    --key-schema file://${MY_TMP_DIR_PATH}/db.KeySchema \
    --global-secondary-indexes file://${MY_TMP_DIR_PATH}/db.GlobalSecondaryIndexes \
    --billing-mode file://${MY_TMP_DIR_PATH}/db.BillingMode \
    --endpoint-url http://localhost:8000 \
    --region `cat ${MY_TMP_DIR_PATH}/region`
aws dynamodb wait table-exists \
    --table-name tmp_table \
    --endpoint-url http://localhost:8000 \
    --region `cat ${MY_TMP_DIR_PATH}/region`

# emulate bucket
cd ${PROJECT_ROOT_PATH}
mkdir ${MY_TMP_DIR_PATH}/public-mutable
mkdir ${MY_TMP_DIR_PATH}/public-deploygen
mkdir ${MY_TMP_DIR_PATH}/public-tmp
mkdir ${MY_TMP_DIR_PATH}/private-mutable
mkdir ${MY_TMP_DIR_PATH}/private-deploygen
mkdir ${MY_TMP_DIR_PATH}/private-tmp
python -m http.server 8100 --directory ${PROJECT_ROOT_PATH}/public-static &
echo $! > ${MY_TMP_DIR_PATH}/public-static.pid
python -m http.server 8101 --directory ${MY_TMP_DIR_PATH}/public-mutable &
echo $! > ${MY_TMP_DIR_PATH}/public-mutable.pid
python -m http.server 8102 --directory ${MY_TMP_DIR_PATH}/public-deploygen &
echo $! > ${MY_TMP_DIR_PATH}/public-deploygen.pid
python -m http.server 8103 --directory ${MY_TMP_DIR_PATH}/public-tmp &
echo $! > ${MY_TMP_DIR_PATH}/public-tmp.pid

# load env var
export STAGE=local
export CONF_PATH=${PROJECT_ROOT_PATH}/stages/local/conf.json
export PUBLIC_STATIC_PATH=${PROJECT_ROOT_PATH}/public-static
export PUBLIC_DEPLOYGEN_PATH=${MY_TMP_DIR_PATH}/public-deploygen
export PUBLIC_MUTABLE_PATH=${MY_TMP_DIR_PATH}/public-mutable
export PUBLIC_TMP_PATH=${MY_TMP_DIR_PATH}/public-tmp
export PRIVATE_STATIC_PATH=${PROJECT_ROOT_PATH}/private-static
export PRIVATE_DEPLOYGEN_PATH=${MY_TMP_DIR_PATH}/private-deploygen
export PRIVATE_MUTABLE_PATH=${MY_TMP_DIR_PATH}/private-mutable
export PRIVATE_TMP_PATH=${MY_TMP_DIR_PATH}/private-tmp
export DB_TABLE_NAME=tmp_table
export DYNAMODB_ENDPOINT_URL=http://localhost:8000
export DYNAMODB_REGION=`cat ${MY_TMP_DIR_PATH}/region`

# local run
cd ${PROJECT_ROOT_PATH}/src
export FLASK_APP=${PROJECT_ROOT_PATH}/src/endpoint.py
${PROJECT_ROOT_PATH}/dev_env/venv/bin/flask run

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${MY_TMP_DIR_PATH}/dynamodb.pid
kill_pid ${MY_TMP_DIR_PATH}/public-static.pid
kill_pid ${MY_TMP_DIR_PATH}/public-mutable.pid
kill_pid ${MY_TMP_DIR_PATH}/public-deploygen.pid
kill_pid ${MY_TMP_DIR_PATH}/public-tmp.pid
rm -rf ${MY_TMP_DIR_PATH}
