#!/bin/bash -e

. _env.sh

bad_exit(){
    echo "${0} stage"
    exit 1
}

# args
ARG_STAGE=${1}
if [ ! -f "stages/${ARG_STAGE}/conf.json" ]; then
    bad_exit
fi

STAGE=${ARG_STAGE}

# init env
MY_TMP_DIR_PATH=${PROJECT_ROOT_PATH}/deploygen.tmp
rm -rf ${MY_TMP_DIR_PATH}
mkdir -p ${MY_TMP_DIR_PATH}/public
mkdir -p ${MY_TMP_DIR_PATH}/private

# real operation here
TIMESTAMP=`date +%s`
echo ${TIMESTAMP} > ${MY_TMP_DIR_PATH}/public/TIMESTAMP.txt
echo ${TIMESTAMP} > ${MY_TMP_DIR_PATH}/private/TIMESTAMP.txt

echo ${STAGE} > ${MY_TMP_DIR_PATH}/public/STAGE.txt
echo ${STAGE} > ${MY_TMP_DIR_PATH}/private/STAGE.txt
