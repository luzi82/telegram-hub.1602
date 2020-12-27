#!/bin/bash -e

. _env.sh

# reset dev_env
cd ${PROJECT_ROOT_PATH}
rm -rf ${PROJECT_ROOT_PATH}/dev_env
mkdir -p ${PROJECT_ROOT_PATH}/dev_env

# create var
mkdir -p ${LOCAL_VAR_DIR_PATH}
mkdir -p ${LOCAL_VAR_DIR_PATH}/init
mkdir -p ${LOCAL_VAR_DIR_PATH}/pid

# init local run env
cd ${PROJECT_ROOT_PATH}
python3 -m venv ${PROJECT_ROOT_PATH}/dev_env/venv
. ${PROJECT_ROOT_PATH}/dev_env/venv/bin/activate
pip install --upgrade pip wheel
pip install awscli flake8 mypy yq
pip install -r ${PROJECT_ROOT_PATH}/src/requirements.txt

# download dynamodb local
cd ${PROJECT_ROOT_PATH}
curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz

# unzip dynamodb local
cd ${PROJECT_ROOT_PATH}/dev_env
mkdir -p ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local
cd ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local
tar -xzf ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz

# run dynamodb local
cd ${PROJECT_ROOT_PATH}
mkdir -p ${LOCAL_VAR_DIR_PATH}/dynamodb.data
java \
  -Djava.library.path=${PROJECT_ROOT_PATH}/dev_env/dynamodb_local/DynamoDBLocal_lib \
  -jar ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local/DynamoDBLocal.jar \
  -port ${LOCAL_DYNAMODB_PORT} \
  -dbPath ${LOCAL_VAR_DIR_PATH}/dynamodb.data \
  &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.pid

# load dynamodb setting
cd ${PROJECT_ROOT_PATH}
yq -cM .resources.Resources.Db.Properties.AttributeDefinitions   ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_VAR_DIR_PATH}/init/db.AttributeDefinitions
yq -cM .resources.Resources.Db.Properties.KeySchema              ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_VAR_DIR_PATH}/init/db.KeySchema
yq -cM .resources.Resources.Db.Properties.GlobalSecondaryIndexes ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_VAR_DIR_PATH}/init/db.GlobalSecondaryIndexes
yq -r  .resources.Resources.Db.Properties.BillingMode            ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_VAR_DIR_PATH}/init/db.BillingMode

# for runtime
export AWS_ACCESS_KEY_ID=${LOCAL_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${LOCAL_AWS_SECRET_ACCESS_KEY}

# create table
cd ${PROJECT_ROOT_PATH}
aws dynamodb create-table \
    --table-name ${LOCAL_DYNAMODB_TABLE_NAME} \
    --attribute-definitions file://${LOCAL_VAR_DIR_PATH}/init/db.AttributeDefinitions \
    --key-schema file://${LOCAL_VAR_DIR_PATH}/init/db.KeySchema \
    --global-secondary-indexes file://${LOCAL_VAR_DIR_PATH}/init/db.GlobalSecondaryIndexes \
    --billing-mode file://${LOCAL_VAR_DIR_PATH}/init/db.BillingMode \
    --endpoint-url "${LOCAL_DYNAMODB_ENDPOINT_URL}" \
    --region "${LOCAL_DYNAMODB_REGION}" \
    > ${LOCAL_VAR_DIR_PATH}/dynamodb.create-table.log
aws dynamodb wait table-exists \
    --table-name ${LOCAL_DYNAMODB_TABLE_NAME} \
    --endpoint-url "${LOCAL_DYNAMODB_ENDPOINT_URL}" \
    --region "${LOCAL_DYNAMODB_REGION}" \
    > ${LOCAL_VAR_DIR_PATH}/dynamodb.wait.table-exists.log

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.pid
