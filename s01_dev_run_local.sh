#!/bin/bash -e

. _env.sh

#LOCAL_PUBLIC_COMPUTE_PORT=${LOCAL_LOCAL_PUBLIC_COMPUTE_PORT}
#LOCAL_PUBLIC_STATIC_PORT=${LOCAL_LOCAL_PUBLIC_STATIC_PORT}
#LOCAL_PUBLIC_DEPLOYGEN_PORT=${LOCAL_LOCAL_PUBLIC_DEPLOYGEN_PORT}
#LOCAL_PUBLIC_MUTABLE_PORT=${LOCAL_LOCAL_PUBLIC_MUTABLE_PORT}
#LOCAL_PUBLIC_TMP_PORT=${LOCAL_LOCAL_PUBLIC_TMP_PORT}

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-static.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-mutable.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-deploygen.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-tmp.pid
rm -rf ${LOCAL_TMP_DIR_PATH}
mkdir -p ${LOCAL_TMP_DIR_PATH}

# activate venv
. ${PROJECT_ROOT_PATH}/dev_env/venv/bin/activate

# load env var
export STAGE=${LOCAL_STAGE}
export CONF_PATH=${LOCAL_CONF_PATH}
if [ -z ${GITPOD_REPO_ROOT+x} ]; then
  export PUBLIC_COMPUTE_URL_PREFIX="http://localhost:${LOCAL_PUBLIC_COMPUTE_PORT}"
  export PUBLIC_STATIC_URL_PREFIX="http://localhost:${LOCAL_PUBLIC_STATIC_PORT}"
  export PUBLIC_DEPLOYGEN_URL_PREFIX="http://localhost:${LOCAL_PUBLIC_DEPLOYGEN_PORT}"
  export PUBLIC_MUTABLE_URL_PREFIX="http://localhost:${LOCAL_PUBLIC_MUTABLE_PORT}"
  export PUBLIC_TMP_URL_PREFIX="http://localhost:${LOCAL_PUBLIC_TMP_PORT}"
else
  export PUBLIC_COMPUTE_URL_PREFIX=`gp url ${LOCAL_PUBLIC_COMPUTE_PORT}`
  export PUBLIC_STATIC_URL_PREFIX=`gp url ${LOCAL_PUBLIC_STATIC_PORT}`
  export PUBLIC_DEPLOYGEN_URL_PREFIX=`gp url ${LOCAL_PUBLIC_DEPLOYGEN_PORT}`
  export PUBLIC_MUTABLE_URL_PREFIX=`gp url ${LOCAL_PUBLIC_MUTABLE_PORT}`
  export PUBLIC_TMP_URL_PREFIX=`gp url ${LOCAL_PUBLIC_TMP_PORT}`
fi
export PUBLIC_STATIC_PATH=${PROJECT_ROOT_PATH}/public-static
export PUBLIC_DEPLOYGEN_PATH=${PROJECT_ROOT_PATH}/deploygen.tmp/public
export PUBLIC_MUTABLE_PATH=${LOCAL_VAR_DIR_PATH}/public-mutable
export PUBLIC_TMP_PATH=${LOCAL_TMP_DIR_PATH}/public-tmp
export PRIVATE_STATIC_PATH=${PROJECT_ROOT_PATH}/private-static
export PRIVATE_DEPLOYGEN_PATH=${PROJECT_ROOT_PATH}/deploygen.tmp/private
export PRIVATE_MUTABLE_PATH=${LOCAL_VAR_DIR_PATH}/private-mutable
export PRIVATE_TMP_PATH=${LOCAL_TMP_DIR_PATH}/private-tmp
export DB_TABLE_NAME=${LOCAL_DYNAMODB_TABLE_NAME}
export DYNAMODB_ENDPOINT_URL=${LOCAL_DYNAMODB_ENDPOINT_URL}
export DYNAMODB_REGION=${LOCAL_DYNAMODB_REGION}

# reset tmp
rm -rf ${LOCAL_TMP_DIR_PATH}
mkdir -p ${LOCAL_TMP_DIR_PATH}

