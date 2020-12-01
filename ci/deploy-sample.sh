#!/bin/bash
set -e

export STAGE="ci"

cat ci/public-key.gpg | gpg --import

curl https://raw.githubusercontent.com/luzi82/codelog.flask.ci.secret/master/secret.tar.gz.gpg.sig | \
gpg --decrypt | \
gpg --quiet --batch --yes --decrypt --passphrase="${CI_SECRET}" | \
tar xzf -

. secret/env.sh

cp ci/conf.json conf/conf.json

./aws-deploy.sh
