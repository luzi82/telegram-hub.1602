#!/bin/bash -e

. _env.sh

# reset tmp
cd ${PROJECT_ROOT_PATH}
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.tmp.pid
rm -rf ${LOCAL_TMP_DIR_PATH}
mkdir -p ${LOCAL_TMP_DIR_PATH}

# activate venv
. ${PROJECT_ROOT_PATH}/dev_env/venv/bin/activate

# flake8
cd ${PROJECT_ROOT_PATH}
flake8 \
  ${PROJECT_ROOT_PATH}/src \
  --count \
  --select=E9,F63,F7,F82 \
  --show-source \
  --statistics
mypy \
  --strict \
  ${PROJECT_ROOT_PATH}/src

export STAGE=${UNITTEST_STAGE}

export CONF_PATH=''
export PUBLIC_COMPUTE_URL_PREFIX=''
export PUBLIC_STATIC_URL_PREFIX=''
export PUBLIC_DEPLOYGEN_URL_PREFIX=''
export PUBLIC_MUTABLE_URL_PREFIX=''
export PUBLIC_TMP_URL_PREFIX=''
export PUBLIC_STATIC_PATH=''
export PUBLIC_DEPLOYGEN_PATH=''
export PUBLIC_MUTABLE_PATH=''
export PUBLIC_TMP_PATH=''
export PRIVATE_STATIC_PATH=''
export PRIVATE_DEPLOYGEN_PATH=''
export PRIVATE_MUTABLE_PATH=''
export PRIVATE_TMP_PATH=''

export DB_TABLE_NAME=${UNITTEST_DYNAMODB_TABLE_NAME}
export DYNAMODB_ENDPOINT_URL=${UNITTEST_DYNAMODB_ENDPOINT_URL}
export DYNAMODB_REGION=${UNITTEST_DYNAMODB_REGION}

export AWS_ACCESS_KEY_ID=${LOCAL_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${LOCAL_AWS_SECRET_ACCESS_KEY}

# run dynamodb local
cd ${PROJECT_ROOT_PATH}
mkdir -p ${LOCAL_TMP_DIR_PATH}/dynamodb.data
java \
  -Djava.library.path=${PROJECT_ROOT_PATH}/dev_env/dynamodb_local/DynamoDBLocal_lib \
  -jar ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local/DynamoDBLocal.jar \
  -port ${UNITTEST_DYNAMODB_PORT} \
  -dbPath ${LOCAL_TMP_DIR_PATH}/dynamodb.data \
  &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.tmp.pid

# create table
cd ${PROJECT_ROOT_PATH}
aws dynamodb create-table \
    --table-name ${UNITTEST_DYNAMODB_TABLE_NAME} \
    --attribute-definitions file://${LOCAL_VAR_DIR_PATH}/init/db.AttributeDefinitions \
    --key-schema file://${LOCAL_VAR_DIR_PATH}/init/db.KeySchema \
    --global-secondary-indexes file://${LOCAL_VAR_DIR_PATH}/init/db.GlobalSecondaryIndexes \
    --billing-mode file://${LOCAL_VAR_DIR_PATH}/init/db.BillingMode \
    --endpoint-url "${UNITTEST_DYNAMODB_ENDPOINT_URL}" \
    --region "${UNITTEST_DYNAMODB_REGION}" \
    > ${LOCAL_VAR_DIR_PATH}/dynamodb.tmp.create-table.log
aws dynamodb wait table-exists \
    --table-name ${UNITTEST_DYNAMODB_TABLE_NAME} \
    --endpoint-url "${UNITTEST_DYNAMODB_ENDPOINT_URL}" \
    --region "${UNITTEST_DYNAMODB_REGION}" \
    > ${LOCAL_VAR_DIR_PATH}/dynamodb.tmp.wait.table-exists.log

# run test
cd ${PROJECT_ROOT_PATH}
python3 unit_test/db_test.py

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.tmp.pid
rm -rf ${LOCAL_TMP_DIR_PATH}
