#!/bin/bash
set -e

TMP_FILE=`mktemp`
trap "{ rm -f ${TMP_FILE}; }" EXIT

curl https://raw.githubusercontent.com/luzi82/codelog.web-template.1601.secret/sample-ci/secret.tar.gz.gpg.sig -o ${TMP_FILE}
gpg --no-default-keyring --keyring ${PWD}/ci/sample-public-key.gpg --verify ${TMP_FILE}
gpg --no-default-keyring --keyring ${PWD}/ci/sample-public-key.gpg --decrypt ${TMP_FILE} | \
gpg --quiet --batch --yes --decrypt --passphrase="${SAMPLE_CI_SECRET}" | \
tar xzf -

. secret/env.sh

./aws-deploy.sh sample
