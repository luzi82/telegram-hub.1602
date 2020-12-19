#!/bin/bash -e

TMP_DIR=`mktemp -d`
trap 'rm -rf "${TMP_DIR}"' EXIT

curl https://raw.githubusercontent.com/luzi82/codelog.web-template.1601.secret/sample-ci/secret.tar.gz.gpg.sig \
  -o ${TMP_DIR}/secret.tar.gz.gpg.sig

gpg --no-default-keyring --keyring ci/sample-public-key.gpg --verify ${TMP_DIR}/secret.tar.gz.gpg.sig

gpg --no-default-keyring --keyring ci/sample-public-key.gpg --decrypt ${TMP_DIR}/secret.tar.gz.gpg.sig | \
gpg --quiet --batch --yes --decrypt --passphrase="${SAMPLE_CI_SECRET}" | \
tar xzf -

. secret/env.sh

./s50_aws_init_env.sh
./s51_aws_deploy.sh sample