# # update dynamodb local
# curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz.sha256 -o ${LOCAL_TMP_DIR_PATH}/dynamodb_local_latest.tar.gz.sha256
# TMP0=`cat ${LOCAL_TMP_DIR_PATH}/dynamodb_local_latest.tar.gz.sha256 | awk '{print $1}'`
# TMP1=1 ; echo "${TMP0} ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz" | sha256sum -c - || TMP1=$?
# if [ "${TMP1}" != "0" ]; then
#   rm -f ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz
#   curl https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz
# fi
# echo "${TMP0} ${PROJECT_ROOT_PATH}/dev_env/dynamodb_local_latest.tar.gz" | sha256sum -c -

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

# # load dynamodb setting
# cd ${PROJECT_ROOT_PATH}
# yq -cM .resources.Resources.Db.Properties.AttributeDefinitions   ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_TMP_DIR_PATH}/db.AttributeDefinitions
# yq -cM .resources.Resources.Db.Properties.KeySchema              ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_TMP_DIR_PATH}/db.KeySchema
# yq -cM .resources.Resources.Db.Properties.GlobalSecondaryIndexes ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_TMP_DIR_PATH}/db.GlobalSecondaryIndexes
# yq -r  .resources.Resources.Db.Properties.BillingMode            ${PROJECT_ROOT_PATH}/aws/serverless.yml | tr -d '\n' > ${LOCAL_TMP_DIR_PATH}/db.BillingMode

# # create table
# cd ${PROJECT_ROOT_PATH}
# aws dynamodb create-table \
#     --table-name tmp_table \
#     --attribute-definitions file://${LOCAL_TMP_DIR_PATH}/db.AttributeDefinitions \
#     --key-schema file://${LOCAL_TMP_DIR_PATH}/db.KeySchema \
#     --global-secondary-indexes file://${LOCAL_TMP_DIR_PATH}/db.GlobalSecondaryIndexes \
#     --billing-mode file://${LOCAL_TMP_DIR_PATH}/db.BillingMode \
#     --endpoint-url "${DYNAMODB_ENDPOINT_URL}" \
#     --region "${LOCAL_DYNAMODB_REGION}" \
#     > ${LOCAL_TMP_DIR_PATH}/dynamodb.create-table.log
# aws dynamodb wait table-exists \
#     --table-name tmp_table \
#     --endpoint-url "${DYNAMODB_ENDPOINT_URL}" \
#     --region "${LOCAL_DYNAMODB_REGION}" \
#     > ${LOCAL_TMP_DIR_PATH}/dynamodb.wait.table-exists.log

# deploygen
cd ${PROJECT_ROOT_PATH}
${PROJECT_ROOT_PATH}/_gen_deploygen.sh ${LOCAL_STAGE}

# emulate bucket
cd ${PROJECT_ROOT_PATH}
mkdir -p ${PUBLIC_MUTABLE_PATH}
mkdir -p ${PUBLIC_TMP_PATH}
mkdir -p ${PRIVATE_MUTABLE_PATH}
mkdir -p ${PRIVATE_TMP_PATH}
python -m http.server ${LOCAL_PUBLIC_STATIC_PORT}    --directory ${PUBLIC_STATIC_PATH} &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/public-static.pid
python -m http.server ${LOCAL_PUBLIC_DEPLOYGEN_PORT} --directory ${PUBLIC_DEPLOYGEN_PATH} &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/public-deploygen.pid
python -m http.server ${LOCAL_PUBLIC_MUTABLE_PORT}   --directory ${PUBLIC_MUTABLE_PATH} &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/public-mutable.pid
python -m http.server ${LOCAL_PUBLIC_TMP_PORT}       --directory ${PUBLIC_TMP_PATH} &
echo $! > ${LOCAL_VAR_DIR_PATH}/pid/public-tmp.pid

# local run
cd ${PROJECT_ROOT_PATH}/src
export AWS_ACCESS_KEY_ID=${LOCAL_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${LOCAL_AWS_SECRET_ACCESS_KEY}
export FLASK_RUN_PORT=${LOCAL_PUBLIC_COMPUTE_PORT}
export FLASK_DEBUG=1
export FLASK_APP=${PROJECT_ROOT_PATH}/src/endpoint.py
export FUTSU_GCP_ENABLE=0
${PROJECT_ROOT_PATH}/dev_env/venv/bin/flask run --host 0.0.0.0

# clean up
cd ${PROJECT_ROOT_PATH}
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/dynamodb.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-static.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-mutable.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-deploygen.pid
kill_pid ${LOCAL_VAR_DIR_PATH}/pid/public-tmp.pid
rm -rf ${LOCAL_TMP_DIR_PATH}
